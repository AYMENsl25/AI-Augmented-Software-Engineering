# Week 6 Writeup: Habit Tracker, Guardrails + Human vs. AI Review

**Implementation agent:** Claude Code · **AI reviewer:** <!-- TODO: Graphite Diamond / CodeRabbit / Copilot -->

| PR | Branch | Link |
|---|---|---|
| Task 2: Validation | `week6-validation` | <!-- TODO: PR URL --> |
| Task 1: Streak | `week6-streak` | <!-- TODO: PR URL --> |

Both PRs target `assignment-week-6`, which holds the Part I guardrails. Each PR has two
commits: the raw first agent pass, then my review fixes, so the diff between them shows
exactly what the human review changed.

## Part I: Guardrails

| Command | What it catches |
|---|---|
| `ruff check .` | Lint: unused or unsorted imports, pyflakes errors, bugbear smells (e.g. B904 `raise` without `from`), outdated syntax. Rules `E,F,I,B,UP` in `pyproject.toml`. |
| `black --check .` | Formatting drift (line length 100). `black .` fixes it. |
| `pytest` | Behaviour regressions. Each test gets its own temp SQLite file (`conftest.py`), so tests are isolated and never touch `habits.db`. |
| `sh check.sh` | All three in order with `set -e`. Exits non-zero on the first failure. |
| CI: `.github/workflows/week6-habit-tracker.yml` | Runs `check.sh` on every push or PR that touches `starter/`, so a red check blocks the PR. |

Setup: `pip install -r requirements-dev.txt`.

**Proof that it fails the build:** I appended `assert 1 == 2` as a test and `check.sh`
exited `1` (`1 failed, 3 passed`). A file with `import os` unused and unsorted made ruff
fail with `I001`/`F401`. After reverting both, it exited `0`.

**What the guardrails caught in practice:** unsorted imports in both first passes, and
B904 in the validation pass. **What they could not catch:** every real logic bug below.
All tests were green on both first passes.

## Human vs. AI review

### PR 1: Validation

| # | My review | AI reviewer |
|---|---|---|
| 1 | `"   "` accepted as a name (`v == ""` check) | <!-- TODO --> |
| 2 | `date.fromisoformat` accepts `20260922` / `2026-W39-1`, stored unnormalised | <!-- TODO --> |
| 3 | Tests asserted only the status code, not the message or that nothing was stored | <!-- TODO --> |
| 4 | No max length on name | <!-- TODO --> |
| — | <!-- TODO: anything the AI raised that I missed --> | |

### PR 2: Streak

| # | My review | AI reviewer |
|---|---|---|
| 1 | Duplicate same-day check-ins reset the streak | <!-- TODO --> |
| 2 | Future-dated check-in zeroes the streak | <!-- TODO --> |
| 3 | Unknown habit returns 200 instead of 404 | <!-- TODO --> |
| 4 | Malformed stored day gives a 500 | <!-- TODO --> |
| 5 | `date.today()` inline makes tests clock-dependent | <!-- TODO --> |
| 6 | "No check-in yet today = 0" is a product decision; flagged | <!-- TODO --> |
| — | <!-- TODO: anything the AI raised that I missed --> | |

### Where the AI was better / worse
<!-- TODO after the AI review runs. Give 2–3 concrete examples: something it caught that
     you missed (or vice versa), any false positives or nitpicks, and whether it understood
     the domain (e.g. the streak "today" semantics). -->

## What I learned
<!-- TODO: revise once you've seen the AI review. Draft: -->
Guardrails and LLM review catch different classes of problem. Ruff, black and pytest
caught every style and import issue instantly and deterministically, but both first
passes were fully green while still hiding real logic bugs: duplicate days breaking
streaks, and non-canonical ISO dates slipping through validation. I found those by
reasoning about edge cases and probing the API, which is exactly the kind of semantic
review an LLM reviewer can also attempt. Because its output isn't deterministic, I treat
an AI review as a second pair of eyes that raises questions, not a gate: each comment
gets verified against the code and a test before I act on it, and the deterministic
checks stay as the hard requirement for merging.
