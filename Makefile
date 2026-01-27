# Makefile для удобного запуска команд проверки кода
# Использование: make lint, make format, make type-check, make check-all

.PHONY: help install-dev lint format type-check check-all fix fix-safe lint-errors lint-error pre-commit-install

help:
	@echo "Available commands:"
	@echo "  make install-dev      - Install dev dependencies"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo "  make lint             - Run linter (Ruff)"
	@echo "  make lint-errors      - Show only errors (no warnings)"
	@echo "  make format           - Format code (Ruff)"
	@echo "  make type-check       - Check types (MyPy)"
	@echo "  make fix-safe         - Fix only safe issues"
	@echo "  make fix              - Fix all issues (including unsafe)"
	@echo "  make check-all        - Run all checks"

install-dev:
	pip install -r requirements-dev.txt

pre-commit-install:
	pre-commit install

lint:
	ruff check .

lint-errors:
	@echo "Remaining errors (cannot be fixed automatically):"
	-@ruff check . --output-format=concise

lint-error: lint-errors

format:
	ruff format .

type-check:
	mypy app

fix-safe:
	@echo "Fixing safe issues..."
	-@ruff check --fix .
	@echo "Formatting code..."
	@ruff format .
	@echo "Done! Run 'make lint-errors' to see remaining issues."

fix:
	@echo "Fixing all issues (including unsafe)..."
	-@ruff check --fix --unsafe-fixes .
	@echo "Formatting code..."
	@ruff format .
	@echo "Done! Run 'make lint-errors' to see remaining issues."

check-all: lint type-check
	@echo "All checks completed!"
