# AGENTS.md — Link Shortener

A tiny FastAPI + SQLite service: `POST /shorten` stores a URL and returns a
base62 code; `GET /{code}` redirects (307) to the stored URL.

## Map

| Path | What it is |
|------|------------|
| `main.py` | The whole app: DB helpers, base62 `encode`, routes |
| `tests/` | pytest suite; `tests/conftest.py` gives each test a fresh DB and a fixed clock |
| `docs/TASKS.md` | The feature backlog (pick by number) |
| `docs/sessions/` | Plan / implement / review transcripts of past changes |
| `links.db` | Local SQLite file, created on import. Never commit it |

## Commands (run from this directory)

```bash
pip install -r requirements.txt
python -m pytest -q              # must stay green
uvicorn main:app --reload        # http://localhost:8000/docs
```

## Product boundaries

In scope: shortening, redirecting, and small per-link properties (alias,
click count, expiry). Out of scope: users/auth, analytics dashboards, HTML
pages, background jobs, extra services or ORMs. Keep it one file and SQLite.

## Conventions

- Errors are `HTTPException` with a short lowercase `detail`.
- Existing status codes are a contract: 400 bad URL, 404 unknown code,
  307 redirect. Do not change them.
- Time comes from the `get_now` dependency, never `datetime.now()` inline,
  so tests can control it.
- A schema change must also upgrade an existing `links.db` in `init_db()`
  (add the column if it is missing); do not ask users to delete their DB.
- New dependencies need a reason; the stdlib usually suffices.

## Change workflow

1. **Understand** — read the task, `main.py`, and the related tests.
2. **Test** — write a failing behavioral test through the HTTP API.
3. **Implement** — the smallest change in `main.py` that makes it pass.
4. **Verify** — `python -m pytest -q`, then update `README.md` if the API changed.

For a backlog task, use the `deliver-task` skill (`/deliver-task <number>`).
