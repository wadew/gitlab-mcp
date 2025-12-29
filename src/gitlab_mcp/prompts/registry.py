"""Prompt Registry for MCP Workflow Prompts.

Provides registration and retrieval of GitLab workflow prompts.
"""

from typing import Any

# Constants for commonly used descriptions
DESC_PROJECT_ID = "Project ID or path (e.g., 'group/project')"

# Prompt definitions organized by category
PROMPT_DEFINITIONS: list[dict[str, Any]] = [
    # Core Workflows (4)
    {
        "name": "create-mr-from-issue",
        "description": "Create a branch and merge request from an issue",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "issue_iid",
                "description": "Issue IID (internal ID)",
                "required": True,
            },
        ],
    },
    {
        "name": "review-pipeline-failure",
        "description": "Analyze failed pipeline logs and identify root cause",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "pipeline_id",
                "description": "Pipeline ID to analyze",
                "required": True,
            },
        ],
    },
    {
        "name": "project-health-check",
        "description": "Check CI status, coverage, open issues, and stale MRs",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
        ],
    },
    {
        "name": "release-checklist",
        "description": "Verify release readiness (tests, changelog, version)",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "tag_name",
                "description": "Tag name for the release",
                "required": True,
            },
        ],
    },
    # Code Review Workflows (2)
    {
        "name": "code-review-prep",
        "description": "Gather MR changes, CI status, and comments for review",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "mr_iid",
                "description": "Merge request IID (internal ID)",
                "required": True,
            },
        ],
    },
    {
        "name": "security-scan-review",
        "description": "Review SAST/DAST/dependency findings in pipeline",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "pipeline_id",
                "description": "Pipeline ID with security scan results",
                "required": True,
            },
        ],
    },
    # Maintenance Workflows (3)
    {
        "name": "stale-mr-cleanup",
        "description": "Find old MRs and suggest close/merge/rebase",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "days_stale",
                "description": "Days threshold for stale MRs (optional, default: 30)",
                "required": False,
            },
        ],
    },
    {
        "name": "branch-cleanup",
        "description": "Find merged/stale branches to delete",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
        ],
    },
    {
        "name": "failed-jobs-summary",
        "description": "Summarize recent failed jobs across pipelines",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "days",
                "description": "Number of days to look back (optional, default: 7)",
                "required": False,
            },
        ],
    },
    # Deployment Workflows (1)
    {
        "name": "deployment-readiness",
        "description": "Pre-deployment checklist (CI green, approvals, conflicts)",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "mr_iid",
                "description": "Merge request IID to check for deployment",
                "required": True,
            },
        ],
    },
    # Orchestration Workflows (3)
    {
        "name": "parallel-pipeline-check",
        "description": "Run pipelines on multiple refs in parallel, collect results",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "refs",
                "description": "List of branch/tag refs to check (optional, default: main,develop)",
                "required": False,
            },
        ],
    },
    {
        "name": "bulk-mr-review",
        "description": "Prepare review context for multiple MRs concurrently",
        "arguments": [
            {
                "name": "project_id",
                "description": DESC_PROJECT_ID,
                "required": True,
            },
            {
                "name": "mr_iids",
                "description": "List of MR IIDs to review (optional, reviews all open MRs if not specified)",
                "required": False,
            },
        ],
    },
    {
        "name": "multi-project-deploy",
        "description": "Coordinate releases across multiple projects",
        "arguments": [
            {
                "name": "project_ids",
                "description": "List of project IDs or paths to deploy",
                "required": True,
            },
            {
                "name": "tag_name",
                "description": "Tag name for the release (optional)",
                "required": False,
            },
        ],
    },
]


# Prompt message templates
PROMPT_MESSAGES: dict[str, str] = {
    "create-mr-from-issue": """Create a merge request from issue #{issue_iid} in project {project_id}:

1. First, get the issue details using get_issue tool
2. Create a feature branch named 'feature/{issue_iid}-<issue-title-slug>'
3. Create a merge request with:
   - Title: "Resolve #{issue_iid}: <issue-title>"
   - Description: Closes #{issue_iid}
   - Source branch: the created feature branch
   - Target branch: main or default branch

Execute these steps in order and report the created MR URL.""",
    "review-pipeline-failure": """Analyze the failed pipeline {pipeline_id} in project {project_id}:

1. Get pipeline details using get_pipeline tool
2. List all jobs using list_pipeline_jobs tool
3. For each failed job:
   - Get job trace using get_job_trace tool (use tail_lines=200)
   - Identify the root cause of failure
4. Summarize findings:
   - Which jobs failed
   - Root cause analysis
   - Suggested fixes
   - Whether this is a flaky test or real failure""",
    "project-health-check": """Perform a health check on project {project_id}:

1. Get project details using get_project tool
2. List recent pipelines using list_pipelines tool
3. List open issues using list_issues tool
4. List open merge requests using list_merge_requests tool
5. Generate a health report including:
   - CI/CD status (recent pipeline success rate)
   - Open issue count and age distribution
   - Open MR count and review status
   - Any stale items requiring attention""",
    "release-checklist": """Verify release readiness for tag {tag_name} in project {project_id}:

1. Check if tag exists using get_tag tool
2. List recent pipelines on the release branch
3. Verify all pipelines are passing
4. Check for any open blocking issues
5. Verify CHANGELOG has been updated
6. Generate release checklist report:
   - [ ] All tests passing
   - [ ] CHANGELOG updated
   - [ ] Version bumped
   - [ ] No blocking issues
   - [ ] Release notes drafted""",
    "code-review-prep": """Prepare code review context for MR !{mr_iid} in project {project_id}:

1. Get MR details using get_merge_request tool
2. Get MR changes using get_merge_request_changes tool
3. Get MR pipelines using get_merge_request_pipelines tool
4. List MR comments using list_mr_comments tool
5. Summarize for review:
   - MR title and description
   - Files changed with change summary
   - CI/CD status
   - Existing comments/discussions
   - Review recommendations""",
    "security-scan-review": """Review security scan results from pipeline {pipeline_id} in project {project_id}:

1. Get pipeline details using get_pipeline tool
2. List all jobs to find security scan jobs
3. For security scan jobs, get job trace
4. Parse and summarize findings:
   - SAST vulnerabilities (severity breakdown)
   - Dependency vulnerabilities
   - DAST findings (if applicable)
   - Recommended remediation priority""",
    "stale-mr-cleanup": """Find and analyze stale merge requests in project {project_id}:

1. List all open MRs using list_merge_requests tool
2. Filter for MRs older than threshold (default: 30 days)
3. For each stale MR, analyze:
   - Last activity date
   - CI/CD status
   - Merge conflicts status
   - Reviewer activity
4. Recommend action for each:
   - Close (abandoned)
   - Rebase (conflicts)
   - Ping reviewers (awaiting review)
   - Merge (ready but forgotten)""",
    "branch-cleanup": """Find branches to clean up in project {project_id}:

1. List all branches using list_branches tool
2. Identify:
   - Merged branches (safe to delete)
   - Stale branches (no commits in 60+ days)
   - Orphaned branches (no associated MR)
3. Generate cleanup report:
   - Safe to delete (merged)
   - Review before delete (stale)
   - Keep (active development)""",
    "failed-jobs-summary": """Summarize recent failed jobs in project {project_id}:

1. List recent pipelines using list_pipelines tool
2. For each pipeline with failures, list jobs
3. Aggregate failure patterns:
   - Most frequently failing jobs
   - Common error patterns
   - Flaky test indicators
4. Generate summary report with remediation suggestions""",
    "deployment-readiness": """Check deployment readiness for MR !{mr_iid} in project {project_id}:

1. Get MR details using get_merge_request tool
2. Get MR pipelines using get_merge_request_pipelines tool
3. Check for:
   - All pipelines passing
   - Required approvals obtained
   - No merge conflicts
   - Labels/milestones set correctly
4. Generate deployment checklist:
   - [ ] CI/CD green
   - [ ] Approvals complete
   - [ ] No conflicts
   - [ ] Ready to merge""",
    "parallel-pipeline-check": """Run parallel pipeline checks for project {project_id}:

## Phase 1: Create Pipelines
For each ref to check:
1. Create a pipeline using create_pipeline tool
2. Store the pipeline_id for tracking

## Phase 2: Monitor Progress
Poll each pipeline status:
- Use get_pipeline to check status
- Report progress for each

## Phase 3: Summarize Results
Generate a report:
| Branch | Pipeline | Status | Duration | Failed Jobs |
|--------|----------|--------|----------|-------------|

## Phase 4: Recommendations
Based on results, suggest:
- Which branches are ready for merge
- Which need attention (failed/blocked)""",
    "bulk-mr-review": """Prepare bulk review context for multiple MRs in project {project_id}:

1. List open MRs (or use provided MR IIDs)
2. For each MR in parallel:
   - Get MR details
   - Get MR changes summary
   - Get CI/CD status
3. Generate consolidated review report:
   - MRs by priority (approvals needed, conflicts, stale)
   - Quick summary of each MR
   - Recommended review order""",
    "multi-project-deploy": """Coordinate multi-project deployment:

## Phase 1: Pre-flight Checks
For each project in the list:
1. Verify project access
2. Check latest pipeline status
3. Verify no blocking issues

## Phase 2: Release Coordination
1. Create consistent tags/releases across projects
2. Monitor deployment pipelines

## Phase 3: Verification
1. Verify all deployments succeeded
2. Generate deployment summary report""",
}


class PromptRegistry:
    """Registry for MCP workflow prompts."""

    def __init__(self) -> None:
        """Initialize the prompt registry."""
        self._prompts: dict[str, dict[str, Any]] = {}
        self._load_prompts()

    def _load_prompts(self) -> None:
        """Load prompt definitions into the registry."""
        for prompt_def in PROMPT_DEFINITIONS:
            self._prompts[prompt_def["name"]] = prompt_def

    def list_prompts(self) -> list[dict[str, Any]]:
        """List all registered prompts.

        Returns:
            List of prompt definitions with name, description, and arguments.
        """
        return list(self._prompts.values())

    def get_prompt(self, name: str) -> dict[str, Any] | None:
        """Get a specific prompt by name.

        Args:
            name: Prompt name (e.g., 'create-mr-from-issue')

        Returns:
            Prompt definition or None if not found.
        """
        return self._prompts.get(name)

    def get_prompt_messages(self, name: str, arguments: dict[str, str]) -> list[dict[str, Any]]:
        """Generate prompt messages with provided arguments.

        Args:
            name: Prompt name
            arguments: Dictionary of argument values

        Returns:
            List of message dictionaries with role and content.

        Raises:
            ValueError: If prompt not found or required arguments missing.
        """
        prompt = self.get_prompt(name)
        if prompt is None:
            raise ValueError(f"Unknown prompt: {name}")

        # Validate required arguments
        for arg in prompt["arguments"]:
            if arg["required"] and arg["name"] not in arguments:
                raise ValueError(f"Missing required argument '{arg['name']}' for prompt '{name}'")

        # Get message template
        template = PROMPT_MESSAGES.get(name)
        if template is None:
            raise ValueError(f"No message template for prompt: {name}")

        # Format message with arguments
        try:
            content = template.format(**arguments)
        except KeyError as e:
            raise ValueError(f"Missing argument for template: {e}") from e

        return [
            {
                "role": "user",
                "content": content,
            }
        ]
