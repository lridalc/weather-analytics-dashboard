.PHONY: help all install install-dev dev run cli test test-smoke test-bootstrap test-unit test-integration test-cov lint format format-check type-check pre-commit pre-commit-force pre-commit-all pre-commit-run pre-commit-update pre-commit-uninstall check clean version release release-push

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

# Install pre-commit hooks with overwrite (useful when updating)
pre-commit-force:
	@echo "$(YELLOW)🔧 Force installing pre-commit hooks...$(NC)"
	$(UV_RUN) pre-commit install --force
	@echo "$(GREEN)✅ Pre-commit hooks force installed!$(NC)"

# Run pre-commit on all files (useful for initial setup or CI debugging)
pre-commit-all:
	@echo "$(YELLOW)🔍 Running pre-commit on all files...$(NC)"
	$(UV_RUN) pre-commit run --all-files
	@echo "$(GREEN)✅ Pre-commit checks passed on all files!$(NC)"

# Run a specific hook (example: make pre-commit-run HOOK=ruff)
HOOK ?=
pre-commit-run:
	@if [ -z "$(HOOK)" ]; then \
		echo "$(RED)❌ Please specify HOOK=hook-id$(NC)"; \
		echo "$(YELLOW)Example: make pre-commit-run HOOK=ruff$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)🔍 Running hook: $(HOOK)...$(NC)"
	$(UV_RUN) pre-commit run $(HOOK) --all-files

# Update pre-commit hooks to latest versions
pre-commit-update:
	@echo "$(YELLOW)🔄 Updating pre-commit hooks to latest versions...$(NC)"
	$(UV_RUN) pre-commit autoupdate
	@echo "$(GREEN)✅ Hooks updated! Review changes with: git diff .pre-commit-config.yaml$(NC)"

# Uninstall pre-commit hooks
pre-commit-uninstall:
	@echo "$(YELLOW)🗑️  Uninstalling pre-commit hooks...$(NC)"
	$(UV_RUN) pre-commit uninstall
	@echo "$(GREEN)✅ Pre-commit hooks uninstalled!$(NC)"

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
# RELEASE
# ============================================================================

VERSION ?=

# Show current version from pyproject.toml
version:
	@echo "$(YELLOW)Current version:$(NC) $(GREEN)$$(grep '^version = ' pyproject.toml | cut -d'"' -f2)$(NC)"

# Prepare release (reminder + optional auto-tag)
release:
	@echo "$(YELLOW)📦 Preparing release...$(NC)"
	@echo ""
	@echo "$(GREEN)📋 Release Checklist:$(NC)"
	@echo "  [ ] 1. Update version in pyproject.toml"
	@echo "  [ ] 2. Move [Unreleased] to [vX.Y.Z] in CHANGELOG.md"
	@echo "  [ ] 3. Add date to new version (YYYY-MM-DD)"
	@echo "  [ ] 4. Update roadmap in README.md"
	@echo "  [ ] 5. Run final checks: make check"
	@echo ""
	@echo "$(YELLOW)Current version:$(NC) $(GREEN)$$(grep '^version = ' pyproject.toml | cut -d'"' -f2)$(NC)"
	@echo ""
	@echo "$(YELLOW)Usage:$(NC)"
	@echo "  make release VERSION=0.2.0    # Auto-commit and tag after manual steps"
	@echo "  make release                   # Show this checklist only"
	@echo ""
	@if [ -n "$(VERSION)" ]; then \
		read -p "Have you completed steps 1-5 above? [y/N]: " confirm; \
		if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
			echo "$(YELLOW)📦 Creating commit and tag for v$(VERSION)...$(NC)"; \
			git add pyproject.toml CHANGELOG.md README.md; \
			git commit -m "chore(release): prepare v$(VERSION)" || echo "No changes to commit"; \
			git tag -a "v$(VERSION)" -m "feat: release v$(VERSION)"; \
			echo "$(GREEN)✅ Release v$(VERSION) prepared locally!$(NC)"; \
			echo ""; \
			echo "$(YELLOW)🚀 Next steps:$(NC)"; \
			echo "  make release-push"; \
		else \
			echo "$(RED)❌ Release cancelled. Complete checklist first.$(NC)"; \
		fi \
	fi

# Push release to remote
release-push:
	@echo "$(YELLOW)🚀 Pushing to remote...$(NC)"
	git push origin main --tags
	@echo "$(GREEN)✅ Release published!$(NC)"

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
	@echo "  make pre-commit         		- Install pre-commit hooks"
	@echo "  make pre-commit-force  		- Force reinstall pre-commit hooks"
	@echo "  make pre-commit-all     		- Run all hooks on all files"
	@echo "  make pre-commit-run HOOK=ruff  - Run specific hook"
	@echo "  make pre-commit-update  		- Update hooks to latest versions"
	@echo "  make pre-commit-uninstall 		- Uninstall pre-commit hooks"
	@echo ""
	@echo "$(GREEN)Utilities:$(NC)"
	@echo "  make check             - Run all checks (lint + format + test + type)"
	@echo "  make clean             - Remove cache and temporary files"
	@echo "$(GREEN)Release:$(NC)"
	@echo "  make release [VERSION=X.Y.Z]	- Prepare a new release"
	@echo "  make release-push            	- Push release to remote"
	@echo "  make version                 	- Show current version"
	@echo "  make help              		- Show this help message"
	@echo ""
