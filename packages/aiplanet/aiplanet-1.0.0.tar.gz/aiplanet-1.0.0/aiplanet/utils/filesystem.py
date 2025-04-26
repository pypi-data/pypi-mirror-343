"""
Filesystem utilities for the aiplanet CLI
"""
import os
import shutil
from pathlib import Path
from typing import Optional, Union

from aiplanet.utils.console import print_error, print_warning


def create_directory(path: Union[str, Path]) -> None:
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: Path of the directory to create
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)


def create_file(path: Union[str, Path], content: str) -> None:
    """
    Create a file with the given content.
    
    Args:
        path: Path of the file to create
        content: Content to write to the file
    """
    path = Path(path)
    
    # Create parent directories if they don't exist
    if not path.parent.exists():
        create_directory(path.parent)
    
    # Write content to file
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def ensure_directory_exists(path: Union[str, Path]) -> None:
    """
    Ensure that a directory exists, create it if it doesn't.
    
    Args:
        path: Path of the directory to check/create
    """
    path = Path(path)
    if not path.exists():
        create_directory(path)
        # Create __init__.py to make it a proper Python package
        create_file(path / "__init__.py", "")


def remove_file(path: Union[str, Path]) -> bool:
    """
    Remove a file if it exists.
    
    Args:
        path: Path of the file to remove
        
    Returns:
        True if the file was removed, False otherwise
    """
    path = Path(path)
    if path.exists() and path.is_file():
        try:
            path.unlink()
            return True
        except Exception as e:
            print_error(f"Failed to remove {path}: {str(e)}")
            return False
    else:
        print_warning(f"{path} does not exist or is not a file")
        return False


def remove_directory(path: Union[str, Path], recursive: bool = False) -> bool:
    """
    Remove a directory if it exists.
    
    Args:
        path: Path of the directory to remove
        recursive: Whether to remove recursively
        
    Returns:
        True if the directory was removed, False otherwise
    """
    path = Path(path)
    if path.exists() and path.is_dir():
        try:
            if recursive:
                shutil.rmtree(path)
            else:
                path.rmdir()
            return True
        except Exception as e:
            print_error(f"Failed to remove {path}: {str(e)}")
            return False
    else:
        print_warning(f"{path} does not exist or is not a directory")
        return False


def copy_file(src: Union[str, Path], dst: Union[str, Path]) -> bool:
    """
    Copy a file.
    
    Args:
        src: Source file path
        dst: Destination file path
        
    Returns:
        True if the file was copied, False otherwise
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists() or not src.is_file():
        print_error(f"{src} does not exist or is not a file")
        return False
    
    try:
        # Create parent directories if they don't exist
        if not dst.parent.exists():
            create_directory(dst.parent)
        
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print_error(f"Failed to copy {src} to {dst}: {str(e)}")
        return False


def copy_directory(src: Union[str, Path], dst: Union[str, Path]) -> bool:
    """
    Copy a directory.
    
    Args:
        src: Source directory path
        dst: Destination directory path
        
    Returns:
        True if the directory was copied, False otherwise
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists() or not src.is_dir():
        print_error(f"{src} does not exist or is not a directory")
        return False
    
    try:
        if dst.exists():
            # Remove destination directory if it exists
            shutil.rmtree(dst)
        
        shutil.copytree(src, dst)
        return True
    except Exception as e:
        print_error(f"Failed to copy {src} to {dst}: {str(e)}")
        return False


def get_file_content(path: Union[str, Path]) -> Optional[str]:
    """
    Get the content of a file.
    
    Args:
        path: Path of the file to read
        
    Returns:
        File content, None if the file doesn't exist
    """
    path = Path(path)
    if not path.exists() or not path.is_file():
        print_error(f"{path} does not exist or is not a file")
        return None
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print_error(f"Failed to read {path}: {str(e)}")
        return None


def is_python_package(path: Union[str, Path]) -> bool:
    """
    Check if a directory is a Python package.
    
    Args:
        path: Path of the directory to check
        
    Returns:
        True if the directory is a Python package, False otherwise
    """
    path = Path(path)
    return path.is_dir() and (path / "__init__.py").exists()