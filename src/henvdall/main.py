"""Main CLI application for Henvdall."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .audit import EnvAuditor
from .logo import get_logo_with_tagline
from .sync import EnvSyncManager

app = typer.Typer(
    name="henvdall",
    help="The Gatekeeper of Environment Variables - Ensure your .env stays in sync",
    add_completion=False,
)

console = Console()


@app.command()
def sync(
    example_file: Optional[Path] = typer.Option(
        None,
        "--example",
        "-e",
        help="Path to .env.example file",
    ),
    env_file: Optional[Path] = typer.Option(
        None,
        "--env",
        "-f",
        help="Path to .env file",
    ),
    backup_file: Optional[Path] = typer.Option(
        None,
        "--backup",
        "-b",
        help="Path for backup file (default: .env.bak)",
    ),
):
    """
    Sync .env file with .env.example template.

    Compares your .env.example file with your local .env file and prompts
    you to fill in any missing environment variables.
    """
    cwd = Path.cwd()

    example_path = example_file or cwd / ".env.example"
    env_path = env_file or cwd / ".env"

    console.print(get_logo_with_tagline(), style="cyan")
    console.print()

    manager = EnvSyncManager(console=console)
    manager.sync(
        example_path=example_path,
        env_path=env_path,
        backup_path=backup_file,
    )


@app.command()
def audit(
    env_file: Optional[Path] = typer.Option(
        None,
        "--env",
        "-f",
        help="Path to .env file",
    ),
):
    """
    Audit .env file for placeholder values.

    Scans your .env file and warns about values that look like placeholders
    (e.g., "YOUR_API_KEY_HERE", "admin123") that should be changed before
    running your application.
    """
    cwd = Path.cwd()
    env_path = env_file or cwd / ".env"

    console.print(get_logo_with_tagline(), style="cyan")
    console.print("[bold]Audit Mode:[/bold] Detecting Placeholder Values\n")

    auditor = EnvAuditor(console=console)
    has_issues = auditor.audit(env_path=env_path)

    if has_issues:
        raise typer.Exit(code=1)


@app.command()
def version():
    """Display version information."""
    from . import __version__

    console.print(f"Henvdall version [cyan]{__version__}[/cyan]")


if __name__ == "__main__":
    app()
