import pytest
from pathlib import Path
from promptlint.engine import lint_file

FIXTURES = Path(__file__).parent / "fixtures"


class TestLintFile:
    def test_good_standard_no_violations(self):
        violations = lint_file(FIXTURES / "good_standard.prompt")
        assert len(violations) == 0

    def test_bad_unclosed_pl001_violations(self):
        violations = lint_file(FIXTURES / "bad_unclosed.prompt")
        codes = [v["code"] for v in violations]
        assert "PL001" in codes
        assert len(violations) >= 2

    def test_bad_fluff_pl003_violations(self):
        violations = lint_file(FIXTURES / "bad_fluff.prompt")
        codes = [v["code"] for v in violations]
        assert "PL003" in codes

    def test_bad_fluff_has_system_identity(self):
        violations = lint_file(FIXTURES / "bad_fluff.prompt")
        codes = [v["code"] for v in violations]
        assert "PL002" not in codes

    def test_reads_utf8_file(self):
        path = FIXTURES / "good_standard.prompt"
        violations = lint_file(path)
        assert isinstance(violations, list)
