# tests/registry/test_recommendations.py
"""Tests for recommendation registry functionality."""

import pytest
from pathlib import Path
from datetime import datetime

from scripts.registry.types import MLRStatus, Recommendation, Source, Evidence
from scripts.registry.recommendations import RecommendationRegistry, generate_topic_id
from scripts.registry.identifiers import MLRIdentifierRegistry

@pytest.fixture
def id_registry(tmp_path):
    """Fixture providing a fresh identifier registry."""
    return MLRIdentifierRegistry(tmp_path / "test_mlr_registry.json")

@pytest.fixture
def registry(id_registry):
    """Fixture providing a fresh recommendation registry."""
    return RecommendationRegistry(id_registry)

def test_topic_id_generation():
    """Test topic ID generation."""
    topic = "Optimization"
    rec = "Use gradient clipping with dynamic threshold"
    topic_id = generate_topic_id(topic, rec)
    assert topic_id == "optimization/use-gradient-clipping-with-dynamic"

def test_add_standard_recommendation(registry):
    """Test adding a standard recommendation."""
    mlr_id = registry.add_recommendation(
        topic="optimization",
        recommendation="Use gradient clipping",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020,
        arxiv_id="2020.12345"
    )
    
    rec = registry.get_recommendation_by_mlr(mlr_id)
    assert rec is not None
    assert rec.status == MLRStatus.STANDARD
    assert rec.topic == "optimization"
    assert rec.source.year == 2020

def test_add_experimental_recommendation(registry):
    """Test adding an experimental recommendation."""
    mlr_id = registry.add_recommendation(
        topic="attention",
        recommendation="New attention mechanism",
        first_author="Jones",
        source_paper="Jones et al. (2021)",
        year=2021,
        experimental=True
    )
    
    rec = registry.get_recommendation_by_mlr(mlr_id)
    assert rec.status == MLRStatus.EXPERIMENTAL

def test_add_deprecated_recommendation(registry):
    """Test adding a deprecated recommendation."""
    mlr_id = registry.add_recommendation(
        topic="optimization",
        recommendation="Old method",
        first_author="Brown",
        source_paper="Brown et al. (2019)",
        year=2019,
        superseded_by="MLR-2020-Smith001-0001"
    )
    
    rec = registry.get_recommendation_by_mlr(mlr_id)
    assert rec.status == MLRStatus.DEPRECATED
    assert rec.superseded_by == "MLR-2020-Smith001-0001"
    assert rec.deprecated_date is not None

def test_get_recommendations_by_status(registry):
    """Test filtering recommendations by status."""
    # Add recommendations with different statuses
    registry.add_recommendation(
        topic="optimization",
        recommendation="Standard rec",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020
    )
    
    registry.add_recommendation(
        topic="attention",
        recommendation="Experimental rec",
        first_author="Jones",
        source_paper="Jones et al. (2021)",
        year=2021,
        experimental=True
    )
    
    standard_recs = registry.get_recommendations_by_status(MLRStatus.STANDARD)
    experimental_recs = registry.get_recommendations_by_status(MLRStatus.EXPERIMENTAL)
    
    assert len(standard_recs) == 1
    assert len(experimental_recs) == 1

def test_get_recommendations_by_topic(registry):
    """Test filtering recommendations by topic."""
    # Add multiple recommendations for same topic
    registry.add_recommendation(
        topic="optimization",
        recommendation="Rec 1",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020
    )
    
    registry.add_recommendation(
        topic="optimization",
        recommendation="Rec 2",
        first_author="Jones",
        source_paper="Jones et al. (2021)",
        year=2021
    )
    
    recs = registry.get_recommendations_by_topic("optimization")
    assert len(recs) == 2
    # Check sorting by year
    assert recs[0].source.year < recs[1].source.year

# def test_topic_stats(registry):
#     """Test topic statistics generation."""
#     # Add recommendations with different statuses
#     registry.add_recommendation(
#         topic="optimization",
#         recommendation="Standard rec",
#         first_author="Smith",
#         source_paper="Smith et al. (2020)",
#         year=2020
#     )
    
#     registry.add_recommendation(
#         topic="optimization",
#         recommendation="Experimental rec",
#         first_author="Jones",
#         source_paper="Jones et al. (2021)",
#         year=2021,
#         experimental=True
#     )
    
#     stats = registry._get_topic_stats("optimization")
#     assert stats['total_count'] == 2
#     assert stats['status_counts'][MLRStatus.STANDARD.value] == 1
#     assert stats['status_counts'][MLRStatus.EXPERIMENTAL.value] == 1
#     assert stats['years']['earliest'] == 2020
#     assert stats['years']['latest'] == 2021

def test_registry_export(registry):
    """Test registry export functionality."""
    # Add recommendations with different statuses
    registry.add_recommendation(
        topic="optimization",
        recommendation="Standard rec",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020
    )
    
    registry.add_recommendation(
        topic="attention",
        recommendation="Experimental rec",
        first_author="Jones",
        source_paper="Jones et al. (2021)",
        year=2021,
        experimental=True
    )
    
    exported = registry.export_registry()
    
    # Check basic structure
    assert 'metadata' in exported
    assert 'recommendations' in exported
    assert 'topics' in exported
    assert exported['metadata']['schema_version'] == '1.0'
    
    # Check recommendations are a flat list
    assert isinstance(exported['recommendations'], list)
    assert len(exported['recommendations']) == 2
    
    # Check individual recommendations
    standard_rec = next(
        (r for r in exported['recommendations'] 
         if r['status'] == MLRStatus.STANDARD.value), 
        None
    )
    experimental_rec = next(
        (r for r in exported['recommendations'] 
         if r['status'] == MLRStatus.EXPERIMENTAL.value),
        None
    )
    
    assert standard_rec is not None
    assert experimental_rec is not None
    
    # Verify standard recommendation
    assert standard_rec['recommendation'] == "Standard rec"
    assert standard_rec['topic'] == "optimization"
    assert standard_rec['status'] == MLRStatus.STANDARD.value
    
    # Verify experimental recommendation
    assert experimental_rec['recommendation'] == "Experimental rec"
    assert experimental_rec['topic'] == "attention"
    assert experimental_rec['status'] == MLRStatus.EXPERIMENTAL.value
    
    # Check topic stats
    assert 'optimization' in exported['topics']
    assert 'attention' in exported['topics']
    assert exported['topics']['optimization']['count'] == 1
    assert exported['topics']['attention']['count'] == 1
