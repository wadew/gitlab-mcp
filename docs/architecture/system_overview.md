# System Overview - GitLab MCP Server

## Architecture

The GitLab MCP Server is a Python-based Model Context Protocol server that enables AI tools like Claude Code to interact with self-hosted GitLab instances.

### High-Level Architecture

```
┌─────────────────────────────────────┐
│         MCP Host                    │
│    (Claude Code, Cursor, etc.)      │
└────────────────┬────────────────────┘
                 │
                 │ MCP Protocol
                 │ (JSON-RPC 2.0 over stdio)
                 │
┌────────────────▼────────────────────┐
│     GitLab MCP Server (Python)      │
│  ┌──────────────────────────────┐   │
│  │   MCP Protocol Handler       │   │
│  │   (Tool Discovery, Routing)  │   │
│  └──────────┬───────────────────┘   │
│             │                        │
│  ┌──────────▼───────────────────┐   │
│  │      Tool Implementations    │   │
│  │  - Context   - Repos         │   │
│  │  - Issues    - Merge Requests│   │
│  │  - Pipelines - Projects      │   │
│  └──────────┬───────────────────┘   │
│             │                        │
│  ┌──────────▼───────────────────┐   │
│  │    GitLab API Client         │   │
│  │  (python-gitlab wrapper)     │   │
│  └──────────┬───────────────────┘   │
│             │                        │
│  ┌──────────▼───────────────────┐   │
│  │  Configuration & Auth        │   │
│  │  (PAT, Settings, Validation) │   │
│  └──────────────────────────────┘   │
└─────────────────┬───────────────────┘
                  │
                  │ HTTPS (GitLab REST API v4)
                  │
┌─────────────────▼───────────────────┐
│   Self-Hosted GitLab Instance       │
│   (CE or EE, v15.0+)                │
└─────────────────────────────────────┘
```

## Component Breakdown

### 1. MCP Protocol Layer
**Location**: `src/gitlab_mcp/server.py`

**Responsibilities**:
- Initialize MCP server with stdio transport
- Handle protocol handshake
- Tool discovery and registration
- Route tool calls to appropriate handlers
- Format responses per MCP specification

**Key Classes/Functions**:
- `GitLabMCPServer` - Main server class
- `serve()` - Entry point for starting server

### 2. Configuration Layer
**Location**: `src/gitlab_mcp/config/`

**Responsibilities**:
- Load configuration from environment variables and files
- Validate GitLab URL and token
- Manage default settings
- Provide configuration to other components

**Key Modules**:
- `settings.py` - Configuration schema and loading
- `validation.py` - Input validation and sanitization

**Configuration Sources** (in order of precedence):
1. Environment variables (`GITLAB_URL`, `GITLAB_TOKEN`, etc.)
2. Config file (`~/.gitlab-mcp.json` or `./.gitlab-mcp.json`)
3. Default values

### 3. GitLab API Client Layer
**Location**: `src/gitlab_mcp/client/`

**Responsibilities**:
- Initialize python-gitlab client
- Authenticate using PAT
- Provide typed API methods
- Handle rate limiting
- Convert GitLab API errors to MCP-friendly errors

**Key Modules**:
- `gitlab_client.py` - Wrapper around python-gitlab
- `exceptions.py` - Custom exception classes

**Error Handling**:
- HTTP 401 → `AuthenticationError`
- HTTP 403 → `PermissionError`
- HTTP 404 → `NotFoundError`
- HTTP 422 → `ValidationError`
- HTTP 429 → `RateLimitError`
- HTTP 500+ → `GitLabServerError`

### 4. Tools Layer
**Location**: `src/gitlab_mcp/tools/`

**Responsibilities**:
- Implement each MCP tool
- Define tool schemas (name, description, input schema)
- Validate tool inputs
- Call GitLab API client
- Format responses

**Organization**:
```
tools/
├── __init__.py              # Tool registry
├── base.py                  # Base tool class
├── context/                 # Server/user context tools
│   ├── __init__.py
│   └── info.py
├── repos/                   # Repository operation tools
│   ├── __init__.py
│   ├── search.py
│   ├── files.py
│   ├── commits.py
│   └── branches.py
├── issues/                  # Issue management tools
│   ├── __init__.py
│   ├── crud.py
│   └── comments.py
├── merge_requests/          # MR operation tools
│   ├── __init__.py
│   ├── crud.py
│   ├── changes.py
│   └── approvals.py
└── pipelines/              # CI/CD tools
    ├── __init__.py
    ├── pipelines.py
    └── jobs.py
```

**Base Tool Pattern**:
```python
class BaseTool:
    name: str
    description: str
    input_schema: dict

    def execute(self, **kwargs) -> dict:
        """Execute tool and return result"""
        pass
```

### 5. Schemas Layer
**Location**: `src/gitlab_mcp/schemas/`

**Responsibilities**:
- Define Pydantic models for tool inputs/outputs
- Define GitLab API response models
- Provide JSON schema generation for MCP tool schemas

**Key Modules**:
- `tool_schemas.py` - MCP tool input/output schemas
- `gitlab_models.py` - GitLab API response models (if needed)

### 6. Utilities Layer
**Location**: `src/gitlab_mcp/utils/`

**Responsibilities**:
- Logging configuration
- Rate limit tracking
- Helper functions (pagination, formatting, etc.)

**Key Modules**:
- `logging.py` - Structured logging setup
- `rate_limit.py` - Rate limit tracker
- `helpers.py` - Common utility functions

## Data Flow

### Tool Execution Flow

1. **MCP Host sends tool call** via JSON-RPC over stdio
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "tools/call",
     "params": {
       "name": "get_issue",
       "arguments": {
         "project": "mygroup/myproject",
         "issue_iid": 123
       }
     }
   }
   ```

2. **Server receives and validates** request
   - Parse JSON-RPC message
   - Validate tool name exists
   - Validate arguments against tool schema

3. **Tool handler executes**
   - Load configuration (if needed)
   - Initialize GitLab client (if not cached)
   - Validate and sanitize inputs
   - Call GitLab API client method

4. **GitLab client makes API call**
   - Construct API request
   - Add authentication headers
   - Make HTTPS request to GitLab
   - Check rate limits
   - Handle errors

5. **GitLab API responds**
   ```json
   {
     "id": 123,
     "iid": 123,
     "title": "Fix authentication bug",
     "state": "opened",
     ...
   }
   ```

6. **Tool formats response**
   - Convert GitLab response to MCP response format
   - Add metadata (rate limits, execution time)
   - Handle errors gracefully

7. **Server sends response** back to MCP host
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "result": {
       "success": true,
       "data": {
         "id": 123,
         "iid": 123,
         "title": "Fix authentication bug",
         "state": "opened",
         ...
       },
       "metadata": {
         "rate_limit_remaining": 1500,
         "execution_time_ms": 245
       }
     }
   }
   ```

## Key Design Decisions

### 1. Single GitLab Instance
- Simplifies configuration
- Reduces authentication complexity
- Can be extended later for multi-instance support

### 2. PAT Authentication
- Simpler than OAuth 2.0
- Suitable for personal/team use
- User manages token lifecycle

### 3. Synchronous Implementation (Phase 1)
- Easier to implement and test
- Sufficient for initial use cases
- Can add async later if needed

### 4. Tool-based Architecture
- Each tool is independent
- Easy to add new tools
- Tools can be enabled/disabled

### 5. python-gitlab Library
- Well-maintained, comprehensive
- Handles GitLab API versioning
- Built-in pagination, error handling

## Non-Functional Requirements

### Performance
- Tool execution: < 2s for 95th percentile
- Server startup: < 5s
- Memory footprint: < 100MB typical

### Reliability
- Graceful error handling (no crashes)
- 99%+ successful API call rate
- Automatic retry for transient failures

### Security
- No token logging
- HTTPS enforcement
- Input validation and sanitization
- Secure credential storage

### Maintainability
- 80%+ code coverage
- Type hints throughout
- Comprehensive documentation
- TDD approach

## Future Architecture Considerations

### Phase 3+ Enhancements

**OAuth 2.0 Support**:
- Add OAuth flow components
- Token refresh mechanism
- Multi-user session management

**Async/Await**:
- Convert to async for better concurrency
- Use httpx for async HTTP
- Async python-gitlab client

**Caching Layer**:
- Cache frequent API calls (e.g., project info)
- Configurable TTL
- Redis or in-memory cache

**GraphQL Support**:
- For complex queries
- Reduce API call count
- Better performance

---

**Last Updated**: 2025-10-22
**Status**: Initial design (pre-implementation)
