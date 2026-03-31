import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient) -> None:
    # Register
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "StrongPass123!",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test@example.com"

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "StrongPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    await client.post(
        "/api/v1/auth/register",
        json={"email": "dupe@example.com", "password": "StrongPass123!", "full_name": "Dupe"},
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": "dupe@example.com", "password": "StrongPass123!", "full_name": "Dupe"},
    )
    assert response.status_code == 409
