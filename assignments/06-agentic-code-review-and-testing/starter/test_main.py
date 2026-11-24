from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

import main
from main import app

client = TestClient(app)


def test_create_and_list_habit():
    r = client.post("/habits", json={"name": "Read 20 minutes"})
    assert r.status_code == 200
    hid = r.json()["id"]
    r2 = client.get("/habits")
    assert r2.status_code == 200
    assert any(h["id"] == hid for h in r2.json())


def test_checkin_flow():
    hid = client.post("/habits", json={"name": "Stretch"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 200
    r2 = client.get(f"/habits/{hid}/checkins")
    assert r2.json() == ["2026-09-22"]


def test_checkin_unknown_habit_404():
    r = client.post("/habits/99999/checkin", json={"day": "2026-09-22"})
    assert r.status_code == 404


TODAY = date(2026, 9, 22)


@pytest.fixture
def frozen_today(monkeypatch):
    monkeypatch.setattr(main, "today", lambda: TODAY)


def _habit_with_checkins(*offsets):
    """Create a habit with check-ins at TODAY minus each offset (negative = future)."""
    hid = client.post("/habits", json={"name": "Walk"}).json()["id"]
    for off in offsets:
        day = (TODAY - timedelta(days=off)).isoformat()
        assert client.post(f"/habits/{hid}/checkin", json={"day": day}).status_code == 200
    return hid


@pytest.mark.parametrize(
    "offsets, expected",
    [
        ((), 0),  # no check-ins
        ((0,), 1),  # today only
        ((0, 1, 2), 3),  # three in a row
        ((2, 0, 1), 3),  # inserted out of order
        ((0, 1, 3, 4), 2),  # gap breaks the run
        ((1, 2, 3), 0),  # nothing today yet
        ((0, 0, 1), 2),  # duplicate check-in today counts once
        ((-1, 0, 1), 2),  # future-dated check-in is ignored
    ],
)
def test_streak(frozen_today, offsets, expected):
    hid = _habit_with_checkins(*offsets)
    r = client.get(f"/habits/{hid}/streak")
    assert r.status_code == 200
    assert r.json() == {"habit_id": hid, "streak": expected, "as_of": "2026-09-22"}


def test_streak_across_month_boundary(monkeypatch):
    monkeypatch.setattr(main, "today", lambda: date(2026, 3, 1))
    hid = client.post("/habits", json={"name": "Read"}).json()["id"]
    for day in ["2026-02-27", "2026-02-28", "2026-03-01"]:
        client.post(f"/habits/{hid}/checkin", json={"day": day})
    assert client.get(f"/habits/{hid}/streak").json()["streak"] == 3


def test_streak_unknown_habit_404():
    assert client.get("/habits/99999/streak").status_code == 404


def test_streak_ignores_malformed_stored_day(frozen_today):
    hid = _habit_with_checkins(0)
    client.post(f"/habits/{hid}/checkin", json={"day": "oops"})  # no validation on this branch
    assert client.get(f"/habits/{hid}/streak").json()["streak"] == 1
