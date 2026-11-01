# Stage 3b — Re-review (claude -p --permission-mode plan, read-only)

**Prompt:** RE-REVIEW. Do not edit any files. docs/sessions/03-review.md returned REVISE with 4 findings. Check whether each finding is now addressed in the uncommitted change (`git diff -- .`, `git status`, README.md, tests/test_expiry.py, the correction note at the end of docs/sessions/02-implement.md), run `python -m pytest -q`, and check that the claims in writeup.md match the repo. End with exactly one verdict line, ACCEPT or REVISE, and a short explanation.

---

**REVISE.** Three of the four findings are fixed, but the fix for finding 1 adds a new false claim. One sentence in the correction note needs to change before this can be accepted.

I didn't edit any files. `python -m pytest -q` gives **18 passed in 0.24s**.

| # | Finding | Status |
|---|---------|--------|
| 1 | Test counts in `02-implement.md` | **Partly fixed, and the fix adds a false claim.** "3 → 18" and "15 new" are now correct (3 tests in `test_main.py` and 15 in `test_expiry.py`). But the note says **"All 15 failed before the `main.py` change"**. I ran the new tests against `HEAD:main.py` in a scratch copy: **13 failed, 2 passed**. The two that passed are `test_redirects_just_before_expiry` and `test_bad_url_still_400_with_expiry`, because both already worked before the change. So the original transcript's "the 13 new tests failed" was right about the failures, and the stage-3 review was wrong to doubt it. |
| 2 | README "Files" section | **Fixed.** It now lists `tests/` (`test_main.py`, `test_expiry.py`, `conftest.py`), `AGENTS.md`/`CLAUDE.md`, `.claude/rules/tests.md`, `.claude/skills/deliver-task/`, `docs/sessions/` and `writeup.md`. "Read all three files" is gone, and every listed path exists. |
| 3 | Tests that only checked the status code | **Fixed.** `test_expiry.py:78` now checks `detail` and `:65` checks `location`. Two other tests still check only a status, `:27` and `:100`, but the reviewer didn't name them. Optional. |
| 4 | Unrealistic README example | **Fixed.** `README.md:30` now shows `<now + 7 days, e.g. 2026-11-08T21:04:13.512345+00:00>`. |

**Claims in `writeup.md`:**
- **Correct:**
  - Claude Code 2.1.295 matches `claude --version`.
  - 18 tests pass (3 original + 15 new).
  - `AGENTS.md` is 48 lines.
  - The rule's `paths: ["tests/**/*.py"]` and its contents are described correctly.
  - The skill has 7 steps, and step 5 has the three checks described.
  - `CLAUDE.md` is just `@AGENTS.md`.
  - The review findings are summarized correctly.
- **Not yet true:** line 43 says "The re-review returned ACCEPT (`04-re-review.md`)". `04-re-review.md` contains only the prompt so far, and this verdict is REVISE.
- **Misleading:** line 47 says the reviewer "caught the errors" in the implementer's summary. The reviewer also wrongly doubted the "13 failed" claim. The lesson holds better if it says the reviewer needs checking too.

**What would get this to ACCEPT:**
- Change the correction note to "13 of the 15 failed before the change; the 2 that test behavior that already worked passed, and all 15 pass after."
- Optionally, update line 47 to match.
- Keep line 43 only if the next re-review actually returns ACCEPT.

REVISE — findings 2–4 are fixed and the suite is green, but the correction note now falsely says all 15 new tests failed before the change (13 did, 2 passed), and writeup.md:43 reports an ACCEPT that hasn't happened yet.
