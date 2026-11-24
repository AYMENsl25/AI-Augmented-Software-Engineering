# Self-check questions

Answer these without looking. Each is in the style of the exam. Answers are at the bottom.

1. A developer pastes an error message back into the chat, accepts whatever comes out, and ships it because "it seems to work." Which point on the spectrum is this, and what single factor places it there?
2. The Copilot study reported a 55.8% speed-up. What does that number *not* tell you, according to the reading notes?
3. In the Anthropic skill-formation study, which difference between groups was statistically significant: coding speed or quiz score?
4. Which artifact does an agent consume, and which is "too vague to build from": a user story, a requirements list, or a spec?
5. Name the four headings every spec should start from.
6. A team keeps its spec in the repo and updates it in the same PR as the code, spec first. Which SDD maturity level is this?
7. Which of these is a reason to make the agent *stop and ask*: (a) a test has failed once, (b) two valid designs exist and it cannot pick, (c) a linter warning appeared.
8. Why is Plan Mode "a bridge, not SDD"? Give two reasons from the slides.
9. What is the difference between in-weights and in-context knowledge, and which one is fixed at the training cutoff?
10. Why does the cost of a long agent session grow with every turn?
11. Which harness component clips, dedupes and compresses tool output?
12. What does RLHF teach a model, and what does it *not* guarantee?
13. Which type of model should you use to reformat JSON, and which for a race condition — and what is the cost of the second type?
14. If each of 10 rules is followed 95% of the time, roughly what is the chance all 10 are followed?
15. Where in a long prompt does a model attend *least* well, according to Liu et al.?
16. Rank the three steps of progressive disclosure for a skill, from what loads at startup to what loads last.
17. An agent ignored a constraint that was definitely in its rules file. Give three things to check, in order.
18. In MCP, which component contains the LLM, which routes requests, and which performs the action?
19. Which MCP transport is used for a local process, and what message format does MCP use?
20. A rule says "Never run `git push`." The agent ran it anyway. Which mechanism would have *prevented* it, and why?
21. What is the key difference between a rule and a skill in terms of *when they load*?
22. What did SWE-agent change to improve issue resolution — the model or the interface?
23. What was the headline finding of *Evaluating AGENTS.md* on task success and cost?
24. According to *Guardrails Beat Guidance*, which polarity of rule tends to help and which tends to hurt?
25. A subagent is configured with `is_background: true` and `readonly: true`. What do those two fields control?

## Answers

1. Vibe coding; outputs are verified only by "does it seem to work?" — verification is the differentiator.
2. Nothing about quality, maintainability, review effort, collaboration, learning or user value; and it does not generalise beyond that task and population.
3. The quiz score (17 points lower with AI, p = 0.010). The ~2-minute speed difference was not significant.
4. Agents consume specs; the user story is too vague to build from; requirements are partially usable.
5. Goal, Constraints, Acceptance criteria, Out of scope.
6. Level 2, spec-anchored.
7. (b) ambiguity. Divergence is a test still failing after three tries, not one.
8. It is transient (lives in one chat, a teammate cannot pick it up) and it answers *how*, not *what* — it takes your description at face value and will not surface missing requirements.
9. In-weights (parametric) knowledge is learned during training and fixed at the cutoff; in-context knowledge is supplied with the request and is current but not retained.
10. The API is stateless: the full message history is resent on every call, so each turn re-sends everything before it.
11. Context reduction.
12. What people prefer; it does not guarantee correctness.
13. A standard model for JSON reformatting; a reasoning model for the race condition — slower and more expensive because hidden thinking tokens are billed.
14. About 60% (0.95^10).
15. The middle; accuracy is highest at the start and end.
16. Name + description at startup → full `SKILL.md` when the task matches → scripts, references and assets only when a step needs them.
17. Was it loaded? Where did it sit (middle vs start/end)? Did it stand out? (Then: was it contradicted? Was it summarised away?)
18. Host contains the LLM; client routes; server acts.
19. stdio; JSON-RPC 2.0.
20. A hook (e.g. a shell-permission hook) — it is event-triggered execution that rejects the command, whereas a rule is only an instruction the model reads.
21. Rules load always / by file glob / by relevance / by `@mention`; skills load when selected by description or invoked with `/skill-name`.
22. The interface (ACI) — the model was held constant.
23. Context files generally did not improve task success and raised inference cost by more than 20% on average.
24. Negative constraints help; positive directives tend to hurt.
25. `is_background` sets whether the parent waits for the result; `readonly` restricts the subagent from making changes.

---

[Back to the study guide index](README.md)
