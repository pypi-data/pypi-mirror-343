"""
Build command - Creates a new FastAPI project with the recommended structure
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.prompt import Confirm

from aiplanet.utils.console import (
    confirm,
    print_error,
    print_info,
    print_success,
    print_warning,
    spinner,
)
from aiplanet.utils.filesystem import (
    create_directory,
    create_file,
)
from aiplanet.utils.templates import render_template

app = typer.Typer(help="Create a new FastAPI project")


@app.command(name="project")
def build_project(
    project_name: str = typer.Argument(..., help="Name of the project to create"),
    with_docker: bool = typer.Option(
        False, "--docker", "-d", help="Include Docker configuration"
    ),
    with_pre_commit: bool = typer.Option(
        False, "--pre-commit", "-p", help="Include pre-commit hooks"
    ),
    minimal: bool = typer.Option(
        False, "--minimal", "-m", help="Create a minimal project"
    ),
):
    """
    Create a new FastAPI project with the recommended structure.
    """
    project_dir = Path(project_name)
    
    # Check if directory already exists
    if project_dir.exists():
        overwrite = confirm(
            f"Directory {project_name} already exists. Do you want to overwrite it?",
            default=False,
        )
        if not overwrite:
            print_warning("Project creation aborted.")
            raise typer.Exit(1)
    
    with spinner(f"Creating project: {project_name}"):
        # Create project directory
        create_directory(project_dir)
        
        # Create package directory - using snake_case for the package name
        package_name = project_name.lower().replace("-", "_").replace(" ", "_")
        package_dir = project_dir / package_name
        create_directory(package_dir)
        
        # Create __init__.py in the package root with version
        create_file(
            package_dir / "__init__.py",
            f'"""\\n{project_name} - FastAPI application\\n"""\n__version__ = "0.1.0"\n'
        )
        
        # Create standard directories inside the package
        directories = [
            "routers",
            "services",
            "models",
            "schemas",
            "constants",
            "core",
            "jobs",
            "exceptions",
            "utils",
        ]
        
        if not minimal:
            directories.extend(["middleware"])
        
        for directory in directories:
            create_directory(package_dir / directory)
            create_file(package_dir / directory / "__init__.py", "")
        
        # Create tests directory at the project root (not in the package)
        create_directory(project_dir / "tests")
        create_file(project_dir / "tests" / "__init__.py", "")
        
        # Create core files
        create_core_files(package_dir)
        
        # Create gitignore
        create_gitignore(project_dir)
        
        # Create readme
        create_file(
            project_dir / "README.md",
            render_template("README.md.jinja", {"project_name": project_name})
        )
        
        # Create main.py in the project root
        create_main_file(project_dir, project_name, package_name)
        
        # Create Docker configuration
        if with_docker:
            create_docker_files(project_dir, project_name, package_name)
        
        
        # Create pre-commit hooks
        if with_pre_commit:
            create_pre_commit_config(project_dir)
        
        # Create Poetry configuration
        create_poetry_files(project_dir, project_name, package_name)
        
        # Create migrations directory and alembic.ini at project root
        create_migrations_files(project_dir, package_name)
    
    print_success(f"Project {project_name} created successfully!")
    
    # Ask for Git initialization
    if confirm("Initialize Git repository?", default=True):
        try:
            with spinner("Initializing Git repository"):
                # Check if git is installed
                git_check = subprocess.run(
                    ["git", "--version"],
                    capture_output=True,
                    text=True
                )
                if git_check.returncode != 0:
                    raise FileNotFoundError("Git command not found")
                    
                # Run git init with verbose output
                git_result = subprocess.run(
                    ["git", "init"],
                    cwd=project_dir,
                    capture_output=True,
                    text=True
                )
                
                if git_result.returncode != 0:
                    print_error(f"Git init failed: {git_result.stderr}")
                    raise subprocess.SubprocessError("Git init command failed")
                
                # Verify .git directory exists
                git_dir = project_dir / ".git"
                if not git_dir.exists():
                    print_error(f".git directory was not created at {git_dir}")
                    raise FileNotFoundError(".git directory not found after git init")
                    
            print_success(f"Git repository initialized at {project_dir}")
            print_info(f"Created .git directory: {git_dir}")
        except (subprocess.SubprocessError, FileNotFoundError) as e:
            print_error(f"Failed to initialize Git repository: {str(e)}")
            print_warning("Please make sure Git is installed and try manually with 'git init' in the project directory.")

    print_info("\nTo start working on your project:")
    print_info(f"  cd {project_name}")
    print_info(f"  poetry shell  # Activate the virtual environment")
    print_info(f"  uvicorn main:app --reload  # Start the development server")


def create_core_files(package_dir: Path):
    """Create files in the core directory."""
    # Get the package name (the directory name)
    package_name = package_dir.name
    
    # Create database.py
    db_content = render_template("core/database.py.jinja", {
        "project_name": package_dir.parent.name,
        "package_name": package_name
    })
    create_file(package_dir / "core" / "database.py", db_content)
    
    # Create config.py
    config_content = render_template("core/config.py.jinja", {
        "project_name": package_dir.parent.name,
        "package_name": package_name
    })
    create_file(package_dir / "core" / "config.py", config_content)
    
    # Create security.py
    security_content = render_template("core/security.py.jinja", {
        "package_name": package_name
    })
    create_file(package_dir / "core" / "security.py", security_content)
    
    # Create logging.py
    logging_content = render_template("core/logging.py.jinja", {
        "package_name": package_name
    })
    create_file(package_dir / "core" / "logging.py", logging_content)
    
    # Create .env and .env.example at project root
    create_env_files(package_dir.parent)


def create_migrations_files(project_dir: Path, package_name: str):
    """Create migrations directory and files."""
    # Create migrations directory at project root
    create_directory(project_dir / "migrations")
    create_directory(project_dir / "migrations" / "versions")
    
    # Create alembic.ini
    alembic_ini_content = render_template("alembic.ini.jinja", {
        "project_name": project_dir.name,
        "package_name": package_name
    })
    create_file(project_dir / "alembic.ini", alembic_ini_content)
    
    # Create migrations/env.py
    alembic_env_content = render_template("migrations/env.py.jinja", {
        "project_name": project_dir.name,
        "package_name": package_name
    })
    create_file(project_dir / "migrations" / "env.py", alembic_env_content)

    # Create script.py.mako
    script_migration_content = render_template("migrations/script.py.mako.jinja", {
        "project_name": project_dir.name,
        "package_name": package_name
    })
    create_file(project_dir / "migrations" / "script.py.mako", script_migration_content)


def create_env_files(project_dir: Path):
    """Create .env and .env.example files."""
    env_content = render_template("env.jinja", {
        "project_name": project_dir.name,
        "secret_key": os.urandom(32).hex(),
    })
    create_file(project_dir / ".env", env_content)
    create_file(project_dir / ".env.example", env_content)


def create_gitignore(project_dir: Path):
    """Create .gitignore file."""
    gitignore_content = render_template("gitignore.jinja", {})
    create_file(project_dir / ".gitignore", gitignore_content)


def create_main_file(project_dir: Path, project_name: str, package_name: str):
    """Create main.py file."""
    main_content = render_template("main.py.jinja", {
        "project_name": project_name,
        "package_name": package_name
    })
    create_file(project_dir / "main.py", main_content)


def create_docker_files(project_dir: Path, project_name: str, package_name: str):
    """Create Docker configuration files."""
    # Create docker directory
    create_directory(project_dir / "docker")
    
    # Create Dockerfile
    dockerfile_content = render_template("docker/Dockerfile.jinja", {
        "project_name": project_name,
        "package_name": package_name
    })
    create_file(project_dir / "docker" / "Dockerfile", dockerfile_content)
    
    # Create docker-compose.yml
    docker_compose_content = render_template("docker/docker-compose.yml.jinja", {
        "project_name": project_name,
        "package_name": package_name
    })
    create_file(project_dir / "docker-compose.yml", docker_compose_content)



def create_pre_commit_config(project_dir: Path):
    """Create pre-commit hooks configuration."""
    pre_commit_content = render_template("pre-commit-config.yaml.jinja", {})
    create_file(project_dir / ".pre-commit-config.yaml", pre_commit_content)


def create_poetry_files(project_dir: Path, project_name: str, package_name: str):
    """Create Poetry configuration files."""
    poetry_content = render_template("pyproject.toml.jinja", {
        "project_name": project_name,
        "project_slug": package_name,
    })
    create_file(project_dir / "pyproject.toml", poetry_content)