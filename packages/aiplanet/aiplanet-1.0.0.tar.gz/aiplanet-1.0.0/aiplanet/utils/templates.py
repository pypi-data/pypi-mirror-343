"""
Template rendering utilities for the aiplanet CLI
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml
from jinja2 import Environment, FileSystemLoader, Template, select_autoescape

from aiplanet.utils.console import print_error


def get_template_dir() -> Path:
    """
    Get the template directory path.
    
    Returns:
        Path object representing the template directory
    """
    # Get the directory of this file
    current_dir = Path(__file__).parent.parent
    
    # Templates are in the templates directory
    return current_dir / "templates"


def get_jinja_env(template_dir: Optional[Union[str, Path]] = None) -> Environment:
    """
    Get the Jinja2 environment.
    
    Args:
        template_dir: Path of the template directory
        
    Returns:
        Jinja2 environment
    """
    if template_dir is None:
        template_dir = get_template_dir()
    
    return Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def render_template(template_name: str, context: Dict[str, Any]) -> str:
    """
    Render a template with the given context.
    
    Args:
        template_name: Name of the template file
        context: Dictionary of context variables to pass to the template
        
    Returns:
        The rendered template as a string
    """
    try:
        # Get Jinja2 environment
        env = get_jinja_env()
        
        # Load and render template
        template = env.get_template(template_name)
        return template.render(**context)
    except Exception as e:
        print_error(f"Failed to render template {template_name}: {str(e)}")
        raise


def render_string_template(template_str: str, context: Dict[str, Any]) -> str:
    """
    Render a template string with the given context.
    
    Args:
        template_str: Template string
        context: Dictionary of context variables to pass to the template
        
    Returns:
        The rendered template as a string
    """
    try:
        template = Template(template_str)
        return template.render(**context)
    except Exception as e:
        print_error(f"Failed to render template string: {str(e)}")
        raise


def load_template_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load a template configuration file.
    
    Args:
        config_path: Path of the configuration file
        
    Returns:
        Configuration as a dictionary
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        return config or {}
    except Exception as e:
        print_error(f"Failed to load template configuration {config_path}: {str(e)}")
        return {}