import asyncio
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
  AsyncSession,
  async_sessionmaker,
  create_async_engine,
)

from {{ cookiecutter.project_slug }}.config import get_settings
from {{ cookiecutter.project_slug }}.db import get_db
from {{ cookiecutter.project_slug }}.db.base import Base
from {{ cookiecutter.project_slug }}.main import app

settings = get_settings()


@pytest.fixture(scope="session")
def event_loop():
  loop = asyncio.new_event_loop()
  yield loop
  loop.close()


@pytest.fixture(scope="session")
async def test_engine():
  engine = create_async_engine(settings.database_url, echo=False)
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  yield engine
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)
  await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
  session_factory = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
  )
  async with session_factory() as session:
    yield session
    await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
  async def override_get_db():
    yield db_session

  app.dependency_overrides[get_db] = override_get_db
  async with AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test",
  ) as ac:
    yield ac
  app.dependency_overrides.clear()


@pytest.fixture
async def authenticated_client(
  client: AsyncClient,
  db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
  from {{ cookiecutter.project_slug }}.auth.models import User
  from {{ cookiecutter.project_slug }}.auth.security import create_access_token, hash_password

  user = User(
    email="test@example.com",
    hashed_password=hash_password("testpassword123"),
    full_name="Test User",
    is_active=True,
  )
  db_session.add(user)
  await db_session.flush()
  await db_session.refresh(user)

  token = create_access_token(user.email)
  client.headers["Authorization"] = f"Bearer {token}"
  yield client
