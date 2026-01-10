## Description

<!-- Describe your changes in detail -->

## Related Issue

<!-- Link to the issue this PR addresses (if any) -->
Fixes #

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Test improvement
- [ ] Refactoring (no functional changes)

## Checklist

<!-- Mark completed items with an "x" -->

### Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have run `black` and `ruff` on my code
- [ ] I have run `mypy` and there are no type errors
- [ ] I have added docstrings to new functions/classes

### Testing
- [ ] I have written tests following TDD (tests first)
- [ ] All new and existing tests pass (`pytest tests/ -v`)
- [ ] Code coverage is >= 80% for new code
- [ ] I have added integration tests if applicable

### Documentation
- [ ] I have updated the README if needed
- [ ] I have updated the CHANGELOG if this is a notable change
- [ ] I have updated relevant documentation in `docs/`

## Test Results

<!-- Paste test output or coverage report -->

```
pytest tests/ -v --cov=src/gitlab_mcp
```

## Screenshots / Examples

<!-- If applicable, add screenshots or examples showing the change -->

## Additional Notes

<!-- Any additional information reviewers should know -->
