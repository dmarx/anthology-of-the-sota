from pathlib import Path
from typing import List
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from .utils import load_config, get_project_root, commit_and_push

def get_section_templates(template_dir: Path) -> List[str]:
    """Get all section templates in proper order.
    
    Args:
        template_dir: Path to template directory containing sections/
        
    Returns:
        List of template names in desired order
    """
    # Define section order
    section_order = {
        "introduction.md.j2": 0,
        "prerequisites.md.j2": 1,
        "usage.md.j2": 2,
        "development.md.j2": 3,
        "summaries.md.j2": 4,
        "site.md.j2": 5,
        "structure.md.j2": 6,
        "todo.md.j2": 999  # Always last if present
    }
    
    sections_dir = template_dir / "sections"
    templates = []
    
    # Collect all template files
    for file in sections_dir.glob("*.md.j2"):
        # Skip todo if it doesn't exist (it's optional)
        if file.name == "todo.md.j2" and not file.exists():
            continue
        templates.append(file.name)
    
    # Sort by explicit order, then alphabetically for any new sections
    return sorted(
        templates,
        key=lambda x: section_order.get(x, 500)
    )

def generate_readme() -> None:
    """Generate README from templates and commit changes"""
    project_root = get_project_root()
    logger.debug(f"Project root identified as: {project_root}")
    
    logger.info("Loading configurations")
    project_config = load_config("pyproject.toml")
    
    logger.info("Setting up Jinja2 environment")
    template_dir = project_root / 'docs/readme'
    logger.debug(f"Template directory: {template_dir}")
    
    env = Environment(
        loader=FileSystemLoader(template_dir),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Add template utility functions
    env.globals['get_section_templates'] = lambda: get_section_templates(template_dir)
    
    template = env.get_template('base.md.j2')
    
    variables = {
        'project': project_config['project'],
        'readme': project_config['tool']['readme'],
    }
    
    logger.info("Rendering README template")
    output = template.render(**variables)
    
    readme_path = project_root / 'README.llm'
    logger.debug(f"Writing README to: {readme_path}")
    readme_path.write_text(output)
    
    logger.info("Committing changes")
    commit_and_push(readme_path)

if __name__ == "__main__":
    generate_readme()
