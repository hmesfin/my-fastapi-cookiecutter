# Stage 1: Build dependencies
FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project 2>/dev/null || uv sync --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev 2>/dev/null || uv sync --no-dev

# Stage 2: Runtime
FROM python:{{ cookiecutter.python_version }}-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app /app

# Entrypoint
COPY compose/production/app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user
RUN groupadd -r app && useradd -r -g app app && chown -R app:app /app
USER app

# Add uv venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "{{ cookiecutter.project_slug }}.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
