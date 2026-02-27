# FastAPI Cookiecutter Design

A production-ready FastAPI cookiecutter template modeled after Cookiecutter Django, with 12-factor compliance, Docker-first workflow, and batteries included.

**Target:** Teams / companies
**Templating:** Cookiecutter (Jinja2)

## Technology Mapping

| Cookiecutter Django | Our FastAPI Equivalent |
|---|---|
| django-environ | pydantic-settings |
| Django ORM | SQLAlchemy 2.0 (async) + Alembic |
| Django settings module hierarchy | Pydantic Settings classes (base/local/prod/test) |
| Gunicorn + WSGI | Uvicorn + ASGI (async-native) |
| Django allauth | Custom JWT (access/refresh tokens) |
| Django Admin | sqladmin |
| django-anymail | Direct API calls (httpx/boto3) |
| Django management commands | Typer CLI |
| requirements/*.txt | uv + pyproject.toml |
| Docker + Traefik + Celery + Redis + Postgres | Same |

## Cookiecutter Prompts

```json
{
  "project_name": "My FastAPI Project",
  "project_slug": "{{ cookiecutter.project_name|lower|replace(' ', '_')|replace('-', '_') }}",
  "description": "A short description of the project.",
  "author_name": "Your Name",
  "domain_name": "example.com",
  "email": "{{ cookiecutter.author_name|lower|replace(' ', '-') }}@{{ cookiecutter.domain_name }}",
  "version": "0.1.0",
  "python_version": "3.12",
  "postgres_version": ["16", "15", "17"],
  "use_celery": "y",
  "use_sentry": "y",
  "use_mailpit": "y",
  "mail_service": ["SendGrid", "Mailgun", "Amazon SES"],
  "cloud_storage": ["S3", "R2", "None"],
  "ci_tool": ["GitHub Actions", "GitLab CI", "None"],
  "use_pre_commit": "y",
  "timezone": "UTC",
  "license": ["MIT", "BSD-3-Clause", "Apache-2.0", "Proprietary"]
}
```

Docker is always on (no toggle). No frontend options (API-only).

## Generated Project Structure

```
{{cookiecutter.project_slug}}/
├── .envs/
│   ├── .local/
│   │   ├── .app
│   │   └── .postgres
│   └── .production/
│       ├── .app
│       └── .postgres
├── compose/
│   ├── local/
│   │   ├── app/
│   │   │   ├── Dockerfile
│   │   │   └── entrypoint.sh
│   │   └── postgres/
│   │       └── Dockerfile
│   └── production/
│       ├── app/
│       │   ├── Dockerfile
│       │   └── entrypoint.sh
│       ├── postgres/
│       │   └── Dockerfile
│       └── traefik/
│           └── traefik.yml
├── src/
│   └── {{cookiecutter.project_slug}}/
│       ├── __init__.py
│       ├── main.py                  # FastAPI app factory
│       ├── config/
│       │   ├── __init__.py
│       │   ├── base.py              # BaseSettings (shared)
│       │   ├── local.py             # LocalSettings
│       │   ├── production.py        # ProductionSettings
│       │   ├── test.py              # TestSettings
│       │   └── settings.py          # get_settings() factory
│       ├── admin/
│       │   ├── __init__.py
│       │   └── views.py             # sqladmin ModelAdmin classes
│       ├── auth/
│       │   ├── __init__.py
│       │   ├── models.py            # User SQLAlchemy model
│       │   ├── schemas.py           # Pydantic request/response schemas
│       │   ├── router.py            # /auth/* endpoints
│       │   ├── dependencies.py      # get_current_user, etc.
│       │   ├── security.py          # JWT token create/verify
│       │   └── tasks.py             # (if celery) email verification
│       ├── db/
│       │   ├── __init__.py
│       │   ├── base.py              # DeclarativeBase, metadata
│       │   └── session.py           # async engine, AsyncSession factory
│       ├── core/
│       │   ├── __init__.py
│       │   ├── dependencies.py      # get_db, common deps
│       │   ├── email.py             # Email sending
│       │   ├── storage.py           # S3/R2 file storage client
│       │   └── exceptions.py        # Custom exception handlers
│       └── cli.py                   # Typer CLI
├── alembic/
│   ├── env.py
│   ├── versions/
│   └── alembic.ini
├── tests/
│   ├── conftest.py
│   ├── factories.py
│   ├── test_auth/
│   │   ├── test_router.py
│   │   └── test_security.py
│   └── test_core/
│       └── test_email.py
├── docker-compose.local.yml
├── docker-compose.production.yml
├── pyproject.toml
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
├── .gitlab-ci.yml
├── Makefile
└── README.md
```

## Configuration System (12-Factor)

Uses pydantic-settings with environment-specific classes inheriting from `BaseAppSettings`:

- `FASTAPI_ENV` variable selects settings class (`local`, `production`, `test`)
- `.envs/` directory structure mirrors Cookiecutter Django
- Production settings make critical fields required (no defaults)
- `database_url` is a computed property
- `extra="ignore"` allows shared env files

### Settings hierarchy

- **base.py** — all shared config (db, redis, celery, email, sentry, storage)
- **local.py** — `debug=True`, console email, `celery_task_always_eager=True`
- **production.py** — `debug=False`, required `allowed_hosts` and `sentry_dsn`
- **test.py** — `debug=True`, test db name, eager celery

## Docker Compose

### Local

Services: `app` (uvicorn --reload), `postgres`, `redis`, `mailpit` (optional), `celery_worker` + `celery_beat` + `flower` (if celery).

- All ports exposed directly
- Volume mounts for hot-reload
- `.envs/.local/` env files

### Production

Services: `traefik` (v3.3), `app` (uvicorn --workers 4), `postgres`, `redis`, celery services (if enabled).

- No ports exposed except via Traefik (80/443)
- No code volume mounts
- Let's Encrypt auto-certs
- Traefik labels on app service for routing
- Multi-stage Dockerfiles

### Makefile

Wraps: `up`, `build`, `migrate`, `makemigrations`, `test`, `createsuperuser`.

## Authentication

Custom JWT with access tokens (15min) and refresh tokens (7 days).

### Endpoints

- `POST /auth/register` — create user, return tokens
- `POST /auth/login` — email+password, return tokens
- `POST /auth/refresh` — refresh → new access token
- `POST /auth/password-reset` — send reset email
- `POST /auth/password-reset/confirm` — verify token, set new password
- `GET /auth/me` — current user profile
- `PATCH /auth/me` — update profile

### User model

UUID primary key, email (unique, indexed), hashed_password, full_name, is_active, is_superuser, created_at.

### Dependencies

- `get_current_user` — extracts user from JWT
- `get_current_superuser` — superuser check

## Admin (sqladmin)

Mounted at `/admin`. Auth uses JWT + superuser check. Pre-configured `UserAdmin` view with search, column display, delete disabled.

## Email

Simple function interface: `async def send_email(to, subject, html)`.

Backend switching via `settings.email_backend`:
- `"console"` → stdout
- `"mailpit"` → SMTP localhost:1025
- `"sendgrid"` → SendGrid API via httpx
- `"mailgun"` → Mailgun API via httpx
- `"ses"` → Amazon SES via boto3

## Storage (if cloud_storage != "None")

Thin async wrapper around aioboto3. S3 and R2 use the same client — `aws_s3_endpoint_url` differentiates.

Interface: `upload_file`, `delete_file`, `get_presigned_url`.

## Celery (if use_celery == "y")

- Redis broker
- Autodiscover tasks from modules
- Local: eager mode (runs inline)
- Production: separate worker/beat/flower containers
- Tasks in each module's `tasks.py`

## Sentry (if use_sentry == "y")

Initialized in app factory with FastAPI, SQLAlchemy, and Celery integrations. Traces sample rate 0.1.

## CI/CD

GitHub Actions or GitLab CI (based on cookiecutter choice):
1. Lint (ruff check + ruff format --check)
2. Test (pytest --cov via docker compose)
3. Build (verify Dockerfiles)

## Testing

- **pytest** + **pytest-asyncio** (auto mode)
- **httpx** — async test client
- **factory-boy** — model factories
- **pytest-cov** — coverage
- Real Postgres in tests (not SQLite)
- Per-test session rollback

## Pre-commit (if use_pre_commit == "y")

Ruff (lint + format), trailing-whitespace, end-of-file-fixer, check-yaml, check-added-large-files. No Black (Ruff replaces it).
