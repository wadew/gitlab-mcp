"""
Snippets tools for GitLab MCP server.

This module provides MCP tools for GitLab snippet operations including:
- Listing snippets
- Getting snippet details
- Creating snippets
- Updating snippets
- Deleting snippets

All tools are async functions that accept a GitLabClient and return formatted data.
"""

import asyncio
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_snippets(
    client: GitLabClient,
    project_id: str | int,
) -> list[dict[str, Any]]:
    """
    List project snippets.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)

    Returns:
        List of snippet dictionaries
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.list_snippets(project_id=project_id)


async def get_snippet(
    client: GitLabClient,
    project_id: str | int,
    snippet_id: int,
) -> dict[str, Any]:
    """
    Get snippet details.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        snippet_id: Snippet ID

    Returns:
        Dictionary with snippet details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_snippet(project_id=project_id, snippet_id=snippet_id)


async def create_snippet(
    client: GitLabClient,
    project_id: str | int,
    title: str,
    file_name: str,
    content: str,
    description: str | None = None,
    visibility: str = "private",
) -> dict[str, Any]:
    """
    Create a new snippet.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        title: Snippet title
        file_name: File name
        content: Snippet content
        description: Snippet description (optional)
        visibility: Visibility level (private, internal, public)

    Returns:
        Dictionary with created snippet details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.create_snippet(
        project_id=project_id,
        title=title,
        file_name=file_name,
        content=content,
        description=description,
        visibility=visibility,
    )


async def update_snippet(
    client: GitLabClient,
    project_id: str | int,
    snippet_id: int,
    title: str | None = None,
    file_name: str | None = None,
    content: str | None = None,
    description: str | None = None,
    visibility: str | None = None,
) -> dict[str, Any]:
    """
    Update an existing snippet.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        snippet_id: Snippet ID to update
        title: New title (optional)
        file_name: New file name (optional)
        content: New content (optional)
        description: New description (optional)
        visibility: New visibility level (optional)

    Returns:
        Dictionary with updated snippet details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.update_snippet(
        project_id=project_id,
        snippet_id=snippet_id,
        title=title,
        file_name=file_name,
        content=content,
        description=description,
        visibility=visibility,
    )


async def delete_snippet(
    client: GitLabClient,
    project_id: str | int,
    snippet_id: int,
) -> None:
    """
    Delete a snippet.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        snippet_id: Snippet ID to delete

    Returns:
        None
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.delete_snippet(project_id=project_id, snippet_id=snippet_id)
