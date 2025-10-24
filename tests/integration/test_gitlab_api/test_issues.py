"""Integration tests for issue operations with real GitLab API.

These tests interact with a real GitLab instance and require:
- Valid GITLAB_URL and GITLAB_TOKEN environment variables
- GITLAB_TEST_PROJECT_ID environment variable (project ID or path)
- Network access to the GitLab instance
- Permissions to create/update/close issues in the test project

Run with: pytest tests/integration/ -v -m integration

NOTE: These tests will create and modify real issues in the test project.
They clean up after themselves, but be aware of side effects.
"""

import pytest

from gitlab_mcp.client.gitlab_client import GitLabClient


@pytest.mark.integration
class TestIssueOperations:
    """Integration tests for issue CRUD operations."""

    def test_list_issues_returns_issues(self, gitlab_client: GitLabClient, test_project_id: str):
        """Test that we can list issues from a project.

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # Act: List issues
        issues = gitlab_client.list_issues(project_id=test_project_id, per_page=10)

        # Assert: We got a list (might be empty if no issues exist)
        assert issues is not None
        assert isinstance(issues, list)

        # If there are issues, verify structure
        if len(issues) > 0:
            first_issue = issues[0]
            assert hasattr(first_issue, "id")
            assert hasattr(first_issue, "iid")
            assert hasattr(first_issue, "title")
            assert hasattr(first_issue, "state")
            assert hasattr(first_issue, "web_url")

    def test_create_get_update_close_issue_workflow(
        self, gitlab_client: GitLabClient, test_project_id: str
    ):
        """Test complete issue lifecycle: create, get, update, close.

        This is a comprehensive workflow test that verifies:
        - Creating an issue
        - Getting the issue by IID
        - Updating the issue
        - Closing the issue

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # Step 1: Create an issue
        test_title = "[Integration Test] Test Issue - Please ignore"
        test_description = (
            "This is a test issue created by integration tests. It will be closed automatically."
        )

        created_issue = gitlab_client.create_issue(
            project_id=test_project_id, title=test_title, description=test_description
        )

        # Verify created issue
        assert created_issue is not None
        assert hasattr(created_issue, "id")
        assert hasattr(created_issue, "iid")
        assert created_issue.title == test_title
        assert created_issue.description == test_description
        assert created_issue.state == "opened"

        issue_iid = created_issue.iid

        try:
            # Step 2: Get the issue
            fetched_issue = gitlab_client.get_issue(project_id=test_project_id, issue_iid=issue_iid)

            assert fetched_issue is not None
            assert fetched_issue.id == created_issue.id
            assert fetched_issue.iid == issue_iid
            assert fetched_issue.title == test_title

            # Step 3: Update the issue
            updated_title = f"{test_title} [UPDATED]"
            updated_description = f"{test_description}\n\nUpdated during integration test."

            updated_issue = gitlab_client.update_issue(
                project_id=test_project_id,
                issue_iid=issue_iid,
                title=updated_title,
                description=updated_description,
            )

            assert updated_issue is not None
            assert updated_issue.title == updated_title
            assert updated_description in updated_issue.description

            # Step 4: Close the issue
            closed_issue = gitlab_client.close_issue(
                project_id=test_project_id, issue_iid=issue_iid
            )

            assert closed_issue is not None
            assert closed_issue.state == "closed"

        except Exception as e:
            # If anything fails, try to close the issue to clean up
            try:
                gitlab_client.close_issue(project_id=test_project_id, issue_iid=issue_iid)
            except Exception:
                pass  # Ignore cleanup errors
            raise e  # Re-raise original error

    def test_add_comment_to_issue(self, gitlab_client: GitLabClient, test_project_id: str):
        """Test adding a comment to an issue.

        This test creates an issue, adds a comment, then cleans up.

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # Create a test issue
        test_title = "[Integration Test] Issue for Comment Test"
        created_issue = gitlab_client.create_issue(
            project_id=test_project_id,
            title=test_title,
            description="Testing issue comments",
        )

        issue_iid = created_issue.iid

        try:
            # Add a comment
            comment_body = "This is a test comment added by integration tests."
            comment = gitlab_client.add_issue_comment(
                project_id=test_project_id, issue_iid=issue_iid, body=comment_body
            )

            # Verify comment was created
            assert comment is not None
            assert hasattr(comment, "id")
            assert hasattr(comment, "body")
            assert comment.body == comment_body

            # List comments to verify it appears
            comments = gitlab_client.list_issue_comments(
                project_id=test_project_id, issue_iid=issue_iid
            )

            assert comments is not None
            assert isinstance(comments, list)
            assert len(comments) > 0

            # Find our comment in the list
            comment_bodies = [c.body for c in comments]
            assert comment_body in comment_bodies

        finally:
            # Clean up: close the issue
            try:
                gitlab_client.close_issue(project_id=test_project_id, issue_iid=issue_iid)
            except Exception:
                pass  # Ignore cleanup errors
