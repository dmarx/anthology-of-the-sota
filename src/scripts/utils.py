from pathlib import Path
import tomli
import os
import subprocess
from loguru import logger

def get_project_root() -> Path:
    """
    Get the project root directory by looking for pyproject.toml
    Returns the absolute path to the project root
    """
    current = Path.cwd().absolute()
    
    # Look for pyproject.toml in current and parent directories
    while current != current.parent:
        if (current / 'pyproject.toml').exists():
            return current
        current = current.parent
    
    # If we couldn't find it, use the current working directory
    # and log a warning
    logger.warning("Could not find pyproject.toml in parent directories")
    return Path.cwd().absolute()

def load_config(config_path: str) -> dict:
    """
    Load configuration from a TOML file
    
    Args:
        config_path (str): Path to the TOML configuration file relative to project root
        
    Returns:
        dict: Parsed configuration data
    """
    try:
        full_path = get_project_root() / config_path
        logger.debug(f"Attempting to load config from: {full_path}")
        with open(full_path, "rb") as f:
            return tomli.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {full_path}")
        raise

def commit_and_push(file_to_commit):
    """Commit and push changes for a specific file"""
    try:
        # Configure Git for GitHub Actions
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"], check=True)
        
        # Check if there are any changes to commit
        status = subprocess.run(["git", "status", "--porcelain", file_to_commit], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            logger.info(f"No changes to commit for {file_to_commit}")
            return
        
        subprocess.run(["git", "add", file_to_commit], check=True)
        subprocess.run(["git", "commit", "-m", f"Update {file_to_commit}"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        logger.success(f"Changes to {file_to_commit} committed and pushed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during git operations: {e}")
        if "nothing to commit" in str(e):
            logger.info("No changes to commit. Continuing execution")
        else:
            logger.warning("Exiting early due to Git error")
            raise
