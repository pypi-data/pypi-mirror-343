"""
Run command - Runs the FastAPI application
"""
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer

from aiplanet.utils.console import print_error, print_info, print_success

app = typer.Typer(help="Run the FastAPI application")


@app.command(name="dev")
def run_dev(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="Enable auto-reload"),
    log_level: str = typer.Option("info", "--log-level", "-l", help="Log level"),
    app_module: str = typer.Option("main:app", "--app", "-a", help="Application module"),
    env_file: Optional[str] = typer.Option(None, "--env-file", "-e", help="Environment file"),
):
    """
    Run the FastAPI application in development mode.
    """
    # Check if main.py exists
    main_path = Path("main.py")
    if not main_path.exists() and "main" in app_module:
        print_error(f"Application file {main_path} does not exist.")
        raise typer.Exit(1)
    
    # Prepare uvicorn command
    command = [
        "uvicorn",
        app_module,
        "--host", host,
        "--port", str(port),
        "--log-level", log_level,
    ]
    
    if reload:
        command.append("--reload")
    
    if env_file:
        command.extend(["--env-file", env_file])
    
    # Print command
    command_str = " ".join(command)
    print_info(f"Starting development server: {command_str}")
    
    try:
        # Run uvicorn
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )
        
        # Handle keyboard interrupt
        def signal_handler(sig, frame):
            print_info("\nStopping development server...")
            process.terminate()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Stream output
        for line in iter(process.stdout.readline, ""):
            print(line, end="")
        
        process.wait()
        
        if process.returncode != 0:
            print_error(f"Development server exited with code {process.returncode}")
            raise typer.Exit(process.returncode)
        
    except FileNotFoundError:
        print_error("Failed to run development server. Is uvicorn installed?")
        print_info("You can install it with: pip install uvicorn")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error running development server: {str(e)}")
        raise typer.Exit(1)


@app.command(name="prod")
def run_prod(
    workers: int = typer.Option(2, "--workers", "-w", help="Number of worker processes"),
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
    log_level: str = typer.Option("info", "--log-level", "-l", help="Log level"),
    app_module: str = typer.Option("main:app", "--app", "-a", help="Application module"),
    env_file: Optional[str] = typer.Option(None, "--env-file", "-e", help="Environment file"),
):
    """
    Run the FastAPI application in production mode using Gunicorn.
    """
    # Check if main.py exists
    main_path = Path("main.py")
    if not main_path.exists() and "main" in app_module:
        print_error(f"Application file {main_path} does not exist.")
        raise typer.Exit(1)
    
    # Prepare gunicorn command
    command = [
        "gunicorn",
        app_module,
        "--workers", str(workers),
        "--worker-class", "uvicorn.workers.UvicornWorker",
        "--bind", f"{host}:{port}",
        "--log-level", log_level,
    ]
    
    if env_file:
        os.environ["ENV_FILE"] = env_file
    
    # Print command
    command_str = " ".join(command)
    print_info(f"Starting production server: {command_str}")
    
    try:
        # Run gunicorn
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )
        
        # Handle keyboard interrupt
        def signal_handler(sig, frame):
            print_info("\nStopping production server...")
            process.terminate()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Stream output
        for line in iter(process.stdout.readline, ""):
            print(line, end="")
        
        process.wait()
        
        if process.returncode != 0:
            print_error(f"Production server exited with code {process.returncode}")
            raise typer.Exit(process.returncode)
        
    except FileNotFoundError:
        print_error("Failed to run production server. Is gunicorn installed?")
        print_info("You can install it with: pip install gunicorn")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error running production server: {str(e)}")
        raise typer.Exit(1)


@app.command(name="docker")
def run_docker(
    build: bool = typer.Option(True, "--build/--no-build", help="Build images before starting"),
    detached: bool = typer.Option(False, "--detach", "-d", help="Run in detached mode"),
):
    """
    Run the FastAPI application using Docker Compose.
    """
    # Check if docker-compose.yml exists
    docker_compose_path = Path("docker-compose.yml")
    if not docker_compose_path.exists():
        print_error("Docker Compose file does not exist.")
        print_info("You can create it with: aiplanet build project --docker")
        raise typer.Exit(1)
    
    # Prepare docker-compose command
    command = ["docker-compose", "up"]
    
    if build:
        command.append("--build")
    
    if detached:
        command.append("-d")
    
    # Print command
    command_str = " ".join(command)
    print_info(f"Starting Docker: {command_str}")
    
    try:
        # Run docker-compose
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )
        
        # Handle keyboard interrupt
        def signal_handler(sig, frame):
            if not detached:
                print_info("\nStopping Docker...")
                process.terminate()
                sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Stream output if not detached
        if not detached:
            for line in iter(process.stdout.readline, ""):
                print(line, end="")
            
            process.wait()
            
            if process.returncode != 0:
                print_error(f"Docker exited with code {process.returncode}")
                raise typer.Exit(process.returncode)
        else:
            print_success("Docker started in detached mode.")
            print_info("You can stop it with: docker-compose down")
        
    except FileNotFoundError:
        print_error("Failed to run Docker. Is docker-compose installed?")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error running Docker: {str(e)}")
        raise typer.Exit(1)