"""Habit Tracker — starter app for Week 6.

A tiny FastAPI service for habits and daily check-ins. You'll add features on
branches, open PRs, and compare your manual review with an AI reviewer.

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload
Test:
    pytest
"""

import sqlite3
from contextlib import closing
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = Path(__file__).parent / "habits.db"

app = FastAPI(title="Habit Tracker")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(get_db()) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS habits (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS checkins (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                day      TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )""")
        conn.commit()


init_db()


class HabitIn(BaseModel):
    name: str


class CheckinIn(BaseModel):
    day: str  # ISO date, e.g. "2026-09-22"


@app.post("/habits")
def create_habit(habit: HabitIn):
    with closing(get_db()) as conn:
        cur = conn.execute("INSERT INTO habits (name) VALUES (?)", (habit.name,))
        conn.commit()
        return {"id": cur.lastrowid, "name": habit.name}


@app.get("/habits")
def list_habits():
    with closing(get_db()) as conn:
        rows = conn.execute("SELECT id, name FROM habits ORDER BY id").fetchall()
    return [dict(r) for r in rows]


@app.post("/habits/{habit_id}/checkin")
def add_checkin(habit_id: int, checkin: CheckinIn):
    with closing(get_db()) as conn:
        habit = conn.execute("SELECT id FROM habits WHERE id = ?", (habit_id,)).fetchone()
        if habit is None:
            raise HTTPException(status_code=404, detail="unknown habit")
        conn.execute("INSERT INTO checkins (habit_id, day) VALUES (?, ?)", (habit_id, checkin.day))
        conn.commit()
    return {"habit_id": habit_id, "day": checkin.day}


@app.get("/habits/{habit_id}/checkins")
def list_checkins(habit_id: int):
    with closing(get_db()) as conn:
        rows = conn.execute(
            "SELECT day FROM checkins WHERE habit_id = ? ORDER BY day", (habit_id,)
        ).fetchall()
    return [r["day"] for r in rows]


def today() -> date:
    """Current date. A function so tests can freeze it."""
    return date.today()


@app.get("/habits/{habit_id}/streak")
def get_streak(habit_id: int):
    """Consecutive days with a check-in, ending today. 0 if there is no check-in today."""
    current = today()
    with closing(get_db()) as conn:
        if conn.execute("SELECT 1 FROM habits WHERE id = ?", (habit_id,)).fetchone() is None:
            raise HTTPException(status_code=404, detail="unknown habit")
        # DISTINCT: several check-ins on one day count once.
        # day <= today: future-dated check-ins must not break the run.
        rows = conn.execute(
            "SELECT DISTINCT day FROM checkins WHERE habit_id = ? AND day <= ? ORDER BY day DESC",
            (habit_id, current.isoformat()),
        ).fetchall()
    streak = 0
    expected = current
    for r in rows:
        try:
            day = date.fromisoformat(r["day"])
        except ValueError:
            continue  # legacy malformed row: ignore rather than 500
        if day != expected:
            break
        streak += 1
        expected -= timedelta(days=1)
    return {"habit_id": habit_id, "streak": streak, "as_of": current.isoformat()}
