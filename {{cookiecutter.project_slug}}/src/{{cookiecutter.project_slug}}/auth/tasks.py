{%- if cookiecutter.use_celery == "y" %}
from {{ cookiecutter.project_slug }}.celery_app import celery_app


@celery_app.task
def send_verification_email(user_email: str, token: str) -> None:
  """Send account verification email."""
  from {{ cookiecutter.project_slug }}.core.email import send_email_sync

  send_email_sync(
    to=user_email,
    subject="Verify your email",
    html="<p>Click <a href='https://{{ cookiecutter.domain_name }}/verify?token=" + token + "'>here</a> to verify.</p>",
  )


@celery_app.task
def send_password_reset_email(user_email: str, token: str) -> None:
  """Send password reset email."""
  from {{ cookiecutter.project_slug }}.core.email import send_email_sync

  send_email_sync(
    to=user_email,
    subject="Reset your password",
    html="<p>Click <a href='https://{{ cookiecutter.domain_name }}/reset?token=" + token + "'>here</a> to reset.</p>",
  )
{%- endif %}
