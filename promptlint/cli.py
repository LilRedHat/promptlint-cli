import glob as glob_mod
import os
import sys

import click

from promptlint.engine import lint_file
from promptlint.reporter import print_results, print_summary, print_success, format_json


@click.group()
def cli():
    """promptlint — a linting tool for LLM prompt files."""


@cli.command()
@click.argument("paths", nargs=-1, required=True)
@click.option("--json", "json_output", is_flag=True, help="Output results as JSON")
def check(paths, json_output):
    """Lint one or more prompt files.

    PATHS may be file paths or glob patterns (e.g. ``prompts/**/*.md``).
    """
    if json_output:
        _check_json(paths)
    else:
        _check_rich(paths)


def _check_rich(paths):
    """Lint files and print human-readable output via Rich."""
    all_results = {}
    total_errors = 0
    total_warnings = 0
    missing_files = 0
    files_scanned = set()

    for pattern in paths:
        for fp in _resolve_paths(pattern):
            if fp in files_scanned:
                continue
            files_scanned.add(fp)
            if not os.path.isfile(fp):
                click.echo(f"File not found: {fp}", err=True)
                missing_files += 1
                continue
            try:
                results = lint_file(fp)
            except Exception as exc:
                click.echo(f"Error reading {fp}: {exc}", err=True)
                continue

            all_results[fp] = results
            for r in results:
                if r["severity"] == "error":
                    total_errors += 1
                else:
                    total_warnings += 1

            if results:
                print_results(results, fp)
            else:
                print_success(fp)

    if files_scanned:
        print_summary(len(files_scanned), total_errors, total_warnings)

    sys.exit(1 if total_errors > 0 or total_warnings > 0 or missing_files > 0 else 0)


def _check_json(paths):
    """Lint files and emit a JSON blob to stdout."""
    all_results = {}
    total_errors = 0
    total_warnings = 0
    missing_files = 0
    files_scanned = set()

    for pattern in paths:
        for fp in _resolve_paths(pattern):
            if fp in files_scanned:
                continue
            files_scanned.add(fp)
            if not os.path.isfile(fp):
                missing_files += 1
                continue
            try:
                results = lint_file(fp)
            except Exception:
                continue

            all_results[fp] = results
            for r in results:
                if r["severity"] == "error":
                    total_errors += 1
                else:
                    total_warnings += 1

    output = {
        "files": all_results,
        "summary": {
            "total_files": len(files_scanned),
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "missing_files": missing_files,
        },
    }
    click.echo(format_json(output))
    sys.exit(1 if total_errors > 0 or total_warnings > 0 or missing_files > 0 else 0)


def _resolve_paths(pattern):
    """Expand a glob pattern or return the literal path."""
    expanded = glob_mod.glob(pattern, recursive=True)
    if expanded:
        for p in expanded:
            yield os.path.normpath(p)
    else:
        yield os.path.normpath(pattern)


main = cli

if __name__ == "__main__":
    main()
