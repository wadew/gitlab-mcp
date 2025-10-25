"""
Unit tests for merge request tools.

Tests the MCP tools for GitLab merge request operations.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.merge_requests import (
    add_mr_comment,
    approve_merge_request,
    close_merge_request,
    create_merge_request,
    get_merge_request,
    get_merge_request_changes,
    get_merge_request_commits,
    get_merge_request_pipelines,
    list_merge_requests,
    list_mr_comments,
    merge_merge_request,
    reopen_merge_request,
    unapprove_merge_request,
    update_merge_request,
)


class TestListMergeRequests:
    """Test list_merge_requests tool."""

    @pytest.mark.asyncio
    async def test_list_merge_requests_returns_list(self):
        """Test listing merge requests."""
        mock_client = Mock()
        mock_mrs = [{"id": 1, "title": "MR 1"}, {"id": 2, "title": "MR 2"}]
        mock_client.list_merge_requests = Mock(return_value=mock_mrs)

        result = await list_merge_requests(mock_client, "project/path")

        mock_client.list_merge_requests.assert_called_once_with(
            project_id="project/path", state=None, page=1, per_page=20
        )
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_list_merge_requests_with_filters(self):
        """Test listing merge requests with filters."""
        mock_client = Mock()
        mock_client.list_merge_requests = Mock(return_value=[])

        await list_merge_requests(mock_client, 123, state="opened", page=2, per_page=50)

        mock_client.list_merge_requests.assert_called_once_with(
            project_id=123, state="opened", page=2, per_page=50
        )


class TestGetMergeRequest:
    """Test get_merge_request tool."""

    @pytest.mark.asyncio
    async def test_get_merge_request_returns_details(self):
        """Test getting merge request details."""
        mock_client = Mock()
        mock_mr = {"id": 1, "iid": 10, "title": "Test MR"}
        mock_client.get_merge_request = Mock(return_value=mock_mr)

        result = await get_merge_request(mock_client, "project/path", 10)

        mock_client.get_merge_request.assert_called_once_with(project_id="project/path", mr_iid=10)
        assert result["iid"] == 10


class TestCreateMergeRequest:
    """Test create_merge_request tool."""

    @pytest.mark.asyncio
    async def test_create_merge_request_minimal(self):
        """Test creating merge request with minimal parameters."""
        mock_client = Mock()
        mock_mr = {"id": 1, "iid": 10, "title": "New MR"}
        mock_client.create_merge_request = Mock(return_value=mock_mr)

        result = await create_merge_request(mock_client, 123, "feature", "main", "New Feature")

        mock_client.create_merge_request.assert_called_once_with(
            project_id=123,
            source_branch="feature",
            target_branch="main",
            title="New Feature",
            description=None,
            assignee_ids=None,
        )
        assert result["title"] == "New MR"

    @pytest.mark.asyncio
    async def test_create_merge_request_with_description_and_assignees(self):
        """Test creating merge request with description and assignees."""
        mock_client = Mock()
        mock_mr = {"id": 1, "iid": 10}
        mock_client.create_merge_request = Mock(return_value=mock_mr)

        await create_merge_request(
            mock_client,
            "project/path",
            "feature",
            "main",
            "New Feature",
            description="Description",
            assignee_ids=[1, 2],
        )

        mock_client.create_merge_request.assert_called_once_with(
            project_id="project/path",
            source_branch="feature",
            target_branch="main",
            title="New Feature",
            description="Description",
            assignee_ids=[1, 2],
        )


class TestUpdateMergeRequest:
    """Test update_merge_request tool."""

    @pytest.mark.asyncio
    async def test_update_merge_request(self):
        """Test updating merge request."""
        mock_client = Mock()
        mock_mr = {"id": 1, "iid": 10, "title": "Updated"}
        mock_client.update_merge_request = Mock(return_value=mock_mr)

        result = await update_merge_request(mock_client, 123, 10, title="Updated", labels=["bug"])

        mock_client.update_merge_request.assert_called_once_with(
            project_id=123,
            mr_iid=10,
            title="Updated",
            description=None,
            labels=["bug"],
            assignee_ids=None,
        )
        assert result["title"] == "Updated"


class TestMergeMergeRequest:
    """Test merge_merge_request tool."""

    @pytest.mark.asyncio
    async def test_merge_merge_request(self):
        """Test merging a merge request."""
        mock_client = Mock()
        mock_mr = {"id": 1, "iid": 10, "state": "merged"}
        mock_client.merge_merge_request = Mock(return_value=mock_mr)

        result = await merge_merge_request(mock_client, "project/path", 10)

        mock_client.merge_merge_request.assert_called_once_with(
            project_id="project/path", mr_iid=10, merge_commit_message=None
        )
        assert result["state"] == "merged"

    @pytest.mark.asyncio
    async def test_merge_merge_request_with_message(self):
        """Test merging with custom commit message."""
        mock_client = Mock()
        mock_mr = {"id": 1}
        mock_client.merge_merge_request = Mock(return_value=mock_mr)

        await merge_merge_request(mock_client, 123, 10, merge_commit_message="Custom msg")

        mock_client.merge_merge_request.assert_called_once_with(
            project_id=123, mr_iid=10, merge_commit_message="Custom msg"
        )


class TestCloseMergeRequest:
    """Test close_merge_request tool."""

    @pytest.mark.asyncio
    async def test_close_merge_request(self):
        """Test closing a merge request."""
        mock_client = Mock()
        mock_mr = {"id": 1, "iid": 10, "state": "closed"}
        mock_client.close_merge_request = Mock(return_value=mock_mr)

        result = await close_merge_request(mock_client, 123, 10)

        mock_client.close_merge_request.assert_called_once_with(project_id=123, mr_iid=10)
        assert result["state"] == "closed"


class TestReopenMergeRequest:
    """Test reopen_merge_request tool."""

    @pytest.mark.asyncio
    async def test_reopen_merge_request(self):
        """Test reopening a merge request."""
        mock_client = Mock()
        mock_client.reopen_merge_request = Mock(return_value=None)

        await reopen_merge_request(mock_client, "project/path", 10)

        mock_client.reopen_merge_request.assert_called_once_with(
            project_id="project/path", mr_iid=10
        )


class TestApproveMergeRequest:
    """Test approve_merge_request tool."""

    @pytest.mark.asyncio
    async def test_approve_merge_request(self):
        """Test approving a merge request."""
        mock_client = Mock()
        mock_approval = {"approved": True}
        mock_client.approve_merge_request = Mock(return_value=mock_approval)

        result = await approve_merge_request(mock_client, 123, 10)

        mock_client.approve_merge_request.assert_called_once_with(project_id=123, mr_iid=10)
        assert result["approved"] is True


class TestUnapproveMergeRequest:
    """Test unapprove_merge_request tool."""

    @pytest.mark.asyncio
    async def test_unapprove_merge_request(self):
        """Test unapproving a merge request."""
        mock_client = Mock()
        mock_client.unapprove_merge_request = Mock(return_value=None)

        await unapprove_merge_request(mock_client, "project/path", 10)

        mock_client.unapprove_merge_request.assert_called_once_with(
            project_id="project/path", mr_iid=10
        )


class TestGetMergeRequestChanges:
    """Test get_merge_request_changes tool."""

    @pytest.mark.asyncio
    async def test_get_merge_request_changes(self):
        """Test getting merge request changes."""
        mock_client = Mock()
        mock_changes = {"changes": [{"old_path": "file.py", "new_path": "file.py"}]}
        mock_client.get_merge_request_changes = Mock(return_value=mock_changes)

        result = await get_merge_request_changes(mock_client, 123, 10)

        mock_client.get_merge_request_changes.assert_called_once_with(
            project_id=123, merge_request_iid=10
        )
        assert "changes" in result


class TestGetMergeRequestCommits:
    """Test get_merge_request_commits tool."""

    @pytest.mark.asyncio
    async def test_get_merge_request_commits(self):
        """Test getting merge request commits."""
        mock_client = Mock()
        mock_commits = [{"id": "abc123", "message": "Commit 1"}]
        mock_client.get_merge_request_commits = Mock(return_value=mock_commits)

        result = await get_merge_request_commits(mock_client, "project/path", 10)

        mock_client.get_merge_request_commits.assert_called_once_with(
            project_id="project/path", merge_request_iid=10
        )
        assert len(result) == 1


class TestGetMergeRequestPipelines:
    """Test get_merge_request_pipelines tool."""

    @pytest.mark.asyncio
    async def test_get_merge_request_pipelines(self):
        """Test getting merge request pipelines."""
        mock_client = Mock()
        mock_pipelines = [{"id": 1, "status": "success"}]
        mock_client.get_merge_request_pipelines = Mock(return_value=mock_pipelines)

        result = await get_merge_request_pipelines(mock_client, 123, 10)

        mock_client.get_merge_request_pipelines.assert_called_once_with(
            project_id=123, merge_request_iid=10
        )
        assert len(result) == 1


class TestAddMrComment:
    """Test add_mr_comment tool."""

    @pytest.mark.asyncio
    async def test_add_mr_comment_returns_formatted_result(self):
        """Test adding a comment to a merge request returns properly formatted result."""
        mock_note = Mock()
        mock_note.id = 100
        mock_note.body = "This is a test MR comment"
        mock_note.created_at = "2025-01-15T10:00:00Z"
        mock_note.updated_at = "2025-01-15T10:00:00Z"

        mock_author = Mock()
        mock_author.username = "reviewer1"
        mock_author.name = "Reviewer One"
        mock_note.author = mock_author

        mock_client = Mock()
        mock_client.add_mr_comment = Mock(return_value=mock_note)

        result = await add_mr_comment(
            mock_client, project_id=123, mr_iid=42, body="This is a test MR comment"
        )

        mock_client.add_mr_comment.assert_called_once_with(
            project_id=123, mr_iid=42, body="This is a test MR comment"
        )

        assert result["id"] == 100
        assert result["body"] == "This is a test MR comment"
        assert result["author"]["username"] == "reviewer1"
        assert result["author"]["name"] == "Reviewer One"
        assert result["created_at"] == "2025-01-15T10:00:00Z"

    @pytest.mark.asyncio
    async def test_add_mr_comment_handles_missing_author(self):
        """Test add_mr_comment handles missing author gracefully."""
        mock_note = Mock(spec=["id", "body", "created_at", "updated_at"])
        mock_note.id = 100
        mock_note.body = "Comment without author"
        mock_note.created_at = "2025-01-15T10:00:00Z"
        mock_note.updated_at = "2025-01-15T10:00:00Z"

        mock_client = Mock()
        mock_client.add_mr_comment = Mock(return_value=mock_note)

        result = await add_mr_comment(mock_client, project_id=123, mr_iid=42, body="Test")

        assert result["author"] is None


class TestListMrComments:
    """Test list_mr_comments tool."""

    @pytest.mark.asyncio
    async def test_list_mr_comments_returns_formatted_results(self):
        """Test listing MR comments returns properly formatted results."""
        mock_note1 = Mock()
        mock_note1.id = 100
        mock_note1.body = "First MR comment"
        mock_note1.created_at = "2025-01-15T10:00:00Z"
        mock_note1.updated_at = "2025-01-15T10:00:00Z"
        mock_author1 = Mock()
        mock_author1.username = "reviewer1"
        mock_author1.name = "Reviewer One"
        mock_note1.author = mock_author1

        mock_note2 = Mock()
        mock_note2.id = 101
        mock_note2.body = "Second MR comment"
        mock_note2.created_at = "2025-01-15T11:00:00Z"
        mock_note2.updated_at = "2025-01-15T11:00:00Z"
        mock_author2 = Mock()
        mock_author2.username = "reviewer2"
        mock_author2.name = "Reviewer Two"
        mock_note2.author = mock_author2

        mock_client = Mock()
        mock_client.list_mr_comments = Mock(return_value=[mock_note1, mock_note2])

        result = await list_mr_comments(mock_client, project_id=123, mr_iid=42)

        mock_client.list_mr_comments.assert_called_once_with(
            project_id=123, mr_iid=42, page=1, per_page=20
        )

        assert "comments" in result
        assert "pagination" in result
        assert len(result["comments"]) == 2
        assert result["comments"][0]["body"] == "First MR comment"
        assert result["comments"][1]["author"]["username"] == "reviewer2"

    @pytest.mark.asyncio
    async def test_list_mr_comments_with_pagination(self):
        """Test listing MR comments with pagination."""
        mock_client = Mock()
        mock_client.list_mr_comments = Mock(return_value=[])

        await list_mr_comments(mock_client, project_id=123, mr_iid=42, page=2, per_page=50)

        mock_client.list_mr_comments.assert_called_once_with(
            project_id=123, mr_iid=42, page=2, per_page=50
        )

    @pytest.mark.asyncio
    async def test_list_mr_comments_handles_missing_author(self):
        """Test list_mr_comments handles comments with missing author."""
        mock_note = Mock(spec=["id", "body", "created_at", "updated_at"])
        mock_note.id = 100
        mock_note.body = "Comment without author"
        mock_note.created_at = "2025-01-15T10:00:00Z"
        mock_note.updated_at = "2025-01-15T10:00:00Z"

        mock_client = Mock()
        mock_client.list_mr_comments = Mock(return_value=[mock_note])

        result = await list_mr_comments(mock_client, project_id=123, mr_iid=42)

        assert len(result["comments"]) == 1
        assert result["comments"][0]["author"] is None
