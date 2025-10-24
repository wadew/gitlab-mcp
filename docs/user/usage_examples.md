# GitLab MCP Server - Usage Examples

This document provides practical examples for common workflows using the GitLab MCP Server tools.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Discovery](#project-discovery)
- [Issue Management](#issue-management)
- [Merge Request Workflows](#merge-request-workflows)
- [Code Search and Navigation](#code-search-and-navigation)
- [Pipeline and CI/CD](#pipeline-and-cicd)
- [Wiki and Documentation](#wiki-and-documentation)
- [Advanced Workflows](#advanced-workflows)

---

## Getting Started

### Check Current Context

```python
# Get information about the authenticated user and server
context = await server.call_tool("get_current_context", {})
print(f"User: {context['username']}")
print(f"Server: {context['server_url']}")
```

---

## Project Discovery

### Find Projects

```python
# Search for projects by name
results = await server.call_tool("search_projects", {
    "search": "my-app"
})

for project in results:
    print(f"{project['name']} - {project['path_with_namespace']}")
```

### List All Accessible Projects

```python
# Get first page of projects
projects = await server.call_tool("list_projects", {
    "page": 1,
    "per_page": 50
})

for project in projects:
    print(f"[{project['id']}] {project['name']}")
```

### Get Project Details

```python
# Get detailed project information
project = await server.call_tool("get_project", {
    "project_id": 123  # or "namespace/project-name"
})

print(f"Name: {project['name']}")
print(f"Description: {project['description']}")
print(f"Stars: {project['star_count']}")
print(f"Forks: {project['forks_count']}")
```

---

## Issue Management

### Create an Issue

```python
# Create a new issue with labels
issue = await server.call_tool("create_issue", {
    "project_id": 123,
    "title": "Bug: Login page not responsive",
    "description": "The login page doesn't work on mobile devices",
    "labels": ["bug", "frontend", "priority:high"]
})

print(f"Created issue #{issue['iid']}: {issue['web_url']}")
```

### List Open Issues

```python
# Get all open issues in a project
issues = await server.call_tool("list_issues", {
    "project_id": 123,
    "state": "opened",
    "per_page": 50
})

for issue in issues:
    print(f"#{issue['iid']}: {issue['title']} [{issue['state']}]")
```

### Get Issue Details

```python
# Get full details of a specific issue
issue = await server.call_tool("get_issue", {
    "project_id": 123,
    "issue_iid": 42
})

print(f"Title: {issue['title']}")
print(f"Author: {issue['author']['name']}")
print(f"State: {issue['state']}")
print(f"Labels: {', '.join(issue['labels'])}")
print(f"Description:\n{issue['description']}")
```

### Workflow: Create Issue with Label

```python
# 1. Create a custom label
label = await server.call_tool("create_label", {
    "project_id": 123,
    "name": "needs-review",
    "color": "#FF5733",
    "description": "Requires code review"
})

# 2. Create issue with the new label
issue = await server.call_tool("create_issue", {
    "project_id": 123,
    "title": "Refactor authentication module",
    "description": "Code needs review and refactoring",
    "labels": ["needs-review", "refactoring"]
})

print(f"Issue created: {issue['web_url']}")
```

---

## Merge Request Workflows

### Create a Merge Request

```python
# Create a new merge request
mr = await server.call_tool("create_merge_request", {
    "project_id": 123,
    "source_branch": "feature/new-login",
    "target_branch": "main",
    "title": "Add new login page",
    "description": "Implements responsive login page with OAuth support"
})

print(f"MR created: !{mr['iid']}")
print(f"URL: {mr['web_url']}")
```

### Review a Merge Request

```python
# 1. Get MR details
mr = await server.call_tool("get_merge_request", {
    "project_id": 123,
    "mr_iid": 15
})

print(f"Title: {mr['title']}")
print(f"Author: {mr['author']['name']}")
print(f"Source: {mr['source_branch']} → {mr['target_branch']}")

# 2. Get file changes
changes = await server.call_tool("get_merge_request_changes", {
    "project_id": 123,
    "mr_iid": 15
})

print(f"\nFiles changed: {len(changes)}")
for change in changes:
    print(f"  {change['new_path']} ({change['diff_stats']})")

# 3. Get commits
commits = await server.call_tool("get_merge_request_commits", {
    "project_id": 123,
    "mr_iid": 15
})

print(f"\nCommits: {len(commits)}")
for commit in commits:
    print(f"  {commit['short_id']}: {commit['title']}")
```

### Approve and Merge

```python
# 1. Approve the merge request (🔒 Premium/Ultimate only)
# Note: This requires GitLab Premium or Ultimate tier
approval = await server.call_tool("approve_merge_request", {
    "project_id": 123,
    "mr_iid": 15
})

print(f"MR approved by {approval['approved_by'][0]['name']}")

# 2. Merge the merge request (✅ Available in CE/Free)
merged = await server.call_tool("merge_merge_request", {
    "project_id": 123,
    "mr_iid": 15
})

print(f"MR merged! SHA: {merged['merge_commit_sha']}")
```

**Note**: The `approve_merge_request` and `unapprove_merge_request` tools require GitLab Premium or Ultimate tier. On GitLab CE/Free, you can still:
- Create, update, and merge MRs without formal approvals
- Review and comment on MRs
- Use protected branches to control who can merge

### List Merge Requests by State

```python
# Get all merged MRs
merged_mrs = await server.call_tool("list_merge_requests", {
    "project_id": 123,
    "state": "merged",
    "per_page": 20
})

print(f"Recently merged MRs:")
for mr in merged_mrs:
    print(f"  !{mr['iid']}: {mr['title']} by {mr['author']['name']}")
```

---

## Code Search and Navigation

### Browse Repository Files

```python
# List files in root directory
tree = await server.call_tool("list_repository_tree", {
    "project_id": 123,
    "path": "",
    "ref": "main"
})

print("Project structure:")
for entry in tree['entries']:
    icon = "📁" if entry['type'] == "tree" else "📄"
    print(f"{icon} {entry['name']}")
```

### Read a File

```python
# Get file contents
file_data = await server.call_tool("get_file_contents", {
    "project_id": 123,
    "file_path": "src/main.py",
    "ref": "main"
})

print(f"File: {file_data['file_name']}")
print(f"Size: {file_data['size']} bytes")
print(f"\nContent:\n{file_data['content']}")
```

### Search Code

```python
# Search for specific code patterns
results = await server.call_tool("search_code", {
    "search_term": "def authenticate",
    "project_id": 123
})

print(f"Found {results['total']} matches:")
for result in results['results']:
    print(f"\n{result['path']}:{result['startline']}")
    print(f"  {result['data'].strip()}")
```

### Navigate to Function Definition

```python
# 1. Search for function
search_results = await server.call_tool("search_code", {
    "search_term": "class UserController",
    "project_id": 123
})

if search_results['total'] > 0:
    result = search_results['results'][0]

    # 2. Get the full file
    file_content = await server.call_tool("get_file_contents", {
        "project_id": 123,
        "file_path": result['path'],
        "ref": "main"
    })

    print(f"Found in: {result['path']}")
    print(f"Line {result['startline']}:")
    print(file_content['content'])
```

---

## Pipeline and CI/CD

### Create and Monitor Pipeline

```python
# 1. Create a new pipeline
pipeline = await server.call_tool("create_pipeline", {
    "project_id": 123,
    "ref": "main"
})

print(f"Pipeline created: #{pipeline['id']}")
print(f"Status: {pipeline['status']}")

# 2. List pipeline jobs
jobs = await server.call_tool("list_pipeline_jobs", {
    "project_id": 123,
    "pipeline_id": pipeline['id']
})

print(f"\nJobs:")
for job in jobs:
    print(f"  [{job['status']}] {job['name']} (stage: {job['stage']})")

# 3. Get job logs
for job in jobs:
    if job['status'] == 'failed':
        trace = await server.call_tool("get_job_trace", {
            "project_id": 123,
            "job_id": job['id']
        })
        print(f"\nFailed job '{job['name']}' logs:")
        print(trace)
```

### Retry Failed Pipeline

```python
# 1. Get pipeline details
pipeline = await server.call_tool("get_pipeline", {
    "project_id": 123,
    "pipeline_id": 456
})

if pipeline['status'] == 'failed':
    # 2. Retry the pipeline
    retried = await server.call_tool("retry_pipeline", {
        "project_id": 123,
        "pipeline_id": 456
    })
    print(f"Pipeline retried. New status: {retried['status']}")
```

### Download Job Artifacts

```python
# Download artifacts from a successful job
artifacts = await server.call_tool("download_job_artifacts", {
    "project_id": 123,
    "job_id": 789
})

# Save to file
with open("artifacts.zip", "wb") as f:
    f.write(artifacts)
print("Artifacts downloaded successfully")
```

---

## Wiki and Documentation

### Create Wiki Page

```python
# Create a new wiki page
wiki_page = await server.call_tool("create_wiki_page", {
    "project_id": 123,
    "title": "API Documentation",
    "content": """
# API Documentation

## Endpoints

### GET /api/users
Returns list of users...

### POST /api/users
Creates a new user...
    """,
    "format": "markdown"
})

print(f"Wiki page created: {wiki_page['slug']}")
```

### List and Read Wiki Pages

```python
# 1. List all wiki pages
pages = await server.call_tool("list_wiki_pages", {
    "project_id": 123
})

print("Wiki pages:")
for page in pages:
    print(f"  - {page['title']} ({page['slug']})")

# 2. Read a specific page
page_content = await server.call_tool("get_wiki_page", {
    "project_id": 123,
    "slug": "API-Documentation"
})

print(f"\n{page_content['title']}")
print(page_content['content'])
```

---

## Advanced Workflows

### Code Review Workflow

```python
async def review_merge_request(project_id: int, mr_iid: int):
    """Complete code review workflow."""

    # 1. Get MR details
    mr = await server.call_tool("get_merge_request", {
        "project_id": project_id,
        "mr_iid": mr_iid
    })

    print(f"Reviewing: {mr['title']}")
    print(f"Author: {mr['author']['name']}")

    # 2. Check pipeline status
    pipelines = await server.call_tool("get_merge_request_pipelines", {
        "project_id": project_id,
        "mr_iid": mr_iid
    })

    if pipelines:
        latest_pipeline = pipelines[0]
        print(f"Pipeline status: {latest_pipeline['status']}")

        if latest_pipeline['status'] != 'success':
            print("⚠️ Pipeline not passing!")
            return False

    # 3. Review changes
    changes = await server.call_tool("get_merge_request_changes", {
        "project_id": project_id,
        "mr_iid": mr_iid
    })

    print(f"Files changed: {len(changes)}")

    # 4. If all checks pass, approve (🔒 Premium/Ultimate only)
    # Note: This requires GitLab Premium or Ultimate tier
    # On CE/Free, you can merge without formal approval
    try:
        await server.call_tool("approve_merge_request", {
            "project_id": project_id,
            "mr_iid": mr_iid
        })
        print("✅ MR approved!")
    except PermissionError:
        print("⚠️ Formal approvals require Premium/Ultimate tier")
        print("✅ MR reviewed - can be merged manually")

    return True

# Use the workflow
await review_merge_request(123, 15)
```

**GitLab CE/Free Alternative**: On free tier, use comments and assignee reviews instead of formal approvals.

### Project Setup Workflow

```python
async def setup_project_labels(project_id: int):
    """Set up standard labels for a project."""

    labels = [
        {"name": "bug", "color": "#FF0000", "description": "Something isn't working"},
        {"name": "feature", "color": "#00FF00", "description": "New feature request"},
        {"name": "documentation", "color": "#0000FF", "description": "Documentation improvements"},
        {"name": "priority:high", "color": "#FF5733", "description": "High priority"},
        {"name": "priority:medium", "color": "#FFC300", "description": "Medium priority"},
        {"name": "priority:low", "color": "#DAF7A6", "description": "Low priority"},
    ]

    for label_data in labels:
        label = await server.call_tool("create_label", {
            "project_id": project_id,
            **label_data
        })
        print(f"✅ Created label: {label['name']}")

    print("Project labels setup complete!")

# Use the workflow
await setup_project_labels(123)
```

### Release Workflow

```python
async def create_release(project_id: int, version: str, tag: str):
    """Create a new release with changelog."""

    # 1. Get recent merged MRs
    mrs = await server.call_tool("list_merge_requests", {
        "project_id": project_id,
        "state": "merged",
        "per_page": 10
    })

    # 2. Generate changelog
    changelog = f"# Release {version}\n\n## Changes\n\n"
    for mr in mrs:
        changelog += f"- {mr['title']} (!{mr['iid']}) @{mr['author']['username']}\n"

    # 3. Create release
    release = await server.call_tool("create_release", {
        "project_id": project_id,
        "tag_name": tag,
        "name": f"Version {version}",
        "description": changelog
    })

    print(f"✅ Release created: {release['name']}")
    print(f"Tag: {release['tag_name']}")
    print(f"URL: {release['_links']['self']}")

    return release

# Use the workflow
await create_release(123, "1.2.0", "v1.2.0")
```

### Daily Standup Report

```python
async def generate_standup_report(project_id: int):
    """Generate a daily standup report."""

    from datetime import datetime, timedelta

    yesterday = (datetime.now() - timedelta(days=1)).isoformat()

    # 1. Get recent MRs
    mrs = await server.call_tool("list_merge_requests", {
        "project_id": project_id,
        "state": "opened",
        "per_page": 50
    })

    recent_mrs = [mr for mr in mrs if mr['updated_at'] >= yesterday]

    # 2. Get recent issues
    issues = await server.call_tool("list_issues", {
        "project_id": project_id,
        "state": "opened",
        "per_page": 50
    })

    recent_issues = [issue for issue in issues if issue['updated_at'] >= yesterday]

    # 3. Get recent pipelines
    pipelines = await server.call_tool("list_pipelines", {
        "project_id": project_id,
        "per_page": 10
    })

    # 4. Generate report
    print(f"📊 Daily Standup Report - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"\n🔄 Active Merge Requests: {len(recent_mrs)}")
    for mr in recent_mrs[:5]:
        print(f"  - !{mr['iid']}: {mr['title']} (@{mr['author']['username']})")

    print(f"\n📝 Active Issues: {len(recent_issues)}")
    for issue in recent_issues[:5]:
        print(f"  - #{issue['iid']}: {issue['title']}")

    print(f"\n🚀 Recent Pipelines:")
    for pipeline in pipelines[:3]:
        status_icon = "✅" if pipeline['status'] == "success" else "❌"
        print(f"  {status_icon} #{pipeline['id']}: {pipeline['status']} ({pipeline['ref']})")

# Use the workflow
await generate_standup_report(123)
```

---

## Best Practices

### Error Handling

Always wrap tool calls in try-except blocks:

```python
from gitlab_mcp.client.exceptions import (
    NotFoundError,
    PermissionError,
    AuthenticationError
)

try:
    issue = await server.call_tool("get_issue", {
        "project_id": 123,
        "issue_iid": 999
    })
except NotFoundError:
    print("Issue not found")
except PermissionError:
    print("No permission to access this issue")
except AuthenticationError:
    print("Authentication failed - check your token")
```

### Pagination

When dealing with large result sets, use pagination:

```python
def get_all_issues(project_id: int):
    """Get all issues using pagination."""
    all_issues = []
    page = 1
    per_page = 100

    while True:
        issues = await server.call_tool("list_issues", {
            "project_id": project_id,
            "page": page,
            "per_page": per_page
        })

        if not issues:
            break

        all_issues.extend(issues)
        page += 1

    return all_issues
```

### Rate Limiting

Be mindful of GitLab API rate limits:

```python
import asyncio

async def batch_process_with_delay(items, process_func, delay=0.5):
    """Process items with delay to avoid rate limiting."""
    results = []

    for item in items:
        result = await process_func(item)
        results.append(result)
        await asyncio.sleep(delay)  # Add delay between requests

    return results
```

---

**Last Updated:** 2025-10-24
**Version:** 1.0
