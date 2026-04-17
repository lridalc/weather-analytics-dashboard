class TestCliHelp:
    """Test suite for CLI entrypoint with --help flag."""

    def test_cli_help_shows_help(self, cli_runner):
        """Verify CLI with --help flag displays help message."""
        result = cli_runner(["--help"])
        assert result.stderr == ""
        assert "Usage:" in result.stdout
        assert "Options:" in result.stdout
