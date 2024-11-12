import pytest
import yaml
from pathlib import Path
import json
import os
from scripts.registry import (
    MLRIdentifierRegistry, 
    RecommendationRegistry,
    build_registry_from_yaml,
    save_registry
)

@pytest.fixture
def sample_yaml_data():
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
def temp_registry_file(tmp_path):
    registry_file = tmp_path / "test_registry.json"
    return str(registry_file)

@pytest.fixture
def temp_output_file(tmp_path):
    output_file = tmp_path / "test_output.yaml"
    return str(output_file)

class TestMLRIdentifierRegistry:
    def test_initialization(self, temp_registry_file):
        registry = MLRIdentifierRegistry(temp_registry_file)
        assert registry.current_ids == {'paper_ids': {}, 'recommendation_ids': {}}
        assert isinstance(registry.author_counters, dict)

    def test_paper_id_generation(self, temp_registry_file):
        registry = MLRIdentifierRegistry(temp_registry_file)
        
        # Test first paper ID generation
        paper_id1 = registry.get_paper_id("Smith", 2020, "2020.12345")
        assert paper_id1 == "Smith001"
        
        # Test same author, different paper
        paper_id2 = registry.get_paper_id("Smith", 2020, "2020.99999")
        assert paper_id2 == "Smith002"
        
        # Test different author
        paper_id3 = registry.get_paper_id("Jones", 2020, "2020.54321")
        assert paper_id3 == "Jones001"

    def test_mlr_id_generation(self, temp_registry_file):
        registry = MLRIdentifierRegistry(temp_registry_file)
        
        # Test first recommendation ID
        mlr_id1 = registry.generate_id(2020, "Smith001")
        assert mlr_id1 == "MLR-2020-Smith001-0001"
        
        # Test second recommendation from same paper
        mlr_id2 = registry.generate_id(2020, "Smith001")
        assert mlr_id2 == "MLR-2020-Smith001-0002"

    def test_registry_persistence(self, temp_registry_file):
        # Create and use registry
        registry1 = MLRIdentifierRegistry(temp_registry_file)
        paper_id = registry1.get_paper_id("Smith", 2020, "2020.12345")
        mlr_id = registry1.generate_id(2020, paper_id)
        
        # Create new registry instance and verify state persistence
        registry2 = MLRIdentifierRegistry(temp_registry_file)
        assert registry2.get_paper_id("Smith", 2020, "2020.12345") == paper_id
        assert registry2.generate_id(2020, paper_id) == "MLR-2020-Smith001-0002"

class TestRecommendationRegistry:
    def test_add_recommendation(self, temp_registry_file):
        registry = RecommendationRegistry()
        
        mlr_id = registry.add_recommendation(
            topic="optimization",
            recommendation="Use gradient clipping",
            first_author="Smith",
            source_paper="Smith et al. (2020)",
            year=2020,
            arxiv_id="2020.12345"
        )
        
        assert mlr_id.startswith("MLR-2020-Smith001")
        assert registry.get_recommendation_by_mlr(mlr_id) is not None
        assert registry.get_recommendation_by_mlr(mlr_id)['topic'] == "optimization"

    def test_experimental_recommendation(self, temp_registry_file):
        registry = RecommendationRegistry()
        
        mlr_id = registry.add_recommendation(
            topic="optimization",
            recommendation="Experimental approach",
            first_author="Smith",
            source_paper="Smith et al. (2020)",
            year=2020,
            experimental=True
        )
        
        assert mlr_id in registry.experimental_recommendations
        assert registry.experimental_recommendations[mlr_id]['status'] == 'experimental'

    def test_deprecated_recommendation(self, temp_registry_file):
        registry = RecommendationRegistry()
        
        # Add original recommendation
        mlr_id1 = registry.add_recommendation(
            topic="optimization",
            recommendation="Old approach",
            first_author="Smith",
            source_paper="Smith et al. (2020)",
            year=2020
        )
        
        # Add superseding recommendation
        mlr_id2 = registry.add_recommendation(
            topic="optimization",
            recommendation="Old approach",
            first_author="Jones",
            source_paper="Jones et al. (2021)",
            year=2021,
            superseded_by="2021.99999"
        )
        
        assert mlr_id1 in registry.deprecated_recommendations
        assert registry.deprecated_recommendations[mlr_id1]['status'] == 'deprecated'

    def test_export_registry(self, temp_registry_file):
        registry = RecommendationRegistry()
        
        # Add various recommendations
        registry.add_recommendation(
            topic="optimization",
            recommendation="Recommendation 1",
            first_author="Smith",
            source_paper="Smith et al. (2020)",
            year=2020
        )
        
        registry.add_recommendation(
            topic="optimization",
            recommendation="Recommendation 2",
            first_author="Jones",
            source_paper="Jones et al. (2021)",
            year=2021,
            experimental=True
        )
        
        exported = registry.export_registry()
        assert 'metadata' in exported
        assert 'recommendations' in exported
        assert 'active' in exported['recommendations']
        assert 'experimental' in exported['recommendations']
        assert 'deprecated' in exported['recommendations']

def test_build_registry_from_yaml(sample_yaml_data, temp_registry_file):
    registry = build_registry_from_yaml(sample_yaml_data)
    
    # Verify all recommendations were processed
    exported = registry.export_registry()
    active_recs = []
    for topic_recs in exported['recommendations']['active'].values():
        active_recs.extend(topic_recs)
    
    # Check counts
    assert len(active_recs) == 2  # Two SOTA recommendations from first paper
    assert len(exported['recommendations']['experimental']) == 1  # One experimental recommendation
    assert len(exported['recommendations']['deprecated']) == 1  # One deprecated recommendation

def test_save_registry(sample_yaml_data, temp_registry_file, temp_output_file):
    registry = build_registry_from_yaml(sample_yaml_data)
    save_registry(registry, temp_output_file)
    
    # Verify file was created and contains valid YAML
    assert os.path.exists(temp_output_file)
    with open(temp_output_file, 'r') as f:
        loaded_data = yaml.safe_load(f)
    
    assert 'metadata' in loaded_data
    assert 'recommendations' in loaded_data

@pytest.mark.integration
def test_full_pipeline(sample_yaml_data, temp_registry_file, temp_output_file):
    # Process sample data
    registry = build_registry_from_yaml(sample_yaml_data)
    save_registry(registry, temp_output_file)
    
    # Load and verify output
    with open(temp_output_file, 'r') as f:
        output_data = yaml.safe_load(f)
    
    assert output_data['metadata']['schema_version'] == '1.0'
    assert len(output_data['recommendations']['active']) > 0
    
    # Verify specific recommendations
    topics = set()
    for topic, recs in output_data['recommendations']['active'].items():
        topics.add(topic)
        for rec in recs:
            assert 'id' in rec
            assert rec['id'].startswith('MLR-')
            assert 'recommendation' in rec
            assert 'topic' in rec
            assert 'source' in rec
    
    assert 'optimization' in topics

def test_recommendation_status(temp_registry_file):
    registry = RecommendationRegistry()
    
    # Add recommendations with different statuses
    standard_id = registry.add_recommendation(
        topic="optimization",
        recommendation="Standard recommendation",
        first_author="Smith",
        source_paper="Smith et al. (2020)",
        year=2020
    )
    
    experimental_id = registry.add_recommendation(
        topic="optimization",
        recommendation="Experimental recommendation",
        first_author="Jones",
        source_paper="Jones et al. (2021)",
        year=2021,
        experimental=True
    )
    
    deprecated_id = registry.add_recommendation(
        topic="optimization",
        recommendation="Deprecated recommendation",
        first_author="Brown",
        source_paper="Brown et al. (2019)",
        year=2019,
        superseded_by="MLR-2020-Smith001-0001"
    )
    
    # Check status assignments
    assert registry.recommendations[standard_id].status == MLRStatus.STANDARD
    assert registry.recommendations[experimental_id].status == MLRStatus.EXPERIMENTAL
    assert registry.recommendations[deprecated_id].status == MLRStatus.DEPRECATED
    
    # Check status-based retrieval
    standard_recs = registry.get_recommendations_by_status(MLRStatus.STANDARD)
    experimental_recs = registry.get_recommendations_by_status(MLRStatus.EXPERIMENTAL)
    deprecated_recs = registry.get_recommendations_by_status(MLRStatus.DEPRECATED)
    
    assert len(standard_recs) == 1
    assert len(experimental_recs) == 1
    assert len(deprecated_recs) == 1
    
    # Check export format
    exported = registry.export_registry()
    assert set(exported['recommendations'].keys()) == {status.value for status in MLRStatus}
    assert all(topic in exported['topics'] for topic in registry._get_all_topics())
