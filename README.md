# FastAPI Cookiecutter

A production-ready [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for FastAPI projects — inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).

Generates a fully Dockerized FastAPI application with PostgreSQL, Alembic migrations, JWT authentication, environment-based settings, and optional integrations for Celery, Sentry, cloud storage, and more.

## Features

- **FastAPI** with async SQLAlchemy 2.0 and Pydantic v2
- **PostgreSQL** with Alembic migrations (autogenerate support)
- **Docker Compose** configurations for local development and production (with Traefik)
- **JWT authentication** with login, registration, and password reset
- **SQLAdmin** admin interface
- **Environment-based settings** (local / production / test) via Pydantic Settings
- **Celery** task queue (optional)
- **Sentry** error tracking (optional)
- **Cloud storage** — S3 or Cloudflare R2 (optional)
- **Email** via SendGrid, Mailgun, or Amazon SES with Mailpit for local dev (optional)
- **CI/CD** — GitHub Actions or GitLab CI (optional)
- **Pre-commit hooks** with Ruff linting and formatting (optional)
- **Makefile** with common development commands
- **Pytest** with async fixtures and factory-based test data

## Quickstart

```bash
# Install cookiecutter
pip install cookiecutter

# Generate your project
cookiecutter gh:hamel/my-fastapi-cookiecutter

# Start developing
cd your_project_slug
docker compose -f docker-compose.local.yml up --build
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `project_name` | string | `My FastAPI Project` | Human-readable project name |
| `project_slug` | string | *(auto)* | Python package name (derived from project_name) |
| `description` | string | `A short description of the project.` | One-line project description |
| `author_name` | string | `Your Name` | Author for pyproject.toml |
| `domain_name` | string | `example.com` | Production domain (used in Traefik config) |
| `email` | string | *(auto)* | Contact email (derived from author + domain) |
| `version` | string | `0.1.0` | Initial version |
| `python_version` | string | `3.12` | Python version for Docker images |
| `postgres_version` | choice | `16` | PostgreSQL version (`16`, `15`, `17`) |
| `use_celery` | y/n | `y` | Include Celery task queue with Redis |
| `use_sentry` | y/n | `y` | Include Sentry error tracking |
| `use_mailpit` | y/n | `y` | Include Mailpit for local email testing |
| `mail_service` | choice | `SendGrid` | Production email provider (`SendGrid`, `Mailgun`, `Amazon SES`) |
| `cloud_storage` | choice | `S3` | Cloud storage backend (`S3`, `R2`, `None`) |
| `ci_tool` | choice | `GitHub Actions` | CI/CD configuration (`GitHub Actions`, `GitLab CI`, `None`) |
| `use_pre_commit` | y/n | `y` | Include pre-commit hooks config |
| `timezone` | string | `UTC` | Default timezone |
| `license` | choice | `MIT` | License (`MIT`, `BSD-3-Clause`, `Apache-2.0`, `Proprietary`) |

## Generated Project Structure

```
your_project_slug/
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
│   └── your_project_slug/
│       ├── main.py              # FastAPI app factory
│       ├── cli.py               # Management commands
│       ├── celery_app.py        # Celery configuration (optional)
│       ├── config/
│       │   ├── settings.py      # Environment dispatcher
│       │   ├── base.py          # Shared settings
│       │   ├── local.py         # Dev overrides
│       │   ├── production.py    # Production settings
│       │   └── test.py          # Test overrides
│       ├── auth/
│       │   ├── router.py        # Auth endpoints
│       │   ├── models.py        # User model
│       │   ├── schemas.py       # Pydantic schemas
│       │   ├── security.py      # JWT + password hashing
│       │   ├── dependencies.py  # Auth dependencies
│       │   └── tasks.py         # Email tasks (optional)
│       ├── admin/
│       │   └── views.py         # SQLAdmin setup
│       ├── core/
│       │   ├── dependencies.py  # Shared dependencies
│       │   ├── email.py         # Email utilities
│       │   ├── exceptions.py    # Custom exception handlers
│       │   ├── sentry.py        # Sentry init (optional)
│       │   └── storage.py       # Cloud storage (optional)
│       └── db/
│           ├── base.py          # SQLAlchemy Base
│           └── session.py       # Engine + session factory
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
│   ├── conftest.py
│   ├── factories.py
│   ├── test_auth/
│   └── test_core/
├── .envs/
│   ├── .local/
│   └── .production/
├── docker-compose.local.yml
├── docker-compose.production.yml
├── pyproject.toml
├── alembic.ini
├── Makefile
└── README.md
```

## Optional Features

### Celery (`use_celery`)
Adds a Celery worker and Redis broker. Includes `celery_app.py` configuration and async email tasks in `auth/tasks.py`. Adds `celeryworker` and `redis` services to Docker Compose.

### Sentry (`use_sentry`)
Adds `core/sentry.py` with Sentry SDK initialization. Configured via `SENTRY_DSN` environment variable in production settings.

### Cloud Storage (`cloud_storage`)
Adds `core/storage.py` with an S3-compatible storage client using `boto3`. Works with both AWS S3 and Cloudflare R2. Set to `None` to exclude.

### Mailpit (`use_mailpit`)
Adds a Mailpit container to the local Docker Compose for catching outgoing emails during development. Accessible at `http://localhost:8025`.

### CI/CD (`ci_tool`)
- **GitHub Actions**: Generates `.github/workflows/ci.yml` with lint, test, and build steps.
- **GitLab CI**: Generates `.gitlab-ci.yml` with equivalent pipeline stages.

### Pre-commit (`use_pre_commit`)
Generates `.pre-commit-config.yaml` with Ruff linting and formatting hooks.

### License (`license`)
Generates a `LICENSE` file for MIT, BSD-3-Clause, or Apache-2.0. Selecting `Proprietary` omits the LICENSE file entirely.

## Development Commands

The generated project includes a Makefile with these targets:

| Command | Description |
|---------|-------------|
| `make help` | Show all available commands |
| `make build` | Build all containers |
| `make up` | Start all services (detached) |
| `make down` | Stop all services |
| `make logs` | Tail logs for all services |
| `make migrate` | Run Alembic migrations |
| `make makemigrations msg="description"` | Create a new Alembic migration |
| `make test` | Run pytest |
| `make lint` | Run Ruff linter |
| `make format` | Format code with Ruff |
| `make createsuperuser` | Create an admin user |
| `make shell` | Open a bash shell in the app container |

## Tech Stack

| Component | This Template | cookiecutter-django Equivalent |
|-----------|--------------|-------------------------------|
| Web framework | FastAPI | Django |
| ORM | SQLAlchemy 2.0 (async) | Django ORM |
| Migrations | Alembic | Django migrations |
| Settings | Pydantic Settings | django-environ |
| Auth | JWT (python-jose + passlib) | django-allauth |
| Admin | SQLAdmin | Django Admin |
| Task queue | Celery + Redis | Celery + Redis |
| Package manager | uv | pip |
| Linting | Ruff | Ruff / flake8 |
| Testing | Pytest + httpx | Pytest |
| Reverse proxy | Traefik | Traefik |

## Contributing

Contributions are welcome. To test changes to the template:

```bash
# Generate a project with default options
cookiecutter . --no-input -o /tmp/test

# Verify the generated project
cd /tmp/test/my_fastapi_project
docker compose -f docker-compose.local.yml config  # validate compose
python -c "import ast; ast.parse(open('src/my_fastapi_project/main.py').read())"  # validate Python
```
