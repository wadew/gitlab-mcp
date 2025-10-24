"""Unit tests for context tools.

Tests for get_current_context and list_projects tools.
Following TDD - these tests are written BEFORE implementation.
"""

from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest

from gitlab_mcp.client.exceptions import (
    AuthenticationError,
    NetworkError,
)
from gitlab_mcp.client.gitlab_client import GitLabClient


class TestGetCurrentContext:
    """Tests for get_current_context tool."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock GitLab client."""
        client = Mock(spec=GitLabClient)
        client.authenticated = True
        return client

    @pytest.fixture
    def mock_user(self) -> dict[str, Any]:
        """Mock user data."""
        return {
            "id": 123,
            "username": "testuser",
            "name": "Test User",
            "email": "test@example.com",
        }

    @pytest.fixture
    def mock_instance_info(self) -> dict[str, Any]:
        """Mock instance information."""
        return {
            "url": "https://gitlab.example.com",
            "version": "16.5.0",
        }

    @pytest.mark.asyncio
    async def test_get_current_context_returns_user_info(
        self, mock_client: Mock, mock_user: dict[str, Any]
    ) -> None:
        """Test that get_current_context returns current user information."""
        # Import here to test that function exists
        from gitlab_mcp.tools.context import get_current_context

        # Setup
        mock_client.get_current_user.return_value = mock_user

        # Execute
        result = await get_current_context(mock_client)

        # Assert
        assert "user" in result
        assert result["user"]["username"] == "testuser"
        assert result["user"]["name"] == "Test User"
        assert result["user"]["email"] == "test@example.com"
        mock_client.get_current_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_context_returns_instance_info(
        self,
        mock_client: Mock,
        mock_user: dict[str, Any],
        mock_instance_info: dict[str, Any],
    ) -> None:
        """Test that get_current_context returns GitLab instance information."""
        from gitlab_mcp.tools.context import get_current_context

        # Setup
        mock_client.get_current_user.return_value = mock_user
        mock_client.get_instance_info.return_value = mock_instance_info

        # Execute
        result = await get_current_context(mock_client)

        # Assert
        assert "instance" in result
        assert result["instance"]["url"] == "https://gitlab.example.com"
        assert result["instance"]["version"] == "16.5.0"
        mock_client.get_instance_info.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_context_includes_authenticated_status(
        self, mock_client: Mock, mock_user: dict[str, Any]
    ) -> None:
        """Test that get_current_context includes authentication status."""
        from gitlab_mcp.tools.context import get_current_context

        # Setup
        mock_client.get_current_user.return_value = mock_user
        mock_client.authenticated = True

        # Execute
        result = await get_current_context(mock_client)

        # Assert
        assert "authenticated" in result
        assert result["authenticated"] is True

    @pytest.mark.asyncio
    async def test_get_current_context_handles_auth_error(self, mock_client: Mock) -> None:
        """Test that get_current_context handles authentication errors gracefully."""
        from gitlab_mcp.tools.context import get_current_context

        # Setup
        mock_client.get_current_user.side_effect = AuthenticationError("Invalid token")

        # Execute & Assert
        with pytest.raises(AuthenticationError) as exc_info:
            await get_current_context(mock_client)
        assert "Invalid token" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_current_context_handles_connection_error(self, mock_client: Mock) -> None:
        """Test that get_current_context handles connection errors gracefully."""
        from gitlab_mcp.tools.context import get_current_context

        # Setup
        mock_client.get_current_user.side_effect = NetworkError("Cannot connect to GitLab")

        # Execute & Assert
        with pytest.raises(NetworkError) as exc_info:
            await get_current_context(mock_client)
        assert "Cannot connect to GitLab" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_current_context_includes_permissions(
        self, mock_client: Mock, mock_user: dict[str, Any]
    ) -> None:
        """Test that get_current_context includes user permission information."""
        from gitlab_mcp.tools.context import get_current_context

        # Setup - add permissions to mock user
        mock_user["is_admin"] = False
        mock_user["can_create_project"] = True
        mock_client.get_current_user.return_value = mock_user

        # Execute
        result = await get_current_context(mock_client)

        # Assert
        assert "user" in result
        assert "is_admin" in result["user"]
        assert "can_create_project" in result["user"]

    @pytest.mark.asyncio
    async def test_get_current_context_with_user_object(self, mock_client: Mock) -> None:
        """Test that get_current_context handles user object (not dict)."""
        from gitlab_mcp.tools.context import get_current_context

        # Setup - create mock user object with attributes
        mock_user_obj = Mock()
        mock_user_obj.username = "objuser"
        mock_user_obj.name = "Object User"
        mock_user_obj.email = "obj@example.com"
        mock_user_obj.id = 456
        mock_user_obj.is_admin = True
        mock_user_obj.can_create_project = False

        mock_client.get_current_user.return_value = mock_user_obj

        # Execute
        result = await get_current_context(mock_client)

        # Assert
        assert "user" in result
        assert result["user"]["username"] == "objuser"
        assert result["user"]["name"] == "Object User"
        assert result["user"]["email"] == "obj@example.com"
        assert result["user"]["id"] == 456
        assert result["user"]["is_admin"] is True
        assert result["user"]["can_create_project"] is False


class TestListProjects:
    """Tests for list_projects tool."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock GitLab client."""
        client = Mock(spec=GitLabClient)
        client.authenticated = True
        return client

    @pytest.fixture
    def mock_projects(self) -> list[dict[str, Any]]:
        """Mock project data."""
        return [
            {
                "id": 1,
                "name": "Project One",
                "path": "project-one",
                "visibility": "private",
                "web_url": "https://gitlab.example.com/group/project-one",
                "description": "Test project 1",
            },
            {
                "id": 2,
                "name": "Project Two",
                "path": "project-two",
                "visibility": "public",
                "web_url": "https://gitlab.example.com/group/project-two",
                "description": "Test project 2",
            },
        ]

    @pytest.mark.asyncio
    async def test_list_projects_returns_accessible_projects(
        self, mock_client: Mock, mock_projects: list[dict[str, Any]]
    ) -> None:
        """Test that list_projects returns user's accessible projects."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client.list_projects.return_value = {
            "projects": mock_projects,
            "total": 2,
            "page": 1,
            "per_page": 20,
        }

        # Execute
        result = await list_projects(mock_client)

        # Assert
        assert "projects" in result
        assert len(result["projects"]) == 2
        assert result["projects"][0]["name"] == "Project One"
        assert result["projects"][1]["name"] == "Project Two"
        mock_client.list_projects.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_projects_includes_project_metadata(
        self, mock_client: Mock, mock_projects: list[dict[str, Any]]
    ) -> None:
        """Test that list_projects includes complete project metadata."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client.list_projects.return_value = {
            "projects": mock_projects,
            "total": 2,
            "page": 1,
            "per_page": 20,
        }

        # Execute
        result = await list_projects(mock_client)

        # Assert
        project = result["projects"][0]
        assert "id" in project
        assert "name" in project
        assert "path" in project
        assert "visibility" in project
        assert "web_url" in project
        assert "description" in project

    @pytest.mark.asyncio
    async def test_list_projects_handles_pagination(
        self, mock_client: Mock, mock_projects: list[dict[str, Any]]
    ) -> None:
        """Test that list_projects handles pagination correctly."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client.list_projects.return_value = {
            "projects": mock_projects,
            "total": 50,
            "page": 2,
            "per_page": 10,
        }

        # Execute
        result = await list_projects(mock_client, page=2, per_page=10)

        # Assert
        assert result["page"] == 2
        assert result["per_page"] == 10
        assert result["total"] == 50
        mock_client.list_projects.assert_called_once_with(visibility=None, page=2, per_page=10)

    @pytest.mark.asyncio
    async def test_list_projects_handles_empty_list(self, mock_client: Mock) -> None:
        """Test that list_projects returns empty list when no projects exist."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client.list_projects.return_value = {
            "projects": [],
            "total": 0,
            "page": 1,
            "per_page": 20,
        }

        # Execute
        result = await list_projects(mock_client)

        # Assert
        assert "projects" in result
        assert len(result["projects"]) == 0
        assert result["total"] == 0

    @pytest.mark.asyncio
    async def test_list_projects_filters_by_visibility_public(
        self, mock_client: Mock, mock_projects: list[dict[str, Any]]
    ) -> None:
        """Test that list_projects can filter by public visibility."""
        from gitlab_mcp.tools.context import list_projects

        # Setup - only public projects
        public_projects = [p for p in mock_projects if p["visibility"] == "public"]
        mock_client.list_projects.return_value = {
            "projects": public_projects,
            "total": len(public_projects),
            "page": 1,
            "per_page": 20,
        }

        # Execute
        result = await list_projects(mock_client, visibility="public")

        # Assert
        assert len(result["projects"]) == 1
        assert result["projects"][0]["visibility"] == "public"
        mock_client.list_projects.assert_called_once_with(visibility="public", page=1, per_page=20)

    @pytest.mark.asyncio
    async def test_list_projects_filters_by_visibility_private(
        self, mock_client: Mock, mock_projects: list[dict[str, Any]]
    ) -> None:
        """Test that list_projects can filter by private visibility."""
        from gitlab_mcp.tools.context import list_projects

        # Setup - only private projects
        private_projects = [p for p in mock_projects if p["visibility"] == "private"]
        mock_client.list_projects.return_value = {
            "projects": private_projects,
            "total": len(private_projects),
            "page": 1,
            "per_page": 20,
        }

        # Execute
        result = await list_projects(mock_client, visibility="private")

        # Assert
        assert len(result["projects"]) == 1
        assert result["projects"][0]["visibility"] == "private"
        mock_client.list_projects.assert_called_once_with(visibility="private", page=1, per_page=20)

    @pytest.mark.asyncio
    async def test_list_projects_filters_by_visibility_internal(self, mock_client: Mock) -> None:
        """Test that list_projects can filter by internal visibility."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        internal_projects = [
            {
                "id": 3,
                "name": "Internal Project",
                "path": "internal-project",
                "visibility": "internal",
                "web_url": "https://gitlab.example.com/group/internal-project",
                "description": "Internal project",
            }
        ]
        mock_client.list_projects.return_value = {
            "projects": internal_projects,
            "total": 1,
            "page": 1,
            "per_page": 20,
        }

        # Execute
        result = await list_projects(mock_client, visibility="internal")

        # Assert
        assert len(result["projects"]) == 1
        assert result["projects"][0]["visibility"] == "internal"
        mock_client.list_projects.assert_called_once_with(
            visibility="internal", page=1, per_page=20
        )

    @pytest.mark.asyncio
    async def test_list_projects_handles_api_error(self, mock_client: Mock) -> None:
        """Test that list_projects handles GitLab API errors gracefully."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client.list_projects.side_effect = NetworkError("API request failed")

        # Execute & Assert
        with pytest.raises(NetworkError) as exc_info:
            await list_projects(mock_client)
        assert "API request failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_list_projects_respects_per_page_max(
        self, mock_client: Mock, mock_projects: list[dict[str, Any]]
    ) -> None:
        """Test that list_projects respects maximum per_page limit."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client.list_projects.return_value = {
            "projects": mock_projects,
            "total": 2,
            "page": 1,
            "per_page": 100,
        }

        # Execute - request 150 per page (should be capped at 100)
        result = await list_projects(mock_client, per_page=100)

        # Assert
        assert result["per_page"] == 100
        mock_client.list_projects.assert_called_once_with(visibility=None, page=1, per_page=100)

    @pytest.mark.asyncio
    async def test_list_projects_default_pagination(
        self, mock_client: Mock, mock_projects: list[dict[str, Any]]
    ) -> None:
        """Test that list_projects uses default pagination values."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client.list_projects.return_value = {
            "projects": mock_projects,
            "total": 2,
            "page": 1,
            "per_page": 20,
        }

        # Execute - no pagination params
        result = await list_projects(mock_client)

        # Assert
        assert result["page"] == 1
        assert result["per_page"] == 20
        mock_client.list_projects.assert_called_once_with(visibility=None, page=1, per_page=20)


class TestToolsIntegration:
    """Tests for context tools integration with MCP server."""

    @pytest.fixture
    def mock_server(self) -> Mock:
        """Create a mock MCP server."""
        from gitlab_mcp.server import GitLabMCPServer

        return Mock(spec=GitLabMCPServer)

    @pytest.mark.asyncio
    async def test_tools_register_with_server(self, mock_server: Mock) -> None:
        """Test that context tools can be registered with MCP server."""
        from gitlab_mcp.tools.context import get_current_context, list_projects

        # Setup
        mock_server.register_tool = Mock()

        # Execute
        mock_server.register_tool("get_current_context", get_current_context)
        mock_server.register_tool("list_projects", list_projects)

        # Assert
        assert mock_server.register_tool.call_count == 2

    @pytest.mark.asyncio
    async def test_get_current_context_executes_via_server(self, mock_server: Mock) -> None:
        """Test that get_current_context can be called via server.call_tool()."""
        from gitlab_mcp.tools.context import get_current_context

        # Setup
        mock_client = Mock(spec=GitLabClient)
        mock_client.get_current_user.return_value = {
            "username": "testuser",
            "name": "Test User",
        }
        mock_client.authenticated = True

        mock_server.call_tool = AsyncMock(return_value=await get_current_context(mock_client))

        # Execute
        result = await mock_server.call_tool("get_current_context", {})

        # Assert
        assert "user" in result
        assert result["user"]["username"] == "testuser"

    @pytest.mark.asyncio
    async def test_list_projects_executes_via_server(self, mock_server: Mock) -> None:
        """Test that list_projects can be called via server.call_tool()."""
        from gitlab_mcp.tools.context import list_projects

        # Setup
        mock_client = Mock(spec=GitLabClient)
        mock_client.list_projects.return_value = {
            "projects": [{"name": "Test Project"}],
            "total": 1,
            "page": 1,
            "per_page": 20,
        }

        mock_server.call_tool = AsyncMock(return_value=await list_projects(mock_client))

        # Execute
        result = await mock_server.call_tool("list_projects", {})

        # Assert
        assert "projects" in result
        assert len(result["projects"]) == 1
