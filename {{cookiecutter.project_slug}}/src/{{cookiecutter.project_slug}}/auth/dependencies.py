from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from {{ cookiecutter.project_slug }}.auth.models import User
from {{ cookiecutter.project_slug }}.auth.security import decode_token
from {{ cookiecutter.project_slug }}.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
  token: str = Depends(oauth2_scheme),
  db: AsyncSession = Depends(get_db),
) -> User:
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = decode_token(token)
    email: str | None = payload.get("sub")
    token_type: str | None = payload.get("type")
    if email is None or token_type != "access":
      raise credentials_exception
  except InvalidTokenError:
    raise credentials_exception

  result = await db.execute(select(User).where(User.email == email))
  user = result.scalar_one_or_none()
  if user is None or not user.is_active:
    raise credentials_exception
  return user


async def get_current_superuser(
  current_user: User = Depends(get_current_user),
) -> User:
  if not current_user.is_superuser:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Not enough permissions",
    )
  return current_user
