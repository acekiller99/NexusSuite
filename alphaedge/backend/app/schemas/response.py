from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = 1
    per_page: int = 20
    total: int = 0
    total_pages: int = 0


class ApiResponse(BaseModel, Generic[T]):
    """Standardized API response envelope."""

    success: bool = True
    data: T | None = None
    message: str = ""
    errors: list[str] = []


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response envelope."""

    success: bool = True
    data: list[T] = []
    message: str = ""
    errors: list[str] = []
    meta: PaginationMeta = PaginationMeta()
