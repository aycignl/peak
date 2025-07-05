.PHONY: help install install-dev test lint format type-check docs clean build

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install the package
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -e ".[dev,test]"
	pre-commit install

test:  ## Run tests
	pytest tests/ -v --cov=peak --cov-report=html --cov-report=term

test-fast:  ## Run tests without coverage
	pytest tests/ -v

lint:  ## Run linting checks
	flake8 src/peak tests/
	mypy src/peak/

format:  ## Format code
	black src/peak tests/
	isort src/peak tests/

format-check:  ## Check code formatting
	black --check src/peak tests/
	isort --check-only src/peak tests/

type-check:  ## Run type checking
	mypy src/peak/

docs:  ## Build documentation
	cd docs && make html

docs-serve:  ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python -m build

security:  ## Run security checks
	bandit -r src/peak/
	safety check

pre-commit:  ## Run all pre-commit checks
	pre-commit run --all-files

setup-dev:  ## Set up development environment
	@echo "Setting up development environment..."
	$(MAKE) install-dev
	@echo "Creating .env file from template..."
	@if [ ! -f .env ]; then cp .env.template .env; fi
	@echo "Development environment ready!"
	@echo "Please edit .env file with your actual configuration values."