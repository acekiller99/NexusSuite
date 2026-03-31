"""Integration tests for Watchlist endpoints — requires PostgreSQL."""
import pytest
from httpx import AsyncClient


async def _auth_header(client: AsyncClient, email: str) -> dict[str, str]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "StrongPass123!", "full_name": "WL User"},
    )
    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "StrongPass123!"},
    )
    token = resp.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_watchlist(client: AsyncClient) -> None:
    headers = await _auth_header(client, "wl_create@example.com")
    response = await client.post(
        "/api/v1/watchlists",
        json={"name": "Tech Stocks"},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Tech Stocks"
    assert data["items"] == []


@pytest.mark.asyncio
async def test_list_watchlists(client: AsyncClient) -> None:
    headers = await _auth_header(client, "wl_list@example.com")
    await client.post("/api/v1/watchlists", json={"name": "List A"}, headers=headers)
    await client.post("/api/v1/watchlists", json={"name": "List B"}, headers=headers)

    response = await client.get("/api/v1/watchlists", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) >= 2


@pytest.mark.asyncio
async def test_add_item_to_watchlist(client: AsyncClient) -> None:
    headers = await _auth_header(client, "wl_additem@example.com")
    resp = await client.post(
        "/api/v1/watchlists", json={"name": "My List"}, headers=headers,
    )
    wid = resp.json()["data"]["id"]

    response = await client.post(
        f"/api/v1/watchlists/{wid}/items",
        json={"symbol": "AAPL", "notes": "Great stock"},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["data"]["symbol"] == "AAPL"
    assert response.json()["data"]["notes"] == "Great stock"


@pytest.mark.asyncio
async def test_add_item_default_notes(client: AsyncClient) -> None:
    headers = await _auth_header(client, "wl_defnotes@example.com")
    resp = await client.post(
        "/api/v1/watchlists", json={"name": "Defaults"}, headers=headers,
    )
    wid = resp.json()["data"]["id"]

    response = await client.post(
        f"/api/v1/watchlists/{wid}/items",
        json={"symbol": "GOOGL"},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["data"]["notes"] == ""


@pytest.mark.asyncio
async def test_remove_item_from_watchlist(client: AsyncClient) -> None:
    headers = await _auth_header(client, "wl_remove@example.com")
    resp = await client.post(
        "/api/v1/watchlists", json={"name": "Remove Test"}, headers=headers,
    )
    wid = resp.json()["data"]["id"]

    resp = await client.post(
        f"/api/v1/watchlists/{wid}/items",
        json={"symbol": "TSLA"},
        headers=headers,
    )
    item_id = resp.json()["data"]["id"]

    response = await client.delete(
        f"/api/v1/watchlists/{wid}/items/{item_id}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_add_item_to_nonexistent_watchlist(client: AsyncClient) -> None:
    headers = await _auth_header(client, "wl_404@example.com")
    response = await client.post(
        "/api/v1/watchlists/00000000-0000-0000-0000-000000000000/items",
        json={"symbol": "AAPL"},
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_remove_nonexistent_item(client: AsyncClient) -> None:
    headers = await _auth_header(client, "wl_noitem@example.com")
    resp = await client.post(
        "/api/v1/watchlists", json={"name": "No Item"}, headers=headers,
    )
    wid = resp.json()["data"]["id"]

    response = await client.delete(
        f"/api/v1/watchlists/{wid}/items/00000000-0000-0000-0000-000000000000",
        headers=headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_watchlists_require_auth(client: AsyncClient) -> None:
    response = await client.get("/api/v1/watchlists")
    assert response.status_code == 401
