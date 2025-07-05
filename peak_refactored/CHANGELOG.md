# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Complete refactoring of original PEAK research prototype
- Modular Python package structure with proper separation of concerns
- Configuration management with environment variable support
- Comprehensive logging with structured output options
- Abstract interfaces for extensibility (BaseTagGenerator, etc.)
- Full test suite with pytest framework
- Development tools (pre-commit hooks, linting, formatting)
- CI/CD configuration with GitHub Actions
- Complete API documentation and user guides
- Command-line interface for training and inference
- Docker support for containerized deployment
- Performance optimizations and error handling
- Security improvements and input validation

### Changed
- Transformed Jupyter notebooks into modular Python classes
- Replaced hardcoded values with configurable parameters
- Improved error handling and logging throughout
- Enhanced data loading and processing pipelines
- Modernized dependencies and package management

### Removed
- Google Colab dependencies and hardcoded paths
- Duplicate code across notebooks
- Insecure credential handling

## [0.1.0] - Original Research Prototype

### Added
- Initial implementation as Jupyter notebooks
- Clarifai API integration for image tagging
- NMF topic extraction with TF-IDF
- Random Forest classification with SHAP explanations
- Four explanation categories implementation
- Basic visualization capabilities