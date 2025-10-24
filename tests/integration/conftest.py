"""Integration test configuration and fixtures.

This module provides fixtures for integration testing with a real GitLab instance.

Integration tests are marked with @pytest.mark.integration and are designed to
test interactions with a real GitLab API. They require:
- Valid GITLAB_URL and GITLAB_TOKEN environment variables
- Access to a test GitLab instance
- A test project (will use or create one)

These tests are slower than unit tests and may modify data on the GitLab instance.
They should be run separately from unit tests using: pytest tests/integration/ -v -m integration
"""

import os
from typing import Dict

import pytest

from gitlab_mcp.client.gitlab_client import GitLabClient
from gitlab_mcp.config.settings import GitLabConfig


def pytest_configure(config):
    """Register custom markers for integration tests."""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests (use real GitLab API)"
    )
    config.addinivalue_line("markers", "slow: marks tests as slow-running")


def pytest_collection_modifyitems(config, items):
    """Automatically mark integration tests based on file location."""
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
            item.add_marker(pytest.mark.slow)


@pytest.fixture(scope="session")
def integration_config() -> GitLabConfig:
    """Provide GitLab configuration for integration tests.

    Requires GITLAB_URL and GITLAB_TOKEN environment variables to be set.

    Returns:
        GitLabConfig instance configured for integration testing

    Raises:
        pytest.skip: If required environment variables are not set
    """
    gitlab_url = os.getenv("GITLAB_URL")
    gitlab_token = os.getenv("GITLAB_TOKEN")

    if not gitlab_url or not gitlab_token:
        pytest.skip(
            "Integration tests require GITLAB_URL and GITLAB_TOKEN environment variables. "
            "Set them in your .env file or environment."
        )

    # Create config for integration tests
    config = GitLabConfig(
        gitlab_url=gitlab_url,
        gitlab_token=gitlab_token,
        timeout=30,
        log_level="DEBUG",
        verify_ssl=True,
    )

    return config


@pytest.fixture(scope="session")
def gitlab_client(integration_config: GitLabConfig) -> GitLabClient:
    """Provide a configured GitLab client for integration tests.

    This is a session-scoped fixture that creates a single client instance
    for all integration tests.

    Args:
        integration_config: GitLab configuration fixture

    Yields:
        GitLabClient instance ready for use

    Raises:
        pytest.skip: If client initialization fails
    """
    try:
        client = GitLabClient(integration_config)
        # Client will authenticate lazily on first API call
        return client
    except Exception as e:
        pytest.skip(f"Failed to create GitLab client: {e}")


@pytest.fixture(scope="session")
def test_project_info() -> Dict[str, str]:
    """Provide information about the test project to use.

    This fixture defines which project to use for integration tests.
    You can override this by setting GITLAB_TEST_PROJECT_ID env var.

    Returns:
        Dictionary with test project information:
        - project_id: Project ID or path (e.g., "group/project" or "123")
        - description: Human-readable description

    Raises:
        pytest.skip: If no test project is configured
    """
    # Check for environment variable first
    test_project_id = os.getenv("GITLAB_TEST_PROJECT_ID")

    if not test_project_id:
        pytest.skip(
            "Integration tests require a test project. Set GITLAB_TEST_PROJECT_ID "
            "environment variable to a project ID or path (e.g., 'mcps/gitlab_mcp' or '123')"
        )

    return {
        "project_id": test_project_id,
        "description": f"Test project: {test_project_id}",
    }


@pytest.fixture
def test_project_id(test_project_info: Dict[str, str]) -> str:
    """Provide the test project ID as a simple string.

    This is a convenience fixture that just returns the project_id string.

    Args:
        test_project_info: Test project information fixture

    Returns:
        Project ID or path string
    """
    return test_project_info["project_id"]
