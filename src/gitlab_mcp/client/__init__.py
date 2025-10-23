"""GitLab API client module.

This module provides a wrapper around the python-gitlab library with
MCP-specific error handling and authentication.
"""

from gitlab_mcp.client.exceptions import (
    AuthenticationError,
    ConfigurationError,
    GitLabMCPError,
    GitLabServerError,
    NetworkError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)

__all__ = [
    "GitLabMCPError",
    "ConfigurationError",
    "ValidationError",
    "AuthenticationError",
    "PermissionError",
    "NotFoundError",
    "RateLimitError",
    "GitLabServerError",
    "NetworkError",
    "TimeoutError",
]
