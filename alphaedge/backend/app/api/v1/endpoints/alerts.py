from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate
from app.schemas.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[list[AlertRead]])
async def list_alerts(
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[list[AlertRead]]:
    result = await db.execute(
        select(Alert).where(Alert.user_id == current_user.id, Alert.is_deleted == False)
    )
    alerts = result.scalars().all()
    return ApiResponse(success=True, data=[AlertRead.model_validate(a) for a in alerts])


@router.post("", response_model=ApiResponse[AlertRead], status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_in: AlertCreate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[AlertRead]:
    alert = Alert(
        user_id=current_user.id,
        symbol=alert_in.symbol,
        condition=alert_in.condition,
        threshold=alert_in.threshold,
        message=alert_in.message,
    )
    db.add(alert)
    await db.flush()
    await db.refresh(alert)
    return ApiResponse(success=True, data=AlertRead.model_validate(alert), message="Alert created")


@router.patch("/{alert_id}", response_model=ApiResponse[AlertRead])
async def update_alert(
    alert_id: UUID,
    alert_in: AlertUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[AlertRead]:
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id, Alert.user_id == current_user.id, Alert.is_deleted == False)
    )
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    update_data = alert_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(alert, field, value)

    await db.flush()
    await db.refresh(alert)
    return ApiResponse(success=True, data=AlertRead.model_validate(alert), message="Alert updated")


@router.delete("/{alert_id}", status_code=status.HTTP_200_OK)
async def delete_alert(
    alert_id: UUID,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[None]:
    result = await db.execute(
        select(Alert).where(Alert.id == alert_id, Alert.user_id == current_user.id, Alert.is_deleted == False)
    )
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")

    alert.is_deleted = True
    await db.flush()
    return ApiResponse(success=True, message="Alert deleted")
