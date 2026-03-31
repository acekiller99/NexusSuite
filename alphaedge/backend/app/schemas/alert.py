import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.alert import AlertCondition


class AlertCreate(BaseModel):
    symbol: str
    condition: AlertCondition
    threshold: Decimal
    message: str = ""


class AlertRead(BaseModel):
    id: uuid.UUID
    symbol: str
    condition: AlertCondition
    threshold: Decimal
    is_triggered: bool
    is_active: bool
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AlertUpdate(BaseModel):
    condition: AlertCondition | None = None
    threshold: Decimal | None = None
    is_active: bool | None = None
    message: str | None = None
