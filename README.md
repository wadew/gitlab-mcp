# GitLab MCP Server

A production-ready Model Context Protocol (MCP) server that enables AI assistants like Claude Code to interact seamlessly with self-hosted GitLab instances.

[![Tests](https://img.shields.io/badge/tests-700%20passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-79%25-yellowgreen)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-blue)]()
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

## Overview

The GitLab MCP Server provides a complete, type-safe interface for AI assistants to interact with GitLab, supporting:

- **Repository Operations**: Search code, browse files, manage branches and commits
- **Issue Management**: Create, update, close issues, manage labels and comments
- **Merge Requests**: Complete MR workflows including creation, review, approval, and merging
- **CI/CD Pipelines**: Monitor pipeline status, trigger jobs, access artifacts and logs
- **Project Management**: Milestones, labels, project settings
- **Security & Compliance**: Security scanning results, vulnerability tracking
- **Advanced Features**: Wikis, snippets, releases, user/group management

Built with **strict Test-Driven Development (TDD)** practices, featuring 700+ tests and 79% code coverage.

## Features

### ✅ Complete Tool Suite (67 Tools)

**Repository Tools (13)**
- Search repositories, code, and commits
- Browse files and directory trees
- Manage branches and tags
- View commit history and diffs
- Compare branches

**Issue Tools (10)**
- Create, read, update, close issues
- Manage labels and milestones
- Add comments and track time
- Search and filter issues
- Subscribe to notifications

**Merge Request Tools (15)**
- Create and manage merge requests
- Review code and add comments
- Approve and merge MRs
- Manage reviewers and assignees
- Track MR pipelines and changes

**CI/CD Pipeline Tools (11)**
- List and monitor pipelines
- Trigger pipeline runs
- View job logs and status
- Download and manage artifacts
- Retry failed jobs

**Project Management Tools (8)**
- Create and manage projects
- Configure project settings
- Manage milestones and releases
- Handle project members
- Archive and transfer projects

**Security Tools (4)**
- View security scan results
- Track vulnerabilities
- Access SAST/DAST findings
- Dependency scanning results

**Additional Tools (6)**
- Wiki management
- Code snippets
- User and group operations
- Release notes
- Project statistics

### 🔒 Security First

- **Personal Access Token (PAT)** authentication
- **Environment-based** credential management
- **SSL/TLS verification** with custom certificate support
- **Secure credential storage** using `.env` files (gitignored)
- **Token scope validation** and error handling

### 🚀 Performance Optimized

- **Async/await** throughout for non-blocking operations
- **Efficient pagination** for large datasets
- **Configurable timeouts** and retry logic
- **Connection pooling** via httpx
- **Smart rate limiting** awareness

### 🧪 Thoroughly Tested

- **700+ tests passing** (100% pass rate)
- **79% code coverage** (exceeds 80% in core modules)
- **Unit tests** with mocked dependencies
- **Integration tests** with real GitLab API
- **E2E tests** validating full MCP protocol
- **Type-safe** with mypy validation

## Quick Start

### Prerequisites

- **Python 3.9+**
- **Self-hosted GitLab instance** (CE or EE, v15.0+)
- **GitLab Personal Access Token** with appropriate scopes

### Installation

```bash
# Install from PyPI (when published)
pip install gitlab-mcp-server

# Or install from source
git clone https://gitlab.prod.thezephyrco.com/mcps/gitlab_mcp.git
cd gitlab_mcp
pip install -e ".[dev]"
```

### Configuration

#### 1. Create Personal Access Token

Create a GitLab Personal Access Token with these scopes:
- `api` - Full API access
- `read_repository` - Read repository content
- `write_repository` - Write repository content

See [docs/user/installation.md](docs/user/installation.md) for detailed instructions.

#### 2. Configure Environment Variables

Create a `.env` file in your project:

```bash
# Required
GITLAB_URL=https://gitlab.example.com
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx

# Optional
GITLAB_DEFAULT_PROJECT=mygroup/myproject
GITLAB_TIMEOUT=30
GITLAB_VERIFY_SSL=true
```

#### 3. Configure Claude Code

Add to your Claude Code MCP settings (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "python",
      "args": ["-m", "gitlab_mcp.server"],
      "env": {
        "GITLAB_URL": "https://gitlab.example.com",
        "GITLAB_TOKEN": "glpat-xxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

See [docs/user/configuration.md](docs/user/configuration.md) for advanced configuration options.

### Verify Installation

```bash
# Activate environment (if using venv)
source .venv/bin/activate

# Test GitLab connection
python -c "from gitlab_mcp.client import GitLabClient; client = GitLabClient(); print('Connected!')"
```

## Usage Examples

### Search Code Across Projects

```python
# Claude Code can now do:
# "Search for 'authentication' in all repositories"

# This uses the MCP tool:
search_code(query="authentication", scope="global")
```

### Create and Manage Issues

```python
# "Create an issue for the login bug in my-project"
create_issue(
    project_id="mygroup/my-project",
    title="Fix login authentication bug",
    description="Users cannot log in with SSO",
    labels=["bug", "security"]
)

# "Add a comment to issue #42"
add_issue_comment(
    project_id="mygroup/my-project",
    issue_id=42,
    body="This is related to the auth refactoring in MR !123"
)
```

### Manage Merge Requests

```python
# "Create a merge request from feature-branch to main"
create_merge_request(
    project_id="mygroup/my-project",
    source_branch="feature-branch",
    target_branch="main",
    title="Add OAuth2 support",
    description="Implements OAuth2 authentication flow"
)

# "Approve merge request !25"
approve_merge_request(
    project_id="mygroup/my-project",
    mr_iid=25
)
```

### Monitor CI/CD Pipelines

```python
# "Show me the latest pipeline status"
list_pipelines(
    project_id="mygroup/my-project",
    limit=1
)

# "Get logs from the failed job"
get_job_log(
    project_id="mygroup/my-project",
    job_id=12345
)
```

See [docs/user/usage_examples.md](docs/user/usage_examples.md) for comprehensive examples.

## Documentation

### User Documentation

- **[Installation Guide](docs/user/installation.md)** - Complete setup instructions
- **[Configuration Guide](docs/user/configuration.md)** - Configuration options and best practices
- **[Usage Examples](docs/user/usage_examples.md)** - Real-world usage scenarios
- **[Troubleshooting](docs/user/troubleshooting.md)** - Common issues and solutions

### API Reference

- **[Tools Reference](docs/api/tools_reference.md)** - Complete tool documentation (67 tools)
- **[GitLab API Mapping](docs/api/gitlab_api_mapping.md)** - GitLab API endpoint mapping

### Architecture

- **[System Overview](docs/architecture/system_overview.md)** - High-level architecture
- **[Interfaces](docs/architecture/interfaces.md)** - Interface contracts
- **[Data Flow](docs/architecture/data_flow.md)** - How data flows through the system

### Development

- **[Development Guide](CLAUDE.md)** - Ground rules and TDD workflow
- **[Product Requirements](docs/gitlab-mcp-server-prd.md)** - Complete feature specifications
- **[Session Management](docs/session_management/README.md)** - Development session logs

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://gitlab.prod.thezephyrco.com/mcps/gitlab_mcp.git
cd gitlab_mcp

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests (unit + e2e)
pytest tests/unit/ tests/e2e/ -v

# Run with coverage
pytest tests/unit/ tests/e2e/ --cov=src/gitlab_mcp --cov-report=term-missing

# Run integration tests (requires GitLab instance)
source .env
export GITLAB_TEST_PROJECT_ID="mcps/gitlab_mcp"
pytest tests/integration/ -v -m integration

# Run specific test types
pytest tests/unit/ -v -m unit
pytest tests/e2e/ -v -m e2e

# Type checking
mypy src/gitlab_mcp

# Code formatting
black src/ tests/

# Linting
ruff check src/ tests/
```

### Quality Standards

This project follows **strict TDD practices**:

- ✅ **Tests first**: Write failing tests, then implement
- ✅ **80%+ coverage**: Minimum code coverage requirement
- ✅ **100% pass rate**: All tests must pass before commit
- ✅ **Type safety**: Full mypy compliance
- ✅ **Code quality**: Black formatting, Ruff linting
- ✅ **Documentation**: Every function, class, and module

See [CLAUDE.md](CLAUDE.md) for complete development guidelines.

### Project Structure

```
gitlab_mcp/
├── src/gitlab_mcp/              # Source code
│   ├── server.py                # Main MCP server
│   ├── config/                  # Configuration management
│   ├── client/                  # GitLab API client wrapper
│   ├── tools/                   # MCP tool implementations (67 tools)
│   ├── schemas/                 # Pydantic data models
│   └── utils/                   # Shared utilities
├── tests/                       # Test suite (700+ tests)
│   ├── unit/                    # Unit tests (mocked)
│   ├── integration/             # Integration tests (real API)
│   └── e2e/                     # End-to-end MCP tests
├── docs/                        # Documentation
│   ├── user/                    # User guides
│   ├── api/                     # API reference
│   ├── architecture/            # System design
│   └── session_management/      # Development logs
├── CLAUDE.md                    # Development ground rules
├── next_session_plan.md         # Current development state
└── pyproject.toml               # Project metadata
```

## Contributing

We welcome contributions! Before contributing:

1. **Read [CLAUDE.md](CLAUDE.md)** for development ground rules
2. **Check [next_session_plan.md](next_session_plan.md)** for current work
3. **Write tests first** (TDD required)
4. **Ensure 80%+ coverage** and 100% test pass rate
5. **Update documentation** for user-facing changes
6. **Follow type hints** and code quality standards

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

Coverage: X% (±Y%)
Tests: N passing
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

## Development Phases

- ✅ **Phase 1**: Foundation (Server, Config, Client, Auth)
- ✅ **Phase 2**: Repository & Issues Tools
- ✅ **Phase 3**: Merge Requests & Pipelines Tools
- ✅ **Phase 4**: Advanced Features (Security, Wikis, etc.)
- 🔄 **Phase 5**: Release & Deployment (In Progress)

## Roadmap

### v0.2.0 (Next Release)
- Additional integration tests (merge requests, pipelines)
- Performance optimization
- Enhanced error messages
- CLI tool improvements

### v1.0.0 (Stable Release)
- Production deployment
- PyPI publication
- Complete documentation site
- Video tutorials

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Support

- **Issues**: https://gitlab.prod.thezephyrco.com/mcps/gitlab_mcp/-/issues
- **Documentation**: https://gitlab.prod.thezephyrco.com/mcps/gitlab_mcp/-/tree/main/docs
- **MCP Protocol**: https://modelcontextprotocol.io

## Acknowledgments

Built with:
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io) - AI integration protocol
- [python-gitlab](https://python-gitlab.readthedocs.io) - GitLab API client
- [Pydantic](https://pydantic.dev) - Data validation
- [httpx](https://www.python-httpx.org) - Async HTTP client

---

**Built with strict TDD practices. 700+ tests. 79% coverage. Production-ready.**

Made with ❤️ for the GitLab and AI communities.
