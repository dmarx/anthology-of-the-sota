# tests/registry/test_io.py
"""Tests for registry I/O operations."""

import pytest
import yaml
from pathlib import Path

from scripts.registry.io import (
    load_research_yaml,
    save_registry,
    load_registry,
    registry_to_markdown,
    RegistryDataError
)
from scripts.registry.recommendations import RecommendationRegistry

@pytest.fixture
def sample_research_yaml(tmp_path):
    """Create a sample research YAML file."""
    yaml_path = tmp_path / "research.yaml"
    data = {
        "2020": [{
            "title": "Test Paper",
            "year": "2020",
            "first_author": "Smith",
            "arxiv_id": "2020.12345",
            "topics": ["optimization"],
            "sota": ["Test recommendation"]
        }]
    }
    
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(data, f)
    
    return yaml_path

@pytest.fixture
def sample_registry():
    """Create a sample registry with some recommendations."""
    registry = RecommendationRegistry()
    registry.add_recommendation(
        topic="optimization",
        recommendation="Test recommendation",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020,
        arxiv_id="2020.12345"
    )
    return registry

def test_load_research_yaml(sample_research_yaml):
    """Test loading research data from YAML."""
    data = load_research_yaml(sample_research_yaml)
    assert "2020" in data
    assert len(data["2020"]) == 1
    assert data["2020"][0]["title"] == "Test Paper"

def test_load_research_yaml_invalid_year(tmp_path):
    """Test loading YAML with invalid year."""
    yaml_path = tmp_path / "invalid.yaml"
    data = {"3000": [{"title": "Future Paper", "first_author": "Smith"}]}
    
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(data, f)
    
    with pytest.raises(RegistryDataError):
        load_research_yaml(yaml_path)

def test_load_research_yaml_missing_fields(tmp_path):
    """Test loading YAML with missing required fields."""
    yaml_path = tmp_path / "invalid.yaml"
    data = {"2020": [{"title": "Incomplete Paper"}]}  # Missing first_author
    
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(data, f)
    
    with pytest.raises(RegistryDataError):
        load_research_yaml(yaml_path)

def test_save_and_load_registry(sample_registry, tmp_path):
    """Test saving and loading registry."""
    registry_path = tmp_path / "registry.yaml"
    
    # Save registry
    save_registry(sample_registry, registry_path)
    assert registry_path.exists()
    
    # Load registry
    data = load_registry(registry_path)
    assert 'metadata' in data
    assert 'recommendations' in data
    assert 'topics' in data

def test_load_registry_invalid_format(tmp_path):
    """Test loading invalid registry format."""
    registry_path = tmp_path / "invalid.yaml"
    
    with open(registry_path, 'w') as f:
        yaml.safe_dump({"invalid": "format"}, f)
    
    with pytest.raises(RegistryDataError):
        load_registry(registry_path)

def test_registry_to_markdown(sample_registry, tmp_path):
    """Test markdown export."""
    markdown_path = tmp_path / "registry.md"
    registry_to_markdown(sample_registry, markdown_path)
    
    assert markdown_path.exists()
    content = markdown_path.read_text()
    
    # Check basic structure
    assert "# ML Training Recommendations Registry" in content
    assert "## Standard Recommendations" in content
    assert "### optimization" in content
    assert "Test recommendation" in content
    assert "## Statistics" in content

def test_nonexistent_file():
    """Test handling of nonexistent files."""
    with pytest.raises(FileNotFoundError):
        load_research_yaml("nonexistent.yaml")
    
    with pytest.raises(FileNotFoundError):
        load_registry("nonexistent.yaml")

def test_invalid_yaml(tmp_path):
    """Test handling of invalid YAML."""
    invalid_yaml = tmp_path / "invalid.yaml"
    invalid_yaml.write_text("invalid: yaml: content:")
    
    with pytest.raises(yaml.YAMLError):
        load_research_yaml(invalid_yaml)
