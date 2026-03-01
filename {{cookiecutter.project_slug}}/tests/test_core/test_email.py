import logging

import pytest

from {{ cookiecutter.project_slug }}.core.email import send_email


@pytest.mark.asyncio
async def test_console_email_backend(caplog):
  with caplog.at_level(logging.INFO):
    await send_email(
      to="user@example.com",
      subject="Test Subject",
      html="<p>Hello!</p>",
    )
  assert "user@example.com" in caplog.text
  assert "Test Subject" in caplog.text
  assert "Hello!" in caplog.text
