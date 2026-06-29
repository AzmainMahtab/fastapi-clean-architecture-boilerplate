# Dockerfile
FROM python:3.14-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency manifests
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment (production only)
RUN uv sync --frozen --no-install-project --no-dev

# PRODUCTION RUNTIME
FROM python:3.14-slim AS production

# Install runtime OS dependencies (pg_isready for entrypoint, tini for zombie reaping)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Copy uv and the pre-built virtual environment from builder
COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /app /app

WORKDIR /app

# Copy your application code (will be overridden by volumes in local.yml)
COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./

# Copy entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Point to the virtual environment created in the builder stage
ENV PATH="/app/.venv/bin:$PATH"

# Use tini as PID 1 to handle signals properly (crucial for Gunicorn graceful shutdowns)
ENTRYPOINT ["tini", "--", "/app/entrypoint.sh"]

# ==========================================
# TEST STAGE (extends production with test deps)
# ==========================================
FROM production AS test

# Temporarily switch to root so uv can write to .venv (owned by root from builder)
USER root
RUN uv sync --frozen --no-install-project --group test
USER appuser

# Clear the production entrypoint — test runs pytest directly, no DB wait or server start
ENTRYPOINT []
