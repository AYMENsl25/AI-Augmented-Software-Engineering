import pytest
from fastapi.testclient import TestClient

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


def _error_msg(r):
    return r.json()["detail"][0]["msg"]


@pytest.mark.parametrize("name", ["", "   ", "\t\n"])
def test_blank_name_rejected(name):
    r = client.post("/habits", json={"name": name})
    assert r.status_code == 422
    assert "must not be empty" in _error_msg(r)


def test_overlong_name_rejected():
    r = client.post("/habits", json={"name": "x" * 101})
    assert r.status_code == 422
    assert "at most 100" in _error_msg(r)


def test_name_is_trimmed():
    r = client.post("/habits", json={"name": "  Run  "})
    assert r.status_code == 200
    assert r.json()["name"] == "Run"


@pytest.mark.parametrize(
    "day",
    ["yesterday", "", "2026-02-30", "2026-9-22", "20260922", "2026-W39-1", "2026-09-22T10:00"],
)
def test_malformed_day_rejected(day):
    hid = client.post("/habits", json={"name": "Run"}).json()["id"]
    r = client.post(f"/habits/{hid}/checkin", json={"day": day})
    assert r.status_code == 422
    assert "YYYY-MM-DD" in _error_msg(r)
    assert client.get(f"/habits/{hid}/checkins").json() == []
