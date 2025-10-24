"""
Repository tools for GitLab MCP server.

This module provides MCP tools for GitLab repository operations including:
- Getting repository/project details
- Listing branches
- Getting branch details
- File operations
- Commits
- Tags
- Code search

All tools are async functions that accept a GitLabClient and return formatted data.
"""

import base64
from typing import Any

from gitlab_mcp.client.gitlab_client import GitLabClient


async def get_repository(client: GitLabClient, project_id: str | int) -> dict[str, Any]:
    """
    Get repository/project details and metadata.

    This tool retrieves comprehensive information about a GitLab repository/project
    including name, description, visibility, statistics, and timestamps.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'

    Returns:
        Dictionary with repository details:
        {
            "id": int,
            "name": str,
            "path": str,
            "path_with_namespace": str,
            "description": str,
            "visibility": str (public/private/internal),
            "web_url": str,
            "default_branch": str,
            "created_at": str (ISO 8601),
            "last_activity_at": str (ISO 8601),
            "star_count": int,
            "forks_count": int,
            "open_issues_count": int
        }

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project doesn't exist
        PermissionError: If user doesn't have permission to access project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> repo = await get_repository(client, "mygroup/myproject")
        >>> print(repo["name"])
        "My Project"
    """
    # Get project from GitLab (returns dict after Bug #1 fix)
    project = client.get_project(project_id)

    # Extract and return relevant fields
    return {
        "id": project.get("id"),
        "name": project.get("name", ""),
        "path": project.get("path", ""),
        "path_with_namespace": project.get("path_with_namespace", ""),
        "description": project.get("description", ""),
        "visibility": project.get("visibility", ""),
        "web_url": project.get("web_url", ""),
        "default_branch": project.get("default_branch", "main"),
        "created_at": project.get("created_at", ""),
        "last_activity_at": project.get("last_activity_at", ""),
        "star_count": project.get("star_count", 0),
        "forks_count": project.get("forks_count", 0),
        "open_issues_count": project.get("open_issues_count", 0),
    }


async def list_branches(
    client: GitLabClient,
    project_id: str | int,
    search: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List all branches in a repository.

    This tool retrieves a list of all branches in a GitLab repository with
    information about each branch including name, commit SHA, protection status,
    and whether it's the default branch.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        search: Optional search term to filter branches by name
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 20, max: 100)

    Returns:
        Dictionary with branch list and metadata:
        {
            "branches": [
                {
                    "name": str,
                    "commit_sha": str,
                    "protected": bool,
                    "default": bool,
                    "merged": bool
                },
                ...
            ],
            "total": int,
            "page": int,
            "per_page": int
        }

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project doesn't exist
        PermissionError: If user doesn't have permission to access project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> result = await list_branches(client, "mygroup/myproject", search="feature")
        >>> for branch in result["branches"]:
        ...     print(f"{branch['name']} - Protected: {branch['protected']}")
    """
    # Get branches from GitLab
    branches = client.list_branches(project_id, search, page, per_page)

    # Format branch data
    formatted_branches = [
        {
            "name": branch.name,
            "commit_sha": branch.commit["id"],
            "protected": branch.protected,
            "default": branch.default,
            "merged": getattr(branch, "merged", False),
        }
        for branch in branches
    ]

    return {
        "branches": formatted_branches,
        "total": len(formatted_branches),
        "page": page,
        "per_page": per_page,
    }


async def get_branch(
    client: GitLabClient, project_id: str | int, branch_name: str
) -> dict[str, Any]:
    """
    Get detailed information about a specific branch.

    This tool retrieves comprehensive information about a specific branch in a
    GitLab repository including commit details, protection status, merge permissions,
    and more.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        branch_name: Name of the branch to retrieve

    Returns:
        Dictionary with branch details:
        {
            "name": str,
            "commit": {
                "sha": str,
                "short_sha": str,
                "title": str,
                "author_name": str,
                "author_email": str,
                "created_at": str (ISO 8601),
                "message": str (optional)
            },
            "protected": bool,
            "default": bool,
            "merged": bool,
            "can_push": bool,
            "developers_can_push": bool,
            "developers_can_merge": bool,
            "web_url": str
        }

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or branch doesn't exist
        PermissionError: If user doesn't have permission to access project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> branch = await get_branch(client, "mygroup/myproject", "main")
        >>> print(f"{branch['name']} - Protected: {branch['protected']}")
        >>> print(f"Latest commit: {branch['commit']['title']}")
    """
    # Get branch from GitLab
    branch = client.get_branch(project_id, branch_name)

    # Format branch data with comprehensive commit information
    return {
        "name": branch.name,
        "commit": {
            "sha": branch.commit["id"],
            "short_sha": branch.commit.get("short_id", branch.commit["id"][:7]),
            "title": branch.commit.get("title", ""),
            "author_name": branch.commit.get("author_name", ""),
            "author_email": branch.commit.get("author_email", ""),
            "created_at": branch.commit.get("created_at", ""),
            "message": branch.commit.get("message", ""),
        },
        "protected": branch.protected,
        "default": branch.default,
        "merged": getattr(branch, "merged", False),
        "can_push": getattr(branch, "can_push", False),
        "developers_can_push": getattr(branch, "developers_can_push", False),
        "developers_can_merge": getattr(branch, "developers_can_merge", False),
        "web_url": getattr(branch, "web_url", ""),
    }


async def get_file_contents(
    client: GitLabClient,
    project_id: str | int,
    file_path: str,
    ref: str | None = None,
) -> dict[str, Any]:
    """
    Get the contents of a file from a repository.

    This tool retrieves the contents of a specific file from a GitLab repository.
    The content is automatically decoded from base64 to UTF-8 text.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        file_path: Path to the file in the repository (e.g., "README.md", "src/main.py")
        ref: Branch, tag, or commit SHA (default: project's default branch)

    Returns:
        Dictionary with file details:
        {
            "file_path": str,
            "file_name": str,
            "size": int,
            "content": str (decoded from base64),
            "encoding": str,
            "content_sha256": str,
            "ref": str,
            "blob_id": str,
            "last_commit_id": str
        }

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or file doesn't exist
        PermissionError: If user doesn't have permission to access project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> file = await get_file_contents(client, "mygroup/myproject", "README.md")
        >>> print(file["content"])
        "# My Project..."
    """
    # Get file from GitLab
    file = client.get_file_content(project_id, file_path, ref=ref)

    # Decode base64 content to UTF-8 string (handle binary files)
    try:
        decoded_content = base64.b64decode(file.content).decode("utf-8")
    except UnicodeDecodeError:
        # For binary files, return the base64 content as-is
        decoded_content = file.content

    # Return formatted file data
    return {
        "file_path": file.file_path,
        "file_name": getattr(file, "file_name", file.file_path.split("/")[-1]),
        "size": file.size,
        "content": decoded_content,
        "encoding": getattr(file, "encoding", "base64"),
        "content_sha256": getattr(file, "content_sha256", ""),
        "ref": file.ref,
        "blob_id": getattr(file, "blob_id", ""),
        "last_commit_id": getattr(file, "last_commit_id", ""),
    }


async def list_repository_tree(
    client: GitLabClient,
    project_id: str | int,
    path: str = "",
    ref: str | None = None,
    recursive: bool = False,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List files and directories in a repository.

    Args:
        client: Authenticated GitLab client
        project_id: Project ID or URL-encoded path
        path: Path inside repository (default: root directory)
        ref: Branch/tag/commit to list from (default: project's default branch)
        recursive: Get recursive tree listing (default: False)
        page: Page number for pagination
        per_page: Number of items per page

    Returns:
        Dictionary containing:
        - path: The path that was listed
        - ref: The ref that was used
        - recursive: Whether recursive listing was used
        - entries: List of file/directory entries with metadata
        - total: Total number of entries returned
        - page: Current page number
        - per_page: Items per page

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or path not found
        GitLabAPIError: If API request fails
    """
    tree = client.get_repository_tree(
        project_id, path=path, ref=ref, recursive=recursive, page=page, per_page=per_page
    )

    # Format tree entries
    entries = []
    for entry in tree:
        entries.append(
            {
                "id": entry.get("id", ""),
                "name": entry.get("name", ""),
                "type": entry.get("type", ""),  # "blob" (file) or "tree" (directory)
                "path": entry.get("path", ""),
                "mode": entry.get("mode", ""),  # File permissions
            }
        )

    return {
        "path": path,
        "ref": ref if ref else "default",
        "recursive": recursive,
        "entries": entries,
        "total": len(entries),
        "page": page,
        "per_page": per_page,
    }


async def get_commit(
    client: GitLabClient, project_id: str | int, commit_sha: str
) -> dict[str, Any]:
    """
    Get details of a specific commit.

    Args:
        client: Authenticated GitLab client
        project_id: Project ID or URL-encoded path
        commit_sha: Commit SHA or reference (full or short SHA)

    Returns:
        Dictionary containing:
        - sha: Full commit SHA
        - short_sha: Shortened commit SHA
        - title: Commit title (first line of message)
        - message: Full commit message
        - author_name: Author's name
        - author_email: Author's email
        - authored_date: When the commit was authored
        - committer_name: Committer's name
        - committer_email: Committer's email
        - committed_date: When the commit was committed
        - parent_ids: List of parent commit SHAs
        - web_url: URL to view commit in GitLab

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If commit not found
        GitLabAPIError: If API request fails
    """
    commit = client.get_commit(project_id, commit_sha)

    return {
        "sha": commit.id,
        "short_sha": getattr(commit, "short_id", commit.id[:7]),
        "title": commit.title,
        "message": commit.message,
        "author_name": commit.author_name,
        "author_email": commit.author_email,
        "authored_date": commit.authored_date,
        "committer_name": commit.committer_name,
        "committer_email": commit.committer_email,
        "committed_date": commit.committed_date,
        "parent_ids": getattr(commit, "parent_ids", []),
        "web_url": getattr(commit, "web_url", ""),
    }


async def list_commits(
    client: GitLabClient,
    project_id: str | int,
    ref: str | None = None,
    since: str | None = None,
    until: str | None = None,
    path: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List commits for a project or branch.

    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        ref: Branch/tag name to list commits from (uses default branch if not specified)
        since: Only commits after this date (ISO 8601 format)
        until: Only commits before this date (ISO 8601 format)
        path: Only commits affecting this file path
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 20, max: 100)

    Returns:
        Dictionary with commit list and pagination metadata

    Raises:
        NotFoundError: If project not found
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
    """
    commits = client.list_commits(
        project_id,
        ref=ref,
        since=since,
        until=until,
        path=path,
        page=page,
        per_page=per_page,
    )

    return {
        "ref": ref or "default",
        "commits": [
            {
                "sha": commit.id,
                "short_sha": getattr(commit, "short_id", commit.id[:7]),
                "title": commit.title,
                "message": commit.message,
                "author_name": commit.author_name,
                "author_email": commit.author_email,
                "authored_date": commit.authored_date,
                "committer_name": commit.committer_name,
                "committer_email": commit.committer_email,
                "committed_date": commit.committed_date,
                "parent_ids": getattr(commit, "parent_ids", []),
                "web_url": getattr(commit, "web_url", ""),
            }
            for commit in commits
        ],
        "total": len(commits),
        "page": page,
        "per_page": per_page,
    }


async def compare_branches(
    client: GitLabClient,
    project_id: str | int,
    from_ref: str,
    to_ref: str,
    straight: bool = False,
) -> dict[str, Any]:
    """
    Compare two branches, tags, or commits.

    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        from_ref: Source branch, tag, or commit SHA
        to_ref: Target branch, tag, or commit SHA
        straight: If true, compare refs directly (no merge base)

    Returns:
        Dictionary with comparison details including commits and diffs

    Raises:
        NotFoundError: If project or refs not found
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
    """
    comparison = client.compare_branches(project_id, from_ref, to_ref, straight=straight)

    return {
        "from_ref": from_ref,
        "to_ref": to_ref,
        "commits": [
            {
                "sha": commit.id,
                "short_sha": getattr(commit, "short_id", commit.id[:7]),
                "title": commit.title,
                "message": commit.message,
                "author_name": commit.author_name,
                "created_at": commit.created_at,
            }
            for commit in getattr(comparison, "commits", [])
        ],
        "diffs": [
            {
                "old_path": diff.get("old_path"),
                "new_path": diff.get("new_path"),
                "a_mode": diff.get("a_mode"),
                "b_mode": diff.get("b_mode"),
                "new_file": diff.get("new_file", False),
                "renamed_file": diff.get("renamed_file", False),
                "deleted_file": diff.get("deleted_file", False),
                "diff": diff.get("diff", ""),
            }
            for diff in getattr(comparison, "diffs", [])
        ],
        "compare_same_ref": from_ref == to_ref,
    }


async def create_branch(
    client: GitLabClient,
    project_id: str | int,
    branch_name: str,
    ref: str,
) -> dict[str, Any]:
    """
    Create a new branch.

    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        branch_name: Name for the new branch
        ref: Source branch, tag, or commit SHA

    Returns:
        Dictionary with new branch details

    Raises:
        NotFoundError: If project or ref not found
        ValidationError: If branch name invalid or already exists
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
    """
    branch = client.create_branch(project_id, branch_name, ref)

    return {
        "name": branch.name,
        "commit": {
            "id": branch.commit["id"],
            "short_id": branch.commit.get("short_id", branch.commit["id"][:7]),
            "title": branch.commit.get("title", ""),
            "message": branch.commit.get("message", ""),
            "author_name": branch.commit.get("author_name", ""),
            "created_at": branch.commit.get("created_at", ""),
        },
        "merged": getattr(branch, "merged", False),
        "protected": branch.protected,
        "developers_can_push": branch.developers_can_push,
        "developers_can_merge": branch.developers_can_merge,
        "can_push": branch.can_push,
        "default": getattr(branch, "default", False),
        "web_url": branch.web_url,
    }


async def delete_branch(
    client: GitLabClient,
    project_id: str | int,
    branch_name: str,
) -> dict[str, Any]:
    """
    Delete a branch.

    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        branch_name: Name of branch to delete

    Returns:
        Dictionary with success status

    Raises:
        NotFoundError: If project or branch not found
        PermissionError: If branch is protected or insufficient permissions
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
    """
    client.delete_branch(project_id, branch_name)

    return {
        "deleted": True,
        "branch_name": branch_name,
    }


async def list_tags(
    client: GitLabClient,
    project_id: str | int,
    search: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List repository tags.

    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        search: Optional search pattern to filter tags
        page: Page number (default: 1)
        per_page: Results per page (default: 20, max: 100)

    Returns:
        Dictionary with tags and pagination info

    Raises:
        NotFoundError: If project not found
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
    """
    tags = client.list_tags(project_id, search, page, per_page)

    return {
        "tags": [
            {
                "name": tag.name,
                "message": getattr(tag, "message", ""),
                "target": tag.target,
                "commit": {
                    "id": tag.commit["id"],
                    "short_id": tag.commit.get("short_id", tag.commit["id"][:7]),
                    "title": tag.commit.get("title", ""),
                    "author_name": tag.commit.get("author_name", ""),
                    "created_at": tag.commit.get("created_at", ""),
                },
                "protected": getattr(tag, "protected", False),
            }
            for tag in tags
        ],
        "page": page,
        "per_page": per_page,
        "total": len(tags),
    }


async def get_tag(
    client: GitLabClient,
    project_id: str | int,
    tag_name: str,
) -> dict[str, Any]:
    """
    Get details of a specific tag.

    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        tag_name: Name of the tag

    Returns:
        Dictionary with tag details

    Raises:
        NotFoundError: If project or tag not found
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
    """
    tag = client.get_tag(project_id, tag_name)

    return {
        "name": tag.name,
        "message": getattr(tag, "message", ""),
        "target": tag.target,
        "commit": {
            "id": tag.commit["id"],
            "short_id": tag.commit.get("short_id", tag.commit["id"][:7]),
            "title": tag.commit.get("title", ""),
            "message": tag.commit.get("message", ""),
            "author_name": tag.commit.get("author_name", ""),
            "created_at": tag.commit.get("created_at", ""),
        },
        "protected": getattr(tag, "protected", False),
    }


async def create_tag(
    client: GitLabClient,
    project_id: str | int,
    tag_name: str,
    ref: str,
    message: str | None = None,
) -> dict[str, Any]:
    """
    Create a new tag.

    Args:
        client: GitLab client instance
        project_id: Project ID or URL-encoded path
        tag_name: Name for the new tag
        ref: Source branch, tag, or commit SHA
        message: Optional tag message (creates annotated tag)

    Returns:
        Dictionary with new tag details

    Raises:
        NotFoundError: If project or ref not found
        ValidationError: If tag name invalid or already exists
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
    """
    tag = client.create_tag(project_id, tag_name, ref, message)

    return {
        "name": tag.name,
        "message": getattr(tag, "message", ""),
        "target": tag.target,
        "commit": {
            "id": tag.commit["id"],
            "short_id": tag.commit.get("short_id", tag.commit["id"][:7]),
            "title": tag.commit.get("title", ""),
            "message": tag.commit.get("message", ""),
            "author_name": tag.commit.get("author_name", ""),
            "created_at": tag.commit.get("created_at", ""),
        },
        "protected": getattr(tag, "protected", False),
    }


async def search_code(
    client: GitLabClient,
    search_term: str,
    project_id: str | int | None = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    Search for code across repositories.

    Uses GitLab's code search API to search for code patterns across all
    accessible repositories or within a specific project. Search results include
    code snippets with context and file location information.

    Args:
        client: GitLab client instance
        search_term: Code pattern to search for. Can include filters like
                    'filename:*.py' or 'extension:js' for targeted searches.
                    Examples:
                    - "def search_code" - search for function definition
                    - "TODO filename:*.py" - search TODO in Python files
                    - "class Config extension:js" - search in JavaScript files
        project_id: Optional project ID or path to limit search to specific project.
                   If not provided, searches globally across all accessible projects.
        page: Page number for pagination (default: 1)
        per_page: Number of results per page (default: 20, max: 100)

    Returns:
        Dictionary with search results and metadata:
        - results: List of search result dictionaries, each containing:
            - basename: Filename without path
            - data: Preview of file content with context around match
            - path: Full file path in repository
            - filename: Full path (same as 'path', kept for compatibility)
            - ref: Branch or tag name where match was found
            - startline: Line number where match begins
            - project_id: ID of the project containing the match
        - page: Current page number
        - per_page: Results per page
        - total: Total number of results on this page
        - search_term: The search term used

    Raises:
        NotFoundError: If project not found (when project_id specified)
        AuthenticationError: If not authenticated
        GitLabAPIError: If API request fails
        GitLabServerError: If GitLab server error occurs

    Example:
        # Global code search
        results = await search_code(client, "def main")

        # Project-specific search
        results = await search_code(client, "TODO", project_id=123)

        # Search with filters
        results = await search_code(client, "import flask filename:*.py")
    """
    results = client.search_code(
        search_term,
        project_id,
        page,
        per_page,
    )

    return {
        "results": [
            {
                "basename": result.get("basename", ""),
                "data": result.get("data", ""),
                "path": result.get("path", result.get("filename", "")),
                "filename": result.get("filename", result.get("path", "")),
                "ref": result.get("ref", ""),
                "startline": result.get("startline"),
                "project_id": result.get("project_id"),
            }
            for result in results
        ],
        "page": page,
        "per_page": per_page,
        "total": len(results),
        "search_term": search_term,
    }


async def create_file(
    client: GitLabClient,
    project_id: str | int,
    file_path: str,
    branch: str,
    content: str,
    commit_message: str,
    author_email: str | None = None,
    author_name: str | None = None,
    encoding: str = "text",
) -> dict[str, Any]:
    """
    Create a new file in a repository.

    This tool creates a new file in a GitLab repository with a commit message,
    enabling AI to generate and save new files directly via the API.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        file_path: Full path for the new file (e.g., "src/main.py", "README.md")
        branch: Name of the branch to create the file in
        content: Content of the file (text or base64-encoded for binary files)
        commit_message: Commit message for the file creation
        author_email: Optional email of the commit author
        author_name: Optional name of the commit author
        encoding: Content encoding - "text" (default) or "base64" for binary files

    Returns:
        Dictionary with file creation details including file_path, branch, and commit info

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project doesn't exist
        ValidationError: If file already exists or path is invalid
        PermissionError: If user doesn't have permission to write to project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> result = await create_file(
        ...     client,
        ...     "mygroup/myproject",
        ...     "README.md",
        ...     "main",
        ...     "# My Project\n\nDescription here",
        ...     "Add README file"
        ... )
        >>> print(result["file_path"])
        "README.md"
    """
    # Call client method to create the file
    file_obj = client.create_file(
        project_id,
        file_path,
        branch,
        content,
        commit_message,
        author_email=author_email,
        author_name=author_name,
        encoding=encoding,
    )

    # Convert python-gitlab object to dictionary
    return {
        "file_path": getattr(file_obj, "file_path", file_path),
        "branch": branch,
        "commit": {
            "id": getattr(file_obj, "commit_id", ""),
            "message": commit_message,
        },
    }


async def update_file(
    client: GitLabClient,
    project_id: str | int,
    file_path: str,
    branch: str,
    content: str,
    commit_message: str,
    author_email: str | None = None,
    author_name: str | None = None,
    encoding: str = "text",
) -> dict[str, Any]:
    """
    Update an existing file in a repository.

    This tool updates the content of an existing file in a GitLab repository,
    enabling AI to make edits, fixes, and refactorings directly via the API.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        file_path: Full path to the file to update (e.g., "src/main.py")
        branch: Name of the branch containing the file
        content: New content for the file (text or base64-encoded for binary files)
        commit_message: Commit message for the file update
        author_email: Optional email of the commit author
        author_name: Optional name of the commit author
        encoding: Content encoding - "text" (default) or "base64" for binary files

    Returns:
        Dictionary with file update details including file_path, branch, and commit info

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or file doesn't exist
        PermissionError: If user doesn't have permission to write to project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> result = await update_file(
        ...     client,
        ...     "mygroup/myproject",
        ...     "README.md",
        ...     "main",
        ...     "# Updated Project\n\nNew description",
        ...     "Update README with new description"
        ... )
        >>> print(result["commit"]["message"])
        "Update README with new description"
    """
    # Call client method to update the file
    file_obj = client.update_file(
        project_id,
        file_path,
        branch,
        content,
        commit_message,
        author_email=author_email,
        author_name=author_name,
        encoding=encoding,
    )

    # Convert python-gitlab object to dictionary
    return {
        "file_path": getattr(file_obj, "file_path", file_path),
        "branch": branch,
        "commit": {
            "id": getattr(file_obj, "commit_id", ""),
            "message": commit_message,
        },
    }


async def delete_file(
    client: GitLabClient,
    project_id: str | int,
    file_path: str,
    branch: str,
    commit_message: str,
    author_email: str | None = None,
    author_name: str | None = None,
) -> dict[str, Any]:
    """
    Delete a file from a repository.

    This tool deletes a file from a GitLab repository with a commit message,
    enabling AI to clean up files directly via the API.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str) in format 'namespace/project'
        file_path: Full path to the file to delete (e.g., "old_file.py")
        branch: Name of the branch containing the file
        commit_message: Commit message for the file deletion
        author_email: Optional email of the commit author
        author_name: Optional name of the commit author

    Returns:
        Dictionary with file deletion confirmation including file_path, branch, and commit info

    Raises:
        AuthenticationError: If not authenticated
        NotFoundError: If project or file doesn't exist
        PermissionError: If user doesn't have permission to write to project
        GitLabAPIError: If API call fails

    Example:
        >>> client = GitLabClient(config)
        >>> result = await delete_file(
        ...     client,
        ...     "mygroup/myproject",
        ...     "deprecated.py",
        ...     "main",
        ...     "Remove deprecated module"
        ... )
        >>> print(result["file_path"])
        "deprecated.py"
    """
    # Call client method to delete the file
    client.delete_file(
        project_id,
        file_path,
        branch,
        commit_message,
        author_email=author_email,
        author_name=author_name,
    )

    # Return confirmation (delete_file returns None, so we construct the response)
    return {
        "file_path": file_path,
        "branch": branch,
        "commit": {
            "message": commit_message,
        },
    }
