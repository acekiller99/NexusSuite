import uuid
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, Numeric, String, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OrderSide(str, PyEnum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, PyEnum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(str, PyEnum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class Order(Base):
    __tablename__ = "orders"

    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False, index=True
    )
    strategy_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=True, index=True
    )
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    side: Mapped[OrderSide] = mapped_column(Enum(OrderSide), nullable=False)
    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType), nullable=False, default=OrderType.MARKET)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    limit_price: Mapped[Decimal | None] = mapped_column(Numeric(15, 4), nullable=True)
    stop_price: Mapped[Decimal | None] = mapped_column(Numeric(15, 4), nullable=True)
    filled_price: Mapped[Decimal | None] = mapped_column(Numeric(15, 4), nullable=True)
    filled_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    broker_order_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    portfolio = relationship("Portfolio", back_populates="orders")
