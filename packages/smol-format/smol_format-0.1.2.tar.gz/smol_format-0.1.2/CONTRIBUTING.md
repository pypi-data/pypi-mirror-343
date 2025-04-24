# Contributing to smol-format

Thank you for your interest in contributing to smol-format! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/smol-data/smol-format.git
   cd smol-format
   ```
3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use type hints for all function parameters and return values
- Keep functions focused and small
- Write docstrings for all public functions and classes

### Testing

- Write tests for all new functionality
- Ensure all tests pass:
  ```bash
  pytest
  ```
- Maintain or improve test coverage:
  ```bash
  pytest --cov=smol_format
  ```

### Documentation

- Update docstrings for any modified code
- Update README.md if adding new features
- Add examples for new functionality

### Pull Request Process

1. Create a new branch for your feature/fix
2. Make your changes
3. Run tests and ensure they pass
4. Update documentation
5. Submit a pull request

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

## Project Structure

```
smol-format/
├── smol_format/       # Main package
│   ├── __init__.py     # Package initialization
│   └── core.py         # Core functionality
├── tests/             # Test files
├── examples/          # Example scripts
├── docs/              # Documentation
├── pyproject.toml     # Project configuration
├── README.md          # Project documentation
├── LICENSE            # MIT License
└── CONTRIBUTING.md    # This file
```

## Questions?

Feel free to open an issue for any questions or concerns.