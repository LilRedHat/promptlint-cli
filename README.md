markdown

# promptlint-cli

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

**Lint your prompts. Ship with confidence.**

`promptlint-cli` is a static analysis tool for detecting common issues in prompt files used with large language models (LLMs). It helps teams maintain consistency, clarity, and quality across their prompt libraries by enforcing a set of best-practice rules.

## Features

- **PL001 — Unclosed Variables** — Flags unclosed `{{` or `[` delimiters, preventing broken variable injection during runtime.
- **PL002 — Missing System Identity** — Flags prompts that fail to define a system role (e.g., `# System`, `Role:`, `You are a`) within the first 500 characters.
- **PL003 — Token Waste (Politeness)** — Flags excessive conversational politeness (e.g., "Please", "Kindly", "Thank you") that consumes unnecessary context window tokens.
- **PL004 — Empty Files** — Flags target files that are completely empty or contain only whitespace characters.

## Installation

```bash
pip install promptlint-cli

```

Or install from source:

```bash
git clone [https://github.com/your-org/promptlint-cli.git](https://github.com/your-org/promptlint-cli.git)
cd promptlint-cli
pip install .

```

## Quick Start

Analyze a single prompt file:

```bash
promptlint check prompt.prompt

```

Analyze all prompt files in a directory:

```bash
promptlint check *.prompt

```

Output results in JSON format:

```bash
promptlint check --json *.prompt

```

## Rule Reference

| Code  | Severity | Description                                                      |
| ----- | -------- | ---------------------------------------------------------------- |
| PL001 | Error    | Unclosed `{{` or `[` delimiters detected.                        |
| PL002 | Warning  | Missing system identity flag (`# System`, `Role:`, `You are a`). |
| PL003 | Warning  | Excessive politeness consuming unnecessary tokens.               |
| PL004 | Error    | Empty or whitespace-only files.                                  |

## Exit Codes

| Code | Meaning                                  |
| ---- | ---------------------------------------- |
| 0    | All checks passed — no violations found. |
| 1    | One or more violations were detected.    |

## Development

```bash
git clone [https://github.com/your-org/promptlint-cli.git](https://github.com/your-org/promptlint-cli.git)
cd promptlint-cli
pip install -e .
pytest tests/

```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-org/promptlint-cli). Make sure existing tests pass and add new tests for any added functionality.

## License

This project is licensed under the MIT License. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

## Project Status

**Alpha** — The API and rule set are under active development and may change without notice. Use in production at your own discretion.

```

```
