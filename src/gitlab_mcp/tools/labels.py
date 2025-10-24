"""
Labels tools for GitLab MCP server.

This module provides MCP tools for GitLab label operations including:
- Listing labels
- Creating labels
- Updating labels
- Deleting labels

All tools are async functions that accept a GitLabClient and return formatted data.
"""

from typing import Any, Optional, Union

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_labels(
    client: GitLabClient,
    project_id: Union[str, int],
    search: Optional[str] = None,
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
    return client.list_labels(project_id=project_id, search=search)


async def create_label(
    client: GitLabClient,
    project_id: Union[str, int],
    name: str,
    color: str,
    description: Optional[str] = None,
    priority: Optional[int] = None,
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
    return client.create_label(
        project_id=project_id,
        name=name,
        color=color,
        description=description,
        priority=priority,
    )


async def update_label(
    client: GitLabClient,
    project_id: Union[str, int],
    label_id: int,
    new_name: Optional[str] = None,
    color: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[int] = None,
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
    project_id: Union[str, int],
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
    client.delete_label(project_id=project_id, label_id=label_id)
