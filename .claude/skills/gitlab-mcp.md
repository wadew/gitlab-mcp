# GitLab MCP Server Usage Guide

## Overview
This skill provides comprehensive guidance on using the GitLab MCP (Model Context Protocol) server to interact with GitLab repositories, issues, merge requests, pipelines, and more.

## Prerequisites
- GitLab MCP server must be configured and running
- Valid GitLab personal access token with appropriate permissions
- Project ID or path (format: 'group/project' or numeric ID)

## Common Patterns

### Project Identification
Projects can be referenced by:
- **Numeric ID**: `22`
- **Path**: `mcps/gitlab_mcp`
- **Full path**: `group/subgroup/project`

### Getting Current Context
Start by understanding your GitLab environment:

```
mcp__gitlab__get_current_context
```

Returns:
- Current user information
- GitLab server URL
- API version
- Authentication status

## Core Operations

### 1. Projects

#### List All Projects
```
mcp__gitlab__list_projects
Parameters:
  - membership: boolean (optional) - only projects where user is member
  - owned: boolean (optional) - only owned projects
  - visibility: string (optional) - "public", "internal", "private"
  - per_page: integer (optional) - results per page (default: 20)
```

#### Get Project Details
```
mcp__gitlab__get_project
Parameters:
  - project_id: string (required) - project ID or path
```

#### Create Project
```
mcp__gitlab__create_project
Parameters:
  - name: string (required) - project name
  - path: string (optional) - project path/slug (defaults to name if not provided)
  - namespace_id: integer (optional) - ID of the namespace/group to create project in
  - description: string (optional) - project description
  - visibility: string (optional) - "private", "internal", or "public" (default: private)
  - initialize_with_readme: boolean (optional) - initialize with README.md (default: false)
```

#### Search Projects
```
mcp__gitlab__search_projects
Parameters:
  - search: string (required) - search query
```

#### Project Members
```
mcp__gitlab__list_project_members
Parameters:
  - project_id: string (required)
```

#### Project Statistics
```
mcp__gitlab__get_project_statistics
Parameters:
  - project_id: string (required)
```

### 2. Repository Operations

#### List Repository Tree
```
mcp__gitlab__list_repository_tree
Parameters:
  - project_id: string (required)
  - path: string (optional) - subdirectory path
  - ref: string (optional) - branch, tag, or commit SHA (default: HEAD)
  - recursive: boolean (optional) - list recursively (default: false)
```

#### Get File Contents
```
mcp__gitlab__get_file_contents
Parameters:
  - project_id: string (required)
  - file_path: string (required)
  - ref: string (optional) - branch, tag, or commit SHA (default: HEAD)
```

#### Search Code
```
mcp__gitlab__search_code
Parameters:
  - search: string (required) - search query
  - project_id: string (optional) - limit to specific project
```

### 3. Issues

#### List Issues
```
mcp__gitlab__list_issues
Parameters:
  - project_id: string (required)
  - state: string (optional) - "opened", "closed", "all" (default: opened)
  - assignee_id: integer (optional)
  - author_id: integer (optional)
  - labels: array (optional) - filter by labels
  - milestone: string (optional) - milestone title
  - per_page: integer (optional) - default: 20
```

#### Get Issue Details
```
mcp__gitlab__get_issue
Parameters:
  - project_id: string (required)
  - issue_iid: integer (required) - issue IID (internal ID)
```

#### Create Issue
```
mcp__gitlab__create_issue
Parameters:
  - project_id: string (required)
  - title: string (required)
  - description: string (optional)
  - assignee_ids: array of integers (optional)
  - labels: array of strings (optional)
  - milestone_id: integer (optional)
```

### 4. Merge Requests

#### List Merge Requests
```
mcp__gitlab__list_merge_requests
Parameters:
  - project_id: string (required)
  - state: string (optional) - "opened", "closed", "merged", "all" (default: opened)
  - assignee_id: integer (optional)
  - author_id: integer (optional)
  - labels: array (optional)
  - milestone: string (optional)
  - per_page: integer (optional)
```

#### Get Merge Request Details
```
mcp__gitlab__get_merge_request
Parameters:
  - project_id: string (required)
  - mr_iid: integer (required) - MR IID (internal ID)
```

#### Create Merge Request
```
mcp__gitlab__create_merge_request
Parameters:
  - project_id: string (required)
  - source_branch: string (required)
  - target_branch: string (required)
  - title: string (required)
  - description: string (optional)
  - assignee_ids: array of integers (optional)
  - labels: array of strings (optional)
  - milestone_id: integer (optional)
```

#### Update Merge Request
```
mcp__gitlab__update_merge_request
Parameters:
  - project_id: string (required)
  - mr_iid: integer (required)
  - title: string (optional)
  - description: string (optional)
  - assignee_ids: array of integers (optional)
  - labels: array of strings (optional)
  - milestone_id: integer (optional)
```

#### Merge Request Actions
```
# Approve
mcp__gitlab__approve_merge_request
Parameters:
  - project_id: string (required)
  - mr_iid: integer (required)

# Unapprove
mcp__gitlab__unapprove_merge_request
Parameters: same as approve

# Merge
mcp__gitlab__merge_merge_request
Parameters:
  - project_id: string (required)
  - mr_iid: integer (required)
  - merge_commit_message: string (optional)
  - should_remove_source_branch: boolean (optional)

# Close (without merging)
mcp__gitlab__close_merge_request
Parameters:
  - project_id: string (required)
  - mr_iid: integer (required)

# Reopen
mcp__gitlab__reopen_merge_request
Parameters: same as close
```

#### Get Merge Request Details
```
# Get file changes
mcp__gitlab__get_merge_request_changes
Parameters:
  - project_id: string (required)
  - mr_iid: integer (required)

# Get commits
mcp__gitlab__get_merge_request_commits
Parameters: same as changes

# Get pipelines
mcp__gitlab__get_merge_request_pipelines
Parameters: same as changes
```

### 5. Pipelines & CI/CD

#### List Pipelines
```
mcp__gitlab__list_pipelines
Parameters:
  - project_id: string (required)
  - ref: string (optional) - filter by branch/tag
  - status: string (optional) - "running", "pending", "success", "failed", "canceled"
  - per_page: integer (optional)
```

#### Get Pipeline Details
```
mcp__gitlab__get_pipeline
Parameters:
  - project_id: string (required)
  - pipeline_id: integer (required)
```

#### Create Pipeline
```
mcp__gitlab__create_pipeline
Parameters:
  - project_id: string (required)
  - ref: string (required) - branch or tag name
  - variables: object (optional) - pipeline variables
```

#### Pipeline Actions
```
# Retry failed pipeline
mcp__gitlab__retry_pipeline
Parameters:
  - project_id: string (required)
  - pipeline_id: integer (required)

# Cancel running pipeline
mcp__gitlab__cancel_pipeline
Parameters: same as retry

# Delete pipeline
mcp__gitlab__delete_pipeline
Parameters: same as retry
```

#### Pipeline Jobs
```
# List jobs in pipeline
mcp__gitlab__list_pipeline_jobs
Parameters:
  - project_id: string (required)
  - pipeline_id: integer (required)

# Get job details
mcp__gitlab__get_job
Parameters:
  - project_id: string (required)
  - job_id: integer (required)

# Get job trace/log
mcp__gitlab__get_job_trace
Parameters: same as get_job

# Job actions
mcp__gitlab__retry_job
mcp__gitlab__cancel_job
mcp__gitlab__play_job  # For manual jobs
Parameters: same as get_job

# Download artifacts
mcp__gitlab__download_job_artifacts
Parameters:
  - project_id: string (required)
  - job_id: integer (required)
  - artifact_path: string (optional) - specific artifact path

# List pipeline variables
mcp__gitlab__list_pipeline_variables
Parameters:
  - project_id: string (required)
  - pipeline_id: integer (required)
```

### 6. Milestones

#### List Milestones
```
mcp__gitlab__list_milestones
Parameters:
  - project_id: string (required)
  - state: string (optional) - "active", "closed", "all" (default: active)
```

#### Get Milestone
```
mcp__gitlab__get_milestone
Parameters:
  - project_id: string (required)
  - milestone_id: integer (required)
```

#### Create Milestone
```
mcp__gitlab__create_milestone
Parameters:
  - project_id: string (required)
  - title: string (required)
  - description: string (optional)
  - start_date: string (optional) - YYYY-MM-DD format
  - due_date: string (optional) - YYYY-MM-DD format
```

#### Update Milestone
```
mcp__gitlab__update_milestone
Parameters:
  - project_id: string (required)
  - milestone_id: integer (required)
  - title: string (optional)
  - description: string (optional)
  - start_date: string (optional)
  - due_date: string (optional)
  - state_event: string (optional) - "close" or "activate"
```

### 7. Labels

#### List Labels
```
mcp__gitlab__list_labels
Parameters:
  - project_id: string (required)
```

#### Create Label
```
mcp__gitlab__create_label
Parameters:
  - project_id: string (required)
  - name: string (required)
  - color: string (required) - hex format (e.g., '#FF0000')
  - description: string (optional)
```

#### Update Label
```
mcp__gitlab__update_label
Parameters:
  - project_id: string (required)
  - name: string (required) - current label name
  - new_name: string (optional)
  - color: string (optional) - hex format
  - description: string (optional)
```

#### Delete Label
```
mcp__gitlab__delete_label
Parameters:
  - project_id: string (required)
  - name: string (required)
```

### 8. Wiki

#### List Wiki Pages
```
mcp__gitlab__list_wiki_pages
Parameters:
  - project_id: string (required)
```

#### Get Wiki Page
```
mcp__gitlab__get_wiki_page
Parameters:
  - project_id: string (required)
  - slug: string (required) - URL-friendly identifier
```

#### Create Wiki Page
```
mcp__gitlab__create_wiki_page
Parameters:
  - project_id: string (required)
  - title: string (required)
  - content: string (required) - Markdown format
```

#### Update Wiki Page
```
mcp__gitlab__update_wiki_page
Parameters:
  - project_id: string (required)
  - slug: string (required)
  - title: string (optional)
  - content: string (optional)
```

#### Delete Wiki Page
```
mcp__gitlab__delete_wiki_page
Parameters:
  - project_id: string (required)
  - slug: string (required)
```

### 9. Snippets

#### List Snippets
```
mcp__gitlab__list_snippets
Parameters:
  - project_id: string (required)
```

#### Get Snippet
```
mcp__gitlab__get_snippet
Parameters:
  - project_id: string (required)
  - snippet_id: integer (required)
```

#### Create Snippet
```
mcp__gitlab__create_snippet
Parameters:
  - project_id: string (required)
  - title: string (required)
  - file_name: string (required)
  - content: string (required)
  - visibility: string (optional) - "private", "internal", "public" (default: private)
```

#### Update Snippet
```
mcp__gitlab__update_snippet
Parameters:
  - project_id: string (required)
  - snippet_id: integer (required)
  - title: string (optional)
  - file_name: string (optional)
  - content: string (optional)
  - visibility: string (optional)
```

#### Delete Snippet
```
mcp__gitlab__delete_snippet
Parameters:
  - project_id: string (required)
  - snippet_id: integer (required)
```

### 10. Releases

#### List Releases
```
mcp__gitlab__list_releases
Parameters:
  - project_id: string (required)
```

#### Get Release
```
mcp__gitlab__get_release
Parameters:
  - project_id: string (required)
  - tag_name: string (required) - Git tag name
```

#### Create Release
```
mcp__gitlab__create_release
Parameters:
  - project_id: string (required)
  - tag_name: string (required)
  - name: string (required)
  - description: string (optional)
  - ref: string (optional) - commit SHA, branch, or tag (default: default branch)
```

#### Update Release
```
mcp__gitlab__update_release
Parameters:
  - project_id: string (required)
  - tag_name: string (required)
  - name: string (optional)
  - description: string (optional)
```

#### Delete Release
```
mcp__gitlab__delete_release
Parameters:
  - project_id: string (required)
  - tag_name: string (required)
```

### 11. Users & Groups

#### Get User
```
mcp__gitlab__get_user
Parameters:
  - user_id: integer (required)
```

#### Search Users
```
mcp__gitlab__search_users
Parameters:
  - search: string (required) - username or email
```

#### List User Projects
```
mcp__gitlab__list_user_projects
Parameters:
  - user_id: integer (required)
```

#### List Groups
```
mcp__gitlab__list_groups
Parameters:
  - owned: boolean (optional) - only owned groups
  - per_page: integer (optional)
```

#### Get Group
```
mcp__gitlab__get_group
Parameters:
  - group_id: string (required) - group ID or path
```

#### List Group Members
```
mcp__gitlab__list_group_members
Parameters:
  - group_id: string (required)
```

## Common Workflows

### Workflow 1: Review a Merge Request
```
1. List merge requests:
   mcp__gitlab__list_merge_requests
   - project_id: "mcps/gitlab_mcp"
   - state: "opened"

2. Get MR details:
   mcp__gitlab__get_merge_request
   - project_id: "mcps/gitlab_mcp"
   - mr_iid: <from list>

3. Get file changes:
   mcp__gitlab__get_merge_request_changes
   - project_id: "mcps/gitlab_mcp"
   - mr_iid: <same>

4. Check pipeline status:
   mcp__gitlab__get_merge_request_pipelines
   - project_id: "mcps/gitlab_mcp"
   - mr_iid: <same>

5. Approve if good:
   mcp__gitlab__approve_merge_request
   - project_id: "mcps/gitlab_mcp"
   - mr_iid: <same>
```

### Workflow 2: Debug a Failed Pipeline
```
1. List recent pipelines:
   mcp__gitlab__list_pipelines
   - project_id: "mcps/gitlab_mcp"
   - status: "failed"

2. Get pipeline details:
   mcp__gitlab__get_pipeline
   - project_id: "mcps/gitlab_mcp"
   - pipeline_id: <from list>

3. List jobs in pipeline:
   mcp__gitlab__list_pipeline_jobs
   - project_id: "mcps/gitlab_mcp"
   - pipeline_id: <same>

4. Get failed job trace:
   mcp__gitlab__get_job_trace
   - project_id: "mcps/gitlab_mcp"
   - job_id: <failed job ID>

5. After fix, retry:
   mcp__gitlab__retry_pipeline
   - project_id: "mcps/gitlab_mcp"
   - pipeline_id: <same>
```

### Workflow 3: Explore a New Repository
```
1. Get project details:
   mcp__gitlab__get_project
   - project_id: "group/project"

2. List repository tree:
   mcp__gitlab__list_repository_tree
   - project_id: "group/project"
   - recursive: true

3. Read important files:
   mcp__gitlab__get_file_contents
   - project_id: "group/project"
   - file_path: "README.md"

4. Search for specific code:
   mcp__gitlab__search_code
   - project_id: "group/project"
   - search: "function_name"
```

### Workflow 4: Create and Manage an Issue
```
1. Create issue:
   mcp__gitlab__create_issue
   - project_id: "mcps/gitlab_mcp"
   - title: "Add new feature"
   - description: "Description here"
   - labels: ["enhancement", "priority::high"]

2. Get issue details:
   mcp__gitlab__get_issue
   - project_id: "mcps/gitlab_mcp"
   - issue_iid: <from create response>

3. Track related issues:
   mcp__gitlab__list_issues
   - project_id: "mcps/gitlab_mcp"
   - labels: ["enhancement"]
   - state: "opened"
```

### Workflow 5: Release Management
```
1. List recent releases:
   mcp__gitlab__list_releases
   - project_id: "mcps/gitlab_mcp"

2. Create new release:
   mcp__gitlab__create_release
   - project_id: "mcps/gitlab_mcp"
   - tag_name: "v1.0.0"
   - name: "Version 1.0.0"
   - description: "Release notes here"

3. Check pipeline for release tag:
   mcp__gitlab__list_pipelines
   - project_id: "mcps/gitlab_mcp"
   - ref: "v1.0.0"

4. Download artifacts if needed:
   mcp__gitlab__download_job_artifacts
   - project_id: "mcps/gitlab_mcp"
   - job_id: <from pipeline>
```

### Workflow 6: Create a New Project
```
1. Get the group/namespace ID (if creating in a group):
   mcp__gitlab__get_group
   - group_id: "mcps"

2. Create the project:
   mcp__gitlab__create_project
   - name: "my-new-project"
   - path: "my-new-project"
   - namespace_id: <from group response>
   - description: "Project description"
   - visibility: "private"
   - initialize_with_readme: true

3. Verify project was created:
   mcp__gitlab__get_project
   - project_id: "mcps/my-new-project"

4. Set up initial structure (optional):
   mcp__gitlab__create_file
   - project_id: "mcps/my-new-project"
   - file_path: ".gitlab-ci.yml"
   - branch: "main"
   - content: <CI/CD configuration>
   - commit_message: "Add CI/CD configuration"
```

## Best Practices

1. **Always use project paths when possible** - More readable than numeric IDs
2. **Check context first** - Use `get_current_context` to verify connection
3. **Use pagination** - Set `per_page` for large result sets
4. **Filter early** - Use parameters like `state`, `labels`, `milestone` to reduce data
5. **Handle errors gracefully** - Check for required permissions and valid references
6. **Use IIDs not IDs** - Issues and MRs use Internal IDs (IID), not global IDs
7. **Reference branches explicitly** - Use `ref` parameter to specify branch/tag

## Troubleshooting

### Common Issues

1. **"Project not found"**
   - Verify project path format: `group/project` or use numeric ID
   - Check user has access to the project

2. **"401 Unauthorized"**
   - Verify GitLab token is valid and not expired
   - Check token has required scopes (api, read_api, write_repository, etc.)

3. **"404 Not Found" for issues/MRs**
   - Use IID (internal ID), not global ID
   - IIDs are per-project sequential numbers

4. **Pipeline/Job not starting**
   - Check project has CI/CD configured (.gitlab-ci.yml)
   - Verify runners are available for the project

5. **Rate limiting**
   - GitLab has API rate limits (varies by plan)
   - Space out requests or use pagination efficiently

## Reference

### Tool Naming Convention
All GitLab MCP tools follow the pattern:
```
mcp__gitlab__<action>_<resource>
```

Examples:
- `mcp__gitlab__get_project`
- `mcp__gitlab__list_merge_requests`
- `mcp__gitlab__create_issue`

### Parameter Types
- **string**: Text values, project paths, branch names
- **integer**: Numeric IDs (project ID, issue IID, user ID)
- **boolean**: true/false flags
- **array**: Lists of values (labels, assignee_ids)
- **object**: Complex structures (pipeline variables)

### Date Format
When dates are required: `YYYY-MM-DD` (ISO 8601 date format)
Example: `2025-10-24`

### Color Format
For labels: Hex color codes with `#` prefix
Example: `#FF0000` (red)

## Quick Reference

Most commonly used operations:
1. `list_projects` - Find available projects
2. `get_project` - Get project details
3. `create_project` - Create a new project
4. `list_repository_tree` - Browse files
5. `get_file_contents` - Read files
6. `list_issues` - View issues
7. `list_merge_requests` - View MRs
8. `get_merge_request_changes` - Review MR diff
9. `list_pipelines` - Check CI/CD status
10. `get_job_trace` - Debug failed jobs
11. `search_code` - Find code across repos

---

**Last Updated**: 2025-10-26
**MCP Server Version**: Compatible with gitlab-mcp v1.0+
