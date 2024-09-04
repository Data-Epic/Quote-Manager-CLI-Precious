# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make help          - Show this message"
	@echo "  make setup         - Setup environment"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linter"
	@echo "  make format        - Format code"
	@echo "  make install       - Install dependencies"
	@echo "  make clean         - Clean up"
	@echo "  make type_check	- Run mypy to type check"
	@echo "  make build     	- Build the package"
	@echo "  make publish   	- Publish the package"
	@echo "  make all_checks    - Run tests,  formatter, type check, linter, and clean"

# Setup environment
.PHONY: setup
setup:
	poetry shell
	poetry install
	wget https://raw.githubusercontent.com/shravan20/github-readme-quotes/main/customQuotes/category.json

# Install dependencies
.PHONY: install
install:
	poetry install

# Update dependencies
.PHONY: update
update:
	poetry update

# Run tests
.PHONY: test
test:
	poetry run pytest

# Run linter
.PHONY: lint
lint:
	poetry run flake8 quote_manager_cli

# Format code
.PHONY: format
format:
	poetry run black quote_manager_cli

# Run mypy
.PHONY: type_check
type_check:
	poetry run mypy -p quote_manager_cli

# Clean up
.PHONY: clean
clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf .coverage
	@rm -rf htmlcov

# Run all checks
.PHONY: all_checks
all_checks: test format type_check lint clean
