import logging
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for real-time market data and notifications."""

    def __init__(self) -> None:
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel: str = "default") -> None:
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)
        logger.info("WebSocket connected to channel: %s", channel)

    def disconnect(self, websocket: WebSocket, channel: str = "default") -> None:
        if channel in self.active_connections:
            self.active_connections[channel].remove(websocket)
            if not self.active_connections[channel]:
                del self.active_connections[channel]
        logger.info("WebSocket disconnected from channel: %s", channel)

    async def broadcast(self, message: dict[str, Any], channel: str = "default") -> None:
        if channel not in self.active_connections:
            return
        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except Exception:
                logger.warning("Failed to send message to WebSocket in channel %s", channel)


manager = ConnectionManager()
