# Phase 1: Foundation

**Status**: In Progress
**Started**: 2025-10-22
**Target Completion**: TBD

---

## Overview

Phase 1 establishes the foundational components required for the GitLab MCP Server:
- Configuration management with validation
- GitLab API client with authentication
- Error handling framework
- Logging infrastructure
- Basic MCP server skeleton
- Context tools (server info, user info)

**This phase MUST follow strict TDD**: Write tests first (Red), implement code (Green), refactor.

---

## Phase 1 Components

### 1. Configuration Module (`src/gitlab_mcp/config/`)

**Purpose**: Load, validate, and manage GitLab MCP server configuration

#### Files to Create
- `src/gitlab_mcp/config/__init__.py`
- `src/gitlab_mcp/config/settings.py` - Configuration model and loading
- `src/gitlab_mcp/config/validation.py` - Validation helpers

#### Test Files (Write FIRST)
- `tests/unit/test_config/__init__.py`
- `tests/unit/test_config/test_settings.py`
- `tests/unit/test_config/test_validation.py`

#### Requirements
- Use Pydantic for data validation
- Support environment variables (primary)
- Support config file `.gitlab-mcp.json` (secondary)
- Environment variables override config file
- Validate required fields: `gitlab_url`, `gitlab_token`
- Validate optional fields with defaults: `timeout`, `log_level`, `verify_ssl`
- Never expose token in `__repr__()` or logs

#### TDD Test Checklist
- [ ] `test_load_config_from_env` - Load config from env vars
- [ ] `test_load_config_from_file` - Load from JSON file
- [ ] `test_config_precedence_env_overrides_file` - Env vars take precedence
- [ ] `test_missing_gitlab_url_raises_validation_error` - Required field validation
- [ ] `test_missing_gitlab_token_raises_validation_error` - Required field validation
- [ ] `test_invalid_url_format_raises_validation_error` - URL format validation
- [ ] `test_default_timeout_value` - Default timeout=30
- [ ] `test_default_log_level_value` - Default log_level="INFO"
- [ ] `test_default_verify_ssl_value` - Default verify_ssl=True
- [ ] `test_token_not_in_repr` - Token hidden in string representation
- [ ] `test_token_not_in_dict` - Token marked as secret in dict export
- [ ] `test_timeout_range_validation` - Timeout between 1-300 seconds
- [ ] `test_log_level_validation` - Valid log levels only (DEBUG, INFO, WARNING, ERROR)
- [ ] `test_config_file_discovery` - Find .gitlab-mcp.json in current dir
- [ ] `test_config_file_not_found_uses_env_only` - Graceful fallback

**Coverage Target**: 85%+

---

### 2. Exception Module (`src/gitlab_mcp/client/`)

**Purpose**: Define custom exception hierarchy for clear error handling

#### Files to Create
- `src/gitlab_mcp/client/__init__.py`
- `src/gitlab_mcp/client/exceptions.py`

#### Test Files (Write FIRST)
- `tests/unit/test_client/__init__.py`
- `tests/unit/test_client/test_exceptions.py`

#### Exception Hierarchy
```python
GitLabMCPError (base)
├── ConfigurationError
│   └── ValidationError
├── AuthenticationError
├── PermissionError
├── NotFoundError
├── RateLimitError
├── GitLabServerError
└── NetworkError
    └── TimeoutError
```

#### TDD Test Checklist
- [ ] `test_exception_hierarchy` - All inherit from GitLabMCPError
- [ ] `test_exception_messages` - All accept and store message
- [ ] `test_validation_error_includes_field_name` - ValidationError stores field info
- [ ] `test_rate_limit_error_includes_retry_after` - RateLimitError stores retry info
- [ ] `test_exception_repr` - Clear string representation

**Coverage Target**: 100% (simple classes)

---

### 3. GitLab Client Module (`src/gitlab_mcp/client/`)

**Purpose**: Wrapper around python-gitlab library with error handling and MCP integration

#### Files to Create
- `src/gitlab_mcp/client/gitlab_client.py`

#### Test Files (Write FIRST)
- `tests/unit/test_client/test_gitlab_client.py`

#### Requirements
- Wrap `python-gitlab` library (v6.5.0)
- Initialize with GitLabConfig
- Lazy connection (don't connect until first API call)
- Convert all python-gitlab exceptions to custom exceptions
- Track rate limits from response headers
- Provide methods: `get_current_user()`, `get_version()`, `health_check()`
- Implement retry logic for transient failures (configurable)

#### TDD Test Checklist
- [ ] `test_client_initialization` - Create client with config
- [ ] `test_lazy_connection` - Don't connect on __init__
- [ ] `test_authenticate_success` - Successful authentication
- [ ] `test_authenticate_invalid_token` - Raise AuthenticationError
- [ ] `test_get_current_user_success` - Return user object
- [ ] `test_get_current_user_not_authenticated` - Raise AuthenticationError
- [ ] `test_get_version_success` - Return GitLab version
- [ ] `test_health_check_success` - Server is healthy
- [ ] `test_health_check_server_down` - Raise NetworkError
- [ ] `test_handle_401_error` - Convert to AuthenticationError
- [ ] `test_handle_403_error` - Convert to PermissionError
- [ ] `test_handle_404_error` - Convert to NotFoundError
- [ ] `test_handle_429_rate_limit` - Convert to RateLimitError with retry_after
- [ ] `test_handle_500_server_error` - Convert to GitLabServerError
- [ ] `test_handle_network_timeout` - Convert to TimeoutError
- [ ] `test_rate_limit_tracking` - Track remaining rate limit
- [ ] `test_retry_on_transient_failure` - Retry on 5xx errors
- [ ] `test_no_retry_on_client_error` - Don't retry on 4xx errors

**Coverage Target**: 85%+

---

### 4. Logging Module (`src/gitlab_mcp/utils/`)

**Purpose**: Structured logging with sensitive data redaction

#### Files to Create
- `src/gitlab_mcp/utils/__init__.py`
- `src/gitlab_mcp/utils/logging.py`

#### Test Files (Write FIRST)
- `tests/unit/test_utils/__init__.py`
- `tests/unit/test_utils/test_logging.py`

#### Requirements
- Use Python's built-in `logging` module
- Structured logging (JSON format option)
- Automatic redaction of sensitive data (tokens, passwords)
- Configurable log levels
- Log to stdout (for MCP server compatibility)
- Include context: timestamp, level, module, message

#### TDD Test Checklist
- [ ] `test_logger_initialization` - Create logger with config
- [ ] `test_log_level_from_config` - Respect config log level
- [ ] `test_redact_token_in_message` - Token values redacted
- [ ] `test_redact_password_in_message` - Password values redacted
- [ ] `test_structured_logging_format` - JSON format output
- [ ] `test_log_includes_timestamp` - Timestamp in logs
- [ ] `test_log_includes_module_name` - Module name in logs

**Coverage Target**: 85%+

---

### 5. MCP Server Skeleton (`src/gitlab_mcp/`)

**Purpose**: Basic MCP server initialization and protocol handling

#### Files to Create
- `src/gitlab_mcp/__init__.py`
- `src/gitlab_mcp/server.py`

#### Test Files (Write FIRST)
- `tests/unit/test_server.py`
- `tests/e2e/test_mcp_server/test_server_initialization.py`

#### Requirements
- Use `mcp` SDK v1.18.0
- Initialize MCP server with name "gitlab-mcp"
- Register tool handlers (empty stubs for Phase 1)
- Handle server lifecycle (start, stop)
- Load configuration on startup
- Initialize GitLab client on startup

#### TDD Test Checklist
- [ ] `test_server_initialization` - Create server instance
- [ ] `test_server_loads_config` - Config loaded on init
- [ ] `test_server_initializes_client` - GitLab client created
- [ ] `test_server_name` - Server name is "gitlab-mcp"
- [ ] `test_server_version` - Server version from package
- [ ] `test_server_handles_invalid_config` - Raise error on bad config

**Coverage Target**: 80%+

---

### 6. Context Tools (`src/gitlab_mcp/tools/context/`)

**Purpose**: Basic context/info tools for MCP server

#### Files to Create
- `src/gitlab_mcp/tools/__init__.py`
- `src/gitlab_mcp/tools/context/__init__.py`
- `src/gitlab_mcp/tools/context/info.py`

#### Test Files (Write FIRST)
- `tests/unit/test_tools/__init__.py`
- `tests/unit/test_tools/test_context/__init__.py`
- `tests/unit/test_tools/test_context/test_info.py`

#### Tools to Implement
1. `get_current_user` - Get authenticated user info
2. `get_server_version` - Get GitLab server version
3. `get_gitlab_version` - Alias for get_server_version

#### TDD Test Checklist
- [ ] `test_get_current_user_success` - Return user dict
- [ ] `test_get_current_user_not_authenticated` - Raise error
- [ ] `test_get_current_user_includes_username` - User dict has username
- [ ] `test_get_current_user_includes_id` - User dict has id
- [ ] `test_get_server_version_success` - Return version string
- [ ] `test_get_server_version_format` - Version format "X.Y.Z"

**Coverage Target**: 85%+

---

## Phase 1 Implementation Order

Follow this sequence strictly (TDD for each):

1. **Exceptions** (foundational, needed by everything)
   - Write exception tests
   - Implement exception classes
   - Verify coverage

2. **Logging** (needed for debugging)
   - Write logging tests
   - Implement logging module
   - Verify coverage

3. **Configuration** (needed by client)
   - Write configuration tests
   - Implement configuration module
   - Verify coverage

4. **GitLab Client** (core integration)
   - Write client tests
   - Implement client module
   - Verify coverage

5. **MCP Server Skeleton** (orchestration)
   - Write server tests
   - Implement server module
   - Verify coverage

6. **Context Tools** (first tools)
   - Write context tool tests
   - Implement context tools
   - Verify coverage

---

## Phase 1 Gate Criteria

Before proceeding to Phase 2, ALL must be met:

- [ ] All exception tests written and passing (100%)
- [ ] All logging tests written and passing (100%)
- [ ] All configuration tests written and passing (100%)
- [ ] All client tests written and passing (100%)
- [ ] All server tests written and passing (100%)
- [ ] All context tool tests written and passing (100%)
- [ ] Overall Phase 1 code coverage ≥80%
- [ ] No mypy type errors in Phase 1 code
- [ ] All code formatted with black
- [ ] No ruff linting errors
- [ ] Phase 1 documentation complete:
  - [ ] `docs/api/tools_reference.md` updated with context tools
  - [ ] `docs/architecture/interfaces.md` updated with client interface
  - [ ] `docs/development/tdd_workflow.md` created with examples
- [ ] Session log updated
- [ ] `next_session_plan.md` updated with Phase 2 plan

---

## Testing Strategy

### Unit Tests
- Mock all external dependencies (python-gitlab, file system, env vars)
- Fast execution (< 1 second total)
- Test all code paths and edge cases
- Use pytest fixtures for common test data

### Integration Tests (Optional for Phase 1)
- Test against real GitLab instance (test server or local)
- Verify actual API calls work
- Can be run separately from unit tests

### E2E Tests
- Test full MCP protocol communication
- Verify tool registration and invocation
- Test server lifecycle

---

## Dependencies

**Runtime**:
- `python-gitlab>=6.5.0` - GitLab API client
- `mcp>=1.18.0` - MCP SDK
- `pydantic>=2.11.0` - Data validation
- `pydantic-settings>=2.8.0` - Settings management

**Development**:
- `pytest>=8.4.2` - Testing framework
- `pytest-cov>=6.1.0` - Coverage reporting
- `pytest-mock>=3.14.0` - Mocking utilities
- `black>=25.1.0` - Code formatting
- `ruff>=0.14.1` - Linting
- `mypy>=1.18.2` - Type checking

All versions are pinned to October 2025 latest stable releases.

---

## Documentation to Create During Phase 1

- [x] This file (`docs/phases/phase_1_foundation.md`)
- [ ] `docs/development/tdd_workflow.md` - TDD examples and patterns
- [ ] `docs/api/tools_reference.md` - Context tools documentation
- [ ] `docs/architecture/interfaces.md` - Client and server interfaces
- [ ] Session logs as we progress

---

## Key Design Decisions

### Configuration
- **Decision**: Use Pydantic Settings for validation and env var support
- **Rationale**: Type-safe, automatic validation, excellent env var support
- **Trade-off**: Adds dependency, but worth it for robustness

### GitLab Client
- **Decision**: Wrap python-gitlab instead of direct HTTP calls
- **Rationale**: Mature library, handles auth/pagination/rate limits
- **Trade-off**: Adds abstraction layer, but reduces maintenance burden

### Error Handling
- **Decision**: Custom exception hierarchy inheriting from base GitLabMCPError
- **Rationale**: Clear error types, easy to catch specific errors, good error messages
- **Trade-off**: More code, but significantly better error handling

### Logging
- **Decision**: Automatic sensitive data redaction
- **Rationale**: Security-first, prevent token leakage in logs
- **Trade-off**: Small performance overhead, but critical for security

---

**Next Steps**: Begin with Exceptions module (TDD Red phase)
**First Test to Write**: `tests/unit/test_client/test_exceptions.py`
