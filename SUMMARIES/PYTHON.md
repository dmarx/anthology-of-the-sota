# Python Project Structure

## src/scripts/generate_summaries/__main__.py
```python
def commit_and_push(message: str, branch: str, paths: list[str | Path], base_branch: Optional[str], force: bool) -> None
    """
    Commit changes and push to specified branch.
    Args:
        message: Commit message
        branch: Branch to push to
        paths: List of paths to commit
        base_branch: Optional base branch to create new branch from
        force: If True, create fresh branch and force push (for generated content)
    """

def generate(root_dir: str, push: bool) -> list[Path]
    """
    Generate directory summaries and special summaries.
    Args:
        root_dir: Root directory to generate summaries for
        push: Whether to commit and push changes
    Returns:
        List of paths to generated summary files
    """

def main()
    """CLI entry point."""

```

## src/scripts/generate_summaries/generator.py
```python
class SummaryGenerator
    """Generate summary files for each directory in the project."""

    def __init__(self, root_dir: str | Path)
        """
        Initialize generator with root directory.
        Args:
            root_dir: Root directory to generate summaries for
        """

    def should_include_file(self, file_path: Path) -> bool
        """
        Determine if a file should be included in the summary.
        Args:
            file_path: Path to file to check
        Returns:
            True if file should be included in summary
        """

    def should_include_directory(self, directory: Path) -> bool
        """
        Determine if a directory should have a summary generated.
        Args:
            directory: Directory to check
        Returns:
            True if directory should have a summary
        """

    def _collect_directories(self) -> Set[Path]
        """
        Collect all directories containing files to summarize.
        Returns:
            Set of directory paths
        """

    def generate_directory_summary(self, directory: Path) -> str
        """
        Generate a summary for a single directory.
        Args:
            directory: Directory to generate summary for
        Returns:
            Generated summary text
        """

    def generate_all_summaries(self) -> List[Path]
        """
        Generate summary files for all directories.
        Returns:
            List of paths to generated summary files
        """


```

## src/scripts/generate_summaries/signature_extractor.py
```python
@dataclass
class Signature
    """Represents a Python function or class signature with documentation."""

class ParentNodeTransformer
    """Add parent references to all nodes in the AST."""

    def visit(self, node: Any) -> Any
        """Visit a node and add parent references to all its children."""


class SignatureExtractor
    """Extracts detailed signatures from Python files."""

    def get_type_annotation(self, node: Any) -> str
        """Convert AST annotation node to string representation."""

    def get_arg_string(self, arg: Any) -> str
        """Convert function argument to string with type annotation."""

    def extract_signatures(self, source: str) -> List[Signature]
        """Extract all function and class signatures from source code."""

    def format_signature(self, sig: Signature, indent: int) -> List[str]
        """Format a signature for display with proper indentation."""


def generate_python_summary(root_dir: str | Path) -> str
    """
    Generate enhanced Python project structure summary.
    Args:
        root_dir: Root directory of the project
    Returns:
        Formatted markdown string of Python signatures
    """

```

## src/scripts/generate_summaries/special_summaries.py
```python
class SpecialSummariesGenerator
    """Generate special project-wide summary files."""

    def __init__(self, root_dir: str | Path)
        """Initialize generator with root directory."""

    def _find_readmes(self, include_root: bool) -> List[Path]
        """Find all README files in the project."""

    def generate_special_summaries(self) -> List[Path]
        """
        Generate all special summary files.
        Returns:
            List of paths to generated summary files
        """


def generate_special_summaries(root_dir: str | Path) -> List[Path]
    """Generate special summaries for the project."""

```

## src/scripts/readme_generator.py
```python
def get_section_templates(template_dir: Path) -> List[str]
    """
    Get all section templates in proper order.
    Args:
        template_dir: Path to template directory containing sections/
    Returns:
        List of template names in desired order
    """

def generate_readme() -> None
    """Generate README from templates and commit changes"""

```

## src/scripts/registry/cli.py
```python
def build(input_path: str | Path, output_dir: str | Path, push: bool, branch: Optional[str]) -> None
    """
    Build registry from research YAML and generate outputs.
    Args:
        input_path: Path to research YAML file
        output_dir: Directory to save outputs (default: data directory)
        push: Whether to commit and push changes
        branch: Optional branch name to commit to (default: current branch)
    """

def cli()
    """CLI entry point."""

```

## src/scripts/registry/identifiers.py
```python
class MLRIdentifierRegistry
    """Manages unique identifiers for ML recommendations."""

    def __init__(self, registry_file: str | Path)
        """
        Initialize the identifier registry.
        Args:
            registry_file: Path to the JSON file storing ID mappings
        """

    def _load_registry(self) -> Dict[[str, Dict]]
        """Load existing MLR IDs from registry file."""

    def _initialize_author_counters(self) -> Dict[[str, int]]
        """Initialize counters for author IDs from existing registry."""

    def _save_registry(self) -> None
        """Save current MLR IDs to registry file."""

    def get_paper_id(self, first_author: str, year: int, arxiv_id: Optional[str]) -> str
        """
        Get or generate a paper identifier.
        Args:
            first_author: First author's name
            year: Publication year
            arxiv_id: Optional arXiv identifier
        Returns:
            Unique paper identifier string
        """

    def generate_id(self, year: int, paper_id: str) -> str
        """
        Generate a new unique MLR identifier.
        Args:
            year: Publication year
            paper_id: Unique paper identifier
        Returns:
            MLR identifier string
        """


```

## src/scripts/registry/io.py
```python
class RegistryDataError(Exception)
    """Raised when there are issues with registry data format."""

def validate_paper_entry(paper: Dict, year: str) -> None
    """
    Validate a single paper entry.
    Args:
        paper: Dictionary containing paper data
        year: Year the paper is from (for error messages)
    Raises:
        RegistryDataError: If paper data is invalid
    """

def load_research_yaml(file_path: Union[[str, Path]]) -> Dict
    """
    Load research data from YAML file.
    Args:
        file_path: Path to the YAML file
    Returns:
        Dictionary containing the research data
    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the file contains invalid YAML
        RegistryDataError: If the data format is invalid
    """

def save_registry(registry: RecommendationRegistry, output_file: Union[[str, Path]]) -> None
    """
    Save registry to a file.
    Args:
        registry: RecommendationRegistry instance
        output_file: Path where to save the file
    """

def load_registry(file_path: Union[[str, Path]]) -> Dict
    """
    Load a saved registry file.
    Args:
        file_path: Path to the registry file
    Returns:
        Dictionary containing the registry data
    """

def registry_to_markdown(registry: RecommendationRegistry, output_file: Union[[str, Path]]) -> None
    """Export registry to a markdown document."""

```

## src/scripts/registry/recommendations.py
```python
def generate_topic_id(topic: str, recommendation: str) -> str
    """Generate a unique topic-based ID for a recommendation."""

class RecommendationRegistry
    """Registry for ML training recommendations."""

    def __init__(self, id_registry: Optional[MLRIdentifierRegistry])
        """Initialize the recommendation registry."""

    def add_recommendation(self, topic: str, recommendation: str, first_author: str, source_paper: str, year: int, arxiv_id: Optional[str], experimental: bool, superseded_by: Optional[str], implementations: Optional[List[str]]) -> str
        """Add a recommendation to the registry."""

    def get_recommendation_by_mlr(self, mlr_id: str) -> Optional[Recommendation]
        """Get a recommendation by its MLR ID."""

    def get_recommendations_by_status(self, status: MLRStatus) -> List[Recommendation]
        """Get all recommendations with a given status."""

    def get_recommendations_by_topic(self, topic: str, status: Optional[MLRStatus]) -> List[Recommendation]
        """Get recommendations for a topic, optionally filtered by status."""

    def get_topics(self) -> Set[str]
        """Get all unique topics in the registry."""

    def export_registry(self) -> Dict
        """Export the registry as a list of atomic recommendations."""


def build_registry_from_yaml(yaml_data: Dict) -> RecommendationRegistry
    """Build a recommendation registry from YAML research data."""

```

## src/scripts/registry/types.py
```python
class MLRStatus(str, Enum)
    """Status states for ML recommendations."""

@dataclass
class Source
    """Source information for a recommendation."""

    @classmethod
    def from_dict(cls, data: Union[[Dict, DictConfig]]) -> 'Source'
        """Create Source from dictionary or DictConfig."""

    def to_dict(self) -> Dict
        """Convert to dictionary, omitting None values."""


@dataclass
class Evidence
    """Supporting evidence for a recommendation."""

    @classmethod
    def from_dict(cls, data: Union[[Dict, DictConfig]]) -> 'Evidence'
        """Create Evidence from dictionary or DictConfig."""

    def to_dict(self) -> Dict
        """Convert to dictionary, omitting None values."""


@dataclass
class Recommendation
    """ML training recommendation."""

    @classmethod
    def create(cls, id: str, recommendation: str, topic: str, topic_id: str, source: Union[[Dict, DictConfig, Source]], status: MLRStatus) -> 'Recommendation'
        """Create a recommendation from raw data."""

    def to_dict(self) -> Dict
        """Convert recommendation to dictionary."""


def create_config_from_dict(data: Dict) -> DictConfig
    """Create an OmegaConf config from a dictionary."""

```

## src/scripts/utils.py
```python
def get_project_root() -> Path
    """
    Get the project root directory by looking for pyproject.toml
    Returns the absolute path to the project root
    """

def load_config(config_path: str) -> dict
    """
    Load configuration from a TOML file
    Args:
        config_path (str): Path to the TOML configuration file relative to project root
    Returns:
        dict: Parsed configuration data
    """

def commit_and_push(paths: str | Path | list[str | Path], message: str | None, branch: str | None, base_branch: str | None, force: bool) -> None
    """
    Commit changes and push to specified or current branch.
    Args:
        paths: Path or list of paths to commit
        message: Commit message (defaults to "Update files via automated commit")
        branch: Branch to push to (defaults to current branch)
        base_branch: Optional base branch to create new branch from
        force: If True, create fresh branch and force push (for generated content)
    """

```

## tests/conftest.py
```python
def temp_dir()
    """Provide a clean temporary directory"""

def mock_repo(temp_dir)
    """Create a mock repository structure for testing"""

def sample_research_yaml() -> Dict
    """Sample research data for testing."""

def sample_yaml_file(tmp_path, sample_research_yaml)
    """Create a sample YAML file for testing."""

def id_registry(tmp_path)
    """Fixture providing a fresh identifier registry."""

def registry(id_registry)
    """Fixture providing a fresh recommendation registry."""

def populated_registry(registry, sample_research_yaml)
    """Fixture providing a registry populated with sample data."""

```

## tests/registry/test_identifiers.py
```python
def temp_registry_file(tmp_path)
    """Provide a temporary registry file path."""

def identifier_registry(temp_registry_file)
    """Provide a fresh identifier registry."""

def test_initialization(temp_registry_file)
    """Test registry initialization."""

def test_paper_id_generation(identifier_registry)
    """Test paper ID generation and consistency."""

def test_mlr_id_generation(identifier_registry)
    """Test MLR ID generation."""

def test_registry_persistence(temp_registry_file)
    """Test that registry state persists between instances."""

def test_special_character_handling(identifier_registry)
    """Test handling of special characters in author names."""

def test_invalid_registry_file(tmp_path)
    """Test handling of corrupted registry file."""

```

## tests/registry/test_io.py
```python
def sample_research_yaml(tmp_path)
    """Create a sample research YAML file."""

def sample_registry()
    """Create a sample registry with some recommendations."""

def test_load_research_yaml(sample_research_yaml)
    """Test loading research data from YAML."""

def test_load_research_yaml_invalid_year(tmp_path)
    """Test loading YAML with invalid year."""

def test_load_research_yaml_missing_fields(tmp_path)
    """Test loading YAML with missing required fields."""

def test_save_and_load_registry(sample_registry, tmp_path)
    """Test saving and loading registry."""

def test_load_registry_invalid_format(tmp_path)
    """Test loading invalid registry format."""

def test_registry_to_markdown(sample_registry, tmp_path)
    """Test markdown export."""

def test_nonexistent_file()
    """Test handling of nonexistent files."""

def test_invalid_yaml(tmp_path)
    """Test handling of invalid YAML."""

```

## tests/registry/test_recommendations.py
```python
def id_registry(tmp_path)
    """Fixture providing a fresh identifier registry."""

def registry(id_registry)
    """Fixture providing a fresh recommendation registry."""

def test_topic_id_generation()
    """Test topic ID generation."""

def test_add_standard_recommendation(registry)
    """Test adding a standard recommendation."""

def test_add_experimental_recommendation(registry)
    """Test adding an experimental recommendation."""

def test_add_deprecated_recommendation(registry)
    """Test adding a deprecated recommendation."""

def test_get_recommendations_by_status(registry)
    """Test filtering recommendations by status."""

def test_get_recommendations_by_topic(registry)
    """Test filtering recommendations by topic."""

def test_registry_export(registry)
    """Test registry export functionality."""

```

## tests/test_generate_readme.py
```python
def test_load_config(mock_repo)
    """Test configuration loading"""

def test_project_root(mock_repo, monkeypatch)
    """Test project root detection"""

```
