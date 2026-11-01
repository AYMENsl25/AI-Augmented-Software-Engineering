"""Link Shortener — starter app for Week 5.

A deliberately tiny FastAPI service you will make *agent-native*. Run it, read it,
then use your coding agent (Antigravity by default) plus the tasks in docs/TASKS.md.

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload
Test:
    pytest
"""
import sqlite3
import string
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

DB_PATH = Path(__file__).parent / "links.db"
ALPHABET = string.ascii_letters + string.digits

app = FastAPI(title="Link Shortener")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(get_db()) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS links (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                url  TEXT NOT NULL,
                expires_at TEXT
            )"""
        )
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(links)")}
        if "expires_at" not in columns:
            conn.execute("ALTER TABLE links ADD COLUMN expires_at TEXT")
        conn.commit()


init_db()


def get_now() -> datetime:
    """Current UTC time. A dependency so tests can override the clock."""
    return datetime.now(timezone.utc)


def encode(n: int) -> str:
    """Base62-encode a row id into a short code."""
    base = len(ALPHABET)
    if n == 0:
        return ALPHABET[0]
    chars = []
    while n > 0:
        n, r = divmod(n, base)
        chars.append(ALPHABET[r])
    return "".join(reversed(chars))


class ShortenRequest(BaseModel):
    url: str
    # Cap keeps now + timedelta from overflowing into a 500.
    expires_in_days: Annotated[int, Field(strict=True, gt=0, le=3650)] | None = None


@app.post("/shorten")
def shorten(req: ShortenRequest, now: datetime = Depends(get_now)):
    if not req.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="url must start with http:// or https://")
    expires_at = None
    if req.expires_in_days is not None:
        expires_at = (now.astimezone(timezone.utc) + timedelta(days=req.expires_in_days)).isoformat()
    with closing(get_db()) as conn:
        cur = conn.execute("INSERT INTO links (url, expires_at) VALUES (?, ?)", (req.url, expires_at))
        row_id = cur.lastrowid
        code = encode(row_id)
        conn.execute("UPDATE links SET code = ? WHERE id = ?", (code, row_id))
        conn.commit()
    return {"code": code, "short_url": f"/{code}", "expires_at": expires_at}


@app.get("/{code}")
def redirect(code: str, now: datetime = Depends(get_now)):
    with closing(get_db()) as conn:
        row = conn.execute("SELECT url, expires_at FROM links WHERE code = ?", (code,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="unknown code")
    if row["expires_at"] and now >= datetime.fromisoformat(row["expires_at"]):
        raise HTTPException(status_code=410, detail="link expired")
    return RedirectResponse(url=row["url"], status_code=307)
