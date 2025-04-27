# -*- coding: utf-8 -*-
"""
Author: Harsha Krishnareddy
Email: c0mpiler@ins8s.dev
"""
"""Core authentication logic using Keycloak, YAML config, and Keyring."""

import json
import logging
import random  # For jitter
import time
from typing import Any, Callable, Dict, Optional, TypeVar

import keyring
import requests
import urllib3
from jose import jwt as jose_jwt
from jose.exceptions import ExpiredSignatureError, JOSEError, JWTError
from requests.exceptions import ConnectionError, RequestException, SSLError, Timeout
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from urllib3.exceptions import InsecureRequestWarning

# Use relative import for config within the same package
from . import config

# --- Logging Setup --- #
# Get logger configured in config.py
logger = logging.getLogger(__name__)
console = Console()

# --- Disable InsecureRequestWarning --- #
# This check happens after config is loaded
if config.get_config_value("ssl_verify") is False:
    logger.debug("Disabling InsecureRequestWarning due to ssl_verify=False")
    urllib3.disable_warnings(InsecureRequestWarning)

# --- Constants --- #
# Retry settings for network requests
RETRYABLE_STATUS_CODES = {500, 502, 503, 504}
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0  # seconds
BACKOFF_FACTOR = 2
MAX_BACKOFF = 10.0  # seconds
JITTER_FACTOR = 0.3  # +/- 30% jitter

# Type variable for retry decorator
T = TypeVar("T")


# --- Network Request Retry Logic --- #
def _retry_network_call(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Adds retry logic with exponential backoff and jitter to network calls."""
    attempt = 0
    backoff = INITIAL_BACKOFF
    while True:
        attempt += 1
        try:
            return func(*args, **kwargs)
        except (ConnectionError, Timeout, SSLError) as e:
            # Retry on common network/SSL errors
            error_type = type(e).__name__
            logger.warning(
                f"Network error ({error_type}) during call (attempt {attempt}/{MAX_RETRIES}): {e}"
            )
            if attempt >= MAX_RETRIES:
                logger.error(f"Max retries ({MAX_RETRIES}) exceeded for {error_type}.")
                raise
        except RequestException as e:
            # Retry on specific HTTP status codes for other request errors
            status_code = e.response.status_code if e.response is not None else None
            if status_code in RETRYABLE_STATUS_CODES:
                logger.warning(
                    f"HTTP error {status_code} during call (attempt {attempt}/{MAX_RETRIES}), retrying..."
                )
                if attempt >= MAX_RETRIES:
                    logger.error(
                        f"Max retries ({MAX_RETRIES}) exceeded for HTTP {status_code}."
                    )
                    raise
            else:
                # Don't retry on other HTTP errors (like 4xx)
                raise
        except Exception:
            # Don't retry on unexpected errors
            raise

        # --- Calculate backoff with jitter --- #
        sleep_time = backoff + random.uniform(
            -JITTER_FACTOR * backoff, JITTER_FACTOR * backoff
        )
        sleep_time = max(0.1, sleep_time)  # Ensure minimum sleep time
        logger.info(f"Retrying in {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

        # Increase backoff for next retry
        backoff = min(MAX_BACKOFF, backoff * BACKOFF_FACTOR)


# --- Cached Public Keys --- #
_public_keys: Optional[Dict[str, Any]] = None
_jwks_uri: Optional[str] = None


# --- Keyring Storage --- #
def _get_keyring_service_name() -> str:
    """Gets the keyring service name from config."""
    return config.get_config_value("keyring_service_name", "novactl")


def _get_keyring_username() -> str:
    """Gets the keyring username (derived in config) from config."""
    # Relies on load_config() deriving this value
    return config.get_config_value("keyring_username", "novactl_tokens")


def _save_tokens(tokens: Dict[str, Any]):
    """Saves the token dictionary to the system keyring."""
    service = _get_keyring_service_name()
    username = _get_keyring_username()
    try:
        keyring.set_password(service, username, json.dumps(tokens))
        logger.info(
            f"Tokens saved to keyring service '{service}' for username '{username}'"
        )
    except Exception:
        logger.exception(
            f"Failed to save tokens to keyring",
            extra={"service": service, "username": username},
        )
        console.print(
            "[bold yellow]Warning:[/bold yellow] Could not save tokens securely. Session may not persist."
        )


def _load_tokens() -> Optional[Dict[str, Any]]:
    """Loads the token dictionary from the system keyring."""
    service = _get_keyring_service_name()
    username = _get_keyring_username()
    try:
        token_json = keyring.get_password(service, username)
        if token_json:
            tokens = json.loads(token_json)
            logger.debug("Tokens loaded from keyring.")
            return tokens
        logger.debug("No tokens found in keyring.")
        return None
    except Exception:
        logger.exception(
            f"Failed to load tokens from keyring",
            extra={"service": service, "username": username},
        )
        console.print(
            "[bold yellow]Warning:[/bold yellow] Could not load tokens from storage."
        )
        return None


def _clear_tokens():
    """Deletes tokens from the system keyring."""
    service = _get_keyring_service_name()
    username = _get_keyring_username()
    try:
        # Import dynamically to avoid hard dependency if keyring has issues
        from keyring.errors import PasswordDeleteError

        keyring.delete_password(service, username)
        logger.info("Tokens deleted from keyring.")
    except PasswordDeleteError:
        logger.debug("No tokens found in keyring to delete.")
    except Exception:
        logger.exception(
            f"Failed to delete tokens from keyring",
            extra={"service": service, "username": username},
        )
        console.print(
            "[bold yellow]Warning:[/bold yellow] Could not clear tokens from storage."
        )


# --- Token Validation --- #
def _get_public_keys() -> Dict[str, Any]:
    """Fetches and caches JWKS public keys from the configured endpoint."""
    global _public_keys, _jwks_uri
    # Reload config values inside function in case config changes
    _jwks_uri = config.get_config_value("oidc_jwks_uri")
    ssl_verify = config.get_config_value("ssl_verify", True)

    if _public_keys is None:
        if not _jwks_uri:
            logger.critical("JWKS URI is not configured. Cannot fetch public keys.")
            raise ValueError("JWKS URI missing in configuration.")

        try:
            logger.debug(f"Fetching public keys from {_jwks_uri}")
            response = _retry_network_call(
                requests.get, _jwks_uri, timeout=10, verify=ssl_verify
            )
            response.raise_for_status()
            jwks = response.json()
            _public_keys = {key["kid"]: key for key in jwks["keys"]}
            logger.debug(
                f"Successfully fetched and cached {len(_public_keys)} public keys."
            )
        except (JOSEError, RequestException, json.JSONDecodeError, KeyError) as e:
            # Log specific errors caught during fetch/parse
            logger.critical(
                f"Failed to get or parse public keys from {_jwks_uri}: {e}",
                exc_info=True,
            )
            raise JOSEError(f"Could not fetch/parse public keys: {e}") from e
        except Exception as e:
            # Catch any other unexpected error
            logger.critical("Unexpected error fetching public keys.", exc_info=True)
            raise JOSEError("Unexpected error fetching public keys.") from e

    return _public_keys


def _decode_and_validate_token(
    token: str, token_type: str = "access", access_token: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Decodes and validates a JWT token (signature, expiry, issuer, audience, at_hash)."""
    if not token:
        return None

    cfg = config.load_config()  # Ensure latest config
    leeway = cfg.get("token_leeway_seconds", 60)
    expected_issuer = cfg.get("oidc_issuer")
    client_id = cfg.get("keycloak_client_id")
    audience = client_id

    if not expected_issuer or not client_id:
        logger.error("Issuer or Client ID missing from config for validation.")
        return None

    try:
        public_keys = _get_public_keys()  # This handles its own retries
        unverified_headers = jose_jwt.get_unverified_headers(token)
        kid = unverified_headers.get("kid")
        if not kid:
            raise JWTError("Token header missing 'kid'.")

        public_key = public_keys.get(kid)
        if not public_key:
            logger.warning(
                f"Public key for kid '{kid}' not found in current JWKS. Refetching keys..."
            )
            global _public_keys
            _public_keys = None  # Clear cache
            public_keys = _get_public_keys()  # Try fetching again
            public_key = public_keys.get(kid)
            if not public_key:
                raise JWTError(f"Unknown key ID '{kid}' after refetching JWKS.")

        # Determine if at_hash validation should be attempted
        # It's only relevant when validating an ID token and the corresponding access token is provided
        should_verify_at_hash = token_type.lower() == "id" and access_token is not None

        options = {
            "verify_signature": True,
            "verify_aud": True,
            "verify_iss": True,
            "verify_exp": True,
            "verify_at_hash": should_verify_at_hash,  # Re-enabled: Verify if ID token and access token are present
            "leeway": leeway,
        }

        # Pass the access_token parameter to jose_jwt.decode ONLY if verifying at_hash
        at_hash_access_token_arg = access_token if should_verify_at_hash else None

        decoded_payload = jose_jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=audience,
            issuer=expected_issuer,
            access_token=at_hash_access_token_arg,  # Pass only when needed for at_hash
            options=options,
        )
        logger.debug(f"{token_type.capitalize()} token validated successfully.")
        return decoded_payload

    except ExpiredSignatureError:
        logger.info(f"{token_type.capitalize()} token has expired.")
        return None
    except JWTError as e:  # Covers validation errors (aud, iss, kid, at_hash)
        logger.warning(f"{token_type.capitalize()} token JWT validation failed: {e}")
        return None
    except JOSEError as e:  # Covers JWKS fetch errors, bad crypto signatures
        logger.error(
            f"JOSE error during {token_type.capitalize()} token validation: {e}"
        )
        return None
    except Exception:
        logger.exception(f"Unexpected error during token validation")
        return None


# --- Token Refresh --- #
def _refresh_tokens(refresh_token: str) -> Optional[Dict[str, Any]]:
    """Attempts to refresh tokens using the provided refresh token."""
    cfg = config.load_config()
    token_endpoint = cfg.get("oidc_token_endpoint")
    client_id = cfg.get("keycloak_client_id")
    ssl_verify = cfg.get("ssl_verify", True)

    if not all([token_endpoint, client_id, refresh_token]):
        logger.error("Missing configuration data for token refresh attempt.")
        return None

    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
    }

    try:
        console.print("Attempting to refresh session...", end="")
        response = _retry_network_call(
            requests.post, token_endpoint, data=payload, timeout=15, verify=ssl_verify
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx/5xx) after retries
        new_tokens = response.json()
        console.print(
            "Session refreshed successfully.       "
        )  # Spaces to overwrite previous msg
        logger.info("Tokens refreshed successfully.")

        id_token = new_tokens.get("id_token")
        access_token = new_tokens.get("access_token")

        # Crucial: Validate the *new* ID token before saving
        if id_token and access_token:
            # Validate new ID token, providing the *new* access token for at_hash check
            if not _decode_and_validate_token(id_token, "refreshed ID", access_token):
                logger.warning("Refreshed ID token failed validation. Clearing tokens.")
                _clear_tokens()
                return None
        else:
            logger.warning(
                "Refreshed token response missing ID or Access token. Clearing tokens."
            )
            _clear_tokens()
            return None

        _save_tokens(new_tokens)
        return new_tokens

    except RequestException as e:
        console.print(
            "Session refresh failed.                  "
        )  # Spaces to overwrite
        logger.warning(f"Token refresh failed: {e}", exc_info=True)
        if hasattr(e, "response") and e.response is not None:
            status_code = e.response.status_code
            try:
                error_details = e.response.json()
                error_code = error_details.get("error")
                logger.warning(
                    f"Refresh error details (HTTP {status_code}): {error_details}"
                )
                if status_code in [400, 401] and error_code == "invalid_grant":
                    console.print(
                        "[yellow]Refresh token is invalid or expired. Please login again.[/yellow]"
                    )
                    _clear_tokens()
                elif error_code:
                    console.print(
                        f"[yellow]Refresh failed ({error_code}, HTTP {status_code}). Please try login again.[/yellow]"
                    )
                    # Decide whether to clear tokens based on error - maybe not for server errors?
                else:
                    console.print(
                        f"[yellow]Refresh failed (HTTP {status_code}). Please try login again.[/yellow]"
                    )
            except (ValueError, json.JSONDecodeError):
                logger.warning(
                    f"Refresh raw error response (HTTP {status_code}): {e.response.text}"
                )
                console.print(
                    f"[yellow]Refresh failed (HTTP {status_code}, non-JSON response). Please try login again.[/yellow]"
                )
        else:
            # Likely a network error that exhausted retries
            console.print(
                "[yellow]Network error during refresh. Check connection and try again.[/yellow]"
            )
        return None  # Return None on failure
    except Exception:
        console.print("Session refresh failed unexpectedly.     ")  # Spaces
        logger.exception(f"Unexpected error during token refresh")
        return None


# --- Public Authentication Functions --- #


def get_tokens(
    force_refresh: bool = False, allow_prompt: bool = True
) -> Optional[Dict[str, Any]]:
    """Retrieves tokens, validating and attempting refresh if necessary."""
    tokens = _load_tokens()
    if not tokens:
        logger.debug("No tokens found in storage.")
        return None

    if force_refresh:
        logger.info("Forcing token refresh.")
        refresh_token = tokens.get("refresh_token")
        if refresh_token:
            return _refresh_tokens(refresh_token)
        else:
            logger.warning("Force refresh requested, but no refresh token available.")
            _clear_tokens()
            return None

    id_token = tokens.get("id_token")
    access_token = tokens.get("access_token")

    # Validate ID token first (includes expiry check and at_hash)
    validated_payload = _decode_and_validate_token(
        id_token, "ID", access_token=access_token
    )

    if validated_payload:
        logger.debug("Current tokens are valid.")
        return tokens
    else:
        logger.info("Current tokens invalid or expired, attempting refresh.")
        refresh_token = tokens.get("refresh_token")
        if refresh_token:
            return _refresh_tokens(
                refresh_token
            )  # Refresh handles its own errors/return
        else:
            logger.warning("Token validation failed and no refresh token available.")
            _clear_tokens()
            if allow_prompt:
                # Only show user message if interactive prompt is allowed
                console.print(
                    "[yellow]Your session has expired. Please login again.[/yellow]"
                )
            return None


def is_authenticated(verify: bool = True) -> bool:
    """Checks if the user is authenticated, optionally verifying token validity."""
    if not verify:
        # Simple check: do tokens exist?
        return _load_tokens() is not None
    else:
        # Robust check: try to get valid (potentially refreshed) tokens
        # Suppress user prompts during this check
        return get_tokens(allow_prompt=False) is not None


def login() -> bool:
    """Initiates the OAuth 2.0 Device Authorization Grant flow."""
    # Check if already logged in with valid tokens first
    if is_authenticated(verify=True):
        console.print(
            "[green]You are already logged in and session appears valid.[/green]"
        )
        return True

    cfg = config.load_config()
    device_auth_endpoint = cfg.get("oidc_device_auth_endpoint")
    token_endpoint = cfg.get("oidc_token_endpoint")
    client_id = cfg.get("keycloak_client_id")
    scopes = cfg.get("additional_scopes", "openid email profile")
    ssl_verify = cfg.get("ssl_verify", True)

    if not all([device_auth_endpoint, token_endpoint, client_id]):
        console.print(
            "[bold red]Error:[/bold red] Required Keycloak configuration missing."
        )
        console.print(
            f"Please ensure oidc_device_auth_endpoint, oidc_token_endpoint, and keycloak_client_id are set in {config.get_config_path()}"
        )
        logger.critical("Device flow configuration check failed.")
        return False

    try:
        # --- Device Authorization Request --- #
        console.print("Requesting device authorization from Keycloak...")
        device_auth_payload = {"client_id": client_id, "scope": scopes}

        response = _retry_network_call(
            requests.post,
            device_auth_endpoint,
            data=device_auth_payload,
            timeout=15,
            verify=ssl_verify,
        )
        response.raise_for_status()  # Raise HTTPError for bad responses after retries
        device_data = response.json()

        device_code = device_data.get("device_code")
        user_code = device_data.get("user_code")
        verification_uri = device_data.get("verification_uri")
        verification_uri_complete = device_data.get("verification_uri_complete")
        expires_in = device_data.get("expires_in")
        interval = device_data.get("interval", 5)

        if not all([device_code, user_code, verification_uri, expires_in]):
            logger.error(
                f"Incomplete response from device auth endpoint: {device_data}"
            )
            raise ValueError("Incomplete response received from authorization server.")

        # --- Display Instructions --- #
        console.print("[bold cyan]Action Required:[/bold cyan]")
        display_uri = verification_uri_complete or verification_uri
        console.print(
            f"1. Open the following URL in any browser:   [link={display_uri}]{display_uri}[/link]"
        )
        if not verification_uri_complete:
            # Only show user code if there isn't a combined verification+code URI
            console.print(
                f"2. Enter the following code: [bold yellow]{user_code}[/bold yellow]"
            )
        else:
            console.print(f"2. Confirm authorization for client '{client_id}'.")

        # --- Token Polling --- #
        polling_start_time = time.monotonic()
        polling_timeout = polling_start_time + expires_in
        polling_success = False
        tokens = None
        # Use provided interval, potentially increased by 'slow_down'
        polling_interval = max(5, interval)  # Ensure at least 5s interval per RFC8628

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,  # Auto-remove progress on exit
        ) as progress:
            task_id = progress.add_task(
                description="Waiting for authorization...", total=None  # Indeterminate
            )

            while time.monotonic() < polling_timeout:
                progress.update(
                    task_id,
                    description=f"Waiting for authorization... (Checking in {polling_interval}s)",
                )
                time.sleep(polling_interval)

                try:
                    token_payload = {
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "client_id": client_id,
                        "device_code": device_code,
                    }
                    logger.debug(
                        f"Polling token endpoint with device code ending in ...{device_code[-5:]}"
                    )
                    # NO RETRY on polling loop itself: The spec defines specific errors for polling status
                    token_response = requests.post(
                        token_endpoint,
                        data=token_payload,
                        timeout=10,  # Shorter timeout for polling requests
                        verify=ssl_verify,
                    )

                    if token_response.status_code == 200:
                        tokens = token_response.json()
                        logger.info("Token received successfully via device flow.")
                        polling_success = True
                        progress.update(
                            task_id,
                            description="Authorization successful!",
                            completed=100,  # Mark as complete
                            total=100,
                        )
                        break  # Exit polling loop
                    elif token_response.status_code == 400:
                        error_data = token_response.json()
                        error_code = error_data.get("error")
                        logger.debug(f"Polling error response: {error_data}")
                        if error_code == "authorization_pending":
                            # Expected case, continue polling
                            progress.update(
                                task_id, description="Waiting for authorization..."
                            )
                            continue
                        elif error_code == "slow_down":
                            # Increase interval as requested by server
                            polling_interval = max(
                                polling_interval + 2, 5
                            )  # Increase by 2, min 5s
                            logger.info(
                                f"'slow_down' received, increasing polling interval to {polling_interval}s."
                            )
                            progress.update(
                                task_id,
                                description=f"Waiting for authorization... (Slowing down to {polling_interval}s)",
                            )
                            continue
                        elif error_code == "access_denied":
                            console.print(
                                "[bold red]Login failed:[/bold red] Authorization request denied by user."
                            )
                            progress.stop()
                            return False
                        elif error_code == "expired_token":
                            console.print(
                                "[bold red]Login failed:[/bold red] Authorization request expired. Please try login again."
                            )
                            progress.stop()
                            return False
                        else:
                            # Unknown 400 error during polling
                            console.print(
                                f"[bold red]Login failed:[/bold red] Received unexpected error during polling: {error_data}"
                            )
                            logger.error(
                                f"Unknown 400 error during token polling: {error_data}"
                            )
                            progress.stop()
                            return False
                    else:
                        # Handle other unexpected HTTP errors during polling
                        logger.error(
                            f"Unexpected HTTP {token_response.status_code} during token polling: {token_response.text}"
                        )
                        console.print(
                            f"[bold red]Login failed:[/bold red] Unexpected server response (HTTP {token_response.status_code})."
                        )
                        progress.stop()
                        return False

                except (ConnectionError, Timeout, SSLError) as e:
                    # Network errors during polling - show warning and continue polling
                    error_type = type(e).__name__
                    logger.warning(
                        f"Network error ({error_type}) during polling: {e}. Will retry after interval."
                    )
                    progress.update(
                        task_id,
                        description=f"Network issue, retrying in {polling_interval}s...",
                    )
                    continue  # Let the loop continue and time.sleep handle delay
                except RequestException as e:
                    # Catch other request exceptions (e.g., bad proxy, DNS)
                    logger.error(
                        f"Unexpected RequestException during polling: {e}",
                        exc_info=True,
                    )
                    console.print(
                        f"[bold red]Login failed:[/bold red] Unexpected network request error: {e}"
                    )
                    progress.stop()
                    return False
                except Exception as e:
                    # Catch any other unexpected error during the poll attempt
                    console.print(
                        f"[bold red]An unexpected error occurred during polling: {e}[/bold red]"
                    )
                    logger.exception("Unexpected error during token polling loop")
                    progress.stop()
                    return False
            # --- End of Polling Loop --- #

        # Check outcome after loop exits
        if not polling_success:
            # This means the loop timed out
            console.print("[bold red]Login failed:[/bold red] Authorization timed out.")
            logger.warning(f"Device flow timed out after {expires_in} seconds.")
            return False

        # --- Post-Success Validation --- #
        if tokens:
            access_token = tokens.get("access_token")
            id_token = tokens.get("id_token")
            if not access_token or not id_token:
                logger.error(
                    f"Incomplete token response received from successful poll: {tokens}"
                )
                raise ValueError(
                    "Incomplete token response received (missing access or ID token)."
                )

            # Validate the received ID token (at_hash check now re-enabled)
            if not _decode_and_validate_token(
                id_token, "initial ID", access_token=access_token
            ):
                logger.error(
                    "Initial token validation failed after successful device flow. Check system clock/config/keys."
                )
                # Raise the specific validation error for clarity
                raise ValueError(
                    "Initial token validation failed (check logs for details). Check system clock or Keycloak config."
                )

            console.print("[green]Tokens received and validated.[/green]")
            _save_tokens(tokens)
            return True
        else:
            # Should not happen if polling_success is True and loop exited cleanly
            logger.critical(
                "Internal logic error: Polling succeeded but no tokens found."
            )
            console.print(
                "[bold red]Internal Error:[/bold red] Login completed but failed to retrieve tokens."
            )
            return False

    # --- Error Handling for Initial Device Auth Request or Other Flow Errors --- #
    except RequestException as e:
        # Handles errors from the initial device auth request after retries exhausted
        console.print(f"[bold red]Login failed (Network Error):[/bold red] {e}")
        if hasattr(e, "response") and e.response is not None:
            status_code = e.response.status_code
            try:
                error_details = e.response.json()
                console.print(
                    f"[red]Error details (HTTP {status_code}):[/red] {error_details}"
                )
            except (ValueError, json.JSONDecodeError):
                console.print(
                    f"[red]Raw error response (HTTP {status_code}):[/red] {e.response.text}"
                )
        else:
            console.print(
                "[red]Could not connect to the authorization server. Check network and configuration.[/red]"
            )
        return False
    except ValueError as e:  # Catch our own validation/config errors
        console.print(f"[bold red]Login failed:[/bold red] {e}")
        return False
    except Exception as e:
        console.print(
            f"[bold red]An unexpected error occurred during login: {e}[/bold red]"
        )
        logger.exception("Unexpected error during login flow")
        return False


def logout():
    """Clears local tokens and provides Keycloak logout URL if configured."""
    _clear_tokens()
    console.print("Local session cleared.")
    cfg = config.load_config()
    logout_endpoint = cfg.get("oidc_logout_endpoint")

    if logout_endpoint:
        # Optional: Future enhancement could attempt server-side refresh token revocation
        console.print("To ensure complete logout from Keycloak, you may need to visit:")
        console.print(f"  [link={logout_endpoint}]{logout_endpoint}[/link]")
    else:
        logger.warning(
            "Logout endpoint (oidc_logout_endpoint) not configured in settings."
        )
        # Inform user if endpoint isn't set
        console.print(
            "[yellow]Logout endpoint not configured; cannot provide Keycloak logout URL.[/yellow]"
        )
