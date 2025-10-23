"""
Unit tests for GitLab Client.

Tests the GitLabClient class which wraps python-gitlab library and handles
authentication, error conversion, and basic API operations.
"""

from unittest.mock import Mock, patch

import pytest
from gitlab import GitlabAuthenticationError, GitlabGetError, GitlabHttpError
from gitlab.exceptions import GitlabError

from gitlab_mcp.client.exceptions import (
    AuthenticationError,
    GitLabAPIError,
    GitLabServerError,
    NotFoundError,
    PermissionError,
    RateLimitError,
)
from gitlab_mcp.client.gitlab_client import GitLabClient
from gitlab_mcp.config.settings import GitLabConfig


class TestGitLabClientInitialization:
    """Test GitLabClient initialization and lazy connection."""

    def test_client_initialization(self):
        """Test that client initializes with a GitLabConfig."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        client = GitLabClient(config)

        assert client.config == config
        assert client._gitlab is None  # Lazy connection - not connected yet

    def test_lazy_connection(self):
        """Test that client doesn't connect to GitLab on __init__."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        # Should not make any API calls during __init__
        with patch("gitlab_mcp.client.gitlab_client.Gitlab") as mock_gitlab:
            _ = GitLabClient(config)
            mock_gitlab.assert_not_called()


class TestGitLabClientAuthentication:
    """Test authentication and connection to GitLab."""

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_authenticate_success(self, mock_gitlab_class):
        """Test successful authentication to GitLab."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        # Mock the Gitlab instance
        mock_gitlab_instance = Mock()
        mock_gitlab_instance.auth.return_value = None
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client.authenticate()

        # Verify Gitlab was instantiated correctly
        mock_gitlab_class.assert_called_once_with(
            url="https://gitlab.example.com",
            private_token="test-token-123",
            timeout=30,  # Default timeout
        )

        # Verify auth was called
        mock_gitlab_instance.auth.assert_called_once()

        # Verify client is connected
        assert client._gitlab is not None

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_authenticate_invalid_token(self, mock_gitlab_class):
        """Test that invalid token raises AuthenticationError."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="invalid-token",
        )

        # Mock authentication failure
        mock_gitlab_instance = Mock()
        mock_gitlab_instance.auth.side_effect = GitlabAuthenticationError()
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)

        with pytest.raises(AuthenticationError) as exc_info:
            client.authenticate()

        assert "authentication failed" in str(exc_info.value).lower()

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_authenticate_network_error(self, mock_gitlab_class):
        """Test that network errors during auth raise GitLabAPIError."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        # Mock network error
        mock_gitlab_instance = Mock()
        mock_gitlab_instance.auth.side_effect = ConnectionError("Network unreachable")
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)

        with pytest.raises(GitLabAPIError) as exc_info:
            client.authenticate()

        assert "network unreachable" in str(exc_info.value).lower()


class TestGitLabClientOperations:
    """Test basic GitLab API operations."""

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_get_current_user_success(self, mock_gitlab_class):
        """Test getting current authenticated user."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        # Mock the user object
        mock_user = Mock()
        mock_user.username = "testuser"
        mock_user.email = "testuser@example.com"
        mock_user.id = 42

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.user = mock_user
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()  # Skip actual auth
        client._gitlab = mock_gitlab_instance

        user = client.get_current_user()

        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        assert user.id == 42

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_get_version_success(self, mock_gitlab_class):
        """Test getting GitLab server version."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        # Mock version info
        mock_version = {"version": "16.5.0", "revision": "abc123"}

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.return_value = mock_version
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        version = client.get_version()

        assert version["version"] == "16.5.0"
        assert version["revision"] == "abc123"

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_health_check_success(self, mock_gitlab_class):
        """Test health check returns True for healthy server."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.return_value = {"version": "16.5.0"}
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        is_healthy = client.health_check()

        assert is_healthy is True

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_health_check_failure(self, mock_gitlab_class):
        """Test health check returns False on error."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.side_effect = GitlabError("Server error")
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        is_healthy = client.health_check()

        assert is_healthy is False


class TestGitLabClientErrorHandling:
    """Test conversion of python-gitlab errors to custom exceptions."""

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_handle_401_error(self, mock_gitlab_class):
        """Test that 401 errors are converted to AuthenticationError."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        # Create a mock response with 401 status
        mock_response = Mock()
        mock_response.status_code = 401

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.side_effect = GitlabAuthenticationError(response_code=401)
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        with pytest.raises(AuthenticationError):
            client.get_version()

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_handle_403_error(self, mock_gitlab_class):
        """Test that 403 errors are converted to PermissionError."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.side_effect = GitlabHttpError(
            response_code=403, response_body=b"Forbidden"
        )
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        with pytest.raises(PermissionError):
            client.get_version()

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_handle_404_error(self, mock_gitlab_class):
        """Test that 404 errors are converted to NotFoundError."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.side_effect = GitlabGetError(
            response_code=404, response_body=b"Not Found"
        )
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        with pytest.raises(NotFoundError):
            client.get_version()

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_handle_429_rate_limit(self, mock_gitlab_class):
        """Test that 429 errors are converted to RateLimitError."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.side_effect = GitlabHttpError(
            response_code=429, response_body=b"Rate limit exceeded"
        )
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        with pytest.raises(RateLimitError):
            client.get_version()

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_handle_500_server_error(self, mock_gitlab_class):
        """Test that 5xx errors are converted to GitLabServerError."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.version.side_effect = GitlabHttpError(
            response_code=500, response_body=b"Internal Server Error"
        )
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client._ensure_authenticated = Mock()
        client._gitlab = mock_gitlab_instance

        with pytest.raises(GitLabServerError):
            client.get_version()


class TestGitLabClientEnsureAuthenticated:
    """Test the _ensure_authenticated helper method."""

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_ensure_authenticated_when_not_connected(self, mock_gitlab_class):
        """Test _ensure_authenticated calls authenticate if not connected."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.auth.return_value = None
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)

        # Should not be authenticated initially
        assert client._gitlab is None

        # Call ensure_authenticated
        client._ensure_authenticated()

        # Should now be authenticated
        assert client._gitlab is not None
        mock_gitlab_instance.auth.assert_called_once()

    @patch("gitlab_mcp.client.gitlab_client.Gitlab")
    def test_ensure_authenticated_when_already_connected(self, mock_gitlab_class):
        """Test _ensure_authenticated skips auth if already connected."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        mock_gitlab_instance = Mock()
        mock_gitlab_instance.auth.return_value = None
        mock_gitlab_class.return_value = mock_gitlab_instance

        client = GitLabClient(config)
        client.authenticate()  # Connect once

        # Reset the mock to check it's not called again
        mock_gitlab_instance.auth.reset_mock()

        # Call ensure_authenticated again
        client._ensure_authenticated()

        # Should NOT call auth again
        mock_gitlab_instance.auth.assert_not_called()
