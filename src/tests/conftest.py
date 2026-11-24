import pytest
import db_handler
from auth.auth import register

@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setattr(db_handler, "DB_PATH", tmp_path / "test.db")
    db_handler.initDB()

@pytest.fixture
def clock(monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("auth.user_lockout.time.time", lambda: now[0])
    return now

@pytest.fixture(autouse=True)
def forceDevModeOff(monkeypatch):
    monkeypatch.setattr("auth.auth.TEST_MODE", False)

@pytest.fixture
def client(db, monkeypatch):
    import app as app_module
    app_module.app.config["SECRET_KEY"] = "test-key"
    monkeypatch.setattr(app_module.limiter, "enabled", False)
    return app_module.app.test_client()

@pytest.fixture
def user(db):
    register("user@example.com", "password123!", "password123!")