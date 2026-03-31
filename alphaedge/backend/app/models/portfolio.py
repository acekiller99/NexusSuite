import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), default="")
    initial_capital: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=Decimal("10000.00"))
    cash_balance: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, default=Decimal("10000.00"))
    is_paper: Mapped[bool] = mapped_column(default=True)

    # Relationships
    user = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio", lazy="selectin")
    orders = relationship("Order", back_populates="portfolio", lazy="selectin")


class Position(Base):
    __tablename__ = "positions"

    portfolio_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("portfolios.id"), nullable=False, index=True
    )
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_entry_price: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=Decimal("0"))
    current_price: Mapped[Decimal] = mapped_column(Numeric(15, 4), nullable=False, default=Decimal("0"))

    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
