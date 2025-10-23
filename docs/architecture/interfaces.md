# Interface Contracts

This document defines the contracts between components. All interfaces must be maintained for backward compatibility.

## 1. MCP Tool Interface

All tools must implement this interface:

```python
from typing import Any, Dict
from abc import ABC, abstractmethod

class BaseTool(ABC):
    """Base interface for all MCP tools"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (e.g., 'get_issue')"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable tool description"""
        pass

    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """JSON Schema for tool input parameters"""
        pass

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.

        Args:
            **kwargs: Tool-specific parameters matching input_schema

        Returns:
            Response dict with structure:
            {
                "success": bool,
                "data": Any,  # Tool-specific response data
                "metadata": {
                    "rate_limit_remaining": int,
                    "rate_limit_reset": str,  # ISO 8601 datetime
                    "execution_time_ms": int
                }
            }

        Raises:
            ValidationError: Invalid input parameters
            GitLabAPIError: GitLab API error
            AuthenticationError: Invalid credentials
            PermissionError: Insufficient permissions
            NotFoundError: Resource not found
        """
        pass
```

## 2. GitLab Client Interface

```python
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod

class IGitLabClient(ABC):
    """Interface for GitLab API client"""

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with GitLab using configured credentials"""
        pass

    @abstractmethod
    def get_current_user(self) -> Dict[str, Any]:
        """Get authenticated user information"""
        pass

    @abstractmethod
    def get_project(self, project_id: str) -> Dict[str, Any]:
        """Get project by ID or path"""
        pass

    @abstractmethod
    def get_issue(self, project_id: str, issue_iid: int) -> Dict[str, Any]:
        """Get issue details"""
        pass

    @abstractmethod
    def create_issue(
        self,
        project_id: str,
        title: str,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create new issue"""
        pass

    # Additional methods defined per GitLab API requirements
```

## 3. Configuration Interface

```python
from typing import Optional
from pydantic import BaseModel, Field

class GitLabConfig(BaseModel):
    """Configuration schema for GitLab connection"""

    gitlab_url: str = Field(
        ...,
        description="GitLab instance URL (e.g., https://gitlab.example.com)"
    )

    gitlab_token: str = Field(
        ...,
        description="Personal Access Token for authentication",
        repr=False  # Don't print in logs
    )

    default_project: Optional[str] = Field(
        None,
        description="Default project path (e.g., 'group/project')"
    )

    timeout: int = Field(
        30,
        description="API request timeout in seconds",
        ge=1,
        le=300
    )

    verify_ssl: bool = Field(
        True,
        description="Verify SSL certificates"
    )

    log_level: str = Field(
        "INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
```

## 4. Response Format Standards

### Success Response
```python
{
    "success": True,
    "data": {
        # Tool-specific response data
        # Structure depends on tool
    },
    "metadata": {
        "rate_limit_remaining": 1500,      # Remaining API calls
        "rate_limit_reset": "2025-10-22T15:30:00Z",  # ISO 8601
        "execution_time_ms": 245           # Time taken
    }
}
```

### Error Response
```python
{
    "success": False,
    "error": {
        "code": "ERROR_CODE",              # Machine-readable error code
        "message": "Human-readable message",
        "details": {                       # Optional contextual details
            "field": "value",
            # Additional context
        }
    }
}
```

### Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input parameters |
| `AUTHENTICATION_ERROR` | 401 | Invalid or missing credentials |
| `PERMISSION_ERROR` | 403 | Insufficient permissions |
| `NOT_FOUND_ERROR` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | GitLab validation failed |
| `RATE_LIMIT_ERROR` | 429 | Rate limit exceeded |
| `GITLAB_SERVER_ERROR` | 500+ | GitLab server error |
| `NETWORK_ERROR` | N/A | Network/connection error |
| `TIMEOUT_ERROR` | N/A | Request timeout |
| `UNKNOWN_ERROR` | N/A | Unexpected error |

## 5. Exception Hierarchy

```python
class GitLabMCPError(Exception):
    """Base exception for all GitLab MCP errors"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)

class ValidationError(GitLabMCPError):
    """Input validation failed"""
    pass

class AuthenticationError(GitLabMCPError):
    """Authentication failed"""
    pass

class PermissionError(GitLabMCPError):
    """Insufficient permissions"""
    pass

class NotFoundError(GitLabMCPError):
    """Resource not found"""
    pass

class RateLimitError(GitLabMCPError):
    """Rate limit exceeded"""
    def __init__(self, message: str, reset_time: str, **kwargs):
        super().__init__(message, **kwargs)
        self.reset_time = reset_time

class GitLabServerError(GitLabMCPError):
    """GitLab server error (5xx)"""
    pass

class NetworkError(GitLabMCPError):
    """Network/connection error"""
    pass

class TimeoutError(GitLabMCPError):
    """Request timeout"""
    pass
```

## 6. Logging Interface

All components must use structured logging:

```python
import logging
from typing import Any, Dict

def log_tool_execution(
    tool_name: str,
    params: Dict[str, Any],
    duration_ms: int,
    success: bool,
    error: Optional[str] = None
) -> None:
    """Log tool execution with structured data"""
    logger = logging.getLogger("gitlab_mcp")

    log_data = {
        "tool": tool_name,
        "duration_ms": duration_ms,
        "success": success,
        "params": {k: v for k, v in params.items() if k != "token"},  # Redact sensitive data
    }

    if error:
        log_data["error"] = error
        logger.warning(f"Tool execution failed: {tool_name}", extra=log_data)
    else:
        logger.info(f"Tool execution completed: {tool_name}", extra=log_data)
```

## 7. Pagination Interface

For tools that return lists:

```python
class PaginationParams(BaseModel):
    """Standard pagination parameters"""

    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")

class PaginatedResponse(BaseModel):
    """Standard paginated response"""

    items: List[Any]
    total_count: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_previous: bool
```

## 8. Rate Limit Interface

```python
class RateLimitInfo(BaseModel):
    """Rate limit information from GitLab API"""

    limit: int              # Total rate limit
    remaining: int          # Remaining calls
    reset: str             # Reset time (ISO 8601)
    used: int              # Used calls

def track_rate_limit(response_headers: Dict[str, str]) -> RateLimitInfo:
    """Extract rate limit info from response headers"""
    return RateLimitInfo(
        limit=int(response_headers.get("RateLimit-Limit", 0)),
        remaining=int(response_headers.get("RateLimit-Remaining", 0)),
        reset=response_headers.get("RateLimit-Reset", ""),
        used=int(response_headers.get("RateLimit-Observed", 0))
    )
```

## 9. Testing Interfaces

### Test Fixture Interface

```python
@pytest.fixture
def gitlab_config() -> GitLabConfig:
    """Provide test GitLab configuration"""
    return GitLabConfig(
        gitlab_url="https://gitlab.example.com",
        gitlab_token="test-token-123",
        default_project="test-group/test-project"
    )

@pytest.fixture
def mock_gitlab_client() -> Mock:
    """Provide mocked GitLab client"""
    client = Mock(spec=IGitLabClient)
    # Configure mock responses
    return client
```

### Test Data Interface

```python
# tests/fixtures/gitlab_responses.py

MOCK_ISSUE_RESPONSE = {
    "id": 12345,
    "iid": 123,
    "project_id": 5,
    "title": "Test issue",
    "state": "opened",
    # ... complete response
}

MOCK_MERGE_REQUEST_RESPONSE = {
    "id": 67890,
    "iid": 456,
    "project_id": 5,
    "title": "Test MR",
    # ... complete response
}
```

## 10. Versioning Contract

### API Version Support
- **GitLab API**: v4
- **Minimum GitLab Version**: 15.0
- **MCP Protocol**: 2025-06-18 specification

### Version Detection

```python
def check_gitlab_version(client: IGitLabClient) -> bool:
    """Check if GitLab version is supported"""
    version_info = client.get_version()
    major, minor = parse_version(version_info["version"])
    return major >= 15
```

---

**Interface Stability**: All interfaces in this document are considered **stable** once implementation begins. Breaking changes require major version bump and migration guide.

**Last Updated**: 2025-10-22
**Status**: Initial design
