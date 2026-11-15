import pytest
import db_handler

@pytest.fixture
def db(tmp_path, monkeypatch):
    monkeypatch.setattr(db_handler, "DB_PATH", tmp_path / "test.db")
    db_handler.initDB()

@pytest.fixture
def clock(monkeypatch):
    now = [1000.0]
    monkeypatch.setattr("auth.user_lockout.time.time", lambda: now[0])
    return now