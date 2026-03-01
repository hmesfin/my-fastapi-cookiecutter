{%- if cookiecutter.cloud_storage != "None" %}
import aioboto3

from {{ cookiecutter.project_slug }}.config import get_settings


def _get_client_kwargs() -> dict:
  settings = get_settings()
  kwargs = {
    "region_name": settings.aws_s3_region_name,
    "aws_access_key_id": settings.aws_access_key_id,
    "aws_secret_access_key": settings.aws_secret_access_key,
  }
  {%- if cookiecutter.cloud_storage == "R2" %}
  kwargs["endpoint_url"] = settings.aws_s3_endpoint_url
  {%- endif %}
  return kwargs


async def upload_file(
  file_obj,
  key: str,
  content_type: str = "application/octet-stream",
) -> str:
  """Upload a file and return its key."""
  settings = get_settings()
  session = aioboto3.Session()
  async with session.client("s3", **_get_client_kwargs()) as client:
    await client.upload_fileobj(
      file_obj,
      settings.aws_storage_bucket_name,
      key,
      ExtraArgs={"ContentType": content_type},
    )
  return key


async def delete_file(key: str) -> None:
  """Delete a file by key."""
  settings = get_settings()
  session = aioboto3.Session()
  async with session.client("s3", **_get_client_kwargs()) as client:
    await client.delete_object(
      Bucket=settings.aws_storage_bucket_name,
      Key=key,
    )


async def get_presigned_url(key: str, expires_in: int = 3600) -> str:
  """Generate a presigned URL for a file."""
  settings = get_settings()
  session = aioboto3.Session()
  async with session.client("s3", **_get_client_kwargs()) as client:
    url = await client.generate_presigned_url(
      "get_object",
      Params={
        "Bucket": settings.aws_storage_bucket_name,
        "Key": key,
      },
      ExpiresIn=expires_in,
    )
  return url
{%- endif %}
