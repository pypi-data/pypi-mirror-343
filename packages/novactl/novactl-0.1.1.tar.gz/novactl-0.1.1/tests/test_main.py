import json
import time
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlparse

import pytest
import requests
from jose import JWTError
from jose import jwt as jose_jwt

# --- IMPORTANT: Import modules using the NEW package name 'novactl' --- #
from novactl import auth, config, main

# Import constants using the new package name reference if needed
from tests.conftest import TEST_CONFIG_DATA  # Use updated config data structure
from tests.conftest import TEST_KEYRING_USERNAME  # Use derived username
from tests.conftest import (
    private_key_pem,  # PREDICTABLE_STATE is removed as it's not used in device flow tests; MOCK_KID is used internally by helpers, no need to import here
)
from tests.conftest import (
    TEST_SERVICE_NAME,
)


# Helper to save tokens to the mock keyring
def save_mock_tokens(mock_keyring, tokens):
    service = TEST_CONFIG_DATA["keyring_service_name"]  # Use constant
    username = TEST_KEYRING_USERNAME  # Use constant derived username
    mock_keyring[(service, username)] = json.dumps(tokens)


# Helper to clear mock keyring
def clear_mock_tokens(mock_keyring):
    service = TEST_CONFIG_DATA["keyring_service_name"]
    username = TEST_KEYRING_USERNAME
    if (service, username) in mock_keyring:
        del mock_keyring[(service, username)]


# --- Basic Command Tests ---


def test_help(runner):
    """Test the --help flag."""
    result = runner.invoke(main.app, ["--help"])
    output = result.stdout + result.stderr
    assert result.exit_code == 0
    assert "Usage:" in output
    assert "novactl" in output  # Check for new command name
    assert "login" in output
    assert "status" in output
    assert "my-command" in output  # Check example command


def test_no_args_shows_help(runner):
    """Test that running with no arguments shows help (due to no_args_is_help=True)."""
    result = runner.invoke(main.app, [])
    output = result.stdout + result.stderr
    assert result.exit_code == 0
    assert "Usage:" in output


def test_status_logged_out(runner, mock_keyring):
    """Test `status` command when no tokens are stored."""
    clear_mock_tokens(mock_keyring)  # Ensure logged out
    result = runner.invoke(main.app, ["status"])
    assert result.exit_code == 0
    assert "Status: Not logged in." in result.stdout


# --- Login Flow Tests (Device Flow) ---


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_login_success(runner, mock_keyring, mock_requests):
    """Test successful device flow login."""
    clear_mock_tokens(mock_keyring)  # Start clean
    rmock, helpers = mock_requests
    # Mock the sequence: pending -> success
    rmock.post(
        helpers["token_url"],
        [
            {
                "json": {"error": "authorization_pending"},
                "status_code": 400,
            },  # First poll: pending
            {
                "json": helpers["generate_token_response"](),
                "status_code": 200,
            },  # Second poll: success
        ],
    )

    # Act
    result = runner.invoke(main.app, ["login"])

    # Assertions
    assert (
        result.exit_code == 0
    ), f"Login failed. stdout: {result.stdout} stderr: {result.stderr}"
    # Check for device flow prompts
    assert "Action Required:" in result.stdout
    assert helpers["mock_device_response"]["verification_uri_complete"] in result.stdout
    # Don't assert transient progress message
    # assert "Waiting for authorization..." in result.stdout # Progress bar text
    # assert "Authorization successful!" in result.stdout
    assert "Tokens received and validated." in result.stdout
    # assert "Login successful." in result.stdout
    assert "Welcome, mockuser!" in result.stdout

    # Verify tokens saved in keyring
    saved_token_str = mock_keyring.get((TEST_SERVICE_NAME, TEST_KEYRING_USERNAME))
    assert saved_token_str is not None
    saved_tokens = json.loads(saved_token_str)
    assert "access_token" in saved_tokens
    assert "id_token" in saved_tokens
    assert "refresh_token" in saved_tokens  # Ensure refresh token is included

    # Verify calls: 1 device auth, 2 token polls
    assert rmock.call_count == 3
    assert rmock.request_history[0].url == helpers["device_auth_url"]
    assert rmock.request_history[1].url == helpers["token_url"]
    assert rmock.request_history[2].url == helpers["token_url"]


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_login_already_logged_in(runner, mock_keyring, mock_requests):
    """Test `login` command when already logged in with valid tokens."""
    rmock, helpers = mock_requests
    # Arrange: Pre-populate keyring with fresh, valid tokens
    valid_tokens = helpers["generate_token_response"](access_token_expiry=3600)
    save_mock_tokens(mock_keyring, valid_tokens)

    # Act
    result = runner.invoke(main.app, ["login"])

    # Assert
    assert result.exit_code == 0, f"stdout: {result.stdout} stderr: {result.stderr}"
    assert "You are already logged in and session appears valid." in result.stdout
    # Ensure device auth flow was *not* initiated
    # JWKS might still be called by is_authenticated check
    device_auth_calls = [
        r for r in rmock.request_history if r.url == helpers["device_auth_url"]
    ]
    assert len(device_auth_calls) == 0


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_login_polling_timeout(runner, mock_keyring, mock_requests):
    """Test device flow login when polling times out."""
    clear_mock_tokens(mock_keyring)
    rmock, helpers = mock_requests
    # Mock token endpoint to *always* return pending
    helpers["set_token_endpoint_error"](error_code="authorization_pending", status=400)

    # Mock time.monotonic to simulate time passing and trigger timeout
    # Get expiry from mock device response
    expires_in = helpers["mock_device_response"]["expires_in"]
    start_time = time.monotonic()
    # Simulate time advancing just past the timeout on the second check
    # (first check happens immediately, then sleep, then second check)
    monotonic_values = [start_time, start_time + expires_in + 1]
    with patch("time.monotonic", side_effect=monotonic_values):
        # Act
        result = runner.invoke(main.app, ["login"])

    # Assert
    assert result.exit_code == 1, f"stdout: {result.stdout} stderr: {result.stderr}"
    assert "Login failed: Authorization timed out." in result.stdout
    assert "Login process failed or was cancelled." in result.stdout
    # Ensure tokens were not saved
    assert mock_keyring.get((TEST_SERVICE_NAME, TEST_KEYRING_USERNAME)) is None


def test_login_device_auth_fails(runner, mock_keyring, mock_requests):
    """Test login failure if the initial device auth request fails."""
    clear_mock_tokens(mock_keyring)
    rmock, helpers = mock_requests
    # Arrange: Mock the device auth endpoint to return an error
    rmock.post(helpers["device_auth_url"], status_code=500, text="Server Error")

    # Act
    result = runner.invoke(main.app, ["login"])

    # Assert
    assert result.exit_code == 1, f"stdout: {result.stdout} stderr: {result.stderr}"
    assert "Login failed (Network Error):" in result.stdout  # From auth retry handler
    assert "500 Server Error" in result.stdout
    assert "Login process failed or was cancelled." in result.stdout
    assert mock_keyring.get((TEST_SERVICE_NAME, TEST_KEYRING_USERNAME)) is None


# --- Authenticated Command Tests ---


@pytest.fixture
def logged_in_state(mock_keyring, mock_requests):
    """Fixture to set up a logged-in state with fresh tokens."""
    rmock, helpers = mock_requests
    if private_key_pem is None:
        pytest.skip("cryptography library not installed, cannot generate valid JWTs")
    # Generate fresh tokens for the logged-in state
    valid_tokens = helpers["generate_token_response"](access_token_expiry=3600)
    save_mock_tokens(mock_keyring, valid_tokens)
    yield valid_tokens, helpers  # Provide tokens and helpers to tests
    # Cleanup (clearing keyring) happens in reset_auth_caches fixture


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_status_logged_in(runner, logged_in_state):
    """Test `status` command when logged in with valid tokens."""
    result = runner.invoke(main.app, ["status"])
    assert result.exit_code == 0
    assert "Status: Logged in and session appears valid." in result.stdout
    assert "Session valid for approx:" in result.stdout


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_whoami_success(runner, logged_in_state):
    """Test `whoami` command when logged in."""
    result = runner.invoke(main.app, ["whoami"])
    assert result.exit_code == 0
    assert "Authenticated User Info:" in result.stdout
    assert "(Verified)" in result.stdout
    assert "mockuser" in result.stdout  # Check username
    assert "mock-user-id" in result.stdout  # Check subject
    assert "Token Expires In" in result.stdout


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_get_roles_success(runner, logged_in_state):
    """Test `get-roles` command when logged in."""
    result = runner.invoke(main.app, ["get-roles"])
    assert result.exit_code == 0
    assert "User Roles (from Access Token):" in result.stdout
    assert "(Decoded Only)" in result.stdout  # Display only status
    assert "Realm Roles:" in result.stdout
    assert "realm-test-role" in result.stdout
    assert "Client Roles:" in result.stdout
    assert "client-test-role" in result.stdout


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_tkn_id_decode(runner, logged_in_state):
    """Test `tkn id --decode` command."""
    result = runner.invoke(main.app, ["tkn", "id", "--decode"])
    assert result.exit_code == 0
    assert "'preferred_username': 'mockuser'" in result.stdout  # Check decoded payload
    assert "'sub': 'mock-user-id'" in result.stdout


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_tkn_refresh_no_decode(runner, logged_in_state):
    """Test `tkn refresh` command (shows raw token)."""
    valid_tokens, _ = logged_in_state
    refresh_token = valid_tokens.get("refresh_token")
    assert refresh_token is not None, "Test setup error: No refresh token generated"

    result = runner.invoke(main.app, ["tkn", "refresh"])
    assert result.exit_code == 0
    assert refresh_token in result.stdout
    assert "Decoded" not in result.stdout  # Ensure it wasn't decoded


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_logout_success(runner, logged_in_state, mock_keyring):
    """Test `logout` command when logged in."""
    # We need the config fixture to get the expected logout URL
    cfg = config.load_config()  # Load mocked config
    logout_url_expected = cfg.get("oidc_logout_endpoint")

    # Act
    result = runner.invoke(main.app, ["logout"])

    # Assert
    assert result.exit_code == 0, f"stdout: {result.stdout} stderr: {result.stderr}"
    assert "Local session cleared." in result.stdout
    assert "To ensure complete logout from Keycloak" in result.stdout
    # Check for the core part of the URL, avoiding line break issues
    assert logout_url_expected in result.stdout.replace("\n", "")
    # Verify tokens cleared from keyring
    assert mock_keyring.get((TEST_SERVICE_NAME, TEST_KEYRING_USERNAME)) is None


def test_logout_when_logged_out(runner, mock_keyring):
    """Test `logout` command when already logged out."""
    clear_mock_tokens(mock_keyring)
    cfg = config.load_config()  # Load mocked config for URL
    logout_url_expected = cfg.get("oidc_logout_endpoint")

    result = runner.invoke(main.app, ["logout"])
    assert result.exit_code == 0
    assert "Local session cleared." in result.stdout
    # Check for the core part of the URL, avoiding line break issues
    assert logout_url_expected in result.stdout.replace(
        "\n", ""
    )  # Should still provide URL


# --- Test Auth Failure/Refresh Handling for Commands ---


def test_authenticated_command_fails_when_logged_out(runner, mock_keyring):
    """Test that commands protected by _ensure_authenticated fail if not logged in."""
    clear_mock_tokens(mock_keyring)
    # Act: Call a protected command (e.g., whoami)
    result = runner.invoke(main.app, ["whoami"])
    # Assert
    assert result.exit_code == 1  # Should exit with error code
    # Check for the specific message printed by _ensure_authenticated
    assert "Authentication required." in result.stdout
    assert "Please run `novactl login`" in result.stdout


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_authenticated_command_triggers_refresh(runner, mock_keyring, mock_requests):
    """Test that accessing a protected command triggers token refresh if tokens are expired."""
    rmock, helpers = mock_requests
    # Arrange: Store EXPIRED tokens but a VALID refresh token
    expired_iat = int(time.time()) - 5000  # Expired
    valid_refresh_token = "valid-refresh-token-for-test-refresh"
    initial_tokens = helpers["generate_token_response"](
        iat_override=expired_iat, access_token_expiry=-3600  # Expired access/id
    )
    initial_tokens["refresh_token"] = valid_refresh_token
    save_mock_tokens(mock_keyring, initial_tokens)

    # Arrange: Mock the refresh grant response to return NEW, VALID tokens
    refreshed_iat = int(time.time())
    refreshed_token_response = helpers["generate_token_response"](
        iat_override=refreshed_iat, access_token_expiry=3600  # Fresh tokens
    )
    new_refresh_token = refreshed_token_response["refresh_token"]
    # Match only the refresh grant for the specific token
    rmock.post(
        helpers["token_url"],
        additional_matcher=lambda req: f"refresh_token={valid_refresh_token}"
        in req.text
        and "grant_type=refresh_token" in req.text,
        json=refreshed_token_response,
        status_code=200,
    )

    # Act: Run a command that requires auth (e.g., whoami)
    result = runner.invoke(main.app, ["whoami"])

    # Assert: Command should succeed after refresh
    assert result.exit_code == 0, f"stdout: {result.stdout} stderr: {result.stderr}"
    assert (
        "Session refreshed successfully." in result.stdout
    )  # Check refresh message from auth
    assert "Authenticated User Info:" in result.stdout  # Check command output
    assert "(Verified)" in result.stdout

    # Verify refresh grant was called
    refresh_request = next(
        (r for r in rmock.request_history if "grant_type=refresh_token" in r.text), None
    )
    assert refresh_request is not None, "Refresh token grant was not called"

    # Verify NEW tokens are stored
    final_tokens_str = mock_keyring.get((TEST_SERVICE_NAME, TEST_KEYRING_USERNAME))
    assert final_tokens_str is not None
    final_tokens = json.loads(final_tokens_str)
    assert final_tokens["access_token"] == refreshed_token_response["access_token"]
    assert final_tokens["refresh_token"] == new_refresh_token


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_authenticated_command_fails_on_bad_refresh(
    runner, mock_keyring, mock_requests
):
    """Test command failure when tokens are expired AND refresh fails."""
    rmock, helpers = mock_requests
    # Arrange: Store expired tokens with an INVALID refresh token
    expired_iat = int(time.time()) - 5000
    invalid_refresh_token = "invalid-refresh-token-test"
    initial_tokens = helpers["generate_token_response"](
        iat_override=expired_iat, access_token_expiry=-3600
    )
    initial_tokens["refresh_token"] = invalid_refresh_token
    save_mock_tokens(mock_keyring, initial_tokens)

    # Arrange: Mock the refresh grant to return 'invalid_grant'
    helpers["set_token_endpoint_error"](error_code="invalid_grant", status=400)

    # Act: Run a protected command
    result = runner.invoke(main.app, ["whoami"])

    # Assert: Command should fail, exit code 1 from _ensure_authenticated
    assert result.exit_code == 1, f"stdout: {result.stdout} stderr: {result.stderr}"
    # Check for messages from the failed refresh attempt in auth module
    assert "Session refresh failed." in result.stdout
    assert "Refresh token is invalid or expired. Please login again." in result.stdout
    # Check for the standard message from _ensure_authenticated
    assert "Authentication required." in result.stdout
    assert "Please run `novactl login`" in result.stdout
    # Verify tokens were cleared by the failed refresh handler
    assert mock_keyring.get((TEST_SERVICE_NAME, TEST_KEYRING_USERNAME)) is None


# --- Example Command Test --- #


@pytest.mark.skipif(private_key_pem is None, reason="cryptography lib not installed")
def test_my_command_success(runner, logged_in_state):
    """Test the example 'my-command'."""
    result = runner.invoke(main.app, ["my-command", "--name", "Tester"])
    assert result.exit_code == 0
    assert "Hello Tester! You are authenticated." in result.stdout
    assert "Retrieved access token" in result.stdout


def test_my_command_needs_auth(runner, mock_keyring):
    """Test that 'my-command' fails if not logged in."""
    clear_mock_tokens(mock_keyring)
    result = runner.invoke(main.app, ["my-command"])
    assert result.exit_code == 1
    # Check for the specific message printed by _ensure_authenticated
    assert "Authentication required." in result.stdout
    assert "Please run `novactl login`" in result.stdout


# TODO: Add more tests:
# - More JWT validation failure scenarios (sig, iss, aud)
# - Config file variations (missing optional keys, bad ssl_verify path)
# - Keyring specific errors (if mockable)
# - Network errors during JWKS fetch
# - Device flow specific errors (access_denied, slow_down handled correctly)
# - Edge cases for `tkn` command (e.g., no refresh token available)
