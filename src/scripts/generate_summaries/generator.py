"""Core summary generation functionality."""
from pathlib import Path
from typing import List, Set
from loguru import logger

class SummaryGenerator:
    """Generate summary files for each directory in the project."""
    
    def __init__(self, root_dir: str | Path):
        """Initialize generator with root directory.
        
        Args:
            root_dir: Root directory to generate summaries for
        """
        self.root_dir = Path(root_dir)
        
    def should_include_file(self, file_path: Path) -> bool:
        """Determine if a file should be included in the summary.
        
        Args:
            file_path: Path to file to check
            
        Returns:
            True if file should be included in summary
        """
        # Skip common files we don't want to summarize
        excluded_files = {
            '.git', '.gitignore', '.pytest_cache', '__pycache__',
            'SUMMARY', '.coverage', '.env', '.venv', '.idea', '.vscode'
        }
        
        # Skip excluded directories and files
        if any(part in excluded_files for part in file_path.parts):
            return False
            
        # Skip .github/workflows directory
        if '.github/workflows' in str(file_path):
            return False
            
        # Only include text files
        text_extensions = {'.py', '.md', '.txt', '.yml', '.yaml', '.toml', 
                         '.json', '.html', '.css', '.js', '.j2'}
        return file_path.suffix in text_extensions
    
    def should_include_directory(self, directory: Path) -> bool:
        """Determine if a directory should have a summary generated.
        
        Args:
            directory: Directory to check
            
        Returns:
            True if directory should have a summary
        """
        # Skip .github/workflows directory
        if '.github/workflows' in str(directory):
            return False
            
        # Skip other excluded directories
        excluded_dirs = {
            '.git', '__pycache__', '.pytest_cache',
            '.venv', '.idea', '.vscode'
        }
        
        return not any(part in excluded_dirs for part in directory.parts)
    
    def _collect_directories(self) -> Set[Path]:
        """Collect all directories containing files to summarize.
        
        Returns:
            Set of directory paths
        """
        directories = set()
        for file_path in self.root_dir.rglob('*'):
            if (file_path.is_file() and 
                self.should_include_file(file_path) and
                self.should_include_directory(file_path.parent)):
                directories.add(file_path.parent)
        return directories
        
    def generate_directory_summary(self, directory: Path) -> str:
        """Generate a summary for a single directory.
        
        Args:
            directory: Directory to generate summary for
            
        Returns:
            Generated summary text
        """
        logger.debug(f"Generating summary for {directory}")
        summary = []
        
        # Process all files in the directory
        for file_path in sorted(directory.rglob('*')):
            if not file_path.is_file() or not self.should_include_file(file_path):
                continue
                
            try:
                # Get relative path from root for the header
                rel_path = file_path.relative_to(self.root_dir)
                
                # Read file content
                content = file_path.read_text(encoding='utf-8')
                
                # Add to summary with clear separation
                summary.extend([
                    '=' * 80,
                    f'File: {rel_path}',
                    '=' * 80,
                    content,
                    '\n'  # Extra newline for separation
                ])
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                
        return '\n'.join(summary)
        
    def generate_all_summaries(self) -> List[Path]:
        """Generate summary files for all directories.
        
        Returns:
            List of paths to generated summary files
        """
        logger.info("Starting summary generation")
        summary_files = []
        
        # Collect directories
        directories = self._collect_directories()
        logger.info(f"Found {len(directories)} directories to process")
        
        # Generate summaries
        for directory in sorted(directories):
            if not self.should_include_directory(directory):
                continue
                
            summary_content = self.generate_directory_summary(directory)
            summary_path = directory / 'SUMMARY'
            
            try:
                summary_path.write_text(summary_content, encoding='utf-8')
                logger.info(f"Generated summary for {directory}")
                summary_files.append(summary_path)
            except Exception as e:
                logger.error(f"Error writing summary for {directory}: {e}")
                
        return summary_files
