# Changelog

All notable changes to the GitLab MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional GitLab API coverage
- Performance optimization for large repositories
- Enhanced error messages and debugging tools
- WebSocket transport support

## [1.0.0] - 2026-01-10

### First Public Release

This is the first public release of gitlab-mcp on PyPI and GitHub. The project has been in production use internally and is now available for the broader community.

### Added

#### Meta-Tools & Slim Mode
- **3 meta-tools** for dynamic tool discovery and execution
  - `discover_tools` - List available tools by category (95% context reduction)
  - `get_tool_schema` - Get full JSON schema for any tool
  - `execute_tool` - Execute any tool by name with arguments
- **Slim mode** (`--mode slim`) reduces LLM context usage by loading only meta-tools

#### Streamable HTTP Transport
- **HTTP transport** (`--transport http`) for remote clients
- SSE streaming support via Starlette and uvicorn
- Configurable host and port (`--host`, `--port`)

#### MCP Prompts (14 prompts)
- Core workflows: create-mr-from-issue, review-pipeline-failure, project-health-check, release-checklist
- Code review: code-review-prep, security-scan-review
- Maintenance: stale-mr-cleanup, branch-cleanup, failed-jobs-summary
- Deployment: deployment-readiness
- Orchestration: parallel-pipeline-check, bulk-mr-review, multi-project-deploy

#### MCP Resources (13 resources)
- Static resources: gitlab://projects, gitlab://user/current, gitlab://groups
- Template resources for projects, issues, MRs, pipelines, branches, files

### Changed
- Package name: `python-gitlab-mcp` (PyPI)
- Version scheme changed from CalVer to SemVer
- Development status upgraded from Beta to Production/Stable

### Metrics
- **87 MCP tools** (full mode) or **3 meta-tools** (slim mode)
- **14 MCP prompts** for GitLab workflows
- **13 MCP resources** (static and template-based)
- **1257 tests** passing (100% pass rate)
- **84% code coverage**
- **Zero mypy errors** (strict mode)
- **Zero ruff errors**

## [0.1.0] - 2025-10-24

### 🎉 Initial Release - Production-Ready MCP Server

This is the first production-ready release of the GitLab MCP Server, featuring 67 tools, 700+ tests, and 79% code coverage. Built with strict Test-Driven Development (TDD) practices.

### Added

#### Core Infrastructure
- **MCP Server** implementation with stdio transport
- **Configuration system** supporting environment variables, JSON files, and Claude Code integration
- **GitLab API client** wrapper with comprehensive error handling
- **Type-safe** implementation with full mypy compliance
- **Async/await** throughout for non-blocking operations

#### Repository Tools (13 tools)
- `search_repositories` - Search for GitLab repositories
- `get_repository` - Get repository details
- `list_repository_tree` - Browse repository file tree
- `get_file_content` - Read file contents
- `search_code` - Search code across repositories
- `list_branches` - List repository branches
- `get_branch` - Get branch details
- `create_branch` - Create new branch
- `delete_branch` - Delete branch
- `list_commits` - List commit history
- `get_commit` - Get commit details
- `compare_branches` - Compare two branches
- `list_tags` - List repository tags

#### Issue Tools (10 tools)
- `list_issues` - List project issues
- `get_issue` - Get issue details
- `create_issue` - Create new issue
- `update_issue` - Update existing issue
- `close_issue` - Close issue
- `reopen_issue` - Reopen closed issue
- `add_issue_comment` - Add comment to issue
- `list_issue_comments` - List issue comments
- `add_issue_labels` - Add labels to issue
- `remove_issue_label` - Remove label from issue

#### Merge Request Tools (15 tools)
- `list_merge_requests` - List project merge requests
- `get_merge_request` - Get merge request details
- `create_merge_request` - Create new merge request
- `update_merge_request` - Update merge request
- `merge_merge_request` - Merge merge request
- `close_merge_request` - Close merge request
- `reopen_merge_request` - Reopen merge request
- `approve_merge_request` - Approve merge request
- `unapprove_merge_request` - Unapprove merge request
- `get_merge_request_changes` - Get MR changes/diffs
- `list_merge_request_comments` - List MR comments
- `add_merge_request_comment` - Add comment to MR
- `list_merge_request_commits` - List MR commits
- `list_merge_request_pipelines` - List MR pipelines
- `assign_merge_request` - Assign reviewers to MR

#### CI/CD Pipeline Tools (11 tools)
- `list_pipelines` - List project pipelines
- `get_pipeline` - Get pipeline details
- `create_pipeline` - Trigger new pipeline
- `retry_pipeline` - Retry failed pipeline
- `cancel_pipeline` - Cancel running pipeline
- `delete_pipeline` - Delete pipeline
- `list_pipeline_jobs` - List pipeline jobs
- `get_job` - Get job details
- `retry_job` - Retry failed job
- `cancel_job` - Cancel running job
- `get_job_log` - Get job execution logs

#### Project Management Tools (8 tools)
- `list_projects` - List GitLab projects
- `get_project` - Get project details
- `create_project` - Create new project
- `update_project` - Update project settings
- `delete_project` - Delete project
- `archive_project` - Archive project
- `unarchive_project` - Unarchive project
- `list_project_members` - List project members

#### Security Tools (4 tools)
- `get_vulnerability_findings` - Get security vulnerabilities
- `list_security_reports` - List security scan reports
- `get_sast_report` - Get SAST scan results
- `get_dependency_scanning_report` - Get dependency scan results

#### Additional Tools (6 tools)
- `list_milestones` - List project milestones
- `get_milestone` - Get milestone details
- `create_milestone` - Create milestone
- `list_labels` - List project labels
- `create_label` - Create label
- `search_users` - Search GitLab users

### Testing & Quality

#### Test Suite (700+ tests, 100% pass rate)
- **691 unit tests** with mocked dependencies for fast, isolated testing
- **9 integration tests** with real GitLab API for validation
- **16 E2E tests** validating full MCP protocol integration
- **79.14% code coverage** (exceeds 80% in core modules)

#### Code Quality
- **Zero mypy errors** - Full type safety
- **Zero ruff errors** - Strict linting compliance
- **Black formatted** - Consistent code style
- **Comprehensive docstrings** - Every module, class, and function

### Documentation

#### User Documentation
- **Installation Guide** (`docs/user/installation.md`) - Complete setup instructions
- **Configuration Guide** (`docs/user/configuration.md`) - Configuration options and best practices
- **Usage Examples** (`docs/user/usage_examples.md`) - Real-world usage scenarios
- **Troubleshooting Guide** (`docs/user/troubleshooting.md`) - Common issues and solutions

#### API Reference
- **Tools Reference** (`docs/api/tools_reference.md`) - Complete documentation for all 67 tools
- **GitLab API Mapping** (`docs/api/gitlab_api_mapping.md`) - GitLab API endpoint mapping

#### Architecture
- **System Overview** (`docs/architecture/system_overview.md`) - High-level architecture
- **Interfaces** (`docs/architecture/interfaces.md`) - Interface contracts
- **Data Flow** (`docs/architecture/data_flow.md`) - Data flow diagrams

#### Development
- **Development Guide** (`CLAUDE.md`) - TDD workflow and ground rules
- **Product Requirements** (`docs/gitlab-mcp-server-prd.md`) - Complete feature specifications
- **Session Management** (`docs/session_management/`) - Development session logs (37 sessions)

### Security
- Personal Access Token (PAT) authentication
- Environment-based credential management
- SSL/TLS verification with custom certificate support
- Secure credential storage using `.env` files (gitignored)
- Token scope validation and error handling

### Performance
- Async/await throughout for non-blocking operations
- Efficient pagination for large datasets
- Configurable timeouts and retry logic
- Connection pooling via httpx
- Smart rate limiting awareness

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Development Process

This release was built over **37 development sessions** following strict Test-Driven Development (TDD):

#### Phase 1: Foundation (Sessions 1-10)
- MCP server implementation
- Configuration management
- GitLab API client
- Authentication system

#### Phase 2: Repository & Issues (Sessions 11-20)
- Repository operations
- Issue management
- Search functionality

#### Phase 3: Merge Requests & Pipelines (Sessions 21-30)
- Merge request workflows
- CI/CD pipeline monitoring
- Job execution and artifacts

#### Phase 4: Advanced Features (Sessions 31-34)
- Security scanning integration
- Project management tools
- MCP tool layer integration

#### Phase 5: Testing & Documentation (Sessions 35-37)
- E2E integration tests
- Integration tests with real GitLab API
- Complete user documentation
- Tools reference documentation
- Final polish and release prep

### Metrics
- **Total Lines of Code**: ~15,000
- **Test Files**: 150+
- **Documentation Files**: 50+
- **Development Sessions**: 37
- **Total Development Time**: ~100 hours

## Version History

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

### Release Process

1. Update version in `pyproject.toml`
2. Update this CHANGELOG with release notes
3. Run full test suite (must pass 100%)
4. Verify code coverage (must be ≥80%)
5. Run type checking (must have 0 errors)
6. Run linting (must have 0 errors)
7. Create git tag: `git tag -a v0.1.0 -m "Release v0.1.0"`
8. Push to GitLab: `git push origin main --tags`
9. Create GitLab release with notes
10. Publish to PyPI (when ready)

---

[Unreleased]: https://github.com/wadew/gitlab-mcp/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/wadew/gitlab-mcp/releases/tag/v1.0.0
[0.1.0]: https://github.com/wadew/gitlab-mcp/releases/tag/v0.1.0
