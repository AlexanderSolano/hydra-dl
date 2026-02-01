.PHONY: install format lint test clean

install:
	@echo "🚀 Installing dependencies..."
	uv pip install -e ".[dev]"

format:
	@echo "🎨 Formatting code..."
	uv run ruff format .
	uv run ruff check --fix .

lint:
	@echo "🔍 Linting & Type Checking..."
	uv run ruff check .
	uv run mypy app/

test:
	@echo "🧪 Running Tests..."
	uv run pytest

clean:
	rm -rf .ruff_cache .mypy_cache .pytest_cache .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +