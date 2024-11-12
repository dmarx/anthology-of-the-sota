# tests/conftest.py
"""Shared test fixtures."""

import pytest
from pathlib import Path
import yaml
from typing import Dict
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    """Provide a clean temporary directory"""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

@pytest.fixture
def mock_repo(temp_dir):
    """Create a mock repository structure for testing"""
    # Create basic structure
    docs_dir = temp_dir / "docs" / "readme" / "sections"
    src_dir = temp_dir / "src" / "readme_generator"
    
    docs_dir.mkdir(parents=True)
    src_dir.mkdir(parents=True)
    
    # Create mock files
    (docs_dir / "introduction.md.j2").write_text("## Introduction\n{{ test }}")
    (temp_dir / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "0.1.0"

[tool.readme]
test = "Test Value"
    """)
    
    return temp_dir

@pytest.fixture
def sample_research_yaml() -> Dict:
    """Sample research data for testing."""
    return {
        "2020": [{
            "title": "Test Paper 1",
            "first_author": "Smith",
            "arxiv_id": "2020.12345",
            "year": 2020,
            "topics": ["optimization", "training"],
            "sota": [
                "Use gradient clipping with threshold 1.0",
                "Scale learning rate with batch size"
            ],
            "models": ["model1", "model2"]
        }],
        "2021": [{
            "title": "Test Paper 2",
            "first_author": "Jones",
            "arxiv_id": "2021.67890",
            "year": 2021,
            "topics": ["attention"],
            "sota": ["Use flash attention for better memory efficiency"],
            "experimental": True
        }, {
            "title": "Test Paper 3",
            "first_author": "Smith",
            "year": 2021,
            "topics": ["optimization"],
            "sota": ["Old recommendation"],
            "attic": {
                "superseded_by": "2021.99999"
            }
        }]
    }

@pytest.fixture
def sample_yaml_file(tmp_path, sample_research_yaml):
    """Create a sample YAML file for testing."""
    yaml_path = tmp_path / "research.yaml"
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(sample_research_yaml, f)
    return yaml_path

@pytest.fixture
def id_registry(tmp_path):
    """Fixture providing a fresh identifier registry."""
    from scripts.registry.identifiers import MLRIdentifierRegistry
    return MLRIdentifierRegistry(tmp_path / "test_mlr_registry.json")

@pytest.fixture
def registry(id_registry):
    """Fixture providing a fresh recommendation registry."""
    from scripts.registry.recommendations import RecommendationRegistry
    return RecommendationRegistry(id_registry)

@pytest.fixture
def populated_registry(registry, sample_research_yaml):
    """Fixture providing a registry populated with sample data."""
    from scripts.registry.recommendations import build_registry_from_yaml
    return build_registry_from_yaml(sample_research_yaml)
