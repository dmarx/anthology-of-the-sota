# tests/registry/test_recommendations.py
"""Tests for recommendation registry functionality."""

import pytest
from datetime import datetime

from scripts.registry.types import MLRStatus, Recommendation
from scripts.registry.recommendations import RecommendationRegistry, generate_topic_id

@pytest.fixture
def registry(temp_registry_file):
    """Provide a fresh recommendation registry."""
    return RecommendationRegistry()

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
    
    rec = registry.get_recommendation(mlr_id)
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
    
    rec = registry.get_recommendation(mlr_id)
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
    
    rec = registry.get_recommendation(mlr_id)
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

def test_topic_stats(registry):
    """Test topic statistics generation."""
    # Add recommendations with different statuses
    registry.add_recommendation(
        topic="optimization",
        recommendation="Standard rec",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020
    )
    
    registry.add_recommendation(
        topic="optimization",
        recommendation="Experimental rec",
        first_author="Jones",
        source_paper="Jones et al. (2021)",
        year=2021,
        experimental=True
    )
    
    stats = registry.get_topic_stats("optimization")
    assert stats['total_count'] == 2
    assert stats['status_counts'][MLRStatus.STANDARD.value] == 1
    assert stats['status_counts'][MLRStatus.EXPERIMENTAL.value] == 1
    assert stats['years']['earliest'] == 2020
    assert stats['years']['latest'] == 2021

def test_export_registry(registry):
    """Test registry export functionality."""
    # Add recommendations
    registry.add_recommendation(
        topic="optimization",
        recommendation="Rec 1",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020
    )
    
    exported = registry.export_registry()
    assert 'metadata' in exported
    assert 'recommendations' in exported
    assert 'topics' in exported
    assert exported['metadata']['schema_version'] == '1.0'
    assert MLRStatus.STANDARD.value in exported['recommendations']
    assert 'optimization' in exported['topics']
