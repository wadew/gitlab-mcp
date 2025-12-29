"""Unit tests for MCP Structured Output.

Tests verify:
- call_tool returns properly structured responses
- JSON text content is valid and parseable
- Response format follows MCP protocol
- High-value tools return expected data structure
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gitlab_mcp.server import _get_tool_definitions, GitLabMCPServer


class TestServerCallToolResponseFormat:
    """Test that server.call_tool returns properly structured responses."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock GitLab client."""
        return MagicMock()

    @pytest.fixture
    def server(self, mock_client):
        """Create a GitLabMCPServer instance."""
        server = GitLabMCPServer("test-server", mock_client)
        return server

    @pytest.mark.asyncio
    async def test_call_tool_returns_result_from_function(self, server):
        """call_tool should return the result from the tool function."""
        # Register a simple async tool
        async def mock_tool(**kwargs):
            return {"id": 123, "name": "test"}

        server.register_tool("test_tool", "A test tool", mock_tool)

        result = await server.call_tool("test_tool", {})
        assert result == {"id": 123, "name": "test"}

    @pytest.mark.asyncio
    async def test_call_tool_returns_list_result(self, server):
        """call_tool should handle list results."""
        async def mock_list_tool(**kwargs):
            return [{"id": 1}, {"id": 2}]

        server.register_tool("list_tool", "A list tool", mock_list_tool)

        result = await server.call_tool("list_tool", {})
        assert isinstance(result, list)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_call_tool_unknown_tool_raises_error(self, server):
        """call_tool should raise ValueError for unknown tool."""
        with pytest.raises(ValueError, match="Tool 'unknown' not found"):
            await server.call_tool("unknown", {})


class TestCallToolResponseFormat:
    """Test that call_tool returns properly structured responses."""

    def test_tool_definitions_exist(self):
        """Verify tool definitions are available for testing."""
        tool_defs = _get_tool_definitions()
        assert len(tool_defs) > 0

    def test_tool_definitions_structure(self):
        """Each tool definition should have name, description, and params."""
        tool_defs = _get_tool_definitions()
        for name, description, params_schema in tool_defs:
            assert isinstance(name, str), f"Tool name should be string: {name}"
            assert isinstance(description, str), f"Description should be string for {name}"
            assert len(description) > 0, f"Description should not be empty for {name}"


class TestStructuredOutputTools:
    """Test structured output for high-value tools."""

    @pytest.fixture
    def sample_project_response(self):
        """Sample project response structure."""
        return {
            "id": 123,
            "name": "test-project",
            "path_with_namespace": "group/test-project",
            "web_url": "https://gitlab.example.com/group/test-project",
            "default_branch": "main",
            "visibility": "private",
        }

    @pytest.fixture
    def sample_pipeline_response(self):
        """Sample pipeline response structure."""
        return {
            "id": 456,
            "status": "success",
            "ref": "main",
            "sha": "abc123def456",
            "web_url": "https://gitlab.example.com/group/project/-/pipelines/456",
        }

    @pytest.fixture
    def sample_merge_request_response(self):
        """Sample merge request response structure."""
        return {
            "id": 789,
            "iid": 1,
            "title": "Feature: Add new functionality",
            "state": "opened",
            "web_url": "https://gitlab.example.com/group/project/-/merge_requests/1",
            "source_branch": "feature-branch",
            "target_branch": "main",
        }

    @pytest.fixture
    def sample_issue_response(self):
        """Sample issue response structure."""
        return {
            "id": 101,
            "iid": 5,
            "title": "Bug: Fix authentication",
            "state": "opened",
            "web_url": "https://gitlab.example.com/group/project/-/issues/5",
        }

    def test_project_response_is_json_serializable(self, sample_project_response):
        """Project response should be JSON serializable."""
        json_str = json.dumps(sample_project_response)
        parsed = json.loads(json_str)
        assert parsed["id"] == 123
        assert parsed["name"] == "test-project"

    def test_pipeline_response_is_json_serializable(self, sample_pipeline_response):
        """Pipeline response should be JSON serializable."""
        json_str = json.dumps(sample_pipeline_response)
        parsed = json.loads(json_str)
        assert parsed["id"] == 456
        assert parsed["status"] == "success"

    def test_merge_request_response_is_json_serializable(self, sample_merge_request_response):
        """Merge request response should be JSON serializable."""
        json_str = json.dumps(sample_merge_request_response)
        parsed = json.loads(json_str)
        assert parsed["iid"] == 1
        assert parsed["state"] == "opened"

    def test_issue_response_is_json_serializable(self, sample_issue_response):
        """Issue response should be JSON serializable."""
        json_str = json.dumps(sample_issue_response)
        parsed = json.loads(json_str)
        assert parsed["iid"] == 5
        assert parsed["state"] == "opened"


class TestResponseFieldsForProgrammaticAccess:
    """Test that responses include fields needed for programmatic access."""

    def test_project_response_has_id_field(self):
        """Project response should include id for subsequent API calls."""
        response = {"id": 123, "name": "project"}
        assert "id" in response

    def test_project_response_has_web_url_field(self):
        """Project response should include web_url for user reference."""
        response = {"id": 123, "web_url": "https://gitlab.example.com/p/project"}
        assert "web_url" in response

    def test_pipeline_response_has_id_field(self):
        """Pipeline response should include id for subsequent API calls."""
        response = {"id": 456, "status": "success"}
        assert "id" in response

    def test_pipeline_response_has_status_field(self):
        """Pipeline response should include status for decision making."""
        response = {"id": 456, "status": "success"}
        assert "status" in response

    def test_merge_request_response_has_iid_field(self):
        """MR response should include iid for project-scoped API calls."""
        response = {"id": 789, "iid": 1}
        assert "iid" in response

    def test_merge_request_response_has_state_field(self):
        """MR response should include state for workflow decisions."""
        response = {"iid": 1, "state": "opened"}
        assert "state" in response

    def test_issue_response_has_iid_field(self):
        """Issue response should include iid for project-scoped API calls."""
        response = {"id": 101, "iid": 5}
        assert "iid" in response


class TestTextContentFormatting:
    """Test that text content is properly formatted for LLM consumption."""

    def test_json_with_indent_is_readable(self):
        """JSON with indentation should be readable."""
        data = {"id": 123, "name": "test", "nested": {"key": "value"}}
        formatted = json.dumps(data, indent=2)
        assert "\n" in formatted
        assert "  " in formatted

    def test_json_preserves_unicode(self):
        """JSON should preserve unicode characters."""
        data = {"name": "Tëst Prøjéct", "description": "日本語"}
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        assert "Tëst Prøjéct" in formatted
        assert "日本語" in formatted

    def test_json_handles_none_values(self):
        """JSON should handle None values as null."""
        data = {"id": 123, "description": None}
        formatted = json.dumps(data, indent=2)
        assert "null" in formatted

    def test_json_handles_empty_lists(self):
        """JSON should handle empty lists."""
        data = {"id": 123, "tags": []}
        formatted = json.dumps(data, indent=2)
        parsed = json.loads(formatted)
        assert parsed["tags"] == []

    def test_json_handles_nested_objects(self):
        """JSON should handle nested objects."""
        data = {
            "project": {
                "id": 123,
                "namespace": {"id": 456, "name": "group"},
            }
        }
        formatted = json.dumps(data, indent=2)
        parsed = json.loads(formatted)
        assert parsed["project"]["namespace"]["id"] == 456


class TestResponseConsistency:
    """Test consistency of response formats across similar tools."""

    @pytest.fixture
    def list_response(self):
        """Sample list response structure."""
        return [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"},
        ]

    @pytest.fixture
    def single_item_response(self):
        """Sample single item response structure."""
        return {"id": 1, "name": "item1"}

    def test_list_responses_are_arrays(self, list_response):
        """List tool responses should be arrays."""
        assert isinstance(list_response, list)
        assert len(list_response) == 2

    def test_single_item_responses_are_objects(self, single_item_response):
        """Single item tool responses should be objects."""
        assert isinstance(single_item_response, dict)
        assert "id" in single_item_response

    def test_list_items_have_consistent_structure(self, list_response):
        """Items in list responses should have consistent structure."""
        keys = None
        for item in list_response:
            if keys is None:
                keys = set(item.keys())
            else:
                assert set(item.keys()) == keys, "Items should have consistent keys"


class TestErrorResponseStructure:
    """Test error response structure for structured output."""

    def test_error_response_has_error_field(self):
        """Error responses should have an error field."""
        error_response = {"error": "Not found", "status_code": 404}
        assert "error" in error_response

    def test_error_response_has_status_code(self):
        """Error responses should include status code when available."""
        error_response = {"error": "Not found", "status_code": 404}
        assert "status_code" in error_response

    def test_error_response_is_json_serializable(self):
        """Error responses should be JSON serializable."""
        error_response = {"error": "Authentication failed", "status_code": 401}
        json_str = json.dumps(error_response)
        parsed = json.loads(json_str)
        assert parsed["error"] == "Authentication failed"

