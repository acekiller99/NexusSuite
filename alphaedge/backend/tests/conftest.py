"""
Shared test fixtures for AlphaEdge backend.

Unit tests (tests/unit/) run WITHOUT a database — they test schemas,
JWT tokens, config, WebSocket manager, etc.

Integration tests (tests/integration/) require a running PostgreSQL
instance.  They are auto-skipped when the database is unreachable.
"""
import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.config import settings

# ---------------------------------------------------------------------------
# Detect whether PostgreSQL is available for integration tests
# ---------------------------------------------------------------------------
_DB_URL: str = os.environ.get("DATABASE_URL", settings.database_url)
_db_available: bool = False
_db_verified: bool = False

try:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
    from app.database import Base, get_db
    from app.main import app

    engine_test = create_async_engine(_DB_URL, echo=False)
    async_session_test = async_sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
    _db_available = True
except Exception:
    engine_test = None  # type: ignore[assignment]
    async_session_test = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Session-scoped event loop (needed by pytest-asyncio)
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ---------------------------------------------------------------------------
# Integration-test fixtures — only activate when DB is reachable
# ---------------------------------------------------------------------------
@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """Create all tables at the start of the test session, drop at the end."""
    global _db_verified
    if not _db_available:
        yield
        return

    try:
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        _db_verified = True
        yield
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    except Exception:
        # DB is configured but unreachable — integration tests will be skipped
        _db_verified = False
        yield


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator:
    if not _db_available or not _db_verified:
        pytest.skip("PostgreSQL not available — skipping integration test")
    try:
        async with async_session_test() as session:
            yield session
            await session.rollback()
    except Exception:
        pytest.skip("PostgreSQL not reachable — skipping integration test")


@pytest_asyncio.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """ASGI test client with database session override."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
