# src/scripts/registry/cli.py
"""Command-line interface for registry operations."""

import fire
from pathlib import Path
from loguru import logger
from typing import Optional
from . import (
    build_registry_from_yaml,
    load_research_yaml, 
    save_registry,
    registry_to_markdown
)
#from ..utils import commit_and_push
from llamero.utils import commit_and_push_to_branch #commit_and_push

def build(
    input_path: str | Path = "data/research.yaml",
    output_dir: str | Path = "data",
    push: bool = True,
    branch: Optional[str] = "HEAD"
) -> None:
    """Build registry from research YAML and generate outputs.
    
    Args:
        input_path: Path to research YAML file
        output_dir: Directory to save outputs (default: data directory)
        push: Whether to commit and push changes
        branch: Optional branch name to commit to (default: current branch)
    """
    logger.info(f"Building registry from {input_path}")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate registry
    yaml_data = load_research_yaml(input_path)
    registry = build_registry_from_yaml(yaml_data)
    
    # Save outputs
    registry_yaml = output_dir / "registry.yaml"
    registry_md = output_dir / "REGISTRY.md"
    
    save_registry(registry, registry_yaml)
    registry_to_markdown(registry, registry_md)
    logger.info(f"Registry outputs saved to {output_dir}")

    rdme= output_dir.parent / "docs/readme/sections/registry.md.j2"
    registry_to_markdown(registry, rdme)
    
    
    if push:
        logger.info("Committing changes")
        #commit_and_push([registry_yaml, registry_md, rdme])
        commit_and_push_to_branch(
            message="Update ML training registry",
            branch=branch or "main",
            paths=[registry_yaml, registry_md, rdme],
            force=False
        )


def cli():
    """CLI entry point."""
    return fire.Fire({
        'build': build
    })


if __name__ == "__main__":
    cli()
