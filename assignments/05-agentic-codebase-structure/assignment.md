# Week 5 — Structuring a Repo for Agents: The Link Shortener

**Estimated time: ~3 hours.**

## Overview
A codebase an agent works in well looks different from one built only for humans. You'll
make a small **link shortener** *agent-native*: give it context/rules, a guardrail hook,
a reusable workflow, and use role-specialized **subagents** to ship one feature.

A working starter app is in [`starter/`](starter/) — you don't build the app, you make
it agent-ready.

> **IDE-agnostic.** Use the agent from Week 1 (**Antigravity** by default). The concepts
> below exist in every modern agent; map each to your agent's equivalent and note it.

## Learning goals
- Use rules and guardrails to shape agent behavior.
- Author the cross-tool `AGENTS.md` and an `intent.md`.
- Wire a **hook** for a lint/test gate.
- Apply the **planner / implementer / reviewer** subagent pattern.

---

## Setup
```bash
cd starter && pip install -r requirements.txt && pytest   # 3 tests should pass
uvicorn main:app --reload
```
Read `main.py` and `docs/TASKS.md`.

## What to do (all four)
1. **`AGENTS.md`** (+ `intent.md`) — document how to run the app, where things live,
   safe vs. forbidden commands, and the workflow "new endpoint: failing test → implement
   → run the hook". (See https://agents.md/.)
2. **One hook** — a git `pre-commit` hook (or your agent's hook) that runs lint/format +
   `pytest` and **blocks** on failure. Show it catching a bad change.
3. **One reusable workflow/command** — e.g. a "run tests + summarize failures" command
   using your agent's saved-workflow feature (or a `docs/PLAYBOOKS.md` prompt).
4. **Subagents** — use planner → implementer → reviewer to complete **one** task from
   `docs/TASKS.md` (code + a test), reviewing before you accept.

## Deliverables
**Submit the GitHub repository link** for `starter/`, with `AGENTS.md`, `intent.md`, the
hook, and your workflow committed, plus a `writeup.md`:
- Each artifact: what it does and which agent feature you mapped it to.
- A screenshot of the hook blocking a failing change.
- The subagent transcript completing the task.
- **What you learned:** 3–5 sentences on structuring a repo for agents.

## Evaluation (100 pts)
- 30 — `AGENTS.md` + `intent.md` that meaningfully guide the agent.
- 25 — A **working hook** that blocks on failure (evidence shown).
- 25 — Subagent (planner/implementer/reviewer) pattern completing one task.
- 20 — Reusable workflow + `writeup.md` reflection.
