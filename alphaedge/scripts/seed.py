"""
Seed script for AlphaEdge — creates initial data for development.

Usage:
    python scripts/seed.py
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from passlib.context import CryptContext

from app.database import async_session, engine, Base
from app.models.user import User
from app.models.portfolio import Portfolio

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Create demo user
        demo_user = User(
            email="demo@alphaedge.local",
            hashed_password=pwd_context.hash("demo1234"),
            full_name="Demo User",
            is_active=True,
        )
        session.add(demo_user)
        await session.flush()

        # Create demo portfolio
        portfolio = Portfolio(
            user_id=demo_user.id,
            name="Demo Portfolio",
            description="Default paper trading portfolio",
            initial_capital=100_000,
            cash_balance=100_000,
            is_paper=True,
        )
        session.add(portfolio)
        await session.commit()

        print(f"Seeded demo user: demo@alphaedge.local / demo1234")
        print(f"Seeded demo portfolio: {portfolio.name} (${portfolio.initial_capital:,.2f})")


if __name__ == "__main__":
    asyncio.run(seed())
