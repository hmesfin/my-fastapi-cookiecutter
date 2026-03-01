.DEFAULT_GOAL := help
COMPOSE := docker compose -f docker-compose.local.yml
RUN := $(COMPOSE) run --rm app

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build: ## Build all containers
	$(COMPOSE) build

.PHONY: up
up: ## Start all services
	$(COMPOSE) up -d

.PHONY: down
down: ## Stop all services
	$(COMPOSE) down

.PHONY: logs
logs: ## Tail logs for all services
	$(COMPOSE) logs -f

.PHONY: migrate
migrate: ## Run database migrations
	$(RUN) uv run alembic upgrade head

.PHONY: makemigrations
makemigrations: ## Create a new migration
	$(RUN) uv run alembic revision --autogenerate -m "$(msg)"

.PHONY: test
test: ## Run tests
	$(RUN) uv run pytest -v

.PHONY: lint
lint: ## Run linter
	$(RUN) uv run ruff check .

.PHONY: format
format: ## Format code
	$(RUN) uv run ruff format .

.PHONY: createsuperuser
createsuperuser: ## Create a superuser
	$(RUN) uv run python -m {{ cookiecutter.project_slug }}.cli createsuperuser

.PHONY: shell
shell: ## Open a shell in the app container
	$(RUN) bash
