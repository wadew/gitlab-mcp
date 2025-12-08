"""
Releases tools for GitLab MCP server.

This module provides MCP tools for GitLab release operations including:
- Listing releases
- Getting release details
- Creating releases
- Updating releases
- Deleting releases

All tools are async functions that accept a GitLabClient and return formatted data.
"""

import asyncio
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_releases(
    client: GitLabClient,
    project_id: str | int,
) -> list[dict[str, Any]]:
    """
    List project releases.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)

    Returns:
        List of release dictionaries
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.list_releases(project_id=project_id)


async def get_release(
    client: GitLabClient,
    project_id: str | int,
    tag_name: str,
) -> dict[str, Any]:
    """
    Get release details.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        tag_name: Tag name associated with the release

    Returns:
        Dictionary with release details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_release(project_id=project_id, tag_name=tag_name)


async def create_release(
    client: GitLabClient,
    project_id: str | int,
    tag_name: str,
    name: str,
    description: str | None = None,
    ref: str | None = None,
) -> None:
    """
    Create a new release.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        tag_name: Tag name for the release
        name: Release name
        description: Release description (optional)
        ref: Reference (branch/commit SHA) if tag doesn't exist (optional)

    Returns:
        None
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.create_release(
        project_id=project_id,
        tag_name=tag_name,
        name=name,
        description=description,
        ref=ref,
    )


async def update_release(
    client: GitLabClient,
    project_id: str | int,
    tag_name: str,
    name: str | None = None,
    description: str | None = None,
) -> None:
    """
    Update an existing release.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        tag_name: Tag name of the release to update
        name: New release name (optional)
        description: New release description (optional)

    Returns:
        None
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.update_release(
        project_id=project_id,
        tag_name=tag_name,
        name=name,
        description=description,
    )


async def delete_release(
    client: GitLabClient,
    project_id: str | int,
    tag_name: str,
) -> None:
    """
    Delete a release.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        tag_name: Tag name of the release to delete

    Returns:
        None
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.delete_release(project_id=project_id, tag_name=tag_name)
