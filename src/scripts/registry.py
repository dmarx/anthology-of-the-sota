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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
    """Main registry for ML training recommendations."""
    
    def __init__(self):
        """Initialize the recommendation registry."""
        self.recommendations = {}
        self.deprecated_recommendations = {}
        self.experimental_recommendations = {}
        self.evidence = defaultdict(list)
        self.implementations = defaultdict(list)
        self.id_registry = MLRIdentifierRegistry()
        self.id_to_recommendation = {}
        
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
            MLR identifier string
        """
        topic_id = self._generate_topic_id(topic, recommendation)
        
        paper_id = self.id_registry.get_paper_id(first_author, year, arxiv_id)
        mlr_id = self.id_registry.generate_id(year, paper_id)
        
        rec_data = {
            'id': mlr_id,
            'recommendation': recommendation,
            'topic': topic,
            'topic_id': topic_id,
            'source': {
                'paper': source_paper,
                'paper_id': paper_id,
                'arxiv_id': arxiv_id,
                'year': year
            },
            'supporting_evidence': [],
            'status': 'experimental' if experimental else 'active'
        }
        
        if superseded_by:
            if topic_id in self.recommendations:
                old_rec = self.recommendations[topic_id]
                self.deprecated_recommendations[old_rec['id']] = {
                    **old_rec,
                    'status': 'deprecated',
                    'superseded_by': superseded_by,
                    'deprecated_date': datetime.now().strftime('%Y-%m-%d')
                }
                del self.recommendations[topic_id]
            return mlr_id

        if experimental:
            self.experimental_recommendations[mlr_id] = rec_data
        else:
            if topic_id not in self.recommendations:
                self.recommendations[topic_id] = rec_data
            self.evidence[topic_id].append({
                'paper': source_paper,
                'paper_id': paper_id,
                'arxiv_id': arxiv_id,
                'year': year
            })
            
        if implementations:
            self.implementations[mlr_id].extend(implementations)
            
        self.id_to_recommendation[mlr_id] = rec_data
        return mlr_id

    def _generate_topic_id(self, topic: str, recommendation: str) -> str:
        """Generate a unique topic-based ID for internal use."""
        words = recommendation.lower().split()[:5]
        slug = '-'.join(words)
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        return f"{topic.lower().replace(' ', '-')}/{slug}"

    def get_recommendation_by_mlr(self, mlr_id: str) -> Optional[Dict]:
        """Retrieve a recommendation by its MLR ID."""
        return self.id_to_recommendation.get(mlr_id)

    def export_registry(self) -> Dict:
        """Export the full registry as a dictionary."""
        return {
            'metadata': {
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'schema_version': '1.0'
            },
            'recommendations': {
                'active': {
                    topic: sorted(
                        [rec for rec in self.recommendations.values() if rec['topic'] == topic],
                        key=lambda x: x['source']['year']
                    )
                    for topic in self._get_all_topics()
                },
                'experimental': self.experimental_recommendations,
                'deprecated': self.deprecated_recommendations
            },
            'implementation_references': {
                mlr_id: impls for mlr_id, impls in self.implementations.items()
            },
            'cross_references': self._generate_cross_references()
        }
    
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
