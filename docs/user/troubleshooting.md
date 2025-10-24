# GitLab MCP Server - Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the GitLab MCP Server.

## Table of Contents

1. [Connection Issues](#connection-issues)
2. [Authentication Problems](#authentication-problems)
3. [SSL/TLS Errors](#ssltls-errors)
4. [Performance Issues](#performance-issues)
5. [Tool Errors](#tool-errors)
6. [Debug Mode](#debug-mode)
7. [Getting Help](#getting-help)

---

## Connection Issues

### Issue: Cannot Connect to GitLab Instance

**Symptoms:**
```
GitLabAPIError: Network error: connection refused
```

**Possible Causes & Solutions:**

1. **Incorrect GitLab URL**
   ```bash
   # Check your URL includes the scheme
   echo $GITLAB_URL
   # Should output: https://gitlab.example.com (not gitlab.example.com)
   ```

   **Fix:**
   ```bash
   export GITLAB_URL="https://gitlab.example.com"  # Add https://
   ```

2. **GitLab Instance is Down**
   ```bash
   # Test connectivity
   curl -I https://gitlab.example.com
   ```

   **Fix:** Wait for instance to come back online or contact your GitLab admin.

3. **Network/Firewall Issues**
   ```bash
   # Test network connectivity
   ping gitlab.example.com

   # Test HTTPS port
   nc -zv gitlab.example.com 443
   ```

   **Fix:** Configure firewall rules or use VPN if required.

4. **Proxy Configuration**

   **Fix:** Set proxy environment variables:
   ```bash
   export HTTP_PROXY="http://proxy.company.com:8080"
   export HTTPS_PROXY="http://proxy.company.com:8080"
   export NO_PROXY="localhost,127.0.0.1"
   ```

---

## Authentication Problems

### Issue: Authentication Failed

**Symptoms:**
```
AuthenticationError: GitLab authentication failed
```

**Diagnostic Steps:**

1. **Verify Token is Set**
   ```bash
   echo $GITLAB_TOKEN
   # Should output: glpat-xxxxxxxxxxxxxxxxxxxx
   ```

2. **Test Token with curl**
   ```bash
   curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        https://gitlab.example.com/api/v4/user
   ```

   Expected response:
   ```json
   {
     "id": 123,
     "username": "your-username",
     "email": "your-email@example.com"
   }
   ```

**Common Fixes:**

1. **Token Not Set**
   ```bash
   export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
   ```

2. **Token Expired**
   - Go to GitLab → Preferences → Access Tokens
   - Check expiration date
   - Create new token if expired

3. **Insufficient Token Scopes**

   Required scopes:
   - ✅ `api`
   - ✅ `read_api`
   - ✅ `read_user`
   - ✅ `read_repository`
   - ✅ `write_repository` (for write operations)

   **Fix:** Create new token with correct scopes.

4. **Token Revoked**
   - Check if token exists in GitLab → Access Tokens
   - Create new token if revoked

### Issue: Permission Denied

**Symptoms:**
```
PermissionError: User does not have permission to perform this action
```

**Diagnostic Steps:**

1. **Check User Permissions**
   ```bash
   # Get current user info
   curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        https://gitlab.example.com/api/v4/user
   ```

2. **Check Project Access**
   ```bash
   # Get project details
   curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
        https://gitlab.example.com/api/v4/projects/PROJECT_ID
   ```

**Fixes:**

1. **Insufficient Project Role**
   - Minimum required: Developer role for most operations
   - Maintainer role for admin operations
   - **Fix:** Ask project owner to grant appropriate role

2. **Protected Branch**
   - Cannot push to protected branches without proper role
   - **Fix:** Push to non-protected branch or ask for permissions

3. **Token Without API Scope**
   - **Fix:** Create new token with `api` scope

---

## SSL/TLS Errors

### Issue: SSL Certificate Verification Failed

**Symptoms:**
```
ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Diagnostic Steps:**

1. **Check Certificate**
   ```bash
   openssl s_client -connect gitlab.example.com:443 -showcerts
   ```

2. **Verify SSL Configuration**
   ```bash
   echo $GITLAB_VERIFY_SSL
   # Should output: true (or false for development)
   ```

**Fixes:**

1. **Self-Signed Certificate (Development Only)**
   ```bash
   export GITLAB_VERIFY_SSL=false
   ```

   ⚠️ **Warning:** Never use in production!

2. **Custom CA Certificate**
   ```bash
   # Set path to custom CA bundle
   export SSL_CERT_FILE=/path/to/ca-bundle.crt
   export REQUESTS_CA_BUNDLE=/path/to/ca-bundle.crt
   ```

3. **Update System Certificates**
   ```bash
   # macOS
   sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /path/to/cert.pem

   # Ubuntu/Debian
   sudo cp /path/to/cert.crt /usr/local/share/ca-certificates/
   sudo update-ca-certificates

   # RHEL/CentOS
   sudo cp /path/to/cert.crt /etc/pki/ca-trust/source/anchors/
   sudo update-ca-trust
   ```

### Issue: SSL Handshake Timeout

**Symptoms:**
```
ssl.SSLError: The handshake operation timed out
```

**Fixes:**

1. **Increase Timeout**
   ```bash
   export GITLAB_TIMEOUT=60  # Increase to 60 seconds
   ```

2. **Check Network Latency**
   ```bash
   ping gitlab.example.com
   ```

3. **Check Firewall/Proxy**
   - Ensure HTTPS (port 443) is not blocked
   - Configure proxy if required

---

## Performance Issues

### Issue: Slow API Responses

**Symptoms:**
- Operations take longer than expected
- Timeout errors occur frequently

**Diagnostic Steps:**

1. **Measure API Response Time**
   ```bash
   time curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
             https://gitlab.example.com/api/v4/projects?per_page=10
   ```

2. **Check GitLab Performance**
   - Visit GitLab web interface
   - Check if it's slow for web users too

**Fixes:**

1. **Increase Timeout**
   ```bash
   export GITLAB_TIMEOUT=120  # 2 minutes
   ```

2. **Reduce Page Size**
   - Use smaller `per_page` values (default: 20, max: 100)
   - Paginate through results instead of fetching all at once

3. **Use Pagination Efficiently**
   ```python
   # Good: Use pagination
   for page in range(1, 6):
       projects = client.list_projects(page=page, per_page=20)

   # Bad: Request all at once
   projects = client.list_projects(per_page=100)  # Slow!
   ```

4. **Filter Results**
   ```python
   # Filter on server-side (fast)
   issues = client.list_issues(
       project_id="my/project",
       state="opened",
       labels="bug"
   )
   ```

### Issue: Rate Limiting

**Symptoms:**
```
RateLimitError: API rate limit exceeded
```

**Diagnostic Steps:**

1. **Check Rate Limit Status**
   ```bash
   curl -I -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
            https://gitlab.example.com/api/v4/user
   # Look for: RateLimit-Limit, RateLimit-Remaining, RateLimit-Reset
   ```

**Fixes:**

1. **Add Delays Between Requests**
   ```python
   import time

   for project in projects:
       result = client.get_project(project["id"])
       time.sleep(0.1)  # 100ms delay
   ```

2. **Use Batch Operations**
   - Fetch multiple items in single request where possible
   - Use search instead of multiple individual queries

3. **Increase Rate Limits (Self-Hosted)**
   - Contact GitLab admin to increase limits
   - Configure in `/etc/gitlab/gitlab.rb`:
     ```ruby
     gitlab_rails['rate_limit_requests_per_period'] = 1000
     ```

---

## Tool Errors

### Issue: Tool Not Found

**Symptoms:**
```
Error: Tool 'gitlab_list_projects' not found
```

**Diagnostic Steps:**

1. **Verify Server is Running**
   ```bash
   python -m gitlab_mcp.server
   ```

2. **Check Tool Registration**
   ```python
   from gitlab_mcp.server import list_tools
   tools = list_tools()
   print([t.name for t in tools])
   ```

**Fixes:**

1. **Restart MCP Server**
   - Quit Claude Code
   - Restart Claude Code

2. **Verify Installation**
   ```bash
   pip install -e "."
   ```

### Issue: Tool Returns Error

**Symptoms:**
```
Error: NotFoundError: Project not found
```

**Diagnostic Steps:**

1. **Verify Arguments**
   - Check project ID/path is correct
   - Verify you have access to the resource

2. **Test Directly**
   ```python
   from gitlab_mcp.client.gitlab_client import GitLabClient
   from gitlab_mcp.config.settings import load_config

   config = load_config()
   client = GitLabClient(config)

   # Test directly
   project = client.get_project("my/project")
   print(project.name)
   ```

**Common Fixes:**

1. **Project Not Found**
   ```python
   # Bad: Using project name
   project = client.get_project("myproject")

   # Good: Using full path
   project = client.get_project("group/myproject")

   # Good: Using project ID
   project = client.get_project(123)
   ```

2. **Issue Not Found**
   ```python
   # Use IID (issue number), not ID
   issue = client.get_issue(project_id="my/project", issue_iid=42)
   ```

3. **Permission Denied**
   - Verify you have appropriate project role
   - Check token scopes

---

## Debug Mode

### Enabling Debug Logging

1. **Environment Variable**
   ```bash
   export GITLAB_LOG_LEVEL=DEBUG
   python -m gitlab_mcp.server
   ```

2. **Configuration File**
   ```json
   {
     "gitlab_url": "https://gitlab.example.com",
     "gitlab_token": "glpat-xxxxxxxxxxxxxxxxxxxx",
     "log_level": "DEBUG"
   }
   ```

3. **Claude Code Configuration**
   ```json
   {
     "mcpServers": {
       "gitlab": {
         "command": "python",
         "args": ["-m", "gitlab_mcp.server"],
         "env": {
           "GITLAB_URL": "https://gitlab.example.com",
           "GITLAB_TOKEN": "glpat-xxxxxxxxxxxxxxxxxxxx",
           "GITLAB_LOG_LEVEL": "DEBUG"
         }
       }
     }
   }
   ```

### Reading Debug Logs

Debug logs show:
- API requests and responses
- Authentication attempts
- Error details
- Performance metrics

Example debug output:
```
2024-10-24 12:34:56 DEBUG gitlab_mcp.client Authenticating with GitLab
2024-10-24 12:34:56 DEBUG gitlab_mcp.client GET https://gitlab.com/api/v4/user
2024-10-24 12:34:57 DEBUG gitlab_mcp.client Response: 200 OK
2024-10-24 12:34:57 INFO gitlab_mcp.client Successfully authenticated as: username
```

### Collecting Debug Information

When reporting issues, include:

```bash
# 1. Configuration (redact sensitive data!)
echo "GitLab URL: $GITLAB_URL"
echo "Python version: $(python --version)"
echo "Platform: $(uname -a)"

# 2. Package versions
pip list | grep -E "(gitlab|mcp|pydantic)"

# 3. Test connection
python -c "
from gitlab_mcp.config.settings import load_config
from gitlab_mcp.client.gitlab_client import GitLabClient

config = load_config()
print(f'URL: {config.gitlab_url}')
print(f'Timeout: {config.timeout}')
print(f'SSL Verify: {config.verify_ssl}')

client = GitLabClient(config)
user = client.get_current_user()
print(f'Authenticated as: {user.username}')
"
```

---

## Common Error Messages

| Error Message | Likely Cause | Fix |
|---------------|-------------|-----|
| `ValidationError: gitlab_url: field required` | Missing URL | Set `GITLAB_URL` |
| `ValidationError: gitlab_token: field required` | Missing token | Set `GITLAB_TOKEN` |
| `AuthenticationError: GitLab authentication failed` | Invalid token | Check token validity |
| `NotFoundError: Project not found` | Invalid project ID/path | Verify project exists |
| `PermissionError: Forbidden` | Insufficient permissions | Check project role |
| `GitLabAPIError: 401 Unauthorized` | Token expired/invalid | Create new token |
| `GitLabAPIError: 404 Not Found` | Resource doesn't exist | Verify ID/path |
| `GitLabAPIError: 500 Internal Server Error` | GitLab server error | Check GitLab status |
| `RateLimitError: Too many requests` | Rate limit exceeded | Add delays, reduce requests |
| `ssl.SSLError` | SSL certificate issue | See [SSL/TLS Errors](#ssltls-errors) |

---

## Getting Help

### Before Asking for Help

1. ✅ Check this troubleshooting guide
2. ✅ Enable debug logging
3. ✅ Test with curl to isolate issue
4. ✅ Verify GitLab instance is accessible
5. ✅ Check token hasn't expired

### Where to Get Help

1. **Documentation**
   - [Installation Guide](installation.md)
   - [Configuration Guide](configuration.md)
   - [Tools Reference](../api/tools_reference.md)

2. **GitLab Issues**
   - Search existing issues: https://gitlab.prod.thezephyrco.com/mcps/gitlab_mcp/-/issues
   - Create new issue (include debug info)

3. **Community**
   - GitLab Community Forum
   - Stack Overflow (tag: `gitlab-mcp-server`)

### Creating a Bug Report

Include:

1. **Environment Information**
   - Python version
   - Operating system
   - GitLab version (if self-hosted)

2. **Configuration** (redact sensitive data!)
   ```bash
   GitLab URL: https://gitlab.example.com
   Timeout: 30s
   SSL Verify: true
   ```

3. **Error Message**
   - Full error traceback
   - Debug logs (if applicable)

4. **Steps to Reproduce**
   - Minimal code example
   - Expected vs actual behavior

5. **Attempted Fixes**
   - What you've already tried
   - Results of those attempts

---

## Additional Resources

- **GitLab API Status**: Check your instance's status page
- **GitLab Documentation**: https://docs.gitlab.com/ee/api/
- **python-gitlab Docs**: https://python-gitlab.readthedocs.io/
- **MCP Protocol**: https://github.com/anthropics/mcp

---

**Still Stuck?** Open an issue with detailed debug information, and we'll help you resolve it!
