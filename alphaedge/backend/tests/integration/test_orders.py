"""Integration tests for Order endpoints — requires PostgreSQL."""
import pytest
from httpx import AsyncClient


async def _setup_user_portfolio(client: AsyncClient, email: str) -> tuple[dict[str, str], str]:
    """Register user, login, create portfolio, return (headers, portfolio_id)."""
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "StrongPass123!", "full_name": "Order User"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "StrongPass123!"},
    )
    token = resp.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await client.post(
        "/api/v1/portfolios",
        json={"name": "Trading Portfolio", "initial_capital": "100000.00"},
        headers=headers,
    )
    portfolio_id = resp.json()["data"]["id"]
    return headers, portfolio_id


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient) -> None:
    headers, pid = await _setup_user_portfolio(client, "order_create@example.com")
    response = await client.post(
        "/api/v1/orders",
        json={
            "portfolio_id": pid,
            "symbol": "AAPL",
            "side": "buy",
            "order_type": "market",
            "quantity": 10,
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["symbol"] == "AAPL"
    assert data["side"] == "buy"
    assert data["quantity"] == 10
    assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_create_limit_order(client: AsyncClient) -> None:
    headers, pid = await _setup_user_portfolio(client, "order_limit@example.com")
    response = await client.post(
        "/api/v1/orders",
        json={
            "portfolio_id": pid,
            "symbol": "MSFT",
            "side": "buy",
            "order_type": "limit",
            "quantity": 5,
            "limit_price": "400.50",
        },
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["data"]["order_type"] == "limit"
    assert response.json()["data"]["limit_price"] == "400.5000"


@pytest.mark.asyncio
async def test_list_orders(client: AsyncClient) -> None:
    headers, pid = await _setup_user_portfolio(client, "order_list@example.com")
    # Create two orders
    for sym in ["AAPL", "GOOGL"]:
        await client.post(
            "/api/v1/orders",
            json={"portfolio_id": pid, "symbol": sym, "side": "buy", "order_type": "market", "quantity": 1},
            headers=headers,
        )
    response = await client.get("/api/v1/orders", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 2


@pytest.mark.asyncio
async def test_list_orders_filter_by_portfolio(client: AsyncClient) -> None:
    headers, pid = await _setup_user_portfolio(client, "order_filter@example.com")
    await client.post(
        "/api/v1/orders",
        json={"portfolio_id": pid, "symbol": "SPY", "side": "buy", "order_type": "market", "quantity": 1},
        headers=headers,
    )
    response = await client.get(f"/api/v1/orders?portfolio_id={pid}", headers=headers)
    assert response.status_code == 200
    for order in response.json()["data"]:
        assert order["portfolio_id"] == pid


@pytest.mark.asyncio
async def test_get_order(client: AsyncClient) -> None:
    headers, pid = await _setup_user_portfolio(client, "order_get@example.com")
    resp = await client.post(
        "/api/v1/orders",
        json={"portfolio_id": pid, "symbol": "TSLA", "side": "sell", "order_type": "market", "quantity": 3},
        headers=headers,
    )
    oid = resp.json()["data"]["id"]

    response = await client.get(f"/api/v1/orders/{oid}", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["id"] == oid


@pytest.mark.asyncio
async def test_order_with_invalid_portfolio(client: AsyncClient) -> None:
    headers, _ = await _setup_user_portfolio(client, "order_badpf@example.com")
    response = await client.post(
        "/api/v1/orders",
        json={
            "portfolio_id": "00000000-0000-0000-0000-000000000000",
            "symbol": "X",
            "side": "buy",
            "order_type": "market",
            "quantity": 1,
        },
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_orders_require_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/orders")
    assert response.status_code == 401
