"""MCP Prompts module for GitLab workflow templates.

This module provides MCP Prompt primitives for common GitLab workflows
including MR creation, pipeline review, code review, and deployment.
"""

from gitlab_mcp.prompts.registry import PromptRegistry

__all__ = ["PromptRegistry"]
