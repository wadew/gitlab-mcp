"""
Labels tools for GitLab MCP server.

This module provides MCP tools for GitLab label operations including:
- Listing labels
- Creating labels
- Updating labels
- Deleting labels

All tools are async functions that accept a GitLabClient and return formatted data.
"""

import asyncio
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_labels(
    client: GitLabClient,
    project_id: str | int,
    search: str | None = None,
) -> list[dict[str, Any]]:
    """
    List project labels.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        search: Optional search term to filter labels

    Returns:
        List of label dictionaries
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.list_labels(project_id=project_id, search=search)


async def create_label(
    client: GitLabClient,
    project_id: str | int,
    name: str,
    color: str,
    description: str | None = None,
    priority: int | None = None,
) -> dict[str, Any]:
    """
    Create a new label.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        name: Label name
        color: Label color (hex format like #FF0000)
        description: Label description (optional)
        priority: Label priority (optional)

    Returns:
        Dictionary with created label details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.create_label(
        project_id=project_id,
        name=name,
        color=color,
        description=description,
        priority=priority,
    )


async def update_label(
    client: GitLabClient,
    project_id: str | int,
    label_id: int,
    new_name: str | None = None,
    color: str | None = None,
    description: str | None = None,
    priority: int | None = None,
) -> dict[str, Any]:
    """
    Update an existing label.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        label_id: Label ID
        new_name: New name for the label (optional)
        color: New color (hex format) (optional)
        description: New description (optional)
        priority: New priority (optional)

    Returns:
        Dictionary with updated label details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.update_label(
        project_id=project_id,
        label_id=label_id,
        new_name=new_name,
        color=color,
        description=description,
        priority=priority,
    )


async def delete_label(
    client: GitLabClient,
    project_id: str | int,
    label_id: int,
) -> None:
    """
    Delete a label.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        label_id: Label ID to delete

    Returns:
        None
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.delete_label(project_id=project_id, label_id=label_id)
