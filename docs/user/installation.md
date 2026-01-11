# GitLab MCP Server - Installation Guide

This guide walks you through installing and setting up the GitLab MCP Server for use with Claude Code and other MCP-compatible AI tools.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [GitLab Personal Access Token](#gitlab-personal-access-token)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Next Steps](#next-steps)

---

## Prerequisites

Before installing the GitLab MCP Server, ensure you have:

### System Requirements

- **Python**: Version 3.11 or higher
- **pip**: Python package installer
- **uv** (recommended): Fast Python package manager (optional but recommended)
- **GitLab Instance**: Access to a GitLab instance (self-hosted or GitLab.com)
- **GitLab Token**: Personal Access Token with appropriate permissions

### Recommended Tools

- **uv**: Fast Python package and environment manager
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

---

## Installation

### Option 1: Install from Source (Recommended for Development)

1. **Clone the Repository**

   ```bash
   git clone https://gitlab.prod.thezephyrco.com/mcps/gitlab_mcp.git
   cd gitlab_mcp
   ```

2. **Create Virtual Environment**

   Using `uv` (recommended):
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

   Or using standard Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**

   Using `uv`:
   ```bash
   uv pip install -e "."
   ```

   Or using pip:
   ```bash
   pip install -e "."
   ```

### Option 2: Install from PyPI (When Published)

*Note: This option will be available once the package is published to PyPI.*

```bash
pip install python-gitlab-mcp
```

---

## GitLab Personal Access Token

The GitLab MCP Server requires a Personal Access Token (PAT) to authenticate with your GitLab instance.

### Creating a Personal Access Token

1. **Log in to GitLab**
   - Navigate to your GitLab instance (e.g., `https://gitlab.com` or your self-hosted URL)

2. **Access Token Settings**
   - Click your profile picture → **Preferences**
   - In the left sidebar, click **Access Tokens**

3. **Create New Token**
   - Click **Add new token**
   - **Token name**: `MCP Server` (or any descriptive name)
   - **Expiration date**: Choose an appropriate expiration (or leave blank for no expiration)

4. **Select Scopes**

   The following scopes are **required** for full functionality:

   - ✅ **api**: Full API access (required)
   - ✅ **read_api**: Read-only API access
   - ✅ **read_user**: Read user information
   - ✅ **read_repository**: Read repository data
   - ✅ **write_repository**: Create/update files and branches

   Optional scopes (for advanced features):
   - ✅ **read_registry**: Access container registry
   - ✅ **sudo**: Perform API actions as admin (self-hosted only)

5. **Create Token**
   - Click **Create personal access token**
   - **IMPORTANT**: Copy the token immediately! You won't be able to see it again.

### Storing Your Token Securely

**NEVER commit your token to version control!**

You have several options for storing your token:

#### Option 1: Environment Variable (Recommended)

Create a `.env` file in your project directory:

```bash
# .env
GITLAB_URL=https://gitlab.example.com
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
```

**Important**: Add `.env` to your `.gitignore`:
```bash
echo ".env" >> .gitignore
```

#### Option 2: System Environment Variables

Add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export GITLAB_URL="https://gitlab.example.com"
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
```

Then reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc
```

#### Option 3: Configuration File

Create a `.gitlab-mcp.json` file in your project directory:

```json
{
  "gitlab_url": "https://gitlab.example.com",
  "gitlab_token": "glpat-xxxxxxxxxxxxxxxxxxxx",
  "timeout": 30,
  "log_level": "INFO",
  "verify_ssl": true
}
```

**Important**: Add `.gitlab-mcp.json` to your `.gitignore`:
```bash
echo ".gitlab-mcp.json" >> .gitignore
```

---

## Configuration

### Configuration Options

The GitLab MCP Server can be configured via environment variables or a JSON configuration file.

| Setting | Environment Variable | JSON Key | Default | Description |
|---------|---------------------|----------|---------|-------------|
| GitLab URL | `GITLAB_URL` | `gitlab_url` | *required* | Your GitLab instance URL |
| Access Token | `GITLAB_TOKEN` | `gitlab_token` | *required* | Personal Access Token |
| Timeout | `GITLAB_TIMEOUT` | `timeout` | 30 | Request timeout (seconds) |
| Log Level | `GITLAB_LOG_LEVEL` | `log_level` | INFO | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| Verify SSL | `GITLAB_VERIFY_SSL` | `verify_ssl` | true | Verify SSL certificates |

### Configuration Priority

Configuration sources are loaded in this order (later overrides earlier):

1. JSON configuration file (`.gitlab-mcp.json`)
2. Environment variables (`GITLAB_*`)

**Best Practice**: Use environment variables for sensitive data (token) and JSON for other settings.

### Example Configurations

#### Self-Hosted GitLab

```bash
# .env
GITLAB_URL=https://gitlab.company.com
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
GITLAB_TIMEOUT=60
GITLAB_LOG_LEVEL=DEBUG
GITLAB_VERIFY_SSL=true
```

#### GitLab.com

```bash
# .env
GITLAB_URL=https://gitlab.com
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
```

#### Development Environment (with self-signed SSL)

```bash
# .env
GITLAB_URL=https://gitlab.dev.local
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
GITLAB_VERIFY_SSL=false  # Only for development!
GITLAB_LOG_LEVEL=DEBUG
```

---

## Verification

After installation and configuration, verify everything works:

### 1. Check Python Environment

```bash
python --version  # Should be 3.11 or higher
which python      # Should point to your virtual environment
```

### 2. Verify Installation

```bash
python -c "from gitlab_mcp.server import main; print('✓ GitLab MCP Server installed successfully')"
```

### 3. Test GitLab Connection

Create a simple test script (`test_connection.py`):

```python
#!/usr/bin/env python3
"""Test GitLab connection."""

from gitlab_mcp.config.settings import load_config
from gitlab_mcp.client.gitlab_client import GitLabClient

# Load configuration
config = load_config()
print(f"✓ Configuration loaded: {config.gitlab_url}")

# Create client
client = GitLabClient(config)
print("✓ GitLab client created")

# Test authentication
try:
    user = client.get_current_user()
    print(f"✓ Successfully authenticated as: {user.username}")
    print(f"✓ User email: {user.email}")
except Exception as e:
    print(f"✗ Authentication failed: {e}")
    exit(1)

print("\n🎉 Connection test successful!")
```

Run the test:

```bash
python test_connection.py
```

Expected output:
```
✓ Configuration loaded: https://gitlab.example.com
✓ GitLab client created
✓ Successfully authenticated as: your-username
✓ User email: your-email@example.com

🎉 Connection test successful!
```

### 4. Test MCP Server

Start the MCP server:

```bash
python -m gitlab_mcp.server
```

You should see:
```
GitLab MCP Server starting...
Server initialized successfully
Listening for MCP connections...
```

---

## Next Steps

Now that you have the GitLab MCP Server installed:

1. **Configure Claude Code**: See [Configuration Guide](configuration.md) for integrating with Claude Code
2. **Explore Tools**: Check [Tools Reference](../api/tools_reference.md) for available MCP tools
3. **Review Examples**: See [Usage Examples](usage_examples.md) for common workflows
4. **Troubleshooting**: If you encounter issues, see [Troubleshooting Guide](troubleshooting.md)

---

## Common Installation Issues

### Issue: `python-gitlab` not found

**Solution**: Ensure you're in your virtual environment and dependencies are installed:
```bash
source .venv/bin/activate
uv pip install -e "."
```

### Issue: SSL Certificate Verification Failed

**Solution**: For self-signed certificates in development:
```bash
export GITLAB_VERIFY_SSL=false
```

**Warning**: Never disable SSL verification in production!

### Issue: Token Authentication Failed

**Solution**: Verify your token:
1. Check token hasn't expired
2. Verify token has correct scopes (`api`, `read_api`)
3. Test token with curl:
   ```bash
   curl -H "PRIVATE-TOKEN: your-token" https://gitlab.example.com/api/v4/user
   ```

### Issue: Import Error

**Solution**: Ensure the package is installed in editable mode:
```bash
pip install -e "."
```

---

## Additional Resources

- **GitLab API Documentation**: https://docs.gitlab.com/ee/api/
- **MCP Protocol**: https://github.com/anthropics/mcp
- **python-gitlab**: https://python-gitlab.readthedocs.io/

---

**Need Help?** Check the [Troubleshooting Guide](troubleshooting.md) or open an issue on GitLab.
