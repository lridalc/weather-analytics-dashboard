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

# Run the API server without hot reload (for production)
run:
	uv run uvicorn weather_analytics_dashboard.main:app

# Run the CLI tool
cli:
	uv run weather


# Run smoke tests with verbose output
test-smoke:
	uv run pytest tests/integration/test_00_smoke.py -v

# Run bootstrap tests with verbose output
test-bootstrap:
	uv run pytest tests/integration/bootstrap -v

# Run unit tests with verbose output
test-unit:
	uv run pytest tests/unit -v

# Run integration tests (ignore bootstrap tests) with verbose output
test-integration:
	uv run pytest tests/integration --ignore=tests/integration/bootstrap -v

# Run all tests with verbose output
test:
	uv run pytest -v

# Run ruff linter
lint:
	uv run ruff check .

# Run ruff formatter
format:
	uv run ruff format .

# Run ruff formatter in check mode to verify formatting without making changes
format-check:
	uv run ruff format . --check

# Run mypy type checking
type-check:
	uv run mypy .

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
	@echo "  make install          	 - Install dependencies in the virtual environment"
	@echo "  make install-dev      	 - Install dependencies including development tools"
	@echo "  make dev              	 - Run API server with hot reload"
	@echo "  make run              	 - Run API server without hot reload (production)"
	@echo "  make cli              	 - Run the CLI tool"
	@echo "  make test-smoke       	 - Run smoke tests with verbose output"
	@echo "  make test-bootstrap   	 - Run bootstrap tests with verbose output"
	@echo "  make test-unit        	 - Run unit tests with verbose output"
	@echo "  make test-integration 	 - Run integration tests (ignore bootstrap) with verbose output"
	@echo "  make test         		 - Run all tests"
	@echo "  make lint         		 - Run ruff linter"
	@echo "  make format       		 - Run ruff formatter"
	@echo "  make format-check 		 - Run ruff formatter in check mode"
	@echo "  make type-check   		 - Run mypy type checking"
	@echo "  make check        		 - Run lint + format check + tests + type check"
	@echo "  make clean        		 - Remove cache files"