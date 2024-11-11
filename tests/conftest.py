import pytest
from pathlib import Path
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    """Provide a clean temporary directory"""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)

@pytest.fixture
def mock_repo(temp_dir):
    """Create a mock repository structure for testing"""
    # Create basic structure
    docs_dir = temp_dir / "docs" / "readme" / "sections"
    src_dir = temp_dir / "src" / "readme_generator"
    
    docs_dir.mkdir(parents=True)
    src_dir.mkdir(parents=True)
    
    # Create mock files
    (docs_dir / "introduction.md.j2").write_text("## Introduction\n{{ test }}")
    (temp_dir / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "0.1.0"

[tool.readme]
test = "Test Value"
    """)
    
    return temp_dir
