# AI-Augmented Software Engineering

Course materials for the **AI-Augmented Software Engineering** lecture series.

This repository collects lecture notes, slides, code examples, assignments, and resources exploring how modern AI tools change the way software is designed, built, tested, and maintained.

## Course Overview

AI-augmented software engineering is the practice of using AI systems — code assistants, agents, and LLM-based tooling — as active collaborators across the software development lifecycle. This course covers both the *how* (practical use of these tools) and the *why* (their strengths, limits, and implications for engineering practice).

## Lectures

1. [Setup Environments](lectures/01-setup-environments/) — install Git, GitHub, Python, and a coding agent before the rest of the course.
2. [Specs-Driven Development](lectures/02-specs-driven-development/) — the agentic SDLC, when SDD fits, Plan Mode, SDD maturity levels, good specs, and SDD frameworks.
3. [Anatomy of Coding Agents](lectures/03-anatomy-of-coding-agents/) — how LLMs work, the model landscape, why LLMs are good at coding, and coding agents under the hood.
4. [Advanced Context Management](lectures/04-advanced-context-management/) — a taxonomy of context, context assembly and discovery, the agent runtime pipeline, session management, and MCP fundamentals.
5. [Agentic Codebase Structure](lectures/05-agentic-codebase-structure/) — skills, rules, and guardrails; CLAUDE.md / AGENTS.md / SKILL.md / intent.md; hooks; and subagent patterns.
6. [Agentic Code Review and Testing](lectures/06-agentic-code-review-and-testing/) — deterministic guardrails, LLM-based review, safe deployment, runtime safety, and monitoring agents.
7. [Agent Orchestration](lectures/07-agent-orchestration/) — the generator-critic loop, the goal pattern, the Ralph loop, running multiple agents, and the subagent pattern.
8. [Security in the Age of AI](lectures/08-security-in-the-age-of-ai/) — SAST/SCA and secret leaks, prompt injection and agent attack surfaces, and agent-assisted triage.
9. [Software Factory and the Future of Software Engineering](lectures/09-software-factory-and-the-future/) — self-running, self-improving systems and where AI software engineering goes next.
10. [AI-Native Engineering Teams](lectures/10-ai-native-engineering-teams/) — how AI-native teams work, the standardized team stack, and LLM gateways, model routing, and cost optimization.

## Repository Structure

```
.
├── lectures/       # Lecture notes and slides, one folder per session
├── assignments/    # Homework and project briefs, one folder per lecture
├── resources/      # Papers, links, and supplementary reading, one folder per lecture
└── README.md
```

## Getting Started

Browse the `lectures/` folder for session-by-session material. Each lecture folder contains a short README describing that session's goals and contents.

## License

Course materials are shared for educational use. See [LICENSE](LICENSE) if present, or contact the instructor for reuse terms.

---

_AI-Augmented Software Engineering_
