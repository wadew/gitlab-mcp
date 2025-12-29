"""Unit tests for Resource Handlers.

Tests verify:
- Reading static resources (projects, user/current, groups)
- Reading templated resources (project details, issues, MRs, pipelines)
- Error handling for invalid URIs
- Error handling for missing resources
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from gitlab_mcp.resources.registry import ResourceRegistry


class TestResourceHandlers:
    """Test resource handler functions."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock GitLab client."""
        client = MagicMock()
        # Configure async methods
        client.get_current_user = AsyncMock(return_value={
            "id": 1,
            "username": "testuser",
            "name": "Test User",
            "email": "test@example.com",
        })
        client.list_projects = AsyncMock(return_value=[
            {"id": 1, "name": "project-1", "path_with_namespace": "group/project-1"},
            {"id": 2, "name": "project-2", "path_with_namespace": "group/project-2"},
        ])
        client.list_groups = AsyncMock(return_value=[
            {"id": 10, "name": "group-1", "path": "group-1"},
        ])
        client.get_project = AsyncMock(return_value={
            "id": 123,
            "name": "test-project",
            "path_with_namespace": "group/test-project",
        })
        client.get_file_contents = AsyncMock(return_value={
            "content": "# README\nThis is a test project.",
            "file_name": "README.md",
        })
        client.list_issues = AsyncMock(return_value=[
            {"id": 1, "iid": 1, "title": "Issue 1", "state": "opened"},
        ])
        client.get_issue = AsyncMock(return_value={
            "id": 1, "iid": 1, "title": "Issue 1", "state": "opened",
        })
        client.list_merge_requests = AsyncMock(return_value=[
            {"id": 100, "iid": 1, "title": "MR 1", "state": "opened"},
        ])
        client.get_merge_request = AsyncMock(return_value={
            "id": 100, "iid": 1, "title": "MR 1", "state": "opened",
        })
        client.list_pipelines = AsyncMock(return_value=[
            {"id": 500, "status": "success", "ref": "main"},
        ])
        client.get_pipeline = AsyncMock(return_value={
            "id": 500, "status": "success", "ref": "main",
        })
        client.list_branches = AsyncMock(return_value=[
            {"name": "main", "default": True},
            {"name": "develop", "default": False},
        ])
        return client

    @pytest.fixture
    def registry(self):
        """Create a resource registry."""
        return ResourceRegistry()


class TestReadStaticResources:
    """Test reading static resources."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock GitLab client."""
        client = MagicMock()
        client.get_current_user = AsyncMock(return_value={
            "id": 1, "username": "testuser",
        })
        client.list_projects = AsyncMock(return_value=[
            {"id": 1, "name": "project-1"},
        ])
        client.list_groups = AsyncMock(return_value=[
            {"id": 10, "name": "group-1"},
        ])
        return client

    @pytest.mark.asyncio
    async def test_read_projects_resource(self, mock_client):
        """Read gitlab://projects resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://projects", mock_client)
        assert result is not None
        assert isinstance(result, list)
        mock_client.list_projects.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_user_current_resource(self, mock_client):
        """Read gitlab://user/current resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://user/current", mock_client)
        assert result is not None
        assert "username" in result
        mock_client.get_current_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_groups_resource(self, mock_client):
        """Read gitlab://groups resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://groups", mock_client)
        assert result is not None
        assert isinstance(result, list)
        mock_client.list_groups.assert_called_once()


class TestReadTemplatedResources:
    """Test reading templated resources."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock GitLab client."""
        client = MagicMock()
        client.get_project = AsyncMock(return_value={
            "id": 123, "name": "test-project",
        })
        client.get_file_contents = AsyncMock(return_value={
            "content": "# README",
            "file_name": "README.md",
        })
        client.list_issues = AsyncMock(return_value=[
            {"iid": 1, "title": "Issue 1"},
        ])
        client.get_issue = AsyncMock(return_value={
            "iid": 5, "title": "Issue 5",
        })
        client.list_merge_requests = AsyncMock(return_value=[
            {"iid": 1, "title": "MR 1"},
        ])
        client.get_merge_request = AsyncMock(return_value={
            "iid": 1, "title": "MR 1",
        })
        client.list_pipelines = AsyncMock(return_value=[
            {"id": 500, "status": "success"},
        ])
        client.get_pipeline = AsyncMock(return_value={
            "id": 500, "status": "success",
        })
        client.list_branches = AsyncMock(return_value=[
            {"name": "main"},
        ])
        return client

    @pytest.mark.asyncio
    async def test_read_project_details(self, mock_client):
        """Read gitlab://project/{id} resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123", mock_client)
        assert result is not None
        assert result["id"] == 123
        mock_client.get_project.assert_called_once_with("123")

    @pytest.mark.asyncio
    async def test_read_project_readme(self, mock_client):
        """Read gitlab://project/{id}/readme resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/readme", mock_client)
        assert result is not None
        mock_client.get_file_contents.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_open_issues(self, mock_client):
        """Read gitlab://project/{id}/issues/open resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/issues/open", mock_client)
        assert result is not None
        assert isinstance(result, list)
        mock_client.list_issues.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_issue_by_iid(self, mock_client):
        """Read gitlab://project/{id}/issues/{iid} resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/issues/5", mock_client)
        assert result is not None
        assert result["iid"] == 5
        mock_client.get_issue.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_open_merge_requests(self, mock_client):
        """Read gitlab://project/{id}/mrs/open resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/mrs/open", mock_client)
        assert result is not None
        assert isinstance(result, list)
        mock_client.list_merge_requests.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_merge_request_by_iid(self, mock_client):
        """Read gitlab://project/{id}/mrs/{iid} resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/mrs/1", mock_client)
        assert result is not None
        mock_client.get_merge_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_recent_pipelines(self, mock_client):
        """Read gitlab://project/{id}/pipelines/recent resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/pipelines/recent", mock_client)
        assert result is not None
        assert isinstance(result, list)
        mock_client.list_pipelines.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_pipeline_by_id(self, mock_client):
        """Read gitlab://project/{id}/pipelines/{id} resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/pipelines/500", mock_client)
        assert result is not None
        mock_client.get_pipeline.assert_called_once()

    @pytest.mark.asyncio
    async def test_read_branches(self, mock_client):
        """Read gitlab://project/{id}/branches resource."""
        from gitlab_mcp.resources.handlers import read_resource

        result = await read_resource("gitlab://project/123/branches", mock_client)
        assert result is not None
        assert isinstance(result, list)
        mock_client.list_branches.assert_called_once()


class TestResourceErrorHandling:
    """Test error handling for resource reading."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock GitLab client."""
        return MagicMock()

    @pytest.mark.asyncio
    async def test_invalid_uri_raises_error(self, mock_client):
        """Invalid URI should raise ValueError."""
        from gitlab_mcp.resources.handlers import read_resource

        with pytest.raises(ValueError, match="Invalid resource URI"):
            await read_resource("http://example.com", mock_client)

    @pytest.mark.asyncio
    async def test_unknown_resource_raises_error(self, mock_client):
        """Unknown resource should raise ValueError."""
        from gitlab_mcp.resources.handlers import read_resource

        with pytest.raises(ValueError, match="Unknown resource"):
            await read_resource("gitlab://unknown/path", mock_client)

    @pytest.mark.asyncio
    async def test_empty_uri_raises_error(self, mock_client):
        """Empty URI should raise ValueError."""
        from gitlab_mcp.resources.handlers import read_resource

        with pytest.raises(ValueError, match="Invalid resource URI"):
            await read_resource("", mock_client)

