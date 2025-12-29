"""Unit tests for Resource Registry.

Tests verify:
- URI parsing for gitlab:// scheme
- Static resource matching
- Resource template matching with parameters
- Parameter extraction from URIs
- Invalid URI handling
"""

import pytest


class TestURIParsing:
    """Test URI parsing for gitlab:// scheme."""

    def test_parse_simple_uri(self):
        """Parse simple gitlab://projects URI."""
        from gitlab_mcp.resources.registry import parse_resource_uri

        result = parse_resource_uri("gitlab://projects")
        assert result is not None
        assert result["scheme"] == "gitlab"
        assert result["path"] == "projects"
        assert result["params"] == {}

    def test_parse_uri_with_path_segments(self):
        """Parse URI with multiple path segments."""
        from gitlab_mcp.resources.registry import parse_resource_uri

        result = parse_resource_uri("gitlab://project/123/issues")
        assert result["path"] == "project/123/issues"

    def test_parse_uri_with_user_current(self):
        """Parse user/current URI."""
        from gitlab_mcp.resources.registry import parse_resource_uri

        result = parse_resource_uri("gitlab://user/current")
        assert result["path"] == "user/current"

    def test_parse_invalid_scheme_returns_none(self):
        """Invalid scheme should return None."""
        from gitlab_mcp.resources.registry import parse_resource_uri

        result = parse_resource_uri("http://example.com")
        assert result is None

    def test_parse_empty_uri_returns_none(self):
        """Empty URI should return None."""
        from gitlab_mcp.resources.registry import parse_resource_uri

        result = parse_resource_uri("")
        assert result is None

    def test_parse_malformed_uri_returns_none(self):
        """Malformed URI should return None."""
        from gitlab_mcp.resources.registry import parse_resource_uri

        result = parse_resource_uri("not-a-valid-uri")
        assert result is None


class TestResourceRegistry:
    """Test resource registry for matching URIs to handlers."""

    @pytest.fixture
    def registry(self):
        """Create a resource registry instance."""
        from gitlab_mcp.resources.registry import ResourceRegistry

        return ResourceRegistry()

    def test_registry_has_static_resources(self, registry):
        """Registry should have static resources defined."""
        static = registry.get_static_resources()
        assert isinstance(static, list)
        assert len(static) > 0

    def test_registry_has_resource_templates(self, registry):
        """Registry should have resource templates defined."""
        templates = registry.get_resource_templates()
        assert isinstance(templates, list)
        assert len(templates) > 0

    def test_static_resource_projects_exists(self, registry):
        """Static resource gitlab://projects should exist."""
        static = registry.get_static_resources()
        uris = [r["uri"] for r in static]
        assert "gitlab://projects" in uris

    def test_static_resource_user_current_exists(self, registry):
        """Static resource gitlab://user/current should exist."""
        static = registry.get_static_resources()
        uris = [r["uri"] for r in static]
        assert "gitlab://user/current" in uris

    def test_static_resource_groups_exists(self, registry):
        """Static resource gitlab://groups should exist."""
        static = registry.get_static_resources()
        uris = [r["uri"] for r in static]
        assert "gitlab://groups" in uris

    def test_template_project_details_exists(self, registry):
        """Template gitlab://project/{project_id} should exist."""
        templates = registry.get_resource_templates()
        patterns = [t["uri_template"] for t in templates]
        assert "gitlab://project/{project_id}" in patterns

    def test_template_project_readme_exists(self, registry):
        """Template gitlab://project/{project_id}/readme should exist."""
        templates = registry.get_resource_templates()
        patterns = [t["uri_template"] for t in templates]
        assert "gitlab://project/{project_id}/readme" in patterns

    def test_template_project_issues_exists(self, registry):
        """Template gitlab://project/{project_id}/issues/open should exist."""
        templates = registry.get_resource_templates()
        patterns = [t["uri_template"] for t in templates]
        assert "gitlab://project/{project_id}/issues/open" in patterns


class TestURITemplateMatching:
    """Test URI template matching and parameter extraction."""

    @pytest.fixture
    def registry(self):
        """Create a resource registry instance."""
        from gitlab_mcp.resources.registry import ResourceRegistry

        return ResourceRegistry()

    def test_match_project_template(self, registry):
        """Match gitlab://project/123 to template."""
        match = registry.match_uri("gitlab://project/123")
        assert match is not None
        assert match["template"] == "gitlab://project/{project_id}"
        assert match["params"]["project_id"] == "123"

    def test_match_project_with_namespace(self, registry):
        """Match gitlab://project/group/subgroup/repo to template."""
        match = registry.match_uri("gitlab://project/group/subgroup/repo")
        assert match is not None
        assert match["params"]["project_id"] == "group/subgroup/repo"

    def test_match_project_readme(self, registry):
        """Match gitlab://project/123/readme to template."""
        match = registry.match_uri("gitlab://project/123/readme")
        assert match is not None
        assert match["template"] == "gitlab://project/{project_id}/readme"
        assert match["params"]["project_id"] == "123"

    def test_match_project_issues(self, registry):
        """Match gitlab://project/123/issues/open to template."""
        match = registry.match_uri("gitlab://project/123/issues/open")
        assert match is not None
        assert match["params"]["project_id"] == "123"

    def test_match_project_issue_by_iid(self, registry):
        """Match gitlab://project/123/issues/5 to template."""
        match = registry.match_uri("gitlab://project/123/issues/5")
        assert match is not None
        assert match["params"]["project_id"] == "123"
        assert match["params"]["iid"] == "5"

    def test_match_static_resource(self, registry):
        """Match static resource gitlab://projects."""
        match = registry.match_uri("gitlab://projects")
        assert match is not None
        assert match["is_static"] is True
        assert match["params"] == {}

    def test_no_match_for_unknown_uri(self, registry):
        """Unknown URI should return None."""
        match = registry.match_uri("gitlab://unknown/path")
        assert match is None


class TestResourceMetadata:
    """Test resource metadata (name, description, mimeType)."""

    @pytest.fixture
    def registry(self):
        """Create a resource registry instance."""
        from gitlab_mcp.resources.registry import ResourceRegistry

        return ResourceRegistry()

    def test_static_resource_has_name(self, registry):
        """Static resources should have a name."""
        static = registry.get_static_resources()
        for resource in static:
            assert "name" in resource
            assert len(resource["name"]) > 0

    def test_static_resource_has_description(self, registry):
        """Static resources should have a description."""
        static = registry.get_static_resources()
        for resource in static:
            assert "description" in resource
            assert len(resource["description"]) > 0

    def test_static_resource_has_mime_type(self, registry):
        """Static resources should have a mimeType."""
        static = registry.get_static_resources()
        for resource in static:
            assert "mime_type" in resource
            assert resource["mime_type"] in ["application/json", "text/markdown", "text/yaml"]

    def test_template_has_name(self, registry):
        """Resource templates should have a name."""
        templates = registry.get_resource_templates()
        for template in templates:
            assert "name" in template
            assert len(template["name"]) > 0

    def test_template_has_description(self, registry):
        """Resource templates should have a description."""
        templates = registry.get_resource_templates()
        for template in templates:
            assert "description" in template
            assert len(template["description"]) > 0

    def test_template_has_mime_type(self, registry):
        """Resource templates should have a mimeType."""
        templates = registry.get_resource_templates()
        for template in templates:
            assert "mime_type" in template


class TestResourceCounts:
    """Test expected resource counts."""

    @pytest.fixture
    def registry(self):
        """Create a resource registry instance."""
        from gitlab_mcp.resources.registry import ResourceRegistry

        return ResourceRegistry()

    def test_static_resource_count(self, registry):
        """Should have 3 static resources."""
        static = registry.get_static_resources()
        assert len(static) == 3  # projects, user/current, groups

    def test_resource_template_count(self, registry):
        """Should have expected number of resource templates."""
        templates = registry.get_resource_templates()
        # project, project/readme, project/.gitlab-ci.yml, project/issues/open,
        # project/issues/{iid}, project/mrs/open, project/mrs/{iid},
        # project/pipelines/recent, project/pipelines/{id}, project/branches,
        # project/file/{path}
        assert len(templates) >= 10
