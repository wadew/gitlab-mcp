"""Configuration settings for GitLab MCP Server.

This module provides:
- GitLabConfig Pydantic model with validation
- load_config() function to load from env vars or file
- Field validators for URL, timeout, and log level
- Automatic token redaction in string representations
"""

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import (
    Field,
    SecretStr,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class GitLabConfig(BaseSettings):
    """GitLab MCP Server configuration model.

    Configuration can be loaded from:
    1. Environment variables (GITLAB_URL, GITLAB_TOKEN, etc.)
    2. JSON file (.gitlab-mcp.json in current directory)

    Environment variables take precedence over file settings.

    Attributes:
        gitlab_url: GitLab instance URL (required)
        gitlab_token: Personal Access Token (required, secret)
        timeout: Request timeout in seconds (default: 30, range: 1-300)
        log_level: Logging level (default: INFO)
        verify_ssl: Verify SSL certificates (default: True)
    """

    model_config = SettingsConfigDict(env_prefix="GITLAB_", case_sensitive=False, extra="ignore")

    # Required fields
    gitlab_url: str = Field(
        ..., description="GitLab instance URL (e.g., https://gitlab.com)", min_length=1
    )

    gitlab_token: SecretStr = Field(..., description="GitLab Personal Access Token", min_length=1)

    # Optional fields with defaults
    timeout: int = Field(default=30, description="Request timeout in seconds", ge=1, le=300)

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )

    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")

    @field_validator("gitlab_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate that gitlab_url is a valid URL with scheme.

        Args:
            v: URL string to validate

        Returns:
            Validated URL string

        Raises:
            ValueError: If URL is invalid or missing scheme
        """
        if not v:
            raise ValueError("gitlab_url cannot be empty")

        # Check for URL scheme
        if not v.startswith(("http://", "https://")):
            raise ValueError("gitlab_url must include scheme (http:// or https://). " f"Got: {v}")

        # Basic URL validation - check for domain
        url_parts = v.replace("http://", "").replace("https://", "").split("/")
        domain = url_parts[0]
        if not domain or "." not in domain and "localhost" not in domain:
            raise ValueError(f"gitlab_url appears invalid. Got: {v}")

        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: int) -> int:
        """Validate timeout is within acceptable range.

        Args:
            v: Timeout value in seconds

        Returns:
            Validated timeout value

        Raises:
            ValueError: If timeout is outside range [1, 300]
        """
        if v < 1:
            raise ValueError("timeout must be at least 1 second")
        if v > 300:
            raise ValueError("timeout must not exceed 300 seconds")
        return v

    def __repr__(self) -> str:
        """Return string representation with redacted token.

        Returns:
            String representation safe for logging
        """
        return (
            f"GitLabConfig(gitlab_url='{self.gitlab_url}', "
            f"gitlab_token='***', "
            f"timeout={self.timeout}, "
            f"log_level='{self.log_level}', "
            f"verify_ssl={self.verify_ssl})"
        )

    def __str__(self) -> str:
        """Return human-readable string with redacted token.

        Returns:
            Human-readable string safe for logging
        """
        return self.__repr__()


def load_config(config_file: Path | None = None) -> GitLabConfig:
    """Load configuration from environment variables and/or file.

    Configuration sources (in order of precedence):
    1. Environment variables (GITLAB_URL, GITLAB_TOKEN, etc.)
    2. JSON configuration file (.gitlab-mcp.json or specified file)

    Environment variables always override file settings.

    Args:
        config_file: Optional path to config file. If not provided,
                    looks for .gitlab-mcp.json in current directory.

    Returns:
        GitLabConfig instance with loaded configuration

    Raises:
        ValidationError: If required fields are missing or invalid

    Examples:
        >>> config = load_config()  # Load from env/file
        >>> config = load_config(Path("/path/to/config.json"))  # Specific file
    """
    # Determine config file path
    if config_file is None:
        config_file = Path.cwd() / ".gitlab-mcp.json"

    # Build settings from file if it exists
    settings_kwargs = {}

    if config_file.exists():
        try:
            with open(config_file) as f:
                file_config = json.load(f)
                settings_kwargs.update(file_config)
        except (OSError, json.JSONDecodeError):
            # If file is invalid, just skip it and use env vars
            pass

    # Now override with environment variables (they take precedence)
    # Check for each env var and override file values if present
    env_vars = {
        "gitlab_url": os.getenv("GITLAB_URL"),
        "gitlab_token": os.getenv("GITLAB_TOKEN"),
        "timeout": os.getenv("GITLAB_TIMEOUT"),
        "log_level": os.getenv("GITLAB_LOG_LEVEL"),
        "verify_ssl": os.getenv("GITLAB_VERIFY_SSL"),
    }

    for key, value in env_vars.items():
        if value is not None:
            # Convert string values to appropriate types
            if key == "timeout":
                settings_kwargs[key] = int(value)
            elif key == "verify_ssl":
                settings_kwargs[key] = value.lower() in ("true", "1", "yes")
            else:
                settings_kwargs[key] = value

    # Create config with merged settings
    config = GitLabConfig(**settings_kwargs)

    return config
