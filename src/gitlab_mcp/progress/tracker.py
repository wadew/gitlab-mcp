"""Progress Tracker for MCP long-running operations.

Provides progress tracking and reporting for operations like
log fetching, search, and bulk operations.
"""

from dataclasses import dataclass


@dataclass
class ProgressReport:
    """Report of current progress for an operation.

    Attributes:
        operation: Name of the operation being tracked
        current: Current progress value
        total: Total expected value
        percentage: Progress as percentage (0-100)
        is_complete: Whether the operation is complete
        message: Optional status message
    """

    operation: str
    current: int
    total: int
    percentage: float
    is_complete: bool
    message: str | None = None


class ProgressTracker:
    """Tracks progress for long-running operations.

    Provides methods to update progress, calculate percentage,
    and generate status reports.

    Attributes:
        total: Total expected value
        operation: Name of the operation
        current: Current progress value
    """

    def __init__(
        self,
        total: int,
        operation: str = "operation",
    ) -> None:
        """Initialize the ProgressTracker.

        Args:
            total: Total expected value for the operation
            operation: Name of the operation (for reporting)
        """
        self.total = total
        self.operation = operation
        self._current = 0

    @property
    def current(self) -> int:
        """Get current progress value."""
        return self._current

    @property
    def percentage(self) -> float:
        """Get progress as percentage (0-100).

        Returns:
            Progress percentage, or 100.0 if total is 0
        """
        if self.total == 0:
            return 100.0
        return (self._current / self.total) * 100.0

    @property
    def is_complete(self) -> bool:
        """Check if operation is complete.

        Returns:
            True if current >= total, or total is 0
        """
        if self.total == 0:
            return True
        return self._current >= self.total

    @property
    def status(self) -> str:
        """Get human-readable status message.

        Returns:
            Status message including operation name and percentage
        """
        if self.is_complete:
            return f"{self.operation}: complete (100%)"
        return f"{self.operation}: {self.percentage:.0f}% ({self._current}/{self.total})"

    def update(self, increment: int) -> None:
        """Update progress by incrementing current value.

        Args:
            increment: Amount to add to current progress

        Note:
            Current value will not exceed total
        """
        self._current = min(self._current + increment, self.total)

    def complete(self) -> None:
        """Mark operation as complete.

        Sets current to total to indicate completion.
        """
        self._current = self.total

    def get_report(self, message: str | None = None) -> ProgressReport:
        """Generate a progress report.

        Args:
            message: Optional custom status message

        Returns:
            ProgressReport with current progress details
        """
        return ProgressReport(
            operation=self.operation,
            current=self._current,
            total=self.total,
            percentage=self.percentage,
            is_complete=self.is_complete,
            message=message,
        )
