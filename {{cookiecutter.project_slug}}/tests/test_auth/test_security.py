import pytest
from jwt.exceptions import InvalidTokenError

from {{ cookiecutter.project_slug }}.auth.security import (
  create_access_token,
  create_refresh_token,
  decode_token,
  hash_password,
  verify_password,
)


def test_hash_and_verify_password():
  hashed = hash_password("mysecretpassword")
  assert hashed != "mysecretpassword"
  assert verify_password("mysecretpassword", hashed)
  assert not verify_password("wrongpassword", hashed)


def test_create_and_decode_access_token():
  token = create_access_token("user@example.com")
  payload = decode_token(token)
  assert payload["sub"] == "user@example.com"
  assert payload["type"] == "access"


def test_create_and_decode_refresh_token():
  token = create_refresh_token("user@example.com")
  payload = decode_token(token)
  assert payload["sub"] == "user@example.com"
  assert payload["type"] == "refresh"


def test_decode_invalid_token():
  with pytest.raises(InvalidTokenError):
    decode_token("invalid.token.here")
