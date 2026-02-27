import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from {{ cookiecutter.project_slug }}.db.base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
  __tablename__ = "users"

  email: Mapped[str] = mapped_column(
    String(320),
    unique=True,
    index=True,
    nullable=False,
  )
  hashed_password: Mapped[str] = mapped_column(
    String(1024),
    nullable=False,
  )
  full_name: Mapped[str] = mapped_column(
    String(255),
    default="",
  )
  is_active: Mapped[bool] = mapped_column(
    Boolean,
    default=True,
  )
  is_superuser: Mapped[bool] = mapped_column(
    Boolean,
    default=False,
  )

  def __repr__(self) -> str:
    return f"<User {self.email}>"
