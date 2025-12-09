"""
Wikis tools for GitLab MCP server.

This module provides MCP tools for GitLab wiki operations including:
- Listing wiki pages
- Getting wiki page content
- Creating wiki pages
- Updating wiki pages
- Deleting wiki pages

All tools are async functions that accept a GitLabClient and return formatted data.
"""

import asyncio
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_wiki_pages(
    client: GitLabClient,
    project_id: str | int,
    page: int | None = None,
    per_page: int | None = None,
) -> list[dict[str, Any]]:
    """
    List wiki pages for a project.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        page: Page number for pagination (optional)
        per_page: Number of items per page (optional)

    Returns:
        List of wiki page dictionaries
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.list_wiki_pages(project_id=project_id, page=page, per_page=per_page)


async def get_wiki_page(
    client: GitLabClient,
    project_id: str | int,
    slug: str,
) -> dict[str, Any]:
    """
    Get wiki page content.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        slug: Wiki page slug

    Returns:
        Dictionary with wiki page content
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_wiki_page(project_id=project_id, slug=slug)


async def create_wiki_page(
    client: GitLabClient,
    project_id: str | int,
    title: str,
    content: str,
    format: str = "markdown",
) -> dict[str, Any]:
    """
    Create a new wiki page.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        title: Page title
        content: Page content
        format: Content format (markdown, rdoc, asciidoc, org)

    Returns:
        Dictionary with created wiki page details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.create_wiki_page(
        project_id=project_id,
        title=title,
        content=content,
        format=format,
    )


async def update_wiki_page(
    client: GitLabClient,
    project_id: str | int,
    slug: str,
    title: str | None = None,
    content: str | None = None,
    format: str | None = None,
) -> dict[str, Any]:
    """
    Update an existing wiki page.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        slug: Wiki page slug to update
        title: New title (optional)
        content: New content (optional)
        format: New format (optional)

    Returns:
        Dictionary with updated wiki page details
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.update_wiki_page(
        project_id=project_id,
        slug=slug,
        title=title,
        content=content,
        format=format,
    )


async def delete_wiki_page(
    client: GitLabClient,
    project_id: str | int,
    slug: str,
) -> None:
    """
    Delete a wiki page.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        slug: Wiki page slug to delete

    Returns:
        None
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.delete_wiki_page(project_id=project_id, slug=slug)
