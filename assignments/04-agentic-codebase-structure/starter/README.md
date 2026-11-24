# Starter — Link Shortener

A tiny FastAPI + SQLite service that you will make easier for a coding agent to understand and modify. The application already works; you will add repository guidance, one scoped instruction, one reusable workflow, and complete one feature.

## Setup

```bash
pip install -r requirements.txt
pytest                       # 3 tests should pass
uvicorn main:app --reload    # http://localhost:8000  (docs at /docs)
```

## Try it

```bash
curl -X POST localhost:8000/shorten -H 'Content-Type: application/json' \
  -d '{"url":"https://example.com"}'
# -> {"code":"b","short_url":"/b"}  then GET localhost:8000/<code> redirects
```

## Files

- `main.py` — the app (`POST /shorten`, `GET /{code}`)
- `test_main.py` — the existing pytest suite
- `docs/TASKS.md` — choose one feature to implement

Start by running the existing tests, then read all three files before adding agent guidance.
