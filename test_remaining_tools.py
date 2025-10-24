#!/usr/bin/env python3
"""
Test Remaining 38 Tools - Comprehensive test of all untested MCP tools

Tests all previously untested tools on the mcps/mcp-test repository (ID: 23).
Creates necessary test data (MRs, pipelines, wikis, snippets, releases, tags).
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
    repositories, merge_requests, pipelines, wikis, snippets,
    releases, projects, users, groups
)


@dataclass
class TestResult:
    tool_name: str
    module: str
    status: str
    error: str = ""
    error_type: str = ""


class RemainingToolsTester:
    """Test all remaining untested tools."""

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
        self.test_data = {}

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
            return TestResult(name, module.__name__, "fail", str(e)[:200], type(e).__name__)

    async def run_all(self):
        """Run all remaining tool tests."""
        print("="*80)
        print("TESTING REMAINING 38 UNTESTED TOOLS")
        print("="*80)
        print(f"GitLab: {self.gitlab_url}")
        print(f"Test Project: {self.test_project_id} (mcps/mcp-test)")
        print("="*80 + "\n")

        # === SETUP: Create test branches and commits ===
        print("--- Setup: Creating test data ---")

        # Create a test branch for MR
        try:
            await repositories.create_branch(
                self.client,
                project_id=self.test_project_id,
                branch_name="test-mr-branch",
                ref="main"
            )
            self.test_data["mr_branch"] = "test-mr-branch"
            print("  ✓ Created test-mr-branch")
        except Exception as e:
            print(f"  ⚠ Branch might already exist: {str(e)[:100]}")
            self.test_data["mr_branch"] = "test-mr-branch"

        # === REPOSITORIES ===
        print("\n--- Testing Repositories (1 tool) ---")

        # create_tag
        print("Testing create_tag...")
        result = await self.test(repositories, "create_tag", {
            "project_id": self.test_project_id,
            "tag_name": "v0.0.1-test",
            "ref": "main",
            "message": "Test tag"
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_tag")
            self.test_data["tag"] = "v0.0.1-test"
        else:
            print(f"  ✗ create_tag: {result.error}")

        # === MERGE REQUESTS ===
        print("\n--- Testing Merge Requests (11 tools) ---")

        # create_merge_request
        print("Testing create_merge_request...")
        result = await self.test(merge_requests, "create_merge_request", {
            "project_id": self.test_project_id,
            "source_branch": "test-mr-branch",
            "target_branch": "main",
            "title": "Test MR - Automated Testing",
            "description": "This is a test merge request"
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_merge_request")
            # Get the created MR
            mr_list = await merge_requests.list_merge_requests(
                self.client, project_id=self.test_project_id, per_page=1
            )
            if mr_list and len(mr_list) > 0:
                self.test_data["mr_iid"] = mr_list[0]["iid"]
                print(f"    Created MR IID: {self.test_data['mr_iid']}")
        else:
            print(f"  ✗ create_merge_request: {result.error}")

        if "mr_iid" in self.test_data:
            mr_iid = self.test_data["mr_iid"]

            # get_merge_request
            print("Testing get_merge_request...")
            result = await self.test(merge_requests, "get_merge_request", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_merge_request{': ' + result.error if result.status == 'fail' else ''}")

            # get_merge_request_changes
            print("Testing get_merge_request_changes...")
            result = await self.test(merge_requests, "get_merge_request_changes", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_merge_request_changes{': ' + result.error if result.status == 'fail' else ''}")

            # get_merge_request_commits
            print("Testing get_merge_request_commits...")
            result = await self.test(merge_requests, "get_merge_request_commits", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_merge_request_commits{': ' + result.error if result.status == 'fail' else ''}")

            # get_merge_request_pipelines
            print("Testing get_merge_request_pipelines...")
            result = await self.test(merge_requests, "get_merge_request_pipelines", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_merge_request_pipelines{': ' + result.error if result.status == 'fail' else ''}")

            # update_merge_request
            print("Testing update_merge_request...")
            result = await self.test(merge_requests, "update_merge_request", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid,
                "description": "Updated description for test MR"
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} update_merge_request{': ' + result.error if result.status == 'fail' else ''}")

            # approve_merge_request
            print("Testing approve_merge_request...")
            result = await self.test(merge_requests, "approve_merge_request", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} approve_merge_request{': ' + result.error if result.status == 'fail' else ''}")

            # unapprove_merge_request
            print("Testing unapprove_merge_request...")
            result = await self.test(merge_requests, "unapprove_merge_request", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} unapprove_merge_request{': ' + result.error if result.status == 'fail' else ''}")

            # close_merge_request
            print("Testing close_merge_request...")
            result = await self.test(merge_requests, "close_merge_request", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} close_merge_request{': ' + result.error if result.status == 'fail' else ''}")

            # reopen_merge_request
            print("Testing reopen_merge_request...")
            result = await self.test(merge_requests, "reopen_merge_request", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} reopen_merge_request{': ' + result.error if result.status == 'fail' else ''}")

            # merge_merge_request (do this last to clean up)
            print("Testing merge_merge_request...")
            result = await self.test(merge_requests, "merge_merge_request", {
                "project_id": self.test_project_id,
                "mr_iid": mr_iid
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} merge_merge_request{': ' + result.error if result.status == 'fail' else ''}")

        # === PIPELINES ===
        print("\n--- Testing Pipelines (10 tools) ---")

        # create_pipeline
        print("Testing create_pipeline...")
        result = await self.test(pipelines, "create_pipeline", {
            "project_id": self.test_project_id,
            "ref": "main"
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_pipeline")
            # Get the created pipeline
            pipeline_list = await pipelines.list_pipelines(
                self.client, project_id=self.test_project_id, per_page=1
            )
            if pipeline_list and pipeline_list.get("pipelines"):
                self.test_data["pipeline_id"] = pipeline_list["pipelines"][0]["id"]
                print(f"    Created pipeline ID: {self.test_data['pipeline_id']}")
        else:
            print(f"  ✗ create_pipeline: {result.error}")

        if "pipeline_id" in self.test_data:
            pipeline_id = self.test_data["pipeline_id"]

            # get_pipeline
            print("Testing get_pipeline...")
            result = await self.test(pipelines, "get_pipeline", {
                "project_id": self.test_project_id,
                "pipeline_id": pipeline_id
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_pipeline{': ' + result.error if result.status == 'fail' else ''}")

            # list_pipeline_variables
            print("Testing list_pipeline_variables...")
            result = await self.test(pipelines, "list_pipeline_variables", {
                "project_id": self.test_project_id,
                "pipeline_id": pipeline_id
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} list_pipeline_variables{': ' + result.error if result.status == 'fail' else ''}")

            # Wait a bit for jobs to be created
            await asyncio.sleep(2)

            # Get job from pipeline
            try:
                jobs = await pipelines.list_pipeline_jobs(
                    self.client, project_id=self.test_project_id, pipeline_id=pipeline_id
                )
                if jobs and len(jobs) > 0:
                    self.test_data["job_id"] = jobs[0]["id"]
                    print(f"    Found job ID: {self.test_data['job_id']}")
            except:
                pass

            if "job_id" in self.test_data:
                job_id = self.test_data["job_id"]

                # get_job
                print("Testing get_job...")
                result = await self.test(pipelines, "get_job", {
                    "project_id": self.test_project_id,
                    "job_id": job_id
                })
                self.results.append(result)
                print(f"  {'✓' if result.status == 'pass' else '✗'} get_job{': ' + result.error if result.status == 'fail' else ''}")

                # play_job (if manual)
                print("Testing play_job...")
                result = await self.test(pipelines, "play_job", {
                    "project_id": self.test_project_id,
                    "job_id": job_id
                })
                self.results.append(result)
                print(f"  {'✓' if result.status == 'pass' else '✗'} play_job{': ' + result.error if result.status == 'fail' else ''}")

                # retry_job
                print("Testing retry_job...")
                result = await self.test(pipelines, "retry_job", {
                    "project_id": self.test_project_id,
                    "job_id": job_id
                })
                self.results.append(result)
                print(f"  {'✓' if result.status == 'pass' else '✗'} retry_job{': ' + result.error if result.status == 'fail' else ''}")

                # cancel_job
                print("Testing cancel_job...")
                result = await self.test(pipelines, "cancel_job", {
                    "project_id": self.test_project_id,
                    "job_id": job_id
                })
                self.results.append(result)
                print(f"  {'✓' if result.status == 'pass' else '✗'} cancel_job{': ' + result.error if result.status == 'fail' else ''}")

            # retry_pipeline
            print("Testing retry_pipeline...")
            result = await self.test(pipelines, "retry_pipeline", {
                "project_id": self.test_project_id,
                "pipeline_id": pipeline_id
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} retry_pipeline{': ' + result.error if result.status == 'fail' else ''}")

            # cancel_pipeline
            print("Testing cancel_pipeline...")
            result = await self.test(pipelines, "cancel_pipeline", {
                "project_id": self.test_project_id,
                "pipeline_id": pipeline_id
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} cancel_pipeline{': ' + result.error if result.status == 'fail' else ''}")

            # delete_pipeline
            print("Testing delete_pipeline...")
            result = await self.test(pipelines, "delete_pipeline", {
                "project_id": self.test_project_id,
                "pipeline_id": pipeline_id
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} delete_pipeline{': ' + result.error if result.status == 'fail' else ''}")

        # === WIKIS ===
        print("\n--- Testing Wikis (4 tools) ---")

        # create_wiki_page
        print("Testing create_wiki_page...")
        result = await self.test(wikis, "create_wiki_page", {
            "project_id": self.test_project_id,
            "title": "Test Wiki Page",
            "content": "# Test Wiki\n\nThis is a test wiki page."
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_wiki_page")
            self.test_data["wiki_slug"] = "test-wiki-page"
        else:
            print(f"  ✗ create_wiki_page: {result.error}")

        if "wiki_slug" in self.test_data:
            # get_wiki_page
            print("Testing get_wiki_page...")
            result = await self.test(wikis, "get_wiki_page", {
                "project_id": self.test_project_id,
                "slug": self.test_data["wiki_slug"]
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_wiki_page{': ' + result.error if result.status == 'fail' else ''}")

            # update_wiki_page
            print("Testing update_wiki_page...")
            result = await self.test(wikis, "update_wiki_page", {
                "project_id": self.test_project_id,
                "slug": self.test_data["wiki_slug"],
                "content": "# Updated Test Wiki\n\nContent has been updated."
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} update_wiki_page{': ' + result.error if result.status == 'fail' else ''}")

            # delete_wiki_page
            print("Testing delete_wiki_page...")
            result = await self.test(wikis, "delete_wiki_page", {
                "project_id": self.test_project_id,
                "slug": self.test_data["wiki_slug"]
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} delete_wiki_page{': ' + result.error if result.status == 'fail' else ''}")

        # === SNIPPETS ===
        print("\n--- Testing Snippets (4 tools) ---")

        # create_snippet
        print("Testing create_snippet...")
        result = await self.test(snippets, "create_snippet", {
            "project_id": self.test_project_id,
            "title": "Test Snippet",
            "file_name": "test.py",
            "content": "print('Hello from test snippet')"
        })
        self.results.append(result)
        if result.status == "pass":
            print("  ✓ create_snippet")
            # Get the created snippet
            snippet_list = await snippets.list_snippets(
                self.client, project_id=self.test_project_id
            )
            if snippet_list and len(snippet_list) > 0:
                self.test_data["snippet_id"] = snippet_list[0]["id"]
                print(f"    Created snippet ID: {self.test_data['snippet_id']}")
        else:
            print(f"  ✗ create_snippet: {result.error}")

        if "snippet_id" in self.test_data:
            snippet_id = self.test_data["snippet_id"]

            # get_snippet
            print("Testing get_snippet...")
            result = await self.test(snippets, "get_snippet", {
                "project_id": self.test_project_id,
                "snippet_id": snippet_id
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_snippet{': ' + result.error if result.status == 'fail' else ''}")

            # update_snippet
            print("Testing update_snippet...")
            result = await self.test(snippets, "update_snippet", {
                "project_id": self.test_project_id,
                "snippet_id": snippet_id,
                "content": "print('Updated snippet content')"
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} update_snippet{': ' + result.error if result.status == 'fail' else ''}")

            # delete_snippet
            print("Testing delete_snippet...")
            result = await self.test(snippets, "delete_snippet", {
                "project_id": self.test_project_id,
                "snippet_id": snippet_id
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} delete_snippet{': ' + result.error if result.status == 'fail' else ''}")

        # === RELEASES ===
        print("\n--- Testing Releases (4 tools) ---")

        # create_release (need a tag first)
        if "tag" in self.test_data:
            print("Testing create_release...")
            result = await self.test(releases, "create_release", {
                "project_id": self.test_project_id,
                "tag_name": self.test_data["tag"],
                "name": "Test Release v0.0.1",
                "description": "Test release for automated testing"
            })
            self.results.append(result)
            if result.status == "pass":
                print("  ✓ create_release")
            else:
                print(f"  ✗ create_release: {result.error}")

            # get_release
            print("Testing get_release...")
            result = await self.test(releases, "get_release", {
                "project_id": self.test_project_id,
                "tag_name": self.test_data["tag"]
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} get_release{': ' + result.error if result.status == 'fail' else ''}")

            # update_release
            print("Testing update_release...")
            result = await self.test(releases, "update_release", {
                "project_id": self.test_project_id,
                "tag_name": self.test_data["tag"],
                "description": "Updated release description"
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} update_release{': ' + result.error if result.status == 'fail' else ''}")

            # delete_release
            print("Testing delete_release...")
            result = await self.test(releases, "delete_release", {
                "project_id": self.test_project_id,
                "tag_name": self.test_data["tag"]
            })
            self.results.append(result)
            print(f"  {'✓' if result.status == 'pass' else '✗'} delete_release{': ' + result.error if result.status == 'fail' else ''}")

        # === PROJECTS ===
        print("\n--- Testing Projects (1 tool) ---")

        # create_milestone (with unique name this time)
        print("Testing create_milestone...")
        import time
        milestone_title = f"Test Milestone {int(time.time())}"
        result = await self.test(projects, "create_milestone", {
            "project_id": self.test_project_id,
            "title": milestone_title,
            "description": "Test milestone with unique name"
        })
        self.results.append(result)
        print(f"  {'✓' if result.status == 'pass' else '✗'} create_milestone{': ' + result.error if result.status == 'fail' else ''}")

        # === USERS ===
        print("\n--- Testing Users (1 tool) ---")

        # Get current user ID
        try:
            from gitlab_mcp.tools import context
            ctx = await context.get_current_context(self.client)
            user_id = ctx.get("current_user", {}).get("id")
            if user_id:
                # list_user_projects
                print("Testing list_user_projects...")
                result = await self.test(users, "list_user_projects", {
                    "user_id": user_id
                })
                self.results.append(result)
                print(f"  {'✓' if result.status == 'pass' else '✗'} list_user_projects{': ' + result.error if result.status == 'fail' else ''}")
        except Exception as e:
            print(f"  ✗ Could not test list_user_projects: {e}")

        # === GROUPS ===
        print("\n--- Testing Groups (2 tools) ---")

        # Get a group ID
        try:
            group_list = await groups.list_groups(self.client, per_page=1)
            if group_list and len(group_list) > 0:
                group_id = group_list[0]["id"]

                # get_group
                print("Testing get_group...")
                result = await self.test(groups, "get_group", {
                    "group_id": group_id
                })
                self.results.append(result)
                print(f"  {'✓' if result.status == 'pass' else '✗'} get_group{': ' + result.error if result.status == 'fail' else ''}")

                # list_group_members
                print("Testing list_group_members...")
                result = await self.test(groups, "list_group_members", {
                    "group_id": group_id
                })
                self.results.append(result)
                print(f"  {'✓' if result.status == 'pass' else '✗'} list_group_members{': ' + result.error if result.status == 'fail' else ''}")
        except Exception as e:
            print(f"  ✗ Could not test group tools: {e}")

        self.print_summary()

    def print_summary(self):
        """Print summary."""
        print("\n" + "="*80)
        print("REMAINING TOOLS TEST RESULTS")
        print("="*80)

        total = len(self.results)
        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")

        print(f"\nTested: {total} tools")
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

        with open("remaining_tools_test_results.json", 'w') as f:
            json.dump([asdict(r) for r in self.results], f, indent=2)

        print(f"\nResults: remaining_tools_test_results.json")
        print("="*80)


async def main():
    tester = RemainingToolsTester()
    await tester.run_all()


if __name__ == "__main__":
    asyncio.run(main())
