from pathlib import Path
import pytest
from scripts.readme_generator import generate_readme, get_section_templates
from scripts.utils import get_project_root, load_config

def test_load_config(mock_repo):
    """Test configuration loading"""
    config = load_config(str(mock_repo / "pyproject.toml"))
    assert config["project"]["name"] == "test-project"
    assert config["project"]["version"] == "0.1.0"

def test_project_root(mock_repo, monkeypatch):
    """Test project root detection"""
    monkeypatch.chdir(mock_repo)
    root = get_project_root()
    assert root.samefile(mock_repo)
