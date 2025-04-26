"""
Gen command - Generates complete modules with all necessary components
"""
import os
from pathlib import Path
from typing import Optional

import typer
from rich.prompt import Confirm

from aiplanet.commands.add import (
    add_const,
    add_exception,
    add_job,
    add_middleware,
    add_model,
    add_route,
    add_schema,
    add_service,
    add_utils,
)
from aiplanet.utils.console import print_info, print_success, print_warning, spinner

app = typer.Typer(help="Generate complete modules with all necessary components")


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


@app.command(name="module")
def gen_module(
    name: str = typer.Argument(..., help="Name of the module to generate"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the module"
    ),
    with_middleware: bool = typer.Option(
        False, "--middleware", "-m", help="Include middleware"
    ),
    with_exception: bool = typer.Option(
        False, "--exception", "-e", help="Include exception"
    ),
    version: Optional[str] = typer.Option(
        "v1", "--version", "-v", help="API version for router"
    ),
):
    """
    Generate a complete module with service, job, constants, router, utils, schema, and model.
    """
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description_base = name_snake.replace("_", " ")
        description = f"Module for {description_base} functionality"
    
    print_info(f"Generating complete module: {name_snake}")
    
    with spinner("Generating module components"):
        # Generate all components with error handling to continue even if some fail
        try:
            add_service(name_snake, description=f"Service for {description_base} operations")
        except Exception as e:
            print_warning(f"Service {name_snake}_service.py could not be generated. Continuing with other components.")
        
        try:
            add_job(name_snake, description=f"Jobs related to {description_base}")
        except Exception as e:
            print_warning(f"Job {name_snake}_job.py could not be generated. Continuing with other components.")
        
        try:
            add_const(name_snake, description=f"Constants related to {description_base}")
        except Exception as e:
            print_warning(f"Constants {name_snake}.py could not be generated. Continuing with other components.")
        
        try:
            # Modified route generation with version parameter
            add_route(
                name_snake, 
                description=f"Router for {description_base} endpoints", 
                version=version
            )
        except Exception as e:
            print_warning(f"Router {name_snake}.py could not be generated. Continuing with other components.")
        
        try:
            add_utils(name_snake, description=f"Utility functions for {description_base}")
        except Exception as e:
            print_warning(f"Utils {name_snake}.py could not be generated. Continuing with other components.")
        
        try:
            add_schema(name_snake, description=f"Pydantic schemas for {description_base}")
        except Exception as e:
            print_warning(f"Schema {name_snake}.py could not be generated. Continuing with other components.")
        
        try:
            add_model(name_snake, description=f"{description_base.title()} model")
        except Exception as e:
            print_warning(f"Model {name_snake}.py could not be generated. Continuing with other components.")
        
        # Optional components
        if with_middleware:
            try:
                add_middleware(name_snake, description=f"Middleware for {description_base}")
            except Exception as e:
                print_warning(f"Middleware {name_snake}.py could not be generated. Continuing with other components.")
        
        if with_exception:
            try:
                add_exception(name_snake, description=f"Custom exceptions for {description_base}")
            except Exception as e:
                print_warning(f"Exception {name_snake}.py could not be generated.")
    
    # Get package name for output information
    package_dir = get_package_dir()
    package_name = package_dir.name
    
    print_success(f"Module {name_snake} generated successfully!")
    print_info(f"Components created under {package_name}/ directory")


@app.command(name="crud")
def gen_crud(
    name: str = typer.Argument(..., help="Name of the resource for CRUD operations"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the resource"
    ),
    version: Optional[str] = typer.Option(
        "v1", "--version", "-v", help="API version for router"
    )
):
    """
    Generate a complete CRUD setup for a resource.
    """
    # This is similar to gen_module but optimized for CRUD operations
    gen_module(name, description, version=version)
    
    # Get package name for output information
    package_dir = get_package_dir()
    package_name = package_dir.name
    
    print_success(f"CRUD operations for {name} generated successfully!")
    print_info("The CRUD setup includes:")
    print_info("- Model with standard fields")
    print_info("- Service with CRUD operations")
    print_info("- Router with CRUD endpoints")
    print_info("- Schemas for Create, Update, and Response")
    print_info(f"Components created under {package_name}/ directory")