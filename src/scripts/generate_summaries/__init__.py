"""Package for generating directory summaries to assist LLM interactions."""
from pathlib import Path
from typing import List

__version__ = "0.1.0"

# Re-export main functionality
from .generator import SummaryGenerator

__all__ = ["SummaryGenerator"]
