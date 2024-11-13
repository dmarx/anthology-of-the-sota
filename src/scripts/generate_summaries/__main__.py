import subprocess
from pathlib import Path
from typing import Optional

def commit_and_push(
    message: str,
    branch: str,
    paths: list[str | Path],
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


"""CLI entry point for summary generator."""
import fire
from loguru import logger
from pathlib import Path
from . import generator
#from readme_generator.utils import commit_and_push
from . import special_summaries


def generate(root_dir: str = ".", push: bool = True) -> list[Path]:
    """Generate directory summaries and special summaries.
    
    Args:
        root_dir: Root directory to generate summaries for
        push: Whether to commit and push changes
        
    Returns:
        List of paths to generated summary files
    """
    logger.info(f"Generating summaries for {root_dir}")
    
    # Generate regular directory summaries
    gen = generator.SummaryGenerator(root_dir)
    summary_files = gen.generate_all_summaries()
    
    # Generate special summaries
    special_files = special_summaries.generate_special_summaries(root_dir)
    all_files = summary_files + special_files
    
    if push:
        logger.info("Committing and pushing changes")
        commit_and_push(
            message="Update directory summaries and special summaries",
            branch="summaries",
            paths=all_files,
            base_branch="main",
            force=True  # Use force push for generated content
        )
    
    return all_files

def main():
    """CLI entry point."""
    fire.Fire(generate)

if __name__ == "__main__":
    main()
