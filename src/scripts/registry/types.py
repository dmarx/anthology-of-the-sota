# scripts/registry/types.py
"""Type definitions for ML recommendation registry."""

from enum import Enum
from dataclasses import dataclass, field, asdict
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

    def to_dict(self) -> Dict:
        """Convert source to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class Evidence:
    """Supporting evidence for a recommendation."""
    paper: str
    paper_id: str
    year: int
    arxiv_id: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert evidence to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}

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

    def to_dict(self) -> Dict:
        """Convert recommendation to dictionary."""
        data = {
            'id': self.id,
            'recommendation': self.recommendation,
            'topic': self.topic,
            'topic_id': self.topic_id,
            'source': self.source.to_dict(),
            'status': self.status.value,
            'supporting_evidence': [e.to_dict() for e in self.supporting_evidence],
            'implementations': self.implementations
        }
        if self.superseded_by:
            data['superseded_by'] = self.superseded_by
        if self.deprecated_date:
            data['deprecated_date'] = self.deprecated_date
        return {k: v for k, v in data.items() if v is not None}
