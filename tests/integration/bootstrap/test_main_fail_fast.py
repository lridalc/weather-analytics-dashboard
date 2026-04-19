"""
Entrypoint fail-fast verification tests.

These tests validate that the application fails fast and exits cleanly when
configuration is invalid. This ensures the application never starts in a degraded or
misconfigured state.
"""

import subprocess
import sys


class TestMainFailFast:
    """Verify application fails fast on invalid configuration."""

    def test_main_exits_with_code_1_on_invalid_config(self, tmp_path, monkeypatch):
        """
        Given an environment with an invalid LOG_LEVEL,
        When main.py is executed as a module,
        Then the process should exit with code 1 (Error).
        """
        # 1. Arrange: Clean environment due to fixtures

        # Ensure we don't accidentally read a valid .env file
        monkeypatch.chdir(tmp_path)

        # Set invalid LOG_LEVEL
        monkeypatch.setenv("LOG_LEVEL", "error")

        # 2. Act: Run the module as a script
        result = subprocess.run(
            [sys.executable, "-m", "weather_analytics_dashboard.main"],
            capture_output=True,
            text=True,
        )

        # 3. Assert
        assert result.returncode == 1
        assert "Configuration validation failed" in result.stderr

    def test_main_exits_with_code_0_on_valid_config(self, tmp_path, monkeypatch):
        """
        Sanity check:
        Given a valid environment (an empty one, as there are not required variables),
        When main.py is executed,
        Then the import should succeed (exit code 0).

        Note: We don't actually start the server in this test, we only verify
        that the module can be imported/executed without configuration errors.
        """

        result = subprocess.run(
            [sys.executable, "-m", "weather_analytics_dashboard.main"],
            capture_output=True,
            text=True,
            env={},
        )

        assert result.returncode == 0
