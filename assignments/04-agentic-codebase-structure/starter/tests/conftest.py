from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture(autouse=True)
def fresh_db(tmp_path, monkeypatch):
    """Give every test its own empty database instead of the shared links.db."""
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "links.db")
    main.init_db()


@pytest.fixture
def client():
    return TestClient(main.app)


class FakeClock:
    def __init__(self, now: datetime):
        self.now = now

    def advance(self, **kwargs) -> None:
        self.now += timedelta(**kwargs)


@pytest.fixture
def clock():
    """Freeze "now" for the app; move it with clock.advance(days=..., seconds=...)."""
    fake = FakeClock(datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc))
    main.app.dependency_overrides[main.get_now] = lambda: fake.now
    yield fake
    main.app.dependency_overrides.pop(main.get_now, None)
