import re


class Rule:
    __slots__ = ("code", "severity", "name", "description", "check")

    def __init__(self, code, severity, name, description, check):
        self.code = code
        self.severity = severity
        self.name = name
        self.description = description
        self.check = check


def _check_pl001(content):
    """PL001 — Unclosed variable delimiters (Error)."""
    results = []
    lines = content.split("\n")
    for line_no, line in enumerate(lines, 1):
        if "{{" in line and "}}" not in line:
            col = line.index("{{") + 1
            results.append(
                {
                    "code": "PL001",
                    "severity": "error",
                    "name": "Unclosed variable delimiters",
                    "description": "Unclosed variable delimiters",
                    "line": line_no,
                    "column": col,
                    "message": "Unclosed opening delimiter `{{` found without matching `}}` on the same line",
                }
            )
        if "[" in line and "]" not in line:
            col = line.index("[") + 1
            results.append(
                {
                    "code": "PL001",
                    "severity": "error",
                    "name": "Unclosed variable delimiters",
                    "description": "Unclosed variable delimiters",
                    "line": line_no,
                    "column": col,
                    "message": "Unclosed opening delimiter `[` found without matching `]` on the same line",
                }
            )
    return results


def _check_pl002(content):
    """PL002 — Missing system identity flag (Warning)."""
    results = []
    preview = content[:500]
    patterns = [r"#\s*System", r"Role:", r"You are a"]
    found = any(re.search(p, preview, re.IGNORECASE) for p in patterns)
    if not found:
        results.append(
            {
                "code": "PL002",
                "severity": "warning",
                "name": "Missing system identity flag",
                "description": "Missing system identity flag",
                "line": 1,
                "column": 1,
                "message": (
                    "No system identity flag found in the first 500 characters "
                    '(expected "# System", "Role:", or "You are a")'
                ),
            }
        )
    return results


_PL003_PATTERN = re.compile(
    r"(Please|Kindly|Thank you|I would like|Could you please)",
    re.IGNORECASE,
)


def _check_pl003(content):
    """PL003 — Excessive politeness (Warning)."""
    results = []
    for line_no, line in enumerate(content.split("\n"), 1):
        for match in _PL003_PATTERN.finditer(line):
            results.append(
                {
                    "code": "PL003",
                    "severity": "warning",
                    "name": "Excessive politeness",
                    "description": "Excessive politeness",
                    "line": line_no,
                    "column": match.start() + 1,
                    "message": (
                        f'Unnecessary polite phrase "{match.group()}" detected; '
                        "prefer direct instructions"
                    ),
                }
            )
    return results


def _check_pl004(content):
    """PL004 — Empty or whitespace-only file (Error)."""
    results = []
    if not content or not content.strip():
        results.append(
            {
                "code": "PL004",
                "severity": "error",
                "name": "Empty or whitespace-only file",
                "description": "Empty or whitespace-only file",
                "line": 1,
                "column": 1,
                "message": "File is empty or contains only whitespace",
            }
        )
    return results


RULES = [
    Rule("PL001", "error", "Unclosed variable delimiters",
         "Unclosed variable delimiters", _check_pl001),
    Rule("PL002", "warning", "Missing system identity flag",
         "Missing system identity flag", _check_pl002),
    Rule("PL003", "warning", "Excessive politeness",
         "Excessive politeness", _check_pl003),
    Rule("PL004", "error", "Empty or whitespace-only file",
         "Empty or whitespace-only file", _check_pl004),
]


def check_all(content):
    """Run every registered rule against *content* and return a flat list of result dicts."""
    results = []
    for rule in RULES:
        results.extend(rule.check(content))
    return results
