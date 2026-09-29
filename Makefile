.PHONY: install test lint format-check validate

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check backend

format-check:
	ruff format --check backend

validate: lint format-check test
