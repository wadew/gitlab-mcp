"""Context tools for GitLab MCP Server.

This module provides tools for getting current context information:
- get_current_context: Get current user and instance information
- list_projects: List accessible GitLab projects
"""

import asyncio
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def get_current_context(client: GitLabClient) -> dict[str, Any]:
    """
    Get current GitLab context (user and instance information).

    This tool provides information about:
    - Current authenticated user
    - GitLab instance (URL, version)
    - Authentication status

    Args:
        client: GitLabClient instance

    Returns:
        Dictionary with:
        - user: Current user info (username, name, email, id, etc.)
        - instance: GitLab instance info (url, version)
        - authenticated: Authentication status (bool)

    Raises:
        AuthenticationError: If authentication fails
        NetworkError: If connection to GitLab fails
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    # Get user information
    user = client.get_current_user()

    # Get instance information
    instance = client.get_instance_info()

    # Build response
    result: dict[str, Any] = {
        "authenticated": True,
        "user": {},
        "instance": instance,
    }

    # Extract user attributes - handle both dict and object types
    if isinstance(user, dict):
        # User is a dictionary (from mock)
        result["user"] = user
    else:
        # User is an object (from python-gitlab)
        if hasattr(user, "username"):
            result["user"]["username"] = user.username
        if hasattr(user, "name"):
            result["user"]["name"] = user.name
        if hasattr(user, "email"):
            result["user"]["email"] = user.email
        if hasattr(user, "id"):
            result["user"]["id"] = user.id
        if hasattr(user, "is_admin"):
            result["user"]["is_admin"] = user.is_admin
        if hasattr(user, "can_create_project"):
            result["user"]["can_create_project"] = user.can_create_project

    return result


async def list_projects(
    client: GitLabClient,
    visibility: Any = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List accessible GitLab projects.

    Args:
        client: GitLabClient instance
        visibility: Filter by visibility (public, private, internal, or None for all)
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 20, max: 100)

    Returns:
        Dictionary with:
        - projects: List of project dictionaries with metadata
        - total: Total count of projects returned
        - page: Current page number
        - per_page: Results per page

    Raises:
        AuthenticationError: If authentication fails
        NetworkError: If connection to GitLab fails
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    # Get projects from client
    result = client.list_projects(
        visibility=visibility,
        page=page,
        per_page=per_page,
    )

    return result
