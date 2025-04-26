"""
Add command - Adds components to the project
"""
import os
from pathlib import Path
from typing import Optional

import typer
import questionary
from rich.prompt import Prompt

from aiplanet.utils.console import print_error, print_info, print_success, print_warning
from aiplanet.utils.filesystem import create_file, ensure_directory_exists
from aiplanet.utils.templates import render_template

app = typer.Typer(help="Add components to the project")

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
def add_service(
    name: str = typer.Argument(..., help="Name of the service"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the service"
    ),
):
    """Add a service to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Service for {name_snake.replace('_', ' ')} operations"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure services directory exists
    services_dir = package_dir / "services"
    ensure_directory_exists(services_dir)
    
    # Create the service file
    service_path = services_dir / f"{name_snake}_service.py"
    
    # Check if file already exists
    if service_path.exists():
        print_warning(f"Service {name_snake}_service.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the service template
    content = render_template("service.py.jinja", {
        "name": name_snake,
        "class_name": "".join(word.capitalize() for word in name_snake.split("_")) + "Service",
        "description": description,
        "package_name": package_dir.name
    })
    
    # Create the file
    create_file(service_path, content)
    print_success(f"Created service: {service_path}")


@app.command(name="const")
def add_const(
    name: str = typer.Argument(..., help="Name of the constants file"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the constants file"
    ),
):
    """Add constants file to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Constants related to {name_snake.replace('_', ' ')}"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure constants directory exists
    const_dir = package_dir / "constants"
    ensure_directory_exists(const_dir)
    
    # Create the constants file
    const_path = const_dir / f"{name_snake}.py"
    
    # Check if file already exists
    if const_path.exists():
        print_warning(f"Constants file {name_snake}.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the constants template
    content = render_template("constant.py.jinja", {
        "name": name_snake,
        "description": description,
    })
    
    # Create the file
    create_file(const_path, content)
    print_success(f"Created constants file: {const_path}")


@app.command(name="middleware")
def add_middleware(
    name: str = typer.Argument(..., help="Name of the middleware"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the middleware"
    ),
):
    """Add a middleware to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Middleware for {name_snake.replace('_', ' ')}"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure middleware directory exists
    middleware_dir = package_dir / "middleware"
    ensure_directory_exists(middleware_dir)
    
    # Create the middleware file
    middleware_path = middleware_dir / f"{name_snake}.py"
    
    # Check if file already exists
    if middleware_path.exists():
        print_warning(f"Middleware {name_snake}.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the middleware template
    content = render_template("middleware.py.jinja", {
        "name": name_snake,
        "description": description,
        "class_name": "".join(word.capitalize() for word in name_snake.split("_")),
    })
    
    # Create the file
    create_file(middleware_path, content)
    print_success(f"Created middleware: {middleware_path}")

@app.command(name="job")
def add_job(
    name: str = typer.Argument(..., help="Name of the job"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the job"
    ),
):
    """Add a job to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Job for {name_snake.replace('_', ' ')} operations"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure jobs directory exists
    jobs_dir = package_dir / "jobs"
    ensure_directory_exists(jobs_dir)
    
    # Create the job file
    job_path = jobs_dir / f"{name_snake}_job.py"
    
    # Check if file already exists
    if job_path.exists():
        print_warning(f"Job {name_snake}_job.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the job template
    content = render_template("job.py.jinja", {
        "name": name_snake,
        "class_name": "".join(word.capitalize() for word in name_snake.split("_")) + "Job",
        "description": description,
        "package_name": package_dir.name
    })
    
    # Create the file
    create_file(job_path, content)
    print_success(f"Created job: {job_path}")


@app.command(name="model")
def add_model(
    name: str = typer.Argument(..., help="Name of the model"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the model"
    ),
    table_name: Optional[str] = typer.Option(
        None, "--table", "-t", help="Database table name (defaults to pluralized name)"
    ),
):
    """Add a model to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"{name_snake.replace('_', ' ').title()} model"
    
    if table_name is None:
        # Simple pluralization (for English only)
        table_name = f"{name_snake}s"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure models directory exists
    models_dir = package_dir / "models"
    ensure_directory_exists(models_dir)
    
    # Create the model file
    model_path = models_dir / f"{name_snake}.py"
    
    # Check if file already exists
    if model_path.exists():
        print_warning(f"Model {name_snake}.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the model template
    content = render_template("model.py.jinja", {
        "name": name_snake,
        "class_name": "".join(word.capitalize() for word in name_snake.split("_")),
        "description": description,
        "table_name": table_name,
        "package_name": package_dir.name
    })
    
    # Create the file
    create_file(model_path, content)
    print_success(f"Created model: {model_path}")


@app.command(name="route")
def add_route(
    name: str = typer.Argument(..., help="Name of the router"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the router"
    ),
    prefix: Optional[str] = typer.Option(
        None, "--prefix", "-p", help="API prefix (defaults to pluralized name)"
    ),
    tag: Optional[str] = typer.Option(
        None, "--tag", "-t", help="Swagger tag (defaults to pluralized name)"
    ),
    version: Optional[str] = typer.Option(
        None, "--version", "-v", help="API version (e.g., v1, v2)"
    ),
):
    """Add a router to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Router for {name_snake.replace('_', ' ')} endpoints"
    
    if prefix is None:
        # Simple pluralization (for English only)
        prefix = f"/{name_snake}s"
    
    if tag is None:
        # Simple pluralization (for English only)
        tag = f"{name_snake}s"
    
    # Ask for version if not provided
    if version is None:
        version = questionary.text("API version (e.g., v1, v2):", default="v1").ask()
    
    # Ask if it's a private or public endpoint
    is_private = questionary.confirm("Is this a private endpoint? (requires authentication)", default=False).ask()
    access_type = "private" if is_private else "public"
    
    # Get the package directory
    package_dir = get_package_dir()
    package_name = package_dir.name
    
    # Determine the directory structure
    api_dir = package_dir / "routers"
    ensure_directory_exists(api_dir)
    
    version_dir = api_dir / version
    ensure_directory_exists(version_dir)
    
    # Create private/public directory
    access_dir = version_dir / access_type
    ensure_directory_exists(access_dir)
    
    # Create __init__.py files to make directories proper packages
    for dir_path in [api_dir, version_dir, access_dir]:
        init_path = dir_path / "__init__.py"
        if not init_path.exists():
            create_file(init_path, '"""API package"""\n')
    
    # Set the router path in the appropriate directory
    router_path = access_dir / f"{name_snake}.py"
    
    # Check if file already exists
    if router_path.exists():
        print_warning(f"Router {router_path} already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            print_info("Skipping router creation.")
            return
    
    # Render the router template
    content = render_template("router.py.jinja", {
        "name": name_snake,
        "description": description,
        "prefix": prefix,
        "tag": tag,
        "class_name": "".join(word.capitalize() for word in name_snake.split("_")),
        "is_private": is_private,
        "version": version,
        "package_name": package_name
    })
    
    # Create the file
    create_file(router_path, content)
    print_success(f"Created router: {router_path}")
    
    # Update the access_type (private/public) __init__.py to import the router
    access_init_path = access_dir / "__init__.py"
    
    # Create content for the access_type's __init__.py if it doesn't exist or is empty
    access_init_content = f'''"""API package"""
    from fastapi import APIRouter

    router = APIRouter(
        prefix="/{access_type}",
        tags=["{access_type}"],
    )

    # Include routers
    '''
    if not access_init_path.exists() or access_init_path.read_text().strip() == '"""API package"""' or not access_init_path.read_text().strip():
        create_file(access_init_path, access_init_content)
    
    # Import line for the new router in the access_type's __init__.py (using absolute imports)
    abs_import_line = f"from {package_name}.routers.{version}.{access_type}.{name_snake} import router as {name_snake}_router"
    include_line = f"router.include_router({name_snake}_router)"
    
    # Read current content of access_type's __init__.py
    with open(access_init_path, "r") as f:
        current_content = f.read()
    
    # Check if router is already imported (either relative or absolute)
    router_already_imported = False
    router_already_included = False
    
    for line in current_content.splitlines():
        if f"import router as {name_snake}_router" in line:
            router_already_imported = True
        if f"router.include_router({name_snake}_router)" in line:
            router_already_included = True
    
    # Add the import and include statements if they don't exist
    lines = current_content.splitlines()
    
    # Find the last import to group imports together at the top
    last_import_index = -1
    first_non_import_index = -1
    router_def_index = -1
    include_comment_index = -1
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if (line_stripped.startswith("from ") or line_stripped.startswith("import ")) and not line_stripped.startswith("# import"):
            last_import_index = i
        elif first_non_import_index == -1 and i > 0 and not line_stripped.startswith("#") and not line_stripped == "" and not '"""' in line_stripped:
            first_non_import_index = i
        
        if line_stripped.startswith("router = APIRouter"):
            router_def_index = i
        
        if "# Include routers" in line:
            include_comment_index = i
    
    # If we found imports, add after the last import
    if last_import_index != -1:
        import_index = last_import_index + 1
    # If no imports but we found where non-import code starts, insert before that
    elif first_non_import_index != -1:
        import_index = first_non_import_index
    # Otherwise add after docstring
    else:
        for i, line in enumerate(lines):
            if '"""' in line and i > 0:
                import_index = i + 1
                break
        # Last resort - add after first line
        if import_index == -1:
            import_index = 1 if len(lines) > 0 else 0
    
    # Find position to add router inclusion
    # First priority: after existing include comment
    if include_comment_index != -1:
        include_index = include_comment_index + 1
    # Second priority: add after router definition and add comment
    elif router_def_index != -1:
        # Find end of router definition (possibly multi-line)
        i = router_def_index
        while i < len(lines) and ")" not in lines[i]:
            i += 1
        include_index = i + 1 if i < len(lines) else router_def_index + 1
        
        # Insert the comment if it doesn't exist
        if "# Include routers" not in "\n".join(lines):
            lines.insert(include_index, "# Include routers")
            include_index += 1
    # Last resort - add at end with comment
    else:
        include_index = len(lines)
        if "# Include routers" not in "\n".join(lines):
            lines.append("")
            lines.append("# Include routers")
            include_index += 2
    
    # Add import if not already present
    if not router_already_imported:
        lines.insert(import_index, abs_import_line)
        # If we insert before include_index, we need to adjust the index
        if import_index <= include_index:
            include_index += 1
    
    # Add include if not already present
    if not router_already_included:
        lines.insert(include_index, include_line)
    
    # Write the updated content to access_type's __init__.py
    with open(access_init_path, "w") as f:
        f.write("\n".join(lines))
    
    # Update the version's __init__.py to import the access_type router
    version_init_path = version_dir / "__init__.py"
    
    # Create content for the version's __init__.py
    version_init_content = f'''"""API router for {version}"""
    from fastapi import APIRouter

    router = APIRouter(
        tags=["{version}"],
    )

    # Include routers
    '''
    # If the file doesn't exist or is just the default package docstring or empty
    if not version_init_path.exists() or version_init_path.read_text().strip() == '"""API package"""' or not version_init_path.read_text().strip():
        create_file(version_init_path, version_init_content)
    
    # Import line for the access_type router in the version's __init__.py
    abs_import_line = f"from {package_name}.routers.{version}.{access_type} import router as {access_type}_router"
    include_line = f"router.include_router({access_type}_router)"
    
    # Read current content of version's __init__.py
    with open(version_init_path, "r") as f:
        current_content = f.read()
    
    # Check if router is already imported (either relative or absolute)
    router_already_imported = False
    router_already_included = False
    
    for line in current_content.splitlines():
        if f"import router as {access_type}_router" in line:
            router_already_imported = True
        if f"router.include_router({access_type}_router)" in line:
            router_already_included = True
    
    # Add the import and include statements if they don't exist
    lines = current_content.splitlines()
    
    # Find the last import to group imports together at the top
    last_import_index = -1
    first_non_import_index = -1
    router_def_index = -1
    include_comment_index = -1
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if (line_stripped.startswith("from ") or line_stripped.startswith("import ")) and not line_stripped.startswith("# import"):
            last_import_index = i
        elif first_non_import_index == -1 and i > 0 and not line_stripped.startswith("#") and not line_stripped == "" and not '"""' in line_stripped:
            first_non_import_index = i
        
        if line_stripped.startswith("router = APIRouter"):
            router_def_index = i
        
        if "# Include routers" in line:
            include_comment_index = i
    
    # If we found imports, add after the last import
    if last_import_index != -1:
        import_index = last_import_index + 1
    # If no imports but we found where non-import code starts, insert before that
    elif first_non_import_index != -1:
        import_index = first_non_import_index
    # Otherwise add after docstring
    else:
        for i, line in enumerate(lines):
            if '"""' in line and i > 0:
                import_index = i + 1
                break
        # Last resort - add after first line
        if import_index == -1:
            import_index = 1 if len(lines) > 0 else 0
    
    # Find position to add router inclusion
    # First priority: after existing include comment
    if include_comment_index != -1:
        include_index = include_comment_index + 1
    # Second priority: add after router definition and add comment
    elif router_def_index != -1:
        # Find end of router definition (possibly multi-line)
        i = router_def_index
        while i < len(lines) and ")" not in lines[i]:
            i += 1
        include_index = i + 1 if i < len(lines) else router_def_index + 1
        
        # Insert the comment if it doesn't exist
        if "# Include routers" not in "\n".join(lines):
            lines.insert(include_index, "# Include routers")
            include_index += 1
    # Last resort - add at end with comment
    else:
        include_index = len(lines)
        if "# Include routers" not in "\n".join(lines):
            lines.append("")
            lines.append("# Include routers")
            include_index += 2
    
    # Add import if not already present
    if not router_already_imported:
        lines.insert(import_index, abs_import_line)
        # If we insert before include_index, we need to adjust the index
        if import_index <= include_index:
            include_index += 1
    
    # Add include if not already present
    if not router_already_included:
        lines.insert(include_index, include_line)
    
    # Write the updated content to version's __init__.py
    with open(version_init_path, "w") as f:
        f.write("\n".join(lines))
    
    # Update the api/__init__.py to import and register the versioned router
    api_init_path = api_dir / "__init__.py"
    
    # Create content for the api's __init__.py
    api_init_content = f'''"""API package"""

    # Import version routers
    '''
    # If the file doesn't exist or is just the default package docstring or empty
    if not api_init_path.exists() or api_init_path.read_text().strip() == '"""API package"""' or not api_init_path.read_text().strip():
        create_file(api_init_path, api_init_content)
    
    # Import line for the version router
    abs_import_line = f"from {package_name}.routers.{version} import router as {version}_router"
    
    # Read current content
    with open(api_init_path, "r") as f:
        current_content = f.read()
    
    # Check if router is already imported
    router_already_imported = False
    
    for line in current_content.splitlines():
        if f"import router as {version}_router" in line:
            router_already_imported = True
    
    # Add the import statement if it doesn't exist
    if not router_already_imported:
        lines = current_content.splitlines()
        
        # Find the last import to group imports together
        last_import_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("from ") or line.strip().startswith("import "):
                last_import_index = i
        
        # If we found imports, add after the last import
        if last_import_index != -1:
            lines.insert(last_import_index + 1, abs_import_line)
        # Otherwise add under "# Import version routers" comment
        else:
            comment_index = -1
            for i, line in enumerate(lines):
                if "# Import version routers" in line:
                    comment_index = i
            
            # If we found the comment, add right after it
            if comment_index != -1:
                lines.insert(comment_index + 1, abs_import_line)
            # Otherwise add at the end
            else:
                if lines and lines[-1].strip():  # If last line is not empty
                    lines.append("")
                lines.append(abs_import_line)
        
        # Write the updated content
        with open(api_init_path, "w") as f:
            f.write("\n".join(lines))
    
    print_success(f"Updated API registry files")
    print_info(f"To use this router in your application, add this to your main.py:")
    print_info(f"from {package_name}.routers import {version}_router")
    print_info(f"app.include_router({version}_router, prefix='/api/{version}')")


@app.command(name="utils")
def add_utils(
    name: str = typer.Argument(..., help="Name of the utils file"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the utils file"
    ),
):
    """Add a utils file to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Utility functions for {name_snake.replace('_', ' ')}"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure utils directory exists
    utils_dir = package_dir / "utils"
    ensure_directory_exists(utils_dir)
    
    # Create the utils file
    utils_path = utils_dir / f"{name_snake}.py"
    
    # Check if file already exists
    if utils_path.exists():
        print_warning(f"Utils file {name_snake}.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the utils template
    content = render_template("util.py.jinja", {
        "name": name_snake,
        "description": description,
    })
    
    # Create the file
    create_file(utils_path, content)
    print_success(f"Created utils file: {utils_path}")


@app.command(name="schema")
def add_schema(
    name: str = typer.Argument(..., help="Name of the schema"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the schema"
    ),
):
    """Add a schema to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Pydantic schemas for {name_snake.replace('_', ' ')}"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure schemas directory exists
    schemas_dir = package_dir / "schemas"
    ensure_directory_exists(schemas_dir)
    
    # Create the schema file
    schema_path = schemas_dir / f"{name_snake}.py"
    
    # Check if file already exists
    if schema_path.exists():
        print_warning(f"Schema {name_snake}.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the schema template
    content = render_template("schema.py.jinja", {
        "name": name_snake,
        "description": description,
        "class_name": "".join(word.capitalize() for word in name_snake.split("_")),
    })
    
    # Create the file
    create_file(schema_path, content)
    print_success(f"Created schema: {schema_path}")


@app.command(name="exception")
def add_exception(
    name: str = typer.Argument(..., help="Name of the exception"),
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Description of the exception"
    ),
):
    """Add an exception to the project."""
    # Convert name to snake_case if necessary
    name_snake = name.lower().replace("-", "_")
    
    if description is None:
        description = f"Custom exceptions for {name_snake.replace('_', ' ')}"
    
    # Get the package directory
    package_dir = get_package_dir()
    
    # Ensure exceptions directory exists
    exceptions_dir = package_dir / "exceptions"
    ensure_directory_exists(exceptions_dir)
    
    # Create the exception file
    exception_path = exceptions_dir / f"{name_snake}.py"
    
    # Check if file already exists
    if exception_path.exists():
        print_warning(f"Exception {name_snake}.py already exists.")
        overwrite = typer.confirm("Do you want to overwrite it?", default=False)
        if not overwrite:
            raise typer.Exit(1)
    
    # Render the exception template
    content = render_template("exception.py.jinja", {
        "name": name_snake,
        "description": description,
        "class_name": "".join(word.capitalize() for word in name_snake.split("_")),
    })
    
    # Create the file
    create_file(exception_path, content)
    print_success(f"Created exception: {exception_path}")