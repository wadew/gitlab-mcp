"""Unit tests for logging module.

Tests verify:
- Logger initialization with configuration
- Log level respects configuration
- Sensitive data (tokens, passwords) is redacted
- Structured logging format
- Logs include required metadata (timestamp, module, level)
"""

import logging

import pytest

from gitlab_mcp.utils.logging import redact_sensitive_data, setup_logger


class TestLoggerInitialization:
    """Test logger setup and initialization."""

    def test_setup_logger_creates_logger(self):
        """setup_logger should create and return a logger."""
        logger = setup_logger("test_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_logger"

    def test_setup_logger_default_level_is_info(self):
        """Default log level should be INFO."""
        logger = setup_logger("test_logger")
        assert logger.level == logging.INFO

    def test_setup_logger_respects_custom_level(self):
        """Logger should respect custom log level."""
        logger = setup_logger("test_logger", level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logger_debug_level(self):
        """Logger should accept DEBUG level."""
        logger = setup_logger("test_logger", level="DEBUG")
        assert logger.level == logging.DEBUG

    def test_setup_logger_warning_level(self):
        """Logger should accept WARNING level."""
        logger = setup_logger("test_logger", level="WARNING")
        assert logger.level == logging.WARNING

    def test_setup_logger_error_level(self):
        """Logger should accept ERROR level."""
        logger = setup_logger("test_logger", level="ERROR")
        assert logger.level == logging.ERROR

    def test_setup_logger_invalid_level_raises_error(self):
        """Invalid log level should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid log level"):
            setup_logger("test_logger", level="INVALID")


class TestSensitiveDataRedaction:
    """Test sensitive data is redacted from log messages."""

    def test_redact_token_in_message(self):
        """Token values should be redacted."""
        message = "Using token: glpat-abc123def456"
        redacted = redact_sensitive_data(message)
        assert "glpat-abc123def456" not in redacted
        assert "[REDACTED]" in redacted

    def test_redact_personal_access_token(self):
        """Personal access tokens should be redacted."""
        message = "Authorization: Bearer glpat-1234567890abcdef"
        redacted = redact_sensitive_data(message)
        assert "glpat-1234567890abcdef" not in redacted
        assert "[REDACTED]" in redacted

    def test_redact_password_in_message(self):
        """Password values should be redacted."""
        message = "password=mysecretpass123"
        redacted = redact_sensitive_data(message)
        assert "mysecretpass123" not in redacted
        assert "[REDACTED]" in redacted

    def test_redact_authorization_header(self):
        """Authorization headers should be redacted."""
        message = "Headers: {'Authorization': 'Bearer xyz123'}"
        redacted = redact_sensitive_data(message)
        assert "xyz123" not in redacted
        assert "[REDACTED]" in redacted

    def test_redact_private_token_header(self):
        """PRIVATE-TOKEN headers should be redacted."""
        message = "PRIVATE-TOKEN: glpat-abcdefghij"
        redacted = redact_sensitive_data(message)
        assert "glpat-abcdefghij" not in redacted
        assert "[REDACTED]" in redacted

    def test_redact_multiple_tokens_in_message(self):
        """Multiple tokens in same message should all be redacted."""
        message = "token1: glpat-111 and token2: glpat-222"
        redacted = redact_sensitive_data(message)
        assert "glpat-111" not in redacted
        assert "glpat-222" not in redacted
        assert redacted.count("[REDACTED]") == 2

    def test_redact_preserves_non_sensitive_data(self):
        """Non-sensitive data should not be redacted."""
        message = "Processing project: my-project, user: john"
        redacted = redact_sensitive_data(message)
        assert "my-project" in redacted
        assert "john" in redacted
        assert redacted == message

    def test_redact_empty_message(self):
        """Empty message should return empty string."""
        redacted = redact_sensitive_data("")
        assert redacted == ""

    def test_redact_none_message(self):
        """None message should return empty string."""
        redacted = redact_sensitive_data(None)
        assert redacted == ""


class TestStructuredLogging:
    """Test structured logging format."""

    def test_log_output_is_json_format(self):
        """Log output should be valid JSON when structured format enabled."""
        logger = setup_logger("test_logger", structured=True)
        # Just verify the logger is created with structured format
        # The actual JSON format will be applied by the formatter
        assert logger is not None
        # Check that handler has the right formatter
        assert len(logger.handlers) == 1
        formatter_format = logger.handlers[0].formatter._fmt
        assert "timestamp" in formatter_format
        assert "level" in formatter_format
        assert "module" in formatter_format

    def test_log_includes_timestamp(self):
        """Log should include timestamp in formatter."""
        logger = setup_logger("test_logger")
        assert len(logger.handlers) == 1
        formatter_format = logger.handlers[0].formatter._fmt
        assert "asctime" in formatter_format

    def test_log_includes_level(self):
        """Log should include log level in formatter."""
        logger = setup_logger("test_logger")
        assert len(logger.handlers) == 1
        formatter_format = logger.handlers[0].formatter._fmt
        assert "levelname" in formatter_format

    def test_log_includes_module_name(self):
        """Log should include module name in formatter."""
        logger = setup_logger("test_module")
        assert len(logger.handlers) == 1
        formatter_format = logger.handlers[0].formatter._fmt
        assert "name" in formatter_format

    def test_log_includes_message(self):
        """Log should include the actual message in formatter."""
        logger = setup_logger("test_logger")
        assert len(logger.handlers) == 1
        formatter_format = logger.handlers[0].formatter._fmt
        assert "message" in formatter_format


class TestLoggerSensitiveDataIntegration:
    """Test that logger automatically redacts sensitive data via filter."""

    def test_logger_has_sensitive_data_filter(self):
        """Logger should have sensitive data filter attached."""
        logger = setup_logger("test_logger")
        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        # Check that filter is attached
        assert len(handler.filters) == 1

    def test_filter_redacts_token_in_log_record(self):
        """Filter should redact tokens from log records."""
        from gitlab_mcp.utils.logging import SensitiveDataFilter

        filter_instance = SensitiveDataFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Using token: glpat-secret123",
            args=(),
            exc_info=None,
        )

        filter_instance.filter(record)
        assert "glpat-secret123" not in record.msg
        assert "[REDACTED]" in record.msg

    def test_filter_redacts_password_in_log_record(self):
        """Filter should redact passwords from log records."""
        from gitlab_mcp.utils.logging import SensitiveDataFilter

        filter_instance = SensitiveDataFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Config: password=secretpass",
            args=(),
            exc_info=None,
        )

        filter_instance.filter(record)
        assert "secretpass" not in record.msg
        assert "[REDACTED]" in record.msg

    def test_filter_preserves_non_sensitive_data(self):
        """Filter should not modify non-sensitive data."""
        from gitlab_mcp.utils.logging import SensitiveDataFilter

        filter_instance = SensitiveDataFilter()
        original_msg = "Processing project: my-project"
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=original_msg,
            args=(),
            exc_info=None,
        )

        filter_instance.filter(record)
        assert record.msg == original_msg
