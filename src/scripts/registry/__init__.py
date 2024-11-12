# scripts/registry/__init__.py
"""ML Training Recommendations Registry.

A system for tracking, managing, and organizing machine learning training recommendations
from research papers with unique identifiers and status tracking.
"""

from .types import MLRStatus, Recommendation, Source, Evidence
from .identifiers import MLRIdentifierRegistry
from .recommendations import RecommendationRegistry
from .io import (
    load_research_yaml,
    save_registry,
    load_registry,
    registry_to_markdown,
    RegistryDataError
)

__version__ = "0.1.0"

__all__ = [
    'MLRStatus',
    'Recommendation',
    'Source',
    'Evidence',
    'MLRIdentifierRegistry',
    'RecommendationRegistry',
    'load_research_yaml',
    'save_registry',
    'load_registry',
    'registry_to_markdown',
    'RegistryDataError',
]
