# Week 4 — Structuring a Repo for Agents: The Link Shortener

**Estimated time: ~2 hours.**

## Overview

A coding agent works best when a repository explains how to navigate, change, and verify it. In this assignment, you will make a small **link shortener** easier for an unfamiliar coding agent to work in.

The application is already implemented in [`starter/`](starter/). Your job is not to rebuild it. You will add a small agent-readiness layer, then use it to complete one feature.

A complete example of an agent-ready repository: https://github.com/scottyUX/agent-ready-ticket-api

> **Tool-agnostic.** Use the coding agent you selected earlier in the course. Different tools use different filenames and directories. The assignment evaluates the purpose and behavior of your artifacts, not a specific IDE.

## Learning goals

- Give an agent concise repository-wide context.
- Separate always-relevant guidance from instructions that apply only in one area.
- Turn a repeated development procedure into a reusable workflow.
- Use planning, implementation, and review as distinct stages of an agent-assisted change.

---

## Setup

```bash
cd starter
pip install -r requirements.txt
pytest                       # 3 tests should pass
uvicorn main:app --reload    # http://localhost:8000
```

Before changing anything, read:

- `README.md`
- `main.py`
- `test_main.py`
- `docs/TASKS.md`

The starter is intentionally small: one application file, one test file, and three feature choices.

## What to do

### 1. Create repository guidance

Create a root `AGENTS.md` that helps an unfamiliar agent work in this repository.

Include:

- What the application does.
- Where the important files are.
- How to install, run, and test it.
- Product boundaries: what belongs in this small service and what does not.
- A short change workflow: understand → test → implement → verify.

Keep the file concise. Aim for no more than about 60 lines. It should orient the agent, not contain every possible rule or procedure.

See [agents.md](https://agents.md/) for the cross-tool convention.

### 2. Add one scoped instruction

Create one instruction that applies only to part of the repository.

The recommended tool-neutral option is `tests/AGENTS.md`. It could require:

- Tests through the public API.
- Success and failure coverage.
- Independent tests that do not rely on execution order.
- Assertions about behavior rather than private implementation details.

You may instead use your agent's native scoped-rule feature. For example, some tools support path patterns or file globs.

In `writeup.md`, explain:

- Which files activate the instruction.
- Why this guidance should not be loaded for every task.
- How your selected agent discovers it.

### 3. Create one reusable workflow

Create one reusable skill, command, or saved workflow for implementing a feature in this repository.

It should guide the agent through:

1. Read the selected task and repository guidance.
2. Inspect the related code and tests.
3. State the expected behavior and affected files.
4. Add a failing behavioral test.
5. Implement the smallest change that satisfies the task.
6. Run `pytest`.
7. Summarize the change and any remaining risks.

Use your agent's native reusable-workflow mechanism. If it supports the Agent Skills standard, use a `SKILL.md` file. Otherwise, use its equivalent and document the mapping.

### 4. Complete one feature

Choose **one** task from `docs/TASKS.md`.

Use three distinct stages:

1. **Plan** — ask the agent to inspect the task and propose a plan without editing.
2. **Implement** — invoke your reusable workflow and complete the feature with tests.
3. **Review** — ask the agent to inspect the final change without editing and return `ACCEPT` or `REVISE` with a short explanation.

If the review returns `REVISE`, address the findings before submitting.

Run `pytest` and confirm that the original tests and your new tests pass.

## Deliverables

Submit the GitHub repository link for your completed `starter/` project. Include:

- `AGENTS.md`
- One scoped instruction
- One reusable workflow
- The implemented feature and its tests
- `writeup.md`

Your `writeup.md` should briefly answer:

1. What information did you put in `AGENTS.md`, and why should it be broadly available?
2. What instruction did you scope, and when does it load?
3. What procedure does your reusable workflow encode?
4. How does your selected agent discover or invoke each artifact?
5. What did the agent identify during planning or review that improved the result?
6. What did you learn about structuring a repository for coding agents?

Aim for **400–500 words**.

## Evaluation (100 pts)

- **25** — Concise and useful `AGENTS.md`
- **20** — Appropriately scoped instruction
- **20** — Clear, reusable workflow
- **25** — Working feature with meaningful success and failure tests
- **10** — Tool mapping and reflection in `writeup.md`

## Scope

You do **not** need to create hooks, custom subagents, plugins, or a new application architecture. Those are useful advanced mechanisms, but this assignment focuses on the smallest useful agent-ready repository:

```text
repository context → scoped guidance → reusable procedure → verified change
```
