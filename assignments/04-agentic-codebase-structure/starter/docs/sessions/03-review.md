# Stage 3 — Review (claude -p --permission-mode plan, read-only)

**Prompt:** Stage 3 of 3: REVIEW. Do not edit any files. Review the uncommitted change for task 3 (Expiry): run `git diff -- .` and `git status`, read tests/test_expiry.py, and run `python -m pytest -q`. Check it against docs/TASKS.md, AGENTS.md, the test rules in .claude/rules/tests.md, and the plan in docs/sessions/01-plan.md. Also check the implementer summary in docs/sessions/02-implement.md for accuracy, and whether README.md is consistent with the repo layout. Look for correctness bugs, missing failure cases, and stale docs. End with exactly one verdict line: ACCEPT or REVISE, followed by a short numbered list of findings.

---

I reviewed the change without editing anything. The code is correct and the 18 tests pass, but my verdict is REVISE because of two documentation problems: the implementer summary gets its test counts wrong, and README.md lists files that are in the wrong place or missing.

**What I checked**
- **`git status`:** only `README.md` and `main.py` are modified. `tests/test_expiry.py` and `docs/sessions/` are new. `links.db` is gitignored, so it won't be committed by accident.
- **Tests:** `python -m pytest -q` gives `18 passed in 0.23s`. The upgrade test and the "exactly at expiry" test also pass when run on their own.
- **Against `docs/TASKS.md`:** `expires_in_days` is optional and must be positive. Expired links get 410 and invalid values get 422. Both are tested.
- **Against `AGENTS.md`:**
  - Status codes 400, 404 and 307 are unchanged.
  - Time comes from `get_now` in both routes.
  - `init_db()` adds `expires_at` to an older `links.db`.
  - No new dependencies.
- **Against the plan:** it matches `01-plan.md`. The 3650-day cap and returning 422 are as approved. Returning `expires_at` in the POST response was approved later, in the stage 2 prompt.
- **Correctness:**
  - The `>=` comparison makes a link expire exactly at `expires_at`.
  - Stored times always carry a UTC offset, so the comparison can't mix timezone-aware and naive datetimes.
  - Older rows have `NULL` and never expire.
  - The 3650-day cap prevents a 500 when a huge value would overflow the date calculation.
- **Against `.claude/rules/tests.md`:**
  - Both sides of the expiry time are tested (one second before, exactly at, and after).
  - Both limits (1 and 3650) and every kind of invalid value are tested: zero, negative, too large, wrong type, and missing/null.
  - Codes are read from the response, not hard-coded.
  - Raw SQLite is used only to set up the old-schema table, as the plan allowed.

REVISE
1. **The implementer summary has the wrong numbers.** `docs/sessions/02-implement.md:20` says 13 new tests and `:32` says "5 before → 18 after". It is 15 new tests (`tests/test_expiry.py` collects 15) and 3 before (`tests/test_main.py` collects 3). The claim at `:33` that "the 13 new tests failed" first therefore can't be accurate as written.
2. **README.md's "Files" section is out of date** (`README.md:41-47`):
   - It says the suite is `test_main.py`, but the tests now live in `tests/` (`test_main.py`, `test_expiry.py`, `conftest.py`).
   - It doesn't mention `AGENTS.md`/`CLAUDE.md`, `.claude/` or `docs/sessions/`.
   - "read all three files" no longer fits.
   - The implementer edited README.md and changed the "3 tests" note at `:9`, but left this section alone.
3. **Minor: two tests check only the status code.** `tests/test_expiry.py:73-75` (bad URL with an expiry) doesn't check `detail`, and `:63` (3650-day link) doesn't check `location`. The test rules ask for the status plus the relevant body field or header.
4. **Minor: the README example output is unrealistic** (`README.md:30`). A real `expires_at` includes microseconds (e.g. `...T12:00:00.123456+00:00`), and the example is dated in January when it's November. A note that the value is illustrative would cover it.

Nothing needs to change in `main.py`. Fixing 1 and 2 is enough to accept; 3 and 4 are optional.
