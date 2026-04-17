"""
Tests for logging configuration.

These tests validate:
- Root logger configuration
- Log level behavior
- Idempotency of setup
- Real log emission

They avoid fragile assertions tied to exact formatting or environment.
"""

import logging

import pytest

from weather_analytics_dashboard.config import setup_logging


class TestLoggingSetup:
    """Tests for logging setup behavior."""

    # ==================================================================================
    # ROOT LOGGER CONFIGURATION
    # ==================================================================================

    @pytest.mark.no_test_environment
    def test_setup_logging_sets_root_level(self, settings):
        """setup_logging should configure the root logger level."""
        setup_logging(settings)

        root_logger = logging.getLogger()

        assert root_logger.level == logging.DEBUG

    # ==================================================================================
    # LOG EMISSION
    # ==================================================================================

    def test_logging_emits_messages_at_expected_level(self, settings, caplog):
        """Logging should respect configured log level."""
        settings.log_level = "WARNING"

        setup_logging(settings)

        logger = logging.getLogger("test_logger")  # Inherits log level from root logger

        logger.debug("debug message")
        logger.warning("warning message")

        messages = [record.message for record in caplog.records]

        # DEBUG message should not appear because logger level is WARNING
        assert "debug message" not in messages
        assert "warning message" in messages

    @pytest.mark.no_test_environment
    def test_logging_outputs_messages(self, settings, capsys):
        """Logging should produce output to stdout/stderr."""
        setup_logging(settings)

        logger = logging.getLogger("test_logger")
        logger.info("test message")

        captured = capsys.readouterr()

        # Avoid strict formatting checks → only validate signal
        assert "test message" in captured.out or "test message" in captured.err

    # ==================================================================================
    # IDEMPOTENCY
    # ==================================================================================
    @pytest.mark.no_test_environment
    def test_setup_logging_is_idempotent(self, settings):
        """
        Calling setup_logging multiple times should not break logging.

        We avoid strict handler counting (fragile across environments), but ensure no
        uncontrolled growth happens.
        """
        setup_logging(settings)  # To override pytest root logger

        root_logger = logging.getLogger()

        initial_handlers = len(root_logger.handlers)

        setup_logging(settings)
        handlers_after_first = len(root_logger.handlers)

        setup_logging(settings)
        handlers_after_second = len(root_logger.handlers)

        # No uncontrolled growth
        assert handlers_after_second == handlers_after_first

        # Should not remove existing handlers
        assert handlers_after_first >= initial_handlers

    # =========================================================================
    # THIRD-PARTY LOGGING CONTROL
    # =========================================================================

    @pytest.mark.parametrize(
        "logger_name",
        ["httpx", "httpcore", "urllib3", "uvicorn.access"],
    )
    def test_external_loggers_are_silenced(self, settings, logger_name):
        """External noisy libraries should be set to WARNING or higher."""
        setup_logging(settings)

        logger = logging.getLogger(logger_name)

        assert logger.level >= logging.WARNING

    # =========================================================================
    # ERROR HANDLING
    # =========================================================================

    def test_invalid_log_level_raises_error(self, settings):
        """Invalid log level should raise ValueError."""
        settings.log_level = "INVALID"

        with pytest.raises(ValueError):
            setup_logging(settings)
