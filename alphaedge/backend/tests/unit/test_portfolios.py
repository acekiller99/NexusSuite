import pytest
from httpx import AsyncClient


async def _get_auth_header(client: AsyncClient) -> dict[str, str]:
    """Helper to register + login and return auth header."""
    await client.post(
        "/api/v1/auth/register",
        json={"email": "portfolio@example.com", "password": "StrongPass123!", "full_name": "Portfolio User"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "portfolio@example.com", "password": "StrongPass123!"},
    )
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_and_list_portfolios(client: AsyncClient) -> None:
    headers = await _get_auth_header(client)

    # Create portfolio
    response = await client.post(
        "/api/v1/portfolios",
        json={"name": "Test Portfolio", "initial_capital": "50000.00", "is_paper": True},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["name"] == "Test Portfolio"
    portfolio_id = data["data"]["id"]

    # List portfolios
    response = await client.get("/api/v1/portfolios", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 1

    # Get single portfolio
    response = await client.get(f"/api/v1/portfolios/{portfolio_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == portfolio_id
