"""
Projects tools for GitLab MCP server.

This module provides MCP tools for GitLab project management operations including:
- Listing projects
- Getting project details
- Searching projects
- Listing project members
- Getting project statistics
- Managing milestones

All tools are async functions that accept a GitLabClient and return formatted data.
"""

from typing import Any, Optional, Union

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_projects(
    client: GitLabClient,
    visibility: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List accessible projects.

    Args:
        client: Authenticated GitLabClient instance
        visibility: Filter by visibility (public, internal, private)
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        Dictionary with projects list and pagination info
    """
    return client.list_projects(
        visibility=visibility,
        page=page,
        per_page=per_page,
    )


async def get_project(
    client: GitLabClient,
    project_id: Union[str, int],
) -> Any:
    """
    Get detailed information about a specific project.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)

    Returns:
        Project object from python-gitlab
    """
    return client.get_project(project_id=project_id)


async def search_projects(
    client: GitLabClient,
    search_term: str,
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    Search for projects.

    Args:
        client: Authenticated GitLabClient instance
        search_term: Search query
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of project dictionaries
    """
    return client.search_projects(
        search_term=search_term,
        page=page,
        per_page=per_page,
    )


async def list_project_members(
    client: GitLabClient,
    project_id: Union[str, int],
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    List project members.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of member dictionaries
    """
    return client.list_project_members(
        project_id=project_id,
        page=page,
        per_page=per_page,
    )


async def get_project_statistics(
    client: GitLabClient,
    project_id: Union[str, int],
) -> dict[str, Any]:
    """
    Get project statistics.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)

    Returns:
        Dictionary with project statistics
    """
    return client.get_project_statistics(project_id=project_id)


async def list_milestones(
    client: GitLabClient,
    project_id: Union[str, int],
    state: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    List project milestones.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        state: Filter by state (active, closed)
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of milestone dictionaries
    """
    return client.list_milestones(
        project_id=project_id,
        state=state,
        page=page,
        per_page=per_page,
    )


async def get_milestone(
    client: GitLabClient,
    project_id: Union[str, int],
    milestone_id: int,
) -> dict[str, Any]:
    """
    Get milestone details.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        milestone_id: Milestone ID

    Returns:
        Dictionary with milestone details
    """
    return client.get_milestone(project_id=project_id, milestone_id=milestone_id)


async def create_milestone(
    client: GitLabClient,
    project_id: Union[str, int],
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    start_date: Optional[str] = None,
) -> dict[str, Any]:
    """
    Create a new milestone.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        title: Milestone title
        description: Milestone description (optional)
        due_date: Due date in YYYY-MM-DD format (optional)
        start_date: Start date in YYYY-MM-DD format (optional)

    Returns:
        Dictionary with created milestone details
    """
    return client.create_milestone(
        project_id=project_id,
        title=title,
        description=description,
        due_date=due_date,
        start_date=start_date,
    )


async def update_milestone(
    client: GitLabClient,
    project_id: Union[str, int],
    milestone_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    start_date: Optional[str] = None,
    state: Optional[str] = None,
) -> dict[str, Any]:
    """
    Update an existing milestone.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        milestone_id: Milestone ID
        title: New title (optional)
        description: New description (optional)
        due_date: New due date in YYYY-MM-DD format (optional)
        start_date: New start date in YYYY-MM-DD format (optional)
        state: State (optional)

    Returns:
        Dictionary with updated milestone details
    """
    return client.update_milestone(
        project_id=project_id,
        milestone_id=milestone_id,
        title=title,
        description=description,
        due_date=due_date,
        start_date=start_date,
        state=state,
    )
