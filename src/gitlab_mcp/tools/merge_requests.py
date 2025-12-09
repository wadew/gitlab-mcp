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

import asyncio
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_merge_requests(
    client: GitLabClient,
    project_id: str | int,
    state: str | None = None,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.list_merge_requests(
        project_id=project_id,
        state=state,
        page=page,
        per_page=per_page,
    )


async def get_merge_request(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_merge_request(project_id=project_id, mr_iid=mr_iid)


async def create_merge_request(
    client: GitLabClient,
    project_id: str | int,
    source_branch: str,
    target_branch: str,
    title: str,
    description: str | None = None,
    assignee_ids: list[int] | None = None,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
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
    project_id: str | int,
    mr_iid: int,
    title: str | None = None,
    description: str | None = None,
    labels: list[str] | None = None,
    assignee_ids: list[int] | None = None,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
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
    project_id: str | int,
    mr_iid: int,
    merge_commit_message: str | None = None,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.merge_merge_request(
        project_id=project_id,
        mr_iid=mr_iid,
        merge_commit_message=merge_commit_message,
    )


async def close_merge_request(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.close_merge_request(project_id=project_id, mr_iid=mr_iid)


async def reopen_merge_request(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.reopen_merge_request(project_id=project_id, mr_iid=mr_iid)


async def approve_merge_request(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.approve_merge_request(project_id=project_id, mr_iid=mr_iid)


async def unapprove_merge_request(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    client.unapprove_merge_request(project_id=project_id, mr_iid=mr_iid)


async def get_merge_request_changes(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_merge_request_changes(
        project_id=project_id, merge_request_iid=merge_request_iid
    )


async def get_merge_request_commits(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_merge_request_commits(
        project_id=project_id, merge_request_iid=merge_request_iid
    )


async def get_merge_request_pipelines(
    client: GitLabClient,
    project_id: str | int,
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
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    return client.get_merge_request_pipelines(
        project_id=project_id, merge_request_iid=merge_request_iid
    )


async def add_mr_comment(
    client: GitLabClient,
    project_id: str | int,
    mr_iid: int,
    body: str,
) -> dict[str, Any]:
    """
    Add a comment to a merge request.

    This tool adds a new comment/note to an existing merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        mr_iid: MR IID (internal ID within the project)
        body: Comment text (supports Markdown)

    Returns:
        Dictionary with comment details

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or MR doesn't exist
        PermissionError: If user doesn't have permission to comment
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> comment = await add_mr_comment(
        ...     client,
        ...     "mygroup/myproject",
        ...     15,
        ...     "LGTM! This looks good to merge."
        ... )
        >>> print(f"Added comment by {comment['author']['username']}")
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    note = client.add_mr_comment(
        project_id=project_id,
        mr_iid=mr_iid,
        body=body,
    )

    # Extract author info
    author = None
    if hasattr(note, "author") and note.author:
        author = {
            "username": getattr(note.author, "username", ""),
            "name": getattr(note.author, "name", ""),
        }

    return {
        "id": note.id,
        "body": note.body,
        "author": author,
        "created_at": getattr(note, "created_at", ""),
        "updated_at": getattr(note, "updated_at", ""),
    }


async def list_mr_comments(
    client: GitLabClient,
    project_id: str | int,
    mr_iid: int,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List all comments on a merge request.

    This tool retrieves all comments/notes for a specific merge request.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        mr_iid: MR IID (internal ID within the project)
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 20, max: 100)

    Returns:
        Dictionary with comments list

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or MR doesn't exist
        PermissionError: If user doesn't have permission to view comments
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> result = await list_mr_comments(client, "mygroup/myproject", 15)
        >>> for comment in result["comments"]:
        ...     print(f"{comment['author']['username']}: {comment['body'][:50]}...")
    """
    await asyncio.sleep(0)  # Allow event loop to process other tasks
    notes = client.list_mr_comments(
        project_id=project_id,
        mr_iid=mr_iid,
        page=page,
        per_page=per_page,
    )

    # Format comments
    formatted_comments = []
    for note in notes:
        # Extract author info
        author = None
        if hasattr(note, "author") and note.author:
            author = {
                "username": getattr(note.author, "username", ""),
                "name": getattr(note.author, "name", ""),
            }

        formatted_comments.append(
            {
                "id": note.id,
                "body": note.body,
                "author": author,
                "created_at": getattr(note, "created_at", ""),
                "updated_at": getattr(note, "updated_at", ""),
            }
        )

    return {
        "comments": formatted_comments,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(formatted_comments),
        },
    }
