"""
Migrate command - Manages database migrations
"""
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.prompt import Prompt

from aiplanet.utils.console import print_error, print_info, print_success, print_warning, spinner

app = typer.Typer(help="Manage database migrations")


def get_package_dir() -> Path:
    """
    Find the package directory in the current project.
    The package directory is assumed to be the first directory that:
    1. Contains a __init__.py file
    2. And isn't 'tests', 'migrations', etc.
    
    Returns:
        Path to the package directory
    """
    ignored_dirs = ['tests', 'migrations', 'venv', '.venv', '.git', '__pycache__']
    
    # Look for directories in the current working directory
    cwd = Path.cwd()
    for path in cwd.iterdir():
        if path.is_dir() and path.name not in ignored_dirs:
            # Check if it has an __init__.py file (indicating it's a package)
            if (path / "__init__.py").is_file():
                return path
    
    # If no package directory is found, use the current directory
    # This fallback is to maintain compatibility with projects using the old structure
    print_warning("No package directory found. Using current directory.")
    return cwd


@app.command(name="init")
def migrate_init():
    """
    Initialize migrations with Alembic.
    """
    # Check if alembic.ini already exists
    alembic_ini_path = Path("alembic.ini")
    migrations_dir = Path("migrations")
    
    if alembic_ini_path.exists() and migrations_dir.exists():
        print_warning("Migrations are already initialized.")
        reinit = typer.confirm("Do you want to reinitialize?", default=False)
        if not reinit:
            raise typer.Exit(0)
    
    with spinner("Initializing migrations"):
        try:
            # Run alembic init
            subprocess.run(
                ["alembic", "init", "migrations"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            
            # Get package name for env.py modification
            package_dir = get_package_dir()
            package_name = package_dir.name
            
            # Modify env.py to include the package models
            env_py_path = Path("migrations") / "env.py"
            if env_py_path.exists():
                with open(env_py_path, "r") as f:
                    content = f.read()
                
                # Add import for the package models
                if "target_metadata = None" in content and f"import {package_name}" not in content:
                    # Find where to insert imports
                    import_pos = content.find("from alembic import context")
                    if import_pos != -1:
                        import_end = content.find("\n\n", import_pos)
                        if import_end != -1:
                            # Add imports for the models
                            new_imports = f"\nfrom {package_name}.models import Base"
                            modified_content = content[:import_end] + new_imports + content[import_end:]
                            
                            # Replace target_metadata = None with Base.metadata
                            modified_content = modified_content.replace(
                                "target_metadata = None",
                                f"target_metadata = Base.metadata"
                            )
                            
                            with open(env_py_path, "w") as f:
                                f.write(modified_content)
                            
                            print_info(f"Modified migrations/env.py to use {package_name}.models.Base")
            
            print_success("Migrations initialized successfully.")
            
        except (subprocess.SubprocessError, FileNotFoundError):
            print_error("Failed to initialize migrations. Is alembic installed?")
            print_info("You can install it with: pip install alembic")
            raise typer.Exit(1)
        except Exception as e:
            print_error(f"Error initializing migrations: {str(e)}")
            raise typer.Exit(1)


@app.command(name="create")
def migrate_create(
    message: str = typer.Argument(..., help="Migration message"),
    autogenerate: bool = typer.Option(
        True, "--autogenerate/--no-autogenerate", help="Auto-generate migration"
    ),
):
    """
    Create a new migration revision.
    """
    # Check if alembic.ini exists
    alembic_ini_path = Path("alembic.ini")
    if not alembic_ini_path.exists():
        print_error("Migrations are not initialized.")
        print_info("Run 'aiplanet migrate init' first.")
        raise typer.Exit(1)
    
    # Prepare alembic command
    command = ["alembic", "revision"]
    
    if autogenerate:
        command.append("--autogenerate")
    
    command.extend(["-m", message])
    
    with spinner(f"Creating migration: {message}"):
        try:
            # Run alembic revision
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            
            # Extract revision file path from output
            output = result.stdout
            print_success("Migration created successfully.")
            print_info(output)
            
        except (subprocess.SubprocessError, FileNotFoundError):
            print_error("Failed to create migration. Is alembic installed?")
            print_info("You can install it with: pip install alembic")
            raise typer.Exit(1)
        except Exception as e:
            print_error(f"Error creating migration: {str(e)}")
            raise typer.Exit(1)


@app.command(name="upgrade")
def migrate_upgrade(
    revision: str = typer.Argument("head", help="Revision to upgrade to (default: head)"),
    sql: bool = typer.Option(False, "--sql", help="Generate SQL instead of executing"),
):
    """
    Upgrade database to the specified revision.
    """
    # Check if alembic.ini exists
    alembic_ini_path = Path("alembic.ini")
    if not alembic_ini_path.exists():
        print_error("Migrations are not initialized.")
        print_info("Run 'aiplanet migrate init' first.")
        raise typer.Exit(1)
    
    # Prepare alembic command
    command = ["alembic", "upgrade"]
    
    if sql:
        command.append("--sql")
    
    command.append(revision)
    
    action = "Generating SQL for" if sql else "Upgrading database to"
    with spinner(f"{action} revision: {revision}"):
        try:
            # Run alembic upgrade
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            
            output = result.stdout
            if output:
                print_info(output)
            
            if sql:
                print_success(f"SQL generated for revision: {revision}")
            else:
                print_success(f"Database upgraded to revision: {revision}")
            
        except (subprocess.SubprocessError, FileNotFoundError):
            print_error("Failed to upgrade database. Is alembic installed?")
            print_info("You can install it with: pip install alembic")
            raise typer.Exit(1)
        except Exception as e:
            print_error(f"Error upgrading database: {str(e)}")
            raise typer.Exit(1)


@app.command(name="downgrade")
def migrate_downgrade(
    revision: str = typer.Argument(..., help="Revision to downgrade to"),
    sql: bool = typer.Option(False, "--sql", help="Generate SQL instead of executing"),
):
    """
    Downgrade database to the specified revision.
    """
    # Check if alembic.ini exists
    alembic_ini_path = Path("alembic.ini")
    if not alembic_ini_path.exists():
        print_error("Migrations are not initialized.")
        print_info("Run 'aiplanet migrate init' first.")
        raise typer.Exit(1)
    
    # Confirm downgrade
    if not sql:
        confirm = typer.confirm(
            "Downgrading may result in data loss. Are you sure you want to continue?",
            default=False,
        )
        if not confirm:
            print_warning("Operation cancelled.")
            raise typer.Exit(0)
    
    # Prepare alembic command
    command = ["alembic", "downgrade"]
    
    if sql:
        command.append("--sql")
    
    command.append(revision)
    
    action = "Generating SQL for" if sql else "Downgrading database to"
    with spinner(f"{action} revision: {revision}"):
        try:
            # Run alembic downgrade
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            
            output = result.stdout
            if output:
                print_info(output)
            
            if sql:
                print_success(f"SQL generated for downgrade to revision: {revision}")
            else:
                print_success(f"Database downgraded to revision: {revision}")
            
        except (subprocess.SubprocessError, FileNotFoundError):
            print_error("Failed to downgrade database. Is alembic installed?")
            print_info("You can install it with: pip install alembic")
            raise typer.Exit(1)
        except Exception as e:
            print_error(f"Error downgrading database: {str(e)}")
            raise typer.Exit(1)


@app.command(name="history")
def migrate_history(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed history"),
):
    """
    Show migration history.
    """
    # Check if alembic.ini exists
    alembic_ini_path = Path("alembic.ini")
    if not alembic_ini_path.exists():
        print_error("Migrations are not initialized.")
        print_info("Run 'aiplanet migrate init' first.")
        raise typer.Exit(1)
    
    # Prepare alembic command
    command = ["alembic", "history"]
    
    if verbose:
        command.append("--verbose")
    
    try:
        # Run alembic history
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        
        output = result.stdout
        if output:
            print_info(output)
        else:
            print_info("No migration history found.")
        
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("Failed to get migration history. Is alembic installed?")
        print_info("You can install it with: pip install alembic")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error getting migration history: {str(e)}")
        raise typer.Exit(1)


@app.command(name="current")
def migrate_current():
    """
    Show current migration revision.
    """
    # Check if alembic.ini exists
    alembic_ini_path = Path("alembic.ini")
    if not alembic_ini_path.exists():
        print_error("Migrations are not initialized.")
        print_info("Run 'aiplanet migrate init' first.")
        raise typer.Exit(1)
    
    try:
        # Run alembic current
        result = subprocess.run(
            ["alembic", "current"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        
        output = result.stdout
        if output:
            print_info(output)
        else:
            print_info("No current revision found.")
        
    except (subprocess.SubprocessError, FileNotFoundError):
        print_error("Failed to get current revision. Is alembic installed?")
        print_info("You can install it with: pip install alembic")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error getting current revision: {str(e)}")
        raise typer.Exit(1)