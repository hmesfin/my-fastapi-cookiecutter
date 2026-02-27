import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
  email: EmailStr
  password: str = Field(min_length=8, max_length=128)
  full_name: str = ""


class UserLogin(BaseModel):
  email: EmailStr
  password: str


class UserResponse(BaseModel):
  id: uuid.UUID
  email: EmailStr
  full_name: str
  is_active: bool
  is_superuser: bool
  created_at: datetime

  model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
  full_name: str | None = None
  email: EmailStr | None = None


class TokenResponse(BaseModel):
  access_token: str
  refresh_token: str
  token_type: str = "bearer"


class RefreshRequest(BaseModel):
  refresh_token: str


class PasswordReset(BaseModel):
  email: EmailStr


class PasswordResetConfirm(BaseModel):
  token: str
  new_password: str = Field(min_length=8, max_length=128)
