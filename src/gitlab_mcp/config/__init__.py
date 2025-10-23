"""Configuration module for GitLab MCP Server.

This module handles loading and validating configuration from:
- Environment variables (primary source)
- JSON configuration file (secondary source)

Environment variables take precedence over file settings.
"""

from gitlab_mcp.config.settings import GitLabConfig, load_config

__all__ = ["GitLabConfig", "load_config"]
