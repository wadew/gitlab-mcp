"""
Groups tools for GitLab MCP server.

This module provides MCP tools for GitLab group operations including:
- Listing groups
- Getting group details
- Listing group members

All tools are async functions that accept a GitLabClient and return formatted data.
"""

from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_groups(
    client: GitLabClient,
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    List accessible groups.

    Args:
        client: Authenticated GitLabClient instance
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of group dictionaries
    """
    return client.list_groups(
        page=page,
        per_page=per_page,
    )


async def get_group(
    client: GitLabClient,
    group_id: str | int,
) -> dict[str, Any]:
    """
    Get group details.

    Args:
        client: Authenticated GitLabClient instance
        group_id: Group ID (int) or path (str)

    Returns:
        Dictionary with group details
    """
    return client.get_group(group_id=group_id)


async def list_group_members(
    client: GitLabClient,
    group_id: str | int,
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    List group members.

    Args:
        client: Authenticated GitLabClient instance
        group_id: Group ID (int) or path (str)
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of member dictionaries
    """
    return client.list_group_members(
        group_id=group_id,
        page=page,
        per_page=per_page,
    )
