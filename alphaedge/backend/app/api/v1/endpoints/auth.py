from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, create_access_token, create_refresh_token
from app.database import get_db
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.user import Token, UserCreate, UserRead

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=ApiResponse[UserRead], status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[UserRead]:
    # Check for existing user
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=pwd_context.hash(user_in.password),
        full_name=user_in.full_name,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    return ApiResponse(success=True, data=UserRead.model_validate(user), message="User registered successfully")


@router.post("/login", response_model=ApiResponse[Token])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApiResponse[Token]:
    result = await db.execute(select(User).where(User.email == form_data.username, User.is_deleted == False))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")

    token = Token(
        access_token=create_access_token(str(user.id)),
        refresh_token=create_refresh_token(str(user.id)),
    )
    return ApiResponse(success=True, data=token, message="Login successful")


@router.get("/me", response_model=ApiResponse[UserRead])
async def get_me(current_user: CurrentUser) -> ApiResponse[UserRead]:
    return ApiResponse(success=True, data=UserRead.model_validate(current_user))
