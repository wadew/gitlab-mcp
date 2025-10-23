"""Logging utilities with automatic sensitive data redaction.

This module provides:
- Logger setup with configurable levels
- Automatic redaction of sensitive data (tokens, passwords, auth headers)
- Structured logging support (JSON format)
- stdout output for MCP server compatibility
"""

import logging
import re
from typing import Optional

# Patterns to identify and redact sensitive data
SENSITIVE_PATTERNS = [
    # GitLab Personal Access Tokens
    (re.compile(r"glpat-[a-zA-Z0-9_-]+"), "[REDACTED]"),
    # Generic tokens in key-value pairs
    (re.compile(r'(?i)(token["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'), r"\1[REDACTED]"),
    # Passwords in key-value pairs
    (re.compile(r'(?i)(password["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'), r"\1[REDACTED]"),
    # Authorization headers
    (
        re.compile(r'(?i)(Authorization["\']?\s*[:=]\s*["\']?(?:Bearer\s+)?)([^"\'\s]+)'),
        r"\1[REDACTED]",
    ),
    # PRIVATE-TOKEN headers
    (re.compile(r'(?i)(PRIVATE-TOKEN["\']?\s*[:=]\s*["\']?)([^"\'\s]+)'), r"\1[REDACTED]"),
]


def redact_sensitive_data(message: Optional[str]) -> str:
    """Redact sensitive data from a message.

    Replaces tokens, passwords, and authentication credentials with [REDACTED].

    Args:
        message: The message to redact (can be None)

    Returns:
        The redacted message string

    Examples:
        >>> redact_sensitive_data("Using token: glpat-abc123")
        'Using token: [REDACTED]'
        >>> redact_sensitive_data("password=secret123")
        'password=[REDACTED]'
    """
    if not message:
        return ""

    redacted = message
    for pattern, replacement in SENSITIVE_PATTERNS:
        redacted = pattern.sub(replacement, redacted)

    return redacted


class SensitiveDataFilter(logging.Filter):
    """Logging filter that redacts sensitive data from log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter and redact sensitive data from log record.

        Args:
            record: The log record to filter

        Returns:
            True (always allow the record, just redact it)
        """
        # Redact the message
        record.msg = redact_sensitive_data(str(record.msg))

        # Redact any args that might contain sensitive data
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: redact_sensitive_data(str(v)) if isinstance(v, str) else v
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    redact_sensitive_data(str(arg)) if isinstance(arg, str) else arg
                    for arg in record.args
                )

        return True


def setup_logger(name: str, level: str = "INFO", structured: bool = False) -> logging.Logger:
    """Set up a logger with sensitive data redaction.

    Args:
        name: Logger name (typically module name)
        level: Log level (DEBUG, INFO, WARNING, ERROR)
        structured: If True, use JSON structured logging format

    Returns:
        Configured logger instance

    Raises:
        ValueError: If log level is invalid

    Examples:
        >>> logger = setup_logger("my_module")
        >>> logger.info("Processing request")

        >>> logger = setup_logger("my_module", level="DEBUG")
        >>> logger.debug("Debug information")
    """
    # Validate log level
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level.upper() not in valid_levels:
        raise ValueError(f"Invalid log level: {level}. Must be one of {', '.join(valid_levels)}")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create console handler (stdout for MCP compatibility)
    handler = logging.StreamHandler()
    handler.setLevel(getattr(logging, level.upper()))

    # Set formatter
    if structured:
        # JSON structured format (basic implementation)
        formatter = logging.Formatter(
            '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
            '"module": "%(name)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable format
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)

    # Add sensitive data filter
    sensitive_filter = SensitiveDataFilter()
    handler.addFilter(sensitive_filter)

    # Add handler to logger
    logger.addHandler(handler)

    # Prevent propagation to root logger (avoid duplicate logs)
    logger.propagate = False

    return logger
