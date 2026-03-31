"""Tests for app configuration — no database needed."""
import os

import pytest

from app.config import Settings


class TestSettings:
    def test_default_values(self) -> None:
        s = Settings()
        assert s.app_name == "AlphaEdge"
        assert s.app_env == "development"
        assert s.debug is True
        assert s.postgres_port == 5432
        assert s.redis_port == 6379

    def test_database_url_construction(self) -> None:
        s = Settings(
            postgres_user="user", postgres_password="pass",
            postgres_host="dbhost", postgres_port=5433, postgres_db="mydb",
        )
        assert s.database_url == "postgresql+asyncpg://user:pass@dbhost:5433/mydb"

    def test_redis_url_without_password(self) -> None:
        s = Settings(redis_host="redis-host", redis_port=6380, redis_password="")
        assert s.redis_url == "redis://redis-host:6380/0"

    def test_redis_url_with_password(self) -> None:
        s = Settings(redis_host="redis-host", redis_port=6379, redis_password="secret")
        assert s.redis_url == "redis://:secret@redis-host:6379/0"

    def test_cors_origin_list_single(self) -> None:
        s = Settings(cors_origins="http://localhost:3000")
        assert s.cors_origin_list == ["http://localhost:3000"]

    def test_cors_origin_list_multiple(self) -> None:
        s = Settings(cors_origins="http://localhost:3000, http://localhost:8000, https://app.example.com")
        assert s.cors_origin_list == [
            "http://localhost:3000",
            "http://localhost:8000",
            "https://app.example.com",
        ]

    def test_jwt_defaults(self) -> None:
        s = Settings()
        assert s.jwt_algorithm == "HS256"
        assert s.jwt_access_token_expire_minutes == 30
        assert s.jwt_refresh_token_expire_days == 7

    def test_trading_defaults(self) -> None:
        s = Settings()
        assert s.trading_mode == "paper"
        assert s.alpaca_base_url == "https://paper-api.alpaca.markets"

    def test_custom_jwt_settings(self) -> None:
        s = Settings(jwt_secret_key="my-key", jwt_access_token_expire_minutes=60)
        assert s.jwt_secret_key == "my-key"
        assert s.jwt_access_token_expire_minutes == 60

    def test_log_level_default(self) -> None:
        s = Settings()
        assert s.log_level == "INFO"
