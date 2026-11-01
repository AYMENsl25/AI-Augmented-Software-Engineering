# Starter — Link Shortener

A tiny FastAPI + SQLite service that you will make easier for a coding agent to understand and modify. The application already works; you will add repository guidance, one scoped instruction, one reusable workflow, and complete one feature.

## Setup

```bash
pip install -r requirements.txt
pytest                       # all tests should pass
uvicorn main:app --reload    # http://localhost:8000  (docs at /docs)
```

## Try it

```bash
curl -X POST localhost:8000/shorten -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com"}'
# -> {"code":"b","short_url":"/b","expires_at":null}  then GET localhost:8000/<code> redirects
```

### Expiry

`POST /shorten` accepts an optional `expires_in_days` (integer, 1–3650).
The response's `expires_at` is the UTC expiry time (ISO-8601), or `null` if
the link never expires.

```bash
curl -X POST localhost:8000/shorten -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com","expires_in_days":7}'
# -> {"code":"c","short_url":"/c","expires_at":"<now + 7 days, e.g. 2026-11-08T21:04:13.512345+00:00>"}
```

| Status | When |
|--------|------|
| 307 | `GET /{code}` for a live link |
| 400 | `url` is not http(s) |
| 404 | unknown code |
| 410 | `GET /{code}` at or after `expires_at` (`"link expired"`) |
| 422 | `expires_in_days` is not an integer in 1–3650 |

## Files

- `main.py` — the app (`POST /shorten`, `GET /{code}`)
- `tests/` — the pytest suite (`test_main.py`, `test_expiry.py`) and `conftest.py` (temp DB + fake clock per test)
- `docs/TASKS.md` — the feature backlog
- `AGENTS.md` — guidance for coding agents (`CLAUDE.md` imports it)
- `.claude/rules/tests.md` — test rules, loaded only for files under `tests/`
- `.claude/skills/deliver-task/` — the `/deliver-task <n>` workflow
- `docs/sessions/` — plan, implement and review transcripts for task 3
- `writeup.md` — assignment reflection
