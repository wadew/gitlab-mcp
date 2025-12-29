"""Elicitation Registry for MCP dangerous operation confirmations.

Provides configuration and request generation for tools that require
user confirmation before execution (destructive/irreversible operations).
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ElicitationConfig:
    """Configuration for a tool's elicitation behavior.

    Attributes:
        tool_name: Name of the tool requiring confirmation
        message_template: Template for confirmation message (supports {var} substitution)
        severity: Severity level (info, warning, error)
        condition: Optional condition for when to require confirmation
    """

    tool_name: str
    message_template: str
    severity: str
    condition: str | None = None


@dataclass
class ElicitationRequest:
    """Request for user confirmation before tool execution.

    Attributes:
        tool_name: Name of the tool requiring confirmation
        message: Formatted confirmation message
        severity: Severity level (info, warning, error)
        arguments: Optional tool arguments for context
    """

    tool_name: str
    message: str
    severity: str
    arguments: dict[str, Any] | None = None


# Elicitation configurations for dangerous operations
ELICITATION_CONFIGS: dict[str, ElicitationConfig] = {
    "delete_branch": ElicitationConfig(
        tool_name="delete_branch",
        message_template=(
            "Are you sure you want to delete branch '{branch_name}' "
            "from project '{project_id}'? This action cannot be undone."
        ),
        severity="warning",
        condition="branch_not_merged",
    ),
    "delete_pipeline": ElicitationConfig(
        tool_name="delete_pipeline",
        message_template=(
            "Are you sure you want to delete pipeline {pipeline_id} "
            "from project '{project_id}'? This will remove all job logs and artifacts."
        ),
        severity="warning",
    ),
    "delete_file": ElicitationConfig(
        tool_name="delete_file",
        message_template=(
            "Are you sure you want to delete file '{file_path}' "
            "from project '{project_id}'? This creates a commit deleting the file."
        ),
        severity="warning",
    ),
    "delete_snippet": ElicitationConfig(
        tool_name="delete_snippet",
        message_template=(
            "Are you sure you want to delete snippet {snippet_id} "
            "from project '{project_id}'? This action cannot be undone."
        ),
        severity="warning",
    ),
    "delete_release": ElicitationConfig(
        tool_name="delete_release",
        message_template=(
            "Are you sure you want to delete release '{tag_name}' "
            "from project '{project_id}'? The tag will remain but release notes will be lost."
        ),
        severity="warning",
    ),
    "delete_wiki_page": ElicitationConfig(
        tool_name="delete_wiki_page",
        message_template=(
            "Are you sure you want to delete wiki page '{slug}' "
            "from project '{project_id}'? This action cannot be undone."
        ),
        severity="warning",
    ),
    "delete_label": ElicitationConfig(
        tool_name="delete_label",
        message_template=(
            "Are you sure you want to delete label '{name}' "
            "from project '{project_id}'? It will be removed from all issues and MRs."
        ),
        severity="warning",
    ),
    "close_issue": ElicitationConfig(
        tool_name="close_issue",
        message_template=(
            "Are you sure you want to close issue #{issue_iid} "
            "in project '{project_id}'? It can be reopened later."
        ),
        severity="info",
    ),
    "close_merge_request": ElicitationConfig(
        tool_name="close_merge_request",
        message_template=(
            "Are you sure you want to close merge request !{mr_iid} "
            "in project '{project_id}'? It can be reopened later."
        ),
        severity="info",
    ),
    "merge_merge_request": ElicitationConfig(
        tool_name="merge_merge_request",
        message_template=(
            "Are you sure you want to merge request !{mr_iid} "
            "into the target branch in project '{project_id}'?"
        ),
        severity="info",
    ),
    "cancel_pipeline": ElicitationConfig(
        tool_name="cancel_pipeline",
        message_template=(
            "Are you sure you want to cancel pipeline {pipeline_id} "
            "in project '{project_id}'? All running jobs will be stopped."
        ),
        severity="info",
    ),
    "cancel_job": ElicitationConfig(
        tool_name="cancel_job",
        message_template=(
            "Are you sure you want to cancel job {job_id} " "in project '{project_id}'?"
        ),
        severity="info",
    ),
}

# Default message for unknown tools
DEFAULT_CONFIRMATION_MESSAGE = "Are you sure you want to proceed with this action?"


class ElicitationRegistry:
    """Registry for tool elicitation configurations.

    Manages confirmation requirements for dangerous operations,
    generating appropriate confirmation requests for clients.
    """

    def __init__(self) -> None:
        """Initialize the ElicitationRegistry with default configs."""
        self._configs: dict[str, ElicitationConfig] = ELICITATION_CONFIGS.copy()

    def get_elicitation_config(self, tool_name: str) -> ElicitationConfig | None:
        """Get elicitation configuration for a tool.

        Args:
            tool_name: Name of the tool

        Returns:
            ElicitationConfig if tool requires confirmation, None otherwise
        """
        return self._configs.get(tool_name)

    def requires_confirmation(self, tool_name: str) -> bool:
        """Check if a tool requires user confirmation.

        Args:
            tool_name: Name of the tool

        Returns:
            True if tool requires confirmation, False otherwise
        """
        return tool_name in self._configs

    def list_elicitation_tools(self) -> list[str]:
        """List all tools that require elicitation.

        Returns:
            List of tool names requiring confirmation
        """
        return list(self._configs.keys())

    def format_message(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> str:
        """Format confirmation message with provided arguments.

        Args:
            tool_name: Name of the tool
            **kwargs: Arguments to substitute in message template

        Returns:
            Formatted confirmation message
        """
        config = self._configs.get(tool_name)
        if config is None:
            return DEFAULT_CONFIRMATION_MESSAGE

        try:
            return config.message_template.format(**kwargs)
        except KeyError:
            # Return template with available substitutions
            message = config.message_template
            for key, value in kwargs.items():
                message = message.replace(f"{{{key}}}", str(value))
            return message

    def create_request(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> ElicitationRequest | None:
        """Create an elicitation request for a tool.

        Args:
            tool_name: Name of the tool
            **kwargs: Tool arguments for message formatting

        Returns:
            ElicitationRequest if tool requires confirmation, None otherwise
        """
        config = self._configs.get(tool_name)
        if config is None:
            return None

        message = self.format_message(tool_name, **kwargs)

        return ElicitationRequest(
            tool_name=tool_name,
            message=message,
            severity=config.severity,
            arguments=kwargs if kwargs else None,
        )
