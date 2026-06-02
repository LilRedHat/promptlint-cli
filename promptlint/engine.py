import os

from promptlint.rules import check_all as _default_check_all


def parse_file(filepath):
    """Read *filepath* and return its content as a string.

    Tries UTF-8 first, then falls back to Latin-1.
    Raises ``ValueError`` when neither encoding succeeds.
    """
    encodings = ("utf-8", "latin-1")
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"Unable to decode file with any supported encoding: {filepath}")


def run_lint(content, rules_func=None):
    """Pass *content* through the rules engine.

    When *rules_func* is omitted it defaults to ``check_all`` from
    :mod:`promptlint.rules`.
    """
    if rules_func is None:
        rules_func = _default_check_all
    return rules_func(content)


def lint_file(filepath):
    """Convenience: parse *filepath*, lint the content, return results."""
    content = parse_file(filepath)
    return run_lint(content)
