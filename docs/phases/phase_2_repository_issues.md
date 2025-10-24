# Phase 2: Repository & Issues Tools

**Status**: In Progress
**Started**: 2025-10-23 (Session 006)
**Estimated Duration**: 8-10 sessions (~15-20 hours)

---

## Overview

Phase 2 focuses on implementing the core GitLab repository operations and issues management tools. This is the foundation for user-facing GitLab interactions through the MCP server.

### Goals
1. ✅ Implement all repository operation tools (REPO-001 through REPO-014)
2. ✅ Implement all issues management tools (ISSUE-001 through ISSUE-009)
3. ✅ Add labels and milestones support
4. ✅ Maintain ≥80% code coverage
5. ✅ 100% test pass rate
6. ✅ Setup integration testing framework

---

## Repository Tools (17 tools - 14 complete, 3 file operations pending)

### Priority 1: Read Operations (Session 006-007)
Basic read-only operations for repository inspection.

#### REPO-014: `get_repository`
**Description**: Get repository/project details and metadata
**GitLab API**: `GET /projects/:id`
**Inputs**:
- `project_id` (str | int, required): Project ID or path (namespace/project)
**Outputs**:
- Project metadata (name, description, URL, visibility, etc.)
- Repository stats (stars, forks, issues count)
- Default branch
- Created/updated timestamps

**Implementation**:
- `GitLabClient.get_project(project_id)` - Backend method
- `get_repository(client, project_id)` - MCP tool wrapper

**Tests**:
- [ ] `test_get_repository_by_project_id`
- [ ] `test_get_repository_by_path`
- [ ] `test_get_repository_includes_all_metadata`
- [ ] `test_get_repository_not_found`
- [ ] `test_get_repository_permission_denied`
- [ ] `test_get_repository_auth_error`

---

#### REPO-006: `list_branches`
**Description**: List all branches in a repository
**GitLab API**: `GET /projects/:id/repository/branches`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `search` (str, optional): Search pattern for branch names
- `page` (int, optional): Page number (default: 1)
- `per_page` (int, optional): Items per page (default: 20, max: 100)
**Outputs**:
- List of branches with:
  - Branch name
  - Commit SHA
  - Protected status
  - Default branch indicator

**Implementation**:
- `GitLabClient.list_branches(project_id, search, page, per_page)` - Backend method
- `list_branches(client, project_id, search, page, per_page)` - MCP tool wrapper

**Tests**:
- [ ] `test_list_branches_returns_all_branches`
- [ ] `test_list_branches_with_search_filter`
- [ ] `test_list_branches_pagination`
- [ ] `test_list_branches_identifies_default_branch`
- [ ] `test_list_branches_shows_protected_status`
- [ ] `test_list_branches_empty_repository`
- [ ] `test_list_branches_not_found`

---

#### REPO-007: `get_branch`
**Description**: Get details of a specific branch
**GitLab API**: `GET /projects/:id/repository/branches/:branch`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `branch` (str, required): Branch name
**Outputs**:
- Branch details:
  - Name
  - Commit SHA and message
  - Protected status
  - Can push status
  - Default branch indicator
  - Developers can push/merge status

**Implementation**:
- `GitLabClient.get_branch(project_id, branch)` - Backend method
- `get_branch(client, project_id, branch)` - MCP tool wrapper

**Tests**:
- [ ] `test_get_branch_returns_details`
- [ ] `test_get_branch_default_branch`
- [ ] `test_get_branch_protected_branch`
- [ ] `test_get_branch_not_found`
- [ ] `test_get_branch_invalid_project`

---

#### REPO-002: `get_file_contents`
**Description**: Get contents of a specific file from repository
**GitLab API**: `GET /projects/:id/repository/files/:file_path`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `file_path` (str, required): Path to file in repository
- `ref` (str, optional): Branch, tag, or commit SHA (default: default branch)
**Outputs**:
- File content (base64 decoded)
- File name
- File path
- Size
- Content SHA
- Last commit ID

**Implementation**:
- `GitLabClient.get_file_content(project_id, file_path, ref)` - Backend method
- `get_file_contents(client, project_id, file_path, ref)` - MCP tool wrapper

**Tests**:
- [ ] `test_get_file_contents_from_default_branch`
- [ ] `test_get_file_contents_from_specific_branch`
- [ ] `test_get_file_contents_from_tag`
- [ ] `test_get_file_contents_from_commit_sha`
- [ ] `test_get_file_contents_decodes_base64`
- [ ] `test_get_file_contents_not_found`
- [ ] `test_get_file_contents_binary_file`
- [ ] `test_get_file_contents_large_file`

---

#### REPO-003: `list_repository_tree`
**Description**: List files and directories in a repository
**GitLab API**: `GET /projects/:id/repository/tree`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `path` (str, optional): Path within repository (default: root)
- `ref` (str, optional): Branch, tag, or commit (default: default branch)
- `recursive` (bool, optional): Get recursive tree (default: False)
**Outputs**:
- List of tree entries:
  - Name
  - Type (blob/tree)
  - Path
  - Mode (file permissions)

**Implementation**:
- `GitLabClient.get_repository_tree(project_id, path, ref, recursive)` - Backend method
- `list_repository_tree(client, project_id, path, ref, recursive)` - MCP tool wrapper

**Tests**:
- [ ] `test_list_repository_tree_root`
- [ ] `test_list_repository_tree_subdirectory`
- [ ] `test_list_repository_tree_recursive`
- [ ] `test_list_repository_tree_specific_ref`
- [ ] `test_list_repository_tree_distinguishes_files_dirs`
- [ ] `test_list_repository_tree_empty_directory`
- [ ] `test_list_repository_tree_not_found`

---

### Priority 2: Commit Operations (Session 007-008)

#### REPO-004: `get_commit`
**Description**: Get details of a specific commit
**GitLab API**: `GET /projects/:id/repository/commits/:sha`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `sha` (str, required): Commit SHA
**Outputs**:
- Commit details:
  - SHA
  - Message (title and description)
  - Author (name, email, date)
  - Committer (name, email, date)
  - Parent SHAs
  - Stats (additions, deletions, total)

**Tests**:
- [ ] `test_get_commit_returns_details`
- [ ] `test_get_commit_includes_stats`
- [ ] `test_get_commit_not_found`
- [ ] `test_get_commit_invalid_sha`

---

#### REPO-005: `list_commits`
**Description**: List commits for a branch or repository
**GitLab API**: `GET /projects/:id/repository/commits`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `ref_name` (str, optional): Branch/tag name (default: default branch)
- `since` (str, optional): ISO 8601 date - only commits after this
- `until` (str, optional): ISO 8601 date - only commits before this
- `path` (str, optional): Filter by file path
- `page` (int, optional): Page number
- `per_page` (int, optional): Items per page (max: 100)
**Outputs**:
- List of commits with summary info

**Tests**:
- [ ] `test_list_commits_default_branch`
- [ ] `test_list_commits_specific_branch`
- [ ] `test_list_commits_with_date_range`
- [ ] `test_list_commits_for_specific_path`
- [ ] `test_list_commits_pagination`

---

#### REPO-013: `compare_branches`
**Description**: Compare two branches or commits
**GitLab API**: `GET /projects/:id/repository/compare`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `from` (str, required): Branch/tag/commit to compare from
- `to` (str, required): Branch/tag/commit to compare to
**Outputs**:
- Comparison details:
  - Commits in range
  - Diffs
  - Compare same/different

**Tests**:
- [ ] `test_compare_branches_returns_commits`
- [ ] `test_compare_branches_returns_diffs`
- [ ] `test_compare_branches_same_ref`
- [ ] `test_compare_branches_not_found`

---

### Priority 3: Write Operations (Session 008-009)

#### REPO-008: `create_branch`
**Description**: Create a new branch
**GitLab API**: `POST /projects/:id/repository/branches`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `branch` (str, required): New branch name
- `ref` (str, required): Source branch/tag/commit
**Outputs**:
- Created branch details

**Tests**:
- [ ] `test_create_branch_from_default`
- [ ] `test_create_branch_from_specific_ref`
- [ ] `test_create_branch_already_exists`
- [ ] `test_create_branch_invalid_name`
- [ ] `test_create_branch_permission_denied`

---

#### REPO-009: `delete_branch`
**Description**: Delete a branch
**GitLab API**: `DELETE /projects/:id/repository/branches/:branch`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `branch` (str, required): Branch name to delete
**Outputs**:
- Success confirmation

**Tests**:
- [ ] `test_delete_branch_success`
- [ ] `test_delete_branch_not_found`
- [ ] `test_delete_branch_default_branch_protected`
- [ ] `test_delete_branch_permission_denied`

---

### Priority 4: Tags & Search (Session 009-010)

#### REPO-010: `list_tags`
**Description**: List repository tags
**GitLab API**: `GET /projects/:id/repository/tags`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `order_by` (str, optional): "name", "updated" (default: "updated")
- `sort` (str, optional): "asc" or "desc" (default: "desc")
- `search` (str, optional): Search pattern
- `page` (int, optional): Page number
- `per_page` (int, optional): Items per page
**Outputs**:
- List of tags

**Tests**:
- [ ] `test_list_tags_all`
- [ ] `test_list_tags_with_search`
- [ ] `test_list_tags_sorted`
- [ ] `test_list_tags_pagination`

---

#### REPO-011: `get_tag`
**Description**: Get details of a specific tag
**GitLab API**: `GET /projects/:id/repository/tags/:tag_name`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `tag_name` (str, required): Tag name
**Outputs**:
- Tag details

**Tests**:
- [ ] `test_get_tag_returns_details`
- [ ] `test_get_tag_not_found`

---

#### REPO-012: `create_tag`
**Description**: Create a new tag
**GitLab API**: `POST /projects/:id/repository/tags`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `tag_name` (str, required): Tag name
- `ref` (str, required): Source commit SHA
- `message` (str, optional): Tag message
**Outputs**:
- Created tag details

**Tests**:
- [ ] `test_create_tag_success`
- [ ] `test_create_tag_with_message`
- [ ] `test_create_tag_already_exists`
- [ ] `test_create_tag_invalid_ref`

---

#### REPO-001: `search_code`
**Description**: Search for code across repositories
**GitLab API**: `GET /search?scope=blobs`
**Inputs**:
- `project_id` (str | int, optional): Limit to specific project
- `query` (str, required): Search query
- `page` (int, optional): Page number
- `per_page` (int, optional): Items per page
**Outputs**:
- Search results with file paths, content snippets

**Tests**:
- [ ] `test_search_code_finds_results`
- [ ] `test_search_code_in_specific_project`
- [ ] `test_search_code_pagination`
- [ ] `test_search_code_no_results`

---

### Priority 5: File Edit Operations (Session 018)

**Priority**: HIGH - Enables AI-assisted code editing workflows
**Added**: 2025-10-23 based on user request
**Implementation**: After Issues tools complete, before Phase 2 wrap

#### REPO-015: `create_file`
**Description**: Create a new file in repository with commit
**GitLab API**: `POST /projects/:id/repository/files/:file_path`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `file_path` (str, required): Full path to new file (URL-encoded)
- `branch` (str, required): Target branch name
- `content` (str, required): File content
- `commit_message` (str, required): Commit message
- `start_branch` (str, optional): Create new branch from this branch
- `author_email` (str, optional): Override commit author email
- `author_name` (str, optional): Override commit author name
- `encoding` (str, optional): 'text' or 'base64' (default: 'text')

**Outputs**:
- Created file details (path, branch, commit ID, web URL)

**Use Cases**:
- AI generates new source files
- Create configuration files
- Add documentation files

**Tests**:
- [ ] `test_create_file_success`
- [ ] `test_create_file_with_encoding`
- [ ] `test_create_file_on_new_branch`
- [ ] `test_create_file_already_exists_error`
- [ ] `test_create_file_invalid_path_error`

---

#### REPO-016: `update_file`
**Description**: Update existing file content with commit
**GitLab API**: `PUT /projects/:id/repository/files/:file_path`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `file_path` (str, required): Full path to file (URL-encoded)
- `branch` (str, required): Target branch name
- `content` (str, required): New file content
- `commit_message` (str, required): Commit message
- `last_commit_id` (str, optional): For conflict detection
- `start_branch` (str, optional): Create new branch from this branch
- `author_email` (str, optional): Override commit author email
- `author_name` (str, optional): Override commit author name
- `encoding` (str, optional): 'text' or 'base64' (default: 'text')

**Outputs**:
- Updated file details (path, branch, commit ID, web URL)

**Use Cases**:
- AI applies bug fixes
- Refactor code
- Update configuration values
- Fix linting issues

**Tests**:
- [ ] `test_update_file_success`
- [ ] `test_update_file_with_conflict_detection`
- [ ] `test_update_file_not_found_error`
- [ ] `test_update_file_conflict_error`

---

#### REPO-017: `delete_file`
**Description**: Delete a file from repository with commit
**GitLab API**: `DELETE /projects/:id/repository/files/:file_path`
**Inputs**:
- `project_id` (str | int, required): Project ID or path
- `file_path` (str, required): Full path to file (URL-encoded)
- `branch` (str, required): Target branch name
- `commit_message` (str, required): Commit message
- `last_commit_id` (str, optional): For conflict detection
- `start_branch` (str, optional): Create new branch from this branch

**Outputs**:
- Deletion confirmation (path, branch, commit ID)

**Use Cases**:
- Remove deprecated files
- Clean up temporary files
- Delete obsolete configurations

**Tests**:
- [ ] `test_delete_file_success`
- [ ] `test_delete_file_not_found_error`
- [ ] `test_delete_file_conflict_error`

---

## Issues Tools (9 tools)

### Priority 1: Basic CRUD (Session 011-012)

#### ISSUE-001: `create_issue`
#### ISSUE-002: `get_issue`
#### ISSUE-003: `update_issue`
#### ISSUE-004: `list_issues`
#### ISSUE-005: `close_issue`
#### ISSUE-006: `reopen_issue`

### Priority 2: Comments & Search (Session 012-013)

#### ISSUE-007: `add_issue_comment`
#### ISSUE-008: `list_issue_comments`
#### ISSUE-009: `search_issues`

---

## Labels & Milestones (Session 013-014)

- Labels CRUD operations
- Milestones CRUD operations

---

## GitLab Client Extensions

New methods to add to `src/gitlab_mcp/client/gitlab_client.py`:

```python
# Repository operations
def get_project(self, project_id: str | int) -> Any
def list_branches(self, project_id: str | int, search: Optional[str], page: int, per_page: int) -> list[Any]
def get_branch(self, project_id: str | int, branch: str) -> Any
def get_file_content(self, project_id: str | int, file_path: str, ref: str) -> Any
def get_repository_tree(self, project_id: str | int, path: str, ref: str, recursive: bool) -> list[Any]
def get_commit(self, project_id: str | int, sha: str) -> Any
def list_commits(self, project_id: str | int, ref_name: str, since: str, until: str, path: str, page: int, per_page: int) -> list[Any]
def compare_refs(self, project_id: str | int, from_ref: str, to_ref: str) -> Any
def create_branch(self, project_id: str | int, branch: str, ref: str) -> Any
def delete_branch(self, project_id: str | int, branch: str) -> None
def list_tags(self, project_id: str | int, order_by: str, sort: str, search: str, page: int, per_page: int) -> list[Any]
def get_tag(self, project_id: str | int, tag_name: str) -> Any
def create_tag(self, project_id: str | int, tag_name: str, ref: str, message: Optional[str]) -> Any
def search_code(self, query: str, project_id: Optional[str | int], page: int, per_page: int) -> list[Any]

# Issues operations
def create_issue(self, project_id: str | int, title: str, description: str, **kwargs) -> Any
def get_issue(self, project_id: str | int, issue_iid: int) -> Any
def update_issue(self, project_id: str | int, issue_iid: int, **kwargs) -> Any
def list_issues(self, project_id: str | int, **filters) -> list[Any]
def close_issue(self, project_id: str | int, issue_iid: int) -> Any
def reopen_issue(self, project_id: str | int, issue_iid: int) -> Any
def add_issue_note(self, project_id: str | int, issue_iid: int, body: str) -> Any
def list_issue_notes(self, project_id: str | int, issue_iid: int) -> list[Any]
def search_issues(self, query: str, project_id: Optional[str | int], **filters) -> list[Any]
```

---

## Testing Strategy

### Unit Tests
- Mock all GitLab API responses using python-gitlab mocking
- Test all error conditions (404, 403, 401, etc.)
- Test all input validation
- Test pagination logic
- Target: ≥85% coverage per module

### Integration Tests (NEW)
- Setup test GitLab project (or use gitlab.com public test project)
- Real API calls to verify behavior
- Test common workflows end-to-end
- Document setup process in `docs/development/integration_testing.md`

### Test Files Structure
```
tests/
├── unit/
│   ├── test_client/
│   │   └── test_gitlab_client.py (extended)
│   └── test_tools/
│       ├── test_repositories.py (NEW)
│       └── test_issues.py (NEW)
└── integration/ (NEW)
    ├── conftest.py
    ├── test_repository_operations.py
    └── test_issue_operations.py
```

---

## Quality Gates

Before completing Phase 2:
- [ ] All 23 tools implemented (14 repos + 9 issues)
- [ ] ≥80% code coverage overall
- [ ] 100% test pass rate
- [ ] 0 mypy type errors
- [ ] 0 ruff lint errors
- [ ] All code formatted with black
- [ ] Integration tests setup and passing
- [ ] Documentation complete:
  - [ ] `docs/api/tools_reference.md` updated
  - [ ] `docs/api/gitlab_api_mapping.md` updated
  - [ ] `docs/user/usage_examples.md` has Phase 2 examples
  - [ ] Integration test setup guide complete

---

## Session Breakdown

### Session 006 (Current)
- [ ] Create this planning document
- [ ] Start REPO-014: `get_repository` (TDD)
- [ ] Start REPO-006: `list_branches` (TDD)

### Session 007
- [ ] Complete REPO-006: `list_branches`
- [ ] REPO-007: `get_branch`
- [ ] REPO-002: `get_file_contents`

### Session 008
- [ ] REPO-003: `list_repository_tree`
- [ ] REPO-004: `get_commit`
- [ ] REPO-005: `list_commits`

### Session 009
- [ ] REPO-013: `compare_branches`
- [ ] REPO-008: `create_branch`
- [ ] REPO-009: `delete_branch`

### Session 010
- [ ] REPO-010: `list_tags`
- [ ] REPO-011: `get_tag`
- [ ] REPO-012: `create_tag`
- [ ] REPO-001: `search_code`

### Sessions 011-014
- [ ] Issues tools implementation
- [ ] Labels and milestones
- [ ] Integration testing setup

---

## Key Decisions

### Architecture
- **Tool organization**: One file per toolset (`repositories.py`, `issues.py`)
- **Client method pattern**: One client method per API endpoint
- **Error handling**: Convert all python-gitlab exceptions to custom exceptions
- **Async all the way**: All tools are async functions

### Testing
- **TDD mandatory**: RED → GREEN → REFACTOR for every feature
- **Mock strategy**: Use unittest.mock for python-gitlab client
- **Integration tests**: Separate from unit tests, require real GitLab instance

### Data Models
- **Pydantic for validation**: Input validation using Pydantic models
- **Type safety**: Full type hints on all functions
- **Optional fields**: Use `Optional[str]` not `str | None`

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Complex file operations | Medium | Start with read-only, add writes incrementally |
| Integration test setup | Medium | Document thoroughly, use gitlab.com if needed |
| Binary file handling | Low | Handle common cases first, edge cases later |
| API rate limiting | Low | Add retry logic, monitor during integration tests |
| Large file handling | Low | Test with representative sizes, add size warnings |

---

**Last Updated**: 2025-10-23 (Session 006)
**Next Update**: End of Session 006
