# Cross-cutting themes

These ideas appear in more than one week, and the exam likes them.

1. **Verification is the differentiator.** Vibe coding vs engineering (W1), acceptance criteria and done checks (W2), test behaviour not strings (W3), hooks over rules (Codebase Structure).
2. **Guide vs enforce.** Rules, skills, `AGENTS.md`, system prompts and specs *guide* the model. Hooks, linters, tests, locked test files and permission systems *enforce*. The evidence (SWE-agent, Guardrails Beat Guidance, NeMo) favours enforcement and negative constraints for anything that must always hold.
3. **The context window is a finite budget with uneven attention.** Lost in the middle; context rot; the curse of instructions; always-on vs on-demand; progressive disclosure for skills; tool descriptions cost tokens; design tools to return less.
4. **Agents guess fast and silently.** A human writes 50 lines on a bad assumption, an agent writes 500 — and writes tests for its own guess. So: specs, interviews, stop conditions, and reviewing against criteria.
5. **Autonomy scales inversely with risk.** Sandbox → PR → production → incidents; a named human approves production; the agent never approves its own work.
6. **Agent = model + harness.** The same model behaves differently with a different interface, context, tools and loop. Many "model" failures are context or interface failures.
7. **Evidence literacy.** Know which readings are controlled experiments (Copilot study, Lost in the Middle, SWE-agent, Evaluating AGENTS.md, Anthropic skill-formation study) and which are vision or practitioner pieces (SE 3.0, Piskala, Anthropic engineering posts, MCP announcement) — and what each kind can and cannot prove.

---

[Back to the study guide index](README.md)
