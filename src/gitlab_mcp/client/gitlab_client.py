"""
GitLab Client wrapper.

This module provides a wrapper around the python-gitlab library, handling:
- Authentication and connection management
- Error conversion to custom exceptions
- Rate limit tracking
- Basic GitLab API operations
"""

from typing import Any, Optional

from gitlab import Gitlab
from gitlab.exceptions import (
    GitlabAuthenticationError,
    GitlabGetError,
    GitlabHttpError,
)

from gitlab_mcp.client.exceptions import (
    AuthenticationError,
    GitLabAPIError,
    GitLabServerError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)
from gitlab_mcp.config.settings import GitLabConfig


class GitLabClient:
    """
    Wrapper around python-gitlab library.

    Provides a higher-level interface to GitLab API with:
    - Lazy connection (doesn't connect on __init__)
    - Automatic error conversion to custom exceptions
    - Rate limit tracking
    - Basic operations (get user, version, health check)

    Attributes:
        config: GitLab configuration settings
        _gitlab: Internal python-gitlab client (None until authenticated)
    """

    def __init__(self, config: GitLabConfig) -> None:
        """
        Initialize GitLab client with configuration.

        Args:
            config: GitLab configuration settings

        Note:
            Does NOT connect to GitLab immediately (lazy connection).
            Call authenticate() or use any method that calls _ensure_authenticated().
        """
        self.config = config
        self._gitlab: Optional[Gitlab] = None

    def authenticate(self) -> None:
        """
        Authenticate and connect to GitLab.

        Creates the python-gitlab client and authenticates with the token.

        Raises:
            AuthenticationError: If authentication fails (invalid token, wrong URL, etc.)
            GitLabAPIError: If network or other errors occur
        """
        try:
            # Create the python-gitlab client
            self._gitlab = Gitlab(
                url=self.config.gitlab_url,
                private_token=self.config.gitlab_token.get_secret_value(),
                timeout=self.config.timeout,
            )

            # Authenticate
            self._gitlab.auth()

        except GitlabAuthenticationError as e:
            raise AuthenticationError("GitLab authentication failed") from e
        except (ConnectionError, OSError) as e:
            raise GitLabAPIError(f"Network error: {str(e).lower()}") from e
        except Exception as e:
            raise GitLabAPIError(f"Unexpected error during authentication: {str(e)}") from e

    def _ensure_authenticated(self) -> None:
        """
        Ensure client is authenticated, authenticate if not.

        This is called by all API methods to ensure connection is established.
        """
        if self._gitlab is None:
            self.authenticate()

    def get_current_user(self) -> Any:
        """
        Get the currently authenticated user.

        Returns:
            User object from python-gitlab

        Raises:
            AuthenticationError: If not authenticated or auth token invalid
            GitLabAPIError: If API call fails
        """
        self._ensure_authenticated()

        try:
            return self._gitlab.user  # type: ignore
        except GitlabAuthenticationError as e:
            raise AuthenticationError("Failed to get current user") from e
        except Exception as e:
            raise self._convert_exception(e) from e

    def get_version(self) -> dict[str, str]:
        """
        Get GitLab server version information.

        Returns:
            Dictionary with version info (e.g., {"version": "16.5.0", "revision": "abc123"})

        Raises:
            AuthenticationError: If not authenticated
            GitLabAPIError: If API call fails
        """
        self._ensure_authenticated()

        try:
            return self._gitlab.version()  # type: ignore
        except GitlabAuthenticationError as e:
            raise AuthenticationError("Authentication required") from e
        except Exception as e:
            raise self._convert_exception(e) from e

    def health_check(self) -> bool:
        """
        Check if GitLab server is healthy and accessible.

        Returns:
            True if server is healthy, False otherwise
        """
        self._ensure_authenticated()

        try:
            self._gitlab.version()  # type: ignore
            return True
        except Exception:
            return False

    def _convert_exception(self, exc: Exception) -> Exception:
        """
        Convert python-gitlab exceptions to our custom exceptions.

        Args:
            exc: The original exception from python-gitlab

        Returns:
            Our custom exception with appropriate type
        """
        # Handle HTTP errors with status codes
        if isinstance(exc, GitlabHttpError):
            status_code = getattr(exc, "response_code", None)

            if status_code == 401:
                return AuthenticationError("Authentication failed (401)")
            elif status_code == 403:
                return PermissionError("Permission denied (403)")
            elif status_code == 404:
                return NotFoundError("Resource not found (404)")
            elif status_code == 429:
                return RateLimitError("Rate limit exceeded (429)")
            elif status_code and 500 <= status_code < 600:
                return GitLabServerError(f"GitLab server error ({status_code})")

        # Handle specific GitLab exceptions
        if isinstance(exc, GitlabAuthenticationError):
            return AuthenticationError("Authentication failed")
        elif isinstance(exc, GitlabGetError):
            status_code = getattr(exc, "response_code", None)
            if status_code == 404:
                return NotFoundError("Resource not found")

        # Default to generic API error
        return GitLabAPIError(f"GitLab API error: {str(exc)}")
