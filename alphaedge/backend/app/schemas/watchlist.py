import uuid
from datetime import datetime

from pydantic import BaseModel


class WatchlistItemCreate(BaseModel):
    symbol: str
    notes: str = ""


class WatchlistItemRead(BaseModel):
    id: uuid.UUID
    symbol: str
    notes: str
    created_at: datetime

    model_config = {"from_attributes": True}


class WatchlistCreate(BaseModel):
    name: str


class WatchlistRead(BaseModel):
    id: uuid.UUID
    name: str
    items: list[WatchlistItemRead] = []
    created_at: datetime

    model_config = {"from_attributes": True}
