"""
Unit tests for user tools.

Tests the MCP tools for GitLab user operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.users import get_user, list_user_projects, search_users


class TestGetUser:
    """Test get_user tool."""

    @pytest.mark.asyncio
    async def test_get_user_returns_dict(self):
        """Test getting user details."""
        mock_client = Mock()
        mock_user = {"id": 123, "username": "john", "name": "John Doe"}
        mock_client.get_user = Mock(return_value=mock_user)

        result = await get_user(mock_client, 123)

        mock_client.get_user.assert_called_once_with(user_id=123)
        assert result["id"] == 123
        assert result["username"] == "john"


class TestSearchUsers:
    """Test search_users tool."""

    @pytest.mark.asyncio
    async def test_search_users_returns_list(self):
        """Test searching for users."""
        mock_client = Mock()
        mock_users = [{"id": 1, "username": "john"}, {"id": 2, "username": "jane"}]
        mock_client.search_users = Mock(return_value=mock_users)

        result = await search_users(mock_client, "jo")

        mock_client.search_users.assert_called_once_with(search="jo", page=1, per_page=20)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_search_users_with_pagination(self):
        """Test searching users with custom pagination."""
        mock_client = Mock()
        mock_client.search_users = Mock(return_value=[])

        await search_users(mock_client, "test", page=3, per_page=50)

        mock_client.search_users.assert_called_once_with(search="test", page=3, per_page=50)


class TestListUserProjects:
    """Test list_user_projects tool."""

    @pytest.mark.asyncio
    async def test_list_user_projects_returns_list(self):
        """Test listing user's projects."""
        mock_client = Mock()
        mock_projects = [
            {"id": 1, "name": "Project 1"},
            {"id": 2, "name": "Project 2"},
        ]
        mock_client.list_user_projects = Mock(return_value=mock_projects)

        result = await list_user_projects(mock_client, 123)

        mock_client.list_user_projects.assert_called_once_with(user_id=123, page=1, per_page=20)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_user_projects_with_pagination(self):
        """Test listing user projects with custom pagination."""
        mock_client = Mock()
        mock_client.list_user_projects = Mock(return_value=[])

        await list_user_projects(mock_client, 456, page=2, per_page=100)

        mock_client.list_user_projects.assert_called_once_with(user_id=456, page=2, per_page=100)
