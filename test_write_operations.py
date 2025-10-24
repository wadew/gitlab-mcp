#!/usr/bin/env python3
"""
Test Write Operations - Tests create/update/delete operations on mcp-test repo

Tests all write operations safely on the mcps/mcp-test repository (ID: 23).
"""

import os
import sys
import json
import asyncio
from typing import Any, Dict, List
from dataclasses import dataclass, asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gitlab_mcp.client.gitlab_client import GitLabClient
from gitlab_mcp.config.settings import GitLabConfig
from gitlab_mcp.tools import (
    issues, merge_requests, labels, projects, repositories
)


@dataclass
class TestResult:
    tool_name: str
    module: str
    status: str
    error: str = ""
    error_type: str = ""


class WriteOperationsTester:
    """Test all write operations on the test repository."""

    def __init__(self):
        self.gitlab_url = os.getenv("GITLAB_URL")
        self.gitlab_token = os.getenv("GITLAB_TOKEN")
        self.test_project_id = 23  # mcps/mcp-test

        if not all([self.gitlab_url, self.gitlab_token]):
            raise ValueError("Missing env: GITLAB_URL, GITLAB_TOKEN")

        config = GitLabConfig(gitlab_url=self.gitlab_url, gitlab_token=self.gitlab_token)
        self.client = GitLabClient(config=config)
        self.client.authenticate()

        self.results: List[TestResult] = []
        self.created_resources = {
            "issues": [],
            "labels": [],
            "milestones": [],
            "branches": [],
        }

    async def test(self, module, name, kwargs) -> TestResult:
        """Test one tool."""
        try:
            func = getattr(module, name)
            result = await func(self.client, **kwargs)

            try:
                json.dumps(result)
            except TypeError as e:
                return TestResult(name, module.__name__, "fail", f"Not JSON serializable: {e}", "SerializationError")

            return TestResult(name, module.__name__, "pass")
        except Exception as e:
            return TestResult(name, module.__name__, "fail", str(e)[:150], type(e).__name__)

    async def run_all(self):
        """Run all write operation tests."""
        print("="*80)
        print("TESTING WRITE OPERATIONS ON TEST REPO")
        print("="*80)
        print(f"GitLab: {self.gitlab_url}")
        print(f"Test Project: {self.test_project_id} (mcps/mcp-test)")
        print("="*80 + "\n")

        # === ISSUES ===
        print("\n--- Testing Issues ---")

        # Create issue
        print("Creating issue...")
        result = await self.test(issues, "create_issue", {
            "project_id": self.test_project_id,
            "title": "Test Issue - Automated Test",
            "description": "This is a test issue created by automated testing."
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_issue")
        else:
            print(f"  ✗ create_issue: {result.error}")

        # Get the created issue
        issue_result = await issues.list_issues(self.client, project_id=self.test_project_id, per_page=1)
        if issue_result.get("issues"):
            test_issue_iid = issue_result["issues"][0]["iid"]
            self.created_resources["issues"].append(test_issue_iid)
            print(f"  Created issue IID: {test_issue_iid}")

        # === LABELS ===
        print("\n--- Testing Labels ---")

        # Delete existing test label if it exists
        try:
            labels_list = await labels.list_labels(self.client, project_id=self.test_project_id)
            for label in labels_list:  # labels_list is a direct list, not a dict
                if label["name"] == "test-label":
                    await labels.delete_label(self.client, project_id=self.test_project_id, label_id=label["id"])
                    print("  Cleaned up existing test-label")
                    break
        except Exception as e:
            pass  # Label doesn't exist or error, that's fine

        # Create label
        print("Creating label...")
        result = await self.test(labels, "create_label", {
            "project_id": self.test_project_id,
            "name": "test-label",
            "color": "#FF0000",
            "description": "Test label"
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_label")
            self.created_resources["labels"].append("test-label")
        else:
            print(f"  ✗ create_label: {result.error}")

        # Update label (need to get label ID first)
        if "test-label" in self.created_resources["labels"]:
            # Get the label ID
            labels_list = await labels.list_labels(self.client, project_id=self.test_project_id)
            test_label = None
            for label in labels_list:  # labels_list is a direct list
                if label["name"] == "test-label":
                    test_label = label
                    break

            if test_label:
                print("Updating label...")
                result = await self.test(labels, "update_label", {
                    "project_id": self.test_project_id,
                    "label_id": test_label["id"],
                    "color": "#00FF00",
                    "description": "Updated test label"
                })
                self.results.append(result)
                if result.status == "pass":
                    print("  ✓ update_label")
                else:
                    print(f"  ✗ update_label: {result.error}")

        # === MILESTONES ===
        print("\n--- Testing Milestones ---")

        # Create milestone
        print("Creating milestone...")
        result = await self.test(projects, "create_milestone", {
            "project_id": self.test_project_id,
            "title": "Test Milestone v1.0",
            "description": "Test milestone for automated testing"
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_milestone")
        else:
            print(f"  ✗ create_milestone: {result.error}")

        # Get created milestone
        milestone_result = await projects.list_milestones(self.client, project_id=self.test_project_id, per_page=1)
        if milestone_result and len(milestone_result) > 0:
            test_milestone_id = milestone_result[0]["id"]
            self.created_resources["milestones"].append(test_milestone_id)
            print(f"  Created milestone ID: {test_milestone_id}")

            # Update milestone
            print("Updating milestone...")
            result = await self.test(projects, "update_milestone", {
                "project_id": self.test_project_id,
                "milestone_id": test_milestone_id,
                "description": "Updated milestone description"
            })
            self.results.append(result)
            if result.status == "pass":
                print("  ✓ update_milestone")
            else:
                print(f"  ✗ update_milestone: {result.error}")

        # === BRANCHES ===
        print("\n--- Testing Branches ---")

        # Create branch
        print("Creating branch...")
        result = await self.test(repositories, "create_branch", {
            "project_id": self.test_project_id,
            "branch_name": "test-branch-automated",
            "ref": "main"
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_branch")
            self.created_resources["branches"].append("test-branch-automated")
        else:
            print(f"  ✗ create_branch: {result.error}")

        # Delete branch
        if "test-branch-automated" in self.created_resources["branches"]:
            print("Deleting branch...")
            result = await self.test(repositories, "delete_branch", {
                "project_id": self.test_project_id,
                "branch_name": "test-branch-automated"
            })
            self.results.append(result)
            if result.status == "pass":
                print("  ✓ delete_branch")
                self.created_resources["branches"].remove("test-branch-automated")
            else:
                print(f"  ✗ delete_branch: {result.error}")

        # === CLEANUP ===
        print("\n--- Cleanup ---")
        print("Deleting test label...")
        if "test-label" in self.created_resources["labels"]:
            # Get label ID
            labels_list = await labels.list_labels(self.client, project_id=self.test_project_id)
            for label in labels_list:  # labels_list is a direct list
                if label["name"] == "test-label":
                    result = await self.test(labels, "delete_label", {
                        "project_id": self.test_project_id,
                        "label_id": label["id"]
                    })
                    self.results.append(result)
                    if result.status == "pass":
                        print("  ✓ delete_label")
                    else:
                        print(f"  ✗ delete_label: {result.error}")
                    break

        print("\nNote: Issues and milestones left in place for manual review")

        self.print_summary()

    def print_summary(self):
        """Print summary."""
        print("\n" + "="*80)
        print("WRITE OPERATIONS TEST RESULTS")
        print("="*80)

        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")

        print(f"\nTested: {total} write operations")
        print(f"✓ Pass: {passed} ({passed/total*100:.1f}%)")
        print(f"✗ Fail: {failed} ({failed/total*100:.1f}%)")

        if failed > 0:
            print(f"\n{'='*80}")
            print("FAILURES")
            print("="*80)

            by_type = {}
            for r in self.results:
                if r.status == "fail":
                    if r.error_type not in by_type:
                        by_type[r.error_type] = []
                    by_type[r.error_type].append(r)

            for error_type, results in sorted(by_type.items()):
                print(f"\n{error_type} ({len(results)}):")
                for r in results:
                    print(f"  ✗ {r.module}.{r.tool_name}")
                    print(f"    {r.error}")

        with open("write_operations_test_results.json", 'w') as f:
            json.dump([asdict(r) for r in self.results], f, indent=2)

        print(f"\nResults: write_operations_test_results.json")
        print("="*80)


async def main():
    tester = WriteOperationsTester()
    await tester.run_all()


if __name__ == "__main__":
    asyncio.run(main())
