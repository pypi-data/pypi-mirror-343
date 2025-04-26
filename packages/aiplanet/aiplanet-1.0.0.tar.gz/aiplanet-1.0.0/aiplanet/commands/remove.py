"""
Remove command - Removes components from the project
"""
import os
from pathlib import Path
from typing import List, Optional

import typer
from rich.prompt import Confirm

from aiplanet.utils.console import print_error, print_info, print_success, print_warning, spinner

app = typer.Typer(help="Remove components from the project")


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


@app.command(name="service")
def remove_service(
    name: str = typer.Argument(..., help="Name of the service to remove"),
):
    """Remove a service from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if service file exists
    service_path = package_dir / "services" / f"{name_snake}_service.py"
    
    if not service_path.exists():
        print_error(f"Service {name_snake}_service.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {service_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(service_path)
        print_success(f"Removed service: {service_path}")
    except Exception as e:
        print_error(f"Failed to remove {service_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="const")
def remove_const(
    name: str = typer.Argument(..., help="Name of the constants file to remove"),
):
    """Remove a constants file from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if constants file exists
    const_path = package_dir / "constants" / f"{name_snake}.py"
    
    if not const_path.exists():
        print_error(f"Constants file {name_snake}.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {const_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(const_path)
        print_success(f"Removed constants file: {const_path}")
    except Exception as e:
        print_error(f"Failed to remove {const_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="job")
def remove_job(
    name: str = typer.Argument(..., help="Name of the job to remove"),
):
    """Remove a job from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if job file exists
    job_path = package_dir / "jobs" / f"{name_snake}_job.py"
    
    if not job_path.exists():
        print_error(f"Job {name_snake}_job.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {job_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(job_path)
        print_success(f"Removed job: {job_path}")
    except Exception as e:
        print_error(f"Failed to remove {job_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="model")
def remove_model(
    name: str = typer.Argument(..., help="Name of the model to remove"),
):
    """Remove a model from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if model file exists
    model_path = package_dir / "models" / f"{name_snake}.py"
    
    if not model_path.exists():
        print_error(f"Model {name_snake}.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {model_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(model_path)
        print_success(f"Removed model: {model_path}")
    except Exception as e:
        print_error(f"Failed to remove {model_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="route")
def remove_route(
    name: str = typer.Argument(..., help="Name of the router to remove"),
):
    """Remove a router from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if router file exists in any version subdirectory
    router_found = False
    routers_dir = package_dir / "routers"
    
    if routers_dir.exists() and routers_dir.is_dir():
        for version_dir in routers_dir.iterdir():
            if version_dir.is_dir() and version_dir.name.startswith('v'):
                # Check both public and private directories
                for access_type in ['public', 'private']:
                    router_path = version_dir / access_type / f"{name_snake}.py"
                    if router_path.exists():
                        router_found = True
                        
                        # Confirm deletion
                        if not Confirm.ask(f"Are you sure you want to remove {router_path}?", default=False):
                            print_warning("Operation cancelled.")
                            continue
                        
                        # Remove the file
                        try:
                            os.remove(router_path)
                            print_success(f"Removed router: {router_path}")
                            
                            # Update the version's __init__.py
                            version_init_path = version_dir / "__init__.py"
                            if version_init_path.exists():
                                with open(version_init_path, "r") as f:
                                    lines = f.readlines()
                                
                                # Filter out import and include lines for this router
                                import_line = f"from .{access_type}.{name_snake} import router as {name_snake}_router"
                                include_line = f"router.include_router({name_snake}_router)"
                                
                                filtered_lines = [line for line in lines 
                                                if import_line not in line and include_line not in line]
                                
                                with open(version_init_path, "w") as f:
                                    f.writelines(filtered_lines)
                                
                                print_info(f"Updated {version_init_path}")
                        except Exception as e:
                            print_error(f"Failed to remove {router_path}: {str(e)}")
    
    # Check root routers directory (old structure)
    if not router_found:
        router_path = package_dir / "routers" / f"{name_snake}.py"
        if router_path.exists():
            router_found = True
            
            # Confirm deletion
            if not Confirm.ask(f"Are you sure you want to remove {router_path}?", default=False):
                print_warning("Operation cancelled.")
                raise typer.Exit(0)
            
            # Remove the file
            try:
                os.remove(router_path)
                print_success(f"Removed router: {router_path}")
            except Exception as e:
                print_error(f"Failed to remove {router_path}: {str(e)}")
                raise typer.Exit(1)
    
    if not router_found:
        print_error(f"Router for {name_snake} not found.")
        raise typer.Exit(1)


@app.command(name="utils")
def remove_utils(
    name: str = typer.Argument(..., help="Name of the utils file to remove"),
):
    """Remove a utils file from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if utils file exists
    utils_path = package_dir / "utils" / f"{name_snake}.py"
    
    if not utils_path.exists():
        print_error(f"Utils file {name_snake}.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {utils_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(utils_path)
        print_success(f"Removed utils file: {utils_path}")
    except Exception as e:
        print_error(f"Failed to remove {utils_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="schema")
def remove_schema(
    name: str = typer.Argument(..., help="Name of the schema to remove"),
):
    """Remove a schema from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if schema file exists
    schema_path = package_dir / "schemas" / f"{name_snake}.py"
    
    if not schema_path.exists():
        print_error(f"Schema {name_snake}.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {schema_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(schema_path)
        print_success(f"Removed schema: {schema_path}")
    except Exception as e:
        print_error(f"Failed to remove {schema_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="exception")
def remove_exception(
    name: str = typer.Argument(..., help="Name of the exception to remove"),
):
    """Remove an exception from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if exception file exists
    exception_path = package_dir / "exceptions" / f"{name_snake}.py"
    
    if not exception_path.exists():
        print_error(f"Exception {name_snake}.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {exception_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(exception_path)
        print_success(f"Removed exception: {exception_path}")
    except Exception as e:
        print_error(f"Failed to remove {exception_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="middleware")
def remove_middleware(
    name: str = typer.Argument(..., help="Name of the middleware to remove"),
):
    """Remove a middleware from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Check if middleware file exists
    middleware_path = package_dir / "middleware" / f"{name_snake}.py"
    
    if not middleware_path.exists():
        print_error(f"Middleware {name_snake}.py does not exist.")
        raise typer.Exit(1)
    
    # Confirm deletion
    if not Confirm.ask(f"Are you sure you want to remove {middleware_path}?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the file
    try:
        os.remove(middleware_path)
        print_success(f"Removed middleware: {middleware_path}")
    except Exception as e:
        print_error(f"Failed to remove {middleware_path}: {str(e)}")
        raise typer.Exit(1)


@app.command(name="module")
def remove_module(
    name: str = typer.Argument(..., help="Name of the module to remove"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Remove without confirmation"
    ),
):
    """Remove a complete module (service, router, model, schema, etc.) from the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Collect all potential files
    files_to_remove = [
        package_dir / "services" / f"{name_snake}_service.py",
        package_dir / "jobs" / f"{name_snake}_job.py",
        package_dir / "constants" / f"{name_snake}.py",
        package_dir / "utils" / f"{name_snake}.py",
        package_dir / "schemas" / f"{name_snake}.py",
        package_dir / "models" / f"{name_snake}.py",
        package_dir / "exceptions" / f"{name_snake}.py",
        package_dir / "middleware" / f"{name_snake}.py",
    ]
    
    # Also search for router files in all version/access_type directories
    routers_dir = package_dir / "routers"
    if routers_dir.exists() and routers_dir.is_dir():
        for version_dir in routers_dir.iterdir():
            if version_dir.is_dir() and version_dir.name.startswith('v'):
                for access_type in ['public', 'private']:
                    access_dir = version_dir / access_type
                    if access_dir.exists() and access_dir.is_dir():
                        router_path = access_dir / f"{name_snake}.py"
                        if router_path.exists():
                            files_to_remove.append(router_path)
    
    # Filter to existing files
    existing_files = [f for f in files_to_remove if f.exists()]
    
    if not existing_files:
        print_error(f"No files found for module {name_snake}.")
        raise typer.Exit(1)
    
    # Show files to be removed
    print_info(f"The following files will be removed:")
    for file in existing_files:
        print_info(f" - {file}")
    
    # Confirm deletion
    if not force and not Confirm.ask("Are you sure you want to remove these files?", default=False):
        print_warning("Operation cancelled.")
        raise typer.Exit(0)
    
    # Remove the files
    with spinner("Removing module files"):
        for file in existing_files:
            try:
                os.remove(file)
                
                # If it's a router, update the version's __init__.py
                if "routers" in str(file):
                    parts = file.parts
                    version_index = parts.index("routers") + 1
                    access_index = version_index + 1
                    
                    if version_index < len(parts) and access_index < len(parts):
                        version = parts[version_index]
                        access_type = parts[access_index]
                        router_name = file.stem
                        
                        version_init_path = package_dir / "routers" / version / "__init__.py"
                        if version_init_path.exists():
                            with open(version_init_path, "r") as f:
                                lines = f.readlines()
                            
                            # Filter out import and include lines for this router
                            import_line = f"from .{access_type}.{router_name} import router as {router_name}_router"
                            include_line = f"router.include_router({router_name}_router)"
                            
                            filtered_lines = [line for line in lines 
                                            if import_line not in line and include_line not in line]
                            
                            with open(version_init_path, "w") as f:
                                f.writelines(filtered_lines)
            except Exception as e:
                print_error(f"Failed to remove {file}: {str(e)}")
    
    print_success(f"Module {name_snake} removed successfully!")