"""
Entrypoint fail-fast verification tests.

These tests validate that the application fails fast and exits cleanly when
configuration is invalid. This ensures the application never starts in a degraded or
misconfigured state.
"""

import subprocess
import sys
from pathlib import Path


class TestMainFailFast:
    """Verify application fails fast on invalid configuration."""

    def test_main_exits_with_code_1_on_invalid_config(self, tmp_path, monkeypatch):
        """
        Given an environment without WEATHER_API_KEY,
        When main.py is executed as a module,
        Then the process should exit with code 1 (Error).
        """
        # 1. Arrange: Clean environment without WEATHER_API_KEY due to fixtures

        # Ensure we don't accidentally read a valid .env file
        monkeypatch.chdir(tmp_path)

        project_root = Path(__file__).parent.parent.parent.parent
        main_script = project_root / "src" / "weather_analytics_dashboard" / "main.py"

        # 2. Act: Execute main.py as a subprocess
        result = subprocess.run(
            [sys.executable, str(main_script)],
            capture_output=True,
            text=True,
            cwd=project_root,
            env={},  # Inherits clean environment from pytest/monkeypatch
        )

        # 3. Assert
        assert result.returncode == 1, (
            f"Expected exit code 1 for invalid config, got {result.returncode}\n"
            f"STDERR: {result.stderr}"
        )

    def test_main_does_not_start_api_server_on_invalid_config(
        self, tmp_path, monkeypatch
    ):
        """
        Verify that configuration error message is displayed and the Uvicorn server
        never attempts to start.
        """
        # Arrange: Clean environment without WEATHER_API_KEY due to fixtures

        # Ensure we don't accidentally read a valid .env file
        monkeypatch.chdir(tmp_path)

        project_root = Path(__file__).parent.parent.parent.parent
        main_script = project_root / "src" / "weather_analytics_dashboard" / "main.py"

        result = subprocess.run(
            [sys.executable, str(main_script)],
            capture_output=True,
            text=True,
            cwd=project_root,
        )

        # Verify fatal error message appears in stderr
        assert "FATAL: Configuration validation failed" in result.stderr
        assert "WEATHER_API_KEY" in result.stderr

        # Verify Uvicorn/FastAPI banner is NOT printed
        assert "Uvicorn running on" not in result.stdout
        assert "Application startup complete" not in result.stdout

    def test_main_exits_with_code_0_on_valid_config(self, tmp_path, monkeypatch):
        """
        Sanity check:
        Given a valid WEATHER_API_KEY,
        When main.py is executed,
        Then the import should succeed (exit code 0).

        Note: We don't actually start the server in this test, we only verify
        that the module can be imported/executed without configuration errors.
        """
        monkeypatch.setenv("WEATHER_API_KEY", "valid-test-key-for-sanity-check")
        monkeypatch.chdir(tmp_path)

        project_root = Path(__file__).parent.parent.parent.parent

        # Use -c to execute just the import check without running the server
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                f"import sys; sys.path.insert(0, '{project_root}/src'); "
                "from weather_analytics_dashboard.main import app",
            ],
            capture_output=True,
            text=True,
            cwd=project_root,
            env={
                **dict(
                    monkeypatch._getenv() if hasattr(monkeypatch, "_getenv") else {}
                ),
                "WEATHER_API_KEY": "valid-test-key-for-sanity-check",
            },
        )

        assert result.returncode == 0, (
            f"Expected exit code 0 for valid config, got {result.returncode}\n"
            f"STDERR: {result.stderr}"
        )
