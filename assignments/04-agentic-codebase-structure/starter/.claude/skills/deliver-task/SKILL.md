---
name: deliver-task
description: Implement one numbered task from docs/TASKS.md in this link shortener, test-first, and finish with a verified summary. Use when asked to build, implement, or deliver a backlog task or a small API feature here.
argument-hint: <task number from docs/TASKS.md>
---

# Deliver task $ARGUMENTS

Follow these steps in order. Do not skip the failing-test step.

## 1. Read the task and the guidance
- Read task **$ARGUMENTS** in `docs/TASKS.md`. If no number was given, ask.
- Re-read `AGENTS.md` (boundaries, status-code contract, conventions).
- If a plan for this task exists in `docs/sessions/`, read it and follow it
  unless the code proves it wrong.

## 2. Inspect the related code and tests
- Read `main.py` end to end (it is short) and `tests/conftest.py`.
- Read the existing tests that touch the routes you will change.

## 3. State the contract before coding
Write a short list in your reply:
- Request/response changes (new fields, their types, defaults).
- Every new status code and exactly when it is returned.
- Edge cases: missing field, wrong type, zero/negative, too large, boundary.
- Files you expect to touch. Anything outside `main.py`, `tests/`, and
  `README.md` needs a reason.

## 4. Add failing behavioral tests
- New file `tests/test_<feature>.py`, following the test rules for `tests/`.
- Run `python -m pytest -q` and confirm the new tests **fail for the right
  reason** (wrong status/missing behavior, not an import or syntax error).

## 5. Implement the smallest change
- Change `main.py` only as much as the tests require.
- Repo-specific checks:
  - **Schema change?** `init_db()` must add the column to an existing
    `links.db` (check with `PRAGMA table_info`). Old rows must keep working.
  - **Time?** Read it from the `get_now` dependency, in UTC.
  - **Existing contract** (400 / 404 / 307) is unchanged.

## 6. Verify
- Run `python -m pytest -q`. All tests, old and new, must pass.
- Run it a second time (the suite must not depend on leftover state).
- Update the API section of `README.md` if the request or responses changed.

## 7. Summarize
Reply with:
- **Changed:** files and one line each.
- **Behavior:** the contract from step 3, now true.
- **Tests:** count before → after, and the pytest summary line.
- **Risks / not done:** anything left open (e.g. timezone, cleanup of old
  rows, limits you chose).
