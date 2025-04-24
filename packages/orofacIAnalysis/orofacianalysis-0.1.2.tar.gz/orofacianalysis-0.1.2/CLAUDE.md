# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Test Commands
- Install package: `pip install -e .`
- Run all tests: `pytest`
- Run unit tests: `pytest tests/unit/`
- Run integration tests: `pytest tests/integration/`
- Run single test: `pytest tests/path/to/test_file.py::TestClass::test_function`
- Generate coverage report: `pytest --cov=orofacIAnalysis`
- Setup test environment: `python setup_test_env.py --setup`

## Code Style Guidelines
- **Imports**: Group in order: standard lib, external packages, local modules
- **Docstrings**: Google style docstrings with Args, Returns, Raises sections
- **Types**: No formal type annotations but use clear docstrings for types
- **Naming**: snake_case for methods/variables, CamelCase for classes
- **Comments**: Use for complex logic, not obvious code
- **Error handling**: Raise specific exceptions with clear error messages
- **Classes**: Clear class docstrings describing purpose and behavior
- **Method size**: Keep methods focused on single responsibility
- **Formatting**: 4-space indentation, max line length ~100 characters
- **Constants**: Use UPPERCASE for constants and class-level constants