"""Recipe Box — starter app for Week 8.

A tiny FastAPI service for recipes and tags, with a static frontend. Use it as the
playground for concurrent multi-agent work and a generator-critic loop.

Run:
    pip install -r requirements.txt
    uvicorn main:app --reload
    # open http://localhost:8000/
Test:
    pytest
"""
import json
import re
import sqlite3
from contextlib import closing
from fractions import Fraction
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE = Path(__file__).parent
DB_PATH = BASE / "recipes.db"

app = FastAPI(title="Recipe Box")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(get_db()) as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS recipes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                ingredients TEXT NOT NULL,  -- JSON list of strings
                tags        TEXT NOT NULL   -- JSON list of strings
            )"""
        )
        conn.commit()


init_db()


class RecipeIn(BaseModel):
    title: str
    ingredients: list[str] = []
    tags: list[str] = []


def _row_to_recipe(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "ingredients": json.loads(row["ingredients"]),
        "tags": json.loads(row["tags"]),
    }


@app.get("/")
def index():
    return FileResponse(BASE / "static" / "index.html")


@app.post("/recipes")
def create_recipe(recipe: RecipeIn):
    with closing(get_db()) as conn:
        cur = conn.execute(
            "INSERT INTO recipes (title, ingredients, tags) VALUES (?, ?, ?)",
            (recipe.title, json.dumps(recipe.ingredients), json.dumps(recipe.tags)),
        )
        conn.commit()
        rid = cur.lastrowid
    return {"id": rid, **recipe.model_dump()}


@app.get("/recipes")
def list_recipes(tag: str | None = None):
    with closing(get_db()) as conn:
        rows = conn.execute("SELECT * FROM recipes ORDER BY id").fetchall()
    recipes = [_row_to_recipe(r) for r in rows]
    # Blank/whitespace-only tag is treated as "no filter" (lenient, matches an empty search box).
    needle = (tag or "").strip().casefold()
    if not needle:
        return recipes
    # ponytail: filters in Python (tags are a JSON column); move to SQL/json_each if the table grows large
    return [r for r in recipes if any(t.strip().casefold() == needle for t in r["tags"])]


@app.get("/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    with closing(get_db()) as conn:
        row = conn.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="unknown recipe")
    return _row_to_recipe(row)


# --- Task 1: shopping list ---
@app.get("/shopping-list")
def shopping_list(ids: str = ""):
    parts = [p.strip() for p in ids.split(",") if p.strip()]
    if not parts:
        raise HTTPException(status_code=422, detail="ids is required, e.g. ?ids=1,2")
    bad = [p for p in parts if not (p.isascii() and p.isdigit())]
    if bad:
        raise HTTPException(status_code=422, detail=f"ids must be positive integers, got: {', '.join(bad)}")
    recipe_ids = list(dict.fromkeys(int(p) for p in parts))  # dedupe, keep order
    with closing(get_db()) as conn:
        rows = conn.execute(
            f"SELECT * FROM recipes WHERE id IN ({','.join('?' * len(recipe_ids))})", recipe_ids
        ).fetchall()
    found = {r["id"]: r for r in rows}
    missing = [i for i in recipe_ids if i not in found]
    if missing:
        raise HTTPException(status_code=404, detail=f"unknown recipe ids: {missing}")
    items = {}
    for i in recipe_ids:
        for ing in json.loads(found[i]["ingredients"]):
            items.setdefault(ing.strip().casefold(), ing.strip())
    return {"recipe_ids": recipe_ids, "items": [v for v in items.values() if v]}

# --- Task 3: ingredient scaling ---

# Leading quantity: "200", "1.5", "1,5", "1/2", "1 1/2", optionally a range "2-3" / "2–3".
_NUM = r"\d+\s+\d+/\d+|\d+/\d+|\d[\d.,]*\d|\d"
_QTY = re.compile(rf"^\s*({_NUM})(?:\s*([-–])\s*({_NUM}))?(.*)$", re.S)


def _fmt(qty: Fraction) -> str:
    x = float(qty)
    r = round(x, 2)
    # ponytail: decimal output (0.5, not 1/2); add fraction formatting if users want it
    return f"{r:g}" if r or not x else f"{x:.2g}"  # never show a nonzero amount as "0"


def _parse(num: str) -> Fraction:
    """"1,500" -> 1500 (thousands), "1,5" -> 1.5 (decimal comma); "1.000,5" raises ValueError."""
    if "," in num and "." in num:
        raise ValueError("ambiguous separators")  # never guess a quantity
    if re.fullmatch(r"\d{1,3}(,\d{3})+", num):
        return Fraction(num.replace(",", ""))
    return Fraction(num.replace(",", "."))


def _scale(num: str, factor: float) -> str:
    qty = sum(_parse(p) for p in num.split()) * Fraction(str(factor))
    return _fmt(qty)


def scale_ingredient(line: str, factor: float) -> str:
    """Scale the leading quantity (or range) of an ingredient line; others are unchanged."""
    m = _QTY.match(line)
    if not m:
        return line
    low, dash, high, rest = m.groups()
    try:
        out = _scale(low, factor)
        if high:
            out += dash + _scale(high, factor)
    except (ZeroDivisionError, ValueError):  # "1/0 cup", "1.000,5 g": leave user input alone
        return line
    return out + rest


@app.get("/recipes/{recipe_id}/scaled")
def get_scaled_recipe(recipe_id: int, factor: float = Query(..., ge=0.01, le=1000)):
    recipe = get_recipe(recipe_id)
    recipe["ingredients"] = [scale_ingredient(i, factor) for i in recipe["ingredients"]]
    recipe["factor"] = factor
    return recipe
