#!/usr/bin/env python3
"""
ML Training Recommendations Registry Builder

This script processes ML research papers and their recommendations to build
a structured registry with unique identifiers and tracking capabilities.
"""

import yaml
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Set, Union
import re
import json
import os
import logging
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Union, Literal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLRStatus(str, Enum):
    EXPERIMENTAL = "experimental"
    STANDARD = "standard"
    DEPRECATED = "deprecated"

@dataclass
class Recommendation:
    id: str
    recommendation: str
    topic: str
    topic_id: str
    source: Dict
    status: MLRStatus
    supporting_evidence: List[Dict] = None
    superseded_by: Optional[str] = None
    deprecated_date: Optional[str] = None
    implementations: List[str] = None


class MLRIdentifierRegistry:
    """Manages unique identifiers for ML recommendations."""
    
    def __init__(self, registry_file: str = 'mlr_registry.json'):
        """Initialize the identifier registry.
        
        Args:
            registry_file: Path to the JSON file storing ID mappings
        """
        self.registry_file = registry_file
        self.current_ids = self._load_registry()
        self.author_counters = self._initialize_author_counters()
        
    def _load_registry(self) -> Dict[str, Dict]:
        """Load existing MLR IDs from registry file."""
        try:
            if os.path.exists(self.registry_file):
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
        except json.JSONDecodeError:
            logger.warning(f"Error reading registry file {self.registry_file}. Starting fresh.")
        return {'paper_ids': {}, 'recommendation_ids': {}}
    
    def _initialize_author_counters(self) -> Dict[str, int]:
        """Initialize counters for author IDs from existing registry."""
        counters = defaultdict(int)
        for paper_id in self.current_ids['paper_ids'].values():
            if match := re.match(r'([A-Za-z]+)(\d+)', paper_id):
                author, num = match.groups()
                counters[author] = max(counters[author], int(num))
        return counters
    
    def _save_registry(self):
        """Save current MLR IDs to registry file."""
        os.makedirs(os.path.dirname(self.registry_file) or '.', exist_ok=True)
        with open(self.registry_file, 'w') as f:
            json.dump(self.current_ids, f, indent=2)
    
    def get_paper_id(self, first_author: str, year: int, arxiv_id: Optional[str] = None) -> str:
        """Get or generate a paper identifier.
        
        Args:
            first_author: First author's name
            year: Publication year
            arxiv_id: Optional arXiv identifier
            
        Returns:
            Unique paper identifier string
        """
        paper_key = f"{first_author}-{year}-{arxiv_id if arxiv_id else 'none'}"
        
        if paper_key in self.current_ids['paper_ids']:
            return self.current_ids['paper_ids'][paper_key]
        
        author_base = re.sub(r'[^A-Za-z]', '', first_author)
        self.author_counters[author_base] += 1
        paper_id = f"{author_base}{self.author_counters[author_base]:03d}"
        
        self.current_ids['paper_ids'][paper_key] = paper_id
        self._save_registry()
        
        return paper_id
            
    def generate_id(self, year: int, paper_id: str) -> str:
        """Generate a new unique MLR identifier.
        
        Args:
            year: Publication year
            paper_id: Unique paper identifier
            
        Returns:
            MLR identifier string
        """
        key = f"{year}-{paper_id}"
        if key not in self.current_ids['recommendation_ids']:
            self.current_ids['recommendation_ids'][key] = 0
        
        self.current_ids['recommendation_ids'][key] += 1
        mlr_id = f"MLR-{year}-{paper_id}-{self.current_ids['recommendation_ids'][key]:04d}"
        self._save_registry()
        return mlr_id

class RecommendationRegistry:
    def __init__(self):
        """Initialize the recommendation registry."""
        self.recommendations: Dict[str, Recommendation] = {}
        self.id_registry = MLRIdentifierRegistry()
        self.topic_to_recommendations: Dict[str, List[str]] = defaultdict(list)
        
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
        topic_id = self._generate_topic_id(topic, recommendation)
        paper_id = self.id_registry.get_paper_id(first_author, year, arxiv_id)
        mlr_id = self.id_registry.generate_id(year, paper_id)
        
        # Determine status
        if superseded_by:
            status = MLRStatus.DEPRECATED
        elif experimental:
            status = MLRStatus.EXPERIMENTAL
        else:
            status = MLRStatus.STANDARD
            
        rec = Recommendation(
            id=mlr_id,
            recommendation=recommendation,
            topic=topic,
            topic_id=topic_id,
            source={
                'paper': source_paper,
                'paper_id': paper_id,
                'arxiv_id': arxiv_id,
                'year': year,
                'first_author': first_author
            },
            status=status,
            supporting_evidence=[],
            superseded_by=superseded_by,
            deprecated_date=datetime.now().strftime('%Y-%m-%d') if superseded_by else None,
            implementations=implementations or []
        )
        
        self.recommendations[mlr_id] = rec
        self.topic_to_recommendations[topic].append(mlr_id)
        
        return mlr_id

    def get_recommendations_by_status(self, status: MLRStatus) -> List[Recommendation]:
        """Get all recommendations with a given status."""
        return [rec for rec in self.recommendations.values() if rec.status == status]
    
    def get_recommendations_by_topic(self, topic: str, status: Optional[MLRStatus] = None) -> List[Recommendation]:
        """Get recommendations for a topic, optionally filtered by status."""
        recs = [self.recommendations[mlr_id] for mlr_id in self.topic_to_recommendations[topic]]
        if status:
            recs = [rec for rec in recs if rec.status == status]
        return sorted(recs, key=lambda x: x.source['year'])
    
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
                    topic: [rec.__dict__ for rec in self.get_recommendations_by_topic(topic, status)]
                    for topic in self._get_all_topics()
                }
                for status in MLRStatus
            },
            'topics': {
                topic: {
                    'total_count': len(self.topic_to_recommendations[topic]),
                    'status_counts': {
                        status.value: len(self.get_recommendations_by_topic(topic, status))
                        for status in MLRStatus
                    }
                }
                for topic in self._get_all_topics()
            }
        }

    def _generate_topic_id(self, topic: str, recommendation: str) -> str:
        """Generate a unique topic-based ID for internal use."""
        words = recommendation.lower().split()[:5]
        slug = '-'.join(words)
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        return f"{topic.lower().replace(' ', '-')}/{slug}"
    
    def _generate_cross_references(self) -> Dict[str, List[str]]:
        """Generate cross-references between related recommendations."""
        cross_refs = defaultdict(list)
        # Group recommendations by topic
        topic_groups = defaultdict(list)
        for rec_id, rec in self.id_to_recommendation.items():
            topic_groups[rec['topic']].append(rec_id)
        
        # Create cross-references for recommendations in the same topic
        for topic, rec_ids in topic_groups.items():
            for rec_id in rec_ids:
                cross_refs[rec_id] = [rid for rid in rec_ids if rid != rec_id]
        
        return dict(cross_refs)

    def _get_all_topics(self) -> Set[str]:
        """Get all unique topics in the registry."""
        return {rec['topic'] for rec in self.recommendations.values()}

def build_registry_from_yaml(yaml_data: Dict) -> RecommendationRegistry:
    """Build a recommendation registry from YAML research data."""
    registry = RecommendationRegistry()
    
    # Process each year's papers
    for year, papers in yaml_data.items():
        for paper in papers:
            # Extract basic paper info
            first_author = paper['first_author']
            arxiv_id = paper.get('arxiv_id')
            paper_id = f"{first_author} et al. ({year})"
            
            # Process SOTA recommendations
            if 'sota' in paper:
                for rec in paper['sota']:
                    main_topic = paper['topics'][0] if paper['topics'] else 'general'
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
                        topic=paper['topics'][0],
                        recommendation=rec,
                        first_author=first_author,
                        source_paper=paper_id,
                        year=int(year),
                        arxiv_id=arxiv_id,
                        experimental=True
                    )
                    logger.info(f"Added experimental recommendation {mlr_id}: {rec}")
            
            # Process deprecated/superseded recommendations
            if 'attic' in paper and 'superseded_by' in paper['attic']:
                for rec in paper.get('sota', []):
                    mlr_id = registry.add_recommendation(
                        topic=paper['topics'][0],
                        recommendation=rec,
                        first_author=first_author,
                        source_paper=paper_id,
                        year=int(year),
                        arxiv_id=arxiv_id,
                        superseded_by=paper['attic']['superseded_by']
                    )
                    logger.info(f"Added deprecated recommendation {mlr_id}: {rec}")

    return registry

def save_registry(registry: RecommendationRegistry, output_file: str):
    """Save the registry to a YAML file."""
    try:
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w') as f:
            yaml.safe_dump(registry.export_registry(), f, sort_keys=False, allow_unicode=True)
        logger.info(f"Successfully saved registry to {output_file}")
    except Exception as e:
        logger.error(f"Error saving registry to {output_file}: {e}")
        raise

def main():
    """Main execution function."""
    try:
        # Load research data
        with open('data/research.yaml', 'r') as f:
            research_data = yaml.safe_load(f)
        
        # Build and save registry
        registry = build_registry_from_yaml(research_data)
        save_registry(registry, 'ml_training_registry.yaml')
        
    except FileNotFoundError as e:
        logger.error(f"Input file not found: {e}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == '__main__':
    main()
