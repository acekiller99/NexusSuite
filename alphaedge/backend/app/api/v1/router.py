from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, portfolios, strategies, orders, watchlists, alerts, market_data

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["strategies"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(watchlists.router, prefix="/watchlists", tags=["watchlists"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(market_data.router, prefix="/market", tags=["market-data"])
