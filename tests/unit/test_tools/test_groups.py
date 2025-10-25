"""
Unit tests for group tools.

Tests the MCP tools for GitLab group operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.groups import get_group, list_group_members, list_groups


class TestListGroups:
    """Test list_groups tool."""

    @pytest.mark.asyncio
    async def test_list_groups_returns_list(self):
        """Test listing groups."""
        mock_client = Mock()
        mock_groups = [{"id": 1, "name": "Group 1"}, {"id": 2, "name": "Group 2"}]
        mock_client.list_groups = Mock(return_value=mock_groups)

        result = await list_groups(mock_client)

        mock_client.list_groups.assert_called_once_with(page=1, per_page=20)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_groups_with_pagination(self):
        """Test listing groups with custom pagination."""
        mock_client = Mock()
        mock_client.list_groups = Mock(return_value=[])

        await list_groups(mock_client, page=3, per_page=50)

        mock_client.list_groups.assert_called_once_with(page=3, per_page=50)


class TestGetGroup:
    """Test get_group tool."""

    @pytest.mark.asyncio
    async def test_get_group_by_id(self):
        """Test getting group by ID."""
        mock_client = Mock()
        mock_group = {"id": 123, "name": "My Group", "path": "my-group"}
        mock_client.get_group = Mock(return_value=mock_group)

        result = await get_group(mock_client, 123)

        mock_client.get_group.assert_called_once_with(group_id=123)
        assert result["id"] == 123

    @pytest.mark.asyncio
    async def test_get_group_by_path(self):
        """Test getting group by path."""
        mock_client = Mock()
        mock_group = {"id": 456, "name": "Another Group", "path": "another-group"}
        mock_client.get_group = Mock(return_value=mock_group)

        result = await get_group(mock_client, "another-group")

        mock_client.get_group.assert_called_once_with(group_id="another-group")
        assert result["path"] == "another-group"


class TestListGroupMembers:
    """Test list_group_members tool."""

    @pytest.mark.asyncio
    async def test_list_group_members_returns_list(self):
        """Test listing group members."""
        mock_client = Mock()
        mock_members = [{"id": 1, "username": "user1"}, {"id": 2, "username": "user2"}]
        mock_client.list_group_members = Mock(return_value=mock_members)

        result = await list_group_members(mock_client, 123)

        mock_client.list_group_members.assert_called_once_with(
            group_id=123, page=1, per_page=20
        )
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_group_members_with_pagination(self):
        """Test listing group members with custom pagination."""
        mock_client = Mock()
        mock_client.list_group_members = Mock(return_value=[])

        await list_group_members(mock_client, "my-group", page=2, per_page=100)

        mock_client.list_group_members.assert_called_once_with(
            group_id="my-group", page=2, per_page=100
        )
