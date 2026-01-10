# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

**Do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them through one of these channels:

1. **GitHub Security Advisories** (Preferred)
   - Go to the [Security tab](https://github.com/wadew/gitlab-mcp/security/advisories)
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Email**
   - Send details to: wade.woolwine@gmail.com
   - Use subject line: `[SECURITY] gitlab-mcp vulnerability report`

### What to Include

Please include as much of the following information as possible:

- Type of vulnerability (e.g., authentication bypass, injection, etc.)
- Full paths of affected source files
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact assessment (what an attacker could achieve)

### Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Update**: Within 7 days with assessment
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Within 90 days

### Disclosure Policy

- We will acknowledge receipt of your report within 48 hours
- We will confirm the vulnerability and determine its impact
- We will release a fix as soon as possible, depending on severity
- We will publicly disclose the vulnerability after a fix is available
- We will credit you in the security advisory (unless you prefer anonymity)

## Security Best Practices

When using gitlab-mcp, follow these security best practices:

### Token Management

```bash
# Store tokens in environment variables, never in code
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"

# Or use a .env file (ensure it's in .gitignore)
echo "GITLAB_TOKEN=glpat-xxxx" >> .env
```

### Token Scopes

Use the minimum required scopes for your use case:

| Scope | When Needed |
|-------|-------------|
| `read_api` | Read-only operations |
| `api` | Full API access (required for write operations) |
| `read_repository` | Repository read access |
| `write_repository` | Repository write access |

### SSL/TLS Verification

Always verify SSL certificates in production:

```bash
# Enable SSL verification (default)
GITLAB_VERIFY_SSL=true

# Only disable for testing with self-signed certs
GITLAB_VERIFY_SSL=false  # Not recommended for production
```

### Network Security

- Run gitlab-mcp on localhost when possible
- Use TLS for HTTP transport mode
- Restrict access to the MCP server port

## Known Security Considerations

### Token Exposure

- GitLab tokens provide access to your GitLab instance
- Never commit tokens to version control
- Rotate tokens regularly
- Use project-specific tokens when possible

### API Rate Limiting

- gitlab-mcp respects GitLab's rate limits
- Excessive API calls may trigger rate limiting
- Monitor your API usage

### Data Sensitivity

- gitlab-mcp can access sensitive repository data
- Code, issues, and merge requests may contain sensitive information
- Ensure proper access controls on your GitLab projects

## Security Updates

Security updates are released as patch versions (e.g., 1.0.1). To stay updated:

```bash
# Update to latest version
pip install --upgrade gitlab-mcp

# Or pin to a specific secure version
pip install gitlab-mcp==1.0.1
```

## Acknowledgments

We appreciate security researchers who help keep gitlab-mcp secure. Contributors who report valid security issues will be acknowledged in our security advisories (with their permission).
