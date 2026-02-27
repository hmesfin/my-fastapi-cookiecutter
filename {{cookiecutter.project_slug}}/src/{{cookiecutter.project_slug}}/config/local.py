from {{ cookiecutter.project_slug }}.config.base import BaseAppSettings


class LocalSettings(BaseAppSettings):
  debug: bool = True
  email_backend: str = "console"
  {%- if cookiecutter.use_celery == "y" %}
  celery_task_always_eager: bool = True
  {%- endif %}
