from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.database import get_db
from app.models.portfolio import Portfolio, Position
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PositionRead
from app.schemas.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[list[PortfolioRead]])
async def list_portfolios(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[list[PortfolioRead]]:
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id, Portfolio.is_deleted == False)
    )
    portfolios = result.scalars().all()
    return ApiResponse(success=True, data=[PortfolioRead.model_validate(p) for p in portfolios])


@router.post("", response_model=ApiResponse[PortfolioRead], status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio_in: PortfolioCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[PortfolioRead]:
    portfolio = Portfolio(
        user_id=current_user.id,
        name=portfolio_in.name,
        description=portfolio_in.description,
        initial_capital=portfolio_in.initial_capital,
        cash_balance=portfolio_in.initial_capital,
        is_paper=portfolio_in.is_paper,
    )
    db.add(portfolio)
    await db.flush()
    await db.refresh(portfolio)
    return ApiResponse(success=True, data=PortfolioRead.model_validate(portfolio), message="Portfolio created")


@router.get("/{portfolio_id}", response_model=ApiResponse[PortfolioRead])
async def get_portfolio(
    portfolio_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[PortfolioRead]:
    result = await db.execute(
        select(Portfolio).where(
            Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id, Portfolio.is_deleted == False
        )
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")
    return ApiResponse(success=True, data=PortfolioRead.model_validate(portfolio))


@router.get("/{portfolio_id}/positions", response_model=ApiResponse[list[PositionRead]])
async def list_positions(
    portfolio_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[list[PositionRead]]:
    # Verify ownership
    result = await db.execute(
        select(Portfolio).where(
            Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id, Portfolio.is_deleted == False
        )
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    result = await db.execute(
        select(Position).where(Position.portfolio_id == portfolio_id, Position.is_deleted == False)
    )
    positions = result.scalars().all()
    return ApiResponse(success=True, data=[PositionRead.model_validate(p) for p in positions])
