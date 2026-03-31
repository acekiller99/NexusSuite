"""Tests for WebSocket ConnectionManager — no database needed."""
import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.websockets import ConnectionManager


@pytest.fixture
def manager() -> ConnectionManager:
    return ConnectionManager()


def _make_ws() -> AsyncMock:
    """Create a mock WebSocket."""
    ws = AsyncMock()
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    return ws


class TestConnectionManager:
    @pytest.mark.asyncio
    async def test_connect_accepts_websocket(self, manager: ConnectionManager) -> None:
        ws = _make_ws()
        await manager.connect(ws, "test-channel")
        ws.accept.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_connect_adds_to_channel(self, manager: ConnectionManager) -> None:
        ws = _make_ws()
        await manager.connect(ws, "ch1")
        assert "ch1" in manager.active_connections
        assert ws in manager.active_connections["ch1"]

    @pytest.mark.asyncio
    async def test_connect_multiple_to_same_channel(self, manager: ConnectionManager) -> None:
        ws1 = _make_ws()
        ws2 = _make_ws()
        await manager.connect(ws1, "ch")
        await manager.connect(ws2, "ch")
        assert len(manager.active_connections["ch"]) == 2

    @pytest.mark.asyncio
    async def test_connect_to_different_channels(self, manager: ConnectionManager) -> None:
        ws1 = _make_ws()
        ws2 = _make_ws()
        await manager.connect(ws1, "ch1")
        await manager.connect(ws2, "ch2")
        assert "ch1" in manager.active_connections
        assert "ch2" in manager.active_connections

    @pytest.mark.asyncio
    async def test_disconnect_removes_websocket(self, manager: ConnectionManager) -> None:
        ws = _make_ws()
        await manager.connect(ws, "ch")
        manager.disconnect(ws, "ch")
        assert "ch" not in manager.active_connections

    @pytest.mark.asyncio
    async def test_disconnect_keeps_other_connections(self, manager: ConnectionManager) -> None:
        ws1 = _make_ws()
        ws2 = _make_ws()
        await manager.connect(ws1, "ch")
        await manager.connect(ws2, "ch")
        manager.disconnect(ws1, "ch")
        assert len(manager.active_connections["ch"]) == 1
        assert ws2 in manager.active_connections["ch"]

    @pytest.mark.asyncio
    async def test_disconnect_removes_empty_channel(self, manager: ConnectionManager) -> None:
        ws = _make_ws()
        await manager.connect(ws, "ch")
        manager.disconnect(ws, "ch")
        assert "ch" not in manager.active_connections

    @pytest.mark.asyncio
    async def test_broadcast_sends_to_all_in_channel(self, manager: ConnectionManager) -> None:
        ws1 = _make_ws()
        ws2 = _make_ws()
        await manager.connect(ws1, "ch")
        await manager.connect(ws2, "ch")

        msg = {"type": "price", "symbol": "AAPL", "price": 150.0}
        await manager.broadcast(msg, "ch")

        ws1.send_json.assert_awaited_once_with(msg)
        ws2.send_json.assert_awaited_once_with(msg)

    @pytest.mark.asyncio
    async def test_broadcast_only_to_target_channel(self, manager: ConnectionManager) -> None:
        ws1 = _make_ws()
        ws2 = _make_ws()
        await manager.connect(ws1, "ch1")
        await manager.connect(ws2, "ch2")

        await manager.broadcast({"data": 1}, "ch1")

        ws1.send_json.assert_awaited_once()
        ws2.send_json.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_broadcast_to_nonexistent_channel_is_noop(self, manager: ConnectionManager) -> None:
        # Should not raise
        await manager.broadcast({"data": 1}, "nonexistent")

    @pytest.mark.asyncio
    async def test_broadcast_handles_send_failure(self, manager: ConnectionManager) -> None:
        ws1 = _make_ws()
        ws2 = _make_ws()
        ws1.send_json.side_effect = RuntimeError("connection closed")
        await manager.connect(ws1, "ch")
        await manager.connect(ws2, "ch")

        # Should not raise — failed sends are logged and skipped
        await manager.broadcast({"data": 1}, "ch")
        ws2.send_json.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_default_channel(self, manager: ConnectionManager) -> None:
        ws = _make_ws()
        await manager.connect(ws)  # uses "default" channel
        assert "default" in manager.active_connections

    @pytest.mark.asyncio
    async def test_disconnect_from_default_channel(self, manager: ConnectionManager) -> None:
        ws = _make_ws()
        await manager.connect(ws)
        manager.disconnect(ws)
        assert "default" not in manager.active_connections
