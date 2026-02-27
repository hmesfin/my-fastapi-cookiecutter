from {{ cookiecutter.project_slug }}.config.base import BaseAppSettings


class TestSettings(BaseAppSettings):
  debug: bool = True
  postgres_db: str = "{{ cookiecutter.project_slug }}_test"
  {%- if cookiecutter.use_celery == "y" %}
  celery_task_always_eager: bool = True
  {%- endif %}
