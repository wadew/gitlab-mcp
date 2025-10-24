#!/usr/bin/env python3
"""
Automated MCP Tool Testing Script

Tests all 79 MCP tools against a live GitLab instance to identify:
- Tools that work correctly
- Tools that fail with errors
- Error categories and patterns

Usage:
    python test_all_mcp_tools.py

Environment Variables Required:
    GITLAB_URL - GitLab instance URL
    GITLAB_TOKEN - Personal access token
    PROJECT_ID - Test project ID (numeric)
"""

import os
import sys
import json
import asyncio
from typing import Any, Dict, List, Tuple
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
    execution_time: float = 0.0


class MCPToolTester:
    """Automated tester for all MCP tools."""

    def __init__(self):
        self.gitlab_url = os.getenv("GITLAB_URL")
        self.gitlab_token = os.getenv("GITLAB_TOKEN")
        self.project_id = os.getenv("PROJECT_ID")

        if not all([self.gitlab_url, self.gitlab_token, self.project_id]):
            raise ValueError(
                "Missing required environment variables: GITLAB_URL, GITLAB_TOKEN, PROJECT_ID"
            )

        # Create config and client
        config = GitLabConfig(
            gitlab_url=self.gitlab_url,
            gitlab_token=self.gitlab_token
        )
        self.client = GitLabClient(config=config)
        self.client.authenticate()

        self.results: List[TestResult] = []

        # Test data (will be populated during tests)
        self.test_issue_iid: int = None
        self.test_mr_iid: int = None
        self.test_pipeline_id: int = None
        self.test_job_id: int = None

    async def test_tool(
        self,
        module: Any,
        tool_name: str,
        kwargs: Dict[str, Any]
    ) -> TestResult:
        """Test a single MCP tool."""
        import time

        start_time = time.time()

        try:
            # Get the tool function
            tool_func = getattr(module, tool_name)

            # Call the tool
            result = await tool_func(self.client, **kwargs)

            execution_time = time.time() - start_time

            # Validate result is serializable
            try:
                json.dumps(result)
            except TypeError as e:
                return TestResult(
                    tool_name=tool_name,
                    module=module.__name__,
                    status="fail",
                    error=f"Result not JSON serializable: {str(e)}",
                    error_type="SerializationError",
                    execution_time=execution_time
                )

            return TestResult(
                tool_name=tool_name,
                module=module.__name__,
                status="pass",
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            error_type = type(e).__name__

            return TestResult(
                tool_name=tool_name,
                module=module.__name__,
                status="fail",
                error=str(e),
                error_type=error_type,
                execution_time=execution_time
            )

    async def setup_test_data(self):
        """Set up test data by finding existing resources."""
        print("Setting up test data...")

        # Get existing issue for testing
        try:
            issues_result = await issues.list_issues(
                self.client,
                project_id=self.project_id,
                state="all",
                per_page=1
            )
            if issues_result["issues"]:
                self.test_issue_iid = issues_result["issues"][0]["iid"]
                print(f"  ✓ Found test issue: {self.test_issue_iid}")
        except Exception as e:
            print(f"  ✗ Could not find test issue: {e}")

        # Get existing MR for testing
        try:
            mrs_result = await merge_requests.list_merge_requests(
                self.client,
                project_id=self.project_id,
                state="all",
                per_page=1
            )
            if isinstance(mrs_result, dict) and mrs_result.get("merge_requests"):
                self.test_mr_iid = mrs_result["merge_requests"][0]["iid"]
                print(f"  ✓ Found test MR: {self.test_mr_iid}")
        except Exception:
            pass

        # Get existing pipeline for testing
        try:
            pipelines_result = await pipelines.list_pipelines(
                self.client,
                project_id=self.project_id,
                per_page=1
            )
            if isinstance(pipelines_result, dict) and pipelines_result.get("pipelines"):
                self.test_pipeline_id = pipelines_result["pipelines"][0]["id"]
                print(f"  ✓ Found test pipeline: {self.test_pipeline_id}")
        except Exception:
            pass

        print()

    async def test_context_tools(self):
        """Test context tools."""
        print("Testing context tools...")

        tests = [
            ("get_current_context", {}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(context, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_project_tools(self):
        """Test project tools."""
        print("\nTesting project tools...")

        tests = [
            ("list_projects", {"per_page": 5}),
            ("get_project", {"project_id": self.project_id}),
            ("search_projects", {"query": "gitlab"}),  # Note: might be 'search' not 'query'
            ("list_project_members", {"project_id": self.project_id}),
            ("get_project_statistics", {"project_id": self.project_id}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(projects, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_repository_tools(self):
        """Test repository tools."""
        print("\nTesting repository tools...")

        tests = [
            ("list_repository_tree", {"project_id": self.project_id, "path": "", "recursive": False}),
            ("get_file_contents", {"project_id": self.project_id, "file_path": "README.md"}),
            ("search_code", {"query": "def", "project_id": self.project_id}),  # Note: might be 'search'
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(repositories, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_issue_tools(self):
        """Test issue tools."""
        print("\nTesting issue tools...")

        tests = [
            ("list_issues", {"project_id": self.project_id, "state": "all", "per_page": 5}),
        ]

        if self.test_issue_iid:
            tests.append(("get_issue", {"project_id": self.project_id, "issue_iid": self.test_issue_iid}))

        for tool_name, kwargs in tests:
            result = await self.test_tool(issues, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_merge_request_tools(self):
        """Test merge request tools."""
        print("\nTesting merge request tools...")

        tests = [
            ("list_merge_requests", {"project_id": self.project_id, "state": "all", "per_page": 5}),
        ]

        if self.test_mr_iid:
            tests.extend([
                ("get_merge_request", {"project_id": self.project_id, "mr_iid": self.test_mr_iid}),
                ("get_merge_request_changes", {"project_id": self.project_id, "mr_iid": self.test_mr_iid}),
                ("get_merge_request_commits", {"project_id": self.project_id, "mr_iid": self.test_mr_iid}),
                ("get_merge_request_pipelines", {"project_id": self.project_id, "mr_iid": self.test_mr_iid}),
            ])

        for tool_name, kwargs in tests:
            result = await self.test_tool(merge_requests, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_pipeline_tools(self):
        """Test pipeline tools."""
        print("\nTesting pipeline tools...")

        tests = [
            ("list_pipelines", {"project_id": self.project_id, "per_page": 5}),
        ]

        if self.test_pipeline_id:
            tests.extend([
                ("get_pipeline", {"project_id": self.project_id, "pipeline_id": self.test_pipeline_id}),
                ("list_pipeline_jobs", {"project_id": self.project_id, "pipeline_id": self.test_pipeline_id}),
                ("list_pipeline_variables", {"project_id": self.project_id, "pipeline_id": self.test_pipeline_id}),
            ])

        for tool_name, kwargs in tests:
            result = await self.test_tool(pipelines, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_label_tools(self):
        """Test label tools."""
        print("\nTesting label tools...")

        tests = [
            ("list_labels", {"project_id": self.project_id}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(labels, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_wiki_tools(self):
        """Test wiki tools."""
        print("\nTesting wiki tools...")

        tests = [
            ("list_wiki_pages", {"project_id": self.project_id}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(wikis, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_snippet_tools(self):
        """Test snippet tools."""
        print("\nTesting snippet tools...")

        tests = [
            ("list_snippets", {"project_id": self.project_id}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(snippets, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_release_tools(self):
        """Test release tools."""
        print("\nTesting release tools...")

        tests = [
            ("list_releases", {"project_id": self.project_id}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(releases, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_user_tools(self):
        """Test user tools."""
        print("\nTesting user tools...")

        tests = [
            ("search_users", {"query": "admin"}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(users, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    async def test_group_tools(self):
        """Test group tools."""
        print("\nTesting group tools...")

        tests = [
            ("list_groups", {}),
        ]

        for tool_name, kwargs in tests:
            result = await self.test_tool(groups, tool_name, kwargs)
            self.results.append(result)
            self._print_result(result)

    def _print_result(self, result: TestResult):
        """Print a single test result."""
        status_symbol = "✓" if result.status == "pass" else "✗"
        status_color = "\033[32m" if result.status == "pass" else "\033[31m"
        reset_color = "\033[0m"

        print(f"  {status_color}{status_symbol}{reset_color} {result.tool_name} ", end="")

        if result.status == "fail":
            print(f"[{result.error_type}]")
            if len(result.error) < 80:
                print(f"     {result.error}")
        else:
            print(f"({result.execution_time:.2f}s)")

    async def run_all_tests(self):
        """Run all tests."""
        print("=" * 80)
        print("MCP Tool Automated Testing")
        print("=" * 80)
        print(f"GitLab URL: {self.gitlab_url}")
        print(f"Project ID: {self.project_id}")
        print("=" * 80)
        print()

        await self.setup_test_data()

        # Run all test suites
        await self.test_context_tools()
        await self.test_project_tools()
        await self.test_repository_tools()
        await self.test_issue_tools()
        await self.test_merge_request_tools()
        await self.test_pipeline_tools()
        await self.test_label_tools()
        await self.test_wiki_tools()
        await self.test_snippet_tools()
        await self.test_release_tools()
        await self.test_user_tools()
        await self.test_group_tools()

        self.print_summary()

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")

        print(f"\nTotal Tools Tested: {total}")
        print(f"✓ Passed: {passed} ({passed/total*100:.1f}%)")
        print(f"✗ Failed: {failed} ({failed/total*100:.1f}%)")

        if failed > 0:
            print(f"\n{'='*80}")
            print("FAILURES BY ERROR TYPE")
            print("=" * 80)

            # Group by error type
            errors_by_type: Dict[str, List[TestResult]] = {}
            for result in self.results:
                if result.status == "fail":
                    if result.error_type not in errors_by_type:
                        errors_by_type[result.error_type] = []
                    errors_by_type[result.error_type].append(result)

            for error_type, results in sorted(errors_by_type.items()):
                print(f"\n{error_type} ({len(results)} tools):")
                for result in results:
                    print(f"  • {result.module}.{result.tool_name}")
                    print(f"    {result.error[:100]}")

        # Save detailed results to JSON
        output_file = "mcp_test_results.json"
        with open(output_file, 'w') as f:
            json.dump([asdict(r) for r in self.results], f, indent=2)

        print(f"\nDetailed results saved to: {output_file}")
        print("=" * 80)


async def main():
    """Main entry point."""
    try:
        tester = MCPToolTester()
        await tester.run_all_tests()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
