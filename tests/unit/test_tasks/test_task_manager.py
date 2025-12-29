"""Unit tests for MCP Task Manager.

Tests verify:
- Task creation with proper state
- Task state transitions
- Task retrieval and listing
- Task cancellation
- Task metadata handling
"""

from datetime import datetime

import pytest


class TestTaskState:
    """Test TaskState enum."""

    def test_task_state_has_pending(self):
        """TaskState should have PENDING state."""
        from gitlab_mcp.tasks.task_manager import TaskState

        assert hasattr(TaskState, "PENDING")

    def test_task_state_has_working(self):
        """TaskState should have WORKING state."""
        from gitlab_mcp.tasks.task_manager import TaskState

        assert hasattr(TaskState, "WORKING")

    def test_task_state_has_completed(self):
        """TaskState should have COMPLETED state."""
        from gitlab_mcp.tasks.task_manager import TaskState

        assert hasattr(TaskState, "COMPLETED")

    def test_task_state_has_failed(self):
        """TaskState should have FAILED state."""
        from gitlab_mcp.tasks.task_manager import TaskState

        assert hasattr(TaskState, "FAILED")

    def test_task_state_has_cancelled(self):
        """TaskState should have CANCELLED state."""
        from gitlab_mcp.tasks.task_manager import TaskState

        assert hasattr(TaskState, "CANCELLED")


class TestTask:
    """Test Task dataclass."""

    def test_task_has_id(self):
        """Task should have an id field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
        )
        assert task.id == "test-123"

    def test_task_has_task_type(self):
        """Task should have a task_type field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
        )
        assert task.task_type == "pipeline_create"

    def test_task_has_state(self):
        """Task should have a state field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.WORKING,
        )
        assert task.state == TaskState.WORKING

    def test_task_has_metadata(self):
        """Task should have optional metadata field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
            metadata={"project_id": "group/project", "ref": "main"},
        )
        assert task.metadata == {"project_id": "group/project", "ref": "main"}

    def test_task_metadata_defaults_to_none(self):
        """Task metadata should default to None."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
        )
        assert task.metadata is None

    def test_task_has_result(self):
        """Task should have optional result field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.COMPLETED,
            result={"pipeline_id": 500, "status": "success"},
        )
        assert task.result == {"pipeline_id": 500, "status": "success"}

    def test_task_result_defaults_to_none(self):
        """Task result should default to None."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
        )
        assert task.result is None

    def test_task_has_error(self):
        """Task should have optional error field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.FAILED,
            error="Pipeline creation failed: invalid ref",
        )
        assert task.error == "Pipeline creation failed: invalid ref"

    def test_task_error_defaults_to_none(self):
        """Task error should default to None."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
        )
        assert task.error is None

    def test_task_has_created_at(self):
        """Task should have optional created_at field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        now = datetime.now()
        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
            created_at=now,
        )
        assert task.created_at == now

    def test_task_has_updated_at(self):
        """Task should have optional updated_at field."""
        from gitlab_mcp.tasks.task_manager import Task, TaskState

        now = datetime.now()
        task = Task(
            id="test-123",
            task_type="pipeline_create",
            state=TaskState.PENDING,
            updated_at=now,
        )
        assert task.updated_at == now


class TestTaskManager:
    """Test TaskManager class."""

    @pytest.fixture
    def manager(self):
        """Create a TaskManager instance."""
        from gitlab_mcp.tasks.task_manager import TaskManager

        return TaskManager()

    def test_task_manager_initializes_empty(self, manager):
        """TaskManager should initialize with no tasks."""
        assert len(manager.list_tasks()) == 0

    def test_create_task_returns_task(self, manager):
        """create_task should return a Task object."""
        from gitlab_mcp.tasks.task_manager import Task

        task = manager.create_task(
            task_type="pipeline_create",
            metadata={"project_id": "group/project"},
        )
        assert isinstance(task, Task)

    def test_create_task_generates_unique_id(self, manager):
        """create_task should generate a unique task ID."""
        task1 = manager.create_task(task_type="pipeline_create")
        task2 = manager.create_task(task_type="pipeline_create")
        assert task1.id != task2.id

    def test_create_task_sets_pending_state(self, manager):
        """create_task should set task state to PENDING."""
        from gitlab_mcp.tasks.task_manager import TaskState

        task = manager.create_task(task_type="pipeline_create")
        assert task.state == TaskState.PENDING

    def test_create_task_sets_task_type(self, manager):
        """create_task should set the task type."""
        task = manager.create_task(task_type="pipeline_create")
        assert task.task_type == "pipeline_create"

    def test_create_task_sets_metadata(self, manager):
        """create_task should set metadata if provided."""
        task = manager.create_task(
            task_type="pipeline_create",
            metadata={"project_id": "group/project", "ref": "main"},
        )
        assert task.metadata == {"project_id": "group/project", "ref": "main"}

    def test_create_task_sets_created_at(self, manager):
        """create_task should set created_at timestamp."""
        task = manager.create_task(task_type="pipeline_create")
        assert task.created_at is not None
        assert isinstance(task.created_at, datetime)


class TestTaskRetrieval:
    """Test task retrieval operations."""

    @pytest.fixture
    def manager(self):
        """Create a TaskManager instance."""
        from gitlab_mcp.tasks.task_manager import TaskManager

        return TaskManager()

    def test_get_task_by_id(self, manager):
        """get_task should retrieve a task by ID."""
        created = manager.create_task(task_type="pipeline_create")
        retrieved = manager.get_task(created.id)
        assert retrieved is not None
        assert retrieved.id == created.id

    def test_get_task_unknown_id_returns_none(self, manager):
        """get_task should return None for unknown ID."""
        result = manager.get_task("unknown-id")
        assert result is None

    def test_list_tasks_returns_all_tasks(self, manager):
        """list_tasks should return all tasks."""
        manager.create_task(task_type="task1")
        manager.create_task(task_type="task2")
        manager.create_task(task_type="task3")
        tasks = manager.list_tasks()
        assert len(tasks) == 3


class TestTaskStateTransitions:
    """Test task state transitions."""

    @pytest.fixture
    def manager(self):
        """Create a TaskManager instance."""
        from gitlab_mcp.tasks.task_manager import TaskManager

        return TaskManager()

    def test_start_task_changes_state_to_working(self, manager):
        """start_task should change state to WORKING."""
        from gitlab_mcp.tasks.task_manager import TaskState

        task = manager.create_task(task_type="pipeline_create")
        updated = manager.start_task(task.id)
        assert updated is not None
        assert updated.state == TaskState.WORKING

    def test_complete_task_changes_state_to_completed(self, manager):
        """complete_task should change state to COMPLETED."""
        from gitlab_mcp.tasks.task_manager import TaskState

        task = manager.create_task(task_type="pipeline_create")
        manager.start_task(task.id)
        result = {"pipeline_id": 500, "status": "success"}
        updated = manager.complete_task(task.id, result=result)
        assert updated is not None
        assert updated.state == TaskState.COMPLETED
        assert updated.result == result

    def test_fail_task_changes_state_to_failed(self, manager):
        """fail_task should change state to FAILED."""
        from gitlab_mcp.tasks.task_manager import TaskState

        task = manager.create_task(task_type="pipeline_create")
        manager.start_task(task.id)
        updated = manager.fail_task(task.id, error="Pipeline failed")
        assert updated is not None
        assert updated.state == TaskState.FAILED
        assert updated.error == "Pipeline failed"

    def test_cancel_task_changes_state_to_cancelled(self, manager):
        """cancel_task should change state to CANCELLED."""
        from gitlab_mcp.tasks.task_manager import TaskState

        task = manager.create_task(task_type="pipeline_create")
        manager.start_task(task.id)
        updated = manager.cancel_task(task.id)
        assert updated is not None
        assert updated.state == TaskState.CANCELLED

    def test_state_transition_updates_updated_at(self, manager):
        """State transitions should update updated_at timestamp."""
        task = manager.create_task(task_type="pipeline_create")
        original_time = task.updated_at
        updated = manager.start_task(task.id)
        assert updated is not None
        assert updated.updated_at is not None
        # updated_at should be set or changed
        if original_time is not None:
            assert updated.updated_at >= original_time


class TestTaskFiltering:
    """Test task filtering operations."""

    @pytest.fixture
    def manager(self):
        """Create a TaskManager instance with tasks in various states."""
        from gitlab_mcp.tasks.task_manager import TaskManager

        mgr = TaskManager()
        # Create tasks in different states
        task1 = mgr.create_task(task_type="pipeline_create")
        task2 = mgr.create_task(task_type="pipeline_retry")
        _task3 = mgr.create_task(task_type="pipeline_create")  # Remains pending

        # Transition some tasks
        mgr.start_task(task1.id)
        mgr.start_task(task2.id)
        mgr.complete_task(task2.id, result={"status": "success"})

        return mgr

    def test_list_tasks_by_state(self, manager):
        """list_tasks should filter by state."""
        from gitlab_mcp.tasks.task_manager import TaskState

        pending_tasks = manager.list_tasks(state=TaskState.PENDING)
        assert len(pending_tasks) == 1

        working_tasks = manager.list_tasks(state=TaskState.WORKING)
        assert len(working_tasks) == 1

        completed_tasks = manager.list_tasks(state=TaskState.COMPLETED)
        assert len(completed_tasks) == 1

    def test_list_tasks_by_task_type(self, manager):
        """list_tasks should filter by task_type."""
        pipeline_create_tasks = manager.list_tasks(task_type="pipeline_create")
        assert len(pipeline_create_tasks) == 2

        pipeline_retry_tasks = manager.list_tasks(task_type="pipeline_retry")
        assert len(pipeline_retry_tasks) == 1


class TestTaskCancellation:
    """Test task cancellation behavior."""

    @pytest.fixture
    def manager(self):
        """Create a TaskManager instance."""
        from gitlab_mcp.tasks.task_manager import TaskManager

        return TaskManager()

    def test_cancel_pending_task(self, manager):
        """Pending tasks should be cancellable."""
        from gitlab_mcp.tasks.task_manager import TaskState

        task = manager.create_task(task_type="pipeline_create")
        cancelled = manager.cancel_task(task.id)
        assert cancelled is not None
        assert cancelled.state == TaskState.CANCELLED

    def test_cancel_working_task(self, manager):
        """Working tasks should be cancellable."""
        from gitlab_mcp.tasks.task_manager import TaskState

        task = manager.create_task(task_type="pipeline_create")
        manager.start_task(task.id)
        cancelled = manager.cancel_task(task.id)
        assert cancelled is not None
        assert cancelled.state == TaskState.CANCELLED

    def test_cancel_completed_task_returns_none(self, manager):
        """Completed tasks should not be cancellable."""
        task = manager.create_task(task_type="pipeline_create")
        manager.start_task(task.id)
        manager.complete_task(task.id, result={})
        result = manager.cancel_task(task.id)
        assert result is None

    def test_cancel_failed_task_returns_none(self, manager):
        """Failed tasks should not be cancellable."""
        task = manager.create_task(task_type="pipeline_create")
        manager.start_task(task.id)
        manager.fail_task(task.id, error="Error")
        result = manager.cancel_task(task.id)
        assert result is None

    def test_cancel_unknown_task_returns_none(self, manager):
        """Unknown task ID should return None."""
        result = manager.cancel_task("unknown-id")
        assert result is None


class TestTaskDeletion:
    """Test task deletion operations."""

    @pytest.fixture
    def manager(self):
        """Create a TaskManager instance."""
        from gitlab_mcp.tasks.task_manager import TaskManager

        return TaskManager()

    def test_delete_task(self, manager):
        """delete_task should remove a task."""
        task = manager.create_task(task_type="pipeline_create")
        result = manager.delete_task(task.id)
        assert result is True
        assert manager.get_task(task.id) is None

    def test_delete_unknown_task_returns_false(self, manager):
        """delete_task for unknown ID should return False."""
        result = manager.delete_task("unknown-id")
        assert result is False

    def test_clear_completed_tasks(self, manager):
        """clear_completed_tasks should remove all completed tasks."""
        task1 = manager.create_task(task_type="task1")
        task2 = manager.create_task(task_type="task2")
        _task3 = manager.create_task(task_type="task3")  # Remains pending

        manager.start_task(task1.id)
        manager.complete_task(task1.id, result={})
        manager.start_task(task2.id)
        manager.complete_task(task2.id, result={})

        count = manager.clear_completed_tasks()
        assert count == 2
        assert len(manager.list_tasks()) == 1
