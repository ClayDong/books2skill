# Books2Skill Makefile
# Common commands for development and deployment

.PHONY: help install dev-install format lint test test-cov clean dist docker-build docker-run

# Default target
help:
	@echo "Books2Skill Development Commands"
	@echo ""
	@echo "Development:"
	@echo "  install          Install production dependencies"
	@echo "  dev-install      Install development dependencies"
	@echo "  format           Format code with black and isort"
	@echo "  lint             Run linters (flake8, mypy)"
	@echo "  test             Run tests"
	@echo "  test-cov         Run tests with coverage"
	@echo ""
	@echo "Processing:"
	@echo "  extract          Extract text from PDFs"
	@echo "  ocr              Run OCR on scanned PDFs"
	@echo "  validate         Validate system consistency"
	@echo "  distill          Run full distillation pipeline"
	@echo ""
	@echo "Deployment:"
	@echo "  clean            Clean build artifacts"
	@echo "  dist             Build distribution package"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run in Docker container"
	@echo ""

# Development
install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"
	pre-commit install

format:
	black .
	isort .

lint:
	flake8 .
	mypy .

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=books2skill --cov-report=html --cov-report=term-missing -v

# Processing
extract:
	python scripts/extract_pdfs.py

ocr:
	python scripts/ocr_pdfs.py

validate:
	python scripts/validate_system.py

distill:
	python -m books2skill distill --book "path/to/book.pdf"

# Deployment
clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

dist: clean
	python -m build

docker-build:
	docker build -t books2skill .

docker-run:
	docker run -it --rm -v $(pwd)/data:/app/data books2skill

# Pre-commit hooks
pre-commit-run:
	pre-commit run --all-files

pre-commit-autoupdate:
	pre-commit autoupdate

# Documentation
docs:
	@echo "Documentation commands will be added later"

# Utility
venv:
	python -m venv venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source venv/bin/activate  # Linux/Mac"
	@echo "  venv\Scripts\activate     # Windows"

update-deps:
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

check-deps:
	pip list --outdated

# Backup
backup:
	tar -czf backup-$$(date +%Y%m%d-%H%M%S).tar.gz \
		--exclude=venv \
		--exclude=__pycache__ \
		--exclude=*.pyc \
		--exclude=.git \
		.
	@echo "Backup created"

# Development server (if web interface is added)
dev-server:
	@echo "Starting development server..."
	@echo "Web interface not yet implemented"
