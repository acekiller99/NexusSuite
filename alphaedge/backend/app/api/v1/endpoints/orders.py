from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.database import get_db
from app.models.order import Order
from app.models.portfolio import Portfolio
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[list[OrderRead]])
async def list_orders(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
    portfolio_id: UUID | None = Query(None),
) -> ApiResponse[list[OrderRead]]:
    query = (
        select(Order)
        .join(Portfolio)
        .where(Portfolio.user_id == current_user.id, Order.is_deleted == False)
    )
    if portfolio_id:
        query = query.where(Order.portfolio_id == portfolio_id)

    result = await db.execute(query.order_by(Order.created_at.desc()))
    orders = result.scalars().all()
    return ApiResponse(success=True, data=[OrderRead.model_validate(o) for o in orders])


@router.post("", response_model=ApiResponse[OrderRead], status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[OrderRead]:
    # Verify portfolio ownership
    result = await db.execute(
        select(Portfolio).where(
            Portfolio.id == order_in.portfolio_id, Portfolio.user_id == current_user.id, Portfolio.is_deleted == False
        )
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio not found")

    order = Order(
        portfolio_id=order_in.portfolio_id,
        strategy_id=order_in.strategy_id,
        symbol=order_in.symbol,
        side=order_in.side,
        order_type=order_in.order_type,
        quantity=order_in.quantity,
        limit_price=order_in.limit_price,
        stop_price=order_in.stop_price,
    )
    db.add(order)
    await db.flush()
    await db.refresh(order)
    return ApiResponse(success=True, data=OrderRead.model_validate(order), message="Order placed")


@router.get("/{order_id}", response_model=ApiResponse[OrderRead])
async def get_order(
    order_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[OrderRead]:
    result = await db.execute(
        select(Order)
        .join(Portfolio)
        .where(Order.id == order_id, Portfolio.user_id == current_user.id, Order.is_deleted == False)
    )
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return ApiResponse(success=True, data=OrderRead.model_validate(order))
