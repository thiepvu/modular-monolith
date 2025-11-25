# Makefile for Modular Monolith

.PHONY: help install migrate seed run test clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make migrate    - Run database migrations"
	@echo "  make seed       - Seed database with initial data"
	@echo "  make run        - Run the application"
	@echo "  make test       - Run all tests"
	@echo "  make test-unit  - Run unit tests"
	@echo "  make test-int   - Run integration tests"
	@echo "  make test-e2e   - Run e2e tests"
	@echo "  make coverage   - Run tests with coverage"
	@echo "  make clean      - Clean up generated files"

install:
	pip install -r requirements.txt

migrate:
	python scripts/migrate.py --upgrade

seed:
	python scripts/seed.py

run:
	python src/main.py

test:
	pytest

test-unit:
	pytest tests/unit/

test-int:
	pytest tests/integration/

test-e2e:
	pytest tests/e2e/

coverage:
	pytest --cov=src --cov-report=html --cov-report=term

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage
