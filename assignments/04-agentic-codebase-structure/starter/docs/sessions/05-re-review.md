# Stage 3c — Re-review 2 (claude -p --permission-mode plan, read-only)

**Prompt:** RE-REVIEW 2. Do not edit any files. docs/sessions/04-re-review.md returned REVISE: the correction note at the end of docs/sessions/02-implement.md claimed all 15 new tests failed before the change, and writeup.md reported an ACCEPT that had not happened. Check that both are fixed and that the earlier findings in docs/sessions/03-review.md stay fixed. Run `python -m pytest -q`, and check that every claim in writeup.md matches the repo. Note that writeup.md names this run as 05-re-review.md, the file this transcript is being written to. End with exactly one verdict line, ACCEPT or REVISE, and a short explanation.

---

The two fixes from 04 are in place, but the correction note now has a different wrong count, so this round is REVISE. I didn't edit any files.

**Test runs**
- `python -m pytest -q` passed twice: **18 passed in 0.23s**, then **18 passed in 0.25s**.
- `tests/test_main.py` collects 3 tests, and the suite collects 18 in total.
- I also ran `tests/test_expiry.py` against `HEAD:main.py` in a scratch copy: **13 failed, 2 passed**.

**The two findings from 04-re-review**

| Finding | Status |
|---|---|
| Correction note said all 15 new tests failed before the change | **Fixed.** The note at the end of `docs/sessions/02-implement.md` now says 13 of the 15 fail on the old `main.py`. It says the other 2 pass because they check behavior that already worked: `test_redirects_just_before_expiry` and `test_bad_url_still_400_with_expiry`. It also says all 15 pass after the change. My run matches all of this. |
| writeup.md reported an ACCEPT that hadn't happened | **Reworded.** It now says the first re-review returned REVISE, and that a second re-review (`05-re-review.md`) returned ACCEPT. That sentence is only true if this run accepts, and it doesn't, so it is false again (see below). |

**New error in the correction note**
- The note says `test_expiry.py` adds 15 tests as "**9 test functions**, one parametrized over 6 invalid values".
- The file actually has **10** test functions: 9 plain ones plus `test_rejects_invalid_expiry`, which runs 6 times. 9 + 6 = 15.
- Read as written, "9 functions, one parametrized over 6" gives 8 + 6 = 14.
- Like the earlier mistakes, this is a test-count error in a note whose whole purpose is to correct counts.

**Findings from 03-review are still fixed**
1. **Counts:** "3 → 18" and "15 new" are correct, apart from the function count above.
2. **README "Files" section:** it lists `tests/` (`test_main.py`, `test_expiry.py`, `conftest.py`), `AGENTS.md`/`CLAUDE.md`, `.claude/rules/tests.md`, `.claude/skills/deliver-task/`, `docs/sessions/` and `writeup.md`. Every listed path exists.
3. **Tests that only checked the status code:** the bad-URL test now checks `detail`, and the 3650-day test checks `location`.
4. **README example:** it is marked as illustrative and includes microseconds.

`main.py` still keeps 400, 404 and 307 unchanged, reads time from `get_now`, and upgrades an old `links.db` in `init_db()` by checking `PRAGMA table_info`.

**Claims in writeup.md**
- **Correct:**
  - Claude Code 2.1.295 matches `claude --version`.
  - 18 tests pass, 3 original plus 15 new.
  - `AGENTS.md` is 48 lines, and `CLAUDE.md` is just `@AGENTS.md`.
  - The rule has `paths: ["tests/**/*.py"]`, and its contents are described correctly.
  - The skill has 7 steps, and step 5 has the three checks described.
  - The planning findings (`strict=True`, the 3650 cap) match `01-plan.md`.
  - The summaries of the review and of the first re-review are accurate, including 13 failed and 2 passed.
  - Section 6 now mentions the reviewer's wrong doubt about "13 failed".
- **False:** the claim that "A second re-review returned ACCEPT (`05-re-review.md`)". This run returns REVISE.

**To reach ACCEPT**
1. In the correction note, change "9 test functions, one parametrized over 6 invalid values" to "10 test functions, one parametrized over 6 invalid values".
2. In writeup.md, report this REVISE and name the run that actually returns ACCEPT. Only claim an ACCEPT after it happens.

REVISE: both 04 findings and all 03 findings are fixed and the suite is green (18 passed), but the correction note now says "9 test functions" where there are 10, so writeup.md's claim that this run returned ACCEPT is false.
