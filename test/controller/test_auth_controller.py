import pytest
from fastapi.testclient import TestClient
import jwt
from src.helper.settings_helper import load_settings
from src.main import app
from sqlalchemy import text
from src.config.db_dev import SessionLocal, Base, engine

client = TestClient(app)


def reset_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM users"))
        db.commit()
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_each_test():
    reset_db()
    yield
    reset_db()


def test_register_success():
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret12",
        "full_name": "Alice"
    }
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["isSuccess"] is True
    assert body["errorCode"] == "success"
    assert "access_token" in body["result"] and body["result"]["access_token"]
    assert body["result"]["token_type"] == "bearer"
    settings = load_settings()
    jwt_cfg = settings.get("jwt", {})
    payload = jwt.decode(body["result"]["access_token"], jwt_cfg.get("secret"), algorithms=[jwt_cfg.get("algorithm")])
    assert payload.get("sub") == "alice"


def test_register_duplicate():
    payload = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "secret12"
    }
    res1 = client.post("/auth/register", json=payload)
    assert res1.status_code == 201
    res2 = client.post("/auth/register", json=payload)
    assert res2.status_code in (400, 409)
    body = res2.json()
    assert body["isSuccess"] is False
    assert body["errorCode"] == "user_exists"


def test_register_password_too_long_bytes():
    long_pw = "á" * 73
    payload = {
        "username": "charlie",
        "email": "charlie@example.com",
        "password": long_pw
    }
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 422
    body = res.json()
    assert body["isSuccess"] is False
    assert body["errorCode"] == "validation_error"


def test_login_success_and_me():
    reg = {
        "username": "dana",
        "email": "dana@example.com",
        "password": "secret12"
    }
    res_reg = client.post("/auth/register", json=reg)
    assert res_reg.status_code == 201

    login = {
        "username": "dana",
        "password": "secret12"
    }
    res_login = client.post("/auth/login", json=login)
    assert res_login.status_code == 200
    body_login = res_login.json()
    settings = load_settings()
    jwt_cfg = settings.get("jwt", {})
    token = body_login["result"]["access_token"]
    payload = jwt.decode(token, jwt_cfg.get("secret"), algorithms=[jwt_cfg.get("algorithm")])
    assert payload.get("sub") == "dana"

    res_me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    body = res_me.json()
    assert body["isSuccess"] is True
    assert body["result"]["username"] == "dana"


def test_login_invalid_password():
    reg = {
        "username": "erin",
        "email": "erin@example.com",
        "password": "secret12"
    }
    client.post("/auth/register", json=reg)

    bad_login = {
        "username": "erin",
        "password": "wrongpass"
    }
    res = client.post("/auth/login", json=bad_login)
    assert res.status_code == 401
    body = res.json()
    assert body["isSuccess"] is False
    assert body["errorCode"] == "invalid_credentials"


def test_me_invalid_token():
    res = client.get("/auth/me", headers={"Authorization": "Bearer invalid"})
    assert res.status_code == 401
    body = res.json()
    assert body["isSuccess"] is False
    assert body["errorCode"] in ("invalid_token", "inactive_or_not_found")
