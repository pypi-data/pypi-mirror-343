#!/usr/bin/env python3
"""
AIplanet CLI - A tool for generating FastAPI project boilerplate
"""
import sys
from typing import Optional

import typer
from rich.console import Console

from aiplanet.commands import add, build, gen, remove, run, migrate
from aiplanet.utils.console import print_banner

# Create Typer app
app = typer.Typer(
    name="aiplanet",
    help="A tool for generating FastAPI project boilerplate",
    add_completion=True,
)

# Create console
console = Console()

# Add commands
app.add_typer(build.app, name="build")
app.add_typer(add.app, name="add")
app.add_typer(remove.app, name="remove")
app.add_typer(gen.app, name="gen")
app.add_typer(run.app, name="run")
app.add_typer(migrate.app, name="migrate")


@app.callback()
def main(version: Optional[bool] = typer.Option(
    None, "--version", "-v", help="Show version and exit", is_flag=True
)):
    """
    AIplanet CLI - A tool for generating FastAPI project boilerplate
    """
    if version:
        from aiplanet import __version__
        print_banner()
        console.print(f"[bold]AIplanet CLI[/bold] version: [green]{__version__}[/green]")
        raise typer.Exit()


if __name__ == "__main__":
    app()