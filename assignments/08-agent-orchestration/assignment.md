# Week 8 — Agent Orchestration: The Recipe Box Sprint

**Estimated time: ~3 hours.**

## Overview
One agent is useful; orchestrated agents are a workflow. You'll run **two agents
concurrently** on a small recipe app and implement a **generator–critic loop**.

A working starter app is in [`starter/`](starter/) — you extend it.

> **IDE-agnostic.** Use anything that runs more than one agent: **Antigravity's Agent
> Manager** (default), Warp tabs, or two CLI sessions. Isolate parallel work with
> **git worktrees**.

## Learning goals
- Run multiple agents concurrently without clobbering each other.
- Implement the **generator–critic loop**.
- Reason about concurrency wins and risks.

---

## Setup
```bash
cd starter && pip install -r requirements.txt && pytest   # 3 tests should pass
uvicorn main:app --reload   # open http://localhost:8000/
```
Tasks are in `docs/TASKS.md` (they're independent, so they parallelize).

## What to do (both parts)

### Part I — Concurrent agents (2 tasks in parallel)
Pick **two** independent tasks from `docs/TASKS.md`. Run **two agents at the same time**,
each in its own **git worktree**, and land both. Capture how you kept them from colliding.
```bash
git worktree add ../recipe-task-a -b task-a
git worktree add ../recipe-task-b -b task-b
```

### Part II — Generator–critic loop (1 task)
Take **one** task and run a loop: a **generator** agent writes the solution, a **critic**
agent reviews it against a short rubric (correctness, tests, clarity), and the generator
revises. Loop until the critic signs off — **show at least two revision rounds**.

## Deliverables
**Submit the GitHub repository link** for `starter/`, plus a `writeup.md`:
- Concurrency notes: which two tasks, your worktree setup, and any collisions/risks.
- The **generator–critic transcript** with its revision rounds.
- Autonomy levels you allowed each agent and how you supervised.
- **What you learned:** 3–5 sentences on orchestrating agents.

## Evaluation (100 pts)
- 40 — Two tasks genuinely completed by concurrent agents via worktrees.
- 40 — Generator–critic loop with ≥2 revision rounds, evidenced.
- 20 — `writeup.md` with autonomy notes + "what you learned".
