"""Task Manager for MCP long-running operations.

Provides state management for asynchronous tasks like pipeline creation,
polling, and bulk operations.
"""

import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class TaskState(Enum):
    """Task execution states."""

    PENDING = "pending"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Task:
    """Represents an asynchronous task.

    Attributes:
        id: Unique task identifier
        task_type: Type of task (e.g., 'pipeline_create', 'pipeline_retry')
        state: Current task state
        metadata: Optional task parameters/context
        result: Task result (set on completion)
        error: Error message (set on failure)
        created_at: Task creation timestamp
        updated_at: Last state change timestamp
    """

    id: str
    task_type: str
    state: TaskState
    metadata: dict[str, Any] | None = None
    result: dict[str, Any] | None = None
    error: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TaskManager:
    """Manages task lifecycle and state.

    Provides CRUD operations for tasks with state tracking.
    Thread-safe for basic operations.
    """

    def __init__(self) -> None:
        """Initialize the TaskManager with empty task storage."""
        self._tasks: dict[str, Task] = {}

    def create_task(
        self,
        task_type: str,
        metadata: dict[str, Any] | None = None,
    ) -> Task:
        """Create a new task in PENDING state.

        Args:
            task_type: Type of task (e.g., 'pipeline_create')
            metadata: Optional task parameters

        Returns:
            Created Task object
        """
        task_id = str(uuid.uuid4())
        now = datetime.now()
        task = Task(
            id=task_id,
            task_type=task_type,
            state=TaskState.PENDING,
            metadata=metadata,
            created_at=now,
            updated_at=now,
        )
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Task | None:
        """Retrieve a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task object or None if not found
        """
        return self._tasks.get(task_id)

    def list_tasks(
        self,
        state: TaskState | None = None,
        task_type: str | None = None,
    ) -> list[Task]:
        """List all tasks with optional filtering.

        Args:
            state: Filter by task state (optional)
            task_type: Filter by task type (optional)

        Returns:
            List of matching Task objects
        """
        tasks = list(self._tasks.values())

        if state is not None:
            tasks = [t for t in tasks if t.state == state]

        if task_type is not None:
            tasks = [t for t in tasks if t.task_type == task_type]

        return tasks

    def start_task(self, task_id: str) -> Task | None:
        """Transition a task to WORKING state.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task or None if not found
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.state = TaskState.WORKING
        task.updated_at = datetime.now()
        return task

    def complete_task(
        self,
        task_id: str,
        result: dict[str, Any] | None = None,
    ) -> Task | None:
        """Transition a task to COMPLETED state.

        Args:
            task_id: Task identifier
            result: Task result data

        Returns:
            Updated Task or None if not found
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.state = TaskState.COMPLETED
        task.result = result
        task.updated_at = datetime.now()
        return task

    def fail_task(
        self,
        task_id: str,
        error: str,
    ) -> Task | None:
        """Transition a task to FAILED state.

        Args:
            task_id: Task identifier
            error: Error message

        Returns:
            Updated Task or None if not found
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.state = TaskState.FAILED
        task.error = error
        task.updated_at = datetime.now()
        return task

    def cancel_task(self, task_id: str) -> Task | None:
        """Transition a task to CANCELLED state.

        Only PENDING and WORKING tasks can be cancelled.

        Args:
            task_id: Task identifier

        Returns:
            Updated Task or None if not found or not cancellable
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        # Only cancel PENDING or WORKING tasks
        if task.state not in (TaskState.PENDING, TaskState.WORKING):
            return None

        task.state = TaskState.CANCELLED
        task.updated_at = datetime.now()
        return task

    def delete_task(self, task_id: str) -> bool:
        """Delete a task from storage.

        Args:
            task_id: Task identifier

        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def clear_completed_tasks(self) -> int:
        """Remove all completed tasks.

        Returns:
            Number of tasks removed
        """
        completed_ids = [
            task_id for task_id, task in self._tasks.items() if task.state == TaskState.COMPLETED
        ]
        for task_id in completed_ids:
            del self._tasks[task_id]
        return len(completed_ids)
