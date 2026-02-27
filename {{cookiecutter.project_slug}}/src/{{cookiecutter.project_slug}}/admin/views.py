from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from {{ cookiecutter.project_slug }}.auth.models import User
from {{ cookiecutter.project_slug }}.auth.security import verify_password
from {{ cookiecutter.project_slug }}.config import get_settings
from {{ cookiecutter.project_slug }}.db import async_session


class AdminAuth(AuthenticationBackend):
  async def login(self, request: Request) -> bool:
    form = await request.form()
    email = form.get("username", "")
    password = form.get("password", "")

    async with async_session() as session:
      from sqlalchemy import select

      result = await session.execute(
        select(User).where(User.email == email)
      )
      user = result.scalar_one_or_none()
      if user and user.is_superuser and verify_password(password, user.hashed_password):
        request.session.update({"user_id": str(user.id)})
        return True
    return False

  async def logout(self, request: Request) -> bool:
    request.session.clear()
    return True

  async def authenticate(self, request: Request) -> RedirectResponse | bool:
    user_id = request.session.get("user_id")
    if not user_id:
      return RedirectResponse(request.url_for("admin:login"), status_code=302)
    return True


class UserAdmin(ModelView, model=User):
  column_list = [User.id, User.email, User.full_name, User.is_active, User.is_superuser, User.created_at]
  column_searchable_list = [User.email, User.full_name]
  column_sortable_list = [User.email, User.created_at]
  column_details_exclude_list = [User.hashed_password]
  can_create = True
  can_edit = True
  can_delete = True
  name = "User"
  name_plural = "Users"
  icon = "fa-solid fa-user"


def setup_admin(app: FastAPI, engine) -> Admin:
  settings = get_settings()
  authentication_backend = AdminAuth(secret_key=settings.secret_key)
  admin = Admin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title=f"{settings.project_name} Admin",
  )
  admin.add_view(UserAdmin)
  return admin
