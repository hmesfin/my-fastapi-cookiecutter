from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseAppSettings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".envs/.local/.app",
    env_file_encoding="utf-8",
    extra="ignore",
  )

  # Application
  project_name: str = "{{ cookiecutter.project_name }}"
  version: str = "{{ cookiecutter.version }}"
  debug: bool = False
  secret_key: str
  domain: str = "localhost"
  timezone: str = "{{ cookiecutter.timezone }}"

  # Database
  postgres_host: str = "postgres"
  postgres_port: int = 5432
  postgres_user: str = "dev"
  postgres_password: str
  postgres_db: str = "{{ cookiecutter.project_slug }}"

  # Auth
  access_token_expire_minutes: int = 30
  refresh_token_expire_days: int = 7
  algorithm: str = "HS256"
  {%- if cookiecutter.use_celery == "y" %}

  # Celery
  celery_broker_url: str = "redis://redis:6379/0"
  celery_result_backend: str = "redis://redis:6379/0"
  celery_task_always_eager: bool = False
  {%- endif %}
  {%- if cookiecutter.use_sentry == "y" %}

  # Sentry
  sentry_dsn: str = ""
  {%- endif %}
  {%- if cookiecutter.cloud_storage != "None" %}

  # Storage
  aws_access_key_id: str = ""
  aws_secret_access_key: str = ""
  aws_storage_bucket_name: str = ""
  aws_s3_region_name: str = "us-east-1"
  {%- if cookiecutter.cloud_storage == "R2" %}
  aws_s3_endpoint_url: str = ""
  {%- endif %}
  {%- endif %}

  # Email
  email_backend: str = "console"
  smtp_host: str = ""
  smtp_port: int = 587
  smtp_user: str = ""
  smtp_password: str = ""
  email_from: str = "noreply@{{ cookiecutter.domain_name }}"

  @property
  def database_url(self) -> str:
    return (
      f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
      f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    )

  @property
  def sync_database_url(self) -> str:
    return (
      f"postgresql://{self.postgres_user}:{self.postgres_password}"
      f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    )
