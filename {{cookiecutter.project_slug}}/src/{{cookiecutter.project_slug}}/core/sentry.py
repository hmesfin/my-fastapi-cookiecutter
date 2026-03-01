{%- if cookiecutter.use_sentry == "y" %}
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
{%- if cookiecutter.use_celery == "y" %}
from sentry_sdk.integrations.celery import CeleryIntegration
{%- endif %}

from {{ cookiecutter.project_slug }}.config import get_settings


def init_sentry() -> None:
  settings = get_settings()
  if not settings.sentry_dsn:
    return

  sentry_sdk.init(
    dsn=settings.sentry_dsn,
    integrations=[
      FastApiIntegration(),
      SqlalchemyIntegration(),
      {%- if cookiecutter.use_celery == "y" %}
      CeleryIntegration(),
      {%- endif %}
    ],
    traces_sample_rate=0.1,
    send_default_pii=False,
    environment=settings.fastapi_env if hasattr(settings, "fastapi_env") else "production",
  )
{%- endif %}
