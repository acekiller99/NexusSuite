from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.response import ApiResponse
from app.services.market_data import MarketDataService

router = APIRouter()
market_service = MarketDataService()


@router.get("/quote/{symbol}", response_model=ApiResponse[dict])
async def get_quote(symbol: str) -> ApiResponse[dict]:
    """Get real-time quote for a stock symbol."""
    data = await market_service.get_quote(symbol.upper())
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Symbol {symbol} not found")
    return ApiResponse(success=True, data=data)


@router.get("/history/{symbol}", response_model=ApiResponse[list[dict]])
async def get_history(
    symbol: str,
    period: str = Query("1mo", description="Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max"),
    interval: str = Query("1d", description="Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo"),
) -> ApiResponse[list[dict]]:
    """Get historical price data for a stock symbol."""
    data = await market_service.get_history(symbol.upper(), period=period, interval=interval)
    return ApiResponse(success=True, data=data)


@router.get("/search", response_model=ApiResponse[list[dict]])
async def search_symbols(
    q: str = Query(..., min_length=1, max_length=20, description="Search query"),
) -> ApiResponse[list[dict]]:
    """Search for stock symbols by name or ticker."""
    results = await market_service.search_symbols(q)
    return ApiResponse(success=True, data=results)
