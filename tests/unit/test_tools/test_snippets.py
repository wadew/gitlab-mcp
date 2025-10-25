"""
Unit tests for snippet tools.

Tests the MCP tools for GitLab snippet operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.snippets import (
    create_snippet,
    delete_snippet,
    get_snippet,
    list_snippets,
    update_snippet,
)


class TestListSnippets:
    """Test list_snippets tool."""

    @pytest.mark.asyncio
    async def test_list_snippets_returns_list(self):
        """Test listing snippets."""
        mock_client = Mock()
        mock_snippets = [{"id": 1, "title": "Snippet 1"}, {"id": 2, "title": "Snippet 2"}]
        mock_client.list_snippets = Mock(return_value=mock_snippets)

        result = await list_snippets(mock_client, 123)

        mock_client.list_snippets.assert_called_once_with(project_id=123)
        assert len(result) == 2


class TestGetSnippet:
    """Test get_snippet tool."""

    @pytest.mark.asyncio
    async def test_get_snippet_returns_dict(self):
        """Test getting snippet details."""
        mock_client = Mock()
        mock_snippet = {"id": 1, "title": "Test Snippet", "content": "code here"}
        mock_client.get_snippet = Mock(return_value=mock_snippet)

        result = await get_snippet(mock_client, "project/path", 1)

        mock_client.get_snippet.assert_called_once_with(
            project_id="project/path", snippet_id=1
        )
        assert result["id"] == 1


class TestCreateSnippet:
    """Test create_snippet tool."""

    @pytest.mark.asyncio
    async def test_create_snippet_minimal(self):
        """Test creating snippet with minimal parameters."""
        mock_client = Mock()
        mock_snippet = {"id": 1, "title": "New Snippet"}
        mock_client.create_snippet = Mock(return_value=mock_snippet)

        result = await create_snippet(
            mock_client, 123, "New Snippet", "test.py", "print('hello')"
        )

        mock_client.create_snippet.assert_called_once_with(
            project_id=123,
            title="New Snippet",
            file_name="test.py",
            content="print('hello')",
            description=None,
            visibility="private",
        )
        assert result["id"] == 1

    @pytest.mark.asyncio
    async def test_create_snippet_with_all_parameters(self):
        """Test creating snippet with all parameters."""
        mock_client = Mock()
        mock_snippet = {"id": 1}
        mock_client.create_snippet = Mock(return_value=mock_snippet)

        await create_snippet(
            mock_client,
            "project/path",
            "Public Snippet",
            "script.sh",
            "#!/bin/bash",
            description="Useful script",
            visibility="public",
        )

        mock_client.create_snippet.assert_called_once_with(
            project_id="project/path",
            title="Public Snippet",
            file_name="script.sh",
            content="#!/bin/bash",
            description="Useful script",
            visibility="public",
        )


class TestUpdateSnippet:
    """Test update_snippet tool."""

    @pytest.mark.asyncio
    async def test_update_snippet(self):
        """Test updating snippet."""
        mock_client = Mock()
        mock_snippet = {"id": 1, "title": "Updated"}
        mock_client.update_snippet = Mock(return_value=mock_snippet)

        result = await update_snippet(mock_client, 123, 1, title="Updated", content="new code")

        mock_client.update_snippet.assert_called_once_with(
            project_id=123,
            snippet_id=1,
            title="Updated",
            file_name=None,
            content="new code",
            description=None,
            visibility=None,
        )
        assert result["title"] == "Updated"


class TestDeleteSnippet:
    """Test delete_snippet tool."""

    @pytest.mark.asyncio
    async def test_delete_snippet(self):
        """Test deleting snippet."""
        mock_client = Mock()
        mock_client.delete_snippet = Mock(return_value=None)

        await delete_snippet(mock_client, "project/path", 1)

        mock_client.delete_snippet.assert_called_once_with(
            project_id="project/path", snippet_id=1
        )
