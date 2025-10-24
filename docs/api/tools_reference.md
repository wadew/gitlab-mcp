# GitLab MCP Server - Tools Reference

This document provides a comprehensive reference for all 67 MCP tools available in the GitLab MCP Server.

## GitLab CE Compatibility

✅ **97.8% compatible with GitLab CE (Community Edition / Free tier)!**

**65 out of 67 tools** work with GitLab CE. Only 2 tools require Premium/Ultimate:
- 🔒 `approve_merge_request` - Premium/Ultimate only
- 🔒 `unapprove_merge_request` - Premium/Ultimate only

All other tools work perfectly with GitLab CE/Free tier.

## Tool Categories

- [Context Tools](#context-tools) (1 tool)
- [Repository Tools](#repository-tools) (3 tools)
- [Issue Tools](#issue-tools) (3 tools)
- [Merge Request Tools](#merge-request-tools) (12 tools)
- [Pipeline Tools](#pipeline-tools) (14 tools)
- [Project Tools](#project-tools) (9 tools)
- [Label Tools](#label-tools) (4 tools)
- [Wiki Tools](#wiki-tools) (5 tools)
- [Snippet Tools](#snippet-tools) (5 tools)
- [Release Tools](#release-tools) (5 tools)
- [User Tools](#user-tools) (3 tools)
- [Group Tools](#group-tools) (3 tools)

---

## Context Tools

### `get_current_context`

Get current GitLab user and server context information.

**Parameters:**
- None

**Returns:**
- Dictionary with user information and server details

**Example:**
```python
result = await client.call_tool("get_current_context", {})
```

---

## Repository Tools

### `list_repository_tree`

List files and directories in a repository tree.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `path` (str): Path inside repository (default: root)
- `ref` (str): Branch/tag/commit (optional, default: default branch)
- `recursive` (bool): Recursive listing (default: False)
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- Dictionary with tree entries and metadata

### `get_file_contents`

Get the contents of a file from a repository.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `file_path` (str): Path to file (required)
- `ref` (str): Branch/tag/commit (optional)

**Returns:**
- Dictionary with file content and metadata

### `search_code`

Search for code in project repositories.

**Parameters:**
- `search_term` (str): Search query (required)
- `project_id` (int/str): Project ID (optional, searches globally if omitted)
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- Dictionary with search results

---

## Issue Tools

### `list_issues`

List issues for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `state` (str): Filter by state (opened/closed) (optional)
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- List of issue dictionaries

### `get_issue`

Get details of a specific issue.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `issue_iid` (int): Issue IID (required)

**Returns:**
- Dictionary with issue details

### `create_issue`

Create a new issue in a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `title` (str): Issue title (required)
- `description` (str): Issue description (optional)
- `labels` (list): Label names (optional)
- `assignee_ids` (list): Assignee user IDs (optional)

**Returns:**
- Dictionary with created issue details

---

## Merge Request Tools

### `list_merge_requests`

List merge requests for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `state` (str): Filter by state (opened/closed/merged) (optional)
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- List of merge request dictionaries

### `get_merge_request`

Get details of a specific merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- Dictionary with MR details

### `create_merge_request`

Create a new merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `source_branch` (str): Source branch name (required)
- `target_branch` (str): Target branch name (required)
- `title` (str): MR title (required)
- `description` (str): MR description (optional)

**Returns:**
- Dictionary with created MR details

### `update_merge_request`

Update an existing merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)
- `title` (str): New title (optional)
- `description` (str): New description (optional)
- `state_event` (str): State change (close/reopen) (optional)

**Returns:**
- Dictionary with updated MR details

### `merge_merge_request`

Merge an approved merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- Dictionary with merged MR details

### `close_merge_request`

Close a merge request without merging.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- Dictionary with closed MR details

### `reopen_merge_request`

Reopen a closed merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- Dictionary with reopened MR details

### `approve_merge_request` 🔒 Premium/Ultimate

Approve a merge request.

**Tier**: Premium, Ultimate only (not available in GitLab CE/Free)

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- Dictionary with approval details

**Note**: This feature requires GitLab Premium or Ultimate tier. On GitLab CE/Free, this endpoint will return a 403 Forbidden or 404 Not Found error.

### `unapprove_merge_request` 🔒 Premium/Ultimate

Remove approval from a merge request.

**Tier**: Premium, Ultimate only (not available in GitLab CE/Free)

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- Dictionary with unapproval details

**Note**: This feature requires GitLab Premium or Ultimate tier. On GitLab CE/Free, this endpoint will return a 403 Forbidden or 404 Not Found error.

### `get_merge_request_changes`

Get the file changes in a merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- List of file change dictionaries

### `get_merge_request_commits`

Get commits in a merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- List of commit dictionaries

### `get_merge_request_pipelines`

Get pipelines for a merge request.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `mr_iid` (int): MR IID (required)

**Returns:**
- List of pipeline dictionaries

---

## Pipeline Tools

### `list_pipelines`

List pipelines for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- List of pipeline dictionaries

### `get_pipeline`

Get details of a specific pipeline.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `pipeline_id` (int): Pipeline ID (required)

**Returns:**
- Dictionary with pipeline details

### `create_pipeline`

Create a new pipeline.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `ref` (str): Branch/tag name (required)

**Returns:**
- Dictionary with created pipeline details

### `retry_pipeline`

Retry a failed pipeline.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `pipeline_id` (int): Pipeline ID (required)

**Returns:**
- Dictionary with retried pipeline details

### `cancel_pipeline`

Cancel a running pipeline.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `pipeline_id` (int): Pipeline ID (required)

**Returns:**
- Dictionary with cancelled pipeline details

### `delete_pipeline`

Delete a pipeline.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `pipeline_id` (int): Pipeline ID (required)

**Returns:**
- None (deletion confirmation)

### `list_pipeline_jobs`

List jobs in a pipeline.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `pipeline_id` (int): Pipeline ID (required)

**Returns:**
- List of job dictionaries

### `get_job`

Get details of a specific job.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `job_id` (int): Job ID (required)

**Returns:**
- Dictionary with job details

### `get_job_trace`

Get the trace log of a job.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `job_id` (int): Job ID (required)

**Returns:**
- String with job trace log

### `retry_job`

Retry a failed job.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `job_id` (int): Job ID (required)

**Returns:**
- Dictionary with retried job details

### `cancel_job`

Cancel a running job.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `job_id` (int): Job ID (required)

**Returns:**
- Dictionary with cancelled job details

### `play_job`

Play a manual job.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `job_id` (int): Job ID (required)

**Returns:**
- Dictionary with played job details

### `download_job_artifacts`

Download artifacts from a job.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `job_id` (int): Job ID (required)

**Returns:**
- Binary artifact data

### `list_pipeline_variables`

List variables for a pipeline.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `pipeline_id` (int): Pipeline ID (required)

**Returns:**
- List of variable dictionaries

---

## Project Tools

### `list_projects`

List projects accessible by the user.

**Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- List of project dictionaries

### `get_project`

Get details of a specific project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- Dictionary with project details

### `search_projects`

Search for projects by name or description.

**Parameters:**
- `search` (str): Search term (required)
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- List of matching project dictionaries

### `list_project_members`

List members of a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- List of member dictionaries

### `get_project_statistics`

Get statistics for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- Dictionary with project statistics

### `list_milestones`

List milestones for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- List of milestone dictionaries

### `get_milestone`

Get details of a specific milestone.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `milestone_id` (int): Milestone ID (required)

**Returns:**
- Dictionary with milestone details

### `create_milestone`

Create a new milestone.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `title` (str): Milestone title (required)
- `description` (str): Milestone description (optional)
- `due_date` (str): Due date (YYYY-MM-DD) (optional)

**Returns:**
- Dictionary with created milestone details

### `update_milestone`

Update an existing milestone.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `milestone_id` (int): Milestone ID (required)
- `title` (str): New title (optional)
- `description` (str): New description (optional)
- `due_date` (str): New due date (optional)
- `state_event` (str): State change (close/activate) (optional)

**Returns:**
- Dictionary with updated milestone details

---

## Label Tools

### `list_labels`

List labels for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- List of label dictionaries

### `create_label`

Create a new label.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `name` (str): Label name (required)
- `color` (str): Label color hex code (required, e.g., "#FF0000")
- `description` (str): Label description (optional)

**Returns:**
- Dictionary with created label details

### `update_label`

Update an existing label.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `label_id` (int): Label ID (required)
- `name` (str): New name (optional)
- `color` (str): New color (optional)
- `description` (str): New description (optional)

**Returns:**
- Dictionary with updated label details

### `delete_label`

Delete a label.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `label_id` (int): Label ID (required)

**Returns:**
- None (deletion confirmation)

---

## Wiki Tools

### `list_wiki_pages`

List wiki pages for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- List of wiki page dictionaries

### `get_wiki_page`

Get content of a specific wiki page.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `slug` (str): Wiki page slug (required)

**Returns:**
- Dictionary with wiki page content

### `create_wiki_page`

Create a new wiki page.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `title` (str): Page title (required)
- `content` (str): Page content (required)
- `format` (str): Content format (markdown/rdoc/asciidoc) (default: markdown)

**Returns:**
- Dictionary with created wiki page details

### `update_wiki_page`

Update an existing wiki page.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `slug` (str): Wiki page slug (required)
- `title` (str): New title (optional)
- `content` (str): New content (optional)
- `format` (str): Content format (optional)

**Returns:**
- Dictionary with updated wiki page details

### `delete_wiki_page`

Delete a wiki page.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `slug` (str): Wiki page slug (required)

**Returns:**
- None (deletion confirmation)

---

## Snippet Tools

### `list_snippets`

List snippets for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- List of snippet dictionaries

### `get_snippet`

Get content of a specific snippet.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `snippet_id` (int): Snippet ID (required)

**Returns:**
- Dictionary with snippet content

### `create_snippet`

Create a new snippet.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `title` (str): Snippet title (required)
- `file_name` (str): File name (required)
- `content` (str): Snippet content (required)
- `visibility` (str): Visibility level (private/internal/public) (default: private)

**Returns:**
- Dictionary with created snippet details

### `update_snippet`

Update an existing snippet.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `snippet_id` (int): Snippet ID (required)
- `title` (str): New title (optional)
- `file_name` (str): New file name (optional)
- `content` (str): New content (optional)

**Returns:**
- Dictionary with updated snippet details

### `delete_snippet`

Delete a snippet.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `snippet_id` (int): Snippet ID (required)

**Returns:**
- None (deletion confirmation)

---

## Release Tools

### `list_releases`

List releases for a project.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)

**Returns:**
- List of release dictionaries

### `get_release`

Get details of a specific release.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `tag_name` (str): Release tag name (required)

**Returns:**
- Dictionary with release details

### `create_release`

Create a new release.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `tag_name` (str): Tag name for release (required)
- `name` (str): Release name (required)
- `description` (str): Release description (optional)

**Returns:**
- Dictionary with created release details

### `update_release`

Update an existing release.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `tag_name` (str): Release tag name (required)
- `name` (str): New name (optional)
- `description` (str): New description (optional)

**Returns:**
- Dictionary with updated release details

### `delete_release`

Delete a release.

**Parameters:**
- `project_id` (int/str): Project ID or path (required)
- `tag_name` (str): Release tag name (required)

**Returns:**
- None (deletion confirmation)

---

## User Tools

### `get_user`

Get details of a specific user.

**Parameters:**
- `user_id` (int): User ID (required)

**Returns:**
- Dictionary with user details

### `search_users`

Search for users by username or email.

**Parameters:**
- `search` (str): Search term (required)

**Returns:**
- List of matching user dictionaries

### `list_user_projects`

List projects for a specific user.

**Parameters:**
- `user_id` (int): User ID (required)

**Returns:**
- List of project dictionaries

---

## Group Tools

### `list_groups`

List groups accessible by the user.

**Parameters:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Results per page (default: 20)

**Returns:**
- List of group dictionaries

### `get_group`

Get details of a specific group.

**Parameters:**
- `group_id` (int/str): Group ID or path (required)

**Returns:**
- Dictionary with group details

### `list_group_members`

List members of a group.

**Parameters:**
- `group_id` (int/str): Group ID or path (required)

**Returns:**
- List of member dictionaries

---

## Error Handling

All tools may raise the following exceptions:

- `AuthenticationError`: Authentication failed or token invalid
- `NotFoundError`: Requested resource not found
- `PermissionError`: Insufficient permissions for operation
- `ValidationError`: Invalid parameters or data
- `GitLabAPIError`: General API error
- `NetworkError`: Network connectivity issue

**Example Error Handling:**
```python
try:
    result = await client.call_tool("get_issue", {
        "project_id": 123,
        "issue_iid": 1
    })
except NotFoundError:
    print("Issue not found")
except PermissionError:
    print("No permission to access issue")
```

---

## Pagination

Many list tools support pagination with `page` and `per_page` parameters:

- `page`: Page number (starts at 1)
- `per_page`: Results per page (default: 20, maximum: 100)

**Example:**
```python
# Get first page (20 results)
page1 = await client.call_tool("list_issues", {
    "project_id": 123,
    "page": 1,
    "per_page": 20
})

# Get second page
page2 = await client.call_tool("list_issues", {
    "project_id": 123,
    "page": 2,
    "per_page": 20
})
```

---

**Last Updated:** 2025-10-24
**Version:** 1.0
**Total Tools:** 67
