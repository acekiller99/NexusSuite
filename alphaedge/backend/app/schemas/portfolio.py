import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PortfolioCreate(BaseModel):
    name: str
    description: str = ""
    initial_capital: Decimal = Decimal("10000.00")
    is_paper: bool = True


class PortfolioRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    initial_capital: Decimal
    cash_balance: Decimal
    is_paper: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PositionRead(BaseModel):
    id: uuid.UUID
    portfolio_id: uuid.UUID
    symbol: str
    quantity: int
    avg_entry_price: Decimal
    current_price: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}

    @property
    def market_value(self) -> Decimal:
        return self.current_price * self.quantity

    @property
    def unrealized_pnl(self) -> Decimal:
        return (self.current_price - self.avg_entry_price) * self.quantity
