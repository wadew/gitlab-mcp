"""Unit tests for MCP Workflow Prompts.

Tests verify:
- All 13 prompts are registered
- Prompts have required fields (name, description, arguments)
- Prompt messages are generated correctly
- Arguments are validated
"""

import pytest


class TestPromptRegistry:
    """Test prompt registry and listing."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_registry_has_prompts(self, registry):
        """Registry should have prompts defined."""
        prompts = registry.list_prompts()
        assert isinstance(prompts, list)
        assert len(prompts) > 0

    def test_registry_has_13_prompts(self, registry):
        """Registry should have exactly 13 prompts."""
        prompts = registry.list_prompts()
        assert len(prompts) == 13

    def test_all_prompts_have_name(self, registry):
        """All prompts should have a name."""
        prompts = registry.list_prompts()
        for prompt in prompts:
            assert "name" in prompt
            assert len(prompt["name"]) > 0

    def test_all_prompts_have_description(self, registry):
        """All prompts should have a description."""
        prompts = registry.list_prompts()
        for prompt in prompts:
            assert "description" in prompt
            assert len(prompt["description"]) > 0

    def test_all_prompts_have_arguments(self, registry):
        """All prompts should have arguments (even if empty)."""
        prompts = registry.list_prompts()
        for prompt in prompts:
            assert "arguments" in prompt
            assert isinstance(prompt["arguments"], list)


class TestCoreWorkflowPrompts:
    """Test core workflow prompts."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_create_mr_from_issue_exists(self, registry):
        """create-mr-from-issue prompt should exist."""
        prompt = registry.get_prompt("create-mr-from-issue")
        assert prompt is not None
        assert prompt["name"] == "create-mr-from-issue"

    def test_create_mr_from_issue_has_required_args(self, registry):
        """create-mr-from-issue should require project_id and issue_iid."""
        prompt = registry.get_prompt("create-mr-from-issue")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names
        assert "issue_iid" in arg_names

    def test_review_pipeline_failure_exists(self, registry):
        """review-pipeline-failure prompt should exist."""
        prompt = registry.get_prompt("review-pipeline-failure")
        assert prompt is not None

    def test_review_pipeline_failure_has_required_args(self, registry):
        """review-pipeline-failure should require project_id and pipeline_id."""
        prompt = registry.get_prompt("review-pipeline-failure")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names
        assert "pipeline_id" in arg_names

    def test_project_health_check_exists(self, registry):
        """project-health-check prompt should exist."""
        prompt = registry.get_prompt("project-health-check")
        assert prompt is not None

    def test_project_health_check_has_required_args(self, registry):
        """project-health-check should require project_id."""
        prompt = registry.get_prompt("project-health-check")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names

    def test_release_checklist_exists(self, registry):
        """release-checklist prompt should exist."""
        prompt = registry.get_prompt("release-checklist")
        assert prompt is not None

    def test_release_checklist_has_required_args(self, registry):
        """release-checklist should require project_id and tag_name."""
        prompt = registry.get_prompt("release-checklist")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names
        assert "tag_name" in arg_names


class TestCodeReviewPrompts:
    """Test code review workflow prompts."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_code_review_prep_exists(self, registry):
        """code-review-prep prompt should exist."""
        prompt = registry.get_prompt("code-review-prep")
        assert prompt is not None

    def test_code_review_prep_has_required_args(self, registry):
        """code-review-prep should require project_id and mr_iid."""
        prompt = registry.get_prompt("code-review-prep")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names
        assert "mr_iid" in arg_names

    def test_security_scan_review_exists(self, registry):
        """security-scan-review prompt should exist."""
        prompt = registry.get_prompt("security-scan-review")
        assert prompt is not None

    def test_security_scan_review_has_required_args(self, registry):
        """security-scan-review should require project_id and pipeline_id."""
        prompt = registry.get_prompt("security-scan-review")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names
        assert "pipeline_id" in arg_names


class TestMaintenancePrompts:
    """Test maintenance workflow prompts."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_stale_mr_cleanup_exists(self, registry):
        """stale-mr-cleanup prompt should exist."""
        prompt = registry.get_prompt("stale-mr-cleanup")
        assert prompt is not None

    def test_stale_mr_cleanup_has_required_args(self, registry):
        """stale-mr-cleanup should require project_id."""
        prompt = registry.get_prompt("stale-mr-cleanup")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names

    def test_branch_cleanup_exists(self, registry):
        """branch-cleanup prompt should exist."""
        prompt = registry.get_prompt("branch-cleanup")
        assert prompt is not None

    def test_branch_cleanup_has_required_args(self, registry):
        """branch-cleanup should require project_id."""
        prompt = registry.get_prompt("branch-cleanup")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names

    def test_failed_jobs_summary_exists(self, registry):
        """failed-jobs-summary prompt should exist."""
        prompt = registry.get_prompt("failed-jobs-summary")
        assert prompt is not None

    def test_failed_jobs_summary_has_required_args(self, registry):
        """failed-jobs-summary should require project_id."""
        prompt = registry.get_prompt("failed-jobs-summary")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names


class TestDeploymentPrompts:
    """Test deployment workflow prompts."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_deployment_readiness_exists(self, registry):
        """deployment-readiness prompt should exist."""
        prompt = registry.get_prompt("deployment-readiness")
        assert prompt is not None

    def test_deployment_readiness_has_required_args(self, registry):
        """deployment-readiness should require project_id and mr_iid."""
        prompt = registry.get_prompt("deployment-readiness")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names
        assert "mr_iid" in arg_names


class TestOrchestrationPrompts:
    """Test orchestration workflow prompts."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_parallel_pipeline_check_exists(self, registry):
        """parallel-pipeline-check prompt should exist."""
        prompt = registry.get_prompt("parallel-pipeline-check")
        assert prompt is not None

    def test_parallel_pipeline_check_has_required_args(self, registry):
        """parallel-pipeline-check should require project_id."""
        prompt = registry.get_prompt("parallel-pipeline-check")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names

    def test_bulk_mr_review_exists(self, registry):
        """bulk-mr-review prompt should exist."""
        prompt = registry.get_prompt("bulk-mr-review")
        assert prompt is not None

    def test_bulk_mr_review_has_required_args(self, registry):
        """bulk-mr-review should require project_id."""
        prompt = registry.get_prompt("bulk-mr-review")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_id" in arg_names

    def test_multi_project_deploy_exists(self, registry):
        """multi-project-deploy prompt should exist."""
        prompt = registry.get_prompt("multi-project-deploy")
        assert prompt is not None

    def test_multi_project_deploy_has_required_args(self, registry):
        """multi-project-deploy should require project_ids."""
        prompt = registry.get_prompt("multi-project-deploy")
        arg_names = [arg["name"] for arg in prompt["arguments"]]
        assert "project_ids" in arg_names


class TestPromptMessageGeneration:
    """Test prompt message generation."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_get_prompt_messages_returns_list(self, registry):
        """get_prompt_messages should return a list of messages."""
        messages = registry.get_prompt_messages(
            "create-mr-from-issue",
            {"project_id": "group/project", "issue_iid": "5"}
        )
        assert isinstance(messages, list)
        assert len(messages) > 0

    def test_prompt_message_has_role(self, registry):
        """Prompt messages should have a role."""
        messages = registry.get_prompt_messages(
            "create-mr-from-issue",
            {"project_id": "group/project", "issue_iid": "5"}
        )
        for message in messages:
            assert "role" in message
            assert message["role"] in ["user", "assistant", "system"]

    def test_prompt_message_has_content(self, registry):
        """Prompt messages should have content."""
        messages = registry.get_prompt_messages(
            "create-mr-from-issue",
            {"project_id": "group/project", "issue_iid": "5"}
        )
        for message in messages:
            assert "content" in message
            assert len(message["content"]) > 0

    def test_prompt_message_includes_arguments(self, registry):
        """Prompt messages should include provided arguments."""
        messages = registry.get_prompt_messages(
            "create-mr-from-issue",
            {"project_id": "my-project", "issue_iid": "42"}
        )
        # The generated message should reference the issue
        content = messages[0]["content"]
        assert "42" in content or "issue" in content.lower()

    def test_unknown_prompt_raises_error(self, registry):
        """Unknown prompt should raise ValueError."""
        with pytest.raises(ValueError, match="Unknown prompt"):
            registry.get_prompt_messages("unknown-prompt", {})

    def test_missing_required_argument_raises_error(self, registry):
        """Missing required argument should raise ValueError."""
        with pytest.raises(ValueError, match="required"):
            registry.get_prompt_messages("create-mr-from-issue", {"project_id": "test"})


class TestArgumentMetadata:
    """Test argument metadata for prompts."""

    @pytest.fixture
    def registry(self):
        """Create a prompt registry."""
        from gitlab_mcp.prompts.registry import PromptRegistry

        return PromptRegistry()

    def test_argument_has_name(self, registry):
        """Arguments should have a name."""
        prompt = registry.get_prompt("create-mr-from-issue")
        for arg in prompt["arguments"]:
            assert "name" in arg
            assert len(arg["name"]) > 0

    def test_argument_has_description(self, registry):
        """Arguments should have a description."""
        prompt = registry.get_prompt("create-mr-from-issue")
        for arg in prompt["arguments"]:
            assert "description" in arg
            assert len(arg["description"]) > 0

    def test_argument_has_required_flag(self, registry):
        """Arguments should have a required flag."""
        prompt = registry.get_prompt("create-mr-from-issue")
        for arg in prompt["arguments"]:
            assert "required" in arg
            assert isinstance(arg["required"], bool)

