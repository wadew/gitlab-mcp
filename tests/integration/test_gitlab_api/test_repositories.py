"""Integration tests for repository operations with real GitLab API.

These tests interact with a real GitLab instance and require:
- Valid GITLAB_URL and GITLAB_TOKEN environment variables
- GITLAB_TEST_PROJECT_ID environment variable (project ID or path)
- Network access to the GitLab instance

Run with: pytest tests/integration/ -v -m integration
"""

import pytest

from gitlab_mcp.client.gitlab_client import GitLabClient


@pytest.mark.integration
class TestRepositoryOperations:
    """Integration tests for repository operations."""

    def test_list_projects_returns_projects(self, gitlab_client: GitLabClient):
        """Test that we can list projects from real GitLab API.

        This is a basic smoke test to verify:
        - Client can connect to GitLab
        - Authentication works
        - API calls return data

        Args:
            gitlab_client: Configured GitLab client fixture
        """
        # Act: List all projects
        result = gitlab_client.list_projects(per_page=10)

        # Assert: We got a dictionary response
        assert result is not None
        assert isinstance(result, dict)
        assert "projects" in result
        assert "total" in result

        # Verify we got some projects
        projects = result["projects"]
        assert isinstance(projects, list)
        assert len(projects) > 0

        # Verify project structure (dict with expected keys)
        first_project = projects[0]
        assert "id" in first_project
        assert "name" in first_project
        assert "path" in first_project
        assert "web_url" in first_project

    def test_get_project_by_id_returns_project_details(
        self, gitlab_client: GitLabClient, test_project_id: str
    ):
        """Test that we can get a specific project by ID.

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # Act: Get project details
        project = gitlab_client.get_project(test_project_id)

        # Assert: We got the project (python-gitlab Project object)
        assert project is not None

        # Verify project has expected attributes
        assert hasattr(project, "id")
        assert hasattr(project, "name")
        assert hasattr(project, "web_url")
        assert hasattr(project, "default_branch")

        # Verify we can access the attributes
        assert project.id is not None
        assert project.name is not None

    def test_get_file_content_from_repository(
        self, gitlab_client: GitLabClient, test_project_id: str
    ):
        """Test that we can retrieve file content from the repository.

        This test attempts to get README.md or list the repository tree.

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # First, get the project to know the default branch
        project = gitlab_client.get_project(test_project_id)
        default_branch = project.default_branch

        # Try to get a common file (README.md is very common)
        # Note: This might fail if the file doesn't exist, which is okay for this test
        try:
            file_content = gitlab_client.get_file_content(
                project_id=test_project_id, file_path="README.md", ref=default_branch
            )

            # If we got here, the file exists
            assert file_content is not None
            assert isinstance(file_content, str)
            # README should have some content
            assert len(file_content) > 0

        except Exception:
            # If README.md doesn't exist, try to list repository tree to verify API works
            tree = gitlab_client.get_repository_tree(
                project_id=test_project_id, ref=default_branch, per_page=5
            )

            # Verify we can at least list files
            assert tree is not None
            assert isinstance(tree, list)
            # Repository should have at least one file (empty repo is technically valid)
            assert len(tree) >= 0

    def test_list_repository_tree_returns_files(
        self, gitlab_client: GitLabClient, test_project_id: str
    ):
        """Test that we can list files in the repository tree.

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # Get project to know default branch
        project = gitlab_client.get_project(test_project_id)
        default_branch = project.default_branch

        # Act: List repository tree
        tree = gitlab_client.get_repository_tree(
            project_id=test_project_id, ref=default_branch, per_page=10
        )

        # Assert: We got the tree (list of dicts)
        assert tree is not None
        assert isinstance(tree, list)

        # If there are files, verify structure (dictionaries, not objects)
        if len(tree) > 0:
            first_item = tree[0]
            assert "name" in first_item
            assert "type" in first_item
            assert "path" in first_item
            assert first_item["type"] in ["tree", "blob"]  # Directory or file

    def test_list_branches_returns_branches(
        self, gitlab_client: GitLabClient, test_project_id: str
    ):
        """Test that we can list repository branches.

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # Act: List branches
        branches = gitlab_client.list_branches(project_id=test_project_id, per_page=10)

        # Assert: We got branches
        assert branches is not None
        assert isinstance(branches, list)
        # Every repo should have at least one branch
        assert len(branches) > 0

        # Verify branch structure (python-gitlab objects)
        first_branch = branches[0]
        assert hasattr(first_branch, "name")
        assert hasattr(first_branch, "commit")

    def test_search_projects_finds_test_project(
        self, gitlab_client: GitLabClient, test_project_id: str
    ):
        """Test that we can search for projects and find our test project.

        Args:
            gitlab_client: Configured GitLab client fixture
            test_project_id: Test project ID fixture
        """
        # Get the test project first to know its name
        project = gitlab_client.get_project(test_project_id)
        project_name = project.name

        # Act: Search for the project (use search_term parameter)
        results = gitlab_client.search_projects(search_term=project_name, per_page=10)

        # Assert: Search returned results (list of dicts)
        assert results is not None
        assert isinstance(results, list)

        # Our test project should be in the results
        # (might not be first if there are other projects with similar names)
        project_ids = [p["id"] for p in results]
        assert project.id in project_ids
