{%- if cookiecutter.use_celery == "y" %}
from celery import Celery

from {{ cookiecutter.project_slug }}.config import get_settings

settings = get_settings()

celery_app = Celery(
  "{{ cookiecutter.project_slug }}",
  broker=settings.celery_broker_url,
  backend=settings.celery_result_backend,
)

celery_app.conf.update(
  task_always_eager=settings.celery_task_always_eager,
  task_serializer="json",
  result_serializer="json",
  accept_content=["json"],
  timezone=settings.timezone,
  enable_utc=True,
)

celery_app.autodiscover_tasks(
  ["{{ cookiecutter.project_slug }}.auth"],
)
{%- endif %}
