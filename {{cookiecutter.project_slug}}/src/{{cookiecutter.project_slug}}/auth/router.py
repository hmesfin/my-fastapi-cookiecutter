from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from {{ cookiecutter.project_slug }}.auth.dependencies import get_current_user
from {{ cookiecutter.project_slug }}.auth.models import User
from {{ cookiecutter.project_slug }}.auth.schemas import (
  PasswordReset,
  PasswordResetConfirm,
  RefreshRequest,
  TokenResponse,
  UserLogin,
  UserRegister,
  UserResponse,
  UserUpdate,
)
from {{ cookiecutter.project_slug }}.auth.security import (
  create_access_token,
  create_refresh_token,
  decode_token,
  hash_password,
  verify_password,
)
from {{ cookiecutter.project_slug }}.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(User).where(User.email == data.email))
  if result.scalar_one_or_none() is not None:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already registered",
    )
  user = User(
    email=data.email,
    hashed_password=hash_password(data.password),
    full_name=data.full_name,
  )
  db.add(user)
  await db.flush()
  await db.refresh(user)
  return user


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
  result = await db.execute(select(User).where(User.email == data.email))
  user = result.scalar_one_or_none()
  if user is None or not verify_password(data.password, user.hashed_password):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
    )
  if not user.is_active:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Inactive user",
    )
  return TokenResponse(
    access_token=create_access_token(user.email),
    refresh_token=create_refresh_token(user.email),
  )


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
  try:
    payload = decode_token(data.refresh_token)
    if payload.get("type") != "refresh":
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token type",
      )
    email = payload.get("sub")
  except Exception:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid refresh token",
    )
  result = await db.execute(select(User).where(User.email == email))
  user = result.scalar_one_or_none()
  if user is None or not user.is_active:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid refresh token",
    )
  return TokenResponse(
    access_token=create_access_token(user.email),
    refresh_token=create_refresh_token(user.email),
  )


@router.post("/password-reset", status_code=status.HTTP_202_ACCEPTED)
async def password_reset(data: PasswordReset, db: AsyncSession = Depends(get_db)):
  # Always return 202 to prevent email enumeration
  result = await db.execute(select(User).where(User.email == data.email))
  user = result.scalar_one_or_none()
  if user is not None:
    # TODO: generate reset token and send email
    pass
  return {"detail": "If the email exists, a reset link has been sent."}


@router.post("/password-reset/confirm")
async def password_reset_confirm(
  data: PasswordResetConfirm,
  db: AsyncSession = Depends(get_db),
):
  # TODO: validate reset token, update password
  raise HTTPException(
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    detail="Password reset confirmation not yet implemented",
  )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
  return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
  data: UserUpdate,
  current_user: User = Depends(get_current_user),
  db: AsyncSession = Depends(get_db),
):
  update_data = data.model_dump(exclude_unset=True)
  for field, value in update_data.items():
    setattr(current_user, field, value)
  await db.flush()
  await db.refresh(current_user)
  return current_user
