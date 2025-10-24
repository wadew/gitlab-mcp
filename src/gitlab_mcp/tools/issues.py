"""
Issues tools for GitLab MCP server.

This module provides MCP tools for GitLab issues operations including:
- Listing issues
- Getting issue details
- Creating issues
- Updating issues
- Managing issue comments

All tools are async functions that accept a GitLabClient and return formatted data.
"""

from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_issues(
    client: GitLabClient,
    project_id: str | int,
    state: str | None = None,
    labels: list[str] | None = None,
    milestone: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List issues for a project.

    This tool retrieves a list of issues for a GitLab project with optional
    filtering by state, labels, and milestone.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        state: Filter by state ('opened', 'closed', 'all'). Default: None (all states)
        labels: List of label names to filter by. Default: None
        milestone: Milestone title to filter by. Default: None
        page: Page number for pagination. Default: 1
        per_page: Results per page (max 100). Default: 20

    Returns:
        Dictionary with issues list and pagination info:
        {
            "issues": [
                {
                    "iid": int,
                    "title": str,
                    "description": str,
                    "state": str (opened/closed),
                    "labels": [str],
                    "web_url": str,
                    "created_at": str (ISO 8601),
                    "updated_at": str (ISO 8601),
                    "closed_at": str | None (ISO 8601),
                    "author": {"username": str, "name": str} | None,
                    "assignees": [{"username": str, "name": str}],
                    "milestone": {"title": str, "web_url": str} | None
                }
            ],
            "pagination": {
                "page": int,
                "per_page": int,
                "total": int
            }
        }

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project doesn't exist
        PermissionError: If user doesn't have permission to access project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> result = await list_issues(client, "mygroup/myproject", state="opened")
        >>> for issue in result["issues"]:
        ...     print(f"#{issue['iid']}: {issue['title']}")
    """
    # Get issues from GitLab
    issues = client.list_issues(
        project_id=project_id,
        state=state,
        labels=labels,
        milestone=milestone,
        page=page,
        per_page=per_page,
    )

    # Format issues
    formatted_issues = []
    for issue in issues:
        # Extract author info
        author = None
        if hasattr(issue, "author") and issue.author:
            author = {
                "username": getattr(issue.author, "username", ""),
                "name": getattr(issue.author, "name", ""),
            }

        # Extract assignees
        assignees = []
        if hasattr(issue, "assignees") and issue.assignees:
            # Handle both list and non-iterable assignees
            try:
                for assignee in issue.assignees:
                    assignees.append(
                        {
                            "username": getattr(assignee, "username", ""),
                            "name": getattr(assignee, "name", ""),
                        }
                    )
            except TypeError:
                # assignees is not iterable
                pass

        # Extract milestone info
        milestone_info = None
        if hasattr(issue, "milestone") and issue.milestone:
            milestone_info = {
                "title": getattr(issue.milestone, "title", ""),
                "web_url": getattr(issue.milestone, "web_url", ""),
            }

        formatted_issues.append(
            {
                "iid": issue.iid,
                "title": issue.title,
                "description": getattr(issue, "description", ""),
                "state": issue.state,
                "labels": getattr(issue, "labels", []),
                "web_url": issue.web_url,
                "created_at": getattr(issue, "created_at", ""),
                "updated_at": getattr(issue, "updated_at", ""),
                "closed_at": getattr(issue, "closed_at", None),
                "author": author,
                "assignees": assignees,
                "milestone": milestone_info,
            }
        )

    return {
        "issues": formatted_issues,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(formatted_issues),
        },
    }


async def get_issue(
    client: GitLabClient,
    project_id: str | int,
    issue_iid: int,
) -> dict[str, Any]:
    """
    Get detailed information about a specific issue.

    This tool retrieves comprehensive details about a single GitLab issue
    including title, description, state, labels, assignees, and metadata.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        issue_iid: Issue IID (internal ID within the project)

    Returns:
        Dictionary with issue details:
        {
            "iid": int,
            "title": str,
            "description": str,
            "state": str (opened/closed),
            "labels": [str],
            "web_url": str,
            "created_at": str (ISO 8601),
            "updated_at": str (ISO 8601),
            "closed_at": str | None (ISO 8601),
            "author": {"username": str, "name": str} | None,
            "assignees": [{"username": str, "name": str}],
            "milestone": {"title": str, "web_url": str} | None
        }

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or issue doesn't exist
        PermissionError: If user doesn't have permission to access project/issue
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> issue = await get_issue(client, "mygroup/myproject", 42)
        >>> print(f"#{issue['iid']}: {issue['title']}")
        >>> print(f"State: {issue['state']}")
        >>> print(f"Labels: {', '.join(issue['labels'])}")
    """
    # Get issue from GitLab
    issue = client.get_issue(project_id=project_id, issue_iid=issue_iid)

    # Extract author info
    author = None
    if hasattr(issue, "author") and issue.author:
        author = {
            "username": getattr(issue.author, "username", ""),
            "name": getattr(issue.author, "name", ""),
        }

    # Extract assignees
    assignees = []
    if hasattr(issue, "assignees") and issue.assignees:
        # Handle both list and non-iterable assignees
        try:
            for assignee in issue.assignees:
                assignees.append(
                    {
                        "username": getattr(assignee, "username", ""),
                        "name": getattr(assignee, "name", ""),
                    }
                )
        except TypeError:
            # assignees is not iterable
            pass

    # Extract milestone info
    milestone_info = None
    if hasattr(issue, "milestone") and issue.milestone:
        milestone_info = {
            "title": getattr(issue.milestone, "title", ""),
            "web_url": getattr(issue.milestone, "web_url", ""),
        }

    return {
        "iid": issue.iid,
        "title": issue.title,
        "description": getattr(issue, "description", ""),
        "state": issue.state,
        "labels": getattr(issue, "labels", []),
        "web_url": issue.web_url,
        "created_at": getattr(issue, "created_at", ""),
        "updated_at": getattr(issue, "updated_at", ""),
        "closed_at": getattr(issue, "closed_at", None),
        "author": author,
        "assignees": assignees,
        "milestone": milestone_info,
    }


async def create_issue(
    client: GitLabClient,
    project_id: str | int,
    title: str,
    description: str | None = None,
    labels: list[str] | None = None,
    assignee_ids: list[int] | None = None,
    milestone_id: int | None = None,
) -> dict[str, Any]:
    """
    Create a new issue in a GitLab project.

    This tool creates a new issue with the specified title and optional
    additional properties like description, labels, assignees, and milestone.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        title: Issue title (required)
        description: Issue description (optional)
        labels: List of label names to apply to the issue (optional)
        assignee_ids: List of user IDs to assign to the issue (optional)
        milestone_id: Milestone ID to associate with the issue (optional)

    Returns:
        Dictionary with created issue details:
        {
            "iid": int,
            "title": str,
            "description": str,
            "state": str (opened/closed),
            "labels": [str],
            "web_url": str,
            "created_at": str (ISO 8601),
            "updated_at": str (ISO 8601),
            "closed_at": str | None (ISO 8601),
            "author": {"username": str, "name": str} | None,
            "assignees": [{"username": str, "name": str}],
            "milestone": {"title": str, "web_url": str} | None
        }

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project doesn't exist
        PermissionError: If user doesn't have permission to create issues
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> issue = await create_issue(
        ...     client,
        ...     "mygroup/myproject",
        ...     "Bug: Login fails",
        ...     description="Users unable to log in with valid credentials",
        ...     labels=["bug", "critical"]
        ... )
        >>> print(f"Created issue #{issue['iid']}: {issue['title']}")
    """
    # Create issue via GitLab client
    issue = client.create_issue(
        project_id=project_id,
        title=title,
        description=description,
        labels=labels,
        assignee_ids=assignee_ids,
        milestone_id=milestone_id,
    )

    # Extract author info
    author = None
    if hasattr(issue, "author") and issue.author:
        author = {
            "username": getattr(issue.author, "username", ""),
            "name": getattr(issue.author, "name", ""),
        }

    # Extract assignees
    assignees = []
    if hasattr(issue, "assignees") and issue.assignees:
        # Handle both list and non-iterable assignees
        try:
            for assignee in issue.assignees:
                assignees.append(
                    {
                        "username": getattr(assignee, "username", ""),
                        "name": getattr(assignee, "name", ""),
                    }
                )
        except TypeError:
            # assignees is not iterable
            pass

    # Extract milestone info
    milestone_info = None
    if hasattr(issue, "milestone") and issue.milestone:
        milestone_info = {
            "title": getattr(issue.milestone, "title", ""),
            "web_url": getattr(issue.milestone, "web_url", ""),
        }

    return {
        "iid": issue.iid,
        "title": issue.title,
        "description": getattr(issue, "description", ""),
        "state": issue.state,
        "labels": getattr(issue, "labels", []),
        "web_url": issue.web_url,
        "created_at": getattr(issue, "created_at", ""),
        "updated_at": getattr(issue, "updated_at", ""),
        "closed_at": getattr(issue, "closed_at", None),
        "author": author,
        "assignees": assignees,
        "milestone": milestone_info,
    }
