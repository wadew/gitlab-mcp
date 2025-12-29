"""MCP Elicitation module for dangerous operation confirmations.

This module provides elicitation support for tools that require
user confirmation before execution (e.g., delete operations).
"""

from gitlab_mcp.elicitation.registry import (
    ElicitationConfig,
    ElicitationRegistry,
    ElicitationRequest,
)

__all__ = ["ElicitationConfig", "ElicitationRegistry", "ElicitationRequest"]
