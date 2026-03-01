# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Quick Start

```bash
# Build and start all services
docker compose -f docker-compose.local.yml up --build -d

# Run database migrations
make migrate

# Create a superuser
make createsuperuser
```

## Development

All commands use Docker Compose via `make`:

```bash
make up              # Start services
make down            # Stop services
make logs            # Tail logs
make test            # Run tests
make lint            # Run linter
make format          # Format code
make migrate         # Run migrations
make makemigrations msg="description"  # Create migration
make shell           # Open shell in app container
```

## API Documentation

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Admin Panel

Access the admin panel at [http://localhost:8000/admin](http://localhost:8000/admin). Log in with your superuser credentials.

## Deployment

```bash
# Production with Traefik (HTTPS)
docker compose -f docker-compose.production.yml up --build -d
```

Configure `.envs/.production/` files before deploying.

## Project Structure

```
src/{{ cookiecutter.project_slug }}/
├── admin/          # sqladmin panel
├── auth/           # Authentication (JWT, users)
├── config/         # pydantic-settings
├── core/           # Shared dependencies, email, exceptions
├── db/             # SQLAlchemy engine, base models
├── main.py         # FastAPI app factory
└── cli.py          # Typer CLI commands
```
