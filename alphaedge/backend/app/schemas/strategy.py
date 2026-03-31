import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel

from app.models.strategy import StrategyStatus


class StrategyCreate(BaseModel):
    name: str
    description: str = ""
    strategy_type: str
    symbols: list[str]
    parameters: dict[str, Any] = {}
    is_paper: bool = True


class StrategyRead(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    strategy_type: str
    symbols: list[str]
    parameters: dict[str, Any]
    status: StrategyStatus
    is_paper: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class StrategyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    symbols: list[str] | None = None
    parameters: dict[str, Any] | None = None
    status: StrategyStatus | None = None
