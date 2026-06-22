# Cangjie Skill Dockerfile
# Multi-stage build for production and development

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Stage 2: Production
FROM python:3.11-slim AS production

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 cangjie && \
    chown -R cangjie:cangjie /app
USER cangjie

# Copy application code
COPY --chown=cangjie:cangjie . .

# Create necessary directories
RUN mkdir -p data/books_raw data/books_txt data/books_txt_ocr data/library data/logs

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PROJECT_ROOT=/app
ENV BOOKS_RAW_DIR=/app/data/books_raw
ENV BOOKS_TXT_DIR=/app/data/books_txt
ENV BOOKS_TXT_OCR_DIR=/app/data/books_txt_ocr
ENV LIBRARY_DIR=/app/data/library
ENV OUTPUT_DIR=/app/data/output
ENV LOG_FILE=/app/data/logs/cangjie.log

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "-m", "cangjie", "--help"]

# Stage 3: Development (optional)
FROM builder AS development

WORKDIR /app

# Install development dependencies
COPY requirements-dev.txt .
RUN pip install --user --no-cache-dir -r requirements-dev.txt

# Install pre-commit
RUN pip install --user pre-commit && \
    pre-commit install

# Create development directories
RUN mkdir -p .vscode .idea

# Set development environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DEBUG=true
ENV LOG_LEVEL=DEBUG

# Default command for development
CMD ["python", "-m", "pytest", "tests/", "-v"]

# Stage 4: Testing
FROM builder AS testing

WORKDIR /app

# Install test dependencies
COPY requirements-test.txt .
RUN pip install --user --no-cache-dir -r requirements-test.txt

# Copy test files
COPY tests/ tests/

# Run tests
CMD ["python", "-m", "pytest", "tests/", "-v", "--cov=cangjie", "--cov-report=html"]
