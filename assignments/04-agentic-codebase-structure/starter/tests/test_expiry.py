import sqlite3

import pytest

import main


def shorten(client, **extra):
    r = client.post("/shorten", json={"url": "https://example.com", **extra})
    assert r.status_code == 200
    return r.json()


def test_no_expiry_never_expires(client, clock):
    body = shorten(client)
    assert body["expires_at"] is None
    clock.advance(days=10_000)
    r = client.get(f"/{body['code']}", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com"


def test_null_expiry_never_expires(client, clock):
    body = shorten(client, expires_in_days=None)
    assert body["expires_at"] is None
    clock.advance(days=10_000)
    assert client.get(f"/{body['code']}", follow_redirects=False).status_code == 307


def test_response_includes_expires_at(client, clock):
    body = shorten(client, expires_in_days=1)
    assert body["expires_at"] == "2026-01-02T12:00:00+00:00"


def test_redirects_just_before_expiry(client, clock):
    code = shorten(client, expires_in_days=1)["code"]
    clock.advance(days=1, seconds=-1)
    r = client.get(f"/{code}", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com"


def test_410_exactly_at_expiry(client, clock):
    code = shorten(client, expires_in_days=1)["code"]
    clock.advance(days=1)
    r = client.get(f"/{code}", follow_redirects=False)
    assert r.status_code == 410
    assert r.json()["detail"] == "link expired"


def test_410_after_expiry(client, clock):
    code = shorten(client, expires_in_days=1)["code"]
    clock.advance(days=2)
    r = client.get(f"/{code}", follow_redirects=False)
    assert r.status_code == 410
    assert r.json()["detail"] == "link expired"


def test_max_expiry_accepted(client, clock):
    body = shorten(client, expires_in_days=3650)
    assert body["expires_at"] == "2035-12-30T12:00:00+00:00"
    clock.advance(days=3649)
    r = client.get(f"/{body['code']}", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com"


@pytest.mark.parametrize("bad", [0, -1, 3651, "5", 1.5, True])
def test_rejects_invalid_expiry(client, bad):
    r = client.post("/shorten", json={"url": "https://example.com", "expires_in_days": bad})
    assert r.status_code == 422
    assert r.json()["detail"][0]["loc"] == ["body", "expires_in_days"]


def test_bad_url_still_400_with_expiry(client):
    r = client.post("/shorten", json={"url": "ftp://nope", "expires_in_days": 1})
    assert r.status_code == 400
    assert r.json()["detail"] == "url must start with http:// or https://"


def test_upgrades_old_schema_db(tmp_path, monkeypatch, client, clock):
    # Setup only: build a pre-expiry links table with one row.
    db = tmp_path / "old.db"
    with sqlite3.connect(db) as conn:
        conn.execute(
            "CREATE TABLE links (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, url TEXT NOT NULL)"
        )
        conn.execute("INSERT INTO links (code, url) VALUES ('old', 'https://old.example')")
    conn.close()
    monkeypatch.setattr(main, "DB_PATH", db)
    main.init_db()

    clock.advance(days=10_000)
    r = client.get("/old", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://old.example"

    code = shorten(client, expires_in_days=1)["code"]
    clock.advance(days=1)
    assert client.get(f"/{code}", follow_redirects=False).status_code == 410
