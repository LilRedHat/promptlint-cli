import pytest
from promptlint.rules import check_all


class TestPL001UnclosedDelimiters:
    def test_unclosed_double_curly(self):
        violations = check_all("Hello {{name, how are you?")
        codes = [v["code"] for v in violations]
        assert "PL001" in codes

    def test_unclosed_single_bracket(self):
        violations = check_all("Please provide your [contact information.")
        codes = [v["code"] for v in violations]
        assert "PL001" in codes

    def test_closed_delimiters_pass(self):
        violations = check_all("Hello {{name}}, how are you?")
        codes = [v["code"] for v in violations]
        assert "PL001" not in codes


class TestPL002MissingSystemIdentity:
    def test_no_system_flag(self):
        violations = check_all("Just a plain prompt without identity.")
        codes = [v["code"] for v in violations]
        assert "PL002" in codes

    def test_role_flag_passes(self):
        violations = check_all("Role: Technical Writer")
        codes = [v["code"] for v in violations]
        assert "PL002" not in codes

    def test_system_header_passes(self):
        violations = check_all("# System\nYou are a helpful assistant.")
        codes = [v["code"] for v in violations]
        assert "PL002" not in codes

    def test_you_are_pattern_passes(self):
        violations = check_all("You are a helpful assistant.")
        codes = [v["code"] for v in violations]
        assert "PL002" not in codes


class TestPL003ExcessivePoliteness:
    def test_please_triggers(self):
        violations = check_all("Please provide your details.")
        codes = [v["code"] for v in violations]
        assert "PL003" in codes

    def test_kindly_triggers(self):
        violations = check_all("Kindly submit the form.")
        codes = [v["code"] for v in violations]
        assert "PL003" in codes

    def test_thank_you_triggers(self):
        violations = check_all("Thank you for your help.")
        codes = [v["code"] for v in violations]
        assert "PL003" in codes


class TestPL004EmptyFile:
    def test_empty_string(self):
        violations = check_all("")
        codes = [v["code"] for v in violations]
        assert "PL004" in codes

    def test_whitespace_only(self):
        violations = check_all("   \n  \t  \n  ")
        codes = [v["code"] for v in violations]
        assert "PL004" in codes


class TestGoodContentPassesAllRules:
    def test_standard_prompt_no_violations(self):
        content = """# System
Role: Technical Assistant
You are a helpful AI assistant specialized in answering programming questions.

Answer the user's question concisely and accurately.
Provide code examples when relevant."""
        violations = check_all(content)
        assert len(violations) == 0
