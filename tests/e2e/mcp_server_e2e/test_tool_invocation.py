"""
Test MCP tool invocation through the server.

These tests verify that:
1. Tools can be called through the server's call_tool method
2. Tool arguments are properly passed through
3. Tool results are properly returned
4. Error handling works correctly
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from gitlab_mcp.config.settings import GitLabConfig
from gitlab_mcp.server import GitLabMCPServer


class TestToolInvocation:
    """Test tool invocation through MCP server."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock GitLab config."""
        config = MagicMock(spec=GitLabConfig)
        config.gitlab_url = "https://gitlab.example.com"
        config.personal_access_token = "fake-token"
        return config

    @pytest.fixture
    def server(self, mock_config):
        """Create a GitLabMCPServer instance."""
        return GitLabMCPServer(config=mock_config)

    @pytest.mark.asyncio
    async def test_call_tool_not_found_raises_error(self, server):
        """Test that calling a non-existent tool raises ValueError."""
        server.register_all_tools()
        with pytest.raises(ValueError, match="Tool 'nonexistent_tool' not found"):
            await server.call_tool("nonexistent_tool", {})

    @pytest.mark.asyncio
    async def test_call_simple_tool_passes_arguments(self, server):
        """Test that call_tool correctly passes arguments to tool functions."""
        # Register a simple test tool
        async def mock_tool(arg1, arg2):
            return {"result": f"{arg1}-{arg2}"}

        server.register_tool("test_tool", "A test tool", mock_tool)

        # Call the tool
        result = await server.call_tool("test_tool", {"arg1": "hello", "arg2": "world"})

        # Verify result
        assert result == {"result": "hello-world"}

    @pytest.mark.asyncio
    async def test_call_tool_with_no_arguments(self, server):
        """Test calling a tool with no arguments."""
        # Register a tool that takes no arguments
        async def mock_tool():
            return {"status": "success"}

        server.register_tool("simple_tool", "Simple tool", mock_tool)

        # Call the tool with empty dict
        result = await server.call_tool("simple_tool", {})

        # Verify result
        assert result == {"status": "success"}

    @pytest.mark.asyncio
    async def test_call_tool_with_complex_arguments(self, server):
        """Test calling a tool with complex arguments (lists, dicts)."""
        # Register a tool that accepts complex types
        async def mock_tool(items, metadata):
            return {"count": len(items), "name": metadata["name"]}

        server.register_tool("complex_tool", "Complex tool", mock_tool)

        # Call with complex arguments
        result = await server.call_tool(
            "complex_tool",
            {"items": [1, 2, 3], "metadata": {"name": "test"}},
        )

        # Verify result
        assert result == {"count": 3, "name": "test"}

    @pytest.mark.asyncio
    async def test_real_tool_invocation_structure(self, server):
        """Test that real tools can be invoked through the server (structure test)."""
        server.register_all_tools()

        # Verify a tool is registered
        assert "get_user" in server._tools

        # Verify the tool function is callable
        tool_info = server._tools["get_user"]
        assert callable(tool_info["function"])


class TestToolInvocationErrorHandling:
    """Test error handling during tool invocation."""

    @pytest.fixture
    def mock_config(self):
        """Create a mock GitLab config."""
        config = MagicMock(spec=GitLabConfig)
        config.gitlab_url = "https://gitlab.example.com"
        config.personal_access_token = "fake-token"
        return config

    @pytest.fixture
    def server(self, mock_config):
        """Create a GitLabMCPServer instance."""
        return GitLabMCPServer(config=mock_config)

    @pytest.mark.asyncio
    async def test_tool_raises_exception_propagates(self, server):
        """Test that exceptions from tools are propagated."""
        # Register a tool that raises an exception
        async def failing_tool():
            raise ValueError("Tool failed")

        server.register_tool("failing_tool", "A failing tool", failing_tool)

        # Call should propagate the exception
        with pytest.raises(ValueError, match="Tool failed"):
            await server.call_tool("failing_tool", {})

    @pytest.mark.asyncio
    async def test_tool_with_missing_required_argument_raises_error(self, server):
        """Test that calling a tool without required arguments raises TypeError."""
        # Register a tool with required arguments
        async def tool_with_args(required_arg):
            return {"arg": required_arg}

        server.register_tool("tool_with_args", "Tool with args", tool_with_args)

        # Calling without required arg should raise TypeError
        with pytest.raises(TypeError):
            await server.call_tool("tool_with_args", {})

    @pytest.mark.asyncio
    async def test_tool_with_invalid_argument_type_propagates_error(self, server):
        """Test that calling a tool with invalid argument types propagates error."""
        # Register a tool that validates types
        async def strict_tool(number: int):
            if not isinstance(number, int):
                raise TypeError("number must be an integer")
            return {"doubled": number * 2}

        server.register_tool("strict_tool", "Strict tool", strict_tool)

        # Calling with wrong type should propagate error
        with pytest.raises(TypeError, match="number must be an integer"):
            await server.call_tool("strict_tool", {"number": "not_a_number"})
