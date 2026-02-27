from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from {{ cookiecutter.project_slug }}.config import get_settings

password_hash = PasswordHash.recommended()
settings = get_settings()


def hash_password(password: str) -> str:
  return password_hash.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
  return password_hash.verify(plain, hashed)


def create_access_token(sub: str) -> str:
  expire = datetime.now(timezone.utc) + timedelta(
    minutes=settings.access_token_expire_minutes,
  )
  payload = {"sub": sub, "exp": expire, "type": "access"}
  return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(sub: str) -> str:
  expire = datetime.now(timezone.utc) + timedelta(
    days=settings.refresh_token_expire_days,
  )
  payload = {"sub": sub, "exp": expire, "type": "refresh"}
  return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
  return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
