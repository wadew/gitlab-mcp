# GitLab MCP Server - Configuration Guide

This guide explains how to configure the GitLab MCP Server for use with Claude Code and other MCP-compatible tools.

## Table of Contents

1. [Configuration Overview](#configuration-overview)
2. [Claude Code Integration](#claude-code-integration)
3. [Configuration File](#configuration-file)
4. [Environment Variables](#environment-variables)
5. [Advanced Configuration](#advanced-configuration)
6. [Multiple Instances](#multiple-instances)

---

## Configuration Overview

The GitLab MCP Server uses a hierarchical configuration system:

1. **JSON Configuration File** (`.gitlab-mcp.json`) - Default settings
2. **Environment Variables** (`GITLAB_*`) - Override file settings
3. **MCP Client Configuration** - Claude Code settings override all

### Configuration Sources Priority

```
MCP Client Config (highest)
    ↓
Environment Variables
    ↓
JSON Configuration File
    ↓
Default Values (lowest)
```

---

## Claude Code Integration

To use the GitLab MCP Server with Claude Code, you need to configure it in Claude Code's MCP settings.

### Step 1: Locate Claude Code Configuration

Claude Code stores its configuration in:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Step 2: Configure MCP Server

Add the GitLab MCP Server to the `mcpServers` section:

```json
{
  "mcpServers": {
    "gitlab": {
      "command": "python",
      "args": [
        "-m",
        "gitlab_mcp.server"
      ],
      "env": {
        "GITLAB_URL": "https://gitlab.example.com",
        "GITLAB_TOKEN": "glpat-xxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

### Step 3: Restart Claude Code

After modifying the configuration:
1. Save the file
2. Quit Claude Code completely
3. Restart Claude Code

### Step 4: Verify Integration

In Claude Code, you should now be able to use GitLab MCP tools:

```
Can you list my GitLab projects?
```

Claude Code will use the `gitlab_list_projects` tool automatically.

---

## Configuration File

### Creating `.gitlab-mcp.json`

Create a file named `.gitlab-mcp.json` in your project directory:

```json
{
  "gitlab_url": "https://gitlab.example.com",
  "gitlab_token": "glpat-xxxxxxxxxxxxxxxxxxxx",
  "timeout": 30,
  "log_level": "INFO",
  "verify_ssl": true
}
```

### Configuration Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| `gitlab_url` | string | Yes | - | GitLab instance URL (must include scheme) |
| `gitlab_token` | string | Yes | - | Personal Access Token |
| `timeout` | integer | No | 30 | Request timeout in seconds (1-300) |
| `log_level` | string | No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `verify_ssl` | boolean | No | true | Verify SSL certificates |

### Example Configurations

#### Basic Configuration

```json
{
  "gitlab_url": "https://gitlab.com",
  "gitlab_token": "glpat-xxxxxxxxxxxxxxxxxxxx"
}
```

#### Development Configuration

```json
{
  "gitlab_url": "https://gitlab.dev.local",
  "gitlab_token": "glpat-xxxxxxxxxxxxxxxxxxxx",
  "timeout": 60,
  "log_level": "DEBUG",
  "verify_ssl": false
}
```

#### Production Configuration

```json
{
  "gitlab_url": "https://gitlab.company.com",
  "gitlab_token": "glpat-xxxxxxxxxxxxxxxxxxxx",
  "timeout": 30,
  "log_level": "WARNING",
  "verify_ssl": true
}
```

---

## Environment Variables

Environment variables provide a flexible way to configure the server without modifying files.

### Setting Environment Variables

#### Option 1: `.env` File (Recommended)

Create a `.env` file in your project directory:

```bash
# GitLab Configuration
GITLAB_URL=https://gitlab.example.com
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
GITLAB_TIMEOUT=30
GITLAB_LOG_LEVEL=INFO
GITLAB_VERIFY_SSL=true
```

Load the `.env` file before starting:

```bash
source .env
python -m gitlab_mcp.server
```

#### Option 2: Shell Profile

Add to `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
# GitLab MCP Server
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
export GITLAB_TIMEOUT=30
export GITLAB_LOG_LEVEL="INFO"
export GITLAB_VERIFY_SSL=true
```

Reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

#### Option 3: Command Line

Set variables inline when running the server:

```bash
GITLAB_URL="https://gitlab.example.com" \
GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx" \
python -m gitlab_mcp.server
```

### Environment Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `GITLAB_URL` | GitLab instance URL | `https://gitlab.com` |
| `GITLAB_TOKEN` | Personal Access Token | `glpat-abc123xyz456` |
| `GITLAB_TIMEOUT` | Request timeout (seconds) | `30` |
| `GITLAB_LOG_LEVEL` | Logging verbosity | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `GITLAB_VERIFY_SSL` | Verify SSL certificates | `true`, `false`, `1`, `0` |

---

## Advanced Configuration

### Custom Log Configuration

For more control over logging, you can configure Python's logging system:

```python
# custom_logging_config.py
import logging
from gitlab_mcp.utils.logging import setup_logging

# Configure custom logging
setup_logging(log_level="DEBUG")

# Add custom handler
handler = logging.FileHandler("gitlab_mcp.log")
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logger = logging.getLogger("gitlab_mcp")
logger.addHandler(handler)
```

### SSL Certificate Pinning (Advanced)

For enhanced security with self-signed certificates:

```python
from gitlab_mcp.config.settings import GitLabConfig

config = GitLabConfig(
    gitlab_url="https://gitlab.example.com",
    gitlab_token="glpat-xxxxxxxxxxxxxxxxxxxx",
    verify_ssl="/path/to/custom/ca-bundle.crt"  # Custom CA bundle
)
```

### Proxy Configuration

If you're behind a corporate proxy, configure it via environment variables:

```bash
# HTTP/HTTPS Proxy
export HTTP_PROXY="http://proxy.company.com:8080"
export HTTPS_PROXY="http://proxy.company.com:8080"
export NO_PROXY="localhost,127.0.0.1"

# Run server
python -m gitlab_mcp.server
```

### Timeout Strategies

Choose timeout values based on your use case:

| Use Case | Recommended Timeout | Reason |
|----------|---------------------|--------|
| Local Network | 10-15 seconds | Low latency |
| Standard Internet | 30 seconds (default) | Balance speed/reliability |
| Slow Connection | 60-90 seconds | Higher latency tolerance |
| Large Operations | 120-300 seconds | Complex API calls (exports, etc.) |

---

## Multiple Instances

You can configure multiple GitLab instances in Claude Code.

### Example: Multiple GitLab Servers

```json
{
  "mcpServers": {
    "gitlab-prod": {
      "command": "python",
      "args": ["-m", "gitlab_mcp.server"],
      "env": {
        "GITLAB_URL": "https://gitlab.company.com",
        "GITLAB_TOKEN": "glpat-prod-token"
      }
    },
    "gitlab-dev": {
      "command": "python",
      "args": ["-m", "gitlab_mcp.server"],
      "env": {
        "GITLAB_URL": "https://gitlab.dev.company.com",
        "GITLAB_TOKEN": "glpat-dev-token",
        "GITLAB_LOG_LEVEL": "DEBUG"
      }
    },
    "gitlab-com": {
      "command": "python",
      "args": ["-m", "gitlab_mcp.server"],
      "env": {
        "GITLAB_URL": "https://gitlab.com",
        "GITLAB_TOKEN": "glpat-public-token"
      }
    }
  }
}
```

### Usage with Multiple Instances

When you have multiple instances configured, Claude Code will show which server is being used:

```
Using: gitlab-prod
Projects: [list of production projects]

Using: gitlab-dev
Projects: [list of development projects]
```

---

## Configuration Validation

The server automatically validates your configuration on startup.

### Validation Checks

The server verifies:

1. ✅ **GitLab URL**: Valid HTTP/HTTPS URL
2. ✅ **Access Token**: Non-empty string
3. ✅ **Timeout**: Integer between 1-300 seconds
4. ✅ **Log Level**: Valid log level name
5. ✅ **SSL Verification**: Boolean value

### Validation Errors

Common validation errors and fixes:

#### Invalid URL

**Error**:
```
ValidationError: gitlab_url must include scheme (http:// or https://). Got: gitlab.com
```

**Fix**:
```bash
GITLAB_URL=https://gitlab.com  # Add https://
```

#### Missing Token

**Error**:
```
ValidationError: gitlab_token: field required
```

**Fix**:
```bash
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
```

#### Invalid Timeout

**Error**:
```
ValidationError: timeout must not exceed 300 seconds
```

**Fix**:
```bash
GITLAB_TIMEOUT=300  # Maximum allowed
```

---

## Testing Your Configuration

### Quick Test Script

Create `test_config.py`:

```python
#!/usr/bin/env python3
"""Test GitLab MCP Server configuration."""

from gitlab_mcp.config.settings import load_config
from gitlab_mcp.client.gitlab_client import GitLabClient

def test_configuration():
    """Test configuration and connection."""
    try:
        # Load configuration
        config = load_config()
        print(f"✓ Configuration loaded successfully")
        print(f"  GitLab URL: {config.gitlab_url}")
        print(f"  Timeout: {config.timeout}s")
        print(f"  Log Level: {config.log_level}")
        print(f"  SSL Verification: {config.verify_ssl}")

        # Test connection
        client = GitLabClient(config)
        user = client.get_current_user()

        print(f"\n✓ Connection successful!")
        print(f"  Authenticated as: {user.username}")
        print(f"  User ID: {user.id}")

        # Test API access
        projects = client.list_projects(per_page=5)
        print(f"\n✓ API access confirmed")
        print(f"  Total projects: {projects.get('total', 0)}")

        print("\n🎉 Configuration test passed!")
        return True

    except Exception as e:
        print(f"\n✗ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_configuration()
    exit(0 if success else 1)
```

Run the test:

```bash
python test_config.py
```

---

## Security Best Practices

### 1. Token Management

- ✅ **DO**: Store tokens in environment variables or secure vaults
- ✅ **DO**: Use tokens with minimal required scopes
- ✅ **DO**: Set token expiration dates
- ❌ **DON'T**: Commit tokens to version control
- ❌ **DON'T**: Share tokens in plain text
- ❌ **DON'T**: Use the same token for multiple environments

### 2. SSL/TLS Configuration

- ✅ **DO**: Always use HTTPS in production
- ✅ **DO**: Verify SSL certificates (`verify_ssl=true`)
- ❌ **DON'T**: Disable SSL verification in production
- ❌ **DON'T**: Ignore SSL warnings

### 3. Access Control

- ✅ **DO**: Use project-specific tokens when possible
- ✅ **DO**: Regularly rotate tokens
- ✅ **DO**: Audit token usage
- ❌ **DON'T**: Use admin tokens unless necessary
- ❌ **DON'T**: Grant unnecessary API scopes

### 4. Configuration Files

```bash
# Always add sensitive config files to .gitignore
echo ".env" >> .gitignore
echo ".gitlab-mcp.json" >> .gitignore
echo "*.secret" >> .gitignore
```

---

## Troubleshooting

If you encounter configuration issues, see the [Troubleshooting Guide](troubleshooting.md).

Common issues:
- Authentication failures → Check token and scopes
- Connection timeouts → Adjust `GITLAB_TIMEOUT`
- SSL errors → Verify `GITLAB_URL` and `verify_ssl` setting

---

## Next Steps

- **Explore Tools**: See [Tools Reference](../api/tools_reference.md) for available MCP tools
- **Usage Examples**: Check [Usage Examples](usage_examples.md) for common workflows
- **API Reference**: Review [GitLab API Mapping](../api/gitlab_api_mapping.md)

---

**Need Help?** Check the [Troubleshooting Guide](troubleshooting.md) or open an issue on GitLab.
