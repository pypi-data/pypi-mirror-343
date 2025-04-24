# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.2] - 2024-04-23

### Added
- Development environment setup script (`scripts/setup_dev.sh`)
- Docker development environment configuration
- GitHub Actions workflow for CI/CD
- Pre-commit hooks configuration
- Additional development tools (bandit, pytest-asyncio, pytest-xdist, hypothesis)

### Changed
- Updated pyproject.toml with improved development tool configurations
- Simplified build system to use hatchling
- Updated line length to 100 characters for better readability
- Improved mypy configuration for stricter type checking

### Fixed
- Fixed TOML syntax errors in pyproject.toml
- Fixed virtual environment setup issues

## [0.1.1] - 2024-04-23

### Added
- Initial release of smol-format
- Basic data encoding and decoding functionality
- Support for large rational numbers
- Example usage documentation

[Unreleased]: https://github.com/smol-data/smol-format/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/smol-data/smol-format/releases/tag/v0.1.2
[0.1.1]: https://github.com/smol-data/smol-format/releases/tag/v0.1.1

## [0.1.0] - 2025-04-23

### Added
- Initial release
- Core DenseStorage implementation
- JSON encoding with Zstandard compression
- Exact rational number preservation
- Metadata tracking
- Streaming support
- Basic examples and documentation

### Changed
- Simplified architecture to focus on exact number preservation
- Removed PyArrow dependency
- Streamlined API for better usability

### Removed
- PyArrow-based optimization
- Complex type system
- BSD-specific test files
- Outdated test implementations