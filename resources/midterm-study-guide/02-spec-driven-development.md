# Week 2 — Spec-Driven Development

Slides: [`lectures/02-specs-driven-development/`](../../lectures/02-specs-driven-development/) · Readings: [`resources/02-specs-driven-development/papers-to-read.md`](../02-specs-driven-development/papers-to-read.md)

## Core ideas

- **The SDLC became a loop.** Traditional SDLC is a line (plan → design → build → test → deploy → maintain). AI-native SDLC cycles in hours around coding AI. *Build shrinks; the work around it grows* (writing intent, spec review, verification, rules and evals). **Code is no longer the bottleneck** — planning, review and deployment set the pace, and human-speed approval steps stall.
- **Six stages, one artifact chain:** `intent.md` (plan; originator approves) → `spec.md` (design; product owner signs off) → `plan.md` (build; engineer interrogates it) → tests the agent can run itself (test; tests stay locked) → AI pre-review + named human approval (deploy) → alerts trigger read-only diagnosis and a PR; the fix starts as a new `intent.md` (maintain).
- **Autonomy goes down as risk goes up.** Development: act freely in a sandbox. Pull request: AI review + code owner. Production: nothing without a named human's approval; **the agent never approves its own work**. Incidents: small → log; larger → diagnose read-only; severe → propose a fix as a PR. Every allow / block / ask decision is logged.
- **Put team knowledge where the agent can read it:** project context file (conventions, commands, recurring mistakes — under a page), skills (team policies, versioned, *advisory*), hooks (scripts that block/allow/log — for rules that must hold with *no exceptions*).
- **User story vs requirements vs spec.**
  - *User story:* "As a [user], I want [goal] so that [reason]." Written by a PM, in user language, answers why and what — too vague to build from.
  - *Requirements:* "a condition or capability needed by a user to solve a problem or achieve an objective" (IEEE). What the system must do, never how. **Functional** (what it does: register, lock after 5 failures) vs **non-functional** (how well: < 300 ms, 99.9% uptime, 10 req/min per IP).
  - *Spec:* a written description of what a system must do and how well, agreed before building. Technical; written by an engineer. **Agents consume specs, not user stories.**
- **Definition of SDD:** a way of building software where a *written specification, not the code, is the source of truth*. Define what and why first; agents plan, build and verify against the spec. Chain: requirements → `spec.md` → `plan.md` → `tasks.md` → code.
- **Why ambiguity costs more with agents.** *Velocity:* a developer writes 50 lines on a wrong assumption; an agent writes 500. *Silence:* a human stops and asks; an agent resolves ambiguity on its own. Why models behave this way: they predict the *most likely* answer, not yours; context is their only memory; they are trained to finish, not ask; early choices compound. "Garbage in, clean-looking garbage out" — Song et al. (2023): many code-generation errors trace to requirements missing from the prompt.
- **Four human checkpoints:** spec review (before planning — highest leverage), plan review (before execution), code review (during execution), deployment review (before production).
- **Tell the agent when to stop and ask:** ambiguity (two valid options), divergence (a test still fails after 3 tries), contradiction (code contradicts the criteria), irreversibility (about to delete or migrate real data).
- **Let the agent interview you first** — answers replace guesses; make it a team activity.
- **Plan Mode is a bridge, not SDD.** Read-only until you approve; review the plan like a PR; its questions reveal gaps in your spec. But it is *transient* (lives in one chat) and *answers how, not what*. Workflow: Plan Mode on every non-trivial task → notice what you correct → write those things in `spec.md` first → use Plan Mode to check the agent read the spec.
- **Three levels of SDD maturity:**
  1. **Spec-first** — write the spec before the agent starts (goal, constraints, acceptance criteria). Use for any task over ~30 minutes of agent work.
  2. **Spec-anchored** — the spec lives in the repo and changes in the same PR, updated first. Use for code that keeps changing.
  3. **Spec-as-source** — people edit only the spec; code is generated from it. Still theoretical at scale; watch, don't adopt.
- **Two tiers of specs.** *Strategic:* rules file, ADRs, system requirements — living documents every session reads. *Tactical:* `spec.md` / `plan.md` / `tasks.md` per change — drive one feature, then stay as history.
- **What good specs look like.** Four headings: **Goal, Constraints, Acceptance criteria, Out of scope.** Beyond the happy path: failure mode, concurrency, observability, rollback. A bad spec ("add a caching layer to improve performance") lets the agent choose library, TTL, keys, invalidation and monitoring for you.
- **The SDD workflow.** One folder per change (`specs/001-feature/`) with `spec.md` (what and why — no file paths or tech choices), `plan.md` (how: approach, trade-offs, files, order), `tasks.md` (small tasks, each with a **done check**). One short prompt per phase: specify → plan → tasks → execute. Without a done check the agent stops too early or never stops; if a done check says "and" more than once, split the task.
- **SDD frameworks:** GitHub Spec Kit (constitution → specify → plan → tasks → implement → converge; open source, works with most agents), Kiro (AWS; EARS requirements → design → tasks; IDE with specs built in), OpenSpec (propose → apply → archive; lightweight on existing code), BMAD Method (analyst/PM/architect/developer agents; simulates a whole team), Tessl (one spec per code file; spec-as-source experiments).
- **Three things to remember:** the substrate changed, the discipline didn't; speed amplifies everything (a bad spec gets built fast too); match the ceremony to the risk.

## Required readings

- **Graziano, *AI-Native Software Engineering*, ch. 5 "Spec-Driven Development" (O'Reilly).** What makes a spec useful to an agent rather than merely descriptive to a human; which parts establish behaviour, constraints, verification and boundaries.
- **Piskala 2026, *Spec-Driven Development: From Code to Contract*.** A practitioner/position paper (not a controlled study). Specs become the source of truth; code is generated or verified against them. Defines **spec-first, spec-anchored, spec-as-source**. SDD has a cost — match rigor to risk, reversibility, domain complexity, coordination needs and lifetime.
- **Optional — Parnas & Clements 1986, *A Rational Design Process: How and Why to Fake It*.** Real design is messy and iterative; document the *rational* design without pretending requirements were always clear. Review must challenge premises, not just syntax and tests.

---

[Back to the study guide index](README.md)
