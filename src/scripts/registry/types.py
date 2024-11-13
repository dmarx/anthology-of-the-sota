# scripts/registry/types.py
"""Type definitions for ML recommendation registry."""

from enum import Enum
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
from omegaconf import OmegaConf, DictConfig, MISSING

class MLRStatus(str, Enum):
    """Status states for ML recommendations."""
    EXPERIMENTAL = "experimental"
    STANDARD = "standard"
    DEPRECATED = "deprecated"

@dataclass
class Source:
    """Source information for a recommendation."""
    paper: str = MISSING
    paper_id: str = MISSING
    year: int = MISSING
    first_author: str = MISSING
    arxiv_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Union[Dict, DictConfig]) -> 'Source':
        """Create Source from dictionary or DictConfig."""
        conf = OmegaConf.create(data)
        return cls(
            paper=conf.paper,
            paper_id=conf.paper_id,
            year=conf.year,
            first_author=conf.first_author,
            arxiv_id=conf.get('arxiv_id', None)
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary, omitting None values."""
        return {k: v for k, v in OmegaConf.to_container(OmegaConf.create(self)).items() if v is not None}

@dataclass
class Evidence:
    """Supporting evidence for a recommendation."""
    paper: str = MISSING
    paper_id: str = MISSING
    year: int = MISSING
    arxiv_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Union[Dict, DictConfig]) -> 'Evidence':
        """Create Evidence from dictionary or DictConfig."""
        conf = OmegaConf.create(data)
        return cls(
            paper=conf.paper,
            paper_id=conf.paper_id,
            year=conf.year,
            arxiv_id=conf.get('arxiv_id', None)
        )

    def to_dict(self) -> Dict:
        """Convert to dictionary, omitting None values."""
        return {k: v for k, v in OmegaConf.to_container(OmegaConf.create(self)).items() if v is not None}

@dataclass
class Recommendation:
    """ML training recommendation."""
    id: str = MISSING
    recommendation: str = MISSING
    topic: str = MISSING
    topic_id: str = MISSING
    source: Source = MISSING
    status: MLRStatus = MISSING
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
               source: Union[Dict, DictConfig, Source],
               status: MLRStatus,
               **kwargs) -> 'Recommendation':
        """Create a recommendation from raw data."""
        if isinstance(source, (Dict, DictConfig)):
            source = Source.from_dict(source)
        
        evidence_list = kwargs.get('supporting_evidence', [])
        if evidence_list:
            evidence_list = [
                Evidence.from_dict(e) if isinstance(e, (Dict, DictConfig)) else e
                for e in evidence_list
            ]
        
        return cls(
            id=id,
            recommendation=recommendation,
            topic=topic,
            topic_id=topic_id,
            source=source,
            status=status,
            supporting_evidence=evidence_list,
            superseded_by=kwargs.get('superseded_by'),
            deprecated_date=kwargs.get('deprecated_date'),
            implementations=kwargs.get('implementations', [])
        )

    def to_dict(self) -> Dict:
        """Convert recommendation to dictionary."""
        conf = OmegaConf.create({
            'id': self.id,
            'recommendation': self.recommendation,
            'topic': self.topic,
            'topic_id': self.topic_id,
            'source': self.source.to_dict(),
            'status': self.status.value,
            'supporting_evidence': [e.to_dict() for e in self.supporting_evidence],
            'implementations': self.implementations,
            'superseded_by': self.superseded_by,
            'deprecated_date': self.deprecated_date
        })
        return {k: v for k, v in conf.to_container() if v is not None}

def create_config_from_dict(data: Dict) -> DictConfig:
    """Create an OmegaConf config from a dictionary."""
    return OmegaConf.create(data)
