.PHONY: install run test lint format typecheck

install:
	python -m pip install --upgrade pip
	python -m pip install -e .[dev]

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

lint:
	ruff check .
	black --check .

format:
	ruff check . --fix
	black .

typecheck:
	mypy app tests
