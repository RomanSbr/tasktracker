import pytest
from fastapi import HTTPException

from app.core import security


def test_password_hash_roundtrip():
    plain = "SecurePass123!"

    hashed = security.get_password_hash(plain)

    assert hashed != plain
    assert security.verify_password(plain, hashed)
    assert not security.verify_password("WrongPass123!", hashed)


def test_access_and_refresh_tokens_are_distinct():
    user_id = "00000000-0000-0000-0000-000000000001"

    access = security.create_access_token(user_id)
    refresh = security.create_refresh_token(user_id)

    assert access != refresh
    assert security.decode_token(access)["type"] == "access"
    assert security.decode_token(refresh)["type"] == "refresh"


def test_decode_token_rejects_wrong_type():
    refresh = security.create_refresh_token("00000000-0000-0000-0000-000000000001")

    with pytest.raises(HTTPException):
        security.decode_token(refresh, expected_type="access")
