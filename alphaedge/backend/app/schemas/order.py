import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.order import OrderSide, OrderType, OrderStatus


class OrderCreate(BaseModel):
    portfolio_id: uuid.UUID
    strategy_id: uuid.UUID | None = None
    symbol: str
    side: OrderSide
    order_type: OrderType = OrderType.MARKET
    quantity: int
    limit_price: Decimal | None = None
    stop_price: Decimal | None = None


class OrderRead(BaseModel):
    id: uuid.UUID
    portfolio_id: uuid.UUID
    strategy_id: uuid.UUID | None
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: int
    limit_price: Decimal | None
    stop_price: Decimal | None
    filled_price: Decimal | None
    filled_quantity: int | None
    status: OrderStatus
    broker_order_id: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
