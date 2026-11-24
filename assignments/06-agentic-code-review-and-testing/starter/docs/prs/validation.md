## Validation: reject blank habit names and malformed check-in days (Task 2)

### Problem
`POST /habits` accepted `""` and whitespace-only names. `POST /habits/{id}/checkin`
stored any string as `day` (`"yesterday"`, `"2026-02-30"`). Days are stored as text and
sorted as text, so a bad value corrupts ordering and any date math built on top (streaks,
summaries).

### Approach
- Pydantic `field_validator`s on the request models, so FastAPI returns **422** with a
  readable `detail[0].msg` and the bad row never reaches SQLite.
- `name`: trimmed. Rejected if blank or longer than 100 characters.
- `day`: must parse as a real date **and** already be in canonical `YYYY-MM-DD` form.
  `date.fromisoformat` alone also accepts `20260922` and `2026-W39-1`, which would be
  stored unnormalised, so the validator checks `parsed.isoformat() == v`.

### Testing
- 12 new parametrized cases: blank and whitespace names, an overlong name, trimming, and
  7 malformed days (impossible date, missing zero-padding, basic format, ISO week,
  datetime). Each bad day also asserts that nothing was stored.
- `sh check.sh` (ruff + black + pytest): 15 passed.

### Manual review (before opening this PR)
The first agent pass (commit 1) had these problems, fixed in commit 2:
1. **Correctness:** `if v == ""` let `"   "` through.
2. **Correctness:** `date.fromisoformat` accepted the non-canonical `20260922` and
   `2026-W39-1`. The guardrails would never catch this; I found it by trying inputs.
3. **Test gap:** tests checked only the status code, not the message or that nothing was stored.
4. **API shape:** no upper bound on name length.
5. **Lint (caught by ruff, not me):** unsorted imports, and `raise` without `from` inside `except` (B904).

### Tradeoffs / not done
- Future dates are still allowed (you might log ahead). Easy to add if wanted.
- Duplicate check-ins for the same day are still allowed. That's a separate change (a unique index).
- Errors use FastAPI's default 422 shape rather than a custom `{"error": ...}` body.
