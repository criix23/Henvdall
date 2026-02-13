"""Sync logic for environment variables."""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from .parser import EnvEntry, EnvFileParser
from .validator import EnvValueValidator


class EnvSyncManager:
    """Manager for syncing .env files with .env.example."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.parser = EnvFileParser()
        self.validator = EnvValueValidator()

    def sync(
        self,
        example_path: Path,
        env_path: Path,
        backup_path: Optional[Path] = None,
    ) -> bool:
        """
        Sync .env file with .env.example.

        Returns True if any changes were made, False otherwise.
        """
        if not example_path.exists():
            self.console.print(
                f"[red]Error:[/red] .env.example file not found at {example_path}",
                style="bold",
            )
            return False

        example_entries = self.parser.parse_file(example_path)
        env_entries = self.parser.parse_file(env_path)

        missing_keys = self._find_missing_keys(example_entries, env_entries)

        if not missing_keys:
            self.console.print(
                Panel(
                    "[green]✓[/green] All environment variables are in sync!",
                    title="Sync Complete",
                    border_style="green",
                )
            )
            return False

        self._display_missing_keys(missing_keys, example_entries)

        if not self._confirm_sync():
            self.console.print("[yellow]Sync cancelled.[/yellow]")
            return False

        self._create_backup(env_path, backup_path)

        new_entries = self._collect_values(missing_keys, example_entries)

        self._append_to_env(env_path, new_entries)

        self._display_summary(new_entries)

        return True

    def _find_missing_keys(
        self,
        example_entries: Dict[str, EnvEntry],
        env_entries: Dict[str, EnvEntry],
    ) -> List[str]:
        """Find keys present in example but missing in env."""
        return [key for key in example_entries if key not in env_entries]

    def _display_missing_keys(
        self,
        missing_keys: List[str],
        example_entries: Dict[str, EnvEntry],
    ):
        """Display a table of missing keys."""
        table = Table(title="Missing Environment Variables", show_header=True)
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Example Value", style="yellow")
        table.add_column("Validation", style="magenta")

        for key in missing_keys:
            entry = example_entries[key]
            validation_type = self.validator.extract_validation_type(entry.comment)
            validation_str = f"({validation_type})" if validation_type else "-"

            table.add_row(key, entry.value, validation_str)

        self.console.print()
        self.console.print(table)
        self.console.print()

    def _confirm_sync(self) -> bool:
        """Ask user to confirm sync operation."""
        response = Prompt.ask(
            "[bold]Proceed with sync?[/bold]",
            choices=["y", "n"],
            default="y",
        )
        return response.lower() == "y"

    def _create_backup(self, env_path: Path, backup_path: Optional[Path]):
        """Create a backup of the .env file."""
        if not env_path.exists():
            return

        if backup_path is None:
            backup_path = env_path.parent / f"{env_path.name}.bak"

        shutil.copy2(env_path, backup_path)
        self.console.print(
            f"[dim]Created backup at {backup_path}[/dim]",
        )

    def _collect_values(
        self,
        missing_keys: List[str],
        example_entries: Dict[str, EnvEntry],
    ) -> Dict[str, str]:
        """Collect values for missing keys from user input."""
        new_entries = {}

        self.console.print(
            Panel(
                "Please provide values for the missing environment variables",
                title="Interactive Input",
                border_style="blue",
            )
        )
        self.console.print()

        for key in missing_keys:
            entry = example_entries[key]
            validation_type = self.validator.extract_validation_type(entry.comment)

            value = self._prompt_for_value(key, entry.value, validation_type)
            new_entries[key] = value

        return new_entries

    def _prompt_for_value(
        self,
        key: str,
        example_value: str,
        validation_type: Optional[str],
    ) -> str:
        """Prompt user for a value with validation."""
        validation_hint = f" [magenta]({validation_type})[/magenta]" if validation_type else ""
        prompt_text = f"[cyan]{key}[/cyan]{validation_hint} [dim](example: {example_value})[/dim]"

        while True:
            value = Prompt.ask(prompt_text)

            result = self.validator.validate_value(value, validation_type)

            if result.is_valid:
                return value
            else:
                self.console.print(f"[red]✗[/red] {result.error_message}")

    def _append_to_env(self, env_path: Path, new_entries: Dict[str, str]):
        """Append new entries to .env file."""
        with open(env_path, 'a', encoding='utf-8') as f:
            if env_path.exists() and env_path.stat().st_size > 0:
                f.write('\n')

            f.write('# Added by Henvdall\n')
            for key, value in new_entries.items():
                line = self.parser.format_entry(key, value)
                f.write(f"{line}\n")

    def _display_summary(self, new_entries: Dict[str, str]):
        """Display a summary of changes made."""
        self.console.print()
        self.console.print(
            Panel(
                f"[green]✓[/green] Successfully added {len(new_entries)} environment variable(s)",
                title="Sync Complete",
                border_style="green",
            )
        )
