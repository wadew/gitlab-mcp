"""Custom exception classes for GitLab MCP Server.

This module defines a hierarchy of exceptions for clear error handling:

GitLabMCPError (base)
├── ConfigurationError
│   └── ValidationError
├── GitLabAPIError
├── AuthenticationError
├── PermissionError
├── NotFoundError
├── RateLimitError
├── GitLabServerError
└── NetworkError
    └── TimeoutError
"""


class GitLabMCPError(Exception):
    """Base exception for all GitLab MCP errors.

    All custom exceptions in this module inherit from this base class,
    allowing for easy catching of any GitLab MCP related error.
    """

    def __init__(self, message: str) -> None:
        """Initialize the exception with a message.

        Args:
            message: Human-readable error message
        """
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        """Return string representation of the exception."""
        return self.message

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return f"{self.__class__.__name__}('{self.message}')"


class ConfigurationError(GitLabMCPError):
    """Raised when there is a configuration error.

    This includes missing configuration files, invalid settings,
    or other configuration-related issues.
    """

    pass


class ValidationError(ConfigurationError):
    """Raised when configuration validation fails.

    This exception is used for specific field validation errors
    and can optionally include the field name that failed validation.
    """

    def __init__(self, message: str, field_name: str | None = None) -> None:
        """Initialize ValidationError with message and optional field name.

        Args:
            message: Human-readable error message
            field_name: Name of the field that failed validation (optional)
        """
        self.field_name = field_name
        if field_name:
            full_message = f"Validation error for field '{field_name}': {message}"
        else:
            full_message = message
        super().__init__(full_message)

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        if self.field_name:
            return f"{self.__class__.__name__}('{self.message}', field_name='{self.field_name}')"
        return f"{self.__class__.__name__}('{self.message}')"


class GitLabAPIError(GitLabMCPError):
    """Raised for general GitLab API errors.

    This is a catch-all exception for GitLab API errors that don't
    fit into more specific categories. It's useful for wrapping
    unexpected errors from the python-gitlab library.
    """

    pass


class AuthenticationError(GitLabMCPError):
    """Raised when authentication fails.

    This typically occurs when:
    - Invalid or expired Personal Access Token
    - Token lacks required permissions
    - Authentication server is unreachable
    """

    pass


class PermissionError(GitLabMCPError):
    """Raised when the user lacks permission for an operation.

    This occurs when authentication succeeds but the user's token
    doesn't have the necessary scopes or project permissions.
    """

    pass


class NotFoundError(GitLabMCPError):
    """Raised when a requested resource is not found.

    This includes:
    - Projects, issues, merge requests that don't exist
    - Branches, tags, commits that can't be found
    - Any 404 responses from GitLab API
    """

    pass


class RateLimitError(GitLabMCPError):
    """Raised when GitLab API rate limit is exceeded.

    GitLab enforces rate limits on API requests. This exception
    includes retry_after information when available.
    """

    def __init__(self, message: str, retry_after: int | None = None) -> None:
        """Initialize RateLimitError with message and optional retry info.

        Args:
            message: Human-readable error message
            retry_after: Seconds to wait before retrying (optional)
        """
        self.retry_after = retry_after
        if retry_after:
            full_message = f"{message} (retry after {retry_after} seconds)"
        else:
            full_message = message
        super().__init__(full_message)

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        if self.retry_after:
            return (
                f"{self.__class__.__name__}('{self.message}', " f"retry_after={self.retry_after})"
            )
        return f"{self.__class__.__name__}('{self.message}')"


class GitLabServerError(GitLabMCPError):
    """Raised when GitLab server returns a 5xx error.

    This indicates an issue on the GitLab server side, such as:
    - Internal server errors (500)
    - Service unavailable (503)
    - Gateway timeout (504)
    """

    pass


class NetworkError(GitLabMCPError):
    """Raised when a network-related error occurs.

    This includes:
    - Connection failures
    - DNS resolution errors
    - Network timeouts
    """

    pass


class TimeoutError(NetworkError):
    """Raised when a request times out.

    This is a specific type of NetworkError for timeout scenarios.
    """

    pass
