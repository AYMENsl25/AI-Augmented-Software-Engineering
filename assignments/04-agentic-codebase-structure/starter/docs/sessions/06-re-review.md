# Stage 3d — Re-review 3 (claude -p --permission-mode plan, read-only)

**Prompt:** RE-REVIEW 3. Do not edit any files. docs/sessions/05-re-review.md returned REVISE: the correction note at the end of docs/sessions/02-implement.md gave the wrong number of test functions, and writeup.md claimed a verdict before it happened. Check that both are fixed and that the findings in 03-review.md and 04-re-review.md stay fixed. Run `python -m pytest -q` and verify every numeric and factual claim in writeup.md and in that correction note against the repo (you may run the new tests against `git show HEAD:./main.py` in a scratch copy outside the repo). writeup.md points to this transcript, 06-re-review.md, for the final verdict and should not claim it. End with exactly one verdict line, ACCEPT or REVISE, and a short explanation.

---

## Re-review 3: link-shortener expiry change (task 3)

Both findings from 05 are fixed, and the findings from 03 and 04 are still fixed. I didn't edit any files.

**Test runs**
- `python -m pytest -q` passed twice: **18 passed in 0.24s** both times. `tests/test_main.py` on its own: **3 passed**.
- I ran `tests/test_expiry.py` against `git show HEAD:./main.py` in a scratch copy outside the repo: **13 failed, 2 passed**. The 2 that passed are `test_redirects_just_before_expiry` and `test_bad_url_still_400_with_expiry`. The 13 failed for the expected reasons: the `expires_at` key was missing, a link redirected (307) where 410 was expected, an invalid value returned 200 where 422 was expected, and the upgrade test's assertion failed.

**The two findings from 05**

| Finding | Status |
|---|---|
| Correction note gave the wrong number of test functions | **Fixed.** The note now says "15 (10 test functions, one parametrized over 6 invalid values)". `tests/test_expiry.py` has 10 `def test_` functions, and `test_rejects_invalid_expiry` is parametrized over `[0, -1, 3651, "5", 1.5, True]`, so 9 + 6 = 15. |
| writeup.md claimed a verdict before it happened | **Fixed.** Section 5 now says "Re-review `05` found a wrong function count. The final verdict is in `06-re-review.md`." It doesn't claim ACCEPT or REVISE. |

**Every claim in the correction note checks out**
- The suite went from 3 to 18 tests: `test_main.py` has 3 and `test_expiry.py` has 15.
- 13 of the 15 fail on the old `main.py`.
- The 2 that pass are the two regression guards named in the note.
- All 15 pass after the change.
- The original transcript's "13 failed" was correct.

**The findings from 03 and 04 are still fixed**
1. **Counts:** writeup.md says the implementer reported "5 before and 13 new", and that the real numbers were 3 and 15. `02-implement.md` does say "5 before → 18 after" and "13 tests", so the description is accurate.
2. **README "Files" section:** it lists `tests/`, `AGENTS.md`/`CLAUDE.md`, `.claude/rules/tests.md`, `.claude/skills/deliver-task/`, `docs/sessions/` and `writeup.md`. Every listed path exists.
3. **Tests that only checked the status code:** the bad-URL test now checks `detail`, and the 3650-day test checks `location`.
4. **README example:** it is marked as illustrative and includes microseconds.
5. **"All 15 failed" (from 04):** the note now says 13 of 15, which matches my run.

**`main.py` still follows the repo conventions**
- 400, 404 and 307 are unchanged, and the new 410 has the detail `"link expired"`.
- `datetime.now` appears only inside `get_now`, and both routes read time from it.
- `init_db()` checks `PRAGMA table_info` and runs `ALTER TABLE ... ADD COLUMN expires_at`, so an existing `links.db` is upgraded.
- `requirements.txt` is unchanged, so there are no new dependencies.

**Claims in writeup.md**

All are correct:
- Claude Code 2.1.295 matches `claude --version`.
- The suite has 18 tests: 3 original and 15 new.
- `AGENTS.md` is 48 lines, and `CLAUDE.md` contains only `@AGENTS.md`.
- The rule has `paths: ["tests/**/*.py"]`. It requires `TestClient`, a temp database per test and the `clock` fixture, and it bans asserting on `"b"`, `time.sleep` and the real clock. It also asks for tests on both sides of a time boundary.
- The skill has 7 steps, and step 5 has the three checks: migrate old databases, use `get_now`, and keep 400/404/307.
- The planning findings match `01-plan.md`: `strict=True` rejects `"5"`, `1.5` and `true`, and the 3650 cap prevents a 500.
- The summaries of 03, 04 and 05 are accurate.

One wording point that doesn't block acceptance: section 6 says each wrong claim "was caught the same way: by running `pytest`". The 03 README finding and the 05 function count were caught by reading files, not by running pytest. "By checking against the repo" would be more precise.

ACCEPT: both 05 findings and all 03 and 04 findings are fixed, the suite passes (18 passed), the run against the old `main.py` confirms the note's 13 failed and 2 passed, and every number and fact in writeup.md and the correction note matches the repo.
