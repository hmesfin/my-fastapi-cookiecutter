FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev --no-install-project 2>/dev/null || uv sync --no-dev --no-install-project

# Copy application
COPY . .
RUN uv sync --frozen --no-dev 2>/dev/null || uv sync --no-dev

# Entrypoint
COPY compose/local/app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user
RUN groupadd -r app && useradd -r -g app app && chown -R app:app /app
USER app

ENTRYPOINT ["/entrypoint.sh"]
