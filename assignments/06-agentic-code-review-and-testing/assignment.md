# Week 6 — AI Code Review & Testing: The Habit Tracker

**Estimated time: ~3 hours.**

## Overview
Trustworthy agentic development needs both **deterministic guardrails** (tests/lint) and
**LLM-based review**. You'll add **two** features to a small habit-tracker on branches,
open PRs, run an **AI reviewer**, and compare its review to your own.

A working starter app is in [`starter/`](starter/) — you extend it, you don't build it.

> **IDE-agnostic.** Implement with your Week 1 agent (Antigravity by default). For the
> AI review, use any AI PR reviewer — **Graphite Diamond** (default), CodeRabbit, or
> Copilot review. Name the one you used.

## Learning goals
- Set up deterministic guardrails as a first line of defense.
- Practice agent-driven implementation with disciplined human review.
- Compare human vs. AI review and form heuristics for trusting AI reviews.

---

## Setup
```bash
cd starter && pip install -r requirements.txt && pytest   # 3 tests should pass
uvicorn main:app --reload
```
Sign up for your AI reviewer (Graphite: https://app.graphite.dev/signup) and install its
GitHub app so it can comment on PRs.

## What to do
**Part I — guardrails.** Add lint+format (black+ruff) and confirm `pytest` fails the
build on a failing test. Document the commands.

**Part II — two features (from `docs/TASKS.md`).** For **each** of two tasks:
1. Branch, implement with your agent (one-shot prompt), add/update tests.
2. **Manually review** the diff line-by-line; note issues (correctness, naming, test
   gaps, API shape…) and fix them.
3. Open a **PR** (problem + approach, testing done, tradeoffs).
4. Run your **AI reviewer** on the PR.

## Deliverables
**Submit the GitHub repository link** for `starter/` (with the two PRs) and a `writeup.md`:
- **Two PRs**, each with a clear description, commit links, and visible AI review comments.
- Your guardrail setup (commands + what they catch).
- A comparison: **your** review comments vs. **the AI's** for each PR — where the AI was
  better/worse, with examples.
- **What you learned:** 3–5 sentences on combining guardrails with LLM review, and your
  comfort trusting AI reviews.

## Evaluation (100 pts)
- 30 per task (×2 = 60): correctness + tests, depth of your manual review, AI review present.
- 20 — Guardrails set up and documented.
- 20 — Human-vs-AI comparison + "what you learned".
