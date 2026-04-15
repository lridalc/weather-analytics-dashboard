.PHONY: help all install install-dev dev run cli test test-smoke test-bootstrap test-unit test-integration test-cov lint format format-check type-check pre-commit check clean

# ============================================================================
# VARIABLES
# ============================================================================

UV_RUN := uv run
PYTEST := $(UV_RUN) pytest
GREEN := \033[0;32m
RED := \033[0;31m
YELLOW := \033[1;33m
NC := \033[0m # No Color

# ============================================================================
# DEFAULT
# ============================================================================

all: install-dev

# ============================================================================
# INSTALLING
# ============================================================================

# Install dependencies in the virtual environment
install:
	@echo "$(YELLOW)📦 Installing production dependencies...$(NC)"
	uv sync --no-dev
	@echo "$(GREEN)✅ Production dependencies installed!$(NC)"

# Install dependencies including development tools in the virtual environment
install-dev:
	@echo "$(YELLOW)📦 Installing development dependencies...$(NC)"
	uv sync
	@echo "$(GREEN)✅ Development dependencies installed!$(NC)"

# ============================================================================
# RUNNING
# ============================================================================

# Run the API server with hot reload
dev:
	@echo "$(YELLOW)🚀 Starting development server with hot reload...$(NC)"
	$(UV_RUN) uvicorn weather_analytics_dashboard.main:app --reload

# Run the API server without hot reload (for production)
run:
	@echo "$(YELLOW)🚀 Starting production server...$(NC)"
	$(UV_RUN) uvicorn weather_analytics_dashboard.main:app

# Run the CLI tool
cli:
	$(UV_RUN) weather

# ============================================================================
# TESTING
# ============================================================================

# Run smoke tests with verbose output
test-smoke:
	@echo "$(YELLOW)🧪 Running smoke tests...$(NC)"
	$(PYTEST) tests/integration/test_00_smoke.py -v

# Run bootstrap tests with verbose output
test-bootstrap:
	@echo "$(YELLOW)🧪 Running bootstrap tests...$(NC)"
	$(PYTEST) tests/integration/bootstrap -v

# Run unit tests with verbose output
test-unit:
	@echo "$(YELLOW)🧪 Running unit tests...$(NC)"
	$(PYTEST) tests/unit -v

# Run integration tests (ignore bootstrap tests) with verbose output
test-integration:
	@echo "$(YELLOW)🧪 Running integration tests...$(NC)"
	$(PYTEST) tests/integration --ignore=tests/integration/bootstrap -v

# Run all tests with verbose output
test:
	@echo "$(YELLOW)🧪 Running all tests...$(NC)"
	$(PYTEST) -v

# Run tests with coverage report
test-cov:
	@echo "$(YELLOW)🧪 Running tests with coverage...$(NC)"
	$(PYTEST) --cov=weather_analytics_dashboard --cov-report=html --cov-report=term-missing -v
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/index.html$(NC)"

# ============================================================================
# LINTING, FORMATTING AND TYPE CHECKING
# ============================================================================

# Run ruff linter
lint:
	@echo "$(YELLOW)🔍 Running linter...$(NC)"
	$(UV_RUN) ruff check .
	@echo "$(GREEN)✅ Linting passed!$(NC)"

# Run ruff formatter
format:
	@echo "$(YELLOW)✨ Formatting code...$(NC)"
	$(UV_RUN) ruff format .
	@echo "$(GREEN)✅ Code formatted!$(NC)"

# Run ruff formatter in check mode to verify formatting without making changes
format-check:
	@echo "$(YELLOW)✨ Checking code format...$(NC)"
	$(UV_RUN) ruff format . --check
	@echo "$(GREEN)✅ Format check passed!$(NC)"

# Run mypy type checking
type-check:
	@echo "$(YELLOW)🔍 Running type checker...$(NC)"
	$(UV_RUN) mypy .
	@echo "$(GREEN)✅ Type checking passed!$(NC)"

# ============================================================================
# GIT HOOKS
# ============================================================================

# Install pre-commit hooks
pre-commit:
	@echo "$(YELLOW)🔧 Installing pre-commit hooks...$(NC)"
	$(UV_RUN) pre-commit install
	@echo "$(GREEN)✅ Pre-commit hooks installed!$(NC)"

# ============================================================================
# COMPLETE CHECKING
# ============================================================================

# Run lint, format check, tests, and type check
check:
	@echo "$(YELLOW)🔍 Running all checks...$(NC)"
	@$(MAKE) lint
	@$(MAKE) format-check
	@$(MAKE) test
	@$(MAKE) type-check
	@echo "$(GREEN)✅ All checks passed!$(NC)"

# ============================================================================
# CLEANING
# ============================================================================

# Remove cache files and temporary directories
clean:
	@echo "$(YELLOW)🧹 Cleaning cache files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	@echo "$(GREEN)✅ All cache files cleaned!$(NC)"

# ============================================================================
# HELP
# ============================================================================

help:
	@echo "$(YELLOW)Available commands:$(NC)"
	@echo ""
	@echo "$(GREEN)Installation:$(NC)"
	@echo "  make install           - Install production dependencies"
	@echo "  make install-dev       - Install development dependencies"
	@echo ""
	@echo "$(GREEN)Running:$(NC)"
	@echo "  make dev               - Run API server with hot reload"
	@echo "  make run               - Run API server (production mode)"
	@echo "  make cli               - Run the CLI tool"
	@echo ""
	@echo "$(GREEN)Testing:$(NC)"
	@echo "  make test              - Run all tests"
	@echo "  make test-smoke        - Run smoke tests"
	@echo "  make test-bootstrap    - Run bootstrap tests"
	@echo "  make test-unit         - Run unit tests"
	@echo "  make test-integration  - Run integration tests"
	@echo "  make test-cov          - Run tests with coverage report"
	@echo ""
	@echo "$(GREEN)Code Quality:$(NC)"
	@echo "  make lint              - Run ruff linter"
	@echo "  make format            - Run ruff formatter"
	@echo "  make format-check      - Check code formatting"
	@echo "  make type-check        - Run mypy type checking"
	@echo ""
	@echo "$(GREEN)Git Hooks:$(NC)"
	@echo "  make pre-commit        - Install pre-commit hooks"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make check             - Run all checks (lint + format + test + type)"
	@echo "  make clean             - Remove cache and temporary files"
	@echo "  make help              - Show this help message"
	@echo ""