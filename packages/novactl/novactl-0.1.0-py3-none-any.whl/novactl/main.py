# -*- coding: utf-8 -*-
"""
Author: Harsha Krishnareddy
Email: c0mpiler@ins8s.dev
"""
"""Main CLI application entry point for novactl."""

import datetime
import logging

import typer
from jose import jwt as jose_jwt
from jose.exceptions import JWTError
from rich.console import Console
from rich.pretty import pprint
from rich.syntax import Syntax
from rich.table import Table

# Use relative imports for sibling modules within the package
from . import auth, config

# Initialize Rich Console
console = Console()

# Configure logging (basic setup, config module might refine handlers/levels)
logger = logging.getLogger(__name__)
# Basic config to ensure logs are captured if config loading fails
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Initialize Typer app
app = typer.Typer(
    name="novactl",
    help="Boilerplate CLI with Keycloak/OAuth2 Device Flow Authentication.",
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,  # Show help if no command is given
)


@app.callback()
def main_callback(ctx: typer.Context):
    """
    Main callback executed before commands. Loads configuration.
    """
    # Ensure logging is configured early, potentially refined by load_config
    logger.debug("Main callback started. Loading configuration.")
    try:
        cfg = config.load_config()
        # Pass config down via context if needed by commands
        ctx.meta["config"] = cfg
        logger.debug("Configuration loaded successfully in main callback.")
    except SystemExit:  # Catch exit from load_config on critical errors
        # Error message already printed by load_config
        raise  # Re-raise to ensure Typer exits
    except Exception:
        # Catch unexpected errors during config load
        logger.exception("Unexpected error loading configuration in main callback.")
        console.print(
            "[bold red]Fatal Error:[/bold red] Unexpected issue loading configuration. Check logs."
        )
        raise typer.Exit(code=2)


def _ensure_authenticated(command_name: str):
    """Helper to verify authentication before running a command."""
    logger.debug(f"Ensuring authentication for command: {command_name}")
    if not auth.is_authenticated(verify=True):
        # Explicitly print error message before exiting for clarity in tests
        console.print(
            "[bold red]Authentication required.[/bold red] Please run `novactl login`."
        )
        logger.warning(
            f"Authentication check failed for command '{command_name}'. Exiting."
        )
        raise typer.Exit(code=1)
    logger.debug(f"Authentication confirmed for command '{command_name}'.")


# --- Authentication Commands (Essential Boilerplate) --- #


@app.command()
def login():
    """
    Log in using Keycloak OAuth 2.0 Device Authorization Grant.
    """
    console.print("[cyan]Initiating Login...[/cyan]")
    if auth.login():
        console.print("[green]Login successful.[/green]")
        # Display a friendly welcome message
        tokens = auth.get_tokens(allow_prompt=False)
        if tokens and "id_token" in tokens:
            try:
                payload = jose_jwt.get_unverified_claims(tokens["id_token"])
                username = payload.get("preferred_username", "user")
                console.print(f"Welcome, [bold]{username}[/bold]!")
            except JWTError:
                logger.warning("Could not decode ID token for welcome message.")
    else:
        console.print("[bold red]Login process failed or was cancelled.[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def logout():
    """
    Log out, clearing local tokens and providing Keycloak logout URL.
    """
    console.print("[cyan]Initiating Logout...[/cyan]")
    auth.logout()
    # User messages are handled by auth.logout()


@app.command()
def status():
    """
    Check current authentication status and token validity (attempts refresh).
    """
    console.print("Checking authentication status...")
    if auth.is_authenticated(verify=True):
        console.print(
            "[bold green]Status:[/bold green] Logged in and session appears valid."
        )
        tokens = auth.get_tokens(allow_prompt=False)
        if tokens and "id_token" in tokens:
            try:
                id_payload = jose_jwt.get_unverified_claims(tokens["id_token"])
                exp = id_payload.get("exp")
                if exp:
                    expiry_dt = datetime.datetime.fromtimestamp(
                        exp, tz=datetime.timezone.utc
                    )
                    now = datetime.datetime.now(tz=datetime.timezone.utc)
                    leeway_seconds = config.get_config_value("token_leeway_seconds", 60)
                    leeway_delta = datetime.timedelta(seconds=leeway_seconds)

                    if expiry_dt > (now - leeway_delta):
                        delta = expiry_dt - now
                        delta_str = str(delta).split(".")[0]
                        console.print(
                            f"  Session valid for approx: [green]{delta_str}[/green]"
                        )
                    else:
                        # Should be less common now due to refresh attempt in is_authenticated
                        delta = now - expiry_dt
                        delta_str = str(delta).split(".")[0]
                        console.print(
                            f"  Session expired approx: [red]{delta_str} ago[/red] (Refresh likely failed)"
                        )
                else:
                    console.print("  ID Token lacks expiration ('exp') claim.")
            except JWTError:
                logger.warning("Could not decode ID token to check expiry.")
                console.print(
                    "  [yellow]Warning:[/yellow] Could not check token expiry time."
                )
            except Exception:
                logger.warning("Error processing token expiry.", exc_info=True)
                console.print(
                    "  [yellow]Warning:[/yellow] Error processing token expiry."
                )
    else:
        # is_authenticated(verify=True) failed
        if auth._load_tokens() is None:
            console.print("[bold yellow]Status:[/bold yellow] Not logged in.")
        else:
            # Tokens exist but failed validation/refresh
            console.print(
                "[bold yellow]Status:[/bold yellow] Session expired or invalid. Refresh failed."
            )
            console.print("  Run `novactl login` to start a new session.")


@app.command()
def whoami():
    """
    Display validated information about the logged-in user from ID token.
    """
    _ensure_authenticated("whoami")
    tokens = auth.get_tokens(allow_prompt=False)
    if not tokens or "id_token" not in tokens:
        console.print(
            "[bold red]Error:[/bold red] Could not retrieve valid ID token after auth check."
        )
        raise typer.Exit(code=1)
    id_token = tokens["id_token"]

    # Validation happened in _ensure_authenticated, decode here for display
    try:
        user_info = auth._decode_and_validate_token(
            id_token, "ID", access_token=tokens.get("access_token")
        )
        verification_status = "[green](Verified)[/green]"
        if not user_info:
            # Fallback to unverified display if validation failed unexpectedly
            verification_status = (
                "[yellow](Verification Failed - Displaying Unverified)[/yellow]"
            )
            user_info = jose_jwt.get_unverified_claims(id_token)

    except JWTError as e:
        console.print(f"[bold red]Error:[/bold red] Could not decode ID token: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.exception("Unexpected error decoding/validating token in whoami")
        console.print(
            f"[bold red]Error:[/bold red] Unexpected error processing token: {e}"
        )
        raise typer.Exit(code=1)

    console.print(
        f"[bold green]Authenticated User Info:[/bold green] {verification_status}"
    )
    table = Table(show_header=False, box=None, title="User Details")
    table.add_column("Field", style="dim cyan", no_wrap=True)
    table.add_column("Value", style="white")

    # Common OIDC claims
    table.add_row("Subject (sub)", user_info.get("sub", "N/A"))
    table.add_row("Preferred Username", user_info.get("preferred_username", "N/A"))
    table.add_row("Name", user_info.get("name", "N/A"))
    table.add_row("Email", user_info.get("email", "N/A"))
    table.add_row("Email Verified", str(user_info.get("email_verified", "N/A")))
    table.add_row("Issuer (iss)", user_info.get("iss", "N/A"))
    aud = user_info.get("aud", "N/A")
    table.add_row(
        "Audience (aud)", str(aud) if not isinstance(aud, list) else ", ".join(aud)
    )

    # Display token expiry relative to now
    exp = user_info.get("exp")
    if exp:
        try:
            expiry_dt = datetime.datetime.fromtimestamp(exp, tz=datetime.timezone.utc)
            now = datetime.datetime.now(tz=datetime.timezone.utc)
            if expiry_dt > now:
                delta = expiry_dt - now
                delta_str = str(delta).split(".")[0]
                table.add_row("Token Expires In", f"[green]approx {delta_str}[/green]")
            else:
                delta = now - expiry_dt
                delta_str = str(delta).split(".")[0]
                table.add_row("Token Expired", f"[red]approx {delta_str} ago[/red]")
        except (TypeError, ValueError):
            logger.warning(f"Could not parse token expiry timestamp: {exp}")
            table.add_row("Token Expiry", f"Invalid timestamp ({exp})")
    else:
        table.add_row("Token Expiry", "No 'exp' claim")

    console.print(table)


@app.command(name="get-roles")
def get_roles():
    """
    Display Realm and Client roles from the (unverified) access token.
    """
    _ensure_authenticated("get-roles")
    tokens = auth.get_tokens(allow_prompt=False)
    if not tokens or "access_token" not in tokens:
        console.print(
            "[bold red]Error:[/bold red] Could not retrieve valid access token after auth check."
        )
        raise typer.Exit(code=1)
    access_token = tokens["access_token"]

    try:
        # Decode access token without validation just for display
        token_info = jose_jwt.get_unverified_claims(access_token)
        console.print(
            "[bold green]User Roles (from Access Token):[/bold green] [yellow](Decoded Only)[/yellow]"
        )

        realm_access = token_info.get("realm_access", {}).get("roles", [])
        resource_access = token_info.get("resource_access", {})

        if not realm_access and not resource_access:
            console.print("[cyan]  No roles found in access token.[/cyan]")
            return

        if realm_access:
            console.print("[cyan]Realm Roles:[/cyan]")
            for role in sorted(realm_access):
                console.print(f"  - {role}")

        if resource_access:
            console.print("[cyan]Client Roles:[/cyan]")
            client_roles_found = False
            for client, client_data in sorted(resource_access.items()):
                roles = client_data.get("roles", [])
                if roles:
                    client_roles_found = True
                    console.print(f"  [bold magenta]{client}:[/bold magenta]")
                    for role in sorted(roles):
                        console.print(f"    - {role}")
            if not client_roles_found:
                console.print("  (No client-specific roles found)")

    except JWTError as e:
        console.print(f"[bold red]Error decoding access token:[/bold red] {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        logger.exception("Unexpected error decoding roles")
        console.print(
            f"[bold red]An unexpected error occurred decoding roles:[/bold red] {e}"
        )
        raise typer.Exit(code=1)


@app.command()
def tkn(
    token_type: str = typer.Argument(
        "access",
        help="Token type: 'access', 'id', or 'refresh'.",
        case_sensitive=False,
        show_choices=True,
    ),
    decode: bool = typer.Option(
        False, "--decode", "-d", help="Decode JWT token payload (no verification)."
    ),
):
    """
    Display the raw or decoded specified token (access, id, refresh).
    """
    _ensure_authenticated("tkn")
    tokens = auth.get_tokens(allow_prompt=False)
    if not tokens:
        # Should be caught by _ensure_authenticated, but defensive check
        console.print("[bold red]Error:[/bold red] Could not retrieve tokens.")
        raise typer.Exit(code=1)

    token_key_map = {
        "access": "access_token",
        "id": "id_token",
        "refresh": "refresh_token",
    }
    token_key = token_key_map.get(token_type.lower())

    if not token_key:
        # Should be handled by Typer enum/choices, but defensive check
        console.print(f"[bold red]Error:[/bold red] Invalid token type '{token_type}'.")
        raise typer.Exit(code=1)

    token = tokens.get(token_key)

    if not token:
        console.print(
            f"[bold red]Error:[/bold red] {token_type.capitalize()} token not found in session."
        )
        if token_key == "refresh_token":
            console.print(
                "[yellow]Note:[/yellow] Refresh tokens require 'offline_access' scope during login."
            )
        raise typer.Exit(code=1)

    console.print(f"[bold green]{token_type.capitalize()} Token:[/bold green]")
    if decode and token_key != "refresh_token":  # Decode only JWTs
        try:
            decoded_token = jose_jwt.get_unverified_claims(token)
            # Use Rich pretty print for better formatting
            pprint(decoded_token)
        except JWTError as e:
            logger.warning(
                f"Could not decode {token_type} token (not a valid JWT?): {e}"
            )
            console.print(f"[red]Error decoding token (expected JWT): {e}[/red]")
            console.print("[bold yellow]Raw Token:[/bold yellow]")
            console.print(token)
        except Exception as e:
            logger.exception(f"Unexpected error decoding {token_type} token")
            console.print(f"[bold red]Error processing token: {e}[/bold red]")
            console.print("[bold yellow]Raw Token:[/bold yellow]")
            console.print(token)
    else:
        if decode and token_key == "refresh_token":
            console.print(
                "[yellow](Refresh tokens are usually opaque and not JWTs - showing raw)[/yellow]"
            )
        # Print raw token, using syntax highlight for JWTs
        lexer = "jwt" if token_key != "refresh_token" else "text"
        try:
            syntax = Syntax(
                token, lexer, theme="default", line_numbers=False, word_wrap=True
            )
            console.print(syntax)
        except Exception:
            logger.exception(f"Error formatting token with lexer '{lexer}'")
            console.print("[red]Error formatting token, showing raw:[/red]")
            console.print(token)


# --- Placeholder for Your Application's Commands --- #


@app.command()
def my_command(name: str = typer.Option("World", help="Name to greet.")):
    """
    [Example] Replace this with your CLI's actual commands.
    This example command requires authentication.
    """
    _ensure_authenticated("my-command")  # Protect the command
    # *** CORRECTED MARKUP ***
    console.print(f"Hello [bold cyan]{name}[/bold cyan]! You are authenticated.")

    # Example: Get tokens to make an API call
    tokens = auth.get_tokens(allow_prompt=False)
    if tokens:
        access_token = tokens.get("access_token")
        if access_token:
            console.print("Retrieved access token to use for API calls:")
            # Display first/last parts for brevity
            console.print(f"  {access_token[:20]}...{access_token[-20:]}")
            # In a real command, you would use this token:
            # headers = {"Authorization": f"Bearer {access_token}"}
            # response = requests.get("YOUR_API_ENDPOINT", headers=headers)
            # ... process response ...
        else:
            console.print(
                "[yellow]Access token not found in retrieved tokens.[/yellow]"
            )

    # Add your command logic here...


# --- Entry Point --- #

if __name__ == "__main__":
    app()
