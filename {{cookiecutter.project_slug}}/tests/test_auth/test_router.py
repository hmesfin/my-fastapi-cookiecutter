import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
  response = await client.post(
    "/auth/register",
    json={
      "email": "new@example.com",
      "password": "strongpassword123",
      "full_name": "New User",
    },
  )
  assert response.status_code == 201
  data = response.json()
  assert data["email"] == "new@example.com"
  assert data["full_name"] == "New User"
  assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
  payload = {
    "email": "dup@example.com",
    "password": "strongpassword123",
    "full_name": "First",
  }
  await client.post("/auth/register", json=payload)
  response = await client.post("/auth/register", json=payload)
  assert response.status_code == 400
  assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login(client: AsyncClient):
  await client.post(
    "/auth/register",
    json={
      "email": "login@example.com",
      "password": "strongpassword123",
      "full_name": "Login User",
    },
  )
  response = await client.post(
    "/auth/login",
    json={"email": "login@example.com", "password": "strongpassword123"},
  )
  assert response.status_code == 200
  data = response.json()
  assert "access_token" in data
  assert "refresh_token" in data
  assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
  await client.post(
    "/auth/register",
    json={
      "email": "wrongpw@example.com",
      "password": "strongpassword123",
      "full_name": "User",
    },
  )
  response = await client.post(
    "/auth/login",
    json={"email": "wrongpw@example.com", "password": "wrongpassword"},
  )
  assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
  await client.post(
    "/auth/register",
    json={
      "email": "refresh@example.com",
      "password": "strongpassword123",
      "full_name": "Refresh User",
    },
  )
  login_response = await client.post(
    "/auth/login",
    json={"email": "refresh@example.com", "password": "strongpassword123"},
  )
  refresh_token = login_response.json()["refresh_token"]

  response = await client.post(
    "/auth/refresh",
    json={"refresh_token": refresh_token},
  )
  assert response.status_code == 200
  assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_get_me(authenticated_client: AsyncClient):
  response = await authenticated_client.get("/auth/me")
  assert response.status_code == 200
  data = response.json()
  assert data["email"] == "test@example.com"
  assert data["full_name"] == "Test User"


@pytest.mark.asyncio
async def test_update_me(authenticated_client: AsyncClient):
  response = await authenticated_client.patch(
    "/auth/me",
    json={"full_name": "Updated Name"},
  )
  assert response.status_code == 200
  assert response.json()["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_me_unauthenticated(client: AsyncClient):
  response = await client.get("/auth/me")
  assert response.status_code == 401
