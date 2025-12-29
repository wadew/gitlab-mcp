"""MCP Tasks module for long-running operations.

This module provides task management for asynchronous GitLab operations
like pipeline creation, polling, and bulk operations.
"""

from gitlab_mcp.tasks.task_manager import Task, TaskManager, TaskState

__all__ = ["Task", "TaskManager", "TaskState"]
