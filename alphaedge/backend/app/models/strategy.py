import uuid
from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, String, Text, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StrategyStatus(str, PyEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"


class Strategy(Base):
    __tablename__ = "strategies"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    strategy_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "sma_crossover", "rsi", "macd"
    symbols: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)  # list of ticker symbols
    parameters: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)  # strategy-specific params
    status: Mapped[StrategyStatus] = mapped_column(
        Enum(StrategyStatus), default=StrategyStatus.DRAFT, nullable=False
    )
    is_paper: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="strategies")
