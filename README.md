# 

# Anthology of the SOTA

Why we -- AI/ML researchers and practitioners -- do the things that we do, and why we do those things the way that we do them.

You might also be interested in my list of significantly impactful works that has more of a historical perspective: https://github.com/dmarx/anthology-of-modern-ml

The main difference here is that where that prior list was focused on big, impactful works, including those which no longer reflect best practice, this list is focused entirely on whatever the current best practice is understood to be and explaining the justification behind that design choice. Where my `Modern ML` anthology focused on paradigm shifts and made no space for important but comparatively "small" (with respect to paradigmatic impact) incremental improvements, I expect this space to be dominated by incremental works. Additional, because the other list operates as a kind of "hall of fame", it generally should not experience churn. This list however, I plan to maintain as a living document with an "attic" in which to deprecate former best practices that have been supplanted.
## Development Guidelines

### Code Organization for LLM Interaction

When developing this project (or using it as a template), keep in mind these guidelines for effective collaboration with Large Language Models:

1. **File Length and Modularity**
   - Keep files short and focused on a single responsibility
   - If you find yourself using comments like "... rest remains the same" or "... etc", the file is too long
   - Files should be completely replaceable in a single LLM interaction
   - Long files should be split into logical components

2. **Dependencies**
   - All dependencies managed in `pyproject.toml`
   - Optional dependencies grouped by feature:
     ```toml
     [project.optional-dependencies]
     test = ["pytest", ...]
     site = ["markdown2", ...]
     all = ["pytest", "markdown2", ...]  # Everything
     ```
   - Use appropriate groups during development:
     ```bash
     pip install -e ".[test]"  # Just testing
     pip install -e ".[all]"   # Everything
     ```

3. **Testing Standards**
   - Every new feature needs tests
   - Write tests before starting on new features to formalize expected behavior (i.e. TDD)
   - Tests should be clear and focused
   - Use pytest fixtures for common setups
   - All workflows depend on tests passing
   - Test files should follow same modularity principles
   - Use `pytest` fixtures for common setups
   - Keep tests focused and well-documented

4. **Why This Matters**
   - LLMs work best with clear, focused contexts
   - Complete file contents are better than partial updates with ellipsis
   - Tests provide clear examples of intended behavior
   - Shorter files make it easier for LLMs to:
     - Understand the complete context
     - Suggest accurate modifications
     - Maintain consistency
     - Avoid potential errors from incomplete information

5. **Best Practices**
   - Aim for files under 200 lines
   - Each file should have a single, clear purpose
   - Use directory structure to organize related components
   - Prefer many small files over few large files
   - Consider splitting when files require partial updates

6. **Project Conventions**
   - Use `loguru` for all logging
   - Use `fire` for CLI interfaces
   - use `omegaconf` for yaml
   - Prefer `pathlib` for file system operations
   - Type hints should use:
     - Built-in generics over typing module (PEP 585)
     - Union operator (`|`) over Optional (PEP 604)
   - Github Actions is the only available runtime for script execution
   - All workflows depend on tests passing
   - Syntax permitting, all files should begin with a comment detailing the current file's name and relative path within the project
