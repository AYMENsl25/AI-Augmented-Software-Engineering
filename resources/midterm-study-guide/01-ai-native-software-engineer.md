# Week 1 — The AI-Native Software Engineer

Slides: [`lectures/01-setup-environments/`](../../lectures/01-setup-environments/) · Readings: [`resources/01-setup-environments/papers-to-read.md`](../01-setup-environments/papers-to-read.md)

## Core ideas

- **Engineering is not programming.** Programming is a bounded act (hold the problem in your head, write the solution, make tests pass). Engineering is keeping systems working: requirements, design, validation, change. Coding shrinks with AI; everything else grows.
- **The spectrum: vibe coding → structured AI-assisted → agentic engineering.** The differentiator is *not* whether you use AI; it is **how outputs get verified**. Know the dimensions of the spectrum table: intent specification, verification, codebase understanding, error handling, appropriate scope, risk profile.
  - Vibe coding: casual prompts, "does it seem to work?", copy-paste errors back to the AI, prototypes and hackathons, high risk acceptable for disposable code.
  - Structured AI-assisted: detailed prompts with examples and constraints, manual testing and spot checks, features in established codebases, human judgment at checkpoints.
  - Agentic engineering: formal specs and architecture docs, automated test suites / CI gates / LLM judges, production systems at scale, systematic verification at every stage.
- **The role shift: implementer → orchestrator.** Less time typing; more time thinking, specifying, reviewing and deciding. When the agent gets it wrong, *fix the gap in the spec* rather than *rephrase and hope* (a random walk).
- **Human-in-the-loop is the non-negotiable checkpoint.** You own every commit. The agent is a collaborator, not a co-author. Stay close at high stakes (migrations, architecture, production data).
- **What AI-native engineers actually do.** *Before:* write behaviour, constraints, edge cases and acceptance criteria first; set up context (rules files are infrastructure). *During:* review against criteria, not gut feel; test for agent mistakes (edge cases, error paths, boundaries); diagnose the gap before re-running. *Throughout:* own every commit, invest in context, use AI for all the work (docs, PRs, design exploration).
- **The new skill stack:** spec literacy, context engineering, orchestration, verification discipline, risk ownership, systems thinking, communication and translation, harness engineering.
- **Five emerging patterns (Google I/O 2026):**
  1. *Shift up* — higher altitudes: the *why* (context) over the *what* (code).
  2. *Shift left* — structured intent: intent becomes a source of truth (e.g. `INTENT_SPEC.md`); intent > implementation.
  3. *System design: the environment* — build for continuous feedback and validation; verified output > faster code.
  4. *System design: the workforce* — capability > job title; small cross-functional teams at large scale.
  5. *System design: new values* — intelligent failure > the status quo; adaptability and learning.
- **Juniors in the age of AI.** AI writes the boilerplate juniors used to learn from, and "it's easier than ever to be wrong in a way nobody notices." Habits that build a foundation: reach for the harder problem, go one layer deeper, do the design work, read and write docs, understand every line, own it and keep learning. The skills above any technology: problem-solving, critical thinking, communication, working with AI.

## Numbers and studies to recognise

- DORA 2025: ~90% of software engineers use AI at work; ~40% rely on it a lot; ~3/4 of code at Google is AI-generated.
- Anthropic, *How AI assistance impacts the formation of coding skills* (2026): 52 mostly-junior engineers, Trio task. AI-assisted group was ~2 minutes faster (not significant) but scored **17 percentage points lower** on the knowledge quiz (50% vs 67%, p = 0.010). *Bottom line: AI may make you faster on a task while reducing how much you learn from it.*

## Required readings

- **Peng et al. 2023, *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot*.** Controlled experiment; developers implemented a JavaScript HTTP server with or without Copilot. Copilot group finished **55.8% faster**. Know what it does *not* show: a universal productivity gain, or anything about quality, maintainability, review effort or learning. "Developer productivity" is a measurement choice.
- **Hassan et al. 2024, *Towards AI-Native Software Engineering (SE 3.0)*.** A *vision* paper, not evidence: intent-centric, conversation-oriented development where AI moves from task-level copilot toward teammate. Be able to tell a vision claim from an empirical result.
- **Course reading principle:** for every paper — what is the claim, what evidence supports it, where does the evidence apply and not apply, what would change your mind?

---

[Back to the study guide index](README.md)
