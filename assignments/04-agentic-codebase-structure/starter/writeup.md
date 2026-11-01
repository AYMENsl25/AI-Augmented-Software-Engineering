# Week 4 Writeup — Agent-Ready Link Shortener (Task 3: Expiry)

**Agent:** Claude Code 2.1.295. Each stage was a separate headless session (`claude -p`); transcripts are in `docs/sessions/`. **Result:** `python -m pytest -q` → 18 passed (3 original + 15 new).

## 1. What is in `AGENTS.md`, and why is it broadly available?

The purpose, a file map, the commands, product boundaries (one file, SQLite, no auth), and a four-step workflow. It also lists conventions any change can break: the 400/404/307 codes are a contract, time comes from `get_now`, and a schema change must upgrade an existing `links.db`. Every task needs these from the first turn. It is 48 lines.

## 2. What did I scope, and when does it load?

`.claude/rules/tests.md` has `paths: ["tests/**/*.py"]`, so it loads only when the agent reads or edits a file under `tests/`. It requires `TestClient` and a temp database per test, and it bans asserting on generated codes like `"b"`. For time, it bans `time.sleep` and the real clock, requires the `clock` fixture, and asks for a test on both sides of every time boundary. A docs fix doesn't need any of this, so loading it everywhere would waste context.

## 3. What procedure does the workflow encode?

`.claude/skills/deliver-task/SKILL.md`, invoked as `/deliver-task 3`, has seven steps:

1. Read the task and the guidance.
2. Inspect the code and tests.
3. State the contract: fields, status codes, edge cases.
4. Write failing tests and confirm they fail for the *right reason*.
5. Make the smallest change.
6. Run pytest twice.
7. Summarize the change and its risks.

Step 5 adds checks for this repo: migrate old databases, use `get_now`, and keep the status codes unchanged.

## 4. How does Claude Code discover each artifact?

- **`CLAUDE.md`** loads at session start. It contains only `@AGENTS.md`, because Claude Code doesn't read `AGENTS.md` natively; other agents do.
- **The rule** loads when a file matches its glob.
- **The skill** is listed by its description. It runs as `/deliver-task`, or the agent picks it when the request matches. The implement transcript follows its steps and summary format.

## 5. What did planning and review catch?

**Planning** found two input bugs before any code existed. Without `strict=True`, Pydantic accepts `true` and `"5"` as integers. A huge `expires_in_days` overflows `timedelta` into a 500, so the plan capped it at 3650 days.

**Review** (`03`) returned **REVISE**:

- The implementer had miscounted the tests (it said 5 before and 13 new; it was 3 and 15).
- The README file list still pointed at the old `test_main.py`.
- Two tests checked only the status code.

I fixed these and added a correction note instead of rewriting the transcript. Then my note was wrong too. Re-review `04` ran the new tests against the old `main.py`: 13 failed and 2 regression guards passed, not "all 15". Re-review `05` found a wrong function count. The final verdict is in `06-re-review.md`.

## 6. What I learned

Guidance specific to this repo did more than generic advice. The `clock` fixture and the "both sides of the boundary" rule produced tests one second before expiry and exactly at it. Separate stages also mattered. Every stage, including mine, made a confident claim that turned out to be wrong. Each was caught the same way: by checking it against the repo, running `pytest` or reading the files, instead of trusting a summary.
