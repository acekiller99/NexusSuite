from fastapi import APIRouter

from app.schemas.response import ApiResponse

router = APIRouter()


@router.get("", response_model=ApiResponse[dict])
async def health_check() -> ApiResponse[dict]:
    return ApiResponse(
        success=True,
        data={"status": "healthy", "service": "alphaedge"},
        message="Service is running",
    )
