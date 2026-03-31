"""Integration tests for Strategy endpoints — requires PostgreSQL."""
import pytest
from httpx import AsyncClient


async def _auth_header(client: AsyncClient, email: str = "strategy@example.com") -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "StrongPass123!", "full_name": "Strategy User"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "StrongPass123!"},
    )
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_strategy(client: AsyncClient) -> None:
    headers = await _auth_header(client, "strat_create@example.com")
    response = await client.post(
        "/api/v1/strategies",
        json={
            "name": "SMA Crossover",
            "strategy_type": "sma_crossover",
            "symbols": ["AAPL", "GOOGL"],
            "parameters": {"fast_period": 10, "slow_period": 50},
            "is_paper": True,
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "SMA Crossover"
    assert data["data"]["status"] == "draft"
    assert data["data"]["symbols"] == ["AAPL", "GOOGL"]


@pytest.mark.asyncio
async def test_list_strategies(client: AsyncClient) -> None:
    headers = await _auth_header(client, "strat_list@example.com")
    # Create two strategies
    for name in ["Strategy A", "Strategy B"]:
        await client.post(
            "/api/v1/strategies",
            json={"name": name, "strategy_type": "rsi", "symbols": ["SPY"]},
            headers=headers,
        )
    response = await client.get("/api/v1/strategies", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 2


@pytest.mark.asyncio
async def test_get_strategy(client: AsyncClient) -> None:
    headers = await _auth_header(client, "strat_get@example.com")
    resp = await client.post(
        "/api/v1/strategies",
        json={"name": "Get Me", "strategy_type": "macd", "symbols": ["MSFT"]},
        headers=headers,
    )
    sid = resp.json()["data"]["id"]

    response = await client.get(f"/api/v1/strategies/{sid}", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == sid
    assert response.json()["data"]["name"] == "Get Me"


@pytest.mark.asyncio
async def test_update_strategy(client: AsyncClient) -> None:
    headers = await _auth_header(client, "strat_update@example.com")
    resp = await client.post(
        "/api/v1/strategies",
        json={"name": "Original", "strategy_type": "rsi", "symbols": ["TSLA"]},
        headers=headers,
    )
    sid = resp.json()["data"]["id"]

    response = await client.patch(
        f"/api/v1/strategies/{sid}",
        json={"name": "Updated", "status": "active"},
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Updated"
    assert response.json()["data"]["status"] == "active"


@pytest.mark.asyncio
async def test_get_nonexistent_strategy(client: AsyncClient) -> None:
    headers = await _auth_header(client, "strat_404@example.com")
    response = await client.get(
        "/api/v1/strategies/00000000-0000-0000-0000-000000000000",
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_strategy_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/strategies")
    assert response.status_code == 401
