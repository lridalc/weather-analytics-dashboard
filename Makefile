.PHONY: dev test lint format clean check type-check help

# Install dependencies in the virtual environment
install:
	uv sync --no-dev

# Install dependencies including development tools in the virtual environment
install-dev:
	uv sync

# Run the API server with hot reload
dev:
	uv run uvicorn weather_analytics_dashboard.main:app --reload

# Run all tests with verbose output
test:
	uv run pytest tests/ -v

# Run ruff linter on the src/ directory
lint:
	uv run ruff check src/

# Run ruff formatter on the src/ directory
format:
	uv run ruff format src/

# Run ruff formatter in check mode to verify formatting without making changes
format-check:
	uv run ruff format src/ --check

# Run mypy type checking on src/ and tests/ directories
type-check:
	uv run mypy src/ tests/

# Run lint, format check, and tests
check: lint format-check test type-check
	@echo "✅ All checks passed!"

# Remove __pycache__ directories and .pyc files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache .ruff_cache

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies in the virtual environment"
	@echo "  make install-dev  - Install dependencies including development tools"
	@echo "  make dev          - Run API server with hot reload"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run ruff linter"
	@echo "  make format       - Run ruff formatter"
	@echo "  make format-check - Run ruff formatter in check mode"
	@echo "  make type-check   - Run mypy type checking"
	@echo "  make check        - Run lint + format check + tests + type check"
	@echo "  make clean        - Remove cache files"