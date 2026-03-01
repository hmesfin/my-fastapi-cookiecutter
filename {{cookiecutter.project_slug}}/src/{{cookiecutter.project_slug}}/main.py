from contextlib import asynccontextmanager

from fastapi import FastAPI

from {{ cookiecutter.project_slug }}.admin import setup_admin
from {{ cookiecutter.project_slug }}.auth.router import router as auth_router
from {{ cookiecutter.project_slug }}.config import get_settings
from {{ cookiecutter.project_slug }}.core.exceptions import register_exception_handlers
from {{ cookiecutter.project_slug }}.db import engine

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
  yield
  await engine.dispose()


app = FastAPI(
  title=settings.project_name,
  version=settings.version,
  lifespan=lifespan,
  docs_url="/docs",
  redoc_url="/redoc",
)

# Routers
app.include_router(auth_router)

# Admin
setup_admin(app, engine)

# Exception handlers
register_exception_handlers(app)
{%- if cookiecutter.use_sentry == "y" %}

# Sentry
from {{ cookiecutter.project_slug }}.core.sentry import init_sentry  # noqa: E402

init_sentry()
{%- endif %}


@app.get("/health", tags=["health"])
async def health_check():
  return {"status": "ok"}
