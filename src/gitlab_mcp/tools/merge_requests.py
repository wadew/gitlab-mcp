"""
Merge Requests tools for GitLab MCP server.

This module provides MCP tools for GitLab merge request operations including:
- Listing merge requests
- Getting merge request details
- Creating merge requests
- Updating merge requests
- Merging merge requests
- Approving/unapproving merge requests
- Getting MR changes, commits, and pipelines
- Closing and reopening merge requests

All tools are async functions that accept a GitLabClient and return formatted data.
"""

from typing import Any, Optional, Union

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_merge_requests(
    client: GitLabClient,
    project_id: Union[str, int],
    state: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
) -> list[Any]:
    """
    List merge requests for a project.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        state: Filter by state ('opened', 'closed', 'merged', 'all')
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        List of merge request objects
    """
    return client.list_merge_requests(
        project_id=project_id,
        state=state,
        page=page,
        per_page=per_page,
    )


async def get_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    mr_iid: int,
) -> Any:
    """
    Get detailed information about a specific merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        mr_iid: MR IID (internal ID within the project)

    Returns:
        Merge request object
    """
    return client.get_merge_request(project_id=project_id, mr_iid=mr_iid)


async def create_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    source_branch: str,
    target_branch: str,
    title: str,
    description: Optional[str] = None,
    assignee_ids: Optional[list[int]] = None,
) -> Any:
    """
    Create a new merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        source_branch: Source branch name
        target_branch: Target branch name
        title: MR title
        description: MR description (optional)
        assignee_ids: List of user IDs to assign (optional)

    Returns:
        Created merge request object
    """
    return client.create_merge_request(
        project_id=project_id,
        source_branch=source_branch,
        target_branch=target_branch,
        title=title,
        description=description,
        assignee_ids=assignee_ids,
    )


async def update_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    mr_iid: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    labels: Optional[list[str]] = None,
    assignee_ids: Optional[list[int]] = None,
) -> Any:
    """
    Update an existing merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        mr_iid: MR IID to update
        title: New title (optional)
        description: New description (optional)
        labels: New list of labels (optional)
        assignee_ids: New list of assignee IDs (optional)

    Returns:
        Updated merge request object
    """
    return client.update_merge_request(
        project_id=project_id,
        mr_iid=mr_iid,
        title=title,
        description=description,
        labels=labels,
        assignee_ids=assignee_ids,
    )


async def merge_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    mr_iid: int,
    merge_commit_message: Optional[str] = None,
) -> Any:
    """
    Merge a merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        mr_iid: MR IID to merge
        merge_commit_message: Custom merge commit message (optional)

    Returns:
        Merged merge request object
    """
    return client.merge_merge_request(
        project_id=project_id,
        mr_iid=mr_iid,
        merge_commit_message=merge_commit_message,
    )


async def close_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    mr_iid: int,
) -> Any:
    """
    Close a merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        mr_iid: MR IID to close

    Returns:
        Closed merge request object
    """
    return client.close_merge_request(project_id=project_id, mr_iid=mr_iid)


async def reopen_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    mr_iid: int,
) -> None:
    """
    Reopen a closed merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        mr_iid: MR IID to reopen

    Returns:
        None
    """
    client.reopen_merge_request(project_id=project_id, mr_iid=mr_iid)


async def approve_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    mr_iid: int,
) -> Any:
    """
    Approve a merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        mr_iid: MR IID to approve

    Returns:
        Approval object
    """
    return client.approve_merge_request(project_id=project_id, mr_iid=mr_iid)


async def unapprove_merge_request(
    client: GitLabClient,
    project_id: Union[str, int],
    mr_iid: int,
) -> None:
    """
    Remove approval from a merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        mr_iid: MR IID to unapprove

    Returns:
        None
    """
    client.unapprove_merge_request(project_id=project_id, mr_iid=mr_iid)


async def get_merge_request_changes(
    client: GitLabClient,
    project_id: Union[str, int],
    merge_request_iid: int,
) -> dict[str, Any]:
    """
    Get changes (diff) for a merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        merge_request_iid: MR IID

    Returns:
        Dictionary with merge request changes
    """
    return client.get_merge_request_changes(
        project_id=project_id, merge_request_iid=merge_request_iid
    )


async def get_merge_request_commits(
    client: GitLabClient,
    project_id: Union[str, int],
    merge_request_iid: int,
) -> list[dict[str, Any]]:
    """
    Get commits for a merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        merge_request_iid: MR IID

    Returns:
        List of commit dictionaries
    """
    return client.get_merge_request_commits(
        project_id=project_id, merge_request_iid=merge_request_iid
    )


async def get_merge_request_pipelines(
    client: GitLabClient,
    project_id: Union[str, int],
    merge_request_iid: int,
) -> list[dict[str, Any]]:
    """
    Get pipelines for a merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        merge_request_iid: MR IID

    Returns:
        List of pipeline dictionaries
    """
    return client.get_merge_request_pipelines(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
