## Streak: `GET /habits/{id}/streak` (Task 1)

### Problem
Users want to see their current run of consecutive check-in days.

### Approach
- `GET /habits/{id}/streak` returns `{"habit_id", "streak", "as_of"}`.
- One query: `SELECT DISTINCT day ... WHERE day <= today ORDER BY day DESC`, then walk
  backwards from today until the first missing day.
- "Today" comes from a small `today()` function, so tests can freeze the clock. `as_of`
  in the response says which date the streak was computed for.
- Unknown habit gives **404**, matching the existing check-in endpoint.

### Testing
- 8 parametrized scenarios with a frozen date: none, today only, 3 in a row, inserted out
  of order, a gap, nothing today, a duplicate today, and a future-dated check-in.
- Separate tests for a Feb→Mar month boundary, an unknown habit giving 404, and a
  malformed stored day.
- `sh check.sh` (ruff + black + pytest): 14 passed.

### Manual review (before opening this PR)
The first agent pass (commit 1) passed its single happy-path test but had these problems:
1. **Correctness:** two check-ins on the same day reset the streak to 1. Fixed with `DISTINCT`.
2. **Correctness:** a check-in dated tomorrow sorted first and zeroed the streak. Fixed
   with `day <= today`.
3. **Correctness / API:** an unknown habit returned `200 {"streak": 0}`. It now returns 404.
4. **Robustness:** a malformed stored day (possible until the validation PR lands) caused
   a 500. It's now skipped.
5. **Testability:** `date.today()` inline meant the test was tied to the real clock and
   could fail around midnight. Now it's an injectable `today()`.
6. **Test gap:** one happy-path test only. Now 11 cases.
7. **Lint (caught by ruff):** import order.

### Tradeoffs / not done
- Strict reading of the spec ("up to and including today"): if you haven't checked in
  *yet* today, the streak is 0. Many apps give a grace period until midnight and count
  from yesterday. That's a product decision, so I flagged it rather than guessing.
- Uses server-local time. Users in other timezones would need a `tz` parameter.
- Computed on each request. Fine at this scale. A cached column would only matter at much
  larger volume.
