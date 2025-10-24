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

from typing import Any, Optional, Union

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_releases(
    client: GitLabClient,
    project_id: Union[str, int],
) -> list[dict[str, Any]]:
    """
    List project releases.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)

    Returns:
        List of release dictionaries
    """
    return client.list_releases(project_id=project_id)


async def get_release(
    client: GitLabClient,
    project_id: Union[str, int],
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
    return client.get_release(project_id=project_id, tag_name=tag_name)


async def create_release(
    client: GitLabClient,
    project_id: Union[str, int],
    tag_name: str,
    name: str,
    description: Optional[str] = None,
    ref: Optional[str] = None,
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
    client.create_release(
        project_id=project_id,
        tag_name=tag_name,
        name=name,
        description=description,
        ref=ref,
    )


async def update_release(
    client: GitLabClient,
    project_id: Union[str, int],
    tag_name: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
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
    client.update_release(
        project_id=project_id,
        tag_name=tag_name,
        name=name,
        description=description,
    )


async def delete_release(
    client: GitLabClient,
    project_id: Union[str, int],
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
    client.delete_release(project_id=project_id, tag_name=tag_name)
