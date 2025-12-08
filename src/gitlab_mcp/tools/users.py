"""
Users tools for GitLab MCP server.

This module provides MCP tools for GitLab user operations including:
- Getting user details
- Searching users
- Listing user projects

All tools are async functions that accept a GitLabClient and return formatted data.
"""

import asyncio
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def get_user(
    client: GitLabClient,
    user_id: int,
) -> dict[str, Any]:
    """
    Get user details.

    Args:
        client: Authenticated GitLabClient instance
        user_id: User ID

    Returns:
        Dictionary with user details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_user(user_id=user_id)


async def search_users(
    client: GitLabClient,
    search: str,
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    Search for users.

    Args:
        client: Authenticated GitLabClient instance
        search: Search query (username, name, or email)
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of user dictionaries
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.search_users(
        search=search,
        page=page,
        per_page=per_page,
    )


async def list_user_projects(
    client: GitLabClient,
    user_id: int,
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    List user's accessible projects.

    Args:
        client: Authenticated GitLabClient instance
        user_id: User ID
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of project dictionaries
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.list_user_projects(
        user_id=user_id,
        page=page,
        per_page=per_page,
    )
