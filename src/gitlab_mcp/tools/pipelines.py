"""
Pipelines tools for GitLab MCP server.

This module provides MCP tools for GitLab CI/CD pipeline and job operations including:
- Listing pipelines
- Getting pipeline details
- Creating, retrying, canceling, and deleting pipelines
- Listing pipeline jobs
- Getting job details and logs
- Retrying, canceling, and playing jobs
- Downloading job artifacts
- Listing pipeline variables

All tools are async functions that accept a GitLabClient and return formatted data.
"""

from typing import Any, Optional, Union

from gitlab_mcp.client.gitlab_client import GitLabClient


async def list_pipelines(
    client: GitLabClient,
    project_id: Union[str, int],
    ref: Optional[str] = None,
    status: Optional[str] = None,
    page: int = 1,
    per_page: int = 20,
) -> dict[str, Any]:
    """
    List pipelines for a project.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        ref: Filter by ref (branch/tag name)
        status: Filter by status (running, pending, success, failed, canceled, skipped)
        page: Page number for pagination
        per_page: Results per page (max 100)

    Returns:
        Dictionary with pipelines list and pagination info
    """
    result = client.list_pipelines(
        project_id=project_id,
        ref=ref,
        status=status,
        page=page,
        per_page=per_page,
    )

    # Extract pipeline list from result dict
    pipelines = result.get("pipelines", [])

    formatted_pipelines = []
    for pipeline in pipelines:
        formatted_pipelines.append(
            {
                "id": pipeline["id"],
                "status": pipeline["status"],
                "ref": pipeline["ref"],
                "sha": pipeline["sha"],
                "web_url": pipeline["web_url"],
                "created_at": pipeline.get("created_at"),
                "updated_at": pipeline.get("updated_at"),
            }
        )

    return {
        "pipelines": formatted_pipelines,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(formatted_pipelines),
        },
    }


async def get_pipeline(
    client: GitLabClient,
    project_id: Union[str, int],
    pipeline_id: int,
) -> dict[str, Any]:
    """
    Get detailed information about a specific pipeline.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        pipeline_id: Pipeline ID

    Returns:
        Dictionary with pipeline details
    """
    pipeline = client.get_pipeline(project_id=project_id, pipeline_id=pipeline_id)

    return {
        "id": pipeline["id"],
        "status": pipeline["status"],
        "ref": pipeline["ref"],
        "sha": pipeline["sha"],
        "web_url": pipeline["web_url"],
        "created_at": pipeline.get("created_at"),
        "updated_at": pipeline.get("updated_at"),
        "started_at": pipeline.get("started_at"),
        "finished_at": pipeline.get("finished_at"),
        "duration": pipeline.get("duration"),
    }


async def create_pipeline(
    client: GitLabClient,
    project_id: Union[str, int],
    ref: str,
    variables: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    """
    Create (trigger) a new pipeline.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        ref: Branch or tag name
        variables: Pipeline variables as key-value pairs (optional)

    Returns:
        Dictionary with created pipeline details
    """
    pipeline = client.create_pipeline(
        project_id=project_id,
        ref=ref,
        variables=variables,
    )

    return {
        "id": pipeline["id"],
        "status": pipeline["status"],
        "ref": pipeline["ref"],
        "sha": pipeline["sha"],
        "web_url": pipeline["web_url"],
        "created_at": pipeline.get("created_at"),
    }


async def retry_pipeline(
    client: GitLabClient,
    project_id: Union[str, int],
    pipeline_id: int,
) -> dict[str, Any]:
    """
    Retry a failed pipeline.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        pipeline_id: Pipeline ID to retry

    Returns:
        Dictionary with retried pipeline details
    """
    result = client.retry_pipeline(project_id=project_id, pipeline_id=pipeline_id)

    return {
        "id": result["id"],
        "status": result["status"],
        "message": result["message"],
    }


async def cancel_pipeline(
    client: GitLabClient,
    project_id: Union[str, int],
    pipeline_id: int,
) -> dict[str, Any]:
    """
    Cancel a running pipeline.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        pipeline_id: Pipeline ID to cancel

    Returns:
        Dictionary with canceled pipeline details
    """
    result = client.cancel_pipeline(project_id=project_id, pipeline_id=pipeline_id)

    return {
        "id": result["id"],
        "status": result["status"],
        "message": result["message"],
    }


async def delete_pipeline(
    client: GitLabClient,
    project_id: Union[str, int],
    pipeline_id: int,
) -> dict[str, Any]:
    """
    Delete a pipeline.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        pipeline_id: Pipeline ID to delete

    Returns:
        Dictionary with deletion confirmation
    """
    result = client.delete_pipeline(project_id=project_id, pipeline_id=pipeline_id)

    return {
        "pipeline_id": result["pipeline_id"],
        "message": result["message"],
    }


async def list_pipeline_jobs(
    client: GitLabClient,
    project_id: Union[str, int],
    pipeline_id: int,
    page: int = 1,
    per_page: int = 20,
) -> list[dict[str, Any]]:
    """
    List jobs in a pipeline.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        pipeline_id: Pipeline ID
        page: Page number for pagination
        per_page: Results per page

    Returns:
        List of job dictionaries
    """
    return client.list_pipeline_jobs(
        project_id=project_id,
        pipeline_id=pipeline_id,
        page=page,
        per_page=per_page,
    )


async def get_job(
    client: GitLabClient,
    project_id: Union[str, int],
    job_id: int,
) -> dict[str, Any]:
    """
    Get detailed information about a specific job.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        job_id: Job ID

    Returns:
        Dictionary with job details
    """
    job = client.get_job(project_id=project_id, job_id=job_id)

    return {
        "id": job["id"],
        "name": job["name"],
        "stage": job["stage"],
        "status": job["status"],
        "ref": job["ref"],
        "web_url": job["web_url"],
        "created_at": job.get("created_at"),
        "started_at": job.get("started_at"),
        "finished_at": job.get("finished_at"),
        "duration": job.get("duration"),
        "pipeline": job.get("pipeline", {}),
    }


async def get_job_trace(
    client: GitLabClient,
    project_id: Union[str, int],
    job_id: int,
) -> dict[str, Any]:
    """
    Get execution log (trace) for a job.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        job_id: Job ID

    Returns:
        Dictionary with job trace/log
    """
    trace = client.get_job_trace(project_id=project_id, job_id=job_id)

    return {
        "job_id": trace["job_id"],
        "trace": trace["trace"],
    }


async def retry_job(
    client: GitLabClient,
    project_id: Union[str, int],
    job_id: int,
) -> dict[str, Any]:
    """
    Retry a failed job.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        job_id: Job ID to retry

    Returns:
        Dictionary with retried job details
    """
    result = client.retry_job(project_id=project_id, job_id=job_id)

    return {
        "job_id": result["job_id"],
        "status": result["status"],
        "message": result["message"],
    }


async def cancel_job(
    client: GitLabClient,
    project_id: Union[str, int],
    job_id: int,
) -> dict[str, Any]:
    """
    Cancel a running job.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        job_id: Job ID to cancel

    Returns:
        Dictionary with canceled job details
    """
    result = client.cancel_job(project_id=project_id, job_id=job_id)

    return {
        "job_id": result["job_id"],
        "status": result["status"],
        "message": result["message"],
    }


async def play_job(
    client: GitLabClient,
    project_id: Union[str, int],
    job_id: int,
) -> dict[str, Any]:
    """
    Start a manual job.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        job_id: Job ID to play/start

    Returns:
        Dictionary with job details
    """
    result = client.play_job(project_id=project_id, job_id=job_id)

    return {
        "job_id": result["job_id"],
        "status": result["status"],
        "message": result["message"],
    }


async def download_job_artifacts(
    client: GitLabClient,
    project_id: Union[str, int],
    job_id: int,
) -> dict[str, Any]:
    """
    Download job artifacts.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        job_id: Job ID

    Returns:
        Dictionary with artifacts info
    """
    result = client.download_job_artifacts(project_id=project_id, job_id=job_id)

    return {
        "job_id": result["job_id"],
        "size_bytes": result["size_bytes"],
        "message": f"Downloaded {result['size_bytes']} bytes of artifacts for job {job_id}",
    }


async def list_pipeline_variables(
    client: GitLabClient,
    project_id: Union[str, int],
    pipeline_id: int,
) -> list[dict[str, str]]:
    """
    List variables for a pipeline.

    Args:
        client: Authenticated GitLabClient instance
        project_id: Project ID (int) or path (str)
        pipeline_id: Pipeline ID

    Returns:
        List of variable dictionaries
    """
    return client.list_pipeline_variables(project_id=project_id, pipeline_id=pipeline_id)
