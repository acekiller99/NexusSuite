"""Integration tests for Alert endpoints — requires PostgreSQL."""
import pytest
from httpx import AsyncClient


async def _auth_header(client: AsyncClient, email: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "StrongPass123!", "full_name": "Alert User"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "StrongPass123!"},
    )
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_alert(client: AsyncClient) -> None:
    headers = await _auth_header(client, "alert_create@example.com")
    response = await client.post(
        "/api/v1/alerts",
        json={
            "symbol": "AAPL",
            "condition": "price_above",
            "threshold": "200.00",
            "message": "AAPL crossed $200",
        },
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["symbol"] == "AAPL"
    assert data["condition"] == "price_above"
    assert data["is_triggered"] is False
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_list_alerts(client: AsyncClient) -> None:
    headers = await _auth_header(client, "alert_list@example.com")
    for sym in ["AAPL", "GOOGL", "TSLA"]:
        await client.post(
            "/api/v1/alerts",
            json={"symbol": sym, "condition": "price_below", "threshold": "100.00"},
            headers=headers,
        )
    response = await client.get("/api/v1/alerts", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 3


@pytest.mark.asyncio
async def test_update_alert(client: AsyncClient) -> None:
    headers = await _auth_header(client, "alert_update@example.com")
    resp = await client.post(
        "/api/v1/alerts",
        json={"symbol": "MSFT", "condition": "price_above", "threshold": "350.00"},
        headers=headers,
    )
    aid = resp.json()["data"]["id"]

    response = await client.patch(
        f"/api/v1/alerts/{aid}",
        json={"threshold": "400.00", "is_active": False},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["threshold"] == "400.0000"
    assert data["is_active"] is False


@pytest.mark.asyncio
async def test_delete_alert_soft_delete(client: AsyncClient) -> None:
    headers = await _auth_header(client, "alert_delete@example.com")
    resp = await client.post(
        "/api/v1/alerts",
        json={"symbol": "NVDA", "condition": "price_below", "threshold": "500.00"},
        headers=headers,
    )
    aid = resp.json()["data"]["id"]

    # Delete
    response = await client.delete(f"/api/v1/alerts/{aid}", headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] is True

    # Should not appear in list anymore
    response = await client.get("/api/v1/alerts", headers=headers)
    assert response.status_code == 200
    ids = [a["id"] for a in response.json()["data"]]
    assert aid not in ids


@pytest.mark.asyncio
async def test_update_nonexistent_alert(client: AsyncClient) -> None:
    headers = await _auth_header(client, "alert_404@example.com")
    response = await client.patch(
        "/api/v1/alerts/00000000-0000-0000-0000-000000000000",
        json={"is_active": False},
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_alert(client: AsyncClient) -> None:
    headers = await _auth_header(client, "alert_del404@example.com")
    response = await client.delete(
        "/api/v1/alerts/00000000-0000-0000-0000-000000000000",
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_alert_all_conditions(client: AsyncClient) -> None:
    headers = await _auth_header(client, "alert_cond@example.com")
    conditions = ["price_above", "price_below", "percent_change_up", "percent_change_down"]
    for cond in conditions:
        response = await client.post(
            "/api/v1/alerts",
            json={"symbol": "SPY", "condition": cond, "threshold": "5.00"},
            headers=headers,
        )
        assert response.status_code == 201, f"Failed for condition: {cond}"
        assert response.json()["data"]["condition"] == cond


@pytest.mark.asyncio
async def test_alerts_require_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/alerts")
    assert response.status_code == 401
