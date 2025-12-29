"""Resource Handlers for MCP Resources.

Provides functions to read GitLab resources based on URI patterns.
"""

from collections.abc import Callable, Coroutine
from typing import Any

from gitlab_mcp.resources.registry import ResourceRegistry

# Singleton registry instance
_registry = ResourceRegistry()

# Type alias for resource handlers
ResourceHandler = Callable[[dict[str, str], Any], Coroutine[Any, Any, Any]]


async def _handle_project(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id} resource."""
    return await client.get_project(params["project_id"])


async def _handle_readme(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/readme resource."""
    project_id = params["project_id"]
    for filename in ["README.md", "README.rst", "README.txt", "README"]:
        try:
            return await client.get_file_contents(project_id, filename)
        except Exception:
            continue
    raise ValueError(f"README not found in project {project_id}")


async def _handle_gitlab_ci(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/.gitlab-ci.yml resource."""
    return await client.get_file_contents(params["project_id"], ".gitlab-ci.yml")


async def _handle_issues_open(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/issues/open resource."""
    return await client.list_issues(params["project_id"], state="opened")


async def _handle_issue(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/issues/{iid} resource."""
    return await client.get_issue(params["project_id"], int(params["iid"]))


async def _handle_mrs_open(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/mrs/open resource."""
    return await client.list_merge_requests(params["project_id"], state="opened")


async def _handle_mr(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/mrs/{iid} resource."""
    return await client.get_merge_request(params["project_id"], int(params["iid"]))


async def _handle_pipelines_recent(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/pipelines/recent resource."""
    return await client.list_pipelines(params["project_id"], per_page=10)


async def _handle_pipeline(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/pipelines/{id} resource."""
    return await client.get_pipeline(params["project_id"], int(params["id"]))


async def _handle_branches(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/branches resource."""
    return await client.list_branches(params["project_id"])


async def _handle_file(params: dict[str, str], client: Any) -> Any:
    """Handle gitlab://project/{project_id}/file/{path} resource."""
    return await client.get_file_contents(params["project_id"], params["path"])


# Dispatch table for templated resource handlers
_TEMPLATE_HANDLERS: dict[str, ResourceHandler] = {
    "gitlab://project/{project_id}": _handle_project,
    "gitlab://project/{project_id}/readme": _handle_readme,
    "gitlab://project/{project_id}/.gitlab-ci.yml": _handle_gitlab_ci,
    "gitlab://project/{project_id}/issues/open": _handle_issues_open,
    "gitlab://project/{project_id}/issues/{iid}": _handle_issue,
    "gitlab://project/{project_id}/mrs/open": _handle_mrs_open,
    "gitlab://project/{project_id}/mrs/{iid}": _handle_mr,
    "gitlab://project/{project_id}/pipelines/recent": _handle_pipelines_recent,
    "gitlab://project/{project_id}/pipelines/{id}": _handle_pipeline,
    "gitlab://project/{project_id}/branches": _handle_branches,
    "gitlab://project/{project_id}/file/{path}": _handle_file,
}


async def read_resource(uri: str, client: Any) -> Any:
    """Read a GitLab resource by URI.

    Args:
        uri: Resource URI (e.g., "gitlab://projects")
        client: GitLabClient instance

    Returns:
        Resource data (dict or list)

    Raises:
        ValueError: If URI is invalid or resource not found
    """
    if not uri or not uri.startswith("gitlab://"):
        raise ValueError(f"Invalid resource URI: {uri}")

    match = _registry.match_uri(uri)
    if match is None:
        raise ValueError(f"Unknown resource: {uri}")

    if match.get("is_static"):
        return await _read_static_resource(uri, client)
    else:
        return await _read_templated_resource(match, client)


async def _read_static_resource(uri: str, client: Any) -> Any:
    """Read a static resource.

    Args:
        uri: Resource URI
        client: GitLabClient instance

    Returns:
        Resource data
    """
    if uri == "gitlab://projects":
        return await client.list_projects()
    elif uri == "gitlab://user/current":
        return await client.get_current_user()
    elif uri == "gitlab://groups":
        return await client.list_groups()
    else:
        raise ValueError(f"Unknown static resource: {uri}")


async def _read_templated_resource(match: dict[str, Any], client: Any) -> Any:
    """Read a templated resource using dispatch table.

    Args:
        match: Match result from registry
        client: GitLabClient instance

    Returns:
        Resource data
    """
    template = match["template"]
    params = match["params"]

    handler = _TEMPLATE_HANDLERS.get(template)
    if handler is None:
        raise ValueError(f"Unknown resource template: {template}")

    return await handler(params, client)
