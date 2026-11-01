---
paths:
  - "tests/**/*.py"
---

# Rules for writing tests

These apply when you read or edit files under `tests/`.

## Go through the public API
- Use the `client` fixture (`TestClient`) and call real routes.
- Do not import private helpers or query `links.db` to check results.
  If a behavior can't be seen over HTTP, it doesn't need a test.

## Isolation
- Every test gets its own temporary database from `conftest.py`. Never point
  a test at the real `links.db` and never depend on another test's rows.
- Do not assert on a specific generated code (`"b"`, `"c"`): codes depend
  on row ids. Read the code from the `POST /shorten` response.
- Tests must pass alone and in any order (`pytest tests/test_x.py::test_y`).

## Time
- Never call `time.sleep` and never compare against the real current time.
- Use the `clock` fixture: it fixes "now", and `clock.advance(days=...)`
  moves it. Behavior on both sides of a time boundary needs a test
  (just before and exactly at/after the boundary).

## Coverage for each feature
- At least one success case and one failure case per new behavior.
- For validated input, test a valid value, the boundary values, and each
  kind of invalid value (wrong type, zero/negative, too large, missing).
- Check status code **and** the relevant body field or header
  (e.g. `location`, `detail`), not just the status code.
- Keep the 3 original tests passing unchanged in meaning.
