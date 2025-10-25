"""
Unit tests for wiki tools.

Tests the MCP tools for GitLab wiki operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.wikis import (
    create_wiki_page,
    delete_wiki_page,
    get_wiki_page,
    list_wiki_pages,
    update_wiki_page,
)


class TestListWikiPages:
    """Test list_wiki_pages tool."""

    @pytest.mark.asyncio
    async def test_list_wiki_pages_returns_list(self):
        """Test listing wiki pages."""
        mock_client = Mock()
        mock_pages = [{"slug": "home", "title": "Home"}, {"slug": "about", "title": "About"}]
        mock_client.list_wiki_pages = Mock(return_value=mock_pages)

        result = await list_wiki_pages(mock_client, 123)

        mock_client.list_wiki_pages.assert_called_once_with(
            project_id=123, page=None, per_page=None
        )
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_wiki_pages_with_pagination(self):
        """Test listing wiki pages with pagination."""
        mock_client = Mock()
        mock_client.list_wiki_pages = Mock(return_value=[])

        await list_wiki_pages(mock_client, "project/path", page=2, per_page=50)

        mock_client.list_wiki_pages.assert_called_once_with(
            project_id="project/path", page=2, per_page=50
        )


class TestGetWikiPage:
    """Test get_wiki_page tool."""

    @pytest.mark.asyncio
    async def test_get_wiki_page_returns_dict(self):
        """Test getting wiki page content."""
        mock_client = Mock()
        mock_page = {"slug": "home", "title": "Home", "content": "# Welcome"}
        mock_client.get_wiki_page = Mock(return_value=mock_page)

        result = await get_wiki_page(mock_client, "project/path", "home")

        mock_client.get_wiki_page.assert_called_once_with(project_id="project/path", slug="home")
        assert result["slug"] == "home"


class TestCreateWikiPage:
    """Test create_wiki_page tool."""

    @pytest.mark.asyncio
    async def test_create_wiki_page_with_default_format(self):
        """Test creating wiki page with default format."""
        mock_client = Mock()
        mock_page = {"slug": "new-page", "title": "New Page"}
        mock_client.create_wiki_page = Mock(return_value=mock_page)

        result = await create_wiki_page(mock_client, 123, "New Page", "# Content")

        mock_client.create_wiki_page.assert_called_once_with(
            project_id=123,
            title="New Page",
            content="# Content",
            format="markdown",
        )
        assert result["slug"] == "new-page"

    @pytest.mark.asyncio
    async def test_create_wiki_page_with_custom_format(self):
        """Test creating wiki page with custom format."""
        mock_client = Mock()
        mock_page = {"slug": "doc"}
        mock_client.create_wiki_page = Mock(return_value=mock_page)

        await create_wiki_page(
            mock_client, "project/path", "Documentation", "Content", format="asciidoc"
        )

        mock_client.create_wiki_page.assert_called_once_with(
            project_id="project/path",
            title="Documentation",
            content="Content",
            format="asciidoc",
        )


class TestUpdateWikiPage:
    """Test update_wiki_page tool."""

    @pytest.mark.asyncio
    async def test_update_wiki_page(self):
        """Test updating wiki page."""
        mock_client = Mock()
        mock_page = {"slug": "home", "title": "Updated Home"}
        mock_client.update_wiki_page = Mock(return_value=mock_page)

        result = await update_wiki_page(
            mock_client, 123, "home", title="Updated Home", content="New content"
        )

        mock_client.update_wiki_page.assert_called_once_with(
            project_id=123,
            slug="home",
            title="Updated Home",
            content="New content",
            format=None,
        )
        assert result["title"] == "Updated Home"


class TestDeleteWikiPage:
    """Test delete_wiki_page tool."""

    @pytest.mark.asyncio
    async def test_delete_wiki_page(self):
        """Test deleting wiki page."""
        mock_client = Mock()
        mock_client.delete_wiki_page = Mock(return_value=None)

        await delete_wiki_page(mock_client, "project/path", "old-page")

        mock_client.delete_wiki_page.assert_called_once_with(
            project_id="project/path", slug="old-page"
        )
