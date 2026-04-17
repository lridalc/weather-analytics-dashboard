class TestCliNoArgs:
    """Test suite for CLI entrypoint with no arguments."""

    def test_cli_no_args_shows_help(self, cli_runner):
        """Verify CLI without arguments displays help message."""
        result = cli_runner([])
        assert result.stderr == ""
        assert "Usage:" in result.stdout
        assert "Options:" in result.stdout
