"""
Unit tests for issues tools.

Tests the MCP tools for GitLab issues operations including:
- Listing issues
- Getting issue details
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.client.exceptions import AuthenticationError, NotFoundError
from gitlab_mcp.tools.issues import get_issue, list_issues


class TestListIssues:
    """Test list_issues tool."""

    @pytest.mark.asyncio
    async def test_list_issues_returns_formatted_results(self):
        """Test that list_issues returns properly formatted issue list."""
        # Mock GitLab client
        mock_client = Mock()

        # Mock issue objects
        mock_issue1 = Mock()
        mock_issue1.iid = 1
        mock_issue1.title = "First issue"
        mock_issue1.description = "Description 1"
        mock_issue1.state = "opened"
        mock_issue1.labels = ["bug", "critical"]
        mock_issue1.web_url = "https://gitlab.example.com/group/project/issues/1"
        mock_issue1.created_at = "2025-01-01T00:00:00Z"
        mock_issue1.updated_at = "2025-01-02T00:00:00Z"
        mock_issue1.author = Mock(username="user1", name="User One")
        mock_issue1.assignees = [Mock(username="assignee1", name="Assignee One")]

        mock_issue2 = Mock()
        mock_issue2.iid = 2
        mock_issue2.title = "Second issue"
        mock_issue2.description = "Description 2"
        mock_issue2.state = "closed"
        mock_issue2.labels = ["feature"]
        mock_issue2.web_url = "https://gitlab.example.com/group/project/issues/2"
        mock_issue2.created_at = "2025-02-01T00:00:00Z"
        mock_issue2.updated_at = "2025-02-02T00:00:00Z"
        mock_issue2.author = Mock(username="user2", name="User Two")
        mock_issue2.assignees = []

        mock_client.list_issues = Mock(return_value=[mock_issue1, mock_issue2])

        result = await list_issues(mock_client, project_id=123)

        mock_client.list_issues.assert_called_once_with(
            project_id=123,
            state=None,
            labels=None,
            milestone=None,
            page=1,
            per_page=20,
        )

        assert "issues" in result
        assert "pagination" in result
        assert len(result["issues"]) == 2

        # Verify first issue
        issue1 = result["issues"][0]
        assert issue1["iid"] == 1
        assert issue1["title"] == "First issue"
        assert issue1["state"] == "opened"
        assert issue1["labels"] == ["bug", "critical"]
        assert issue1["author"]["username"] == "user1"

    @pytest.mark.asyncio
    async def test_list_issues_with_filters(self):
        """Test listing issues with state, labels, and milestone filters."""
        mock_client = Mock()
        mock_client.list_issues = Mock(return_value=[])

        await list_issues(
            mock_client,
            project_id="group/project",
            state="opened",
            labels=["bug", "critical"],
            milestone="v1.0",
        )

        mock_client.list_issues.assert_called_once_with(
            project_id="group/project",
            state="opened",
            labels=["bug", "critical"],
            milestone="v1.0",
            page=1,
            per_page=20,
        )

    @pytest.mark.asyncio
    async def test_list_issues_with_pagination(self):
        """Test listing issues with pagination parameters."""
        mock_client = Mock()
        mock_client.list_issues = Mock(return_value=[])

        await list_issues(mock_client, project_id=123, page=2, per_page=50)

        mock_client.list_issues.assert_called_once_with(
            project_id=123,
            state=None,
            labels=None,
            milestone=None,
            page=2,
            per_page=50,
        )

    @pytest.mark.asyncio
    async def test_list_issues_empty_results(self):
        """Test that list_issues handles empty results gracefully."""
        mock_client = Mock()
        mock_client.list_issues = Mock(return_value=[])

        result = await list_issues(mock_client, project_id=123)

        assert result["issues"] == []
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["per_page"] == 20
        assert result["pagination"]["total"] == 0

    @pytest.mark.asyncio
    async def test_list_issues_handles_missing_optional_fields(self):
        """Test that list_issues handles issues with missing optional fields."""
        mock_client = Mock()

        mock_issue = Mock(spec=["iid", "title", "state", "web_url", "created_at", "updated_at"])
        mock_issue.iid = 1
        mock_issue.title = "Test issue"
        mock_issue.state = "opened"
        mock_issue.web_url = "https://gitlab.example.com/issues/1"
        mock_issue.created_at = "2025-01-01T00:00:00Z"
        mock_issue.updated_at = "2025-01-02T00:00:00Z"
        # Missing: description, labels, author, assignees, milestone

        mock_client.list_issues = Mock(return_value=[mock_issue])

        result = await list_issues(mock_client, project_id=123)

        issue = result["issues"][0]
        assert issue["iid"] == 1
        assert issue["description"] == ""
        assert issue["labels"] == []
        assert issue["author"] is None
        assert issue["assignees"] == []

    @pytest.mark.asyncio
    async def test_list_issues_propagates_errors(self):
        """Test that list_issues propagates exceptions from client."""
        mock_client = Mock()
        mock_client.list_issues = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError):
            await list_issues(mock_client, project_id=999999)


class TestGetIssue:
    """Test get_issue tool."""

    @pytest.mark.asyncio
    async def test_get_issue_returns_formatted_result(self):
        """Test that get_issue returns properly formatted issue details."""
        mock_client = Mock()

        # Mock issue object
        mock_issue = Mock()
        mock_issue.iid = 42
        mock_issue.title = "Test issue"
        mock_issue.description = "Detailed description"
        mock_issue.state = "opened"
        mock_issue.labels = ["bug", "priority:high"]
        mock_issue.web_url = "https://gitlab.example.com/group/project/issues/42"
        mock_issue.created_at = "2025-01-01T00:00:00Z"
        mock_issue.updated_at = "2025-01-15T00:00:00Z"
        mock_issue.closed_at = None
        mock_issue.author = Mock(username="author1", name="Author One")
        mock_issue.assignees = [
            Mock(username="assignee1", name="Assignee One"),
            Mock(username="assignee2", name="Assignee Two"),
        ]
        mock_issue.milestone = Mock(title="v1.0", web_url="https://gitlab.example.com/milestones/1")

        mock_client.get_issue = Mock(return_value=mock_issue)

        result = await get_issue(mock_client, project_id=123, issue_iid=42)

        mock_client.get_issue.assert_called_once_with(project_id=123, issue_iid=42)

        assert result["iid"] == 42
        assert result["title"] == "Test issue"
        assert result["description"] == "Detailed description"
        assert result["state"] == "opened"
        assert result["labels"] == ["bug", "priority:high"]
        assert result["web_url"] == "https://gitlab.example.com/group/project/issues/42"
        assert result["author"]["username"] == "author1"
        assert len(result["assignees"]) == 2
        assert result["milestone"]["title"] == "v1.0"

    @pytest.mark.asyncio
    async def test_get_issue_by_project_path(self):
        """Test getting issue using project path instead of ID."""
        mock_client = Mock()

        mock_issue = Mock()
        mock_issue.iid = 1
        mock_issue.title = "Test"
        mock_issue.state = "opened"
        mock_issue.web_url = "https://gitlab.example.com/issues/1"
        mock_issue.created_at = "2025-01-01T00:00:00Z"
        mock_issue.updated_at = "2025-01-02T00:00:00Z"

        mock_client.get_issue = Mock(return_value=mock_issue)

        _ = await get_issue(mock_client, project_id="group/project", issue_iid=1)

        mock_client.get_issue.assert_called_once_with(project_id="group/project", issue_iid=1)

    @pytest.mark.asyncio
    async def test_get_issue_handles_missing_optional_fields(self):
        """Test that get_issue handles missing optional fields gracefully."""
        mock_client = Mock()

        mock_issue = Mock(spec=["iid", "title", "state", "web_url", "created_at", "updated_at"])
        mock_issue.iid = 1
        mock_issue.title = "Minimal issue"
        mock_issue.state = "opened"
        mock_issue.web_url = "https://gitlab.example.com/issues/1"
        mock_issue.created_at = "2025-01-01T00:00:00Z"
        mock_issue.updated_at = "2025-01-02T00:00:00Z"
        # Missing: description, labels, author, assignees, milestone, closed_at

        mock_client.get_issue = Mock(return_value=mock_issue)

        result = await get_issue(mock_client, project_id=123, issue_iid=1)

        assert result["description"] == ""
        assert result["labels"] == []
        assert result["author"] is None
        assert result["assignees"] == []
        assert result["milestone"] is None
        assert result["closed_at"] is None

    @pytest.mark.asyncio
    async def test_get_issue_propagates_not_found_error(self):
        """Test that get_issue propagates NotFoundError."""
        mock_client = Mock()
        mock_client.get_issue = Mock(side_effect=NotFoundError("Issue not found"))

        with pytest.raises(NotFoundError):
            await get_issue(mock_client, project_id=123, issue_iid=999999)

    @pytest.mark.asyncio
    async def test_get_issue_propagates_authentication_error(self):
        """Test that get_issue propagates AuthenticationError."""
        mock_client = Mock()
        mock_client.get_issue = Mock(side_effect=AuthenticationError("Not authenticated"))

        with pytest.raises(AuthenticationError):
            await get_issue(mock_client, project_id=123, issue_iid=1)


class TestCreateIssue:
    """Test create_issue tool function."""

    @pytest.mark.asyncio
    async def test_create_issue_returns_formatted_result(self):
        """Test that create_issue returns properly formatted result."""
        # Import the function (will fail initially in RED phase)
        from gitlab_mcp.tools.issues import create_issue

        # Mock created issue
        mock_issue = Mock()
        mock_issue.iid = 42
        mock_issue.id = 1001
        mock_issue.title = "Test Issue"
        mock_issue.description = "Test description"
        mock_issue.state = "opened"
        mock_issue.created_at = "2025-01-15T10:00:00Z"
        mock_issue.updated_at = "2025-01-15T10:00:00Z"
        mock_issue.closed_at = None
        mock_issue.web_url = "https://gitlab.example.com/project/issues/42"

        # Mock author
        mock_author = Mock()
        mock_author.id = 10
        mock_author.username = "testuser"
        mock_author.name = "Test User"
        mock_issue.author = mock_author

        mock_issue.labels = ["bug", "frontend"]
        mock_issue.assignees = []
        mock_issue.milestone = None

        # Mock client
        mock_client = Mock()
        mock_client.create_issue = Mock(return_value=mock_issue)

        # Call create_issue
        result = await create_issue(
            mock_client,
            project_id=123,
            title="Test Issue",
            description="Test description",
            labels=["bug", "frontend"],
        )

        # Verify client method called
        mock_client.create_issue.assert_called_once_with(
            project_id=123,
            title="Test Issue",
            description="Test description",
            labels=["bug", "frontend"],
            assignee_ids=None,
            milestone_id=None,
        )

        # Verify formatted result
        assert result["iid"] == 42
        assert result["title"] == "Test Issue"
        assert result["description"] == "Test description"
        assert result["state"] == "opened"
        assert result["labels"] == ["bug", "frontend"]

    @pytest.mark.asyncio
    async def test_create_issue_with_all_fields(self):
        """Test create_issue with all optional fields."""
        from gitlab_mcp.tools.issues import create_issue

        mock_issue = Mock()
        mock_issue.iid = 1
        mock_issue.id = 100
        mock_issue.title = "Full Issue"
        mock_issue.description = "Full description"
        mock_issue.state = "opened"
        mock_issue.labels = ["bug", "critical"]
        mock_issue.web_url = "https://example.com/issue/1"
        mock_issue.created_at = "2025-01-15T10:00:00Z"
        mock_issue.updated_at = "2025-01-15T10:00:00Z"
        mock_issue.closed_at = None

        mock_author = Mock()
        mock_author.username = "user1"
        mock_issue.author = mock_author

        mock_assignee1 = Mock()
        mock_assignee1.username = "user2"
        mock_assignee1.name = "User Two"
        mock_assignee2 = Mock()
        mock_assignee2.username = "user3"
        mock_assignee2.name = "User Three"
        mock_issue.assignees = [mock_assignee1, mock_assignee2]

        mock_milestone = Mock()
        mock_milestone.title = "v1.0"
        mock_milestone.web_url = "https://example.com/milestone/1"
        mock_issue.milestone = mock_milestone

        mock_client = Mock()
        mock_client.create_issue = Mock(return_value=mock_issue)

        result = await create_issue(
            mock_client,
            project_id=123,
            title="Full Issue",
            description="Full description",
            labels=["bug", "critical"],
            assignee_ids=[10, 20],
            milestone_id=5,
        )

        # Verify all parameters passed
        mock_client.create_issue.assert_called_once_with(
            project_id=123,
            title="Full Issue",
            description="Full description",
            labels=["bug", "critical"],
            assignee_ids=[10, 20],
            milestone_id=5,
        )

        # Verify result includes all fields
        assert len(result["assignees"]) == 2
        assert result["assignees"][0]["username"] == "user2"
        assert result["assignees"][1]["username"] == "user3"
        assert result["milestone"]["title"] == "v1.0"

    @pytest.mark.asyncio
    async def test_create_issue_minimal_fields(self):
        """Test create_issue with only required fields."""
        from gitlab_mcp.tools.issues import create_issue

        mock_issue = Mock()
        mock_issue.iid = 1
        mock_issue.id = 100
        mock_issue.title = "Minimal Issue"
        mock_issue.description = ""
        mock_issue.state = "opened"
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.milestone = None
        mock_issue.web_url = "https://example.com/issue/1"
        mock_issue.created_at = "2025-01-15T10:00:00Z"
        mock_issue.updated_at = "2025-01-15T10:00:00Z"
        mock_issue.closed_at = None

        mock_author = Mock()
        mock_author.username = "user1"
        mock_issue.author = mock_author

        mock_client = Mock()
        mock_client.create_issue = Mock(return_value=mock_issue)

        result = await create_issue(mock_client, project_id=123, title="Minimal Issue")

        # Verify only title passed
        mock_client.create_issue.assert_called_once_with(
            project_id=123,
            title="Minimal Issue",
            description=None,
            labels=None,
            assignee_ids=None,
            milestone_id=None,
        )

        assert result["title"] == "Minimal Issue"
        assert result["description"] == ""

    @pytest.mark.asyncio
    async def test_create_issue_handles_missing_fields(self):
        """Test create_issue handles missing optional fields gracefully."""
        from gitlab_mcp.tools.issues import create_issue

        # Mock issue with minimal attributes (using spec to avoid AttributeError)
        mock_issue = Mock(
            spec=[
                "iid",
                "id",
                "title",
                "state",
                "web_url",
                "created_at",
                "updated_at",
            ]
        )
        mock_issue.iid = 1
        mock_issue.id = 100
        mock_issue.title = "Test"
        mock_issue.state = "opened"
        mock_issue.web_url = "https://example.com/issue/1"
        mock_issue.created_at = "2025-01-15T10:00:00Z"
        mock_issue.updated_at = "2025-01-15T10:00:00Z"

        mock_client = Mock()
        mock_client.create_issue = Mock(return_value=mock_issue)

        result = await create_issue(mock_client, project_id=123, title="Test")

        # Verify defaults for missing fields
        assert result["description"] == ""
        assert result["labels"] == []
        assert result["author"] is None
        assert result["assignees"] == []
        assert result["milestone"] is None
        assert result["closed_at"] is None

    @pytest.mark.asyncio
    async def test_create_issue_by_project_path(self):
        """Test create_issue using project path."""
        from gitlab_mcp.tools.issues import create_issue

        mock_issue = Mock()
        mock_issue.iid = 1
        mock_issue.id = 100
        mock_issue.title = "Test"
        mock_issue.state = "opened"
        mock_issue.web_url = "https://example.com/issue/1"
        mock_issue.created_at = "2025-01-15T10:00:00Z"
        mock_issue.updated_at = "2025-01-15T10:00:00Z"
        mock_issue.closed_at = None
        mock_issue.description = ""
        mock_issue.labels = []
        mock_issue.assignees = []
        mock_issue.milestone = None

        mock_author = Mock()
        mock_author.username = "user1"
        mock_issue.author = mock_author

        mock_client = Mock()
        mock_client.create_issue = Mock(return_value=mock_issue)

        await create_issue(mock_client, project_id="group/project", title="Test")

        # Verify path used
        mock_client.create_issue.assert_called_once()
        call_args = mock_client.create_issue.call_args
        assert call_args[1]["project_id"] == "group/project"

    @pytest.mark.asyncio
    async def test_create_issue_propagates_not_found_error(self):
        """Test that create_issue propagates NotFoundError."""
        from gitlab_mcp.tools.issues import create_issue

        mock_client = Mock()
        mock_client.create_issue = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError):
            await create_issue(mock_client, project_id=999999, title="Test")

    @pytest.mark.asyncio
    async def test_create_issue_propagates_authentication_error(self):
        """Test that create_issue propagates AuthenticationError."""
        from gitlab_mcp.tools.issues import create_issue

        mock_client = Mock()
        mock_client.create_issue = Mock(side_effect=AuthenticationError("Not authenticated"))

        with pytest.raises(AuthenticationError):
            await create_issue(mock_client, project_id=123, title="Test")
