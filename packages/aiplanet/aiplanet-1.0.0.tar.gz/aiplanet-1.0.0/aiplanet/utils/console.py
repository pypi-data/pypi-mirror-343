"""
Console utilities for aiplanet CLI
"""
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.style import Style
from rich.table import Table
from rich.text import Text

console = Console()


def print_banner():
    """Print the AIplanet CLI banner"""
    banner = """
    █████╗ ██╗██████╗ ██╗      █████╗ ███╗   ██╗███████╗████████╗
   ██╔══██╗██║██╔══██╗██║     ██╔══██╗████╗  ██║██╔════╝╚══██╔══╝
   ███████║██║██████╔╝██║     ███████║██╔██╗ ██║█████╗     ██║   
   ██╔══██║██║██╔═══╝ ██║     ██╔══██║██║╚██╗██║██╔══╝     ██║   
   ██║  ██║██║██║     ███████╗██║  ██║██║ ╚████║███████╗   ██║   
   ╚═╝  ╚═╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   
    """
    console.print(Panel(banner, style="bold blue"))


def confirm(message: str, default: bool = True) -> bool:
    """
    Ask for confirmation.
    
    Args:
        message: Message to display
        default: Default value
        
    Returns:
        True if confirmed, False otherwise
    """
    return Confirm.ask(message, default=default)


def prompt(message: str, default: Optional[str] = None) -> str:
    """
    Ask for input.
    
    Args:
        message: Message to display
        default: Default value
        
    Returns:
        User input
    """
    return Prompt.ask(message, default=default)


def print_success(message: str):
    """
    Print a success message.
    
    Args:
        message: Message to display
    """
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str):
    """
    Print an error message.
    
    Args:
        message: Message to display
    """
    console.print(f"[bold red]✗[/bold red] {message}")


def print_warning(message: str):
    """
    Print a warning message.
    
    Args:
        message: Message to display
    """
    console.print(f"[bold yellow]![/bold yellow] {message}")


def print_info(message: str):
    """
    Print an info message.
    
    Args:
        message: Message to display
    """
    console.print(f"[bold blue]i[/bold blue] {message}")


def spinner(message: str):
    """
    Create a spinner context manager.
    
    Args:
        message: Message to display
        
    Returns:
        Progress context manager
    """
    return Progress(
        SpinnerColumn(),
        TextColumn(f"[bold blue]{message}[/bold blue]"),
        transient=True,
    )


def print_table(headers: List[str], rows: List[List[Any]], title: Optional[str] = None):
    """
    Print a table.
    
    Args:
        headers: Table headers
        rows: Table rows
        title: Table title
    """
    table = Table(title=title)
    
    for header in headers:
        table.add_column(header, style="bold")
    
    for row in rows:
        table.add_row(*[str(cell) for cell in row])
    
    console.print(table)