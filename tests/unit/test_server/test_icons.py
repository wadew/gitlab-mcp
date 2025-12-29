"""Unit tests for MCP Tool Icons.

Tests verify:
- All tools have an icon assigned
- Icons are appropriate for tool categories
- Icon helper function works correctly
"""

import pytest

from gitlab_mcp.server import TOOL_ICONS, get_tool_icon


class TestToolIconsConstant:
    """Test TOOL_ICONS constant definition."""

    def test_tool_icons_is_dict(self):
        """TOOL_ICONS should be a dictionary."""
        assert isinstance(TOOL_ICONS, dict)

    def test_tool_icons_has_categories(self):
        """TOOL_ICONS should have icon categories defined."""
        assert len(TOOL_ICONS) > 0

    def test_all_icon_values_are_strings(self):
        """All icon values should be strings (emoji)."""
        for _category, icon in TOOL_ICONS.items():
            assert isinstance(icon, str)
            assert len(icon) > 0


class TestToolIconCategories:
    """Test that expected icon categories exist."""

    def test_pipeline_category_exists(self):
        """Pipeline category should have an icon."""
        assert "pipeline" in TOOL_ICONS

    def test_merge_request_category_exists(self):
        """Merge request category should have an icon."""
        assert "merge_request" in TOOL_ICONS or "mr" in TOOL_ICONS

    def test_issue_category_exists(self):
        """Issue category should have an icon."""
        assert "issue" in TOOL_ICONS

    def test_project_category_exists(self):
        """Project category should have an icon."""
        assert "project" in TOOL_ICONS

    def test_repository_category_exists(self):
        """Repository category should have an icon."""
        assert "repository" in TOOL_ICONS or "repo" in TOOL_ICONS

    def test_user_category_exists(self):
        """User category should have an icon."""
        assert "user" in TOOL_ICONS

    def test_group_category_exists(self):
        """Group category should have an icon."""
        assert "group" in TOOL_ICONS

    def test_label_category_exists(self):
        """Label category should have an icon."""
        assert "label" in TOOL_ICONS

    def test_wiki_category_exists(self):
        """Wiki category should have an icon."""
        assert "wiki" in TOOL_ICONS

    def test_snippet_category_exists(self):
        """Snippet category should have an icon."""
        assert "snippet" in TOOL_ICONS

    def test_release_category_exists(self):
        """Release category should have an icon."""
        assert "release" in TOOL_ICONS

    def test_job_category_exists(self):
        """Job category should have an icon."""
        assert "job" in TOOL_ICONS

    def test_branch_category_exists(self):
        """Branch category should have an icon."""
        assert "branch" in TOOL_ICONS

    def test_file_category_exists(self):
        """File category should have an icon."""
        assert "file" in TOOL_ICONS

    def test_commit_category_exists(self):
        """Commit category should have an icon."""
        assert "commit" in TOOL_ICONS

    def test_tag_category_exists(self):
        """Tag category should have an icon."""
        assert "tag" in TOOL_ICONS


class TestGetToolIconFunction:
    """Test the get_tool_icon helper function."""

    def test_get_tool_icon_returns_string_or_none(self):
        """get_tool_icon should return string or None."""
        result = get_tool_icon("list_projects")
        assert result is None or isinstance(result, str)

    def test_get_tool_icon_for_pipeline_tool(self):
        """Pipeline-related tools should get pipeline icon."""
        icon = get_tool_icon("list_pipelines")
        assert icon is not None
        assert icon == TOOL_ICONS.get("pipeline")

    def test_get_tool_icon_for_get_pipeline(self):
        """get_pipeline should get pipeline icon."""
        icon = get_tool_icon("get_pipeline")
        assert icon is not None

    def test_get_tool_icon_for_issue_tool(self):
        """Issue-related tools should get issue icon."""
        icon = get_tool_icon("list_issues")
        assert icon is not None
        assert icon == TOOL_ICONS.get("issue")

    def test_get_tool_icon_for_get_issue(self):
        """get_issue should get issue icon."""
        icon = get_tool_icon("get_issue")
        assert icon is not None

    def test_get_tool_icon_for_create_issue(self):
        """create_issue should get issue icon."""
        icon = get_tool_icon("create_issue")
        assert icon is not None

    def test_get_tool_icon_for_merge_request_tool(self):
        """MR-related tools should get MR icon."""
        icon = get_tool_icon("list_merge_requests")
        assert icon is not None

    def test_get_tool_icon_for_get_merge_request(self):
        """get_merge_request should get MR icon."""
        icon = get_tool_icon("get_merge_request")
        assert icon is not None

    def test_get_tool_icon_for_project_tool(self):
        """Project-related tools should get project icon."""
        icon = get_tool_icon("list_projects")
        assert icon is not None
        assert icon == TOOL_ICONS.get("project")

    def test_get_tool_icon_for_get_project(self):
        """get_project should get project icon."""
        icon = get_tool_icon("get_project")
        assert icon is not None

    def test_get_tool_icon_for_branch_tool(self):
        """Branch-related tools should get branch icon."""
        icon = get_tool_icon("list_branches")
        assert icon is not None
        assert icon == TOOL_ICONS.get("branch")

    def test_get_tool_icon_for_create_branch(self):
        """create_branch should get branch icon."""
        icon = get_tool_icon("create_branch")
        assert icon is not None

    def test_get_tool_icon_for_job_tool(self):
        """Job-related tools should get job icon."""
        icon = get_tool_icon("list_pipeline_jobs")
        assert icon is not None

    def test_get_tool_icon_for_get_job(self):
        """get_job should get job icon."""
        icon = get_tool_icon("get_job")
        assert icon is not None

    def test_get_tool_icon_for_wiki_tool(self):
        """Wiki-related tools should get wiki icon."""
        icon = get_tool_icon("list_wiki_pages")
        assert icon is not None
        assert icon == TOOL_ICONS.get("wiki")

    def test_get_tool_icon_for_snippet_tool(self):
        """Snippet-related tools should get snippet icon."""
        icon = get_tool_icon("list_snippets")
        assert icon is not None
        assert icon == TOOL_ICONS.get("snippet")

    def test_get_tool_icon_for_release_tool(self):
        """Release-related tools should get release icon."""
        icon = get_tool_icon("list_releases")
        assert icon is not None
        assert icon == TOOL_ICONS.get("release")

    def test_get_tool_icon_for_label_tool(self):
        """Label-related tools should get label icon."""
        icon = get_tool_icon("list_labels")
        assert icon is not None
        assert icon == TOOL_ICONS.get("label")

    def test_get_tool_icon_for_user_tool(self):
        """User-related tools should get user icon."""
        icon = get_tool_icon("get_user")
        assert icon is not None
        assert icon == TOOL_ICONS.get("user")

    def test_get_tool_icon_for_group_tool(self):
        """Group-related tools should get group icon."""
        icon = get_tool_icon("list_groups")
        assert icon is not None
        assert icon == TOOL_ICONS.get("group")

    def test_get_tool_icon_for_file_tool(self):
        """File-related tools should get file icon."""
        icon = get_tool_icon("get_file_contents")
        assert icon is not None
        assert icon == TOOL_ICONS.get("file")

    def test_get_tool_icon_for_commit_tool(self):
        """Commit-related tools should get commit icon."""
        icon = get_tool_icon("list_commits")
        assert icon is not None
        assert icon == TOOL_ICONS.get("commit")

    def test_get_tool_icon_for_tag_tool(self):
        """Tag-related tools should get tag icon."""
        icon = get_tool_icon("list_tags")
        assert icon is not None
        assert icon == TOOL_ICONS.get("tag")

    def test_get_tool_icon_for_unknown_tool(self):
        """Unknown tools should return None."""
        icon = get_tool_icon("unknown_tool_xyz")
        assert icon is None

    def test_get_tool_icon_empty_string(self):
        """Empty string should return None."""
        icon = get_tool_icon("")
        assert icon is None


class TestIconCoverage:
    """Test that common tools have icons assigned."""

    @pytest.fixture
    def common_tools(self):
        """List of common tools that should have icons."""
        return [
            "list_projects",
            "get_project",
            "list_issues",
            "get_issue",
            "create_issue",
            "list_merge_requests",
            "get_merge_request",
            "list_pipelines",
            "get_pipeline",
            "list_branches",
            "create_branch",
            "list_pipeline_jobs",
            "get_job",
            "list_wiki_pages",
            "list_snippets",
            "list_releases",
            "list_labels",
            "get_user",
            "list_groups",
            "get_file_contents",
            "list_commits",
            "list_tags",
        ]

    def test_common_tools_have_icons(self, common_tools):
        """All common tools should have icons assigned."""
        missing_icons = []
        for tool in common_tools:
            if get_tool_icon(tool) is None:
                missing_icons.append(tool)

        assert len(missing_icons) == 0, f"Tools missing icons: {missing_icons}"
