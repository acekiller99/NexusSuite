from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.database import get_db
from app.models.strategy import Strategy
from app.schemas.response import ApiResponse
from app.schemas.strategy import StrategyCreate, StrategyRead, StrategyUpdate

router = APIRouter()


@router.get("", response_model=ApiResponse[list[StrategyRead]])
async def list_strategies(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[list[StrategyRead]]:
    result = await db.execute(
        select(Strategy).where(Strategy.user_id == current_user.id, Strategy.is_deleted == False)
    )
    strategies = result.scalars().all()
    return ApiResponse(success=True, data=[StrategyRead.model_validate(s) for s in strategies])


@router.post("", response_model=ApiResponse[StrategyRead], status_code=status.HTTP_201_CREATED)
async def create_strategy(
    strategy_in: StrategyCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[StrategyRead]:
    strategy = Strategy(
        user_id=current_user.id,
        name=strategy_in.name,
        description=strategy_in.description,
        strategy_type=strategy_in.strategy_type,
        symbols=strategy_in.symbols,
        parameters=strategy_in.parameters,
        is_paper=strategy_in.is_paper,
    )
    db.add(strategy)
    await db.flush()
    await db.refresh(strategy)
    return ApiResponse(success=True, data=StrategyRead.model_validate(strategy), message="Strategy created")


@router.get("/{strategy_id}", response_model=ApiResponse[StrategyRead])
async def get_strategy(
    strategy_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[StrategyRead]:
    result = await db.execute(
        select(Strategy).where(
            Strategy.id == strategy_id, Strategy.user_id == current_user.id, Strategy.is_deleted == False
        )
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    return ApiResponse(success=True, data=StrategyRead.model_validate(strategy))


@router.patch("/{strategy_id}", response_model=ApiResponse[StrategyRead])
async def update_strategy(
    strategy_id: UUID,
    strategy_in: StrategyUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[StrategyRead]:
    result = await db.execute(
        select(Strategy).where(
            Strategy.id == strategy_id, Strategy.user_id == current_user.id, Strategy.is_deleted == False
        )
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")

    update_data = strategy_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(strategy, field, value)

    await db.flush()
    await db.refresh(strategy)
    return ApiResponse(success=True, data=StrategyRead.model_validate(strategy), message="Strategy updated")
