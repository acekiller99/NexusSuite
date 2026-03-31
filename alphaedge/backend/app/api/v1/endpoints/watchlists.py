from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.database import get_db
from app.models.watchlist import Watchlist, WatchlistItem
from app.schemas.response import ApiResponse
from app.schemas.watchlist import WatchlistCreate, WatchlistItemCreate, WatchlistItemRead, WatchlistRead

router = APIRouter()


@router.get("", response_model=ApiResponse[list[WatchlistRead]])
async def list_watchlists(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[list[WatchlistRead]]:
    result = await db.execute(
        select(Watchlist).where(Watchlist.user_id == current_user.id, Watchlist.is_deleted == False)
    )
    watchlists = result.scalars().all()
    return ApiResponse(success=True, data=[WatchlistRead.model_validate(w) for w in watchlists])


@router.post("", response_model=ApiResponse[WatchlistRead], status_code=status.HTTP_201_CREATED)
async def create_watchlist(
    watchlist_in: WatchlistCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[WatchlistRead]:
    watchlist = Watchlist(user_id=current_user.id, name=watchlist_in.name)
    db.add(watchlist)
    await db.flush()
    await db.refresh(watchlist)
    return ApiResponse(success=True, data=WatchlistRead.model_validate(watchlist), message="Watchlist created")


@router.post("/{watchlist_id}/items", response_model=ApiResponse[WatchlistItemRead], status_code=status.HTTP_201_CREATED)
async def add_watchlist_item(
    watchlist_id: UUID,
    item_in: WatchlistItemCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[WatchlistItemRead]:
    result = await db.execute(
        select(Watchlist).where(
            Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id, Watchlist.is_deleted == False
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist not found")

    item = WatchlistItem(watchlist_id=watchlist_id, symbol=item_in.symbol, notes=item_in.notes)
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return ApiResponse(success=True, data=WatchlistItemRead.model_validate(item), message="Item added")


@router.delete("/{watchlist_id}/items/{item_id}", status_code=status.HTTP_200_OK)
async def remove_watchlist_item(
    watchlist_id: UUID,
    item_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[None]:
    result = await db.execute(
        select(Watchlist).where(
            Watchlist.id == watchlist_id, Watchlist.user_id == current_user.id, Watchlist.is_deleted == False
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Watchlist not found")

    result = await db.execute(
        select(WatchlistItem).where(WatchlistItem.id == item_id, WatchlistItem.watchlist_id == watchlist_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    await db.delete(item)
    return ApiResponse(success=True, message="Item removed")
