"""Audit logic for detecting placeholder values."""

from pathlib import Path
from typing import Dict, List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .parser import EnvEntry, EnvFileParser
from .validator import EnvValueValidator


class EnvAuditor:
    """Auditor for detecting placeholder values in .env files."""

    def __init__(self, console: Console = None):
        self.console = console or Console()
        self.parser = EnvFileParser()
        self.validator = EnvValueValidator()

    def audit(self, env_path: Path) -> bool:
        """
        Audit .env file for placeholder values.

        Returns True if issues were found, False otherwise.
        """
        if not env_path.exists():
            self.console.print(
                f"[red]Error:[/red] .env file not found at {env_path}",
                style="bold",
            )
            return False

        entries = self.parser.parse_file(env_path)

        if not entries:
            self.console.print(
                Panel(
                    "[yellow]⚠[/yellow] .env file is empty",
                    title="Audit Result",
                    border_style="yellow",
                )
            )
            return False

        issues = self._find_placeholder_values(entries)

        if not issues:
            self.console.print(
                Panel(
                    "[green]✓[/green] No placeholder values detected!",
                    title="Audit Complete",
                    border_style="green",
                )
            )
            return False

        self._display_issues(issues)

        return True

    def _find_placeholder_values(
        self,
        entries: Dict[str, EnvEntry],
    ) -> List[Tuple[str, str, str]]:
        """
        Find entries with placeholder values.

        Returns a list of tuples: (key, value, reason)
        """
        issues = []

        for key, entry in entries.items():
            if self.validator.is_placeholder(entry.value):
                reason = self._get_placeholder_reason(entry.value)
                issues.append((key, entry.value, reason))

        return issues

    def _get_placeholder_reason(self, value: str) -> str:
        """Get a human-readable reason why a value is considered a placeholder."""
        if not value or not value.strip():
            return "Empty value"

        for pattern in self.validator.PLACEHOLDER_PATTERNS:
            import re
            if re.search(pattern, value):
                return "Contains placeholder text"

        return "Suspicious value"

    def _display_issues(self, issues: List[Tuple[str, str, str]]):
        """Display a table of issues found."""
        self.console.print()
        self.console.print(
            Panel(
                f"[yellow]⚠[/yellow] Found {len(issues)} potential issue(s)",
                title="Audit Results",
                border_style="yellow",
            )
        )
        self.console.print()

        table = Table(show_header=True, title="Placeholder Values Detected")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Current Value", style="yellow")
        table.add_column("Issue", style="red")

        for key, value, reason in issues:
            display_value = value if value else "[dim](empty)[/dim]"
            table.add_row(key, display_value, reason)

        self.console.print(table)
        self.console.print()
        self.console.print(
            "[bold]Recommendation:[/bold] Update these values before running your application.",
        )
