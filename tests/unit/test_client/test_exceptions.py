"""Unit tests for custom exception classes.

Tests verify:
- Exception hierarchy (all inherit from GitLabMCPError)
- Exception messages are stored and accessible
- Special exception attributes (field names, retry info, etc.)
- String representations are clear and helpful
"""

from gitlab_mcp.client.exceptions import (
    AuthenticationError,
    ConfigurationError,
    GitLabAPIError,
    GitLabMCPError,
    GitLabServerError,
    NetworkError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)


class TestExceptionHierarchy:
    """Test that all custom exceptions inherit from GitLabMCPError."""

    def test_configuration_error_inherits_from_base(self):
        """ConfigurationError should inherit from GitLabMCPError."""
        assert issubclass(ConfigurationError, GitLabMCPError)

    def test_validation_error_inherits_from_configuration_error(self):
        """ValidationError should inherit from ConfigurationError."""
        assert issubclass(ValidationError, ConfigurationError)
        assert issubclass(ValidationError, GitLabMCPError)

    def test_gitlab_api_error_inherits_from_base(self):
        """GitLabAPIError should inherit from GitLabMCPError."""
        assert issubclass(GitLabAPIError, GitLabMCPError)

    def test_authentication_error_inherits_from_base(self):
        """AuthenticationError should inherit from GitLabMCPError."""
        assert issubclass(AuthenticationError, GitLabMCPError)

    def test_permission_error_inherits_from_base(self):
        """PermissionError should inherit from GitLabMCPError."""
        assert issubclass(PermissionError, GitLabMCPError)

    def test_not_found_error_inherits_from_base(self):
        """NotFoundError should inherit from GitLabMCPError."""
        assert issubclass(NotFoundError, GitLabMCPError)

    def test_rate_limit_error_inherits_from_base(self):
        """RateLimitError should inherit from GitLabMCPError."""
        assert issubclass(RateLimitError, GitLabMCPError)

    def test_gitlab_server_error_inherits_from_base(self):
        """GitLabServerError should inherit from GitLabMCPError."""
        assert issubclass(GitLabServerError, GitLabMCPError)

    def test_network_error_inherits_from_base(self):
        """NetworkError should inherit from GitLabMCPError."""
        assert issubclass(NetworkError, GitLabMCPError)

    def test_timeout_error_inherits_from_network_error(self):
        """TimeoutError should inherit from NetworkError."""
        assert issubclass(TimeoutError, NetworkError)
        assert issubclass(TimeoutError, GitLabMCPError)


class TestExceptionMessages:
    """Test that exceptions accept and store messages."""

    def test_base_exception_accepts_message(self):
        """GitLabMCPError should accept and store message."""
        error = GitLabMCPError("Test error message")
        assert str(error) == "Test error message"

    def test_configuration_error_accepts_message(self):
        """ConfigurationError should accept and store message."""
        error = ConfigurationError("Invalid configuration")
        assert str(error) == "Invalid configuration"

    def test_validation_error_accepts_message(self):
        """ValidationError should accept and store message."""
        error = ValidationError("Invalid field value")
        assert str(error) == "Invalid field value"

    def test_gitlab_api_error_accepts_message(self):
        """GitLabAPIError should accept and store message."""
        error = GitLabAPIError("API error occurred")
        assert str(error) == "API error occurred"

    def test_authentication_error_accepts_message(self):
        """AuthenticationError should accept and store message."""
        error = AuthenticationError("Invalid token")
        assert str(error) == "Invalid token"

    def test_permission_error_accepts_message(self):
        """PermissionError should accept and store message."""
        error = PermissionError("Access denied")
        assert str(error) == "Access denied"

    def test_not_found_error_accepts_message(self):
        """NotFoundError should accept and store message."""
        error = NotFoundError("Resource not found")
        assert str(error) == "Resource not found"

    def test_rate_limit_error_accepts_message(self):
        """RateLimitError should accept and store message."""
        error = RateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"

    def test_gitlab_server_error_accepts_message(self):
        """GitLabServerError should accept and store message."""
        error = GitLabServerError("Internal server error")
        assert str(error) == "Internal server error"

    def test_network_error_accepts_message(self):
        """NetworkError should accept and store message."""
        error = NetworkError("Connection failed")
        assert str(error) == "Connection failed"

    def test_timeout_error_accepts_message(self):
        """TimeoutError should accept and store message."""
        error = TimeoutError("Request timed out")
        assert str(error) == "Request timed out"


class TestValidationError:
    """Test ValidationError specific functionality."""

    def test_validation_error_stores_field_name(self):
        """ValidationError should store field name when provided."""
        error = ValidationError("Invalid value", field_name="gitlab_url")
        assert error.field_name == "gitlab_url"

    def test_validation_error_includes_field_in_message(self):
        """ValidationError message should include field name."""
        error = ValidationError("Invalid URL format", field_name="gitlab_url")
        error_str = str(error)
        assert "gitlab_url" in error_str
        assert "Invalid URL format" in error_str

    def test_validation_error_without_field_name(self):
        """ValidationError should work without field name."""
        error = ValidationError("General validation error")
        assert str(error) == "General validation error"
        assert error.field_name is None


class TestRateLimitError:
    """Test RateLimitError specific functionality."""

    def test_rate_limit_error_stores_retry_after(self):
        """RateLimitError should store retry_after when provided."""
        error = RateLimitError("Rate limit exceeded", retry_after=60)
        assert error.retry_after == 60

    def test_rate_limit_error_includes_retry_in_message(self):
        """RateLimitError message should include retry_after."""
        error = RateLimitError("Rate limit exceeded", retry_after=120)
        error_str = str(error)
        assert "120" in error_str or "retry" in error_str.lower()

    def test_rate_limit_error_without_retry_after(self):
        """RateLimitError should work without retry_after."""
        error = RateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"
        assert error.retry_after is None


class TestExceptionRepresentation:
    """Test exception string representations are clear."""

    def test_exception_repr_includes_class_name(self):
        """Exception repr should include class name."""
        error = AuthenticationError("Invalid token")
        repr_str = repr(error)
        assert "AuthenticationError" in repr_str

    def test_exception_repr_includes_message(self):
        """Exception repr should include message."""
        error = NotFoundError("Project not found")
        repr_str = repr(error)
        assert "Project not found" in repr_str

    def test_validation_error_repr_includes_field(self):
        """ValidationError repr should include field name."""
        error = ValidationError("Invalid format", field_name="timeout")
        repr_str = repr(error)
        assert "timeout" in repr_str

    def test_rate_limit_error_repr_includes_retry(self):
        """RateLimitError repr should include retry_after."""
        error = RateLimitError("Rate limit exceeded", retry_after=90)
        repr_str = repr(error)
        assert "90" in repr_str
