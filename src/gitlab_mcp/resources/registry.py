"""Resource Registry for MCP Resources.

Provides URI parsing, template matching, and resource metadata for
GitLab MCP resources.
"""

import re
from typing import Any, cast

# Constants for commonly used MIME types
MIME_JSON = "application/json"
MIME_MARKDOWN = "text/markdown"
MIME_YAML = "text/yaml"
MIME_TEXT = "text/plain"


def parse_resource_uri(uri: str) -> dict[str, Any] | None:
    """Parse a gitlab:// URI into components.

    Args:
        uri: URI string to parse (e.g., "gitlab://projects")

    Returns:
        Dictionary with scheme, path, and params, or None if invalid
    """
    if not uri:
        return None

    # Check for gitlab:// scheme
    if not uri.startswith("gitlab://"):
        return None

    # Extract path after scheme
    path = uri[9:]  # len("gitlab://") == 9

    if not path:
        return None

    return {
        "scheme": "gitlab",
        "path": path,
        "params": {},
    }


# Static resources that are always available
STATIC_RESOURCES = [
    {
        "uri": "gitlab://projects",
        "name": "All Projects",
        "description": "List of accessible GitLab projects",
        "mime_type": MIME_JSON,
    },
    {
        "uri": "gitlab://user/current",
        "name": "Current User",
        "description": "Currently authenticated GitLab user",
        "mime_type": MIME_JSON,
    },
    {
        "uri": "gitlab://groups",
        "name": "All Groups",
        "description": "List of accessible GitLab groups",
        "mime_type": MIME_JSON,
    },
]

# Resource templates with parameterized paths
RESOURCE_TEMPLATES = [
    {
        "uri_template": "gitlab://project/{project_id}",
        "name": "Project Details",
        "description": "Get details for a specific project",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/(.+)$",
        "params": ["project_id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/readme",
        "name": "Project README",
        "description": "Get project README content",
        "mime_type": MIME_MARKDOWN,
        "pattern": r"^gitlab://project/([^/]+)/readme$",
        "params": ["project_id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/.gitlab-ci.yml",
        "name": "CI Configuration",
        "description": "Get project CI/CD configuration file",
        "mime_type": MIME_YAML,
        "pattern": r"^gitlab://project/([^/]+)/.gitlab-ci.yml$",
        "params": ["project_id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/issues/open",
        "name": "Open Issues",
        "description": "List open issues for a project",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/([^/]+)/issues/open$",
        "params": ["project_id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/issues/{iid}",
        "name": "Issue Details",
        "description": "Get details for a specific issue",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/([^/]+)/issues/(\d+)$",
        "params": ["project_id", "iid"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/mrs/open",
        "name": "Open Merge Requests",
        "description": "List open merge requests for a project",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/([^/]+)/mrs/open$",
        "params": ["project_id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/mrs/{iid}",
        "name": "Merge Request Details",
        "description": "Get details for a specific merge request",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/([^/]+)/mrs/(\d+)$",
        "params": ["project_id", "iid"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/pipelines/recent",
        "name": "Recent Pipelines",
        "description": "List recent pipelines (last 10)",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/([^/]+)/pipelines/recent$",
        "params": ["project_id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/pipelines/{id}",
        "name": "Pipeline Details",
        "description": "Get details for a specific pipeline",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/([^/]+)/pipelines/(\d+)$",
        "params": ["project_id", "id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/branches",
        "name": "All Branches",
        "description": "List all branches for a project",
        "mime_type": MIME_JSON,
        "pattern": r"^gitlab://project/([^/]+)/branches$",
        "params": ["project_id"],
    },
    {
        "uri_template": "gitlab://project/{project_id}/file/{path}",
        "name": "File Contents",
        "description": "Get contents of a file in the repository",
        "mime_type": MIME_TEXT,
        "pattern": r"^gitlab://project/([^/]+)/file/(.+)$",
        "params": ["project_id", "path"],
    },
]


class ResourceRegistry:
    """Registry for MCP resources with URI matching and metadata."""

    def __init__(self) -> None:
        """Initialize the resource registry."""
        self._static_resources = STATIC_RESOURCES.copy()
        self._resource_templates = RESOURCE_TEMPLATES.copy()

    def get_static_resources(self) -> list[dict[str, Any]]:
        """Get all static resources.

        Returns:
            List of static resource metadata dictionaries
        """
        return self._static_resources.copy()

    def get_resource_templates(self) -> list[dict[str, Any]]:
        """Get all resource templates.

        Returns:
            List of resource template metadata dictionaries
        """
        return self._resource_templates.copy()

    def match_uri(self, uri: str) -> dict[str, Any] | None:
        """Match a URI to a resource or template.

        Args:
            uri: URI to match (e.g., "gitlab://project/123")

        Returns:
            Match result with template and params, or None if no match
        """
        # Check static resources first
        for resource in self._static_resources:
            if uri == resource["uri"]:
                return {
                    "is_static": True,
                    "resource": resource,
                    "params": {},
                }

        # Check templates with more specific patterns first (longer patterns)
        # Sort by pattern length descending to match more specific patterns first
        sorted_templates = sorted(
            self._resource_templates,
            key=lambda t: len(t["pattern"]),
            reverse=True,
        )

        for template in sorted_templates:
            pattern = cast(str, template["pattern"])
            match = re.match(pattern, uri)
            if match:
                # Extract parameters
                params = {}
                for i, param_name in enumerate(template["params"]):
                    params[param_name] = match.group(i + 1)

                return {
                    "is_static": False,
                    "template": template["uri_template"],
                    "resource": template,
                    "params": params,
                }

        return None
