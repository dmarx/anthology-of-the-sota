# src/scripts/registry/recommendations.py
"""Core recommendation registry functionality."""
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set
import logging
from omegaconf import OmegaConf, DictConfig

from .types import MLRStatus, Recommendation, Source, Evidence, create_config_from_dict
from .identifiers import MLRIdentifierRegistry

logger = logging.getLogger(__name__)

def generate_topic_id(topic: str, recommendation: str) -> str:
    """Generate a unique topic-based ID for a recommendation."""
    import re
    words = recommendation.lower().split()[:5]
    slug = '-'.join(words)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return f"{topic.lower().replace(' ', '-')}/{slug}"

class RecommendationRegistry:
    """Registry for ML training recommendations."""
    
    def __init__(self, id_registry: Optional[MLRIdentifierRegistry] = None):
        """Initialize the recommendation registry."""
        self.recommendations: Dict[str, Recommendation] = {}
        self.topic_to_recommendations: Dict[str, List[str]] = defaultdict(list)
        self.id_registry = id_registry or MLRIdentifierRegistry()
        self._config = create_config_from_dict({
            'recommendations': {},
            'metadata': {
                'schema_version': '1.0',
                'last_updated': datetime.now().strftime('%Y-%m-%d')
            }
        })
        logger.info("Initialized recommendation registry")

    def add_recommendation(self, 
                         topic: str,
                         recommendation: str,
                         first_author: str,
                         source_paper: str,
                         year: int,
                         arxiv_id: Optional[str] = None,
                         experimental: bool = False,
                         superseded_by: Optional[str] = None,
                         implementations: Optional[List[str]] = None) -> str:
        """Add a recommendation to the registry."""
        topic_id = generate_topic_id(topic, recommendation)
        paper_id = self.id_registry.get_paper_id(first_author, year, arxiv_id)
        mlr_id = self.id_registry.generate_id(year, paper_id)
        
        source = Source(
            paper=source_paper,
            paper_id=paper_id,
            year=year,
            first_author=first_author,
            arxiv_id=arxiv_id
        )
        
        # Determine status
        if superseded_by:
            status = MLRStatus.DEPRECATED
        elif experimental:
            status = MLRStatus.EXPERIMENTAL
        else:
            status = MLRStatus.STANDARD
            
        rec = Recommendation.create(
            id=mlr_id,
            recommendation=recommendation,
            topic=topic,
            topic_id=topic_id,
            source=source,
            status=status,
            superseded_by=superseded_by,
            deprecated_date=datetime.now().strftime('%Y-%m-%d') if superseded_by else None,
            implementations=implementations or []
        )
        
        self.recommendations[mlr_id] = rec
        self.topic_to_recommendations[topic].append(mlr_id)
        
        logger.info(f"Added recommendation {mlr_id} with status {status}")
        return mlr_id

    def get_recommendation_by_mlr(self, mlr_id: str) -> Optional[Recommendation]:
        """Get a recommendation by its MLR ID."""
        return self.recommendations.get(mlr_id)
    
    def get_recommendations_by_status(self, status: MLRStatus) -> List[Recommendation]:
        """Get all recommendations with a given status."""
        return [rec for rec in self.recommendations.values() if rec.status == status]
    
    def get_recommendations_by_topic(self, topic: str, status: Optional[MLRStatus] = None) -> List[Recommendation]:
        """Get recommendations for a topic, optionally filtered by status."""
        recs = [self.recommendations[mlr_id] for mlr_id in self.topic_to_recommendations[topic]]
        if status:
            recs = [rec for rec in recs if rec.status == status]
        return sorted(recs, key=lambda x: x.source.year)

    def get_topics(self) -> Set[str]:
        """Get all unique topics in the registry."""
        return set(self.topic_to_recommendations.keys())

    def export_registry(self) -> Dict:
        """Export the registry as a list of atomic recommendations."""
        return {
            'metadata': {
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'schema_version': '1.0',
                'status_types': [status.value for status in MLRStatus]
            },
            'recommendations': [
                rec.to_dict() for rec in self.recommendations.values()
            ],
            # Include topic stats for informational purposes
            'topics': {
                topic: {
                    'count': len(recs),
                    'years': {
                        'earliest': min(self.recommendations[rid].source.year for rid in recs),
                        'latest': max(self.recommendations[rid].source.year for rid in recs)
                    }
                }
                for topic, recs in self.topic_to_recommendations.items()
            }
        }

def build_registry_from_yaml(yaml_data: Dict) -> RecommendationRegistry:
    """Build a recommendation registry from YAML research data."""
    registry = RecommendationRegistry()
    config = create_config_from_dict(yaml_data)
    
    # Process each year's papers
    for year, papers in config.items():
        for paper in papers:
            # Extract basic paper info
            first_author = paper.first_author
            arxiv_id = paper.get('arxiv_id', None)
            paper_id = f"{first_author} et al. ({year})"
            
            # Process SOTA recommendations
            if hasattr(paper, 'sota') and paper.sota:
                for rec in paper.sota:
                    main_topic = paper.topics[0] if paper.topics else 'general'
                    mlr_id = registry.add_recommendation(
                        topic=main_topic,
                        recommendation=rec,
                        first_author=first_author,
                        source_paper=paper_id,
                        year=int(year),
                        arxiv_id=arxiv_id,
                        implementations=paper.get('models', [])
                    )
                    logger.info(f"Added recommendation {mlr_id}: {rec}")
            
            # Process experimental recommendations
            if paper.get('experimental', False):
                for rec in paper.get('sota', []):
                    mlr_id = registry.add_recommendation(
                        topic=paper.topics[0],
                        recommendation=rec,
                        first_author=first_author,
                        source_paper=paper_id,
                        year=int(year),
                        arxiv_id=arxiv_id,
                        experimental=True
                    )
                    logger.info(f"Added experimental recommendation {mlr_id}: {rec}")
            
            # Process deprecated/superseded recommendations
            if 'attic' in paper and 'superseded_by' in paper.attic:
                for rec in paper.get('sota', []):
                    mlr_id = registry.add_recommendation(
                        topic=paper.topics[0],
                        recommendation=rec,
                        first_author=first_author,
                        source_paper=paper_id,
                        year=int(year),
                        arxiv_id=arxiv_id,
                        superseded_by=paper.attic.superseded_by
                    )
                    logger.info(f"Added deprecated recommendation {mlr_id}: {rec}")

    return registry
