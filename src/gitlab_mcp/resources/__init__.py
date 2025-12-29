"""MCP Resources module for GitLab data access.

This module provides MCP Resource primitives for browsing GitLab data
including projects, issues, merge requests, pipelines, and files.
"""

from gitlab_mcp.resources.handlers import read_resource
from gitlab_mcp.resources.registry import ResourceRegistry, parse_resource_uri

__all__ = ["ResourceRegistry", "parse_resource_uri", "read_resource"]
