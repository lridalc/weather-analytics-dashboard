import logging

import pytest

from weather_analytics_dashboard.config import Settings, setup_logging


class TestLoggingSetup:
    @pytest.fixture
    def settings(self):
        return Settings(api_key="test-key", log_level="DEBUG")

    def test_root_logger_level(self, settings):
        setup_logging(settings)

        assert logging.getLogger().level == logging.DEBUG

    def test_third_party_loggers_silenced(self, settings):
        setup_logging(settings)

        for name in ["httpx", "httpcore", "urllib3", "uvicorn.access"]:
            assert logging.getLogger(name).level == logging.WARNING

    def test_logging_outputs_message(self, settings, capsys):
        setup_logging(settings)

        logger = logging.getLogger("test")
        logger.info("hello")

        captured = capsys.readouterr()
        assert "hello" in captured.out

    def test_logging_format_applied(self, settings, capsys):
        setup_logging(settings)

        logger = logging.getLogger("test_logger")
        logger.info("formatted message")

        captured = capsys.readouterr()
        assert "test_logger" in captured.out
        assert "INFO" in captured.out
        assert "formatted message" in captured.out

    def test_idempotent(self, settings):
        setup_logging(settings)
        handlers_before = len(logging.getLogger().handlers)

        setup_logging(settings)
        handlers_after = len(logging.getLogger().handlers)

        assert handlers_before == handlers_after
