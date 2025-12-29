"""Unit tests for MCP Elicitation module.

Tests verify:
- Elicitation registry for dangerous operations
- Confirmation request generation
- Elicitation message formatting
- Tool-specific elicitation logic
"""

import pytest


class TestElicitationRegistry:
    """Test ElicitationRegistry class."""

    def test_registry_exists(self):
        """ElicitationRegistry class should exist."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        assert ElicitationRegistry is not None

    def test_registry_has_get_elicitation_config(self):
        """ElicitationRegistry should have get_elicitation_config method."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        registry = ElicitationRegistry()
        assert hasattr(registry, "get_elicitation_config")

    def test_registry_has_requires_confirmation(self):
        """ElicitationRegistry should have requires_confirmation method."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        registry = ElicitationRegistry()
        assert hasattr(registry, "requires_confirmation")

    def test_registry_has_list_elicitation_tools(self):
        """ElicitationRegistry should have list_elicitation_tools method."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        registry = ElicitationRegistry()
        assert hasattr(registry, "list_elicitation_tools")


class TestElicitationConfig:
    """Test ElicitationConfig dataclass."""

    def test_config_exists(self):
        """ElicitationConfig dataclass should exist."""
        from gitlab_mcp.elicitation.registry import ElicitationConfig

        assert ElicitationConfig is not None

    def test_config_has_tool_name(self):
        """ElicitationConfig should have tool_name field."""
        from gitlab_mcp.elicitation.registry import ElicitationConfig

        config = ElicitationConfig(
            tool_name="delete_branch",
            message_template="Are you sure you want to delete branch '{branch_name}'?",
            severity="warning",
        )
        assert config.tool_name == "delete_branch"

    def test_config_has_message_template(self):
        """ElicitationConfig should have message_template field."""
        from gitlab_mcp.elicitation.registry import ElicitationConfig

        config = ElicitationConfig(
            tool_name="delete_branch",
            message_template="Are you sure you want to delete branch '{branch_name}'?",
            severity="warning",
        )
        assert "branch_name" in config.message_template

    def test_config_has_severity(self):
        """ElicitationConfig should have severity field."""
        from gitlab_mcp.elicitation.registry import ElicitationConfig

        config = ElicitationConfig(
            tool_name="delete_branch",
            message_template="Are you sure?",
            severity="warning",
        )
        assert config.severity == "warning"

    def test_config_has_condition(self):
        """ElicitationConfig should have optional condition field."""
        from gitlab_mcp.elicitation.registry import ElicitationConfig

        config = ElicitationConfig(
            tool_name="delete_branch",
            message_template="Are you sure?",
            severity="warning",
            condition="branch_not_merged",
        )
        assert config.condition == "branch_not_merged"

    def test_config_condition_defaults_to_none(self):
        """ElicitationConfig condition should default to None."""
        from gitlab_mcp.elicitation.registry import ElicitationConfig

        config = ElicitationConfig(
            tool_name="delete_branch",
            message_template="Are you sure?",
            severity="warning",
        )
        assert config.condition is None


class TestDeleteBranchElicitation:
    """Test elicitation for delete_branch tool."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_delete_branch_requires_confirmation(self, registry):
        """delete_branch should require confirmation."""
        assert registry.requires_confirmation("delete_branch") is True

    def test_delete_branch_config_exists(self, registry):
        """delete_branch should have elicitation config."""
        config = registry.get_elicitation_config("delete_branch")
        assert config is not None
        assert config.tool_name == "delete_branch"

    def test_delete_branch_has_warning_severity(self, registry):
        """delete_branch should have warning severity."""
        config = registry.get_elicitation_config("delete_branch")
        assert config.severity == "warning"

    def test_delete_branch_message_mentions_branch(self, registry):
        """delete_branch message should mention branch deletion."""
        config = registry.get_elicitation_config("delete_branch")
        assert "branch" in config.message_template.lower()
        assert "delete" in config.message_template.lower()


class TestDeletePipelineElicitation:
    """Test elicitation for delete_pipeline tool."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_delete_pipeline_requires_confirmation(self, registry):
        """delete_pipeline should require confirmation."""
        assert registry.requires_confirmation("delete_pipeline") is True

    def test_delete_pipeline_config_exists(self, registry):
        """delete_pipeline should have elicitation config."""
        config = registry.get_elicitation_config("delete_pipeline")
        assert config is not None
        assert config.tool_name == "delete_pipeline"

    def test_delete_pipeline_has_warning_severity(self, registry):
        """delete_pipeline should have warning severity."""
        config = registry.get_elicitation_config("delete_pipeline")
        assert config.severity == "warning"


class TestCloseIssueElicitation:
    """Test elicitation for close_issue tool."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_close_issue_requires_confirmation(self, registry):
        """close_issue should require confirmation."""
        assert registry.requires_confirmation("close_issue") is True

    def test_close_issue_config_exists(self, registry):
        """close_issue should have elicitation config."""
        config = registry.get_elicitation_config("close_issue")
        assert config is not None
        assert config.tool_name == "close_issue"

    def test_close_issue_has_info_severity(self, registry):
        """close_issue should have info severity (less destructive)."""
        config = registry.get_elicitation_config("close_issue")
        assert config.severity == "info"


class TestMergeMergeRequestElicitation:
    """Test elicitation for merge_merge_request tool."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_merge_merge_request_requires_confirmation(self, registry):
        """merge_merge_request should require confirmation."""
        assert registry.requires_confirmation("merge_merge_request") is True

    def test_merge_merge_request_config_exists(self, registry):
        """merge_merge_request should have elicitation config."""
        config = registry.get_elicitation_config("merge_merge_request")
        assert config is not None
        assert config.tool_name == "merge_merge_request"

    def test_merge_merge_request_has_info_severity(self, registry):
        """merge_merge_request should have info severity."""
        config = registry.get_elicitation_config("merge_merge_request")
        assert config.severity == "info"

    def test_merge_merge_request_message_mentions_merge(self, registry):
        """merge_merge_request message should mention merge."""
        config = registry.get_elicitation_config("merge_merge_request")
        assert "merge" in config.message_template.lower()


class TestNonElicitationTools:
    """Test that non-dangerous tools don't require confirmation."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_list_projects_no_confirmation(self, registry):
        """list_projects should not require confirmation."""
        assert registry.requires_confirmation("list_projects") is False

    def test_get_project_no_confirmation(self, registry):
        """get_project should not require confirmation."""
        assert registry.requires_confirmation("get_project") is False

    def test_get_issue_no_confirmation(self, registry):
        """get_issue should not require confirmation."""
        assert registry.requires_confirmation("get_issue") is False

    def test_search_code_no_confirmation(self, registry):
        """search_code should not require confirmation."""
        assert registry.requires_confirmation("search_code") is False

    def test_unknown_tool_no_confirmation(self, registry):
        """Unknown tools should not require confirmation."""
        assert registry.requires_confirmation("unknown_tool") is False


class TestListElicitationTools:
    """Test listing all tools with elicitation."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_list_returns_list(self, registry):
        """list_elicitation_tools should return a list."""
        tools = registry.list_elicitation_tools()
        assert isinstance(tools, list)

    def test_list_contains_delete_branch(self, registry):
        """list_elicitation_tools should contain delete_branch."""
        tools = registry.list_elicitation_tools()
        assert "delete_branch" in tools

    def test_list_contains_delete_pipeline(self, registry):
        """list_elicitation_tools should contain delete_pipeline."""
        tools = registry.list_elicitation_tools()
        assert "delete_pipeline" in tools

    def test_list_contains_close_issue(self, registry):
        """list_elicitation_tools should contain close_issue."""
        tools = registry.list_elicitation_tools()
        assert "close_issue" in tools

    def test_list_contains_merge_merge_request(self, registry):
        """list_elicitation_tools should contain merge_merge_request."""
        tools = registry.list_elicitation_tools()
        assert "merge_merge_request" in tools

    def test_list_has_minimum_tools(self, registry):
        """list_elicitation_tools should have at least 4 tools."""
        tools = registry.list_elicitation_tools()
        assert len(tools) >= 4


class TestElicitationMessage:
    """Test elicitation message generation."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_registry_has_format_message(self, registry):
        """ElicitationRegistry should have format_message method."""
        assert hasattr(registry, "format_message")

    def test_format_message_substitutes_variables(self, registry):
        """format_message should substitute template variables."""
        message = registry.format_message(
            "delete_branch",
            branch_name="feature/test",
            project_id="my-project",
        )
        assert "feature/test" in message

    def test_format_message_for_delete_pipeline(self, registry):
        """format_message should work for delete_pipeline."""
        message = registry.format_message(
            "delete_pipeline",
            pipeline_id=12345,
            project_id="my-project",
        )
        assert "12345" in message or "pipeline" in message.lower()

    def test_format_message_unknown_tool_returns_default(self, registry):
        """format_message for unknown tool should return default message."""
        message = registry.format_message("unknown_tool")
        assert message is not None
        assert len(message) > 0


class TestElicitationRequest:
    """Test ElicitationRequest dataclass."""

    def test_request_exists(self):
        """ElicitationRequest dataclass should exist."""
        from gitlab_mcp.elicitation.registry import ElicitationRequest

        assert ElicitationRequest is not None

    def test_request_has_tool_name(self):
        """ElicitationRequest should have tool_name field."""
        from gitlab_mcp.elicitation.registry import ElicitationRequest

        request = ElicitationRequest(
            tool_name="delete_branch",
            message="Are you sure?",
            severity="warning",
        )
        assert request.tool_name == "delete_branch"

    def test_request_has_message(self):
        """ElicitationRequest should have message field."""
        from gitlab_mcp.elicitation.registry import ElicitationRequest

        request = ElicitationRequest(
            tool_name="delete_branch",
            message="Are you sure?",
            severity="warning",
        )
        assert request.message == "Are you sure?"

    def test_request_has_severity(self):
        """ElicitationRequest should have severity field."""
        from gitlab_mcp.elicitation.registry import ElicitationRequest

        request = ElicitationRequest(
            tool_name="delete_branch",
            message="Are you sure?",
            severity="warning",
        )
        assert request.severity == "warning"

    def test_request_has_arguments(self):
        """ElicitationRequest should have optional arguments field."""
        from gitlab_mcp.elicitation.registry import ElicitationRequest

        request = ElicitationRequest(
            tool_name="delete_branch",
            message="Are you sure?",
            severity="warning",
            arguments={"branch_name": "main"},
        )
        assert request.arguments == {"branch_name": "main"}


class TestCreateElicitationRequest:
    """Test creating elicitation requests."""

    @pytest.fixture
    def registry(self):
        """Create ElicitationRegistry instance."""
        from gitlab_mcp.elicitation.registry import ElicitationRegistry

        return ElicitationRegistry()

    def test_registry_has_create_request(self, registry):
        """ElicitationRegistry should have create_request method."""
        assert hasattr(registry, "create_request")

    def test_create_request_returns_request(self, registry):
        """create_request should return ElicitationRequest."""
        from gitlab_mcp.elicitation.registry import ElicitationRequest

        request = registry.create_request(
            "delete_branch",
            branch_name="feature/test",
        )
        assert isinstance(request, ElicitationRequest)

    def test_create_request_sets_tool_name(self, registry):
        """create_request should set tool_name."""
        request = registry.create_request(
            "delete_branch",
            branch_name="feature/test",
        )
        assert request.tool_name == "delete_branch"

    def test_create_request_formats_message(self, registry):
        """create_request should format message with arguments."""
        request = registry.create_request(
            "delete_branch",
            branch_name="feature/test",
        )
        assert "feature/test" in request.message

    def test_create_request_sets_severity(self, registry):
        """create_request should set severity from config."""
        request = registry.create_request(
            "delete_branch",
            branch_name="feature/test",
        )
        assert request.severity == "warning"

    def test_create_request_unknown_tool_returns_none(self, registry):
        """create_request for unknown tool should return None."""
        request = registry.create_request("unknown_tool")
        assert request is None
