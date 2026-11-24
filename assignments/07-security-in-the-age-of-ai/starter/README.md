# Starter — Vulnerable Bookstore

⚠️ **This app contains INTENTIONAL vulnerabilities** for the scan-and-fix exercise.
Do **not** deploy it or reuse this code in real projects. The planted issues are listed
in the header of `main.py` — that's your answer key.

## Setup
```bash
pip install -r requirements.txt
pytest                      # 3 tests should pass
uvicorn main:app --reload   # http://localhost:8000  (docs at /docs)
```

## Scan
```bash
semgrep scan --config auto
```
Scan the backend code, `static/index.html`, `requirements.txt`, and config for secrets.

## Endpoints
- `GET /books?q=...`, `GET /books/{id}`
- `POST /reviews` `{ "book_id": 1, "text": ... }`, `GET /reviews/{id}`
- `POST /summarize-review` `{ "text": ... }` — needs Ollama running (`llama3.1:8b`) for
  the prompt-injection exercise

## Files
- `main.py` — the vulnerable app (planted-issue list in the header)
- `static/index.html` — frontend with an XSS sink
- `test_main.py` — pytest suite (non-LLM paths)
