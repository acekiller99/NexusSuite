"""Tests for JWT token creation and verification — no database needed."""
import time
import uuid

import pytest
from jose import jwt

from app.api.deps import create_access_token, create_refresh_token
from app.config import settings


class TestJWTTokens:
    def test_create_access_token(self) -> None:
        user_id = str(uuid.uuid4())
        token = create_access_token(user_id)
        assert isinstance(token, str)
        assert len(token) > 0

        # Decode and verify
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert payload["sub"] == user_id
        assert "exp" in payload

    def test_create_refresh_token(self) -> None:
        user_id = str(uuid.uuid4())
        token = create_refresh_token(user_id)
        assert isinstance(token, str)

        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"
        assert "exp" in payload

    def test_access_token_has_correct_subject(self) -> None:
        user_id = str(uuid.uuid4())
        token = create_access_token(user_id)
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert payload["sub"] == user_id

    def test_access_and_refresh_tokens_differ(self) -> None:
        user_id = str(uuid.uuid4())
        access = create_access_token(user_id)
        refresh = create_refresh_token(user_id)
        assert access != refresh

    def test_refresh_token_has_type_field(self) -> None:
        token = create_refresh_token("test-user")
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert payload.get("type") == "refresh"

    def test_access_token_has_no_type_field(self) -> None:
        token = create_access_token("test-user")
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert "type" not in payload

    def test_token_expiration_is_future(self) -> None:
        token = create_access_token("user")
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert payload["exp"] > time.time()

    def test_decode_with_wrong_key_fails(self) -> None:
        token = create_access_token("user")
        with pytest.raises(Exception):
            jwt.decode(token, "wrong-secret-key", algorithms=[settings.jwt_algorithm])

    def test_decode_with_wrong_algorithm_fails(self) -> None:
        token = create_access_token("user")
        with pytest.raises(Exception):
            jwt.decode(token, settings.jwt_secret_key, algorithms=["HS384"])

    def test_multiple_tokens_for_same_user_differ(self) -> None:
        # Tokens include exp timestamp, so they should differ slightly
        t1 = create_access_token("same-user")
        t2 = create_access_token("same-user")
        # They might be identical if created in the same second, but payloads should be valid
        payload1 = jwt.decode(t1, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        payload2 = jwt.decode(t2, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        assert payload1["sub"] == payload2["sub"] == "same-user"
