"""
Unit tests for label tools.

Tests the MCP tools for GitLab label operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.labels import create_label, delete_label, list_labels, update_label


class TestListLabels:
    """Test list_labels tool."""

    @pytest.mark.asyncio
    async def test_list_labels_returns_list(self):
        """Test listing labels."""
        mock_client = Mock()
        mock_labels = [
            {"id": 1, "name": "bug", "color": "#FF0000"},
            {"id": 2, "name": "feature", "color": "#00FF00"},
        ]
        mock_client.list_labels = Mock(return_value=mock_labels)

        result = await list_labels(mock_client, 123)

        mock_client.list_labels.assert_called_once_with(project_id=123, search=None)
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_labels_with_search(self):
        """Test listing labels with search filter."""
        mock_client = Mock()
        mock_client.list_labels = Mock(return_value=[])

        await list_labels(mock_client, "project/path", search="bug")

        mock_client.list_labels.assert_called_once_with(project_id="project/path", search="bug")


class TestCreateLabel:
    """Test create_label tool."""

    @pytest.mark.asyncio
    async def test_create_label_minimal(self):
        """Test creating label with minimal parameters."""
        mock_client = Mock()
        mock_label = {"id": 1, "name": "bug", "color": "#FF0000"}
        mock_client.create_label = Mock(return_value=mock_label)

        result = await create_label(mock_client, 123, "bug", "#FF0000")

        mock_client.create_label.assert_called_once_with(
            project_id=123,
            name="bug",
            color="#FF0000",
            description=None,
            priority=None,
        )
        assert result["name"] == "bug"

    @pytest.mark.asyncio
    async def test_create_label_with_all_parameters(self):
        """Test creating label with all parameters."""
        mock_client = Mock()
        mock_label = {"id": 1}
        mock_client.create_label = Mock(return_value=mock_label)

        await create_label(
            mock_client,
            "project/path",
            "high-priority",
            "#FF0000",
            description="Critical bugs",
            priority=1,
        )

        mock_client.create_label.assert_called_once_with(
            project_id="project/path",
            name="high-priority",
            color="#FF0000",
            description="Critical bugs",
            priority=1,
        )


class TestUpdateLabel:
    """Test update_label tool."""

    @pytest.mark.asyncio
    async def test_update_label(self):
        """Test updating label."""
        mock_client = Mock()
        mock_label = {"id": 1, "name": "critical-bug", "color": "#CC0000"}
        mock_client.update_label = Mock(return_value=mock_label)

        result = await update_label(mock_client, 123, 1, new_name="critical-bug", color="#CC0000")

        mock_client.update_label.assert_called_once_with(
            project_id=123,
            label_id=1,
            new_name="critical-bug",
            color="#CC0000",
            description=None,
            priority=None,
        )
        assert result["name"] == "critical-bug"


class TestDeleteLabel:
    """Test delete_label tool."""

    @pytest.mark.asyncio
    async def test_delete_label(self):
        """Test deleting label."""
        mock_client = Mock()
        mock_client.delete_label = Mock(return_value=None)

        await delete_label(mock_client, "project/path", 1)

        mock_client.delete_label.assert_called_once_with(project_id="project/path", label_id=1)
