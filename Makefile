.PHONY: help all install install-dev dev run cli test test-smoke test-bootstrap test-unit test-integration test-cov lint format format-check type-check pre-commit pre-commit-force pre-commit-all pre-commit-run pre-commit-update pre-commit-uninstall check clean version release

.DEFAULT_GOAL := all

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

# Run all tests with verbose output
test:
	@echo "$(YELLOW)🧪 Running all tests...$(NC)"
	$(PYTEST) -v

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

# Run tests with coverage report with verbose output
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

# Run ruff formatter in diff mode to show formatting differences without applying changes
format-diff:
	@echo "$(YELLOW)📝 Showing formatting differences...$(NC)"
	@$(UV_RUN) ruff format . --diff
	@echo "$(YELLOW)---$(NC)"
	@echo "$(YELLOW)💡 Run 'make format' to apply these changes$(NC)"

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

# Complete release (reminder + prepare + auto-tag + push + sync + cleanup)
release:
	@echo "$(YELLOW)📦 Preparing release...$(NC)"
	@echo ""
	@# Show steps always (with or without VERSION)
	@echo "$(GREEN)📋 What 'make release VERSION=X.Y.Z' will do:$(NC)"
	@echo "  1. Check if already on a release branch"
	@echo "     - If YES: commit pending changes and proceed to merge"
	@echo "     - If NO: verify clean working tree and develop branch, then create release branch"
	@echo "  2. Show checklist for manual steps (update CHANGELOG, pyproject.toml, README, etc.)"
	@echo "  3. Wait for user confirmation [y/N]"
	@echo "  4. Commit changes in release branch"
	@echo "  5. Merge release branch to main"
	@echo "  6. Create and push tag vX.Y.Z"
	@echo "  7. Merge main back to develop"
	@echo "  8. Delete release branch locally"
	@echo "  9. Push everything to remote"
	@echo ""
	@echo "$(YELLOW)Current version:$(NC) $(GREEN)$$(grep '^version = ' pyproject.toml | cut -d'"' -f2)$(NC)"
	@echo ""
	@echo "$(YELLOW)Usage:$(NC)"
	@echo "  make release VERSION=0.2.0    	# Execute release process"
	@echo "  make release                   # Show this info and steps"
	@echo ""
	@# Check if VERSION is provided
	@if [ -z "$(VERSION)" ]; then \
		echo "$(YELLOW)💡 Tip: Run 'make release' without VERSION to see this anytime$(NC)"; \
		echo "$(RED)❌ No version provided. Nothing to execute.$(NC)"; \
		exit 0; \
	fi
	@# Check if tag already exists
	@if git rev-parse "v$(VERSION)" > /dev/null 2>&1; then \
		echo "$(RED)❌ Tag v$(VERSION) already exists$(NC)"; \
		exit 1; \
	fi
	@# Get current branch and handle logic
	@current_branch=$$(git branch --show-current); \
	if [ "$$current_branch" = "develop" ]; then \
		if [ -n "$$(git status --porcelain)" ]; then \
			echo "$(RED)❌ Working tree has uncommitted changes. Commit or stash first.$(NC)"; \
			exit 1; \
		fi; \
		echo "$(YELLOW)📦 Creating release branch release/v$(VERSION)...$(NC)"; \
		git checkout -b release/v$(VERSION); \
		echo ""; \
		echo "$(GREEN)📋 Release Checklist:$(NC)"; \
		echo "  [ ] 1. Update version to $(VERSION) in pyproject.toml"; \
		echo "  [ ] 2. Move [Unreleased] to [v$(VERSION)] in CHANGELOG.md"; \
		echo "  [ ] 3. Add date to new version (YYYY-MM-DD)"; \
		echo "  [ ] 4. Update roadmap in README.md"; \
		echo "  [ ] 5. Run final checks: make check"; \
		echo ""; \
		echo "$(YELLOW)💡 Make the changes above, then run: make release VERSION=$(VERSION)$(NC)"; \
		echo "$(YELLOW)   (You are now on branch release/v$(VERSION))$(NC)"; \
		exit 0; \
	elif echo "$$current_branch" | grep -q "^release/"; then \
		echo "$(YELLOW)📌 Already on release branch: $$current_branch$(NC)"; \
		echo ""; \
		echo "$(GREEN)📋 Release Checklist:$(NC)"; \
		echo "  [ ] 1. Version updated to $(VERSION) in pyproject.toml?"; \
		echo "  [ ] 2. [Unreleased] moved to [v$(VERSION)] in CHANGELOG.md?"; \
		echo "  [ ] 3. Date added to new version (YYYY-MM-DD)?"; \
		echo "  [ ] 4. Roadmap updated in README.md?"; \
		echo "  [ ] 5. Final checks passed: make check?"; \
		echo ""; \
		read -p "Have you completed all steps above? [y/N]: " confirm; \
		if [ "$$confirm" != "y" ] && [ "$$confirm" != "Y" ]; then \
			echo "$(RED)❌ Release cancelled. Complete checklist first.$(NC)"; \
			exit 1; \
		fi; \
		if [ -n "$$(git status --porcelain)" ]; then \
			echo "$(YELLOW)💾 Committing pending changes...$(NC)"; \
			git add .; \
			git commit -m "chore(release): prepare v$(VERSION)"; \
			echo "$(GREEN)✅ Changes committed$(NC)"; \
		else \
			echo "$(YELLOW)⚠️  No changes detected. Assuming already committed.$(NC)"; \
			read -p "Continue anyway? [y/N]: " continue_anyway; \
			if [ "$$continue_anyway" != "y" ] && [ "$$continue_anyway" != "Y" ]; then \
				echo "$(RED)❌ Release cancelled.$(NC)"; \
				exit 1; \
			fi; \
		fi; \
	else \
		echo "$(RED)❌ You must be on 'develop' or a 'release/*' branch. Current: $$current_branch$(NC)"; \
		exit 1; \
	fi
	@# Continue with merge and tag process (only reached if already on release branch)
	@echo "$(YELLOW)🔀 Merging release/v$(VERSION) to main...$(NC)"
	git switch main
	SKIP=no-commit-to-branch git merge --no-ff release/v$(VERSION) -m "chore(release): merge release/v$(VERSION) into main for v$(VERSION)"
	@echo "$(YELLOW)🏷️  Creating tag v$(VERSION)...$(NC)"
	@if [ -n "$$CI" ]; then \
		git tag -a "v$(VERSION)" -m "feat: release v$(VERSION)"; \
	else \
		git tag -a "v$(VERSION)" -m "feat: release v$(VERSION)" -e; \
	fi
	@echo "$(YELLOW)🔄 Merging main back to develop...$(NC)"
	git switch develop
	git merge --no-ff main -m "chore(release): sync develop with main after v$(VERSION)"
	@echo "$(YELLOW)🚀 Pushing to remote...$(NC)"
	git push origin main develop --tags
	@echo "$(YELLOW)🧹 Cleaning up local release branch...$(NC)"
	git branch -d release/v$(VERSION)
	@echo ""
	@echo "$(GREEN)🎉 Release v$(VERSION) completed successfully!$(NC)"
	@echo ""
	@echo "$(YELLOW)📌 Summary:$(NC)"
	@echo "  ✅ main and develop pushed to origin"
	@echo "  ✅ tag v$(VERSION) created and pushed"
	@echo "  ✅ release/v$(VERSION) branch deleted locally"
	@echo "  ✅ Back on develop branch"

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
	@echo ""
	@echo "$(GREEN)Release:$(NC)"
	@echo "  make release [VERSION=X.Y.Z]	- Prepare a new release and push to remote"
	@echo "  make version                 	- Show current version"
	@echo ""
	@echo "make help				- Show this help message"
	@echo ""
