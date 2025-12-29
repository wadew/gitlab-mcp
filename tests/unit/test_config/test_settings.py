"""Unit tests for configuration settings.

Tests verify:
- Loading config from environment variables
- Loading config from JSON file
- Environment variables override file settings
- Required field validation (gitlab_url, gitlab_token)
- Optional field defaults (timeout, log_level, verify_ssl)
- Token is hidden in repr() and dict export
- URL format validation
- Timeout range validation
- Log level validation
"""

import json

import pytest
from pydantic import ValidationError as PydanticValidationError

from gitlab_mcp.client.exceptions import ValidationError
from gitlab_mcp.config.settings import GitLabConfig, load_config


class TestGitLabConfigModel:
    """Test GitLabConfig Pydantic model."""

    def test_config_with_all_required_fields(self):
        """Config should accept all required fields."""
        config = GitLabConfig(gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123")
        assert config.gitlab_url == "https://gitlab.example.com"
        assert config.gitlab_token.get_secret_value() == "glpat-test123"

    def test_config_with_optional_fields(self):
        """Config should accept optional fields."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="glpat-test123",
            timeout=60,
            log_level="DEBUG",
            verify_ssl=False,
        )
        assert config.timeout == 60
        assert config.log_level == "DEBUG"
        assert config.verify_ssl is False

    def test_config_default_timeout(self):
        """Default timeout should be 30 seconds."""
        config = GitLabConfig(gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123")
        assert config.timeout == 30

    def test_config_default_log_level(self):
        """Default log level should be INFO."""
        config = GitLabConfig(gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123")
        assert config.log_level == "INFO"

    def test_config_default_verify_ssl(self):
        """Default verify_ssl should be True."""
        config = GitLabConfig(gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123")
        assert config.verify_ssl is True


class TestRequiredFieldValidation:
    """Test required field validation."""

    def test_missing_gitlab_url_raises_error(self):
        """Missing gitlab_url should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(gitlab_token="glpat-test123")

    def test_missing_gitlab_token_raises_error(self):
        """Missing gitlab_token should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(gitlab_url="https://gitlab.example.com")

    def test_empty_gitlab_url_raises_error(self):
        """Empty gitlab_url should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(gitlab_url="", gitlab_token="glpat-test123")

    def test_empty_gitlab_token_raises_error(self):
        """Empty gitlab_token should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(gitlab_url="https://gitlab.example.com", gitlab_token="")


class TestURLValidation:
    """Test GitLab URL format validation."""

    def test_valid_https_url(self):
        """Valid HTTPS URL should be accepted."""
        config = GitLabConfig(gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123")
        assert config.gitlab_url == "https://gitlab.example.com"

    def test_valid_http_url(self):
        """Valid HTTP URL should be accepted (for local/dev)."""
        config = GitLabConfig(gitlab_url="http://localhost:8080", gitlab_token="glpat-test123")
        assert config.gitlab_url == "http://localhost:8080"

    def test_url_with_path_is_accepted(self):
        """URL with path should be accepted."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com/api/v4", gitlab_token="glpat-test123"
        )
        assert "gitlab.example.com" in config.gitlab_url

    def test_invalid_url_format_raises_error(self):
        """Invalid URL format should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(gitlab_url="not-a-url", gitlab_token="glpat-test123")

    def test_url_missing_scheme_raises_error(self):
        """URL without http:// or https:// should raise error."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(gitlab_url="gitlab.example.com", gitlab_token="glpat-test123")


class TestTimeoutValidation:
    """Test timeout value validation."""

    def test_valid_timeout_value(self):
        """Valid timeout value should be accepted."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", timeout=120
        )
        assert config.timeout == 120

    def test_timeout_minimum_value(self):
        """Timeout minimum value should be 1."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", timeout=1
        )
        assert config.timeout == 1

    def test_timeout_maximum_value(self):
        """Timeout maximum value should be 300."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", timeout=300
        )
        assert config.timeout == 300

    def test_timeout_below_minimum_raises_error(self):
        """Timeout below 1 should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(
                gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", timeout=0
            )

    def test_timeout_above_maximum_raises_error(self):
        """Timeout above 300 should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(
                gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", timeout=301
            )


class TestLogLevelValidation:
    """Test log level validation."""

    def test_debug_log_level(self):
        """DEBUG log level should be accepted."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", log_level="DEBUG"
        )
        assert config.log_level == "DEBUG"

    def test_info_log_level(self):
        """INFO log level should be accepted."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", log_level="INFO"
        )
        assert config.log_level == "INFO"

    def test_warning_log_level(self):
        """WARNING log level should be accepted."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="glpat-test123",
            log_level="WARNING",
        )
        assert config.log_level == "WARNING"

    def test_error_log_level(self):
        """ERROR log level should be accepted."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-test123", log_level="ERROR"
        )
        assert config.log_level == "ERROR"

    def test_invalid_log_level_raises_error(self):
        """Invalid log level should raise ValidationError."""
        with pytest.raises((PydanticValidationError, ValidationError)):
            GitLabConfig(
                gitlab_url="https://gitlab.example.com",
                gitlab_token="glpat-test123",
                log_level="INVALID",
            )


class TestTokenSecurity:
    """Test that token is never exposed."""

    def test_token_not_in_repr(self):
        """Token should not appear in repr()."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-secret-token-123"
        )
        repr_str = repr(config)
        assert "glpat-secret-token-123" not in repr_str
        assert "***" in repr_str or "[REDACTED]" in repr_str or "SecretStr" in repr_str

    def test_token_not_in_str(self):
        """Token should not appear in str()."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-secret-token-123"
        )
        str_repr = str(config)
        assert "glpat-secret-token-123" not in str_repr

    def test_token_in_model_dump_excludes_secrets(self):
        """Token should be marked as secret in model_dump()."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com", gitlab_token="glpat-secret-token-123"
        )
        # Pydantic's SecretStr should hide the token
        dump = config.model_dump()
        # Token value should not be directly visible
        if "gitlab_token" in dump:
            assert "glpat-secret-token-123" not in str(dump["gitlab_token"])


class TestLoadConfigFromEnv:
    """Test loading configuration from environment variables."""

    def test_load_config_from_env_variables(self, monkeypatch):
        """Should load config from environment variables."""
        monkeypatch.setenv("GITLAB_URL", "https://gitlab.example.com")
        monkeypatch.setenv("GITLAB_TOKEN", "glpat-env-token")

        config = load_config()
        assert config.gitlab_url == "https://gitlab.example.com"
        # Use get_secret_value() to compare token
        assert config.gitlab_token.get_secret_value() == "glpat-env-token"

    def test_load_config_with_optional_env_vars(self, monkeypatch):
        """Should load optional fields from environment."""
        monkeypatch.setenv("GITLAB_URL", "https://gitlab.example.com")
        monkeypatch.setenv("GITLAB_TOKEN", "glpat-env-token")
        monkeypatch.setenv("GITLAB_TIMEOUT", "60")
        monkeypatch.setenv("GITLAB_LOG_LEVEL", "DEBUG")
        monkeypatch.setenv("GITLAB_VERIFY_SSL", "false")

        config = load_config()
        assert config.timeout == 60
        assert config.log_level == "DEBUG"
        assert config.verify_ssl is False

    def test_load_config_missing_required_env_raises_error(self, monkeypatch):
        """Missing required env vars should raise ValidationError."""
        # Clear any existing env vars
        monkeypatch.delenv("GITLAB_URL", raising=False)
        monkeypatch.delenv("GITLAB_TOKEN", raising=False)

        with pytest.raises((PydanticValidationError, ValidationError)):
            load_config()


class TestLoadConfigFromFile:
    """Test loading configuration from JSON file."""

    def test_load_config_from_json_file(self, tmp_path, monkeypatch):
        """Should load config from JSON file."""
        config_file = tmp_path / ".gitlab-mcp.json"
        config_data = {
            "gitlab_url": "https://gitlab.example.com",
            "gitlab_token": "glpat-file-token",
        }
        config_file.write_text(json.dumps(config_data))

        # Change to temp directory
        monkeypatch.chdir(tmp_path)
        # Clear env vars to force file loading
        monkeypatch.delenv("GITLAB_URL", raising=False)
        monkeypatch.delenv("GITLAB_TOKEN", raising=False)

        config = load_config()
        assert config.gitlab_url == "https://gitlab.example.com"
        assert config.gitlab_token.get_secret_value() == "glpat-file-token"

    def test_load_config_file_with_optional_fields(self, tmp_path, monkeypatch):
        """Should load optional fields from JSON file."""
        config_file = tmp_path / ".gitlab-mcp.json"
        config_data = {
            "gitlab_url": "https://gitlab.example.com",
            "gitlab_token": "glpat-file-token",
            "timeout": 90,
            "log_level": "WARNING",
            "verify_ssl": False,
        }
        config_file.write_text(json.dumps(config_data))

        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("GITLAB_URL", raising=False)
        monkeypatch.delenv("GITLAB_TOKEN", raising=False)

        config = load_config()
        assert config.timeout == 90
        assert config.log_level == "WARNING"
        assert config.verify_ssl is False


class TestConfigPrecedence:
    """Test that environment variables override file settings."""

    def test_env_vars_override_file_settings(self, tmp_path, monkeypatch):
        """Environment variables should take precedence over file."""
        config_file = tmp_path / ".gitlab-mcp.json"
        config_data = {
            "gitlab_url": "https://file.example.com",
            "gitlab_token": "glpat-file-token",
            "timeout": 60,
        }
        config_file.write_text(json.dumps(config_data))

        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GITLAB_URL", "https://env.example.com")
        monkeypatch.setenv("GITLAB_TOKEN", "glpat-env-token")
        monkeypatch.setenv("GITLAB_TIMEOUT", "120")

        config = load_config()
        # Env vars should win
        assert config.gitlab_url == "https://env.example.com"
        assert config.gitlab_token.get_secret_value() == "glpat-env-token"
        assert config.timeout == 120

    def test_partial_env_override(self, tmp_path, monkeypatch):
        """Partial env vars should override only those fields."""
        config_file = tmp_path / ".gitlab-mcp.json"
        config_data = {
            "gitlab_url": "https://file.example.com",
            "gitlab_token": "glpat-file-token",
            "timeout": 60,
            "log_level": "WARNING",
        }
        config_file.write_text(json.dumps(config_data))

        monkeypatch.chdir(tmp_path)
        # Clear token env var to ensure file value is used
        monkeypatch.delenv("GITLAB_TOKEN", raising=False)
        # Only override URL, not token
        monkeypatch.setenv("GITLAB_URL", "https://env.example.com")

        config = load_config()
        # URL from env, token from file
        assert config.gitlab_url == "https://env.example.com"
        assert config.gitlab_token.get_secret_value() == "glpat-file-token"
        assert config.timeout == 60


class TestConfigFileDiscovery:
    """Test config file discovery in current directory."""

    def test_config_file_not_found_uses_env_only(self, tmp_path, monkeypatch):
        """If config file doesn't exist, should use env vars only."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("GITLAB_URL", "https://env.example.com")
        monkeypatch.setenv("GITLAB_TOKEN", "glpat-env-token")

        # Should not raise error even though file doesn't exist
        config = load_config()
        assert config.gitlab_url == "https://env.example.com"

    def test_config_file_discovered_in_current_dir(self, tmp_path, monkeypatch):
        """Should discover .gitlab-mcp.json in current directory."""
        config_file = tmp_path / ".gitlab-mcp.json"
        config_data = {
            "gitlab_url": "https://gitlab.example.com",
            "gitlab_token": "glpat-file-token",
        }
        config_file.write_text(json.dumps(config_data))

        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("GITLAB_URL", raising=False)
        monkeypatch.delenv("GITLAB_TOKEN", raising=False)

        config = load_config()
        assert config.gitlab_url == "https://gitlab.example.com"
