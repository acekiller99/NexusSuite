import uuid
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, Numeric, String, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AlertCondition(str, PyEnum):
    PRICE_ABOVE = "price_above"
    PRICE_BELOW = "price_below"
    PERCENT_CHANGE_UP = "percent_change_up"
    PERCENT_CHANGE_DOWN = "percent_change_down"


class Alert(Base):
    __tablename__ = "alerts"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    condition: Mapped[AlertCondition] = mapped_column(Enum(AlertCondition), nullable=False)
    threshold: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False)
    is_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    message: Mapped[str] = mapped_column(String(500), default="")

    # Relationships
    user = relationship("User", back_populates="alerts")
