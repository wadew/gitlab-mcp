"""Unit tests for MCP Progress Reporting module.

Tests verify:
- Progress tracker creation and updates
- Progress percentage calculation
- Progress status messages
- Completion detection
"""

import pytest


class TestProgressTracker:
    """Test ProgressTracker class."""

    def test_tracker_exists(self):
        """ProgressTracker class should exist."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        assert ProgressTracker is not None

    def test_tracker_init_with_total(self):
        """ProgressTracker should initialize with total."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=100)
        assert tracker.total == 100

    def test_tracker_init_with_operation(self):
        """ProgressTracker should initialize with operation name."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=100, operation="fetch_logs")
        assert tracker.operation == "fetch_logs"

    def test_tracker_current_starts_at_zero(self):
        """ProgressTracker current should start at 0."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=100)
        assert tracker.current == 0

    def test_tracker_has_update_method(self):
        """ProgressTracker should have update method."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=100)
        assert hasattr(tracker, "update")

    def test_tracker_has_complete_method(self):
        """ProgressTracker should have complete method."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=100)
        assert hasattr(tracker, "complete")


class TestProgressUpdate:
    """Test progress update functionality."""

    @pytest.fixture
    def tracker(self):
        """Create a ProgressTracker instance."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        return ProgressTracker(total=100, operation="test_operation")

    def test_update_increments_current(self, tracker):
        """update should increment current value."""
        tracker.update(10)
        assert tracker.current == 10

    def test_update_accumulates(self, tracker):
        """update should accumulate progress."""
        tracker.update(10)
        tracker.update(20)
        assert tracker.current == 30

    def test_update_with_increment(self, tracker):
        """update with increment parameter."""
        tracker.update(25)
        tracker.update(25)
        assert tracker.current == 50

    def test_update_does_not_exceed_total(self, tracker):
        """update should not exceed total."""
        tracker.update(150)
        assert tracker.current == 100


class TestProgressPercentage:
    """Test progress percentage calculation."""

    @pytest.fixture
    def tracker(self):
        """Create a ProgressTracker instance."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        return ProgressTracker(total=100, operation="test_operation")

    def test_tracker_has_percentage_property(self, tracker):
        """ProgressTracker should have percentage property."""
        assert hasattr(tracker, "percentage")

    def test_percentage_starts_at_zero(self, tracker):
        """percentage should start at 0."""
        assert tracker.percentage == 0.0

    def test_percentage_at_half(self, tracker):
        """percentage at 50% progress."""
        tracker.update(50)
        assert tracker.percentage == 50.0

    def test_percentage_at_full(self, tracker):
        """percentage at 100% progress."""
        tracker.update(100)
        assert tracker.percentage == 100.0

    def test_percentage_with_fractional(self):
        """percentage with fractional values."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=3)
        tracker.update(1)
        assert 33.0 <= tracker.percentage <= 34.0


class TestProgressCompletion:
    """Test progress completion detection."""

    @pytest.fixture
    def tracker(self):
        """Create a ProgressTracker instance."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        return ProgressTracker(total=100, operation="test_operation")

    def test_tracker_has_is_complete_property(self, tracker):
        """ProgressTracker should have is_complete property."""
        assert hasattr(tracker, "is_complete")

    def test_not_complete_initially(self, tracker):
        """is_complete should be False initially."""
        assert tracker.is_complete is False

    def test_not_complete_at_partial(self, tracker):
        """is_complete should be False at partial progress."""
        tracker.update(50)
        assert tracker.is_complete is False

    def test_complete_at_100(self, tracker):
        """is_complete should be True at 100%."""
        tracker.update(100)
        assert tracker.is_complete is True

    def test_complete_method_sets_complete(self, tracker):
        """complete method should set is_complete to True."""
        tracker.complete()
        assert tracker.is_complete is True

    def test_complete_method_sets_current_to_total(self, tracker):
        """complete method should set current to total."""
        tracker.update(50)
        tracker.complete()
        assert tracker.current == 100


class TestProgressStatus:
    """Test progress status messages."""

    @pytest.fixture
    def tracker(self):
        """Create a ProgressTracker instance."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        return ProgressTracker(total=100, operation="fetch_logs")

    def test_tracker_has_status_property(self, tracker):
        """ProgressTracker should have status property."""
        assert hasattr(tracker, "status")

    def test_status_includes_operation(self, tracker):
        """status should include operation name."""
        assert "fetch_logs" in tracker.status

    def test_status_includes_percentage(self, tracker):
        """status should include percentage."""
        tracker.update(50)
        assert "50" in tracker.status

    def test_status_shows_complete(self, tracker):
        """status should show complete when done."""
        tracker.complete()
        assert "complete" in tracker.status.lower() or "100" in tracker.status


class TestProgressReport:
    """Test ProgressReport dataclass."""

    def test_report_exists(self):
        """ProgressReport dataclass should exist."""
        from gitlab_mcp.progress.tracker import ProgressReport

        assert ProgressReport is not None

    def test_report_has_operation(self):
        """ProgressReport should have operation field."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = ProgressReport(
            operation="fetch_logs",
            current=50,
            total=100,
            percentage=50.0,
            is_complete=False,
        )
        assert report.operation == "fetch_logs"

    def test_report_has_current(self):
        """ProgressReport should have current field."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = ProgressReport(
            operation="fetch_logs",
            current=50,
            total=100,
            percentage=50.0,
            is_complete=False,
        )
        assert report.current == 50

    def test_report_has_total(self):
        """ProgressReport should have total field."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = ProgressReport(
            operation="fetch_logs",
            current=50,
            total=100,
            percentage=50.0,
            is_complete=False,
        )
        assert report.total == 100

    def test_report_has_percentage(self):
        """ProgressReport should have percentage field."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = ProgressReport(
            operation="fetch_logs",
            current=50,
            total=100,
            percentage=50.0,
            is_complete=False,
        )
        assert report.percentage == 50.0

    def test_report_has_is_complete(self):
        """ProgressReport should have is_complete field."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = ProgressReport(
            operation="fetch_logs",
            current=100,
            total=100,
            percentage=100.0,
            is_complete=True,
        )
        assert report.is_complete is True

    def test_report_has_message(self):
        """ProgressReport should have optional message field."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = ProgressReport(
            operation="fetch_logs",
            current=50,
            total=100,
            percentage=50.0,
            is_complete=False,
            message="Fetching log lines...",
        )
        assert report.message == "Fetching log lines..."

    def test_report_message_defaults_to_none(self):
        """ProgressReport message should default to None."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = ProgressReport(
            operation="fetch_logs",
            current=50,
            total=100,
            percentage=50.0,
            is_complete=False,
        )
        assert report.message is None


class TestGetProgressReport:
    """Test getting progress reports from tracker."""

    @pytest.fixture
    def tracker(self):
        """Create a ProgressTracker instance."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        return ProgressTracker(total=100, operation="fetch_logs")

    def test_tracker_has_get_report_method(self, tracker):
        """ProgressTracker should have get_report method."""
        assert hasattr(tracker, "get_report")

    def test_get_report_returns_progress_report(self, tracker):
        """get_report should return ProgressReport."""
        from gitlab_mcp.progress.tracker import ProgressReport

        report = tracker.get_report()
        assert isinstance(report, ProgressReport)

    def test_get_report_includes_operation(self, tracker):
        """get_report should include operation."""
        report = tracker.get_report()
        assert report.operation == "fetch_logs"

    def test_get_report_includes_current(self, tracker):
        """get_report should include current progress."""
        tracker.update(25)
        report = tracker.get_report()
        assert report.current == 25

    def test_get_report_includes_total(self, tracker):
        """get_report should include total."""
        report = tracker.get_report()
        assert report.total == 100

    def test_get_report_includes_percentage(self, tracker):
        """get_report should include percentage."""
        tracker.update(75)
        report = tracker.get_report()
        assert report.percentage == 75.0

    def test_get_report_includes_is_complete(self, tracker):
        """get_report should include is_complete."""
        tracker.complete()
        report = tracker.get_report()
        assert report.is_complete is True

    def test_get_report_with_custom_message(self, tracker):
        """get_report should include custom message."""
        tracker.update(50)
        report = tracker.get_report(message="Processing...")
        assert report.message == "Processing..."


class TestProgressOperations:
    """Test progress for specific operations."""

    def test_log_trace_progress(self):
        """Test progress for log trace fetching."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        total_lines = 1000
        tracker = ProgressTracker(
            total=total_lines,
            operation="get_job_trace",
        )

        # Simulate fetching in chunks
        tracker.update(250)
        assert tracker.percentage == 25.0

        tracker.update(250)
        assert tracker.percentage == 50.0

        tracker.complete()
        assert tracker.is_complete is True

    def test_search_progress(self):
        """Test progress for search operations."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        total_files = 50
        tracker = ProgressTracker(
            total=total_files,
            operation="search_code",
        )

        for _ in range(50):
            tracker.update(1)

        assert tracker.is_complete is True

    def test_bulk_operation_progress(self):
        """Test progress for bulk operations."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        total_items = 10
        tracker = ProgressTracker(
            total=total_items,
            operation="bulk_issue_create",
        )

        for i in range(10):
            tracker.update(1)
            assert tracker.current == i + 1

        assert tracker.is_complete is True


class TestProgressWithZeroTotal:
    """Test progress with edge case of zero total."""

    def test_zero_total_does_not_crash(self):
        """Progress with zero total should not crash."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=0, operation="empty_operation")
        assert tracker.total == 0

    def test_zero_total_percentage(self):
        """Percentage with zero total should be 100 or 0."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=0, operation="empty_operation")
        # Either 0% (nothing to do) or 100% (already complete) is acceptable
        assert tracker.percentage in (0.0, 100.0)

    def test_zero_total_is_complete(self):
        """Zero total should be considered complete."""
        from gitlab_mcp.progress.tracker import ProgressTracker

        tracker = ProgressTracker(total=0, operation="empty_operation")
        assert tracker.is_complete is True
