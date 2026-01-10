# Contributing to gitlab-mcp

Thank you for your interest in contributing to gitlab-mcp! This document provides guidelines and instructions for contributing.

## Development Philosophy

This project follows **strict Test-Driven Development (TDD)**:

1. **Red**: Write a failing test that defines desired behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code while keeping tests green

**No exceptions. No shortcuts. No "I'll add tests later."**

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/wadew/gitlab-mcp.git
cd gitlab-mcp

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/gitlab_mcp --cov-report=term-missing

# Run specific test types
pytest tests/unit/ -v -m unit
pytest tests/integration/ -v -m integration
pytest tests/e2e/ -v -m e2e

# Type checking
mypy src/gitlab_mcp

# Linting
ruff check src/ tests/

# Formatting
black src/ tests/
```

## Code Quality Standards

### Minimum Requirements

- **80%+ code coverage** - Tests must cover at least 80% of new code
- **100% test pass rate** - All tests must pass
- **Zero mypy errors** - Full type safety required
- **Zero ruff errors** - All linting rules must pass
- **Black formatted** - Code must be formatted with black

### Type Hints

All functions must have type hints:

```python
def create_issue(
    project_id: str,
    title: str,
    description: str | None = None,
    labels: list[str] | None = None,
) -> Issue:
    """Create a new issue in a GitLab project."""
    ...
```

### Docstrings

Every module, class, and public function must have docstrings:

```python
def get_merge_request(project_id: str, mr_iid: int) -> MergeRequest:
    """Get details of a specific merge request.

    Args:
        project_id: The project ID or path (e.g., "mygroup/myproject")
        mr_iid: The merge request internal ID

    Returns:
        MergeRequest object with full details

    Raises:
        GitLabNotFoundError: If the merge request doesn't exist
        GitLabAuthError: If authentication fails
    """
    ...
```

### Test Naming

Follow this pattern: `test_<function>_<scenario>_<expected>`

```python
def test_get_issue_valid_id_returns_issue():
    pass

def test_get_issue_invalid_id_raises_not_found():
    pass

def test_create_merge_request_missing_title_raises_validation_error():
    pass
```

## Making Changes

### 1. Create a Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### 2. Write Tests First (TDD)

```python
# tests/unit/test_your_feature.py
def test_your_feature_does_something():
    # Arrange
    ...
    # Act
    result = your_feature()
    # Assert
    assert result == expected
```

### 3. Implement the Feature

Write the minimal code needed to make the test pass.

### 4. Run Quality Checks

```bash
# All tests pass
pytest tests/ -v

# Coverage meets threshold
pytest tests/ --cov=src/gitlab_mcp --cov-fail-under=80

# Type checking
mypy src/gitlab_mcp

# Linting
ruff check src/ tests/

# Formatting
black --check src/ tests/
```

### 5. Commit Your Changes

Follow the commit message format:

```
<type>(<scope>): <subject>

<body>

Coverage: X% (+/-Y%)
Tests: N passing
```

**Types**: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`

**Example**:
```
feat(issues): add issue label management

Implement add_issue_labels and remove_issue_label tools
for managing labels on GitLab issues.

- Add unit tests for label operations
- Add integration test with real GitLab API
- Update tools_reference.md documentation

Coverage: 85% (+2%)
Tests: 1270 passing
```

### 6. Submit a Pull Request

1. Push your branch to GitHub
2. Open a Pull Request against `develop`
3. Fill out the PR template
4. Wait for CI checks to pass
5. Address any review feedback

## Pull Request Guidelines

### PR Checklist

- [ ] Tests written (TDD approach followed)
- [ ] All tests passing
- [ ] Coverage >= 80%
- [ ] Type checking passes (mypy)
- [ ] Linting passes (ruff)
- [ ] Code formatted (black)
- [ ] Documentation updated (if user-facing)
- [ ] CHANGELOG updated (if notable change)

### PR Size

Keep PRs focused and reasonably sized:
- One feature or fix per PR
- If a change is large, consider splitting it
- Include only related changes

## Reporting Issues

### Bug Reports

When reporting bugs, include:

1. Python version and OS
2. gitlab-mcp version
3. GitLab server version
4. Steps to reproduce
5. Expected vs actual behavior
6. Error messages/stack traces

### Feature Requests

When requesting features:

1. Describe the use case
2. Explain the expected behavior
3. Consider implementation approach
4. Note any alternatives considered

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Questions?

- Open a [GitHub Discussion](https://github.com/wadew/gitlab-mcp/discussions)
- Check existing [Issues](https://github.com/wadew/gitlab-mcp/issues)
- Read the [Documentation](https://github.com/wadew/gitlab-mcp#documentation)

## License

By contributing to gitlab-mcp, you agree that your contributions will be licensed under the MIT License.
