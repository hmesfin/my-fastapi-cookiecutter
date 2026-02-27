from {{ cookiecutter.project_slug }}.config.base import BaseAppSettings


class ProductionSettings(BaseAppSettings):
  debug: bool = False
  {%- if cookiecutter.use_sentry == "y" %}
  sentry_dsn: str  # Required in production
  {%- endif %}
