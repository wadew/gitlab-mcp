"""
Unit tests for MCP server module.

Tests the GitLab MCP server initialization, lifecycle, and tool registration.
Following TDD: These tests are written FIRST (RED phase).
"""

from unittest.mock import patch

import pytest

from gitlab_mcp.client.exceptions import AuthenticationError, NetworkError
from gitlab_mcp.config.settings import GitLabConfig
from gitlab_mcp.server import GitLabMCPServer


class TestGitLabMCPServerInitialization:
    """Test MCP server initialization."""

    def test_server_initialization_with_config(self) -> None:
        """Test that server can be initialized with a valid GitLabConfig."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        server = GitLabMCPServer(config)

        assert server is not None
        assert server.config == config
        assert server.name == "gitlab-mcp-server"

    def test_server_initialization_with_custom_name(self) -> None:
        """Test that server accepts a custom name."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        server = GitLabMCPServer(config, name="custom-gitlab-server")

        assert server.name == "custom-gitlab-server"

    def test_server_has_gitlab_client(self) -> None:
        """Test that server creates a GitLabClient instance."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )

        server = GitLabMCPServer(config)

        assert hasattr(server, "gitlab_client")
        assert server.gitlab_client is not None


class TestGitLabMCPServerLifecycle:
    """Test MCP server startup and shutdown."""

    @pytest.mark.asyncio
    async def test_server_startup_success(self) -> None:
        """Test that server starts successfully with valid config."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        # Mock the GitLab client authentication (synchronous, not async)
        with patch.object(server.gitlab_client, "authenticate") as mock_auth:
            mock_auth.return_value = None

            await server.startup()

            mock_auth.assert_called_once()

    @pytest.mark.asyncio
    async def test_server_startup_handles_connection_error(self) -> None:
        """Test that server handles connection errors gracefully during startup."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        # Mock synchronous authenticate method
        with patch.object(server.gitlab_client, "authenticate") as mock_auth:
            mock_auth.side_effect = NetworkError("Cannot connect")

            with pytest.raises(NetworkError):
                await server.startup()

    @pytest.mark.asyncio
    async def test_server_startup_handles_auth_error(self) -> None:
        """Test that server handles authentication errors during startup."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        # Mock synchronous authenticate method
        with patch.object(server.gitlab_client, "authenticate") as mock_auth:
            mock_auth.side_effect = AuthenticationError("Invalid token")

            with pytest.raises(AuthenticationError):
                await server.startup()

    @pytest.mark.asyncio
    async def test_server_shutdown_success(self) -> None:
        """Test that server shuts down gracefully."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        # Should not raise any exceptions
        await server.shutdown()


class TestGitLabMCPServerToolRegistration:
    """Test MCP tool registration."""

    def test_server_has_list_tools_method(self) -> None:
        """Test that server has a method to list available tools."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        assert hasattr(server, "list_tools")
        assert callable(server.list_tools)

    @pytest.mark.asyncio
    async def test_list_tools_returns_empty_list_initially(self) -> None:
        """Test that list_tools returns empty list when no tools registered."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        tools = await server.list_tools()

        assert isinstance(tools, list)
        assert len(tools) == 0

    def test_server_has_register_tool_method(self) -> None:
        """Test that server has a method to register tools."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        assert hasattr(server, "register_tool")
        assert callable(server.register_tool)

    @pytest.mark.asyncio
    async def test_register_tool_adds_tool_to_list(self) -> None:
        """Test that registering a tool adds it to the tools list."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        # Create a mock tool function
        async def mock_tool(param: str) -> str:
            """Mock tool for testing."""
            return f"Result: {param}"

        # Register the tool
        server.register_tool(name="test_tool", description="A test tool", function=mock_tool)

        # Verify tool is in the list
        tools = await server.list_tools()
        assert len(tools) == 1
        assert tools[0]["name"] == "test_tool"
        assert tools[0]["description"] == "A test tool"


class TestGitLabMCPServerToolExecution:
    """Test MCP tool execution."""

    def test_server_has_call_tool_method(self) -> None:
        """Test that server has a method to call tools."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        assert hasattr(server, "call_tool")
        assert callable(server.call_tool)

    @pytest.mark.asyncio
    async def test_call_tool_executes_registered_tool(self) -> None:
        """Test that call_tool executes a registered tool."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        # Create and register a mock tool
        async def mock_tool(param: str) -> str:
            """Mock tool for testing."""
            return f"Result: {param}"

        server.register_tool(name="test_tool", description="A test tool", function=mock_tool)

        # Call the tool
        result = await server.call_tool("test_tool", {"param": "test_value"})

        assert result == "Result: test_value"

    @pytest.mark.asyncio
    async def test_call_tool_raises_error_for_unknown_tool(self) -> None:
        """Test that call_tool raises error for unknown tool."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        with pytest.raises(ValueError, match="Tool 'unknown_tool' not found"):
            await server.call_tool("unknown_tool", {})


class TestGitLabMCPServerInfo:
    """Test MCP server metadata."""

    def test_server_has_get_info_method(self) -> None:
        """Test that server has a method to get server info."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config)

        assert hasattr(server, "get_info")
        assert callable(server.get_info)

    def test_get_info_returns_server_metadata(self) -> None:
        """Test that get_info returns correct server metadata."""
        config = GitLabConfig(
            gitlab_url="https://gitlab.example.com",
            gitlab_token="test-token-123",
        )
        server = GitLabMCPServer(config, name="test-server")

        info = server.get_info()

        assert isinstance(info, dict)
        assert info["name"] == "test-server"
        assert "version" in info
        assert "description" in info
