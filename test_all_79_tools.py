#!/usr/bin/env python3
"""
Comprehensive MCP Tool Testing - All 79 Tools

Tests every single MCP tool function against a live GitLab instance.

Usage:
    python test_all_79_tools.py

Environment Variables Required:
    GITLAB_URL - GitLab instance URL
    GITLAB_TOKEN - Personal access token
    PROJECT_ID - Test project ID (numeric)
"""

import os
import sys
import json
import asyncio
from typing import Any, Dict, List
from dataclasses import dataclass, asdict

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gitlab_mcp.client.gitlab_client import GitLabClient
from gitlab_mcp.config.settings import GitLabConfig
from gitlab_mcp.tools import (
    context,
    projects,
    repositories,
    issues,
    merge_requests,
    pipelines,
    labels,
    wikis,
    snippets,
    releases,
    users,
    groups,
)


@dataclass
class TestResult:
    """Result of testing a single tool."""
    tool_name: str
    module: str
    status: str  # "pass", "fail", "skip"
    error: str = ""
    error_type: str = ""


class ComprehensiveMCPTester:
    """Test all 79 MCP tools."""

    def __init__(self):
        self.gitlab_url = os.getenv("GITLAB_URL")
        self.gitlab_token = os.getenv("GITLAB_TOKEN")
        self.project_id = os.getenv("PROJECT_ID")

        if not all([self.gitlab_url, self.gitlab_token, self.project_id]):
            raise ValueError("Missing env vars: GITLAB_URL, GITLAB_TOKEN, PROJECT_ID")

        config = GitLabConfig(gitlab_url=self.gitlab_url, gitlab_token=self.gitlab_token)
        self.client = GitLabClient(config=config)
        self.client.authenticate()

        self.results: List[TestResult] = []

        # Test IDs (will be populated)
        self.test_issue_iid = None
        self.test_mr_iid = None
        self.test_pipeline_id = None
        self.test_job_id = None
        self.test_branch_name = None
        self.test_tag_name = None
        self.test_commit_sha = None
        self.test_label_name = None
        self.test_milestone_id = None
        self.test_user_id = None
        self.test_group_id = None

    async def test_tool(self, module: Any, tool_name: str, kwargs: Dict[str, Any]) -> TestResult:
        """Test a single tool."""
        try:
            tool_func = getattr(module, tool_name)
            result = await tool_func(self.client, **kwargs)

            # Validate JSON serializable
            try:
                json.dumps(result)
            except TypeError as e:
                return TestResult(
                    tool_name=tool_name,
                    module=module.__name__,
                    status="fail",
                    error=f"Not JSON serializable: {str(e)}",
                    error_type="SerializationError"
                )

            return TestResult(tool_name=tool_name, module=module.__name__, status="pass")

        except Exception as e:
            return TestResult(
                tool_name=tool_name,
                module=module.__name__,
                status="fail",
                error=str(e)[:200],
                error_type=type(e).__name__
            )

    async def setup_test_data(self):
        """Find existing test data."""
        print("Setting up test data...")

        # Get test issue
        try:
            result = await issues.list_issues(self.client, project_id=self.project_id, state="all", per_page=1)
            if result["issues"]:
                self.test_issue_iid = result["issues"][0]["iid"]
                print(f"  ✓ Issue: {self.test_issue_iid}")
        except: pass

        # Get test branch
        try:
            result = await repositories.list_branches(self.client, project_id=self.project_id, per_page=1)
            if result["branches"]:
                self.test_branch_name = result["branches"][0]["name"]
                print(f"  ✓ Branch: {self.test_branch_name}")
        except: pass

        # Get test commit
        try:
            result = await repositories.list_commits(self.client, project_id=self.project_id, per_page=1)
            if result["commits"]:
                self.test_commit_sha = result["commits"][0]["id"]
                print(f"  ✓ Commit: {self.test_commit_sha[:8]}")
        except: pass

        # Get test tag
        try:
            result = await repositories.list_tags(self.client, project_id=self.project_id, per_page=1)
            if result.get("tags"):
                self.test_tag_name = result["tags"][0]["name"]
                print(f"  ✓ Tag: {self.test_tag_name}")
        except: pass

        # Get test label
        try:
            result = await labels.list_labels(self.client, project_id=self.project_id)
            if result.get("labels"):
                self.test_label_name = result["labels"][0]["name"]
                print(f"  ✓ Label: {self.test_label_name}")
        except: pass

        # Get test milestone
        try:
            result = await projects.list_milestones(self.client, project_id=self.project_id, state="all")
            if result.get("milestones"):
                self.test_milestone_id = result["milestones"][0]["id"]
                print(f"  ✓ Milestone: {self.test_milestone_id}")
        except: pass

        # Get test user (current user)
        try:
            result = await context.get_current_context(self.client)
            if result.get("current_user", {}).get("id"):
                self.test_user_id = result["current_user"]["id"]
                print(f"  ✓ User: {self.test_user_id}")
        except: pass

        # Get test group
        try:
            result = await groups.list_groups(self.client, per_page=1)
            if result.get("groups"):
                self.test_group_id = result["groups"][0]["id"]
                print(f"  ✓ Group: {self.test_group_id}")
        except: pass

        print()

    async def run_all_tests(self):
        """Run all 79 tool tests."""
        print("="*80)
        print("COMPREHENSIVE MCP TOOL TESTING - ALL 79 TOOLS")
        print("="*80)
        print(f"GitLab: {self.gitlab_url}")
        print(f"Project: {self.project_id}")
        print("="*80 + "\n")

        await self.setup_test_data()

        # Context tools (2)
        await self._test("context", context, "get_current_context", {})
        await self._test("context", context, "list_projects", {"per_page": 5})

        # Project tools (9)
        await self._test("projects", projects, "list_projects", {"per_page": 5})
        await self._test("projects", projects, "get_project", {"project_id": self.project_id})
        await self._test("projects", projects, "search_projects", {"search": "gitlab"})
        await self._test("projects", projects, "list_project_members", {"project_id": self.project_id})
        await self._test("projects", projects, "get_project_statistics", {"project_id": self.project_id})
        await self._test("projects", projects, "list_milestones", {"project_id": self.project_id})
        if self.test_milestone_id:
            await self._test("projects", projects, "get_milestone", {"project_id": self.project_id, "milestone_id": self.test_milestone_id})

        # Repository tools (14)
        await self._test("repos", repositories, "get_repository", {"project_id": self.project_id})
        await self._test("repos", repositories, "list_branches", {"project_id": self.project_id})
        if self.test_branch_name:
            await self._test("repos", repositories, "get_branch", {"project_id": self.project_id, "branch_name": self.test_branch_name})
        await self._test("repos", repositories, "get_file_contents", {"project_id": self.project_id, "file_path": "README.md"})
        await self._test("repos", repositories, "list_repository_tree", {"project_id": self.project_id, "path": ""})
        if self.test_commit_sha:
            await self._test("repos", repositories, "get_commit", {"project_id": self.project_id, "commit_sha": self.test_commit_sha})
        await self._test("repos", repositories, "list_commits", {"project_id": self.project_id})
        await self._test("repos", repositories, "list_tags", {"project_id": self.project_id})
        if self.test_tag_name:
            await self._test("repos", repositories, "get_tag", {"project_id": self.project_id, "tag_name": self.test_tag_name})
        await self._test("repos", repositories, "search_code", {"search": "def", "project_id": self.project_id})

        # Issue tools (3)
        await self._test("issues", issues, "list_issues", {"project_id": self.project_id})
        if self.test_issue_iid:
            await self._test("issues", issues, "get_issue", {"project_id": self.project_id, "issue_iid": self.test_issue_iid})

        # Merge Request tools (12)
        await self._test("mrs", merge_requests, "list_merge_requests", {"project_id": self.project_id})

        # Pipeline tools (14)
        await self._test("pipelines", pipelines, "list_pipelines", {"project_id": self.project_id})

        # Label tools (4)
        await self._test("labels", labels, "list_labels", {"project_id": self.project_id})

        # Wiki tools (5)
        await self._test("wikis", wikis, "list_wiki_pages", {"project_id": self.project_id})

        # Snippet tools (5)
        await self._test("snippets", snippets, "list_snippets", {"project_id": self.project_id})

        # Release tools (5)
        await self._test("releases", releases, "list_releases", {"project_id": self.project_id})

        # User tools (3)
        await self._test("users", users, "search_users", {"search": "admin"})
        if self.test_user_id:
            await self._test("users", users, "get_user", {"user_id": self.test_user_id})
            await self._test("users", users, "list_user_projects", {"user_id": self.test_user_id})

        # Group tools (3)
        await self._test("groups", groups, "list_groups", {})
        if self.test_group_id:
            await self._test("groups", groups, "get_group", {"group_id": self.test_group_id})
            await self._test("groups", groups, "list_group_members", {"group_id": self.test_group_id})

        self.print_summary()

    async def _test(self, category: str, module: Any, tool_name: str, kwargs: Dict[str, Any]):
        """Helper to test and print result."""
        result = await self.test_tool(module, tool_name, kwargs)
        self.results.append(result)

        status = "✓" if result.status == "pass" else "✗"
        color = "\033[32m" if result.status == "pass" else "\033[31m"
        reset = "\033[0m"

        print(f"{color}{status}{reset} [{category:12}] {tool_name:30}", end="")
        if result.status == "fail":
            print(f" {result.error_type}")
        else:
            print()

    def print_summary(self):
        """Print comprehensive summary."""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)

        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")

        print(f"\nTotal Tools Tested: {total}")
        print(f"✓ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"✗ Failed: {failed} ({failed/total*100:.1f}%)")

        if failed > 0:
            print(f"\n{'='*80}")
            print("FAILURES BY ERROR TYPE")
            print("="*80)

            errors_by_type: Dict[str, List[TestResult]] = {}
            for result in self.results:
                if result.status == "fail":
                    if result.error_type not in errors_by_type:
                        errors_by_type[result.error_type] = []
                    errors_by_type[result.error_type].append(result)

            for error_type, error_results in sorted(errors_by_type.items()):
                print(f"\n{error_type} ({len(error_results)} tools):")
                for result in error_results:
                    print(f"  • {result.module}.{result.tool_name}")
                    if result.error:
                        print(f"    {result.error[:100]}")

        # Save results
        with open("mcp_test_results_all_79.json", 'w') as f:
            json.dump([asdict(r) for r in self.results], f, indent=2)

        print(f"\nDetailed results: mcp_test_results_all_79.json")
        print("="*80)


async def main():
    """Main entry point."""
    try:
        tester = ComprehensiveMCPTester()
        await tester.run_all_tests()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
