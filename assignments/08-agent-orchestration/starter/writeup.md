# Week 7 Writeup: Recipe Box Sprint

**Orchestrator:** Claude Code (main session), which spawned Claude Code subagents as the
workers. Each worker ran in its own **git worktree**.

## Part I: Concurrent agents

**Tasks:** Task 1 *Shopping list* (`GET /shopping-list?ids=`) and Task 2 *Tag filter*
(`GET /recipes?tag=`).

### Worktree setup
```bash
# base branch: assignment-week-7 (+ conftest.py giving every test its own temp SQLite DB)
git worktree add ../recipe-task-a -b w7-task-a-shopping-list assignment-week-7
git worktree add ../recipe-task-b -b w7-task-b-tag-filter    assignment-week-7
git worktree add ../recipe-task-c -b w7-task-c-scaling       assignment-week-7   # Part II
```
Agent A and Agent B were launched in the same orchestrator turn as background subagents.
Each was told its own worktree path and to never touch another directory.

| Agent | Worktree / branch | Started | Finished | Commit | Tests |
|---|---|---|---|---|---|
| A: shopping list | `recipe-task-a` / `w7-task-a-shopping-list` | 15:56:48 | 15:57:03 | `d3d9f07` | 7 passed |
| B: tag filter | `recipe-task-b` / `w7-task-b-tag-filter` | 15:56:49 | 15:57:07 | `9cd8eab` | 7 passed |

The two runs overlapped almost completely, so this was real parallel work. The
generator for Part II was also running at the same time in `recipe-task-c`.

### How I kept them from colliding
- **Separate checkouts:** each agent had its own worktree, so they never shared a working
  directory, an index, or a `recipes.db`.
- **Isolated state:** I added `conftest.py` to the base first, so each test uses a temp
  DB. Parallel test runs can't see each other's rows.
- **Edit zones written into each agent's brief:**
  - A could only *append* a block at the end of `main.py`.
  - B could only *modify* the existing `list_recipes` function.
  - Both appended tests at the end of `test_main.py` under a labelled comment.
  - Neither could touch the README, `index.html` or `conftest.py`.
- **Agents committed but did not push.** I merged both into `assignment-week-7` myself
  with `--no-ff`, so each task stays visible as its own merge.

### Collisions that happened
- `main.py` **merged cleanly**, because the edit zones did their job. A appended at the
  end, and B changed a function in the middle.
- `test_main.py` **conflicted**: both agents appended at the same spot (end of file). It
  was a pure "keep both" conflict, and I resolved it by keeping both sections. The merged
  suite passed 11 tests.
- The Task 3 merge later hit the same end-of-file conflict in both files. I resolved it
  the same way, giving 20 passed.

**Risks / lessons:** "append at the end of the file" is the classic hotspot when work
runs in parallel. Giving each agent its own test file (`test_shopping_list.py`, etc.)
would have avoided the conflict completely. Shared files such as imports, `conftest.py`
and schema migrations are the real risk. I kept those off-limits, and the one shared
change (`conftest.py`) went in *before* the agents were launched.

## Part II: Generator–critic loop (Task 3: ingredient scaling)

- **Generator:** one subagent working in `recipe-task-c`. It was resumed with its full
  context for each revision.
- **Critic:** a *separate* subagent that was not allowed to edit code. It scored the work
  against a rubric (correctness, tests, clarity; each 1–5) and had to **run** probes
  against the real code rather than speculate. Its rule: APPROVE only if every score is ≥4
  and no MUST items remain.
- The critic's full reviews are in [`docs/generator-critic/`](docs/generator-critic/).

| Round | Generator commit | Critic scores (C / T / Cl) | Verdict | Key findings |
|---|---|---|---|---|
| 1 | `ee2b7a0`: regex + `Fraction`, 6 tests | 2 / 3 / 4 | **REVISE** | 3 MUSTs: `"2-3 eggs"`→`"4-3 eggs"`; `"1,5 l"`→`"2,5 l"`; `"1/0 cup"` causes a **500**. SHOULDs: tiny results round to `"0 g"`; echo `factor`. |
| 2 | `48e8b2d`: ranges, decimal comma, catch `ZeroDivisionError`, sig-fig fallback, `factor ≥ 0.01`, echo factor, 11 tests | 3 / 4 / 4 | **REVISE** | New MUST *introduced by the fix*: `"1,500 g flour"`→`"3 g flour"` (1000× wrong). |
| 3 | `1263821`: `_parse()` treats `1,500` as thousands and `1,5` as a decimal; mixed `.`/`,` left unchanged; 12 tests | 4 / 4 / 4 | **APPROVE** | No MUSTs. `"1.500 g"` read as 1.5 is accepted as a documented locale ambiguity. |

That is **2 revision rounds** before sign-off. The most interesting moment was round 2:
fixing the decimal comma *created* a worse bug (thousands separators off by 1000×). The
generator listed it as a "known limitation", but the critic correctly ruled it a MUST
because it's the same class of silent wrong quantity. The generator would have shipped
it without the loop.

## Autonomy levels and supervision

| Agent | Autonomy allowed | How I supervised |
|---|---|---|
| A, B (parallel workers) | High inside their worktree: read, edit, run tests, commit. **No push, no merge**, no edits outside their zone. | Checked their reported timestamps, commit hashes and test output. I did the merges and conflict resolution and re-ran the full suite. |
| Generator | Same as A/B, but only in `recipe-task-c`. | Passed each critic review to it word for word. I set the scope of what to fix (all MUSTs plus selected SHOULDs) so it didn't gold-plate. |
| Critic | **Read-only** for app code. It could only run tests and write probe scripts and review files. | A fixed rubric, plus "evidence or it didn't happen": every finding needed an input → actual vs expected that it had actually run. |
| Orchestrator (me) | Merges, resolving conflicts, pushing. | Final step: a separate verifier agent re-checked everything independently (see below). |

## Final verification (independent verifier agent)
After merging, a fresh agent was given only the assignment spec and the repo (none of my
conclusions). It was told to verify every claim by running commands and not to change
anything. It:
- re-ran the suite (20 passed)
- probed all three new endpoints and the original ones for regressions (no 500s, no
  route clash between `/recipes/{id}` and `/recipes/{id}/scaled`)
- checked that every commit hash, branch, worktree and merge cited here exists
- spot-checked the critic's claims against the code (`"1,500 g flour"`→`"3000 g flour"`,
  `"2-3 eggs"`→`"4-6 eggs"`, `"1/0 cup"`→unchanged with a 200)

Its verdict was **NEEDS FIXES**. These were the findings, and all were fixed afterwards:
1. The writeup wasn't committed yet and the branch wasn't pushed.
2. This section was missing even though the autonomy table pointed to it.
3. Imports had ended up in the middle of `main.py` / `test_main.py` (E402), left behind
   by the append-only edit zones. They're now moved to the top. This is a nice concrete
   cost of the collision-avoidance rule.
4. `/shopping-list` returned **400** for bad input while the rest of the app returns
   **422**, and it called `-1` a "non-integer". It now returns 422 with the message "ids
   must be positive integers".
5. `str.isdigit()` accepted full-width digits (`１`). The check is now ASCII-only.

## What I learned
Orchestration is mostly about **dividing the work so agents can't collide**: separate
worktrees and up-front edit zones made `main.py` merge cleanly, and the one place I left
shared (the end of `test_main.py`) is exactly where the conflicts came from. The
generator–critic loop was worth it. Every round found a real, silent wrong-quantity bug
that the generator's own green tests missed, and round 2 showed that fixes can introduce
new bugs, so the critic has to re-check old cases every time. Making the critic
read-only and requiring it to run its probes kept the reviews concrete instead of
nitpicky. The human role moves from writing code to setting boundaries, rubrics and
stopping rules, and doing the final integration.
