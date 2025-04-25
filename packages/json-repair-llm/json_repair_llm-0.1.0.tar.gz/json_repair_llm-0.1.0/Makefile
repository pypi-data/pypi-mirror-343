library_dir = $(shell pwd)
ENV_FILE := $(firstword $(wildcard $(library_dir)/*.env))
ENV_FILE_WO_EXT := $(basename $(ENV_FILE))
PYTHON := python3
UV := $(shell command -v uv 2> /dev/null)
VERSION := $(shell $(PYTHON) -c "from importlib.metadata import version; print(version('$(shell basename $(library_dir))'))" 2>/dev/null || echo "unknown")

# Colors for prettier output
BLUE := \033[1;34m
GREEN := \033[1;32m
YELLOW := \033[1;33m
RED := \033[1;31m
NC := \033[0m # No Color

ifneq (,$(wildcard $(ENV_FILE)))
    include $(ENV_FILE)
    $(info $(GREEN)Loading environment from $(ENV_FILE)$(NC))
else
    $(warning $(YELLOW)Environment file $(ENV_FILE) not found in $(library_dir), using default environment$(NC))
endif

# Check if we're in a virtual environment
ifeq ($(shell $(PYTHON) -c "import sys; print(int(hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)))"),0)
    $(warning $(YELLOW)Not running in a virtual environment. Consider activating one with 'make init' first.$(NC))
endif

all: help

.PHONY: help init types lint format unit_tests check-release build release install install_dev sync clean version

.SILENT: help
help:
	@echo "$(BLUE)Available targets:$(NC)"
	@echo "$(GREEN)make init$(NC)         - Init the local virtual environment (create if not exists)"
	@echo "$(GREEN)make reinit$(NC)       - Re-create the local virtual environment from scratch"
	@echo "$(GREEN)make types$(NC)        - Run mypy for type checking"
	@echo "$(GREEN)make lint$(NC)         - Run linting (flake8 and ruff)"
	@echo "$(GREEN)make format$(NC)       - Format code using black and isort"
	@echo "$(GREEN)make unit_tests$(NC)   - Run unit tests"
	@echo "$(GREEN)make check-release$(NC)- Run tests, lint, and type checks for release readiness"
	@echo "$(GREEN)make build$(NC)        - Build the package (sdist and wheel)"
	@echo "$(GREEN)make release$(NC)      - Create a release (build, tag, and push)"
	@echo "$(GREEN)make install$(NC)      - Install package requirements"
	@echo "$(GREEN)make install_dev$(NC)  - Install package with development requirements"
	@echo "$(GREEN)make sync$(NC)         - Sync requirements"
	@echo "$(GREEN)make clean$(NC)        - Remove build artifacts and cache files"
	@echo "$(GREEN)make version$(NC)      - Display the current package version"
	@echo ""
	@echo "Current package version: $(VERSION)"
	@echo ""

# Create local virtual environment if it doesn't exist
init:
	@echo "$(BLUE)Checking virtual environment...$(NC)"
	@# Check if uv is installed, if not install it
	@if [ -z "$(UV)" ]; then \
		echo "$(YELLOW)Installing uv package manager...$(NC)"; \
		$(PYTHON) -m pip install --upgrade uv; \
	fi
	@if [ ! -d "$(library_dir)/.venv" ]; then \
		echo "$(BLUE)Creating virtual environment...$(NC)"; \
		$(PYTHON) -m venv $(library_dir)/.venv; \
		echo "$(BLUE)Installing dependencies...$(NC)"; \
		. $(library_dir)/.venv/bin/activate && \
		uv pip install --upgrade pip && \
		uv pip install -e ".[dev]" && \
		echo "$(GREEN)Virtual environment created and dependencies installed.$(NC)" && \
		echo "$(YELLOW)Activate it with: source $(library_dir)/.venv/bin/activate$(NC)"; \
	else \
		echo "$(GREEN)Virtual environment already exists.$(NC)"; \
		echo "$(YELLOW)Activate it with: source $(library_dir)/.venv/bin/activate$(NC)"; \
		echo "$(YELLOW)To reinstall from scratch, use: make reinit$(NC)"; \
	fi

# Re-create local virtual environment from scratch
reinit:
	@echo "$(BLUE)Re-creating virtual environment from scratch...$(NC)"
	@# Check if uv is installed, if not install it
	@if [ -z "$(UV)" ]; then \
		echo "$(YELLOW)Installing uv package manager...$(NC)"; \
		$(PYTHON) -m pip install --upgrade uv; \
	fi
	@echo "$(BLUE)Removing existing environment...$(NC)"
	@rm -rf $(library_dir)/.venv
	@$(PYTHON) -m venv $(library_dir)/.venv
	@echo "$(BLUE)Activating environment and installing dependencies...$(NC)"
	@. $(library_dir)/.venv/bin/activate && \
	uv pip install --upgrade pip && \
	uv pip install -e ".[dev]" && \
	echo "$(GREEN)Virtual environment created and dependencies installed.$(NC)" && \
	echo "$(YELLOW)Activate it with: source $(library_dir)/.venv/bin/activate$(NC)"

# Run type checking using mypy
types:
	@echo "$(BLUE)Running type checks...$(NC)"
	@$(PYTHON) -m mypy --config $(library_dir)/pyproject.toml $(library_dir)

# Run linting (flake8 and ruff)
lint:
	@echo "$(BLUE)Running linting tests (with auto-fix)...$(NC)"
	@$(PYTHON) -m ruff check $(library_dir)

# Format code
format:
	@echo "$(BLUE)Formatting code...$(NC)"
	@$(PYTHON) -m ruff format $(library_dir)
	@echo "$(GREEN)Code formatting complete.$(NC)"

# Run unit tests
unit_tests:
	@echo "$(BLUE)Running unit tests...$(NC)"
	@$(PYTHON) -m pytest --maxfail=1 --disable-warnings -q

# Check for release readiness
check-release: lint types unit_tests
	@echo "$(GREEN)All checks passed. Ready for release.$(NC)"

# Build package (sdist & wheel)
build:
	@echo "$(BLUE)Building the package...$(NC)"
	@$(PYTHON) -m pip install --upgrade build
	@rm -rf dist build *.egg-info
	@$(PYTHON) -m build
	@echo "$(GREEN)Build complete. Artifacts in ./dist/$(NC)"

# Display current version
version:
	@echo "$(BLUE)Current package version:$(NC) $(VERSION)"

# Install package (using pyproject.toml dependencies)
install:
	@echo "$(BLUE)Installing package requirements...$(NC)"
	@if [ -z "$(UV)" ]; then \
		$(PYTHON) -m pip install --upgrade uv --no-cache-dir; \
	fi
	@uv pip install -r pyproject.toml --no-cache-dir -U
	@uv pip install -e .

# Install package with development requirements
install_dev:
	@echo "$(BLUE)Installing package with dev requirements...$(NC)"
	@if [ -z "$(UV)" ]; then \
		$(PYTHON) -m pip install --upgrade uv --no-cache-dir; \
	fi
	@uv pip install -r pyproject.toml --no-cache-dir -U
	@uv pip install -e ".[dev]"

# Sync requirements using uv
sync:
	@echo "$(BLUE)Syncing requirements...$(NC)"
	@if [ -z "$(UV)" ]; then \
		$(PYTHON) -m pip install --upgrade uv --no-cache-dir; \
	fi
	@uv pip sync pyproject.toml

# Clean build artifacts and cache files
clean:
	@echo "$(BLUE)Cleaning build artifacts and cache files...$(NC)"
	@rm -rf dist build *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name .pytest_cache -exec rm -rf {} +
	@find . -type d -name .mypy_cache -exec rm -rf {} +
	@find . -type d -name .ruff_cache -exec rm -rf {} +
	@echo "$(GREEN)Clean complete.$(NC)"

# Create a release
# Steps: check release, build, then push changes and tag release.
release: check-release build
	@echo "$(BLUE)Creating release...$(NC)"
	@echo "$(YELLOW)Current version: $(VERSION)$(NC)"
	@read -p "Enter tag for new release (e.g., v1.0.0): " tag && \
	echo "Creating tag $$tag..." && \
	git tag $$tag && \
	git push && git push --tags
	@echo "$(GREEN)Release created. Don't forget to update CHANGELOG.md and RELEASE_CHECKLIST.md accordingly.$(NC)"