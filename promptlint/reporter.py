import json

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def _severity_style(severity):
    """Return (icon, style_name) for a given severity string."""
    if severity == "error":
        return "X", "red"
    return "!", "yellow"


def print_results(results, filepath):
    """Display all violations for *filepath* in a richly formatted table."""
    if not results:
        return

    console.print()
    console.print(f"[bold underline]{filepath}[/]")
    table = Table(show_header=True, header_style="bold", box=box.SIMPLE)
    table.add_column("", width=3)
    table.add_column("Rule", width=6, no_wrap=True)
    table.add_column("Location", width=10, no_wrap=True)
    table.add_column("Message")
    table.add_column("Description", overflow="fold")

    for r in results:
        icon, style = _severity_style(r["severity"])
        loc = f"{r['line']}:{r['column']}"
        table.add_row(
            f"[{style}]{icon}[/]",
            f"[{style}]{r['code']}[/]",
            loc,
            r.get("message", ""),
            r.get("description", ""),
        )

    console.print(table)


def print_summary(total_files, total_errors, total_warnings):
    """Print a one-line summary of the lint session."""
    parts = [f"Scanned {total_files} file(s)"]
    if total_errors:
        parts.append(f"[red]{total_errors} error(s)[/]")
    else:
        parts.append("[green]0 errors[/]")
    if total_warnings:
        parts.append(f"[yellow]{total_warnings} warning(s)[/]")
    else:
        parts.append("[green]0 warnings[/]")
    console.print(" | ".join(parts))


def print_success(filepath):
    """Print a green checkmark for a clean file."""
    console.print(f"  [green]PASS[/] {filepath}")


def format_json(all_results):
    """Return a JSON string of all results keyed by filepath."""
    return json.dumps(all_results, indent=2, ensure_ascii=False)
