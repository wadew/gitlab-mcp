# IBM ContextForge Integration

This guide explains how to integrate the GitLab MCP server with IBM ContextForge, a centralized MCP server gateway for federating multiple MCP servers.

## Overview

The GitLab MCP server supports two transport modes for ContextForge integration:

| Mode | Command | Description |
|------|---------|-------------|
| **Streamable HTTP** | `--transport http` | Modern MCP transport for HTTP/HTTPS connections |
| **stdio** | `--transport stdio` | Traditional stdin/stdout (default) |

For ContextForge, use **Streamable HTTP transport**.

## Quick Start

### 1. Start the Server with HTTP Transport

```bash
# Full mode (87 tools)
gitlab-mcp-server --transport http --host 0.0.0.0 --port 8000

# Slim mode (3 meta-tools, ~95% context savings)
gitlab-mcp-server --transport http --host 0.0.0.0 --port 8000 --mode slim
```

### 2. Register with ContextForge

In your ContextForge configuration (e.g., `context-forge-config.yaml`):

```yaml
servers:
  - name: gitlab
    url: http://your-host:8000/mcp
    transport: streamable-http
    description: "GitLab MCP Server - Repository, Pipeline, and Issue Management"
```

### 3. Verify Connection

```bash
# Test the MCP endpoint
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}'
```

## CLI Reference

```
gitlab-mcp-server [options]

Options:
  --transport {stdio,http}  Transport protocol (default: stdio)
  --host HOST               HTTP bind address (default: 127.0.0.1)
  --port PORT               HTTP port (default: 8000)
  --mode {full,slim}        Tool exposure mode (default: full)
```

### Transport Modes

| Transport | Use Case | ContextForge Compatible |
|-----------|----------|------------------------|
| `stdio` | CLI tools, Claude Desktop | No |
| `http` | Gateways, web services | **Yes** |

### Tool Modes

| Mode | Tools Exposed | Context Usage | Use Case |
|------|---------------|---------------|----------|
| `full` | 87 | ~22% | Direct tool access |
| `slim` | 3 | ~0.8% | Context-constrained clients |

## Slim Mode (Meta-Tools)

When running with `--mode slim`, the server exposes only 3 meta-tools:

### 1. `discover_tools`
Lists available tools by category.

```json
// Request
{"tool_name": "discover_tools", "arguments": {"category": "merge_requests"}}

// Response
{
  "category": "merge_requests",
  "description": "Merge request operations, approvals, and reviews",
  "tools": [
    {"name": "list_merge_requests", "description": "List merge requests for a project"},
    {"name": "get_merge_request", "description": "Get details of a specific merge request"},
    // ... 12 more tools
  ]
}
```

### 2. `get_tool_schema`
Get the full JSON schema for a specific tool.

```json
// Request
{"tool_name": "get_tool_schema", "arguments": {"tool_name": "list_merge_requests"}}

// Response
{
  "name": "list_merge_requests",
  "description": "List merge requests for a project",
  "category": "merge_requests",
  "inputSchema": {
    "type": "object",
    "properties": {
      "project_id": {"type": "string", "description": "..."},
      "state": {"type": "string", "description": "..."}
    },
    "required": ["project_id"]
  }
}
```

### 3. `execute_tool`
Execute any GitLab tool by name.

```json
// Request
{
  "tool_name": "execute_tool",
  "arguments": {
    "tool_name": "list_merge_requests",
    "arguments": {"project_id": "my-org/my-repo", "state": "opened"}
  }
}

// Response
{
  "merge_requests": [
    {"iid": 123, "title": "Add feature X", "state": "opened", ...}
  ]
}
```

## Tool Categories

The GitLab MCP server organizes 87 tools into 12 categories:

| Category | Tools | Description |
|----------|-------|-------------|
| `context` | 1 | Server and user context |
| `repositories` | 16 | Files, branches, commits, tags |
| `issues` | 8 | Issue CRUD and comments |
| `merge_requests` | 14 | MR operations, approvals, reviews |
| `pipelines` | 14 | CI/CD pipelines and jobs |
| `projects` | 10 | Project management, milestones |
| `labels` | 4 | Label management |
| `wikis` | 5 | Wiki page management |
| `snippets` | 5 | Code snippet management |
| `releases` | 5 | Release management |
| `users` | 3 | User info and search |
| `groups` | 3 | Group info and members |

## Environment Variables

Ensure these are set before starting the server:

```bash
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="your-personal-access-token"
```

See [Configuration Guide](./configuration.md) for all options.

## Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN pip install python-gitlab-mcp

ENV GITLAB_URL="https://gitlab.example.com"
ENV GITLAB_TOKEN=""

EXPOSE 8000

CMD ["gitlab-mcp-server", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t gitlab-mcp-server .
docker run -p 8000:8000 -e GITLAB_TOKEN=your-token gitlab-mcp-server
```

## Troubleshooting

### Connection refused
Ensure the server is running and accessible:
```bash
curl http://localhost:8000/mcp
```

### Authentication errors
Check your GitLab token:
```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" https://gitlab.example.com/api/v4/user
```

### Missing session ID error
This is expected for initial connections. ContextForge handles session management automatically.

## See Also

- [IBM ContextForge Documentation](https://github.com/IBM/mcp-context-forge)
- [Installation Guide](./installation.md)
- [Configuration Guide](./configuration.md)
- [Troubleshooting](./troubleshooting.md)
