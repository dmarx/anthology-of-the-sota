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

def commit_and_push(
    paths: list[str | Path],
    message: str,
    branch: str,
    base_branch: Optional[str] = None,
    force: bool = False
) -> None:
    """Commit changes and push to specified branch.
    
    Args:
        message: Commit message
        branch: Branch to push to
        paths: List of paths to commit
        base_branch: Optional base branch to create new branch from
        force: If True, create fresh branch and force push (for generated content)
    """
    # Convert paths to strings
    path_strs = [str(p) for p in paths]
    
    # Set up git config
    subprocess.run(["git", "config", "--local", "user.email", "github-actions[bot]@users.noreply.github.com"])
    subprocess.run(["git", "config", "--local", "user.name", "github-actions[bot]"])
    
    if force:
        # Create fresh branch from base_branch or HEAD
        base = base_branch or "HEAD"
        logger.info(f"Creating fresh branch {branch} from {base}")
        subprocess.run(["git", "checkout", "-B", branch, base])
    else:
        # Normal branch handling
        if base_branch:
            logger.info(f"Creating new branch {branch} from {base_branch}")
            subprocess.run(["git", "checkout", "-b", branch, base_branch])
        else:
            logger.info(f"Switching to branch {branch}")
            subprocess.run(["git", "checkout", "-b", branch])
            subprocess.run(["git", "pull", "origin", branch], capture_output=True)
    
    # Stage and commit changes
    subprocess.run(["git", "add", *path_strs])
    
    # Only commit if there are changes
    result = subprocess.run(
        ["git", "diff", "--staged", "--quiet"],
        capture_output=True
    )
    if result.returncode == 1:  # Changes exist
        logger.info("Committing changes")
        subprocess.run(["git", "commit", "-m", message])
        
        # Push changes
        if force:
            logger.info(f"Force pushing {branch} branch")
            subprocess.run(["git", "push", "-f", "origin", branch])
        else:
            logger.info("Pushing changes")
            subprocess.run(["git", "push", "origin", branch])
    else:
        logger.info("No changes to commit")
