# scripts/registry/recommendations.py
"""Core recommendation registry functionality."""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set
import logging

from .types import MLRStatus, Recommendation, Source
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
        """Initialize the recommendation registry.
        
        Args:
            id_registry: Optional identifier registry. If not provided, a new one will be created.
        """
        self.recommendations: Dict[str, Recommendation] = {}
        self.topic_to_recommendations: Dict[str, List[str]] = defaultdict(list)
        self.id_registry = id_registry or MLRIdentifierRegistry()
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
        """Add a recommendation to the registry.
        
        Args:
            topic: Main topic of the recommendation
            recommendation: The recommendation text
            first_author: First author's name
            source_paper: Full paper citation
            year: Publication year
            arxiv_id: Optional arXiv identifier
            experimental: Whether this is an experimental recommendation
            superseded_by: Optional MLR ID of superseding recommendation
            implementations: List of known implementations
            
        Returns:
            MLR identifier string for the new recommendation
        """
        topic_id = generate_topic_id(topic, recommendation)
        paper_id = self.id_registry.get_paper_id(first_author, year, arxiv_id)
        mlr_id = self.id_registry.generate_id(year, paper_id)
        
        # Determine status
        if superseded_by:
            status = MLRStatus.DEPRECATED
        elif experimental:
            status = MLRStatus.EXPERIMENTAL
        else:
            status = MLRStatus.STANDARD
        
        source = Source(
            paper=source_paper,
            paper_id=paper_id,
            year=year,
            first_author=first_author,
            arxiv_id=arxiv_id
        )
        
        rec = Recommendation.create(
            id=mlr_id,
            recommendation=recommendation,
            topic=topic,
            topic_id=topic_id,
            source=source.__dict__,
            status=status,
            superseded_by=superseded_by,
            deprecated_date=datetime.now().strftime('%Y-%m-%d') if superseded_by else None,
            implementations=implementations or []
        )
        
        self.recommendations[mlr_id] = rec
        self.topic_to_recommendations[topic].append(mlr_id)
        
        logger.info(f"Added recommendation {mlr_id} with status {status}")
        return mlr_id

    def get_recommendation(self, mlr_id: str) -> Optional[Recommendation]:
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
    
    def get_topic_stats(self, topic: str) -> Dict:
        """Get statistics for a specific topic."""
        recs = self.get_recommendations_by_topic(topic)
        return {
            'total_count': len(recs),
            'status_counts': {
                status.value: len([r for r in recs if r.status == status])
                for status in MLRStatus
            },
            'years': {
                'earliest': min(r.source.year for r in recs),
                'latest': max(r.source.year for r in recs)
            }
        }
    
    def export_registry(self) -> Dict:
        """Export the full registry as a dictionary."""
        return {
            'metadata': {
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'schema_version': '1.0',
                'status_types': [status.value for status in MLRStatus]
            },
            'recommendations': {
                status.value: {
                    topic: [
                        {k: v for k, v in rec.__dict__.items() if v is not None}
                        for rec in self.get_recommendations_by_topic(topic, status)
                    ]
                    for topic in self.get_topics()
                }
                for status in MLRStatus
            },
            'topics': {
                topic: self.get_topic_stats(topic)
                for topic in self.get_topics()
            }
        }
