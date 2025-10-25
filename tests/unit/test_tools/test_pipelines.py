"""
Unit tests for pipeline tools.

Tests the MCP tools for GitLab CI/CD pipeline operations including:
- Listing pipelines
- Getting pipeline details
- Creating, retrying, canceling, and deleting pipelines
- Listing pipeline jobs
- Getting job details and logs
- Retrying, canceling, and playing jobs
- Downloading job artifacts
- Listing pipeline variables
"""

from unittest.mock import Mock

import pytest

from gitlab_mcp.tools.pipelines import (
    cancel_job,
    cancel_pipeline,
    create_pipeline,
    delete_pipeline,
    download_job_artifacts,
    get_job,
    get_job_trace,
    get_pipeline,
    list_pipeline_jobs,
    list_pipeline_variables,
    list_pipelines,
    play_job,
    retry_job,
    retry_pipeline,
)


class TestListPipelines:
    """Test list_pipelines tool."""

    @pytest.mark.asyncio
    async def test_list_pipelines_returns_formatted_list(self):
        """Test listing pipelines with proper formatting."""
        mock_client = Mock()
        mock_client.list_pipelines = Mock(
            return_value={
                "pipelines": [
                    {
                        "id": 1,
                        "status": "success",
                        "ref": "main",
                        "sha": "abc123",
                        "web_url": "https://gitlab.example.com/project/pipelines/1",
                        "created_at": "2025-10-23T10:00:00Z",
                        "updated_at": "2025-10-23T10:30:00Z",
                    },
                    {
                        "id": 2,
                        "status": "failed",
                        "ref": "develop",
                        "sha": "def456",
                        "web_url": "https://gitlab.example.com/project/pipelines/2",
                        "created_at": "2025-10-23T11:00:00Z",
                        "updated_at": "2025-10-23T11:15:00Z",
                    },
                ]
            }
        )

        result = await list_pipelines(mock_client, "project/path")

        mock_client.list_pipelines.assert_called_once_with(
            project_id="project/path",
            ref=None,
            status=None,
            page=1,
            per_page=20,
        )
        assert len(result["pipelines"]) == 2
        assert result["pipelines"][0]["id"] == 1
        assert result["pipelines"][0]["status"] == "success"
        assert result["pipelines"][1]["id"] == 2
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["per_page"] == 20

    @pytest.mark.asyncio
    async def test_list_pipelines_with_filters(self):
        """Test listing pipelines with ref and status filters."""
        mock_client = Mock()
        mock_client.list_pipelines = Mock(
            return_value={
                "pipelines": [
                    {
                        "id": 1,
                        "status": "running",
                        "ref": "main",
                        "sha": "abc123",
                        "web_url": "https://gitlab.example.com/project/pipelines/1",
                        "created_at": "2025-10-23T10:00:00Z",
                        "updated_at": "2025-10-23T10:30:00Z",
                    }
                ]
            }
        )

        result = await list_pipelines(
            mock_client, 123, ref="main", status="running", page=2, per_page=50
        )

        mock_client.list_pipelines.assert_called_once_with(
            project_id=123,
            ref="main",
            status="running",
            page=2,
            per_page=50,
        )
        assert len(result["pipelines"]) == 1
        assert result["pagination"]["page"] == 2
        assert result["pagination"]["per_page"] == 50


class TestGetPipeline:
    """Test get_pipeline tool."""

    @pytest.mark.asyncio
    async def test_get_pipeline_returns_details(self):
        """Test getting pipeline details."""
        mock_client = Mock()
        mock_client.get_pipeline = Mock(
            return_value={
                "id": 123,
                "status": "success",
                "ref": "main",
                "sha": "abc123",
                "web_url": "https://gitlab.example.com/project/pipelines/123",
                "created_at": "2025-10-23T10:00:00Z",
                "updated_at": "2025-10-23T10:30:00Z",
                "started_at": "2025-10-23T10:05:00Z",
                "finished_at": "2025-10-23T10:30:00Z",
                "duration": 1500,
            }
        )

        result = await get_pipeline(mock_client, "project/path", 123)

        mock_client.get_pipeline.assert_called_once_with(project_id="project/path", pipeline_id=123)
        assert result["id"] == 123
        assert result["status"] == "success"
        assert result["ref"] == "main"
        assert result["duration"] == 1500


class TestCreatePipeline:
    """Test create_pipeline tool."""

    @pytest.mark.asyncio
    async def test_create_pipeline_without_variables(self):
        """Test creating pipeline without variables."""
        mock_client = Mock()
        mock_client.create_pipeline = Mock(
            return_value={
                "id": 456,
                "status": "pending",
                "ref": "main",
                "sha": "xyz789",
                "web_url": "https://gitlab.example.com/project/pipelines/456",
                "created_at": "2025-10-23T12:00:00Z",
            }
        )

        result = await create_pipeline(mock_client, 123, "main")

        mock_client.create_pipeline.assert_called_once_with(
            project_id=123, ref="main", variables=None
        )
        assert result["id"] == 456
        assert result["status"] == "pending"
        assert result["ref"] == "main"

    @pytest.mark.asyncio
    async def test_create_pipeline_with_variables(self):
        """Test creating pipeline with variables."""
        mock_client = Mock()
        mock_client.create_pipeline = Mock(
            return_value={
                "id": 789,
                "status": "pending",
                "ref": "develop",
                "sha": "xyz123",
                "web_url": "https://gitlab.example.com/project/pipelines/789",
                "created_at": "2025-10-23T12:00:00Z",
            }
        )

        variables = {"ENV": "production", "DEBUG": "false"}
        result = await create_pipeline(mock_client, "project/path", "develop", variables)

        mock_client.create_pipeline.assert_called_once_with(
            project_id="project/path", ref="develop", variables=variables
        )
        assert result["id"] == 789


class TestRetryPipeline:
    """Test retry_pipeline tool."""

    @pytest.mark.asyncio
    async def test_retry_pipeline_returns_result(self):
        """Test retrying a failed pipeline."""
        mock_client = Mock()
        mock_client.retry_pipeline = Mock(
            return_value={
                "id": 123,
                "status": "pending",
                "message": "Pipeline retry initiated",
            }
        )

        result = await retry_pipeline(mock_client, 456, 123)

        mock_client.retry_pipeline.assert_called_once_with(project_id=456, pipeline_id=123)
        assert result["id"] == 123
        assert result["status"] == "pending"
        assert "retry" in result["message"].lower()


class TestCancelPipeline:
    """Test cancel_pipeline tool."""

    @pytest.mark.asyncio
    async def test_cancel_pipeline_returns_result(self):
        """Test canceling a running pipeline."""
        mock_client = Mock()
        mock_client.cancel_pipeline = Mock(
            return_value={
                "id": 123,
                "status": "canceled",
                "message": "Pipeline canceled",
            }
        )

        result = await cancel_pipeline(mock_client, "project/path", 123)

        mock_client.cancel_pipeline.assert_called_once_with(
            project_id="project/path", pipeline_id=123
        )
        assert result["id"] == 123
        assert result["status"] == "canceled"


class TestDeletePipeline:
    """Test delete_pipeline tool."""

    @pytest.mark.asyncio
    async def test_delete_pipeline_returns_confirmation(self):
        """Test deleting a pipeline."""
        mock_client = Mock()
        mock_client.delete_pipeline = Mock(
            return_value={
                "pipeline_id": 123,
                "message": "Pipeline deleted successfully",
            }
        )

        result = await delete_pipeline(mock_client, 456, 123)

        mock_client.delete_pipeline.assert_called_once_with(project_id=456, pipeline_id=123)
        assert result["pipeline_id"] == 123
        assert "deleted" in result["message"].lower()


class TestListPipelineJobs:
    """Test list_pipeline_jobs tool."""

    @pytest.mark.asyncio
    async def test_list_pipeline_jobs_returns_jobs(self):
        """Test listing jobs in a pipeline."""
        mock_client = Mock()
        mock_jobs = [
            {
                "id": 1,
                "name": "build",
                "stage": "build",
                "status": "success",
                "ref": "main",
                "web_url": "https://gitlab.example.com/project/jobs/1",
                "created_at": "2024-01-01T00:00:00Z",
                "started_at": "2024-01-01T00:01:00Z",
                "finished_at": "2024-01-01T00:05:00Z",
                "duration": 240.0,
                "allow_failure": False,
            },
            {
                "id": 2,
                "name": "test",
                "stage": "test",
                "status": "failed",
                "ref": "main",
                "web_url": "https://gitlab.example.com/project/jobs/2",
                "created_at": "2024-01-01T00:05:00Z",
                "started_at": "2024-01-01T00:06:00Z",
                "finished_at": "2024-01-01T00:07:00Z",
                "duration": 60.0,
                "allow_failure": True,
                "failure_reason": "script_failure",
            },
        ]
        mock_client.list_pipeline_jobs = Mock(return_value=mock_jobs)

        result = await list_pipeline_jobs(mock_client, "project/path", 123)

        mock_client.list_pipeline_jobs.assert_called_once_with(
            project_id="project/path", pipeline_id=123, page=1, per_page=20
        )
        assert len(result) == 2
        assert result[0]["name"] == "build"
        assert result[0]["stage"] == "build"
        assert result[0]["status"] == "success"
        assert result[1]["name"] == "test"
        assert result[1]["failure_reason"] == "script_failure"

    @pytest.mark.asyncio
    async def test_list_pipeline_jobs_with_pagination(self):
        """Test listing jobs with custom pagination."""
        mock_client = Mock()
        mock_client.list_pipeline_jobs = Mock(return_value=[])

        await list_pipeline_jobs(mock_client, 123, 456, page=3, per_page=100)

        mock_client.list_pipeline_jobs.assert_called_once_with(
            project_id=123, pipeline_id=456, page=3, per_page=100
        )


class TestGetJob:
    """Test get_job tool."""

    @pytest.mark.asyncio
    async def test_get_job_returns_details(self):
        """Test getting job details."""
        mock_client = Mock()
        mock_client.get_job = Mock(
            return_value={
                "id": 789,
                "name": "test-job",
                "stage": "test",
                "status": "success",
                "ref": "main",
                "web_url": "https://gitlab.example.com/project/jobs/789",
                "created_at": "2025-10-23T10:00:00Z",
                "started_at": "2025-10-23T10:05:00Z",
                "finished_at": "2025-10-23T10:15:00Z",
                "duration": 600,
                "pipeline": {"id": 123},
            }
        )

        result = await get_job(mock_client, "project/path", 789)

        mock_client.get_job.assert_called_once_with(project_id="project/path", job_id=789)
        assert result["id"] == 789
        assert result["name"] == "test-job"
        assert result["stage"] == "test"
        assert result["status"] == "success"
        assert result["duration"] == 600
        assert result["pipeline"]["id"] == 123


class TestGetJobTrace:
    """Test get_job_trace tool."""

    @pytest.mark.asyncio
    async def test_get_job_trace_full_log(self):
        """Test getting full job trace."""
        mock_client = Mock()
        mock_client.get_job_trace = Mock(
            return_value={
                "job_id": 789,
                "trace": "Job log output here...",
                "truncated": False,
                "total_lines": 100,
                "returned_lines": 100,
            }
        )

        result = await get_job_trace(mock_client, 123, 789)

        mock_client.get_job_trace.assert_called_once_with(
            project_id=123, job_id=789, tail_lines=None
        )
        assert result["job_id"] == 789
        assert result["trace"] == "Job log output here..."
        assert result["truncated"] is False

    @pytest.mark.asyncio
    async def test_get_job_trace_with_tail_lines(self):
        """Test getting job trace with tail_lines limit."""
        mock_client = Mock()
        mock_client.get_job_trace = Mock(
            return_value={
                "job_id": 789,
                "trace": "Last 500 lines...",
                "truncated": True,
                "total_lines": 5000,
                "returned_lines": 500,
            }
        )

        result = await get_job_trace(mock_client, "project/path", 789, tail_lines=500)

        mock_client.get_job_trace.assert_called_once_with(
            project_id="project/path", job_id=789, tail_lines=500
        )
        assert result["truncated"] is True
        assert result["total_lines"] == 5000
        assert result["returned_lines"] == 500


class TestRetryJob:
    """Test retry_job tool."""

    @pytest.mark.asyncio
    async def test_retry_job_returns_result(self):
        """Test retrying a failed job."""
        mock_client = Mock()
        mock_client.retry_job = Mock(
            return_value={
                "job_id": 789,
                "status": "pending",
                "message": "Job retry initiated",
            }
        )

        result = await retry_job(mock_client, 123, 789)

        mock_client.retry_job.assert_called_once_with(project_id=123, job_id=789)
        assert result["job_id"] == 789
        assert result["status"] == "pending"


class TestCancelJob:
    """Test cancel_job tool."""

    @pytest.mark.asyncio
    async def test_cancel_job_returns_result(self):
        """Test canceling a running job."""
        mock_client = Mock()
        mock_client.cancel_job = Mock(
            return_value={
                "job_id": 789,
                "status": "canceled",
                "message": "Job canceled",
            }
        )

        result = await cancel_job(mock_client, "project/path", 789)

        mock_client.cancel_job.assert_called_once_with(project_id="project/path", job_id=789)
        assert result["job_id"] == 789
        assert result["status"] == "canceled"


class TestPlayJob:
    """Test play_job tool."""

    @pytest.mark.asyncio
    async def test_play_job_returns_result(self):
        """Test starting a manual job."""
        mock_client = Mock()
        mock_client.play_job = Mock(
            return_value={
                "job_id": 789,
                "status": "pending",
                "message": "Manual job started",
            }
        )

        result = await play_job(mock_client, 123, 789)

        mock_client.play_job.assert_called_once_with(project_id=123, job_id=789)
        assert result["job_id"] == 789
        assert result["status"] == "pending"


class TestDownloadJobArtifacts:
    """Test download_job_artifacts tool."""

    @pytest.mark.asyncio
    async def test_download_job_artifacts_returns_info(self):
        """Test downloading job artifacts."""
        mock_client = Mock()
        mock_client.download_job_artifacts = Mock(return_value={"job_id": 789, "size_bytes": 12345})

        result = await download_job_artifacts(mock_client, "project/path", 789)

        mock_client.download_job_artifacts.assert_called_once_with(
            project_id="project/path", job_id=789
        )
        assert result["job_id"] == 789
        assert result["size_bytes"] == 12345
        assert "12345" in result["message"]


class TestListPipelineVariables:
    """Test list_pipeline_variables tool."""

    @pytest.mark.asyncio
    async def test_list_pipeline_variables_returns_variables(self):
        """Test listing pipeline variables."""
        mock_client = Mock()
        mock_variables = [
            {"key": "ENV", "value": "production"},
            {"key": "DEBUG", "value": "false"},
        ]
        mock_client.list_pipeline_variables = Mock(return_value=mock_variables)

        result = await list_pipeline_variables(mock_client, 123, 456)

        mock_client.list_pipeline_variables.assert_called_once_with(project_id=123, pipeline_id=456)
        assert len(result) == 2
        assert result[0]["key"] == "ENV"
        assert result[1]["key"] == "DEBUG"
