# GitLab MCP Server

A Model Context Protocol (MCP) server that enables AI tools like Claude Code to interact with self-hosted GitLab instances.

## Status

**Version**: 0.1.0 (Alpha - In Development)

**Current Phase**: Phase 0 - Project Setup

**Test Coverage**: N/A (no code yet)

## Overview

The GitLab MCP Server provides a standardized way for AI assistants to:
- Search and browse repository code
- Manage issues and merge requests
- Monitor and control CI/CD pipelines
- Perform project management tasks
- Access security scanning results

This project follows **strict Test-Driven Development (TDD)** with 80% minimum code coverage and 100% test pass requirements.

## Features (Planned)

### Phase 1: Foundation
- MCP server implementation with stdio transport
- Configuration management (PAT authentication)
- GitLab API client wrapper
- Core context tools

### Phase 2: Repository & Issues
- Repository operations (search, browse, commits, branches)
- Issue management (CRUD operations, comments)
- Basic search functionality

### Phase 3: Merge Requests & Pipelines
- Merge request operations (create, review, approve, merge)
- CI/CD pipeline monitoring and control
- Job execution and artifact management

### Phase 4: Advanced Features
- Project management tools
- Security scanning integration
- Wikis and snippets
- Release management
- User and group operations

## Requirements

- Python 3.9+
- Self-hosted GitLab instance (CE or EE, v15.0+)
- GitLab Personal Access Token with appropriate scopes

## Installation

**Note**: Not yet ready for installation. Coming soon!

```bash
# Future installation method
pip install gitlab-mcp-server
```

## Configuration

**Note**: Configuration system not yet implemented.

```bash
# Set environment variables
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"

# Or create config file
cat > ~/.gitlab-mcp.json << EOF
{
  "gitlab_url": "https://gitlab.example.com",
  "default_project": "mygroup/myproject",
  "timeout": 30,
  "verify_ssl": true
}
EOF
```

## Usage

**Note**: Not yet functional. Coming soon!

```bash
# Start server
gitlab-mcp-server

# Or configure in Claude Code settings
# See docs/user/configuration.md (when available)
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/gitlab-mcp-server.git
cd gitlab-mcp-server

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment with uv (faster than venv)
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies with uv
uv pip install -e ".[dev]"
```

### Development Ground Rules

This project follows **strict TDD**:
1. ✅ Always write tests first (Red)
2. ✅ Write minimal code to pass (Green)
3. ✅ Refactor while keeping tests green
4. ✅ Maintain 80%+ code coverage
5. ✅ 100% test pass rate required
6. ✅ Cannot proceed to next phase without meeting criteria

See [CLAUDE.md](CLAUDE.md) for complete development guidelines.

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/gitlab_mcp --cov-report=term-missing

# Run specific test types
pytest tests/unit/ -v -m unit
pytest tests/integration/ -v -m integration
pytest tests/e2e/ -v -m e2e

# Type checking
mypy src/gitlab_mcp

# Code formatting
black src/ tests/

# Linting
ruff check src/ tests/
```

### Project Structure

```
gitlab_mcp/
├── CLAUDE.md                    # Development ground rules
├── next_session_plan.md         # Current state & next steps
├── docs/                        # Documentation
│   ├── session_management/      # Session logs & audit trail
│   ├── architecture/            # System design docs
│   ├── api/                     # API reference
│   ├── development/             # Developer guides
│   ├── user/                    # User documentation
│   └── phases/                  # Phase planning
├── src/gitlab_mcp/              # Source code
│   ├── server.py                # Main MCP server
│   ├── config/                  # Configuration management
│   ├── client/                  # GitLab API client
│   ├── tools/                   # MCP tool implementations
│   ├── schemas/                 # Pydantic models
│   └── utils/                   # Utilities
└── tests/                       # Test suite
    ├── unit/                    # Unit tests
    ├── integration/             # Integration tests
    └── e2e/                     # End-to-end tests
```

## Documentation

- **PRD**: [docs/gitlab-mcp-server-prd.md](docs/gitlab-mcp-server-prd.md)
- **Architecture**: [docs/architecture/system_overview.md](docs/architecture/system_overview.md)
- **Interfaces**: [docs/architecture/interfaces.md](docs/architecture/interfaces.md)
- **Development Guide**: [CLAUDE.md](CLAUDE.md)
- **Session Management**: [docs/session_management/README.md](docs/session_management/README.md)

## Contributing

We follow TDD strictly. Before contributing:

1. Read [CLAUDE.md](CLAUDE.md) for ground rules
2. Check [next_session_plan.md](next_session_plan.md) for current work
3. Write tests first
4. Ensure 80%+ coverage and 100% test pass rate
5. Update documentation

## License

MIT License - See LICENSE file for details

## Project Phases

- [x] Phase 0: Project Setup & Documentation
- [ ] Phase 1: Foundation (Server, Config, Client, Auth)
- [ ] Phase 2: Repository & Issues Tools
- [ ] Phase 3: Merge Requests & Pipelines Tools
- [ ] Phase 4: Advanced Features

## Support

- **Issues**: https://github.com/yourusername/gitlab-mcp-server/issues
- **Documentation**: https://github.com/yourusername/gitlab-mcp-server/tree/main/docs

---

**Built with strict TDD practices. 80% coverage minimum. 100% test pass rate required.**
