"""
Unit tests for repository tools.

Tests the MCP tools for GitLab repository operations including:
- Getting repository/project details
- Listing branches
- Getting branch details
- File operations
- etc.
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.client.exceptions import (
    AuthenticationError,
    NotFoundError,
    PermissionError,
)
from gitlab_mcp.tools.repositories import (
    compare_branches,
    create_branch,
    create_tag,
    delete_branch,
    get_branch,
    get_commit,
    get_file_contents,
    get_repository,
    get_tag,
    list_branches,
    list_commits,
    list_repository_tree,
    list_tags,
    search_code,
)


class TestGetRepository:
    """Test get_repository tool."""

    @pytest.mark.asyncio
    async def test_get_repository_by_id_returns_details(self):
        """Test getting repository by numeric project ID."""
        # Mock GitLab client
        mock_client = Mock()
        project_dict = {
            "id": 123,
            "name": "Test Project",
            "path": "test-project",
            "path_with_namespace": "group/test-project",
            "description": "A test project",
            "visibility": "private",
            "web_url": "https://gitlab.example.com/group/test-project",
            "default_branch": "main",
            "created_at": "2025-01-01T00:00:00Z",
            "last_activity_at": "2025-10-23T00:00:00Z",
            "star_count": 5,
            "forks_count": 2,
            "open_issues_count": 3,
        }

        mock_client.get_project = Mock(return_value=project_dict)

        result = await get_repository(mock_client, 123)

        mock_client.get_project.assert_called_once_with(123)
        assert result["id"] == 123
        assert result["name"] == "Test Project"
        assert result["path_with_namespace"] == "group/test-project"
        assert result["visibility"] == "private"
        assert result["web_url"] == "https://gitlab.example.com/group/test-project"
        assert result["default_branch"] == "main"
        assert result["star_count"] == 5
        assert result["forks_count"] == 2

    @pytest.mark.asyncio
    async def test_get_repository_by_path_returns_details(self):
        """Test getting repository by path (namespace/project)."""
        mock_client = Mock()
        project_dict = {
            "id": 456,
            "name": "Another Project",
            "path_with_namespace": "mygroup/myproject",
            "description": "Another test project",
            "visibility": "public",
            "web_url": "https://gitlab.example.com/mygroup/myproject",
            "default_branch": "master",
            "created_at": "2024-01-01T00:00:00Z",
            "last_activity_at": "2025-10-22T00:00:00Z",
            "star_count": 10,
            "forks_count": 5,
            "open_issues_count": 7,
        }

        mock_client.get_project = Mock(return_value=project_dict)

        result = await get_repository(mock_client, "mygroup/myproject")

        mock_client.get_project.assert_called_once_with("mygroup/myproject")
        assert result["id"] == 456
        assert result["path_with_namespace"] == "mygroup/myproject"
        assert result["visibility"] == "public"

    @pytest.mark.asyncio
    async def test_get_repository_includes_all_metadata(self):
        """Test that get_repository returns all expected metadata fields."""
        mock_client = Mock()
        mock_project = Mock()
        mock_project.id = 789
        mock_project.name = "Full Project"
        mock_project.path = "full-project"
        mock_project.path_with_namespace = "org/full-project"
        mock_project.description = "Complete metadata"
        mock_project.visibility = "internal"
        mock_project.web_url = "https://gitlab.example.com/org/full-project"
        mock_project.default_branch = "develop"
        mock_project.created_at = "2023-06-15T10:30:00Z"
        mock_project.last_activity_at = "2025-10-23T08:15:00Z"
        mock_project.star_count = 42
        mock_project.forks_count = 15
        mock_project.open_issues_count = 12

        mock_client.get_project = Mock(return_value=mock_project)

        result = await get_repository(mock_client, 789)

        # Verify all expected fields are present
        expected_fields = [
            "id",
            "name",
            "path",
            "path_with_namespace",
            "description",
            "visibility",
            "web_url",
            "default_branch",
            "created_at",
            "last_activity_at",
            "star_count",
            "forks_count",
            "open_issues_count",
        ]

        for field in expected_fields:
            assert field in result, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_get_repository_not_found(self):
        """Test that getting non-existent repository raises NotFoundError."""
        mock_client = Mock()
        mock_client.get_project = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError) as exc_info:
            await get_repository(mock_client, 999)

        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_get_repository_permission_denied(self):
        """Test that permission denied raises PermissionError."""
        mock_client = Mock()
        mock_client.get_project = Mock(side_effect=PermissionError("Permission denied (403)"))

        with pytest.raises(PermissionError) as exc_info:
            await get_repository(mock_client, 123)

        assert (
            "permission" in str(exc_info.value).lower()
            or "forbidden" in str(exc_info.value).lower()
        )

    @pytest.mark.asyncio
    async def test_get_repository_auth_error(self):
        """Test that authentication error raises AuthenticationError."""
        mock_client = Mock()
        mock_client.get_project = Mock(side_effect=AuthenticationError("Authentication failed"))

        with pytest.raises(AuthenticationError):
            await get_repository(mock_client, 123)

    @pytest.mark.asyncio
    async def test_get_repository_handles_missing_optional_fields(self):
        """Test that get_repository handles missing optional fields gracefully."""
        mock_client = Mock()
        # Minimal required fields in dictionary format
        project_dict = {
            "id": 100,
            "name": "Minimal Project",
            "path_with_namespace": "min/project",
            "description": None,
            "visibility": "private",
            "web_url": "https://gitlab.example.com/min/project",
            "default_branch": "main",
            "created_at": "2025-01-01T00:00:00Z",
            "last_activity_at": "2025-01-01T00:00:00Z",
            # Missing optional fields - dict.get() will return None
        }

        mock_client.get_project = Mock(return_value=project_dict)

        result = await get_repository(mock_client, 100)

        # Should not raise errors even with missing fields
        assert result["id"] == 100
        assert result["name"] == "Minimal Project"
        # Missing fields should have sensible defaults
        assert "star_count" in result
        assert "forks_count" in result
        assert "open_issues_count" in result


class TestListBranches:
    """Test list_branches tool."""

    @pytest.mark.asyncio
    async def test_list_branches_returns_formatted_branches(self):
        """Test listing branches returns properly formatted data."""
        mock_client = Mock()

        # Mock branch objects
        mock_branch1 = Mock()
        mock_branch1.name = "main"
        mock_branch1.commit = {"id": "abc123"}
        mock_branch1.protected = True
        mock_branch1.default = True
        mock_branch1.merged = False

        mock_branch2 = Mock()
        mock_branch2.name = "feature/test"
        mock_branch2.commit = {"id": "def456"}
        mock_branch2.protected = False
        mock_branch2.default = False
        mock_branch2.merged = False

        mock_client.list_branches = Mock(return_value=[mock_branch1, mock_branch2])

        result = await list_branches(mock_client, 123)

        mock_client.list_branches.assert_called_once_with(123, None, 1, 20)
        assert "branches" in result
        assert "total" in result
        assert "page" in result
        assert "per_page" in result
        assert len(result["branches"]) == 2
        assert result["branches"][0]["name"] == "main"
        assert result["branches"][0]["protected"] is True
        assert result["branches"][0]["default"] is True
        assert result["branches"][1]["name"] == "feature/test"
        assert result["total"] == 2

    @pytest.mark.asyncio
    async def test_list_branches_includes_metadata(self):
        """Test that list_branches includes all expected branch metadata."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "develop"
        mock_branch.commit = {"id": "xyz789"}
        mock_branch.protected = True
        mock_branch.default = False
        mock_branch.merged = True

        mock_client.list_branches = Mock(return_value=[mock_branch])

        result = await list_branches(mock_client, 456)

        branch = result["branches"][0]
        assert "name" in branch
        assert "commit_sha" in branch
        assert "protected" in branch
        assert "default" in branch
        assert "merged" in branch
        assert branch["name"] == "develop"
        assert branch["commit_sha"] == "xyz789"
        assert branch["protected"] is True
        assert branch["default"] is False
        assert branch["merged"] is True

    @pytest.mark.asyncio
    async def test_list_branches_with_search(self):
        """Test listing branches with search filter."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "feature/awesome"
        mock_branch.commit = {"id": "abc123"}
        mock_branch.protected = False
        mock_branch.default = False
        mock_branch.merged = False

        mock_client.list_branches = Mock(return_value=[mock_branch])

        result = await list_branches(mock_client, 123, search="feature")

        mock_client.list_branches.assert_called_once_with(123, "feature", 1, 20)
        assert len(result["branches"]) == 1
        assert "feature" in result["branches"][0]["name"]

    @pytest.mark.asyncio
    async def test_list_branches_pagination(self):
        """Test listing branches with pagination parameters."""
        mock_client = Mock()
        mock_client.list_branches = Mock(return_value=[])

        result = await list_branches(mock_client, 123, page=2, per_page=10)

        mock_client.list_branches.assert_called_once_with(123, None, 2, 10)
        assert result["page"] == 2
        assert result["per_page"] == 10
        assert result["total"] == 0

    @pytest.mark.asyncio
    async def test_list_branches_handles_errors(self):
        """Test that list_branches propagates errors from client."""
        mock_client = Mock()
        mock_client.list_branches = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError) as exc_info:
            await list_branches(mock_client, 999)

        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_list_branches_empty_repository(self):
        """Test listing branches for repository with no branches."""
        mock_client = Mock()
        mock_client.list_branches = Mock(return_value=[])

        result = await list_branches(mock_client, 123)

        assert result["branches"] == []
        assert result["total"] == 0
        assert result["page"] == 1
        assert result["per_page"] == 20

    @pytest.mark.asyncio
    async def test_list_branches_handles_missing_merged_field(self):
        """Test that list_branches handles branches without merged field."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "main"
        mock_branch.commit = {"id": "abc123"}
        mock_branch.protected = True
        mock_branch.default = True
        # merged field might not exist on some branches
        delattr(mock_branch, "merged")

        mock_client.list_branches = Mock(return_value=[mock_branch])

        result = await list_branches(mock_client, 123)

        # Should handle missing merged field gracefully
        assert "merged" in result["branches"][0]
        assert result["branches"][0]["merged"] is False  # Default value


class TestGetBranch:
    """Test get_branch tool."""

    @pytest.mark.asyncio
    async def test_get_branch_returns_branch_details(self):
        """Test getting specific branch returns detailed information."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "main"
        mock_branch.commit = {
            "id": "abc123def456",
            "short_id": "abc123",
            "title": "Initial commit",
            "author_name": "Test Author",
            "author_email": "author@example.com",
            "created_at": "2025-01-01T00:00:00Z",
            "message": "Initial commit\n\nSetup project",
        }
        mock_branch.protected = True
        mock_branch.default = True
        mock_branch.merged = False
        mock_branch.can_push = True
        mock_branch.developers_can_push = False
        mock_branch.developers_can_merge = False
        mock_branch.web_url = "https://gitlab.example.com/mygroup/myproject/-/tree/main"

        mock_client.get_branch = Mock(return_value=mock_branch)

        result = await get_branch(mock_client, 123, "main")

        mock_client.get_branch.assert_called_once_with(123, "main")
        assert result["name"] == "main"
        assert result["protected"] is True
        assert result["default"] is True
        assert result["commit"]["sha"] == "abc123def456"
        assert result["commit"]["title"] == "Initial commit"
        assert result["commit"]["author_name"] == "Test Author"

    @pytest.mark.asyncio
    async def test_get_branch_includes_all_fields(self):
        """Test that get_branch includes all expected fields."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "develop"
        mock_branch.commit = {
            "id": "xyz789",
            "short_id": "xyz789",
            "title": "Latest commit",
            "author_name": "Dev Author",
            "author_email": "dev@example.com",
            "created_at": "2025-10-23T10:00:00Z",
        }
        mock_branch.protected = False
        mock_branch.default = False
        mock_branch.merged = True
        mock_branch.can_push = False
        mock_branch.developers_can_push = True
        mock_branch.developers_can_merge = True
        mock_branch.web_url = "https://gitlab.example.com/org/project/-/tree/develop"

        mock_client.get_branch = Mock(return_value=mock_branch)

        result = await get_branch(mock_client, 456, "develop")

        # Verify all expected fields
        assert "name" in result
        assert "commit" in result
        assert "protected" in result
        assert "default" in result
        assert "merged" in result
        assert "can_push" in result
        assert "developers_can_push" in result
        assert "developers_can_merge" in result
        assert "web_url" in result

        # Verify commit details
        assert "sha" in result["commit"]
        assert "short_sha" in result["commit"]
        assert "title" in result["commit"]
        assert "author_name" in result["commit"]
        assert "author_email" in result["commit"]
        assert "created_at" in result["commit"]

    @pytest.mark.asyncio
    async def test_get_branch_by_project_path(self):
        """Test getting branch using project path."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "feature/test"
        mock_branch.commit = {"id": "abc123"}
        mock_branch.protected = False
        mock_branch.default = False

        mock_client.get_branch = Mock(return_value=mock_branch)

        result = await get_branch(mock_client, "mygroup/myproject", "feature/test")

        mock_client.get_branch.assert_called_once_with("mygroup/myproject", "feature/test")
        assert result["name"] == "feature/test"

    @pytest.mark.asyncio
    async def test_get_branch_not_found(self):
        """Test that getting non-existent branch raises NotFoundError."""
        mock_client = Mock()
        mock_client.get_branch = Mock(side_effect=NotFoundError("Branch not found"))

        with pytest.raises(NotFoundError) as exc_info:
            await get_branch(mock_client, 123, "nonexistent")

        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_get_branch_handles_missing_optional_fields(self):
        """Test that get_branch handles branches with missing optional fields."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "minimal"
        mock_branch.commit = {
            "id": "abc123",
            "short_id": "abc123",
            "title": "Minimal commit",
        }
        mock_branch.protected = False
        mock_branch.default = False
        # Missing optional fields
        delattr(mock_branch, "merged")
        delattr(mock_branch, "can_push")
        delattr(mock_branch, "developers_can_push")
        delattr(mock_branch, "developers_can_merge")
        delattr(mock_branch, "web_url")

        mock_client.get_branch = Mock(return_value=mock_branch)

        result = await get_branch(mock_client, 123, "minimal")

        # Should handle missing fields gracefully with defaults
        assert result["name"] == "minimal"
        assert "merged" in result
        assert "can_push" in result
        assert "developers_can_push" in result
        assert "developers_can_merge" in result
        assert "web_url" in result

    @pytest.mark.asyncio
    async def test_get_branch_handles_minimal_commit_info(self):
        """Test that get_branch handles commits with minimal information."""
        mock_client = Mock()

        mock_branch = Mock()
        mock_branch.name = "test"
        mock_branch.commit = {
            "id": "abc123",
        }
        mock_branch.protected = False
        mock_branch.default = False

        mock_client.get_branch = Mock(return_value=mock_branch)

        result = await get_branch(mock_client, 123, "test")

        # Should handle missing commit fields gracefully
        assert result["commit"]["sha"] == "abc123"
        assert "short_sha" in result["commit"]
        assert "title" in result["commit"]
        assert "author_name" in result["commit"]
        assert "author_email" in result["commit"]
        assert "created_at" in result["commit"]


class TestGetFileContents:
    """Test get_file_contents tool."""

    @pytest.mark.asyncio
    async def test_get_file_contents_returns_decoded_content(self):
        """Test getting file contents returns decoded base64 content."""
        mock_client = Mock()

        # Mock file object with base64 encoded content
        mock_file = Mock()
        mock_file.file_path = "README.md"
        mock_file.file_name = "README.md"
        mock_file.size = 23
        mock_file.content = (
            "IyBSRUFETUUKClRoaXMgaXMgYSB0ZXN0"  # base64: "# README\n\nThis is a test"
        )
        mock_file.encoding = "base64"
        mock_file.ref = "main"
        mock_file.blob_id = "blob123"
        mock_file.last_commit_id = "commit123"

        mock_client.get_file_content = Mock(return_value=mock_file)

        result = await get_file_contents(mock_client, 123, "README.md")

        mock_client.get_file_content.assert_called_once_with(123, "README.md", ref=None)
        assert result["file_path"] == "README.md"
        assert result["file_name"] == "README.md"
        assert result["size"] == 23
        assert result["content"] == "# README\n\nThis is a test"  # Decoded
        assert result["encoding"] == "base64"
        assert result["ref"] == "main"

    @pytest.mark.asyncio
    async def test_get_file_contents_from_specific_ref(self):
        """Test getting file contents from specific branch/tag/commit."""
        mock_client = Mock()

        mock_file = Mock()
        mock_file.file_path = "src/main.py"
        mock_file.file_name = "main.py"
        mock_file.size = 100
        mock_file.content = "cHJpbnQoImhlbGxvIik="  # base64: print("hello")
        mock_file.encoding = "base64"
        mock_file.ref = "develop"

        mock_client.get_file_content = Mock(return_value=mock_file)

        result = await get_file_contents(mock_client, 456, "src/main.py", ref="develop")

        mock_client.get_file_content.assert_called_once_with(456, "src/main.py", ref="develop")
        assert result["file_path"] == "src/main.py"
        assert result["ref"] == "develop"
        assert result["content"] == 'print("hello")'

    @pytest.mark.asyncio
    async def test_get_file_contents_includes_all_metadata(self):
        """Test that get_file_contents includes all expected metadata."""
        mock_client = Mock()

        mock_file = Mock()
        mock_file.file_path = "config.json"
        mock_file.file_name = "config.json"
        mock_file.size = 50
        mock_file.content = "eyJrZXkiOiAidmFsdWUifQ=="  # base64: {"key": "value"}
        mock_file.encoding = "base64"
        mock_file.content_sha256 = "abc123sha"
        mock_file.ref = "main"
        mock_file.blob_id = "blob789"
        mock_file.commit_id = "commit456"
        mock_file.last_commit_id = "commit456"

        mock_client.get_file_content = Mock(return_value=mock_file)

        result = await get_file_contents(mock_client, 789, "config.json")

        # Verify all expected fields
        assert "file_path" in result
        assert "file_name" in result
        assert "size" in result
        assert "content" in result
        assert "encoding" in result
        assert "content_sha256" in result
        assert "ref" in result
        assert "blob_id" in result
        assert "last_commit_id" in result

    @pytest.mark.asyncio
    async def test_get_file_contents_handles_errors(self):
        """Test that get_file_contents propagates errors from client."""
        mock_client = Mock()
        mock_client.get_file_content = Mock(side_effect=NotFoundError("File not found"))

        with pytest.raises(NotFoundError) as exc_info:
            await get_file_contents(mock_client, 999, "nonexistent.txt")

        assert "not found" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_get_file_contents_handles_binary_files(self):
        """Test getting binary file contents."""
        mock_client = Mock()

        mock_file = Mock()
        mock_file.file_path = "image.png"
        mock_file.file_name = "image.png"
        mock_file.size = 1024
        mock_file.content = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="  # Tiny PNG
        mock_file.encoding = "base64"
        mock_file.ref = "main"

        mock_client.get_file_content = Mock(return_value=mock_file)

        result = await get_file_contents(mock_client, 123, "image.png")

        assert result["file_name"] == "image.png"
        assert result["encoding"] == "base64"
        # Content should be decoded but might not be printable text
        assert "content" in result

    @pytest.mark.asyncio
    async def test_get_file_contents_with_nested_path(self):
        """Test getting file from nested directory path."""
        mock_client = Mock()

        mock_file = Mock()
        mock_file.file_path = "src/components/Header.tsx"
        mock_file.file_name = "Header.tsx"
        mock_file.size = 200
        mock_file.content = (
            "ZXhwb3J0IGNvbnN0IEhlYWRlciA9ICgpID0+IHt9"  # base64: export const Header = () => {}
        )
        mock_file.encoding = "base64"
        mock_file.ref = "main"

        mock_client.get_file_content = Mock(return_value=mock_file)

        result = await get_file_contents(mock_client, 123, "src/components/Header.tsx")

        mock_client.get_file_content.assert_called_once_with(
            123, "src/components/Header.tsx", ref=None
        )
        assert result["file_path"] == "src/components/Header.tsx"
        assert result["content"] == "export const Header = () => {}"


class TestListRepositoryTree:
    """Test list_repository_tree tool."""

    @pytest.mark.asyncio
    async def test_list_repository_tree_root(self):
        """Test listing root directory of repository."""
        mock_client = Mock()
        mock_tree = [
            {
                "id": "1",
                "name": "README.md",
                "type": "blob",
                "path": "README.md",
                "mode": "100644",
            },
            {
                "id": "2",
                "name": "src",
                "type": "tree",
                "path": "src",
                "mode": "040000",
            },
            {
                "id": "3",
                "name": "tests",
                "type": "tree",
                "path": "tests",
                "mode": "040000",
            },
        ]
        mock_client.get_repository_tree = Mock(return_value=mock_tree)

        result = await list_repository_tree(mock_client, 123)

        mock_client.get_repository_tree.assert_called_once_with(
            123, path="", ref=None, recursive=False, page=1, per_page=20
        )
        assert result["path"] == ""
        assert result["ref"] == "default"
        assert result["recursive"] is False
        assert result["total"] == 3
        assert len(result["entries"]) == 3
        assert result["entries"][0]["name"] == "README.md"
        assert result["entries"][0]["type"] == "blob"
        assert result["entries"][1]["name"] == "src"
        assert result["entries"][1]["type"] == "tree"

    @pytest.mark.asyncio
    async def test_list_repository_tree_subdirectory(self):
        """Test listing specific subdirectory."""
        mock_client = Mock()
        mock_tree = [
            {
                "id": "4",
                "name": "main.py",
                "type": "blob",
                "path": "src/main.py",
                "mode": "100644",
            },
            {
                "id": "5",
                "name": "utils.py",
                "type": "blob",
                "path": "src/utils.py",
                "mode": "100644",
            },
        ]
        mock_client.get_repository_tree = Mock(return_value=mock_tree)

        result = await list_repository_tree(mock_client, 123, path="src")

        mock_client.get_repository_tree.assert_called_once_with(
            123, path="src", ref=None, recursive=False, page=1, per_page=20
        )
        assert result["path"] == "src"
        assert result["total"] == 2
        assert result["entries"][0]["path"] == "src/main.py"

    @pytest.mark.asyncio
    async def test_list_repository_tree_recursive(self):
        """Test recursive directory listing."""
        mock_client = Mock()
        mock_tree = [
            {"id": "1", "name": "README.md", "type": "blob", "path": "README.md"},
            {"id": "2", "name": "main.py", "type": "blob", "path": "src/main.py"},
            {"id": "3", "name": "test.py", "type": "blob", "path": "tests/test.py"},
        ]
        mock_client.get_repository_tree = Mock(return_value=mock_tree)

        result = await list_repository_tree(mock_client, 123, recursive=True)

        mock_client.get_repository_tree.assert_called_once_with(
            123, path="", ref=None, recursive=True, page=1, per_page=20
        )
        assert result["recursive"] is True
        assert result["total"] == 3

    @pytest.mark.asyncio
    async def test_list_repository_tree_specific_ref(self):
        """Test listing tree at specific ref (branch/tag)."""
        mock_client = Mock()
        mock_tree = [{"id": "1", "name": "feature.py", "type": "blob", "path": "feature.py"}]
        mock_client.get_repository_tree = Mock(return_value=mock_tree)

        result = await list_repository_tree(mock_client, 123, ref="develop")

        mock_client.get_repository_tree.assert_called_once_with(
            123, path="", ref="develop", recursive=False, page=1, per_page=20
        )
        assert result["ref"] == "develop"

    @pytest.mark.asyncio
    async def test_list_repository_tree_distinguishes_files_dirs(self):
        """Test that tool correctly distinguishes between files and directories."""
        mock_client = Mock()
        mock_tree = [
            {"id": "1", "name": "file.txt", "type": "blob", "path": "file.txt"},
            {"id": "2", "name": "folder", "type": "tree", "path": "folder"},
        ]
        mock_client.get_repository_tree = Mock(return_value=mock_tree)

        result = await list_repository_tree(mock_client, 123)

        assert result["entries"][0]["type"] == "blob"
        assert result["entries"][1]["type"] == "tree"

    @pytest.mark.asyncio
    async def test_list_repository_tree_includes_metadata(self):
        """Test that tool includes all file metadata."""
        mock_client = Mock()
        mock_tree = [
            {
                "id": "abc123",
                "name": "README.md",
                "type": "blob",
                "path": "README.md",
                "mode": "100644",
            }
        ]
        mock_client.get_repository_tree = Mock(return_value=mock_tree)

        result = await list_repository_tree(mock_client, 123)

        entry = result["entries"][0]
        assert entry["id"] == "abc123"
        assert entry["name"] == "README.md"
        assert entry["type"] == "blob"
        assert entry["path"] == "README.md"
        assert entry["mode"] == "100644"

    @pytest.mark.asyncio
    async def test_list_repository_tree_handles_errors(self):
        """Test that tool properly propagates errors."""
        from gitlab_mcp.client.exceptions import NotFoundError

        mock_client = Mock()
        mock_client.get_repository_tree = Mock(side_effect=NotFoundError("Path not found"))

        with pytest.raises(NotFoundError):
            await list_repository_tree(mock_client, 123, path="nonexistent")

    @pytest.mark.asyncio
    async def test_list_repository_tree_with_pagination(self):
        """Test repository tree listing with pagination."""
        mock_client = Mock()
        mock_tree = [{"id": str(i), "name": f"file{i}.py"} for i in range(50)]
        mock_client.get_repository_tree = Mock(return_value=mock_tree)

        result = await list_repository_tree(mock_client, 123, page=2, per_page=50)

        mock_client.get_repository_tree.assert_called_once_with(
            123, path="", ref=None, recursive=False, page=2, per_page=50
        )
        assert result["page"] == 2
        assert result["per_page"] == 50
        assert result["total"] == 50

    @pytest.mark.asyncio
    async def test_list_repository_tree_empty_directory(self):
        """Test listing empty directory."""
        mock_client = Mock()
        mock_client.get_repository_tree = Mock(return_value=[])

        result = await list_repository_tree(mock_client, 123, path="empty")

        assert result["total"] == 0
        assert result["entries"] == []


class TestGetCommit:
    """Test get_commit tool."""

    @pytest.mark.asyncio
    async def test_get_commit_returns_details(self):
        """Test getting commit by SHA returns full details."""
        mock_client = Mock()
        mock_commit = Mock()
        mock_commit.id = "abc123def456789"
        mock_commit.short_id = "abc123d"
        mock_commit.title = "Add authentication feature"
        mock_commit.message = "Add authentication feature\n\nImplemented JWT-based auth"
        mock_commit.author_name = "Jane Doe"
        mock_commit.author_email = "jane@example.com"
        mock_commit.authored_date = "2025-10-23T10:30:00Z"
        mock_commit.committer_name = "Jane Doe"
        mock_commit.committer_email = "jane@example.com"
        mock_commit.committed_date = "2025-10-23T10:30:00Z"
        mock_commit.parent_ids = ["parent123", "parent456"]
        mock_commit.web_url = "https://gitlab.example.com/project/commit/abc123"

        mock_client.get_commit = Mock(return_value=mock_commit)

        result = await get_commit(mock_client, 123, "abc123def456789")

        mock_client.get_commit.assert_called_once_with(123, "abc123def456789")
        assert result["sha"] == "abc123def456789"
        assert result["short_sha"] == "abc123d"
        assert result["title"] == "Add authentication feature"
        assert result["message"] == "Add authentication feature\n\nImplemented JWT-based auth"
        assert result["author_name"] == "Jane Doe"
        assert result["author_email"] == "jane@example.com"
        assert result["authored_date"] == "2025-10-23T10:30:00Z"
        assert result["committer_name"] == "Jane Doe"
        assert result["parent_ids"] == ["parent123", "parent456"]
        assert result["web_url"] == "https://gitlab.example.com/project/commit/abc123"

    @pytest.mark.asyncio
    async def test_get_commit_by_short_sha(self):
        """Test getting commit by short SHA."""
        mock_client = Mock()
        mock_commit = Mock()
        mock_commit.id = "abc123"
        mock_commit.short_id = "abc123"

        mock_client.get_commit = Mock(return_value=mock_commit)

        result = await get_commit(mock_client, 123, "abc123")

        mock_client.get_commit.assert_called_once_with(123, "abc123")
        assert result["sha"] == "abc123"

    @pytest.mark.asyncio
    async def test_get_commit_not_found(self):
        """Test getting commit that doesn't exist raises NotFoundError."""
        mock_client = Mock()
        mock_client.get_commit = Mock(side_effect=NotFoundError("Commit not found"))

        with pytest.raises(NotFoundError):
            await get_commit(mock_client, 123, "invalidsha")

    @pytest.mark.asyncio
    async def test_get_commit_handles_merge_commit(self):
        """Test getting merge commit with multiple parents."""
        mock_client = Mock()
        mock_commit = Mock()
        mock_commit.id = "merge123"
        mock_commit.title = "Merge branch 'feature' into 'main'"
        mock_commit.parent_ids = ["parent1", "parent2", "parent3"]

        mock_client.get_commit = Mock(return_value=mock_commit)

        result = await get_commit(mock_client, 123, "merge123")

        assert len(result["parent_ids"]) == 3
        assert result["title"] == "Merge branch 'feature' into 'main'"


class TestListCommits:
    """Test list_commits tool function."""

    @pytest.mark.asyncio
    async def test_list_commits_returns_formatted_commits(self):
        """Test listing commits returns properly formatted commit data."""
        mock_client = Mock()

        mock_commit1 = Mock()
        mock_commit1.id = "abc123def456"
        mock_commit1.short_id = "abc123d"
        mock_commit1.title = "First commit"
        mock_commit1.message = "First commit\n\nDetailed description"
        mock_commit1.author_name = "John Doe"
        mock_commit1.author_email = "john@example.com"
        mock_commit1.authored_date = "2025-10-23T10:00:00Z"
        mock_commit1.committer_name = "John Doe"
        mock_commit1.committer_email = "john@example.com"
        mock_commit1.committed_date = "2025-10-23T10:00:00Z"
        mock_commit1.parent_ids = ["parent123"]
        mock_commit1.web_url = "https://gitlab.example.com/project/commit/abc123"

        mock_commit2 = Mock()
        mock_commit2.id = "def456ghi789"
        mock_commit2.short_id = "def456g"
        mock_commit2.title = "Second commit"
        mock_commit2.message = "Second commit"
        mock_commit2.author_name = "Jane Smith"
        mock_commit2.author_email = "jane@example.com"
        mock_commit2.authored_date = "2025-10-23T11:00:00Z"
        mock_commit2.committer_name = "Jane Smith"
        mock_commit2.committer_email = "jane@example.com"
        mock_commit2.committed_date = "2025-10-23T11:00:00Z"
        mock_commit2.parent_ids = ["abc123def456"]
        mock_commit2.web_url = "https://gitlab.example.com/project/commit/def456"

        mock_client.list_commits = Mock(return_value=[mock_commit1, mock_commit2])

        result = await list_commits(mock_client, 123)

        mock_client.list_commits.assert_called_once_with(
            123, ref=None, since=None, until=None, path=None, page=1, per_page=20
        )
        assert result["ref"] == "default"
        assert len(result["commits"]) == 2
        assert result["total"] == 2
        assert result["page"] == 1
        assert result["per_page"] == 20

        # Check first commit
        commit1 = result["commits"][0]
        assert commit1["sha"] == "abc123def456"
        assert commit1["short_sha"] == "abc123d"
        assert commit1["title"] == "First commit"
        assert commit1["message"] == "First commit\n\nDetailed description"
        assert commit1["author_name"] == "John Doe"
        assert commit1["author_email"] == "john@example.com"

    @pytest.mark.asyncio
    async def test_list_commits_includes_metadata(self):
        """Test that commit list includes all required metadata."""
        mock_client = Mock()

        mock_commit = Mock()
        mock_commit.id = "abc123"
        mock_commit.short_id = "abc123"
        mock_commit.title = "Test commit"
        mock_commit.message = "Test commit message"
        mock_commit.author_name = "Author"
        mock_commit.author_email = "author@example.com"
        mock_commit.authored_date = "2025-10-23T10:00:00Z"
        mock_commit.committer_name = "Committer"
        mock_commit.committer_email = "committer@example.com"
        mock_commit.committed_date = "2025-10-23T11:00:00Z"
        mock_commit.parent_ids = ["parent1"]
        mock_commit.web_url = "https://gitlab.example.com/commit/abc123"

        mock_client.list_commits = Mock(return_value=[mock_commit])

        result = await list_commits(mock_client, 123)

        commit = result["commits"][0]
        assert "sha" in commit
        assert "short_sha" in commit
        assert "title" in commit
        assert "message" in commit
        assert "author_name" in commit
        assert "author_email" in commit
        assert "authored_date" in commit
        assert "committer_name" in commit
        assert "committer_email" in commit
        assert "committed_date" in commit
        assert "parent_ids" in commit
        assert "web_url" in commit

    @pytest.mark.asyncio
    async def test_list_commits_from_specific_branch(self):
        """Test listing commits from a specific branch."""
        mock_client = Mock()
        mock_client.list_commits = Mock(return_value=[])

        result = await list_commits(mock_client, 123, ref="feature-branch")

        mock_client.list_commits.assert_called_once_with(
            123,
            ref="feature-branch",
            since=None,
            until=None,
            path=None,
            page=1,
            per_page=20,
        )
        assert result["ref"] == "feature-branch"

    @pytest.mark.asyncio
    async def test_list_commits_with_date_filter(self):
        """Test listing commits with date filtering."""
        mock_client = Mock()
        mock_client.list_commits = Mock(return_value=[])

        await list_commits(
            mock_client,
            123,
            since="2025-01-01T00:00:00Z",
            until="2025-12-31T23:59:59Z",
        )

        mock_client.list_commits.assert_called_once_with(
            123,
            ref=None,
            since="2025-01-01T00:00:00Z",
            until="2025-12-31T23:59:59Z",
            path=None,
            page=1,
            per_page=20,
        )

    @pytest.mark.asyncio
    async def test_list_commits_with_path_filter(self):
        """Test listing commits affecting a specific path."""
        mock_client = Mock()
        mock_client.list_commits = Mock(return_value=[])

        await list_commits(mock_client, 123, path="src/main.py")

        mock_client.list_commits.assert_called_once_with(
            123, ref=None, since=None, until=None, path="src/main.py", page=1, per_page=20
        )

    @pytest.mark.asyncio
    async def test_list_commits_with_pagination(self):
        """Test listing commits with custom pagination."""
        mock_client = Mock()
        mock_client.list_commits = Mock(return_value=[])

        result = await list_commits(mock_client, 123, page=3, per_page=50)

        mock_client.list_commits.assert_called_once_with(
            123, ref=None, since=None, until=None, path=None, page=3, per_page=50
        )
        assert result["page"] == 3
        assert result["per_page"] == 50

    @pytest.mark.asyncio
    async def test_list_commits_handles_errors(self):
        """Test that list_commits propagates errors from client."""
        mock_client = Mock()
        mock_client.list_commits = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError):
            await list_commits(mock_client, 999999)

    @pytest.mark.asyncio
    async def test_list_commits_empty_list(self):
        """Test listing commits returns empty list when no commits found."""
        mock_client = Mock()
        mock_client.list_commits = Mock(return_value=[])

        result = await list_commits(mock_client, 123)

        assert result["commits"] == []
        assert result["total"] == 0


class TestCompareBranches:
    """Test compare_branches() tool."""

    @pytest.mark.asyncio
    async def test_compare_branches_returns_formatted_comparison(self):
        """Test comparing branches returns formatted comparison data."""
        mock_commit1 = Mock()
        mock_commit1.id = "abc123def456"
        mock_commit1.short_id = "abc123d"
        mock_commit1.title = "feat: add new feature"
        mock_commit1.message = "feat: add new feature\n\nDetailed description"
        mock_commit1.author_name = "John Doe"
        mock_commit1.created_at = "2024-01-15T10:30:00Z"

        mock_commit2 = Mock()
        mock_commit2.id = "def789ghi012"
        mock_commit2.short_id = "def789g"
        mock_commit2.title = "fix: resolve bug"
        mock_commit2.message = "fix: resolve bug"
        mock_commit2.author_name = "Jane Smith"
        mock_commit2.created_at = "2024-01-14T15:20:00Z"

        mock_diff = {
            "old_path": "src/main.py",
            "new_path": "src/main.py",
            "a_mode": "100644",
            "b_mode": "100644",
            "new_file": False,
            "renamed_file": False,
            "deleted_file": False,
            "diff": "@@ -1,3 +1,4 @@\n import sys\n+import os\n",
        }

        mock_comparison = Mock()
        mock_comparison.commits = [mock_commit1, mock_commit2]
        mock_comparison.diffs = [mock_diff]

        mock_client = Mock()
        mock_client.compare_branches = Mock(return_value=mock_comparison)

        result = await compare_branches(mock_client, 123, "main", "develop")

        mock_client.compare_branches.assert_called_once_with(123, "main", "develop", straight=False)
        assert result["from_ref"] == "main"
        assert result["to_ref"] == "develop"
        assert result["compare_same_ref"] is False
        assert len(result["commits"]) == 2
        assert len(result["diffs"]) == 1

    @pytest.mark.asyncio
    async def test_compare_branches_includes_commits(self):
        """Test comparison includes commit details."""
        mock_commit = Mock()
        mock_commit.id = "abc123def456"
        mock_commit.short_id = "abc123d"
        mock_commit.title = "feat: new feature"
        mock_commit.message = "feat: new feature\n\nImplements XYZ"
        mock_commit.author_name = "Developer"
        mock_commit.created_at = "2024-01-15T10:30:00Z"

        mock_comparison = Mock()
        mock_comparison.commits = [mock_commit]
        mock_comparison.diffs = []

        mock_client = Mock()
        mock_client.compare_branches = Mock(return_value=mock_comparison)

        result = await compare_branches(mock_client, 123, "main", "feature")

        assert len(result["commits"]) == 1
        commit = result["commits"][0]
        assert commit["sha"] == "abc123def456"
        assert commit["short_sha"] == "abc123d"
        assert commit["title"] == "feat: new feature"
        assert commit["message"] == "feat: new feature\n\nImplements XYZ"
        assert commit["author_name"] == "Developer"
        assert commit["created_at"] == "2024-01-15T10:30:00Z"

    @pytest.mark.asyncio
    async def test_compare_branches_includes_diffs(self):
        """Test comparison includes diff information."""
        mock_diff1 = {
            "old_path": "file.py",
            "new_path": "file.py",
            "a_mode": "100644",
            "b_mode": "100644",
            "new_file": False,
            "renamed_file": False,
            "deleted_file": False,
            "diff": "@@ -1,3 +1,4 @@\n line1\n+line2\n",
        }

        mock_diff2 = {
            "old_path": None,
            "new_path": "new_file.py",
            "a_mode": None,
            "b_mode": "100644",
            "new_file": True,
            "renamed_file": False,
            "deleted_file": False,
            "diff": "@@ -0,0 +1,10 @@\n+new content\n",
        }

        mock_comparison = Mock()
        mock_comparison.commits = []
        mock_comparison.diffs = [mock_diff1, mock_diff2]

        mock_client = Mock()
        mock_client.compare_branches = Mock(return_value=mock_comparison)

        result = await compare_branches(mock_client, 123, "main", "develop")

        assert len(result["diffs"]) == 2

        diff1 = result["diffs"][0]
        assert diff1["old_path"] == "file.py"
        assert diff1["new_path"] == "file.py"
        assert diff1["new_file"] is False
        assert diff1["renamed_file"] is False
        assert diff1["deleted_file"] is False

        diff2 = result["diffs"][1]
        assert diff2["old_path"] is None
        assert diff2["new_path"] == "new_file.py"
        assert diff2["new_file"] is True

    @pytest.mark.asyncio
    async def test_compare_branches_with_straight_param(self):
        """Test comparison with straight=True parameter."""
        mock_comparison = Mock()
        mock_comparison.commits = []
        mock_comparison.diffs = []

        mock_client = Mock()
        mock_client.compare_branches = Mock(return_value=mock_comparison)

        result = await compare_branches(mock_client, 123, "feature", "main", straight=True)

        mock_client.compare_branches.assert_called_once_with(123, "feature", "main", straight=True)
        assert result["from_ref"] == "feature"
        assert result["to_ref"] == "main"

    @pytest.mark.asyncio
    async def test_compare_branches_handles_no_diff(self):
        """Test comparing same refs returns empty comparison."""
        mock_comparison = Mock()
        mock_comparison.commits = []
        mock_comparison.diffs = []

        mock_client = Mock()
        mock_client.compare_branches = Mock(return_value=mock_comparison)

        result = await compare_branches(mock_client, 123, "main", "main")

        assert result["from_ref"] == "main"
        assert result["to_ref"] == "main"
        assert result["compare_same_ref"] is True
        assert result["commits"] == []
        assert result["diffs"] == []

    @pytest.mark.asyncio
    async def test_compare_branches_handles_errors(self):
        """Test that compare_branches propagates errors from client."""
        mock_client = Mock()
        mock_client.compare_branches = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError):
            await compare_branches(mock_client, 999999, "main", "develop")

    @pytest.mark.asyncio
    async def test_compare_branches_with_project_path(self):
        """Test comparing branches using project path."""
        mock_comparison = Mock()
        mock_comparison.commits = []
        mock_comparison.diffs = []

        mock_client = Mock()
        mock_client.compare_branches = Mock(return_value=mock_comparison)

        result = await compare_branches(mock_client, "group/project", "main", "develop")

        mock_client.compare_branches.assert_called_once_with(
            "group/project", "main", "develop", straight=False
        )
        assert result["from_ref"] == "main"
        assert result["to_ref"] == "develop"


class TestCreateBranch:
    """Test create_branch tool."""

    @pytest.mark.asyncio
    async def test_create_branch_returns_branch_details(self):
        """Test creating a branch returns formatted branch details."""
        mock_branch = Mock()
        mock_branch.name = "feature-123"
        mock_branch.commit = {
            "id": "abc123def456",
            "short_id": "abc123d",
            "title": "Initial commit",
            "message": "Initial commit\n\nDetails here",
            "author_name": "John Doe",
            "created_at": "2024-01-01T00:00:00Z",
        }
        mock_branch.protected = False
        mock_branch.developers_can_push = True
        mock_branch.developers_can_merge = True
        mock_branch.can_push = True
        mock_branch.default = False
        mock_branch.merged = False
        mock_branch.web_url = "https://gitlab.example.com/owner/repo/-/tree/feature-123"

        mock_client = Mock()
        mock_client.create_branch = Mock(return_value=mock_branch)

        result = await create_branch(mock_client, 123, "feature-123", "main")

        mock_client.create_branch.assert_called_once_with(123, "feature-123", "main")
        assert result["name"] == "feature-123"
        # Commit ID comes from file object attribute, not in mock dict
        assert result["commit"]["short_id"] == "abc123d"
        assert result["commit"]["title"] == "Initial commit"
        assert result["protected"] is False
        assert result["developers_can_push"] is True
        assert result["can_push"] is True
        assert result["web_url"] == "https://gitlab.example.com/owner/repo/-/tree/feature-123"

    @pytest.mark.asyncio
    async def test_create_branch_includes_metadata(self):
        """Test create_branch includes all branch metadata."""
        mock_branch = Mock()
        mock_branch.name = "hotfix-456"
        mock_branch.commit = {
            "id": "xyz789",
            "short_id": "xyz789a",
            "title": "Hotfix",
            "message": "Hotfix message",
            "author_name": "Jane Doe",
            "created_at": "2024-01-02T00:00:00Z",
        }
        mock_branch.protected = True
        mock_branch.developers_can_push = False
        mock_branch.developers_can_merge = False
        mock_branch.can_push = False
        mock_branch.default = False
        mock_branch.merged = False
        mock_branch.web_url = "https://gitlab.example.com/owner/repo/-/tree/hotfix-456"

        mock_client = Mock()
        mock_client.create_branch = Mock(return_value=mock_branch)

        result = await create_branch(mock_client, 123, "hotfix-456", "v1.0.0")

        assert result["name"] == "hotfix-456"
        assert result["protected"] is True
        assert result["developers_can_push"] is False
        assert result["developers_can_merge"] is False
        assert result["can_push"] is False
        assert result["default"] is False
        assert result["merged"] is False

    @pytest.mark.asyncio
    async def test_create_branch_from_commit_sha(self):
        """Test creating a branch from a commit SHA."""
        mock_branch = Mock()
        mock_branch.name = "branch-from-commit"
        mock_branch.commit = {"id": "abc123", "title": "Commit title"}
        mock_branch.protected = False
        mock_branch.developers_can_push = True
        mock_branch.developers_can_merge = True
        mock_branch.can_push = True
        mock_branch.default = False
        mock_branch.merged = False
        mock_branch.web_url = "https://gitlab.example.com/owner/repo/-/tree/branch-from-commit"

        mock_client = Mock()
        mock_client.create_branch = Mock(return_value=mock_branch)

        result = await create_branch(mock_client, 123, "branch-from-commit", "abc123def456")

        mock_client.create_branch.assert_called_once_with(123, "branch-from-commit", "abc123def456")
        assert result["name"] == "branch-from-commit"
        assert result["commit"]["id"] == "abc123"

    @pytest.mark.asyncio
    async def test_create_branch_handles_errors(self):
        """Test that create_branch propagates errors from client."""
        mock_client = Mock()
        mock_client.create_branch = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError):
            await create_branch(mock_client, 999999, "new-branch", "main")

    @pytest.mark.asyncio
    async def test_create_branch_with_project_path(self):
        """Test creating a branch using project path instead of ID."""
        mock_branch = Mock()
        mock_branch.name = "feature-path"
        mock_branch.commit = {"id": "abc123", "title": "Test"}
        mock_branch.protected = False
        mock_branch.developers_can_push = True
        mock_branch.developers_can_merge = True
        mock_branch.can_push = True
        mock_branch.default = False
        mock_branch.merged = False
        mock_branch.web_url = "https://gitlab.example.com/owner/repo/-/tree/feature-path"

        mock_client = Mock()
        mock_client.create_branch = Mock(return_value=mock_branch)

        result = await create_branch(mock_client, "owner/repo", "feature-path", "main")

        mock_client.create_branch.assert_called_once_with("owner/repo", "feature-path", "main")
        assert result["name"] == "feature-path"


class TestDeleteBranch:
    """Test delete_branch tool."""

    @pytest.mark.asyncio
    async def test_delete_branch_returns_success(self):
        """Test deleting a branch returns success status."""
        mock_client = Mock()
        mock_client.delete_branch = Mock(return_value=None)

        result = await delete_branch(mock_client, 123, "feature-branch")

        mock_client.delete_branch.assert_called_once_with(123, "feature-branch")
        assert result["deleted"] is True
        assert result["branch_name"] == "feature-branch"

    @pytest.mark.asyncio
    async def test_delete_branch_handles_errors(self):
        """Test that delete_branch propagates errors from client."""
        mock_client = Mock()
        mock_client.delete_branch = Mock(side_effect=NotFoundError("Branch not found"))

        with pytest.raises(NotFoundError):
            await delete_branch(mock_client, 123, "non-existent-branch")

    @pytest.mark.asyncio
    async def test_delete_branch_with_project_path(self):
        """Test deleting a branch using project path instead of ID."""
        mock_client = Mock()
        mock_client.delete_branch = Mock(return_value=None)

        result = await delete_branch(mock_client, "owner/repo", "feature-branch")

        mock_client.delete_branch.assert_called_once_with("owner/repo", "feature-branch")
        assert result["deleted"] is True
        assert result["branch_name"] == "feature-branch"


class TestListTags:
    """Test list_tags tool."""

    @pytest.mark.asyncio
    async def test_list_tags_returns_formatted_tags(self):
        """Test listing tags returns properly formatted tag list."""
        # Mock tag objects
        mock_tag1 = Mock()
        mock_tag1.name = "v1.0.0"
        mock_tag1.message = "Release 1.0.0"
        mock_tag1.target = "abc123"
        mock_tag1.commit = {
            "id": "abc123def456",
            "short_id": "abc123d",
            "title": "Initial release",
            "author_name": "John Doe",
            "created_at": "2024-01-15T10:00:00Z",
        }
        mock_tag1.protected = False

        mock_tag2 = Mock()
        mock_tag2.name = "v1.1.0"
        mock_tag2.message = "Release 1.1.0"
        mock_tag2.target = "def456"
        mock_tag2.commit = {
            "id": "def456ghi789",
            "short_id": "def456g",
            "title": "Bug fixes",
            "author_name": "Jane Smith",
            "created_at": "2024-02-20T14:30:00Z",
        }
        mock_tag2.protected = True

        mock_client = Mock()
        mock_client.list_tags = Mock(return_value=[mock_tag1, mock_tag2])

        result = await list_tags(mock_client, 123)

        mock_client.list_tags.assert_called_once_with(123, None, 1, 20)
        assert len(result["tags"]) == 2
        assert result["tags"][0]["name"] == "v1.0.0"
        assert result["tags"][0]["message"] == "Release 1.0.0"
        assert result["tags"][0]["target"] == "abc123"
        assert result["tags"][0]["commit"]["id"] == "abc123def456"
        assert result["tags"][0]["commit"]["short_id"] == "abc123d"
        assert result["tags"][0]["commit"]["title"] == "Initial release"
        assert result["tags"][0]["commit"]["author_name"] == "John Doe"
        assert result["tags"][0]["protected"] is False
        assert result["tags"][1]["name"] == "v1.1.0"
        assert result["tags"][1]["protected"] is True

    @pytest.mark.asyncio
    async def test_list_tags_includes_metadata(self):
        """Test that list_tags includes pagination metadata."""
        mock_tag = Mock()
        mock_tag.name = "v1.0.0"
        mock_tag.message = ""
        mock_tag.target = "abc123"
        mock_tag.commit = {"id": "abc123", "title": ""}
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.list_tags = Mock(return_value=[mock_tag])

        result = await list_tags(mock_client, 123, page=2, per_page=50)

        assert result["page"] == 2
        assert result["per_page"] == 50
        assert result["total"] == 1

    @pytest.mark.asyncio
    async def test_list_tags_with_search(self):
        """Test listing tags with search filter."""
        mock_tag = Mock()
        mock_tag.name = "v1.0.0"
        mock_tag.message = ""
        mock_tag.target = "abc123"
        mock_tag.commit = {"id": "abc123", "title": ""}
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.list_tags = Mock(return_value=[mock_tag])

        result = await list_tags(mock_client, 123, search="v1.0")

        mock_client.list_tags.assert_called_once_with(123, "v1.0", 1, 20)
        assert len(result["tags"]) == 1
        assert result["tags"][0]["name"] == "v1.0.0"

    @pytest.mark.asyncio
    async def test_list_tags_pagination(self):
        """Test listing tags with pagination parameters."""
        mock_client = Mock()
        mock_client.list_tags = Mock(return_value=[])

        result = await list_tags(mock_client, 123, page=3, per_page=100)

        mock_client.list_tags.assert_called_once_with(123, None, 3, 100)
        assert result["page"] == 3
        assert result["per_page"] == 100

    @pytest.mark.asyncio
    async def test_list_tags_handles_errors(self):
        """Test that list_tags propagates errors from client."""
        mock_client = Mock()
        mock_client.list_tags = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError):
            await list_tags(mock_client, 999999)

    @pytest.mark.asyncio
    async def test_list_tags_empty_list(self):
        """Test listing tags returns empty list when no tags exist."""
        mock_client = Mock()
        mock_client.list_tags = Mock(return_value=[])

        result = await list_tags(mock_client, 123)

        assert result["tags"] == []
        assert result["total"] == 0


class TestGetTag:
    """Test get_tag tool."""

    @pytest.mark.asyncio
    async def test_get_tag_returns_tag_details(self):
        """Test getting a specific tag returns formatted details."""
        mock_tag = Mock()
        mock_tag.name = "v1.0.0"
        mock_tag.message = "Release 1.0.0"
        mock_tag.target = "abc123"
        mock_tag.commit = {
            "id": "abc123def456",
            "short_id": "abc123d",
            "title": "Initial release",
            "message": "Initial release with core features",
            "author_name": "John Doe",
            "created_at": "2024-01-15T10:00:00Z",
        }
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.get_tag = Mock(return_value=mock_tag)

        result = await get_tag(mock_client, 123, "v1.0.0")

        mock_client.get_tag.assert_called_once_with(123, "v1.0.0")
        assert result["name"] == "v1.0.0"
        assert result["message"] == "Release 1.0.0"
        assert result["target"] == "abc123"
        # Commit ID comes from file object attribute, not in mock dict
        assert result["commit"]["short_id"] == "abc123d"
        assert result["commit"]["title"] == "Initial release"
        assert result["commit"]["message"] == "Initial release with core features"
        assert result["commit"]["author_name"] == "John Doe"
        assert result["commit"]["created_at"] == "2024-01-15T10:00:00Z"
        assert result["protected"] is False

    @pytest.mark.asyncio
    async def test_get_tag_includes_all_fields(self):
        """Test that get_tag includes all metadata fields."""
        mock_tag = Mock()
        mock_tag.name = "v2.5.0"
        mock_tag.message = "Major update"
        mock_tag.target = "xyz789"
        mock_tag.commit = {
            "id": "xyz789abc123",
            "short_id": "xyz789a",
            "title": "Major feature update",
            "message": "Major feature update\n\nAdds many new features",
            "author_name": "Jane Smith",
            "created_at": "2024-05-20T10:30:00Z",
        }
        mock_tag.protected = True

        mock_client = Mock()
        mock_client.get_tag = Mock(return_value=mock_tag)

        result = await get_tag(mock_client, "owner/repo", "v2.5.0")

        assert "name" in result
        assert "message" in result
        assert "target" in result
        assert "commit" in result
        assert "protected" in result
        assert result["protected"] is True

    @pytest.mark.asyncio
    async def test_get_tag_by_project_path(self):
        """Test getting a tag using project path instead of ID."""
        mock_tag = Mock()
        mock_tag.name = "v1.0.0"
        mock_tag.message = ""
        mock_tag.target = "abc123"
        mock_tag.commit = {"id": "abc123", "title": ""}
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.get_tag = Mock(return_value=mock_tag)

        result = await get_tag(mock_client, "owner/repo", "v1.0.0")

        mock_client.get_tag.assert_called_once_with("owner/repo", "v1.0.0")
        assert result["name"] == "v1.0.0"

    @pytest.mark.asyncio
    async def test_get_tag_not_found(self):
        """Test that get_tag propagates NotFoundError."""
        mock_client = Mock()
        mock_client.get_tag = Mock(side_effect=NotFoundError("Tag not found"))

        with pytest.raises(NotFoundError):
            await get_tag(mock_client, 123, "non-existent-tag")

    @pytest.mark.asyncio
    async def test_get_tag_handles_missing_optional_fields(self):
        """Test that get_tag gracefully handles missing optional fields."""
        mock_tag = Mock(spec=["name", "target", "commit"])
        mock_tag.name = "v1.0.0"
        mock_tag.target = "abc123"
        mock_tag.commit = {
            "id": "abc123",
            # Optional fields missing
        }

        mock_client = Mock()
        mock_client.get_tag = Mock(return_value=mock_tag)

        result = await get_tag(mock_client, 123, "v1.0.0")

        # Should use defaults for missing fields
        assert result["message"] == ""
        assert result["commit"]["short_id"] == "abc123"[:7]
        assert result["commit"]["title"] == ""
        assert result["commit"]["message"] == ""
        assert result["commit"]["author_name"] == ""
        assert result["commit"]["created_at"] == ""
        assert result["protected"] is False


class TestCreateTag:
    """Test create_tag tool."""

    @pytest.mark.asyncio
    async def test_create_tag_returns_tag_details(self):
        """Test creating a tag returns formatted tag details."""
        mock_tag = Mock()
        mock_tag.name = "v1.0.0"
        mock_tag.message = "Release 1.0.0"
        mock_tag.target = "abc123"
        mock_tag.commit = {
            "id": "abc123def456",
            "short_id": "abc123d",
            "title": "Initial release",
            "message": "Initial release with core features",
            "author_name": "John Doe",
            "created_at": "2024-01-15T10:00:00Z",
        }
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.create_tag = Mock(return_value=mock_tag)

        result = await create_tag(mock_client, 123, "v1.0.0", "main", "Release 1.0.0")

        mock_client.create_tag.assert_called_once_with(123, "v1.0.0", "main", "Release 1.0.0")
        assert result["name"] == "v1.0.0"
        assert result["message"] == "Release 1.0.0"
        assert result["target"] == "abc123"
        # Commit ID comes from file object attribute, not in mock dict
        assert result["commit"]["title"] == "Initial release"
        assert result["protected"] is False

    @pytest.mark.asyncio
    async def test_create_tag_with_message(self):
        """Test creating an annotated tag with message."""
        mock_tag = Mock()
        mock_tag.name = "v2.0.0"
        mock_tag.message = "Major release"
        mock_tag.target = "xyz789"
        mock_tag.commit = {"id": "xyz789", "title": "Major changes"}
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.create_tag = Mock(return_value=mock_tag)

        result = await create_tag(mock_client, 123, "v2.0.0", "develop", "Major release")

        mock_client.create_tag.assert_called_once_with(123, "v2.0.0", "develop", "Major release")
        assert result["name"] == "v2.0.0"
        assert result["message"] == "Major release"

    @pytest.mark.asyncio
    async def test_create_tag_from_commit_sha(self):
        """Test creating a tag from a commit SHA."""
        mock_tag = Mock()
        mock_tag.name = "v1.5.0"
        mock_tag.message = ""
        mock_tag.target = "abc123def456"
        mock_tag.commit = {"id": "abc123def456", "title": "Feature commit"}
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.create_tag = Mock(return_value=mock_tag)

        result = await create_tag(mock_client, 123, "v1.5.0", "abc123def456")

        mock_client.create_tag.assert_called_once_with(123, "v1.5.0", "abc123def456", None)
        assert result["name"] == "v1.5.0"
        assert result["target"] == "abc123def456"

    @pytest.mark.asyncio
    async def test_create_tag_handles_errors(self):
        """Test that create_tag propagates errors from client."""
        mock_client = Mock()
        mock_client.create_tag = Mock(side_effect=NotFoundError("Ref not found"))

        with pytest.raises(NotFoundError):
            await create_tag(mock_client, 123, "v1.0.0", "non-existent-ref")

    @pytest.mark.asyncio
    async def test_create_tag_with_project_path(self):
        """Test creating a tag using project path instead of ID."""
        mock_tag = Mock()
        mock_tag.name = "v1.0.0"
        mock_tag.message = ""
        mock_tag.target = "main"
        mock_tag.commit = {"id": "abc123", "title": ""}
        mock_tag.protected = False

        mock_client = Mock()
        mock_client.create_tag = Mock(return_value=mock_tag)

        result = await create_tag(mock_client, "owner/repo", "v1.0.0", "main")

        mock_client.create_tag.assert_called_once_with("owner/repo", "v1.0.0", "main", None)
        assert result["name"] == "v1.0.0"


class TestSearchCode:
    """Test search_code tool."""

    @pytest.mark.asyncio
    async def test_search_code_returns_formatted_results(self):
        """Test that search_code returns formatted results."""
        mock_results = [
            {
                "basename": "README",
                "data": "def search_code():\n    pass",
                "path": "README.md",
                "filename": "README.md",
                "ref": "main",
                "startline": 10,
                "project_id": 1,
            },
            {
                "basename": "utils",
                "data": "def search_code():\n    return True",
                "path": "src/utils.py",
                "filename": "src/utils.py",
                "ref": "main",
                "startline": 25,
                "project_id": 2,
            },
        ]

        mock_client = Mock()
        mock_client.search_code = Mock(return_value=mock_results)

        result = await search_code(mock_client, "search_code")

        assert "results" in result
        assert len(result["results"]) == 2
        assert result["results"][0]["path"] == "README.md"
        assert result["results"][0]["startline"] == 10
        assert result["results"][1]["path"] == "src/utils.py"
        assert result["search_term"] == "search_code"
        mock_client.search_code.assert_called_once_with("search_code", None, 1, 20)

    @pytest.mark.asyncio
    async def test_search_code_includes_all_metadata(self):
        """Test that search_code includes all expected fields."""
        mock_results = [
            {
                "basename": "test",
                "data": "test content",
                "path": "test.py",
                "filename": "test.py",
                "ref": "develop",
                "startline": 5,
                "project_id": 100,
            }
        ]

        mock_client = Mock()
        mock_client.search_code = Mock(return_value=mock_results)

        result = await search_code(mock_client, "test", page=2, per_page=10)

        assert result["page"] == 2
        assert result["per_page"] == 10
        assert result["total"] == 1
        assert result["search_term"] == "test"
        assert result["results"][0]["basename"] == "test"
        assert result["results"][0]["data"] == "test content"
        assert result["results"][0]["ref"] == "develop"

    @pytest.mark.asyncio
    async def test_search_code_with_project_id(self):
        """Test search_code with project_id parameter."""
        mock_results = [
            {
                "basename": "main",
                "data": "if __name__ == '__main__':",
                "path": "main.py",
                "filename": "main.py",
                "ref": "main",
                "startline": 1,
                "project_id": 123,
            }
        ]

        mock_client = Mock()
        mock_client.search_code = Mock(return_value=mock_results)

        result = await search_code(mock_client, "__main__", project_id=123)

        assert len(result["results"]) == 1
        assert result["results"][0]["project_id"] == 123
        mock_client.search_code.assert_called_once_with("__main__", 123, 1, 20)

    @pytest.mark.asyncio
    async def test_search_code_with_pagination(self):
        """Test search_code with pagination parameters."""
        mock_results = [{"path": f"file{i}.py", "project_id": 1} for i in range(5)]

        mock_client = Mock()
        mock_client.search_code = Mock(return_value=mock_results)

        result = await search_code(mock_client, "test", page=3, per_page=5)

        assert result["page"] == 3
        assert result["per_page"] == 5
        assert result["total"] == 5
        mock_client.search_code.assert_called_once_with("test", None, 3, 5)

    @pytest.mark.asyncio
    async def test_search_code_empty_results(self):
        """Test search_code with no results."""
        mock_client = Mock()
        mock_client.search_code = Mock(return_value=[])

        result = await search_code(mock_client, "nonexistent")

        assert result["results"] == []
        assert result["total"] == 0
        assert result["search_term"] == "nonexistent"

    @pytest.mark.asyncio
    async def test_search_code_handles_errors(self):
        """Test that search_code propagates client errors."""
        mock_client = Mock()
        mock_client.search_code = Mock(side_effect=NotFoundError("Project not found"))

        with pytest.raises(NotFoundError):
            await search_code(mock_client, "test", project_id=999999)


class TestCreateFile:
    """Test create_file tool function."""

    @pytest.mark.asyncio
    async def test_create_file_returns_success(self):
        """Test creating a file returns success with file details."""
        mock_file = {
            "file_path": "README.md",
            "branch": "main",
            "commit": {
                "id": "abc123def456",
                "message": "Add README",
            },
        }

        mock_client = Mock()
        mock_client.create_file = Mock(return_value=mock_file)

        from gitlab_mcp.tools.repositories import create_file

        result = await create_file(
            mock_client,
            project_id=123,
            file_path="README.md",
            branch="main",
            content="# My Project",
            commit_message="Add README",
        )

        mock_client.create_file.assert_called_once_with(
            123,
            "README.md",
            "main",
            "# My Project",
            "Add README",
            author_email=None,
            author_name=None,
            encoding="text",
        )
        assert result["file_path"] == "README.md"
        assert result["branch"] == "main"
        # Commit ID comes from file object attribute, not in mock dict
        assert result["commit"]["message"] == "Add README"

    @pytest.mark.asyncio
    async def test_create_file_with_author_info(self):
        """Test creating a file with author information."""
        mock_file = {
            "file_path": "src/main.py",
            "branch": "develop",
            "commit": {
                "id": "xyz789",
                "message": "Add main module",
            },
        }

        mock_client = Mock()
        mock_client.create_file = Mock(return_value=mock_file)

        from gitlab_mcp.tools.repositories import create_file

        result = await create_file(
            mock_client,
            project_id="owner/repo",
            file_path="src/main.py",
            branch="develop",
            content="def main():\n    pass",
            commit_message="Add main module",
            author_email="jane@example.com",
            author_name="Jane Smith",
        )

        mock_client.create_file.assert_called_once_with(
            "owner/repo",
            "src/main.py",
            "develop",
            "def main():\n    pass",
            "Add main module",
            author_email="jane@example.com",
            author_name="Jane Smith",
            encoding="text",
        )
        assert result["file_path"] == "src/main.py"

    @pytest.mark.asyncio
    async def test_create_file_with_base64_encoding(self):
        """Test creating a binary file with base64 encoding."""
        mock_file = {
            "file_path": "image.png",
            "branch": "main",
            "commit": {"id": "abc123", "message": "Add image"},
        }

        mock_client = Mock()
        mock_client.create_file = Mock(return_value=mock_file)

        from gitlab_mcp.tools.repositories import create_file

        result = await create_file(
            mock_client,
            project_id=123,
            file_path="image.png",
            branch="main",
            content="iVBORw0KGgoAAAANSUhEUgA...",
            commit_message="Add image",
            encoding="base64",
        )

        mock_client.create_file.assert_called_once_with(
            123,
            "image.png",
            "main",
            "iVBORw0KGgoAAAANSUhEUgA...",
            "Add image",
            author_email=None,
            author_name=None,
            encoding="base64",
        )
        assert result["file_path"] == "image.png"

    @pytest.mark.asyncio
    async def test_create_file_handles_errors(self):
        """Test that create_file propagates errors from client."""
        mock_client = Mock()
        mock_client.create_file = Mock(side_effect=NotFoundError("Project not found"))

        from gitlab_mcp.tools.repositories import create_file

        with pytest.raises(NotFoundError):
            await create_file(
                mock_client,
                project_id=999999,
                file_path="test.txt",
                branch="main",
                content="test",
                commit_message="test",
            )


class TestUpdateFile:
    """Test update_file tool function."""

    @pytest.mark.asyncio
    async def test_update_file_returns_success(self):
        """Test updating a file returns success with file details."""
        mock_file = {
            "file_path": "README.md",
            "branch": "main",
            "commit": {
                "id": "ghi789jkl012",
                "message": "Update README",
            },
        }

        mock_client = Mock()
        mock_client.update_file = Mock(return_value=mock_file)

        from gitlab_mcp.tools.repositories import update_file

        result = await update_file(
            mock_client,
            project_id=123,
            file_path="README.md",
            branch="main",
            content="# Updated Project Description",
            commit_message="Update README",
        )

        mock_client.update_file.assert_called_once_with(
            123,
            "README.md",
            "main",
            "# Updated Project Description",
            "Update README",
            author_email=None,
            author_name=None,
            encoding="text",
        )
        assert result["file_path"] == "README.md"
        assert result["branch"] == "main"
        # Commit ID comes from file object attribute, not in mock dict
        assert result["commit"]["message"] == "Update README"

    @pytest.mark.asyncio
    async def test_update_file_with_author_info(self):
        """Test updating a file with author information."""
        mock_file = {
            "file_path": "src/config.py",
            "branch": "develop",
            "commit": {
                "id": "mno345",
                "message": "Update config",
            },
        }

        mock_client = Mock()
        mock_client.update_file = Mock(return_value=mock_file)

        from gitlab_mcp.tools.repositories import update_file

        result = await update_file(
            mock_client,
            project_id="owner/repo",
            file_path="src/config.py",
            branch="develop",
            content="CONFIG = {'debug': True}",
            commit_message="Update config",
            author_email="jane@example.com",
            author_name="Jane Smith",
        )

        mock_client.update_file.assert_called_once_with(
            "owner/repo",
            "src/config.py",
            "develop",
            "CONFIG = {'debug': True}",
            "Update config",
            author_email="jane@example.com",
            author_name="Jane Smith",
            encoding="text",
        )
        assert result["file_path"] == "src/config.py"

    @pytest.mark.asyncio
    async def test_update_file_with_base64_encoding(self):
        """Test updating a binary file with base64 encoding."""
        mock_file = {
            "file_path": "logo.png",
            "branch": "main",
            "commit": {"id": "stu901", "message": "Update logo"},
        }

        mock_client = Mock()
        mock_client.update_file = Mock(return_value=mock_file)

        from gitlab_mcp.tools.repositories import update_file

        result = await update_file(
            mock_client,
            project_id=123,
            file_path="logo.png",
            branch="main",
            content="iVBORw0KGgoAAAANSUhEUgA...",
            commit_message="Update logo",
            encoding="base64",
        )

        mock_client.update_file.assert_called_once_with(
            123,
            "logo.png",
            "main",
            "iVBORw0KGgoAAAANSUhEUgA...",
            "Update logo",
            author_email=None,
            author_name=None,
            encoding="base64",
        )
        assert result["file_path"] == "logo.png"

    @pytest.mark.asyncio
    async def test_update_file_handles_errors(self):
        """Test that update_file propagates errors from client."""
        mock_client = Mock()
        mock_client.update_file = Mock(side_effect=NotFoundError("File not found"))

        from gitlab_mcp.tools.repositories import update_file

        with pytest.raises(NotFoundError):
            await update_file(
                mock_client,
                project_id=123,
                file_path="nonexistent.txt",
                branch="main",
                content="test",
                commit_message="test",
            )


class TestDeleteFile:
    """Test delete_file tool function."""

    @pytest.mark.asyncio
    async def test_delete_file_returns_success(self):
        """Test deleting a file returns success status."""
        mock_client = Mock()
        mock_client.delete_file = Mock(return_value=None)

        from gitlab_mcp.tools.repositories import delete_file

        result = await delete_file(
            mock_client,
            project_id=123,
            file_path="old_file.txt",
            branch="main",
            commit_message="Remove old file",
        )

        mock_client.delete_file.assert_called_once_with(
            123,
            "old_file.txt",
            "main",
            "Remove old file",
            author_email=None,
            author_name=None,
        )
        assert result["file_path"] == "old_file.txt"
        assert result["branch"] == "main"
        assert result["commit"]["message"] == "Remove old file"

    @pytest.mark.asyncio
    async def test_delete_file_with_author_info(self):
        """Test deleting a file with author information."""
        mock_client = Mock()
        mock_client.delete_file = Mock(return_value=None)

        from gitlab_mcp.tools.repositories import delete_file

        result = await delete_file(
            mock_client,
            project_id="owner/repo",
            file_path="deprecated.py",
            branch="cleanup",
            commit_message="Remove deprecated module",
            author_email="jane@example.com",
            author_name="Jane Smith",
        )

        mock_client.delete_file.assert_called_once_with(
            "owner/repo",
            "deprecated.py",
            "cleanup",
            "Remove deprecated module",
            author_email="jane@example.com",
            author_name="Jane Smith",
        )
        assert result["file_path"] == "deprecated.py"

    @pytest.mark.asyncio
    async def test_delete_file_handles_errors(self):
        """Test that delete_file propagates errors from client."""
        mock_client = Mock()
        mock_client.delete_file = Mock(side_effect=NotFoundError("File not found"))

        from gitlab_mcp.tools.repositories import delete_file

        with pytest.raises(NotFoundError):
            await delete_file(
                mock_client,
                project_id=123,
                file_path="nonexistent.txt",
                branch="main",
                commit_message="test",
            )

    @pytest.mark.asyncio
    async def test_delete_file_handles_permission_error(self):
        """Test that delete_file propagates permission errors."""
        mock_client = Mock()
        mock_client.delete_file = Mock(side_effect=PermissionError("Insufficient permissions"))

        from gitlab_mcp.tools.repositories import delete_file

        with pytest.raises(PermissionError):
            await delete_file(
                mock_client,
                project_id=123,
                file_path="protected.txt",
                branch="main",
                commit_message="test",
            )
