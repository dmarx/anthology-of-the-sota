# scripts/registry/identifiers.py
"""MLR identifier generation and management."""

import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class MLRIdentifierRegistry:
    """Manages unique identifiers for ML recommendations."""
    
    def __init__(self, registry_file: str | Path = "mlr_registry.json"):
        """Initialize the identifier registry.
        
        Args:
            registry_file: Path to the JSON file storing ID mappings
        """
        self.registry_file = Path(registry_file)
        self.current_ids = self._load_registry()
        self.author_counters = self._initialize_author_counters()
        
    def _load_registry(self) -> Dict[str, Dict]:
        """Load existing MLR IDs from registry file."""
        try:
            if self.registry_file.exists():
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            logger.info(f"No existing registry found at {self.registry_file}")
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
    
    def _save_registry(self) -> None:
        """Save current MLR IDs to registry file."""
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_file, 'w') as f:
            json.dump(self.current_ids, f, indent=2)
        logger.debug(f"Saved registry to {self.registry_file}")
    
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
        logger.debug(f"Generated new paper ID {paper_id} for {paper_key}")
        
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
        logger.debug(f"Generated new MLR ID {mlr_id}")
        return mlr_id
