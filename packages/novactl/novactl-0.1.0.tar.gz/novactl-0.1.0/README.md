# novactl - Boilerplate CLI with Keycloak Device Flow Auth

[![PyPI version](https://img.shields.io/pypi/v/novactl.svg?icon=si%3Apython)](https://pypi.org/project/novactl/)
[![License](https://img.shields.io/pypi/l/novactl.svg)](https://github.com/c0mpiler/novactl/blob/main/LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/c0mpiler/novactl/publish.yml?branch=main)](https://github.com/c0mpiler/novactl/actions)
[![Codecov](https://codecov.io/gh/c0mpiler/novactl/branch/main/graph/badge.svg?token=0OCRFPLQSU)](https://codecov.io/gh/c0mpiler/novactl)

`novactl` serves as a **production-ready boilerplate** for building Python Command-Line Interface (CLI) applications that require secure authentication against Keycloak (or potentially other OIDC providers) using the **OAuth 2.0 Device Authorization Grant**. It leverages [`Typer`](https://typer.tiangolo.com/) for the CLI framework, [`Rich`](https://rich.readthedocs.io/) for enhanced terminal output, and [`keyring`](https://pypi.org/project/keyring/) for secure local token storage.

This project provides the core authentication logic (`login`, `logout`, `status`, token validation, refresh, secure storage) so you can focus on building your CLI's specific commands.

## Features

*   **Secure Authentication:** Uses Keycloak's OAuth 2.0 Device Authorization Grant, suitable for headless or terminal-based applications.
*   **Token Management:** Handles access, ID, and refresh tokens.
*   **Automatic Refresh:** Attempts to automatically refresh expired access tokens using the refresh token.
*   **Secure Storage:** Stores tokens securely in the system's native keyring (macOS Keychain, Windows Credential Manager, GNOME Keyring, etc.).
*   **Configuration:** Uses a clear YAML configuration file (`~/.config/novactl/novactl.yml` by default) with schema validation.
*   **Robust:** Includes network retry logic, error handling, and structured logging.
*   **Modern CLI:** Built with Typer and Rich for a great developer and user experience.
*   **Boilerplate Ready:** Designed to be easily adapted for your own CLI application.

## Installation

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   A compatible system keyring backend (most modern OSs have one built-in).

### From PyPI (Recommended for Users)

```bash
# Ensure you have the latest pip
pip install --upgrade pip

pip install novactl
```

### From Source (Development)

1.  Clone the repository:
    ```bash
    git clone https://github.com/c0mpiler/novactl.git
    cd novactl
    ```
2.  Install in editable mode with development dependencies:
    ```bash
    pip install -e ".[dev]"
    ```

## Configuration

### Initial Setup

On the first run of any command requiring configuration (like `login`), `novactl` will create a default configuration file at `~/.config/novactl/novactl.yml` if one doesn't exist.

**You MUST edit this file** to provide your specific Keycloak instance details:

```yaml
# ~/.config/novactl/novactl.yml

# --- Required Keycloak Settings --- #

# Base URL of the Keycloak server (e.g., https://keycloak.example.com)
keycloak_server_url: YOUR_KEYCLOAK_SERVER_URL_HERE

# The Keycloak realm name to authenticate against.
keycloak_realm: YOUR_KEYCLOAK_REALM_HERE

# The Client ID registered in Keycloak for this CLI application.
keycloak_client_id: YOUR_CLI_CLIENT_ID_HERE

# --- Optional Settings (Defaults shown) --- #

# Space-separated list of additional OAuth scopes to request during login.
# 'offline_access' is crucial for getting refresh tokens for persistent sessions.
# Default: "openid email profile offline_access"
# additional_scopes: openid email profile offline_access custom_scope

# The service name used when storing tokens in the system keyring.
# Changing this isolates tokens if multiple instances use this boilerplate.
# Default: "novactl"
# keyring_service_name: my-awesome-cli

# Leeway (seconds) for token expiration validation to handle clock skew.
# Default: 60
# token_leeway_seconds: 60

# Verify server SSL/TLS certificates. Set to false ONLY for trusted dev environments.
# Can also be a path to a custom CA bundle file.
# Default: true
# ssl_verify: true

# Application log level for file logging (~/.config/novactl/novactl.log).
# Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Default: WARNING
# log_level: DEBUG
```

### Keycloak Client Configuration

The `keycloak_client_id` you configure must correspond to a public client in your Keycloak realm. Critical settings include:

*   **Client type:** `OpenID Connect`
*   **Client ID:** (Matches `keycloak_client_id` in `novactl.yml`)
*   **Client authentication:** `Off` (It's a public client)
*   **Authorization:** `Off`
*   **Authentication flow:** Ensure `Standard flow` and `Direct grant` are enabled. Most importantly:
    *   **Device authorization grant:** `On`
*   **Redirect URIs / Web Origins:** Typically not required for device flow.

## Usage

Get help:
```bash
novactl --help
```

### Authentication Commands

*   `novactl login`: Initiates the browser-based device flow. Follow on-screen instructions.
*   `novactl logout`: Clears local tokens from the keyring and provides the Keycloak logout URL.
*   `novactl status`: Checks if logged in and if the current tokens are valid (attempts refresh if needed).
*   `novactl whoami`: Displays user information from the ID token.
*   `novactl get-roles`: Shows roles assigned to the user from the access token.
*   `novactl tkn [access|id|refresh] [--decode]`: Displays the specified token (raw or decoded).

### Example Session

```bash
# 1. Login
novactl login
# Follow browser prompts...
# Output: Login successful. Welcome, <username>!

# 2. Check status
novactl status
# Output: Status: Logged in and session appears valid.
#         Session valid for approx: 0:04:55

# 3. See user info
novactl whoami
# Output: Displays table with user details...

# 4. View raw access token
novactl tkn
# Output: Raw JWT...

# 5. Decode ID token
novactl tkn id --decode
# Output: Decoded JSON payload...

# 6. Logout
novactl logout
# Output: Local session cleared. ... [Optional Logout URL]
```

## Using as a Boilerplate / Template

1.  **Fork or Copy:** Fork this repository or copy the `src/` directory into your project.
2.  **Rename Package:**
    *   Update the `[project.name]` in `pyproject.toml` to your CLI's name (e.g., `my-cli`).
    *   Update the script name in `[project.scripts]` (e.g., `my-cli = nova_controller_cli.main:app`).
    *   Consider renaming the `src/nova_controller_cli` directory to `src/my_cli` and update imports accordingly (in `main.py`, `tests/`, etc.).
    *   Change `keyring_service_name` in `config.py` (or `novactl.yml`) to avoid conflicts.
3.  **Customize `main.py`:**
    *   Keep the `main_callback` and `_ensure_authenticated` helper.
    *   Keep the auth commands (`login`, `logout`, `status`, `whoami`, `get-roles`, `tkn`) as they are useful for managing authentication.
    *   **Add your own commands:** Use the `@app.command()` decorator to add commands specific to your application's functionality. Protect commands requiring authentication by calling `_ensure_authenticated("your-command-name")` at the beginning.
    *   **Access Tokens:** Inside your authenticated commands, use `auth.get_tokens()` to retrieve the current valid tokens. The access token (`tokens['access_token']`) can then be used in `Authorization: Bearer <token>` headers when making API calls.
4.  **Update `pyproject.toml`:** Modify authors, description, keywords, URLs, and classifiers.
5.  **Update `README.md`:** Tailor the README to your specific CLI application.
6.  **Update `LICENSE`:** Ensure the license file reflects your chosen license (if different from MIT).
7.  **Review `config.py`:** Adjust default config values or logging setup if necessary.

## Contributing

Contributions to improve this boilerplate are welcome! Please fork the repository, create a feature branch, add tests, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
