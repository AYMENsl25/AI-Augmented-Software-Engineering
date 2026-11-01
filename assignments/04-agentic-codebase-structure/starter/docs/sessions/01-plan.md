# Stage 1 — Plan (claude -p --permission-mode plan)

**Prompt:** Stage 1 of 3: PLAN. Do not edit any files. Inspect task 3 (Expiry) in docs/TASKS.md, plus AGENTS.md, main.py, and the tests. Propose an implementation plan: the request/response contract, status codes and exactly when each is returned, how invalid expires_in_days values are rejected, the schema change and how an existing links.db is upgraded, how time is handled, which tests to add (success and failure), and risks or open questions. Be concise.

---

Here's the plan for task 3 (Expiry). I haven't edited any files; the plan is saved at `C:\Users\msi\.claude\plans\stage-1-of-3-jolly-parrot.md`.

**Contract**
- `POST /shorten` takes `{"url", "expires_in_days"?}`. If `expires_in_days` is missing or null, the link never expires. The response stays `{"code", "short_url"}`.
- `GET /{code}` checks in this order:
  1. **404** `"unknown code"` if the code doesn't exist.
  2. **410** `"link expired"` if `expires_at` is set and `now >= expires_at`.
  3. Otherwise **307** to the stored URL.
- A bad URL still gets **400**.

**Rejecting invalid `expires_in_days`**
- The field is `Annotated[int, Field(strict=True, gt=0, le=3650)] | None`, which returns **422**.
- `strict=True` rejects `"5"`, `1.5` and `true`. Without it, these would be converted to integers.
- `gt=0` rejects 0 and negative numbers.
- The `le=3650` cap stops a huge value from crashing the request with a 500 when the expiry date is calculated.

**Schema and upgrading an existing `links.db`**
- New nullable `expires_at TEXT` column holding a UTC ISO-8601 string.
- `init_db()` reads the table's current columns and runs `ALTER TABLE links ADD COLUMN expires_at TEXT` if the column is missing.
- Old rows get NULL, so they never expire and nobody has to delete their DB.

**Time**
- Both `shorten` and `redirect` get the time from `get_now` via `Depends`.
- `shorten` stores `now + timedelta(days=n)`; `redirect` parses it back and compares it with `now`.
- Neither calls `datetime.now()` directly, and both times are timezone-aware UTC.

**Tests** (through the HTTP API, using the `clock` fixture)
- **Success:**
  - A link with no expiry still redirects after 10,000 days.
  - With `expires_in_days=1`, it returns 307 and the right `location` one second before expiry.
  - 3650 is accepted.
- **Boundary:**
  - Exactly at expiry it returns 410 with `detail == "link expired"`.
  - One day later it still returns 410.
- **Invalid values:** `0`, `-1`, `3651`, `"5"`, `1.5` and `true` each return 422.
- **Upgrade:** build an old-schema table in the test's temporary DB, then call `init_db()`. Through the API, check that the old row still redirects and a new expiring link works. Raw SQLite is used only to set up that old table, never to check results.

**Verify:** `python -m pytest -q` passes, then add the new field and the 410 response to `README.md`.

**Open questions**
1. **422 or 400 for a bad expiry?** I'd use 422 because FastAPI does it with no extra code. If you'd rather match the 400 used for a bad URL, I'll check the value by hand and return 400 with a short `detail`.
2. **Return `expires_at` in the POST response?** I've left it out because the task doesn't ask for it; adding it is one extra key.
3. **The 3650-day cap is an arbitrary number.** Some cap is needed to avoid the 500.
