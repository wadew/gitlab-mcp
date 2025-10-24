"""
GitLab MCP Server.

This module implements the Model Context Protocol (MCP) server for GitLab integration.
It provides tools for interacting with GitLab repositories, issues, merge requests, and more.
"""

import asyncio
from collections.abc import Callable
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server

from gitlab_mcp import tools
from gitlab_mcp.client.gitlab_client import GitLabClient
from gitlab_mcp.config.settings import GitLabConfig, load_config


class GitLabMCPServer:
    """
    GitLab MCP Server.

    This server implements the MCP protocol and provides tools for GitLab operations.

    Attributes:
        config: GitLabConfig instance with server configuration
        gitlab_client: GitLabClient instance for GitLab API operations
        name: Server name (default: "gitlab-mcp-server")
    """

    def __init__(self, config: GitLabConfig, name: str = "gitlab-mcp-server") -> None:
        """
        Initialize the GitLab MCP Server.

        Args:
            config: GitLabConfig instance with server settings
            name: Server name (default: "gitlab-mcp-server")
        """
        self.config = config
        self.name = name
        self.gitlab_client = GitLabClient(config)
        self._tools: dict[str, dict[str, Any]] = {}

    def register_all_tools(self) -> None:
        """
        Register all available MCP tools.

        This method registers all 70 MCP tools organized by category:
        - Context tools (1)
        - Repository tools (6)
        - Issue tools (3)
        - Merge Request tools (12)
        - Pipeline tools (14)
        - Project tools (9)
        - Label tools (4)
        - Wiki tools (5)
        - Snippet tools (5)
        - Release tools (5)
        - User tools (3)
        - Group tools (3)
        """
        # Context tools
        self.register_tool(
            "get_current_context",
            "Get current GitLab user and server context information",
            lambda **kwargs: tools.get_current_context(self.gitlab_client, **kwargs),
        )

        # Repository tools
        self.register_tool(
            "list_repository_tree",
            "List files and directories in a repository tree",
            lambda **kwargs: tools.list_repository_tree(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_file_contents",
            "Get the contents of a file from a repository",
            lambda **kwargs: tools.get_file_contents(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "search_code",
            "Search for code in project repositories",
            lambda **kwargs: tools.search_code(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_file",
            "Create a new file in a repository with commit",
            lambda **kwargs: tools.create_file(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "update_file",
            "Update existing file content with commit",
            lambda **kwargs: tools.update_file(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "delete_file",
            "Delete a file from repository with commit",
            lambda **kwargs: tools.delete_file(self.gitlab_client, **kwargs),
        )

        # Issue tools
        self.register_tool(
            "list_issues",
            "List issues for a project",
            lambda **kwargs: tools.list_issues(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_issue",
            "Get details of a specific issue",
            lambda **kwargs: tools.get_issue(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_issue",
            "Create a new issue in a project",
            lambda **kwargs: tools.create_issue(self.gitlab_client, **kwargs),
        )

        # Merge Request tools
        self.register_tool(
            "list_merge_requests",
            "List merge requests for a project",
            lambda **kwargs: tools.list_merge_requests(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_merge_request",
            "Get details of a specific merge request",
            lambda **kwargs: tools.get_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_merge_request",
            "Create a new merge request",
            lambda **kwargs: tools.create_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "update_merge_request",
            "Update an existing merge request",
            lambda **kwargs: tools.update_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "merge_merge_request",
            "Merge an approved merge request",
            lambda **kwargs: tools.merge_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "close_merge_request",
            "Close a merge request without merging",
            lambda **kwargs: tools.close_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "reopen_merge_request",
            "Reopen a closed merge request",
            lambda **kwargs: tools.reopen_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "approve_merge_request",
            "Approve a merge request",
            lambda **kwargs: tools.approve_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "unapprove_merge_request",
            "Remove approval from a merge request",
            lambda **kwargs: tools.unapprove_merge_request(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_merge_request_changes",
            "Get the file changes in a merge request",
            lambda **kwargs: tools.get_merge_request_changes(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_merge_request_commits",
            "Get commits in a merge request",
            lambda **kwargs: tools.get_merge_request_commits(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_merge_request_pipelines",
            "Get pipelines for a merge request",
            lambda **kwargs: tools.get_merge_request_pipelines(self.gitlab_client, **kwargs),
        )

        # Pipeline tools
        self.register_tool(
            "list_pipelines",
            "List pipelines for a project",
            lambda **kwargs: tools.list_pipelines(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_pipeline",
            "Get details of a specific pipeline",
            lambda **kwargs: tools.get_pipeline(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_pipeline",
            "Create a new pipeline",
            lambda **kwargs: tools.create_pipeline(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "retry_pipeline",
            "Retry a failed pipeline",
            lambda **kwargs: tools.retry_pipeline(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "cancel_pipeline",
            "Cancel a running pipeline",
            lambda **kwargs: tools.cancel_pipeline(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "delete_pipeline",
            "Delete a pipeline",
            lambda **kwargs: tools.delete_pipeline(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "list_pipeline_jobs",
            "List jobs in a pipeline",
            lambda **kwargs: tools.list_pipeline_jobs(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_job",
            "Get details of a specific job",
            lambda **kwargs: tools.get_job(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_job_trace",
            "Get the trace log of a job",
            lambda **kwargs: tools.get_job_trace(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "retry_job",
            "Retry a failed job",
            lambda **kwargs: tools.retry_job(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "cancel_job",
            "Cancel a running job",
            lambda **kwargs: tools.cancel_job(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "play_job",
            "Play a manual job",
            lambda **kwargs: tools.play_job(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "download_job_artifacts",
            "Download artifacts from a job",
            lambda **kwargs: tools.download_job_artifacts(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "list_pipeline_variables",
            "List variables for a pipeline",
            lambda **kwargs: tools.list_pipeline_variables(self.gitlab_client, **kwargs),
        )

        # Project tools
        self.register_tool(
            "list_projects",
            "List projects accessible by the user",
            lambda **kwargs: tools.list_projects(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_project",
            "Get details of a specific project",
            lambda **kwargs: tools.get_project(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "search_projects",
            "Search for projects by name or description",
            lambda **kwargs: tools.search_projects(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "list_project_members",
            "List members of a project",
            lambda **kwargs: tools.list_project_members(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_project_statistics",
            "Get statistics for a project",
            lambda **kwargs: tools.get_project_statistics(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "list_milestones",
            "List milestones for a project",
            lambda **kwargs: tools.list_milestones(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_milestone",
            "Get details of a specific milestone",
            lambda **kwargs: tools.get_milestone(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_milestone",
            "Create a new milestone",
            lambda **kwargs: tools.create_milestone(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "update_milestone",
            "Update an existing milestone",
            lambda **kwargs: tools.update_milestone(self.gitlab_client, **kwargs),
        )

        # Label tools
        self.register_tool(
            "list_labels",
            "List labels for a project",
            lambda **kwargs: tools.list_labels(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_label",
            "Create a new label",
            lambda **kwargs: tools.create_label(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "update_label",
            "Update an existing label",
            lambda **kwargs: tools.update_label(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "delete_label",
            "Delete a label",
            lambda **kwargs: tools.delete_label(self.gitlab_client, **kwargs),
        )

        # Wiki tools
        self.register_tool(
            "list_wiki_pages",
            "List wiki pages for a project",
            lambda **kwargs: tools.list_wiki_pages(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_wiki_page",
            "Get content of a specific wiki page",
            lambda **kwargs: tools.get_wiki_page(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_wiki_page",
            "Create a new wiki page",
            lambda **kwargs: tools.create_wiki_page(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "update_wiki_page",
            "Update an existing wiki page",
            lambda **kwargs: tools.update_wiki_page(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "delete_wiki_page",
            "Delete a wiki page",
            lambda **kwargs: tools.delete_wiki_page(self.gitlab_client, **kwargs),
        )

        # Snippet tools
        self.register_tool(
            "list_snippets",
            "List snippets for a project",
            lambda **kwargs: tools.list_snippets(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_snippet",
            "Get content of a specific snippet",
            lambda **kwargs: tools.get_snippet(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_snippet",
            "Create a new snippet",
            lambda **kwargs: tools.create_snippet(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "update_snippet",
            "Update an existing snippet",
            lambda **kwargs: tools.update_snippet(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "delete_snippet",
            "Delete a snippet",
            lambda **kwargs: tools.delete_snippet(self.gitlab_client, **kwargs),
        )

        # Release tools
        self.register_tool(
            "list_releases",
            "List releases for a project",
            lambda **kwargs: tools.list_releases(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_release",
            "Get details of a specific release",
            lambda **kwargs: tools.get_release(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "create_release",
            "Create a new release",
            lambda **kwargs: tools.create_release(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "update_release",
            "Update an existing release",
            lambda **kwargs: tools.update_release(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "delete_release",
            "Delete a release",
            lambda **kwargs: tools.delete_release(self.gitlab_client, **kwargs),
        )

        # User tools
        self.register_tool(
            "get_user",
            "Get details of a specific user",
            lambda **kwargs: tools.get_user(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "search_users",
            "Search for users by username or email",
            lambda **kwargs: tools.search_users(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "list_user_projects",
            "List projects for a specific user",
            lambda **kwargs: tools.list_user_projects(self.gitlab_client, **kwargs),
        )

        # Group tools
        self.register_tool(
            "list_groups",
            "List groups accessible by the user",
            lambda **kwargs: tools.list_groups(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "get_group",
            "Get details of a specific group",
            lambda **kwargs: tools.get_group(self.gitlab_client, **kwargs),
        )
        self.register_tool(
            "list_group_members",
            "List members of a group",
            lambda **kwargs: tools.list_group_members(self.gitlab_client, **kwargs),
        )

    async def startup(self) -> None:
        """
        Start the MCP server.

        Authenticates with GitLab and prepares the server for handling requests.

        Raises:
            NetworkError: If connection to GitLab fails
            AuthenticationError: If authentication fails
        """
        # Authenticate with GitLab
        self.gitlab_client.authenticate()

    async def shutdown(self) -> None:
        """
        Shutdown the MCP server gracefully.

        Performs cleanup operations before server shutdown.
        """
        # Currently no cleanup needed, but method exists for future use
        pass

    async def list_tools(self) -> list[dict[str, Any]]:
        """
        List all available MCP tools.

        Returns:
            List of tool dictionaries with name and description
        """
        return [
            {"name": name, "description": tool["description"]} for name, tool in self._tools.items()
        ]

    def register_tool(self, name: str, description: str, function: Callable[..., Any]) -> None:
        """
        Register a new MCP tool.

        Args:
            name: Tool name
            description: Tool description
            function: Tool function to execute
        """
        self._tools[name] = {
            "name": name,
            "description": description,
            "function": function,
        }

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        """
        Call a registered MCP tool.

        Args:
            name: Tool name to call
            arguments: Tool arguments as a dictionary

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool is not found
        """
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not found")

        tool_function = self._tools[name]["function"]
        return await tool_function(**arguments)

    def get_info(self) -> dict[str, str]:
        """
        Get server information and metadata.

        Returns:
            Dictionary with server name, version, and description
        """
        return {
            "name": self.name,
            "version": "0.1.0",
            "description": "GitLab MCP Server - Model Context Protocol server for GitLab",
        }


def _get_tool_definitions() -> list[tuple[str, str, dict[str, Any]]]:
    """
    Get tool definitions with JSON schemas for all 67 GitLab MCP tools.

    Returns:
        List of tuples: (name, description, input_schema)
    """
    return [
        # Context tools (1)
        ("get_current_context", "Get current GitLab user and server context information", {}),
        # Repository tools (6)
        (
            "list_repository_tree",
            "List files and directories in a repository tree",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "path": {"type": "string", "description": "Path in repository (optional)"},
                "ref": {
                    "type": "string",
                    "description": "Branch, tag, or commit SHA (optional, default: HEAD)",
                },
                "recursive": {
                    "type": "boolean",
                    "description": "List recursively (optional, default: false)",
                },
            },
        ),
        (
            "get_file_contents",
            "Get the contents of a file from a repository",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "file_path": {"type": "string", "description": "Path to file in repository"},
                "ref": {
                    "type": "string",
                    "description": "Branch, tag, or commit SHA (optional, default: HEAD)",
                },
            },
        ),
        (
            "search_code",
            "Search for code in project repositories",
            {
                "search_term": {"type": "string", "description": "Search query string"},
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (optional, search all accessible projects if not specified)",
                },
            },
        ),
        (
            "create_file",
            "Create a new file in a repository with commit",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "file_path": {
                    "type": "string",
                    "description": "Full path for the new file (e.g., 'src/main.py')",
                },
                "branch": {
                    "type": "string",
                    "description": "Name of the branch to create the file in",
                },
                "content": {
                    "type": "string",
                    "description": "Content of the file (text or base64-encoded)",
                },
                "commit_message": {
                    "type": "string",
                    "description": "Commit message for the file creation",
                },
                "author_email": {
                    "type": "string",
                    "description": "Email of commit author (optional)",
                },
                "author_name": {
                    "type": "string",
                    "description": "Name of commit author (optional)",
                },
                "encoding": {
                    "type": "string",
                    "description": "Content encoding: 'text' or 'base64' (optional, default: text)",
                },
            },
        ),
        (
            "update_file",
            "Update existing file content with commit",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "file_path": {"type": "string", "description": "Full path to the file to update"},
                "branch": {
                    "type": "string",
                    "description": "Name of the branch containing the file",
                },
                "content": {
                    "type": "string",
                    "description": "New content for the file (text or base64-encoded)",
                },
                "commit_message": {
                    "type": "string",
                    "description": "Commit message for the file update",
                },
                "author_email": {
                    "type": "string",
                    "description": "Email of commit author (optional)",
                },
                "author_name": {
                    "type": "string",
                    "description": "Name of commit author (optional)",
                },
                "encoding": {
                    "type": "string",
                    "description": "Content encoding: 'text' or 'base64' (optional, default: text)",
                },
            },
        ),
        (
            "delete_file",
            "Delete a file from repository with commit",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "file_path": {"type": "string", "description": "Full path to the file to delete"},
                "branch": {
                    "type": "string",
                    "description": "Name of the branch containing the file",
                },
                "commit_message": {
                    "type": "string",
                    "description": "Commit message for the file deletion",
                },
                "author_email": {
                    "type": "string",
                    "description": "Email of commit author (optional)",
                },
                "author_name": {
                    "type": "string",
                    "description": "Name of commit author (optional)",
                },
            },
        ),
        # Issue tools (3)
        (
            "list_issues",
            "List issues for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "state": {
                    "type": "string",
                    "description": "Filter by state: opened, closed, all (optional, default: opened)",
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter by labels (optional)",
                },
                "milestone": {
                    "type": "string",
                    "description": "Filter by milestone title (optional)",
                },
                "author_id": {"type": "integer", "description": "Filter by author ID (optional)"},
                "assignee_id": {
                    "type": "integer",
                    "description": "Filter by assignee ID (optional)",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page (optional, default: 20)",
                },
            },
        ),
        (
            "get_issue",
            "Get details of a specific issue",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "issue_iid": {"type": "integer", "description": "Issue IID (internal ID)"},
            },
        ),
        (
            "create_issue",
            "Create a new issue in a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "title": {"type": "string", "description": "Issue title"},
                "description": {"type": "string", "description": "Issue description (optional)"},
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels (optional)",
                },
                "assignee_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Assignee user IDs (optional)",
                },
                "milestone_id": {"type": "integer", "description": "Milestone ID (optional)"},
            },
        ),
        # Merge Request tools (12)
        (
            "list_merge_requests",
            "List merge requests for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "state": {
                    "type": "string",
                    "description": "Filter by state: opened, closed, merged, all (optional, default: opened)",
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter by labels (optional)",
                },
                "milestone": {
                    "type": "string",
                    "description": "Filter by milestone title (optional)",
                },
                "author_id": {"type": "integer", "description": "Filter by author ID (optional)"},
                "assignee_id": {
                    "type": "integer",
                    "description": "Filter by assignee ID (optional)",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page (optional, default: 20)",
                },
            },
        ),
        (
            "get_merge_request",
            "Get details of a specific merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        (
            "create_merge_request",
            "Create a new merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "source_branch": {"type": "string", "description": "Source branch name"},
                "target_branch": {"type": "string", "description": "Target branch name"},
                "title": {"type": "string", "description": "MR title"},
                "description": {"type": "string", "description": "MR description (optional)"},
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Labels (optional)",
                },
                "assignee_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "Assignee user IDs (optional)",
                },
                "milestone_id": {"type": "integer", "description": "Milestone ID (optional)"},
            },
        ),
        (
            "update_merge_request",
            "Update an existing merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
                "title": {"type": "string", "description": "New title (optional)"},
                "description": {"type": "string", "description": "New description (optional)"},
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "New labels (optional)",
                },
                "assignee_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "New assignee user IDs (optional)",
                },
                "milestone_id": {"type": "integer", "description": "New milestone ID (optional)"},
            },
        ),
        (
            "merge_merge_request",
            "Merge an approved merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
                "merge_commit_message": {
                    "type": "string",
                    "description": "Merge commit message (optional)",
                },
                "should_remove_source_branch": {
                    "type": "boolean",
                    "description": "Remove source branch after merge (optional)",
                },
            },
        ),
        (
            "close_merge_request",
            "Close a merge request without merging",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        (
            "reopen_merge_request",
            "Reopen a closed merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        (
            "approve_merge_request",
            "Approve a merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        (
            "unapprove_merge_request",
            "Remove approval from a merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        (
            "get_merge_request_changes",
            "Get the file changes in a merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        (
            "get_merge_request_commits",
            "Get commits in a merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        (
            "get_merge_request_pipelines",
            "Get pipelines for a merge request",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "mr_iid": {"type": "integer", "description": "Merge request IID (internal ID)"},
            },
        ),
        # Pipeline tools (14)
        (
            "list_pipelines",
            "List pipelines for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "ref": {"type": "string", "description": "Filter by branch/tag (optional)"},
                "status": {
                    "type": "string",
                    "description": "Filter by status: running, pending, success, failed, canceled (optional)",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page (optional, default: 20)",
                },
            },
        ),
        (
            "get_pipeline",
            "Get details of a specific pipeline",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "pipeline_id": {"type": "integer", "description": "Pipeline ID"},
            },
        ),
        (
            "create_pipeline",
            "Create a new pipeline",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "ref": {"type": "string", "description": "Branch or tag name"},
                "variables": {"type": "object", "description": "Pipeline variables (optional)"},
            },
        ),
        (
            "retry_pipeline",
            "Retry a failed pipeline",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "pipeline_id": {"type": "integer", "description": "Pipeline ID"},
            },
        ),
        (
            "cancel_pipeline",
            "Cancel a running pipeline",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "pipeline_id": {"type": "integer", "description": "Pipeline ID"},
            },
        ),
        (
            "delete_pipeline",
            "Delete a pipeline",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "pipeline_id": {"type": "integer", "description": "Pipeline ID"},
            },
        ),
        (
            "list_pipeline_jobs",
            "List jobs in a pipeline",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "pipeline_id": {"type": "integer", "description": "Pipeline ID"},
            },
        ),
        (
            "get_job",
            "Get details of a specific job",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "job_id": {"type": "integer", "description": "Job ID"},
            },
        ),
        (
            "get_job_trace",
            "Get the trace log of a job. Use tail_lines parameter to limit output for large logs.",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "job_id": {"type": "integer", "description": "Job ID"},
                "tail_lines": {
                    "type": "integer",
                    "description": "Optional: Number of lines to return from end of log (e.g., 500-1000 for error analysis). Prevents exceeding token limits on large logs.",
                },
            },
        ),
        (
            "retry_job",
            "Retry a failed job",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "job_id": {"type": "integer", "description": "Job ID"},
            },
        ),
        (
            "cancel_job",
            "Cancel a running job",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "job_id": {"type": "integer", "description": "Job ID"},
            },
        ),
        (
            "play_job",
            "Play a manual job",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "job_id": {"type": "integer", "description": "Job ID"},
            },
        ),
        (
            "download_job_artifacts",
            "Download artifacts from a job",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "job_id": {"type": "integer", "description": "Job ID"},
                "artifact_path": {
                    "type": "string",
                    "description": "Path to specific artifact (optional, download all if not specified)",
                },
            },
        ),
        (
            "list_pipeline_variables",
            "List variables for a pipeline",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "pipeline_id": {"type": "integer", "description": "Pipeline ID"},
            },
        ),
        # Project tools (9)
        (
            "list_projects",
            "List projects accessible by the user",
            {
                "visibility": {
                    "type": "string",
                    "description": "Filter by visibility: public, internal, private (optional)",
                },
                "owned": {"type": "boolean", "description": "Limit to owned projects (optional)"},
                "membership": {
                    "type": "boolean",
                    "description": "Limit to projects where user is a member (optional)",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Results per page (optional, default: 20)",
                },
            },
        ),
        (
            "get_project",
            "Get details of a specific project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
            },
        ),
        (
            "search_projects",
            "Search for projects by name or description",
            {
                "search_term": {"type": "string", "description": "Search query string"},
            },
        ),
        (
            "list_project_members",
            "List members of a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
            },
        ),
        (
            "get_project_statistics",
            "Get statistics for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
            },
        ),
        (
            "list_milestones",
            "List milestones for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "state": {
                    "type": "string",
                    "description": "Filter by state: active, closed, all (optional, default: active)",
                },
            },
        ),
        (
            "get_milestone",
            "Get details of a specific milestone",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "milestone_id": {"type": "integer", "description": "Milestone ID"},
            },
        ),
        (
            "create_milestone",
            "Create a new milestone",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "title": {"type": "string", "description": "Milestone title"},
                "description": {
                    "type": "string",
                    "description": "Milestone description (optional)",
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date (YYYY-MM-DD format, optional)",
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date (YYYY-MM-DD format, optional)",
                },
            },
        ),
        (
            "update_milestone",
            "Update an existing milestone",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "milestone_id": {"type": "integer", "description": "Milestone ID"},
                "title": {"type": "string", "description": "New title (optional)"},
                "description": {"type": "string", "description": "New description (optional)"},
                "due_date": {
                    "type": "string",
                    "description": "New due date (YYYY-MM-DD format, optional)",
                },
                "start_date": {
                    "type": "string",
                    "description": "New start date (YYYY-MM-DD format, optional)",
                },
                "state_event": {
                    "type": "string",
                    "description": "State event: close, activate (optional)",
                },
            },
        ),
        # Label tools (4)
        (
            "list_labels",
            "List labels for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
            },
        ),
        (
            "create_label",
            "Create a new label",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "name": {"type": "string", "description": "Label name"},
                "color": {
                    "type": "string",
                    "description": "Label color (hex format, e.g., '#FF0000')",
                },
                "description": {"type": "string", "description": "Label description (optional)"},
            },
        ),
        (
            "update_label",
            "Update an existing label",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "name": {"type": "string", "description": "Current label name"},
                "new_name": {"type": "string", "description": "New label name (optional)"},
                "color": {"type": "string", "description": "New color (hex format, optional)"},
                "description": {"type": "string", "description": "New description (optional)"},
            },
        ),
        (
            "delete_label",
            "Delete a label",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "name": {"type": "string", "description": "Label name"},
            },
        ),
        # Wiki tools (5)
        (
            "list_wiki_pages",
            "List wiki pages for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
            },
        ),
        (
            "get_wiki_page",
            "Get content of a specific wiki page",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "slug": {
                    "type": "string",
                    "description": "Wiki page slug (URL-friendly identifier)",
                },
            },
        ),
        (
            "create_wiki_page",
            "Create a new wiki page",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "title": {"type": "string", "description": "Page title"},
                "content": {"type": "string", "description": "Page content (Markdown format)"},
            },
        ),
        (
            "update_wiki_page",
            "Update an existing wiki page",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "slug": {
                    "type": "string",
                    "description": "Wiki page slug (URL-friendly identifier)",
                },
                "title": {"type": "string", "description": "New page title (optional)"},
                "content": {"type": "string", "description": "New page content (optional)"},
            },
        ),
        (
            "delete_wiki_page",
            "Delete a wiki page",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "slug": {
                    "type": "string",
                    "description": "Wiki page slug (URL-friendly identifier)",
                },
            },
        ),
        # Snippet tools (5)
        (
            "list_snippets",
            "List snippets for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
            },
        ),
        (
            "get_snippet",
            "Get content of a specific snippet",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "snippet_id": {"type": "integer", "description": "Snippet ID"},
            },
        ),
        (
            "create_snippet",
            "Create a new snippet",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "title": {"type": "string", "description": "Snippet title"},
                "file_name": {"type": "string", "description": "File name"},
                "content": {"type": "string", "description": "Snippet content"},
                "visibility": {
                    "type": "string",
                    "description": "Visibility: private, internal, public (optional, default: private)",
                },
            },
        ),
        (
            "update_snippet",
            "Update an existing snippet",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "snippet_id": {"type": "integer", "description": "Snippet ID"},
                "title": {"type": "string", "description": "New title (optional)"},
                "file_name": {"type": "string", "description": "New file name (optional)"},
                "content": {"type": "string", "description": "New content (optional)"},
                "visibility": {"type": "string", "description": "New visibility (optional)"},
            },
        ),
        (
            "delete_snippet",
            "Delete a snippet",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "snippet_id": {"type": "integer", "description": "Snippet ID"},
            },
        ),
        # Release tools (5)
        (
            "list_releases",
            "List releases for a project",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
            },
        ),
        (
            "get_release",
            "Get details of a specific release",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "tag_name": {
                    "type": "string",
                    "description": "Git tag name associated with release",
                },
            },
        ),
        (
            "create_release",
            "Create a new release",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "tag_name": {"type": "string", "description": "Git tag name"},
                "name": {"type": "string", "description": "Release name"},
                "description": {"type": "string", "description": "Release description (optional)"},
                "ref": {
                    "type": "string",
                    "description": "Commit SHA, branch, or tag (optional, default: default branch)",
                },
            },
        ),
        (
            "update_release",
            "Update an existing release",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "tag_name": {"type": "string", "description": "Git tag name"},
                "name": {"type": "string", "description": "New release name (optional)"},
                "description": {
                    "type": "string",
                    "description": "New release description (optional)",
                },
            },
        ),
        (
            "delete_release",
            "Delete a release",
            {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or path (e.g., 'group/project')",
                },
                "tag_name": {"type": "string", "description": "Git tag name"},
            },
        ),
        # User tools (3)
        (
            "get_user",
            "Get details of a specific user",
            {
                "user_id": {"type": "integer", "description": "User ID"},
            },
        ),
        (
            "search_users",
            "Search for users by username or email",
            {
                "search": {"type": "string", "description": "Search query string"},
            },
        ),
        (
            "list_user_projects",
            "List projects for a specific user",
            {
                "user_id": {"type": "integer", "description": "User ID"},
            },
        ),
        # Group tools (3)
        (
            "list_groups",
            "List groups accessible by the user",
            {
                "owned": {"type": "boolean", "description": "Limit to owned groups (optional)"},
                "per_page": {
                    "type": "integer",
                    "description": "Results per page (optional, default: 20)",
                },
            },
        ),
        (
            "get_group",
            "Get details of a specific group",
            {
                "group_id": {"type": "string", "description": "Group ID or path"},
            },
        ),
        (
            "list_group_members",
            "List members of a group",
            {
                "group_id": {"type": "string", "description": "Group ID or path"},
            },
        ),
    ]


async def async_main() -> None:
    """
    Async main entry point for the GitLab MCP Server.

    This function starts the MCP server with stdio transport, allowing
    Claude Code and other MCP clients to communicate with GitLab.
    """
    # Load configuration from environment
    config = load_config()

    # Create the MCP server instance
    server = Server("gitlab-mcp-server")

    # Create GitLab client
    client = GitLabClient(config)

    # Authenticate client on startup
    try:
        client.authenticate()
    except Exception as e:
        import sys

        print(f"Failed to authenticate with GitLab: {e}", file=sys.stderr)
        sys.exit(1)

    # Get tool definitions
    tool_defs = _get_tool_definitions()

    # Register list_tools handler
    @server.list_tools()
    async def list_tools() -> list[Any]:
        """List all available GitLab tools."""
        from mcp.types import Tool

        result = []
        for name, description, params_schema in tool_defs:
            # Build JSON schema for tool
            properties = {}
            required = []

            for param_name, param_def in params_schema.items():
                properties[param_name] = param_def.copy()
                # Mark parameters as required if they don't have "optional" in description
                if "optional" not in param_def.get("description", "").lower():
                    required.append(param_name)

            input_schema = {
                "type": "object",
                "properties": properties,
            }

            if required:
                input_schema["required"] = required

            result.append(
                Tool(
                    name=name,
                    description=description,
                    inputSchema=input_schema,
                )
            )

        return result

    # Register call_tool handler
    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[Any]:
        """Execute a GitLab tool by name with the provided arguments."""
        from mcp.types import TextContent

        # Route tool calls to appropriate functions
        tool_func = getattr(tools, name, None)
        if tool_func is None:
            raise ValueError(f"Unknown tool: {name}")

        try:
            # Call the tool function with client and arguments
            result = await tool_func(client, **arguments)

            # Convert result to MCP response format
            import json

            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            # Return error as text content
            return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]

    # Run the server with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main() -> None:
    """CLI entry point for the GitLab MCP Server."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
