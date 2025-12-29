"""Unit tests for MCP Tool Annotations.

Tests verify:
- All tools have annotations with destructive and readOnly fields
- Destructive tools (delete_*, cancel_*) are correctly marked
- Read-only tools (list_*, get_*, search_*) are correctly marked
- Mutating tools (create_*, update_*, close_*, reopen_*) have correct annotations
"""

import pytest

from gitlab_mcp.server import TOOL_ANNOTATIONS, _get_tool_definitions, get_tool_annotations


class TestToolAnnotationsMapping:
    """Test the TOOL_ANNOTATIONS constant mapping."""

    def test_tool_annotations_is_dict(self):
        """TOOL_ANNOTATIONS should be a dictionary."""
        assert isinstance(TOOL_ANNOTATIONS, dict)

    def test_all_tools_have_annotations(self):
        """Every tool definition should have corresponding annotations."""
        tool_defs = _get_tool_definitions()
        tool_names = {name for name, _, _ in tool_defs}

        for tool_name in tool_names:
            assert (
                tool_name in TOOL_ANNOTATIONS
            ), f"Tool '{tool_name}' is missing from TOOL_ANNOTATIONS"

    def test_annotations_have_required_fields(self):
        """Each annotation should have destructive and readOnly fields."""
        for tool_name, annotation in TOOL_ANNOTATIONS.items():
            assert (
                "destructive" in annotation
            ), f"Tool '{tool_name}' annotation missing 'destructive' field"
            assert (
                "readOnly" in annotation
            ), f"Tool '{tool_name}' annotation missing 'readOnly' field"
            assert isinstance(
                annotation["destructive"], bool
            ), f"Tool '{tool_name}' destructive field should be bool"
            assert isinstance(
                annotation["readOnly"], bool
            ), f"Tool '{tool_name}' readOnly field should be bool"


class TestDestructiveTools:
    """Test that destructive tools are correctly annotated."""

    @pytest.mark.parametrize(
        "tool_name",
        [
            "delete_file",
            "delete_branch",
            "delete_pipeline",
            "delete_label",
            "delete_wiki_page",
            "delete_snippet",
            "delete_release",
        ],
    )
    def test_delete_tools_are_destructive(self, tool_name):
        """All delete_* tools should be marked as destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is True
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "cancel_pipeline",
            "cancel_job",
        ],
    )
    def test_cancel_tools_are_destructive(self, tool_name):
        """All cancel_* tools should be marked as destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is True
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False


class TestReadOnlyTools:
    """Test that read-only tools are correctly annotated."""

    @pytest.mark.parametrize(
        "tool_name",
        [
            "list_projects",
            "list_repository_tree",
            "list_branches",
            "list_commits",
            "list_tags",
            "list_issues",
            "list_merge_requests",
            "list_pipelines",
            "list_pipeline_jobs",
            "list_milestones",
            "list_labels",
            "list_wiki_pages",
            "list_snippets",
            "list_releases",
            "list_groups",
        ],
    )
    def test_list_tools_are_readonly(self, tool_name):
        """All list_* tools should be marked as readOnly."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is True
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "get_project",
            "get_file_contents",
            "get_branch",
            "get_commit",
            "get_tag",
            "get_issue",
            "get_merge_request",
            "get_pipeline",
            "get_job",
            "get_job_trace",
            "get_milestone",
            "get_wiki_page",
            "get_snippet",
            "get_release",
            "get_user",
            "get_group",
            "get_current_context",
            "get_merge_request_changes",
            "get_merge_request_commits",
            "get_merge_request_pipelines",
        ],
    )
    def test_get_tools_are_readonly(self, tool_name):
        """All get_* tools should be marked as readOnly."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is True
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "search_code",
            "search_users",
            "search_projects",
        ],
    )
    def test_search_tools_are_readonly(self, tool_name):
        """All search_* tools should be marked as readOnly."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is True
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "compare_branches",
            "list_pipeline_variables",
            "list_project_members",
            "get_project_statistics",
            "list_group_members",
            "list_user_projects",
            "list_issue_comments",
            "list_mr_comments",
        ],
    )
    def test_other_readonly_tools(self, tool_name):
        """Other read-only tools should be correctly marked."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is True
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False


class TestMutatingTools:
    """Test that mutating (but not destructive) tools are correctly annotated."""

    @pytest.mark.parametrize(
        "tool_name",
        [
            "create_file",
            "create_branch",
            "create_tag",
            "create_issue",
            "create_merge_request",
            "create_pipeline",
            "create_milestone",
            "create_label",
            "create_wiki_page",
            "create_snippet",
            "create_release",
        ],
    )
    def test_create_tools_are_mutating_not_destructive(self, tool_name):
        """All create_* tools should NOT be readOnly but NOT destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "update_file",
            "update_issue",
            "update_merge_request",
            "update_milestone",
            "update_label",
            "update_wiki_page",
            "update_snippet",
            "update_release",
        ],
    )
    def test_update_tools_are_mutating_not_destructive(self, tool_name):
        """All update_* tools should NOT be readOnly but NOT destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "close_issue",
            "close_merge_request",
        ],
    )
    def test_close_tools_are_mutating_not_destructive(self, tool_name):
        """Close tools should NOT be readOnly but NOT destructive (reversible)."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "reopen_issue",
            "reopen_merge_request",
        ],
    )
    def test_reopen_tools_are_mutating_not_destructive(self, tool_name):
        """Reopen tools should NOT be readOnly but NOT destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "add_issue_comment",
            "add_mr_comment",
        ],
    )
    def test_comment_tools_are_mutating_not_destructive(self, tool_name):
        """Comment tools should NOT be readOnly but NOT destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "approve_merge_request",
            "unapprove_merge_request",
        ],
    )
    def test_approval_tools_are_mutating_not_destructive(self, tool_name):
        """Approval tools should NOT be readOnly but NOT destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "merge_merge_request",
        ],
    )
    def test_merge_tool_is_mutating_not_destructive(self, tool_name):
        """Merge tool should NOT be readOnly but NOT destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False

    @pytest.mark.parametrize(
        "tool_name",
        [
            "retry_pipeline",
            "retry_job",
            "play_job",
            "download_job_artifacts",
        ],
    )
    def test_pipeline_action_tools_are_mutating_not_destructive(self, tool_name):
        """Pipeline action tools should NOT be readOnly but NOT destructive."""
        assert tool_name in TOOL_ANNOTATIONS
        assert TOOL_ANNOTATIONS[tool_name]["readOnly"] is False
        assert TOOL_ANNOTATIONS[tool_name]["destructive"] is False


class TestGetToolAnnotationsFunction:
    """Test the get_tool_annotations helper function."""

    def test_get_tool_annotations_returns_annotations(self):
        """get_tool_annotations should return the annotation for a tool."""
        annotation = get_tool_annotations("list_projects")
        assert annotation == {"destructive": False, "readOnly": True}

    def test_get_tool_annotations_unknown_tool_returns_default(self):
        """Unknown tools should return default non-destructive, non-readonly annotation."""
        annotation = get_tool_annotations("unknown_tool_xyz")
        assert annotation == {"destructive": False, "readOnly": False}

    def test_get_tool_annotations_for_destructive_tool(self):
        """Destructive tools should return correct annotation."""
        annotation = get_tool_annotations("delete_branch")
        assert annotation == {"destructive": True, "readOnly": False}


class TestAnnotationConsistency:
    """Test logical consistency of annotations."""

    def test_no_tool_is_both_destructive_and_readonly(self):
        """No tool should be both destructive and readOnly."""
        for tool_name, annotation in TOOL_ANNOTATIONS.items():
            assert not (
                annotation["destructive"] and annotation["readOnly"]
            ), f"Tool '{tool_name}' cannot be both destructive and readOnly"

    def test_tool_count_matches_definitions(self):
        """TOOL_ANNOTATIONS should have same count as tool definitions."""
        tool_defs = _get_tool_definitions()
        assert len(TOOL_ANNOTATIONS) == len(tool_defs), (
            f"TOOL_ANNOTATIONS has {len(TOOL_ANNOTATIONS)} entries but "
            f"_get_tool_definitions() has {len(tool_defs)} tools"
        )
