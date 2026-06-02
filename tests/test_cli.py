import pytest
from pathlib import Path
from click.testing import CliRunner
from promptlint.cli import cli

FIXTURES = Path(__file__).parent / "fixtures"


class TestCliCheck:
    def setup_method(self):
        self.runner = CliRunner()

    def test_check_valid_file_exits_zero(self):
        path = str(FIXTURES / "good_standard.prompt")
        result = self.runner.invoke(cli, ["check", path])
        assert result.exit_code == 0

    def test_check_bad_file_exits_one(self):
        path = str(FIXTURES / "bad_unclosed.prompt")
        result = self.runner.invoke(cli, ["check", path])
        assert result.exit_code == 1

    def test_check_fluff_file_exits_one(self):
        path = str(FIXTURES / "bad_fluff.prompt")
        result = self.runner.invoke(cli, ["check", path])
        assert result.exit_code == 1

    def test_check_nonexistent_file_exits_nonzero(self):
        result = self.runner.invoke(cli, ["check", "nonexistent.prompt"])
        assert "not found" in result.output.lower() or result.exit_code != 0
