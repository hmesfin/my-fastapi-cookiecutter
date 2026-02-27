import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httpx

from {{ cookiecutter.project_slug }}.config import get_settings

logger = logging.getLogger(__name__)


async def send_email(to: str, subject: str, html: str) -> None:
  """Send an email using the configured backend."""
  settings = get_settings()
  backend = settings.email_backend

  if backend == "console":
    _send_console(to, subject, html)
  elif backend == "smtp":
    _send_smtp(to, subject, html)
  elif backend == "sendgrid":
    await _send_sendgrid(to, subject, html)
  elif backend == "mailgun":
    await _send_mailgun(to, subject, html)
  {%- if cookiecutter.cloud_storage == "S3" or cookiecutter.mail_service == "Amazon SES" %}
  elif backend == "ses":
    await _send_ses(to, subject, html)
  {%- endif %}
  else:
    raise ValueError(f"Unknown email backend: {backend}")


def send_email_sync(to: str, subject: str, html: str) -> None:
  """Synchronous email sending for use in Celery tasks."""
  settings = get_settings()
  backend = settings.email_backend

  if backend == "console":
    _send_console(to, subject, html)
  elif backend == "smtp":
    _send_smtp(to, subject, html)
  else:
    raise ValueError(f"Sync sending not supported for backend: {backend}")


def _send_console(to: str, subject: str, html: str) -> None:
  logger.info("=" * 60)
  logger.info("EMAIL TO: %s", to)
  logger.info("SUBJECT: %s", subject)
  logger.info("BODY:\n%s", html)
  logger.info("=" * 60)


def _send_smtp(to: str, subject: str, html: str) -> None:
  settings = get_settings()
  msg = MIMEMultipart("alternative")
  msg["Subject"] = subject
  msg["From"] = settings.email_from
  msg["To"] = to
  msg.attach(MIMEText(html, "html"))

  with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
    server.starttls()
    if settings.smtp_user:
      server.login(settings.smtp_user, settings.smtp_password)
    server.sendmail(settings.email_from, to, msg.as_string())


async def _send_sendgrid(to: str, subject: str, html: str) -> None:
  settings = get_settings()
  async with httpx.AsyncClient() as client:
    response = await client.post(
      "https://api.sendgrid.com/v3/mail/send",
      headers={"Authorization": f"Bearer {settings.smtp_password}"},
      json={
        "personalizations": [{"to": [{"email": to}]}],
        "from": {"email": settings.email_from},
        "subject": subject,
        "content": [{"type": "text/html", "value": html}],
      },
    )
    response.raise_for_status()


async def _send_mailgun(to: str, subject: str, html: str) -> None:
  settings = get_settings()
  domain = settings.email_from.split("@")[1]
  async with httpx.AsyncClient() as client:
    response = await client.post(
      f"https://api.mailgun.net/v3/{domain}/messages",
      auth=("api", settings.smtp_password),
      data={
        "from": settings.email_from,
        "to": [to],
        "subject": subject,
        "html": html,
      },
    )
    response.raise_for_status()
{%- if cookiecutter.cloud_storage == "S3" or cookiecutter.mail_service == "Amazon SES" %}


async def _send_ses(to: str, subject: str, html: str) -> None:
  import aioboto3

  settings = get_settings()
  session = aioboto3.Session()
  async with session.client(
    "ses",
    region_name=settings.aws_s3_region_name,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
  ) as client:
    await client.send_email(
      Source=settings.email_from,
      Destination={"ToAddresses": [to]},
      Message={
        "Subject": {"Data": subject},
        "Body": {"Html": {"Data": html}},
      },
    )
{%- endif %}
