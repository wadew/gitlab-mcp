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

from typing import Any, Optional, Union

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_wiki_pages(
    client: GitLabClient,
    project_id: Union[str, int],
    page: Optional[int] = None,
    per_page: Optional[int] = None,
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
    return client.list_wiki_pages(project_id=project_id, page=page, per_page=per_page)


async def get_wiki_page(
    client: GitLabClient,
    project_id: Union[str, int],
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
    return client.get_wiki_page(project_id=project_id, slug=slug)


async def create_wiki_page(
    client: GitLabClient,
    project_id: Union[str, int],
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
    return client.create_wiki_page(
        project_id=project_id,
        title=title,
        content=content,
        format=format,
    )


async def update_wiki_page(
    client: GitLabClient,
    project_id: Union[str, int],
    slug: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    format: Optional[str] = None,
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
    return client.update_wiki_page(
        project_id=project_id,
        slug=slug,
        title=title,
        content=content,
        format=format,
    )


async def delete_wiki_page(
    client: GitLabClient,
    project_id: Union[str, int],
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
    client.delete_wiki_page(project_id=project_id, slug=slug)
