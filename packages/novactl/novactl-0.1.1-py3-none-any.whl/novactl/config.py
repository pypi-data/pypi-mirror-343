# -*- coding: utf-8 -*-
"""
Author: Harsha Krishnareddy
Email: c0mpiler@ins8s.dev
"""
"""Handles loading and saving of configuration for novactl."""

import json
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, Optional, Union

import jsonschema
import yaml

# --- Setup Structured Logging --- #

# Basic formatter for console output (human-readable)
cli_formatter = logging.Formatter("%(message)s")


# JSON formatter for file output (machine-readable)
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # Add exception info if present
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        # Add any extra fields
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                # Exclude standard logging attributes and potentially sensitive internal ones
                if key not in [
                    "args",
                    "asctime",
                    "created",
                    "exc_info",
                    "exc_text",
                    "filename",
                    "funcName",
                    "levelname",
                    "levelno",
                    "lineno",
                    "module",
                    "msecs",
                    "message",
                    "msg",
                    "name",
                    "pathname",
                    "process",
                    "processName",
                    "relativeCreated",
                    "stack_info",
                    "thread",
                    "threadName",
                ]:
                    # Ensure value is JSON serializable
                    if (
                        isinstance(value, (str, int, float, bool, list, dict))
                        or value is None
                    ):
                        log_record[key] = value
        return json.dumps(log_record)


# Get root logger
root_logger = logging.getLogger()  # Get the root logger
root_logger.setLevel(logging.DEBUG)  # Capture all levels at the root
root_logger.handlers.clear()  # Clear existing handlers if any (e.g., from basicConfig in main)

# Configure console handler (shows INFO and above by default)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Default console level
console_handler.setFormatter(cli_formatter)
root_logger.addHandler(console_handler)

# Placeholder for file handler (configured later based on config)
file_handler: Optional[RotatingFileHandler] = None

# Silence noisy libraries by default
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("keyring").setLevel(logging.WARNING)
logging.getLogger("jose").setLevel(logging.WARNING)

# Our own module logger instance
logger = logging.getLogger(__name__)

# --- Configuration Constants --- #
DEFAULT_CONFIG_DIR = Path.home() / ".config" / "novactl"  # Package name here
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.yml"  # Changed to config.yml
DEFAULT_SCHEMA_PATH = Path(__file__).parent / "config_schema.json"
DEFAULT_LOG_PATH = DEFAULT_CONFIG_DIR / "novactl.log"

# --- Default Configuration Values --- #
DEFAULT_CONFIG: Dict[str, Any] = {
    "keycloak_server_url": None,
    "keycloak_realm": None,
    "keycloak_client_id": None,
    "keyring_service_name": "novactl",  # Default service name
    "additional_scopes": "openid email profile offline_access",
    "token_leeway_seconds": 60,
    "ssl_verify": True,
    "log_level": "WARNING",  # Default log level for file
    "console_log_level": "INFO",  # Separate level for console
}

# --- Cached Config & Schema ---
_config: Optional[Dict[str, Any]] = None
_config_schema: Optional[Dict[str, Any]] = None
_logging_configured = False


def get_config_path() -> Path:
    """Returns the path to the configuration file, respecting NOVACTL_CONFIG_PATH env var."""
    config_path_str = os.getenv("NOVACTL_CONFIG_PATH", str(DEFAULT_CONFIG_PATH))
    return Path(config_path_str)


def _load_schema(schema_path: Path = DEFAULT_SCHEMA_PATH) -> Dict[str, Any]:
    """Loads the configuration schema from JSON file."""
    global _config_schema
    if _config_schema is None:
        try:
            if not schema_path.exists():
                logger.error(f"Schema file not found at {schema_path}")
                raise FileNotFoundError(f"Schema file missing: {schema_path}")
            with open(schema_path, "r") as f:
                _config_schema = json.load(f)
            logger.debug(f"Configuration schema loaded from {schema_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding schema file {schema_path}: {e}")
            raise ValueError(f"Invalid JSON in schema file: {schema_path}") from e
        except Exception as e:
            logger.exception(f"Unexpected error loading schema {schema_path}")
            raise
    return _config_schema


def _validate_config(config_data: Dict[str, Any], schema: Dict[str, Any]):
    """Validates configuration data against the schema."""
    try:
        jsonschema.validate(instance=config_data, schema=schema)
        logger.debug("Configuration validation successful.")
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Configuration validation failed: {e.message}")
        # Provide a more user-friendly error message
        error_path = " -> ".join(map(str, e.path))
        field_name = f"Field: '{error_path}'" if e.path else "General Structure"
        message = f"Configuration error in '{get_config_path()}': {field_name} - Issue: {e.message}"
        # Include context/schema details if helpful
        if e.context:
            message += f" - Context: {e.context}"
        if e.schema_path:
            schema_details = " -> ".join(map(str, e.schema_path))
            message += f" - Schema rule: {schema_details}"

        raise ValueError(message) from e
    except Exception:
        logger.exception(f"Unexpected error during configuration validation")
        raise ValueError(
            "An unexpected error occurred during configuration validation."
        )


def _process_ssl_verify(value: Any) -> Union[bool, str]:
    """Processes the ssl_verify config value into a format requests understands (bool or path str)."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        val_lower = value.lower()
        if val_lower == "false":
            return False
        if val_lower == "true":
            return True
        # Assume it's a path - check if it exists
        cert_path = Path(value).expanduser()  # Expand ~ character
        if cert_path.is_file():
            abs_path = str(cert_path.resolve())
            logger.debug(f"Using custom CA bundle from path: {abs_path}")
            return abs_path
        else:
            logger.warning(f"ssl_verify path '{value}' not found. Defaulting to True.")
            return True
    # Default for other types (e.g., int, None)
    logger.warning(f"Invalid type for ssl_verify: {type(value)}. Defaulting to True.")
    return True


def _derive_keyring_username(service_name: str) -> str:
    """Derives the keyring username from the service name."""
    # Ensure username is filesystem-safe and identifiable
    safe_service_name = "".join(c if c.isalnum() else "_" for c in service_name).lower()
    return f"{safe_service_name}_oauth_tokens"


def _configure_logging(file_log_level_str: str, console_log_level_str: str):
    """Configures file and console logging handlers based on config."""
    global file_handler, _logging_configured
    if _logging_configured:
        return  # Avoid adding handlers multiple times

    try:
        # Configure File Handler
        log_path = DEFAULT_LOG_PATH
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_log_level = getattr(logging, file_log_level_str.upper(), logging.WARNING)

        # Remove existing file handler if reloading config
        if file_handler:
            root_logger.removeHandler(file_handler)

        file_handler = RotatingFileHandler(
            log_path, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_handler.setLevel(file_log_level)
        file_handler.setFormatter(JsonFormatter())
        root_logger.addHandler(file_handler)
        logger.info(
            f"Structured file logging enabled at level {file_log_level_str} to {log_path}"
        )

        # Configure Console Handler Level
        console_log_level = getattr(
            logging, console_log_level_str.upper(), logging.INFO
        )
        console_handler.setLevel(console_log_level)
        logger.info(f"Console logging level set to {console_log_level_str}")

        _logging_configured = True

    except Exception:
        logger.error(f"Failed to set up file logging", exc_info=True)
        # Continue without file logging, console handler should still work
        file_handler = None
        _logging_configured = False  # Allow retry on next load if it failed


def load_config(
    path: Optional[Path] = None, force_reload: bool = False
) -> Dict[str, Any]:
    """Loads, validates, and processes configuration from YAML file."""
    global _config
    if _config is not None and not force_reload:
        return _config

    config_path = path or get_config_path()
    config_dir = config_path.parent
    raw_loaded_config = {}  # Config exactly as loaded from file
    final_config: Dict[str, Any] = {}  # Config after defaults, validation, processing
    is_new_config = False  # Initialize is_new_config to False *** CORRECTED FIX ***

    try:
        config_dir.mkdir(parents=True, exist_ok=True)

        if config_path.exists():
            logger.debug(f"Loading config from {config_path}")
            with open(config_path, "r") as f:
                loaded_yaml = yaml.safe_load(f)
                # Handle empty file case
                raw_loaded_config = loaded_yaml if isinstance(loaded_yaml, dict) else {}
            # Set is_new_config to False explicitly if file exists
            # is_new_config = False # Redundant due to initialization above
        else:
            logger.info(f"Config file not found at {config_path}. Creating default.")
            # Create a minimal default config dictionary
            default_to_save = {
                k: v
                for k, v in DEFAULT_CONFIG.items()
                if k in ["keycloak_server_url", "keycloak_realm", "keycloak_client_id"]
            }
            default_to_save["keycloak_server_url"] = "YOUR_KEYCLOAK_SERVER_URL_HERE"
            default_to_save["keycloak_realm"] = "YOUR_KEYCLOAK_REALM_HERE"
            default_to_save["keycloak_client_id"] = "YOUR_CLIENT_ID_HERE"
            # Use this default structure for initial validation
            raw_loaded_config = default_to_save
            # Mark that we need to save the full default config later
            is_new_config = True

        # --- Load Schema --- # (Do this before validation and saving)
        schema = _load_schema()

        # --- Apply Defaults & Validate --- #
        # Start with package defaults, override with loaded file, then validate
        config_with_defaults = DEFAULT_CONFIG.copy()
        config_with_defaults.update(raw_loaded_config)

        _validate_config(config_with_defaults, schema)

        # If validation passes, use the merged config for further processing
        final_config = config_with_defaults

    except FileNotFoundError as e:
        # Schema file not found is fatal
        print(f"[Critical] Configuration schema file missing: {e}. Cannot continue.")
        raise SystemExit(1)
    except ValueError as e:
        # Validation error from _validate_config or _load_schema
        print(f"[Critical] {e}. Please check the configuration file or schema.")
        raise SystemExit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config file {config_path}: {e}")
        print(f"[Critical] Could not parse YAML config: {config_path}. Details: {e}")
        raise SystemExit(1)
    except OSError as e:
        logger.error(f"Error accessing config file/dir {config_path}: {e}")
        print(
            f"[Critical] Could not read/write config file/directory: {config_dir}. Error: {e}"
        )
        raise SystemExit(1)
    except Exception as e:
        logger.exception(f"Unexpected error loading config {config_path}")
        print(f"[Critical] Unexpected error loading configuration.")
        raise SystemExit(1)

    # --- Configure Logging (based on validated config) --- #
    # This is called here to ensure logging uses levels from the loaded config
    _configure_logging(
        final_config.get("log_level", "WARNING"),
        final_config.get("console_log_level", "INFO"),
    )

    # --- Post-validation Processing --- #
    try:
        # Process ssl_verify into requests-compatible format (bool or path str)
        final_config["ssl_verify"] = _process_ssl_verify(final_config.get("ssl_verify"))
        logger.debug(f"Processed ssl_verify value: {final_config['ssl_verify']}")

        # Calculate derived keyring username
        final_config["keyring_username"] = _derive_keyring_username(
            final_config.get("keyring_service_name", "novactl")
        )
        logger.debug(f"Derived keyring username: {final_config['keyring_username']}")

        # Calculate derived OIDC endpoints
        server_url = final_config.get("keycloak_server_url", "").rstrip("/")
        realm = final_config.get("keycloak_realm", "")

        if server_url and realm:  # Should be true due to validation
            base_oidc_path = f"{server_url}/realms/{realm}/protocol/openid-connect"
            final_config["oidc_token_endpoint"] = f"{base_oidc_path}/token"
            final_config["oidc_logout_endpoint"] = f"{base_oidc_path}/logout"
            final_config["oidc_jwks_uri"] = f"{base_oidc_path}/certs"
            final_config["oidc_issuer"] = f"{server_url}/realms/{realm}"
            final_config["oidc_device_auth_endpoint"] = f"{base_oidc_path}/auth/device"
            logger.debug("Derived OIDC endpoints calculated.")
        else:
            # This case should ideally not be reachable if validation passed and schema enforces required fields
            missing = [
                k
                for k in ["keycloak_server_url", "keycloak_realm"]
                if not final_config.get(k)
            ]
            if missing:
                # Log critical error as this indicates a logic/schema mismatch
                logger.critical(
                    f"Missing required config values after validation: {', '.join(missing)}"
                )
                raise ValueError(
                    f"Internal Error: Missing required configuration values: {', '.join(missing)}"
                )

    except Exception as e:
        # Catch errors during derived value processing
        logger.exception(f"Error processing derived config values")
        print(f"[Critical] Error processing configuration values: {e}")
        raise SystemExit(1)

    # --- Save Default Config If It Was Just Created --- #
    if is_new_config:
        try:
            # Save the fully processed *default* config back to the file
            save_config(final_config, config_path)
            logger.info(f"Saved default configuration to {config_path}")
            # Don't print user messages here, handled by initial call
        except Exception:
            # Log error but continue, user can still edit the file
            logger.error(
                f"Failed to save the initial default config file to {config_path}",
                exc_info=True,
            )
            # Avoid printing during potential background load
            # print(f"[Warning] Could not automatically save the default config to {config_path}. Please check permissions.")

    # Cache the final processed config
    _config = final_config
    logger.debug(f"Configuration loaded successfully. Keys: {list(_config.keys())}")
    return _config


def save_config(config_data: Dict[str, Any], path: Optional[Path] = None):
    """Saves configuration data to YAML file, omitting defaults and derived keys."""
    config_path = path or get_config_path()
    config_dir = config_path.parent
    try:
        config_dir.mkdir(parents=True, exist_ok=True)

        # Load schema to access default values
        schema = _load_schema()
        # Ensure defaults are fetched correctly from the schema
        defaults = {
            prop: details.get("default")
            for prop, details in schema.get("properties", {}).items()
            if "default" in details
        }

        # Prepare data to save: only non-default, non-derived keys
        config_to_save = {}
        derived_keys = [
            "keyring_username",
            "oidc_token_endpoint",
            "oidc_logout_endpoint",
            "oidc_jwks_uri",
            "oidc_issuer",
            "oidc_device_auth_endpoint",
        ]

        for key, value in config_data.items():
            # Only save keys defined in the schema (properties)
            if key in schema.get("properties", {}):
                # Exclude derived keys
                if key not in derived_keys:
                    # Save if key has no default in schema OR value is different from schema default
                    if key not in defaults or value != defaults.get(key):
                        config_to_save[key] = value

        # Avoid writing an empty file if all current values match defaults
        if not config_to_save and path == DEFAULT_CONFIG_PATH:
            logger.debug(f"Skipping save to {config_path} as all values are default.")
            return

        with open(config_path, "w") as f:
            # Use sort_keys=False to maintain order from DEFAULT_CONFIG potentially
            yaml.dump(
                config_to_save, f, default_flow_style=False, sort_keys=False, indent=2
            )
        logger.info(f"Configuration saved to {config_path}")

    except OSError as e:
        logger.error(f"Error saving config file {config_path}: {e}")
        print(f"[Error] Could not save config file: {config_path}. Error: {e}")
    except Exception:
        logger.exception(f"Unexpected error saving config {config_path}")
        print(f"[Error] Unexpected error saving config: {config_path}")


def get_config_value(key: str, default: Any = None) -> Any:
    """Gets a specific value from the loaded configuration, ensuring config is loaded."""
    config_data = load_config()  # Ensures config is loaded, validated, and processed
    return config_data.get(key, default)


# Initial load attempt on import to set up logging ASAP, but handle failures gracefully.
# Errors during initial load will be caught and printed; subsequent calls will retry.
try:
    load_config()
except SystemExit:  # Catch SystemExit from load_config failures
    pass  # Error message already printed by load_config
except Exception as e:
    # Log any other unexpected error during initial load
    logger.critical(
        f"Critical error during initial config load on import: {e}", exc_info=True
    )
