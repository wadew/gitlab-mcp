"""Resource Handlers for MCP Resources.

Provides functions to read GitLab resources based on URI patterns.
"""

from typing import Any

from gitlab_mcp.resources.registry import ResourceRegistry

# Singleton registry instance
_registry = ResourceRegistry()


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
    """Read a templated resource.

    Args:
        match: Match result from registry
        client: GitLabClient instance

    Returns:
        Resource data
    """
    template = match["template"]
    params = match["params"]

    if template == "gitlab://project/{project_id}":
        return await client.get_project(params["project_id"])

    elif template == "gitlab://project/{project_id}/readme":
        # Try common README file names
        project_id = params["project_id"]
        for filename in ["README.md", "README.rst", "README.txt", "README"]:
            try:
                result = await client.get_file_contents(project_id, filename)
                return result
            except Exception:
                continue
        raise ValueError(f"README not found in project {project_id}")

    elif template == "gitlab://project/{project_id}/.gitlab-ci.yml":
        return await client.get_file_contents(params["project_id"], ".gitlab-ci.yml")

    elif template == "gitlab://project/{project_id}/issues/open":
        return await client.list_issues(params["project_id"], state="opened")

    elif template == "gitlab://project/{project_id}/issues/{iid}":
        return await client.get_issue(params["project_id"], int(params["iid"]))

    elif template == "gitlab://project/{project_id}/mrs/open":
        return await client.list_merge_requests(params["project_id"], state="opened")

    elif template == "gitlab://project/{project_id}/mrs/{iid}":
        return await client.get_merge_request(params["project_id"], int(params["iid"]))

    elif template == "gitlab://project/{project_id}/pipelines/recent":
        return await client.list_pipelines(params["project_id"], per_page=10)

    elif template == "gitlab://project/{project_id}/pipelines/{id}":
        return await client.get_pipeline(params["project_id"], int(params["id"]))

    elif template == "gitlab://project/{project_id}/branches":
        return await client.list_branches(params["project_id"])

    elif template == "gitlab://project/{project_id}/file/{path}":
        return await client.get_file_contents(params["project_id"], params["path"])

    else:
        raise ValueError(f"Unknown resource template: {template}")
