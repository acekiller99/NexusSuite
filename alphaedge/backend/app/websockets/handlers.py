import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websockets import manager

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/market/{symbol}")
async def market_feed(websocket: WebSocket, symbol: str) -> None:
    """WebSocket endpoint for real-time market data feed."""
    channel = f"market:{symbol.upper()}"
    await manager.connect(websocket, channel)
    try:
        while True:
            # Keep connection alive; actual data push comes from background tasks
            data = await websocket.receive_text()
            # Client can send commands like subscribe/unsubscribe
            logger.debug("Received from client on %s: %s", channel, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)


@router.websocket("/ws/notifications")
async def notifications_feed(websocket: WebSocket) -> None:
    """WebSocket endpoint for user notifications (alerts, order fills, etc.)."""
    channel = "notifications"
    await manager.connect(websocket, channel)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel)
