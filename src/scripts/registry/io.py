# src/scripts/registry/io.py
"""I/O operations for the ML recommendation registry."""

import yaml
import json
from pathlib import Path
from typing import Dict, Union
from loguru import logger
from datetime import datetime
from collections import defaultdict

from .recommendations import RecommendationRegistry
from .types import MLRStatus

class RegistryDataError(Exception):
    """Raised when there are issues with registry data format."""
    pass

def validate_paper_entry(paper: Dict, year: str) -> None:
    """Validate a single paper entry.
    
    Args:
        paper: Dictionary containing paper data
        year: Year the paper is from (for error messages)
        
    Raises:
        RegistryDataError: If paper data is invalid
    """
    required_fields = {
        'title': str,
        'first_author': str,
        'year': int,
        #'topics': list
    }

    # Check for missing required fields
    missing_fields = [field for field in required_fields if field not in paper]
    if missing_fields:
        logger.warning(paper)
        raise RegistryDataError(
            f"Paper in year {year} missing required fields: {', '.join(missing_fields)}"
        )

    # Check field types
    # for field, expected_type in required_fields.items():
    #     if not isinstance(paper[field], expected_type):
    #         logger.warning(paper)
    #         raise RegistryDataError(
    #             f"Paper in year {year} has invalid type for {field}: "
    #             f"expected {expected_type.__name__}, got {type(paper[field]).__name__}"
    #         )

    # # Validate year matches container
    # if str(paper['year']) != str(year):
    #     raise RegistryDataError(
    #         f"Paper year {paper['year']} doesn't match container year {year}"
    #     )

    # # Validate topics not empty
    # if not paper['topics']:
    #     raise RegistryDataError(
    #         f"Paper '{paper['title']}' ({year}) has empty topics list"
    #     )

    # Validate topics are strings
    # if not all(isinstance(topic, str) for topic in paper['topics']):
    #     raise RegistryDataError(
    #         f"Paper '{paper['title']}' ({year}) has non-string topics"
    #     )

    # # If SOTA recommendations present, validate they're strings
    # if 'sota' in paper and not all(isinstance(rec, str) for rec in paper['sota']):
    #     raise RegistryDataError(
    #         f"Paper '{paper['title']}' ({year}) has non-string SOTA recommendations"
    #     )

def load_research_yaml(file_path: Union[str, Path]) -> Dict:
    """Load research data from YAML file.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Dictionary containing the research data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the file contains invalid YAML
        RegistryDataError: If the data format is invalid
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Research data file not found: {file_path}")

    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {file_path}: {e}")
        raise

    # Validate basic data structure
    if not isinstance(data, dict):
        raise RegistryDataError("Research data must be a dictionary")

    # Validate years and entries
    for year, papers in data.items():
        try:
            year_int = int(year)
            if not 1900 <= year_int <= datetime.now().year:
                raise RegistryDataError(f"Invalid year: {year}")
        except ValueError:
            raise RegistryDataError(f"Invalid year format: {year}")

        if not isinstance(papers, list):
            raise RegistryDataError(f"Papers for year {year} must be a list")

        # Validate each paper
        for paper in papers:
            if not isinstance(paper, dict):
                raise RegistryDataError(f"Invalid paper entry in year {year}")
            validate_paper_entry(paper, year)

    return data

def save_registry(registry: RecommendationRegistry, output_file: Union[str, Path]) -> None:
    """Save registry to a file.
    
    Args:
        registry: RecommendationRegistry instance
        output_file: Path where to save the file
    """
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    data = registry.export_registry()
    
    try:
        # Write as JSONL if .jsonl extension
        if output_file.suffix == '.jsonl':
            with open(output_file, 'w') as f:
                for rec in data['recommendations']:
                    f.write(json.dumps(rec) + '\n')
        # Write as YAML for other extensions
        else:
            with open(output_file, 'w') as f:
                yaml.safe_dump(
                    data,
                    f,
                    sort_keys=False,
                    allow_unicode=True,
                    default_flow_style=False
                )
        logger.info(f"Registry saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving registry to {output_file}: {e}")
        raise

def load_registry(file_path: Union[str, Path]) -> Dict:
    """Load a saved registry file.
    
    Args:
        file_path: Path to the registry file
        
    Returns:
        Dictionary containing the registry data
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Registry file not found: {file_path}")
    
    try:
        # Handle JSONL format
        if file_path.suffix == '.jsonl':
            recommendations = []
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip():
                        recommendations.append(json.loads(line))
            data = {
                'metadata': {
                    'schema_version': '1.0',
                    'last_updated': datetime.now().strftime('%Y-%m-%d')
                },
                'recommendations': recommendations
            }
        # Handle YAML format
        else:
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing registry file {file_path}: {e}")
        raise
    
    # Basic validation
    if not isinstance(data, dict):
        raise RegistryDataError("Invalid registry format")
    
    if 'recommendations' not in data:
        raise RegistryDataError("Registry missing recommendations")
    
    if not isinstance(data['recommendations'], list):
        raise RegistryDataError("Recommendations must be a list")
        
    return data

def registry_to_markdown(registry: RecommendationRegistry, output_file: Union[str, Path]) -> None:
    """Export registry to a markdown document."""
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    data = registry.export_registry()
    
    with open(output_file, 'w') as f:
        f.write("# ML Training Recommendations Registry\n\n")
        f.write(f"Last updated: {data['metadata']['last_updated']}\n\n")
        
        # Group recommendations by status and topic for display
        status_topics = defaultdict(lambda: defaultdict(list))
        for rec in data['recommendations']:
            status = rec.get('status', 'standard')
            topic = rec.get('topic', 'uncategorized')
            status_topics[status][topic].append(rec)
        
        # Write recommendations by status and topic
        for status in MLRStatus:
            f.write(f"## {status.value.title()} Recommendations\n\n")
            
            for topic, recs in sorted(status_topics[status.value].items()):
                if recs:
                    f.write(f"### {topic}\n\n")
                    for rec in recs:
                        f.write(f"- {rec['recommendation']}\n")
                        if rec.get('implementations'):
                            f.write(f"  - Implementations: {', '.join(rec['implementations'])}\n")
                        f.write("\n")
            f.write("\n")
        
        # Write statistics
        f.write("## Statistics\n\n")
        for topic_data in data['topics'].items():
            topic, stats = topic_data
            f.write(f"### {topic}\n\n")
            f.write(f"- Total recommendations: {stats['count']}\n")
            if stats['years']['earliest'] and stats['years']['latest']:
                f.write(f"- Year range: {stats['years']['earliest']} - {stats['years']['latest']}\n")
            f.write("\n")
