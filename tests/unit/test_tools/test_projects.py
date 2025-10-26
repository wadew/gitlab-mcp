"""
Unit tests for project tools.

Tests the MCP tools for GitLab project operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.projects import (
    create_milestone,
    create_project,
    get_milestone,
    get_project,
    get_project_statistics,
    list_milestones,
    list_project_members,
    list_projects,
    search_projects,
    update_milestone,
)


class TestListProjects:
    """Test list_projects tool."""

    @pytest.mark.asyncio
    async def test_list_projects_returns_dict(self):
        """Test listing projects."""
        mock_client = Mock()
        mock_result = {"projects": [{"id": 1}, {"id": 2}], "pagination": {}}
        mock_client.list_projects = Mock(return_value=mock_result)

        result = await list_projects(mock_client)

        mock_client.list_projects.assert_called_once_with(visibility=None, page=1, per_page=20)
        assert "projects" in result

    @pytest.mark.asyncio
    async def test_list_projects_with_filters(self):
        """Test listing projects with filters."""
        mock_client = Mock()
        mock_client.list_projects = Mock(return_value={"projects": []})

        await list_projects(mock_client, visibility="public", page=2, per_page=50)

        mock_client.list_projects.assert_called_once_with(visibility="public", page=2, per_page=50)


class TestGetProject:
    """Test get_project tool."""

    @pytest.mark.asyncio
    async def test_get_project_returns_project(self):
        """Test getting project details."""
        mock_client = Mock()
        mock_project = {"id": 123, "name": "Test Project"}
        mock_client.get_project = Mock(return_value=mock_project)

        result = await get_project(mock_client, 123)

        mock_client.get_project.assert_called_once_with(project_id=123)
        assert result["id"] == 123


class TestSearchProjects:
    """Test search_projects tool."""

    @pytest.mark.asyncio
    async def test_search_projects_returns_list(self):
        """Test searching projects."""
        mock_client = Mock()
        mock_projects = [{"id": 1, "name": "Match"}]
        mock_client.search_projects = Mock(return_value=mock_projects)

        result = await search_projects(mock_client, "test")

        mock_client.search_projects.assert_called_once_with(search_term="test", page=1, per_page=20)
        assert len(result) == 1


class TestListProjectMembers:
    """Test list_project_members tool."""

    @pytest.mark.asyncio
    async def test_list_project_members_returns_list(self):
        """Test listing project members."""
        mock_client = Mock()
        mock_members = [{"id": 1, "username": "user1"}]
        mock_client.list_project_members = Mock(return_value=mock_members)

        result = await list_project_members(mock_client, "project/path")

        mock_client.list_project_members.assert_called_once_with(
            project_id="project/path", page=1, per_page=20
        )
        assert len(result) == 1


class TestGetProjectStatistics:
    """Test get_project_statistics tool."""

    @pytest.mark.asyncio
    async def test_get_project_statistics_returns_dict(self):
        """Test getting project statistics."""
        mock_client = Mock()
        mock_stats = {"commit_count": 100, "storage_size": 5000}
        mock_client.get_project_statistics = Mock(return_value=mock_stats)

        result = await get_project_statistics(mock_client, 123)

        mock_client.get_project_statistics.assert_called_once_with(project_id=123)
        assert "commit_count" in result


class TestListMilestones:
    """Test list_milestones tool."""

    @pytest.mark.asyncio
    async def test_list_milestones_returns_list(self):
        """Test listing milestones."""
        mock_client = Mock()
        mock_milestones = [{"id": 1, "title": "v1.0"}]
        mock_client.list_milestones = Mock(return_value=mock_milestones)

        result = await list_milestones(mock_client, 123)

        mock_client.list_milestones.assert_called_once_with(
            project_id=123, state=None, page=1, per_page=20
        )
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_list_milestones_with_state_filter(self):
        """Test listing milestones with state filter."""
        mock_client = Mock()
        mock_client.list_milestones = Mock(return_value=[])

        await list_milestones(mock_client, "project/path", state="active")

        mock_client.list_milestones.assert_called_once_with(
            project_id="project/path", state="active", page=1, per_page=20
        )


class TestGetMilestone:
    """Test get_milestone tool."""

    @pytest.mark.asyncio
    async def test_get_milestone_returns_dict(self):
        """Test getting milestone details."""
        mock_client = Mock()
        mock_milestone = {"id": 1, "title": "v1.0"}
        mock_client.get_milestone = Mock(return_value=mock_milestone)

        result = await get_milestone(mock_client, 123, 1)

        mock_client.get_milestone.assert_called_once_with(project_id=123, milestone_id=1)
        assert result["id"] == 1


class TestCreateMilestone:
    """Test create_milestone tool."""

    @pytest.mark.asyncio
    async def test_create_milestone_minimal(self):
        """Test creating milestone with minimal parameters."""
        mock_client = Mock()
        mock_milestone = {"id": 1, "title": "v1.0"}
        mock_client.create_milestone = Mock(return_value=mock_milestone)

        result = await create_milestone(mock_client, 123, "v1.0")

        mock_client.create_milestone.assert_called_once_with(
            project_id=123,
            title="v1.0",
            description=None,
            due_date=None,
            start_date=None,
        )
        assert result["title"] == "v1.0"

    @pytest.mark.asyncio
    async def test_create_milestone_with_all_parameters(self):
        """Test creating milestone with all parameters."""
        mock_client = Mock()
        mock_milestone = {"id": 1}
        mock_client.create_milestone = Mock(return_value=mock_milestone)

        await create_milestone(
            mock_client,
            "project/path",
            "v2.0",
            description="Release 2.0",
            due_date="2025-12-31",
            start_date="2025-10-01",
        )

        mock_client.create_milestone.assert_called_once_with(
            project_id="project/path",
            title="v2.0",
            description="Release 2.0",
            due_date="2025-12-31",
            start_date="2025-10-01",
        )


class TestUpdateMilestone:
    """Test update_milestone tool."""

    @pytest.mark.asyncio
    async def test_update_milestone(self):
        """Test updating milestone."""
        mock_client = Mock()
        mock_milestone = {"id": 1, "title": "v1.1"}
        mock_client.update_milestone = Mock(return_value=mock_milestone)

        result = await update_milestone(mock_client, 123, 1, title="v1.1")

        mock_client.update_milestone.assert_called_once_with(
            project_id=123,
            milestone_id=1,
            title="v1.1",
            description=None,
            due_date=None,
            start_date=None,
            state=None,
        )
        assert result["title"] == "v1.1"


class TestCreateProject:
    """Test create_project tool."""

    @pytest.mark.asyncio
    async def test_create_project_minimal_parameters(self):
        """Test creating project with only required parameter (name)."""
        mock_client = Mock()
        mock_project = {"id": 123, "name": "new-project", "path": "new-project"}
        mock_client.create_project = Mock(return_value=mock_project)

        result = await create_project(mock_client, "new-project")

        mock_client.create_project.assert_called_once_with(
            name="new-project",
            path=None,
            namespace_id=None,
            description=None,
            visibility="private",
            initialize_with_readme=False,
        )
        assert result["name"] == "new-project"

    @pytest.mark.asyncio
    async def test_create_project_with_all_parameters(self):
        """Test creating project with all parameters."""
        mock_client = Mock()
        mock_project = {
            "id": 456,
            "name": "My Project",
            "path": "my-project",
            "description": "A test project",
            "visibility": "public",
        }
        mock_client.create_project = Mock(return_value=mock_project)

        result = await create_project(
            mock_client,
            name="My Project",
            path="my-project",
            namespace_id=10,
            description="A test project",
            visibility="public",
            initialize_with_readme=True,
        )

        mock_client.create_project.assert_called_once_with(
            name="My Project",
            path="my-project",
            namespace_id=10,
            description="A test project",
            visibility="public",
            initialize_with_readme=True,
        )
        assert result["name"] == "My Project"
        assert result["visibility"] == "public"

    @pytest.mark.asyncio
    async def test_create_project_custom_visibility(self):
        """Test creating project with custom visibility."""
        mock_client = Mock()
        mock_project = {"id": 789, "name": "internal-proj", "visibility": "internal"}
        mock_client.create_project = Mock(return_value=mock_project)

        result = await create_project(
            mock_client,
            name="internal-proj",
            visibility="internal",
        )

        mock_client.create_project.assert_called_once_with(
            name="internal-proj",
            path=None,
            namespace_id=None,
            description=None,
            visibility="internal",
            initialize_with_readme=False,
        )
        assert result["visibility"] == "internal"
