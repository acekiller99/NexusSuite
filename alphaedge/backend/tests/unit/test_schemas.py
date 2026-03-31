"""Tests for Pydantic schema validation — no database needed."""
import uuid
from datetime import datetime
from decimal import Decimal

import pytest

from app.schemas.response import ApiResponse, PaginatedResponse, PaginationMeta
from app.schemas.user import UserCreate, UserRead, UserUpdate, Token, TokenPayload
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PositionRead
from app.schemas.strategy import StrategyCreate, StrategyRead, StrategyUpdate
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.watchlist import WatchlistCreate, WatchlistRead, WatchlistItemCreate, WatchlistItemRead
from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate


# ── ApiResponse ──────────────────────────────────────────────


class TestApiResponse:
    def test_success_response(self) -> None:
        resp = ApiResponse(success=True, data={"key": "value"}, message="ok")
        assert resp.success is True
        assert resp.data == {"key": "value"}
        assert resp.message == "ok"
        assert resp.errors == []

    def test_error_response(self) -> None:
        resp = ApiResponse(success=False, errors=["not found"], message="fail")
        assert resp.success is False
        assert resp.data is None
        assert resp.errors == ["not found"]

    def test_generic_typed_response(self) -> None:
        resp = ApiResponse[str](success=True, data="hello")
        assert resp.data == "hello"

    def test_paginated_response(self) -> None:
        meta = PaginationMeta(page=2, per_page=10, total=55, total_pages=6)
        resp = PaginatedResponse(success=True, data=[1, 2, 3], meta=meta)
        assert resp.meta.page == 2
        assert resp.meta.total_pages == 6
        assert len(resp.data) == 3


# ── User Schemas ─────────────────────────────────────────────


class TestUserSchemas:
    def test_user_create_valid(self) -> None:
        user = UserCreate(email="test@example.com", password="Secret123!", full_name="Test")
        assert user.email == "test@example.com"
        assert user.full_name == "Test"

    def test_user_create_invalid_email(self) -> None:
        with pytest.raises(Exception):
            UserCreate(email="not-an-email", password="x", full_name="X")

    def test_user_read(self) -> None:
        uid = uuid.uuid4()
        now = datetime.utcnow()
        user = UserRead(id=uid, email="a@b.com", full_name="A B", is_active=True, created_at=now)
        assert user.id == uid
        assert user.is_active is True

    def test_user_update_partial(self) -> None:
        update = UserUpdate(full_name="New Name")
        assert update.full_name == "New Name"
        assert update.email is None

    def test_token(self) -> None:
        token = Token(access_token="abc", refresh_token="def")
        assert token.token_type == "bearer"

    def test_token_payload(self) -> None:
        payload = TokenPayload(sub="user-id-123", exp=9999999999)
        assert payload.sub == "user-id-123"


# ── Portfolio Schemas ────────────────────────────────────────


class TestPortfolioSchemas:
    def test_portfolio_create_defaults(self) -> None:
        p = PortfolioCreate(name="My Portfolio")
        assert p.name == "My Portfolio"
        assert p.initial_capital == Decimal("10000.00")
        assert p.is_paper is True
        assert p.description == ""

    def test_portfolio_create_custom(self) -> None:
        p = PortfolioCreate(name="Live", initial_capital=Decimal("50000"), is_paper=False, description="prod")
        assert p.is_paper is False
        assert p.initial_capital == Decimal("50000")

    def test_portfolio_read(self) -> None:
        uid = uuid.uuid4()
        p = PortfolioRead(
            id=uid, name="P", description="d", initial_capital=Decimal("10000"),
            cash_balance=Decimal("9500"), is_paper=True, created_at=datetime.utcnow(),
        )
        assert p.cash_balance == Decimal("9500")

    def test_position_read(self) -> None:
        pos = PositionRead(
            id=uuid.uuid4(), portfolio_id=uuid.uuid4(), symbol="AAPL",
            quantity=10, avg_entry_price=Decimal("150"), current_price=Decimal("160"),
            created_at=datetime.utcnow(),
        )
        assert pos.symbol == "AAPL"
        assert pos.quantity == 10


# ── Strategy Schemas ─────────────────────────────────────────


class TestStrategySchemas:
    def test_strategy_create(self) -> None:
        s = StrategyCreate(
            name="SMA Cross", strategy_type="sma_crossover",
            symbols=["AAPL", "GOOGL"], parameters={"fast": 10, "slow": 50},
        )
        assert len(s.symbols) == 2
        assert s.parameters["fast"] == 10

    def test_strategy_create_defaults(self) -> None:
        s = StrategyCreate(name="RSI", strategy_type="rsi", symbols=["SPY"])
        assert s.parameters == {}
        assert s.is_paper is True

    def test_strategy_read(self) -> None:
        s = StrategyRead(
            id=uuid.uuid4(), name="Test", description="", strategy_type="macd",
            symbols=["TSLA"], parameters={}, status="draft", is_paper=True,
            created_at=datetime.utcnow(),
        )
        assert s.status.value == "draft"

    def test_strategy_update_partial(self) -> None:
        u = StrategyUpdate(name="Updated Name")
        dumped = u.model_dump(exclude_unset=True)
        assert dumped == {"name": "Updated Name"}
        assert "symbols" not in dumped


# ── Order Schemas ────────────────────────────────────────────


class TestOrderSchemas:
    def test_order_create_market(self) -> None:
        o = OrderCreate(
            portfolio_id=uuid.uuid4(), symbol="AAPL", side="buy",
            order_type="market", quantity=10,
        )
        assert o.side.value == "buy"
        assert o.order_type.value == "market"
        assert o.limit_price is None

    def test_order_create_limit(self) -> None:
        o = OrderCreate(
            portfolio_id=uuid.uuid4(), symbol="MSFT", side="sell",
            order_type="limit", quantity=5, limit_price=Decimal("400.50"),
        )
        assert o.limit_price == Decimal("400.50")

    def test_order_create_invalid_side(self) -> None:
        with pytest.raises(Exception):
            OrderCreate(
                portfolio_id=uuid.uuid4(), symbol="X", side="invalid",
                order_type="market", quantity=1,
            )

    def test_order_read(self) -> None:
        o = OrderRead(
            id=uuid.uuid4(), portfolio_id=uuid.uuid4(), strategy_id=None,
            symbol="AAPL", side="buy", order_type="market", quantity=10,
            limit_price=None, stop_price=None, filled_price=Decimal("150"),
            filled_quantity=10, status="filled", broker_order_id="ABC123",
            created_at=datetime.utcnow(),
        )
        assert o.status.value == "filled"
        assert o.broker_order_id == "ABC123"


# ── Watchlist Schemas ────────────────────────────────────────


class TestWatchlistSchemas:
    def test_watchlist_create(self) -> None:
        w = WatchlistCreate(name="Tech Stocks")
        assert w.name == "Tech Stocks"

    def test_watchlist_item_create(self) -> None:
        item = WatchlistItemCreate(symbol="NVDA", notes="AI leader")
        assert item.symbol == "NVDA"
        assert item.notes == "AI leader"

    def test_watchlist_item_create_default_notes(self) -> None:
        item = WatchlistItemCreate(symbol="AMZN")
        assert item.notes == ""

    def test_watchlist_read_with_items(self) -> None:
        items = [
            WatchlistItemRead(id=uuid.uuid4(), symbol="AAPL", notes="", created_at=datetime.utcnow()),
            WatchlistItemRead(id=uuid.uuid4(), symbol="GOOGL", notes="Search", created_at=datetime.utcnow()),
        ]
        w = WatchlistRead(id=uuid.uuid4(), name="Watch", items=items, created_at=datetime.utcnow())
        assert len(w.items) == 2
        assert w.items[0].symbol == "AAPL"

    def test_watchlist_read_empty(self) -> None:
        w = WatchlistRead(id=uuid.uuid4(), name="Empty", created_at=datetime.utcnow())
        assert w.items == []


# ── Alert Schemas ────────────────────────────────────────────


class TestAlertSchemas:
    def test_alert_create(self) -> None:
        a = AlertCreate(
            symbol="AAPL", condition="price_above",
            threshold=Decimal("200.00"), message="AAPL crossed $200",
        )
        assert a.condition.value == "price_above"
        assert a.threshold == Decimal("200.00")

    def test_alert_create_invalid_condition(self) -> None:
        with pytest.raises(Exception):
            AlertCreate(symbol="X", condition="invalid", threshold=Decimal("1"))

    def test_alert_read(self) -> None:
        a = AlertRead(
            id=uuid.uuid4(), symbol="TSLA", condition="price_below",
            threshold=Decimal("150"), is_triggered=False, is_active=True,
            message="", created_at=datetime.utcnow(),
        )
        assert a.is_active is True
        assert a.is_triggered is False

    def test_alert_update_partial(self) -> None:
        u = AlertUpdate(is_active=False)
        dumped = u.model_dump(exclude_unset=True)
        assert dumped == {"is_active": False}
        assert "condition" not in dumped

    def test_alert_update_threshold(self) -> None:
        u = AlertUpdate(threshold=Decimal("250.00"), message="Updated")
        dumped = u.model_dump(exclude_unset=True)
        assert dumped["threshold"] == Decimal("250.00")
        assert dumped["message"] == "Updated"
