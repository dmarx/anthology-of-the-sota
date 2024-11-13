# tests/registry/test_identifiers.py
"""Tests for MLR identifier generation and management."""

import pytest
from pathlib import Path
from scripts.registry.identifiers import MLRIdentifierRegistry

@pytest.fixture
def temp_registry_file(tmp_path):
    """Provide a temporary registry file path."""
    return tmp_path / "test_registry.json"

@pytest.fixture
def identifier_registry(temp_registry_file):
    """Provide a fresh identifier registry."""
    return MLRIdentifierRegistry(temp_registry_file)

def test_initialization(temp_registry_file):
    """Test registry initialization."""
    registry = MLRIdentifierRegistry(temp_registry_file)
    assert registry.current_ids == {'paper_ids': {}, 'recommendation_ids': {}}
    assert isinstance(registry.author_counters, dict)

def test_paper_id_generation(identifier_registry):
    """Test paper ID generation and consistency."""
    # Test first paper ID generation
    paper_id1 = identifier_registry.get_paper_id("Smith", 2020, "2020.12345")
    assert paper_id1 == "Smith001"
    
    # Test same author, different paper
    paper_id2 = identifier_registry.get_paper_id("Smith", 2020, "2020.99999")
    assert paper_id2 == "Smith002"
    
    # Test different author
    paper_id3 = identifier_registry.get_paper_id("Jones", 2020, "2020.54321")
    assert paper_id3 == "Jones001"
    
    # Test ID consistency
    assert identifier_registry.get_paper_id("Smith", 2020, "2020.12345") == "Smith001"

def test_mlr_id_generation(identifier_registry):
    """Test MLR ID generation."""
    # Test first recommendation ID
    mlr_id1 = identifier_registry.generate_id(2020, "Smith001")
    assert mlr_id1 == "MLR-2020-Smith001-0001"
    
    # Test second recommendation from same paper
    mlr_id2 = identifier_registry.generate_id(2020, "Smith001")
    assert mlr_id2 == "MLR-2020-Smith001-0002"
    
    # Test ID from different paper
    mlr_id3 = identifier_registry.generate_id(2020, "Jones001")
    assert mlr_id3 == "MLR-2020-Jones001-0001"

def test_registry_persistence(temp_registry_file):
    """Test that registry state persists between instances."""
    # Create and use first registry instance
    registry1 = MLRIdentifierRegistry(temp_registry_file)
    paper_id = registry1.get_paper_id("Smith", 2020, "2020.12345")
    mlr_id = registry1.generate_id(2020, paper_id)
    
    # Create new registry instance and verify state
    registry2 = MLRIdentifierRegistry(temp_registry_file)
    assert registry2.get_paper_id("Smith", 2020, "2020.12345") == paper_id
    assert registry2.generate_id(2020, paper_id) == "MLR-2020-Smith001-0002"

def test_special_character_handling(identifier_registry):
    """Test handling of special characters in author names."""
    paper_id = identifier_registry.get_paper_id("O'Brien", 2020)
    assert paper_id == "OBrien001"
    
    paper_id2 = identifier_registry.get_paper_id("von Neumann", 2020)
    assert paper_id2 == "vonNeumann001"

def test_invalid_registry_file(tmp_path):
    """Test handling of corrupted registry file."""
    bad_file = tmp_path / "bad_registry.json"
    bad_file.write_text("invalid json")
    
    registry = MLRIdentifierRegistry(bad_file)
    assert registry.current_ids == {'paper_ids': {}, 'recommendation_ids': {}}
