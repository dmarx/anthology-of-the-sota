# scripts/registry/types.py
"""Type definitions for ML recommendation registry."""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

class MLRStatus(str, Enum):
    """Status states for ML recommendations."""
    EXPERIMENTAL = "experimental"
    STANDARD = "standard"
    DEPRECATED = "deprecated"

@dataclass
class Source:
    """Source information for a recommendation."""
    paper: str
    paper_id: str
    year: int
    first_author: str
    arxiv_id: Optional[str] = None

@dataclass
class Evidence:
    """Supporting evidence for a recommendation."""
    paper: str
    paper_id: str
    year: int
    arxiv_id: Optional[str] = None

@dataclass
class Recommendation:
    """ML training recommendation."""
    id: str
    recommendation: str
    topic: str
    topic_id: str
    source: Source
    status: MLRStatus
    supporting_evidence: List[Evidence] = field(default_factory=list)
    superseded_by: Optional[str] = None
    deprecated_date: Optional[str] = None
    implementations: List[str] = field(default_factory=list)

    @classmethod
    def create(cls, 
               id: str,
               recommendation: str,
               topic: str,
               topic_id: str,
               source: Dict,
               status: MLRStatus,
               **kwargs) -> 'Recommendation':
        """Create a recommendation from raw data."""
        return cls(
            id=id,
            recommendation=recommendation,
            topic=topic,
            topic_id=topic_id,
            source=Source(**source),
            status=status,
            **kwargs
        )
