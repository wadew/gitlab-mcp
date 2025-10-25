"""
Unit tests for release tools.

Tests the MCP tools for GitLab release operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.releases import (
    create_release,
    delete_release,
    get_release,
    list_releases,
    update_release,
)


class TestListReleases:
    """Test list_releases tool."""

    @pytest.mark.asyncio
    async def test_list_releases_returns_list(self):
        """Test listing releases."""
        mock_client = Mock()
        mock_releases = [{"tag_name": "v1.0"}, {"tag_name": "v2.0"}]
        mock_client.list_releases = Mock(return_value=mock_releases)

        result = await list_releases(mock_client, 123)

        mock_client.list_releases.assert_called_once_with(project_id=123)
        assert len(result) == 2


class TestGetRelease:
    """Test get_release tool."""

    @pytest.mark.asyncio
    async def test_get_release_returns_dict(self):
        """Test getting release details."""
        mock_client = Mock()
        mock_release = {"tag_name": "v1.0", "name": "Release 1.0"}
        mock_client.get_release = Mock(return_value=mock_release)

        result = await get_release(mock_client, "project/path", "v1.0")

        mock_client.get_release.assert_called_once_with(project_id="project/path", tag_name="v1.0")
        assert result["tag_name"] == "v1.0"


class TestCreateRelease:
    """Test create_release tool."""

    @pytest.mark.asyncio
    async def test_create_release_minimal(self):
        """Test creating release with minimal parameters."""
        mock_client = Mock()
        mock_client.create_release = Mock(return_value=None)

        await create_release(mock_client, 123, "v1.0", "Release 1.0")

        mock_client.create_release.assert_called_once_with(
            project_id=123,
            tag_name="v1.0",
            name="Release 1.0",
            description=None,
            ref=None,
        )

    @pytest.mark.asyncio
    async def test_create_release_with_description_and_ref(self):
        """Test creating release with description and ref."""
        mock_client = Mock()
        mock_client.create_release = Mock(return_value=None)

        await create_release(
            mock_client,
            "project/path",
            "v2.0",
            "Release 2.0",
            description="New features",
            ref="main",
        )

        mock_client.create_release.assert_called_once_with(
            project_id="project/path",
            tag_name="v2.0",
            name="Release 2.0",
            description="New features",
            ref="main",
        )


class TestUpdateRelease:
    """Test update_release tool."""

    @pytest.mark.asyncio
    async def test_update_release(self):
        """Test updating release."""
        mock_client = Mock()
        mock_client.update_release = Mock(return_value=None)

        await update_release(
            mock_client, 123, "v1.0", name="Updated 1.0", description="Updated desc"
        )

        mock_client.update_release.assert_called_once_with(
            project_id=123,
            tag_name="v1.0",
            name="Updated 1.0",
            description="Updated desc",
        )


class TestDeleteRelease:
    """Test delete_release tool."""

    @pytest.mark.asyncio
    async def test_delete_release(self):
        """Test deleting release."""
        mock_client = Mock()
        mock_client.delete_release = Mock(return_value=None)

        await delete_release(mock_client, "project/path", "v1.0")

        mock_client.delete_release.assert_called_once_with(
            project_id="project/path", tag_name="v1.0"
        )
