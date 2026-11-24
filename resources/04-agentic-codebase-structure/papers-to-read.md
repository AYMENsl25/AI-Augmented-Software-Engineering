# Papers to Read — Agentic Codebase Structure

This week's lecture argues that a repository can be *designed for agents*: context files such as `AGENTS.md`, rules, skills, hooks, and subagent roles all shape what an agent does before it writes a line of code. The readings test that argument from two directions. The first mandatory paper shows that the interface between an agent and its environment changes outcomes as much as the model does. The second is a controlled study asking whether context files actually help, and its answer is less flattering than the folklore. The reference papers map what developers really put in these files and which kinds of instruction the evidence supports.

## Mandatory

### SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering

- **Authors:** John Yang et al. (2024)
- **Paper:** [arXiv:2405.15793](https://arxiv.org/abs/2405.15793) · [PDF](https://arxiv.org/pdf/2405.15793)
- **Why this paper:** It introduces the idea of an *agent-computer interface* (ACI): the set of commands, feedback formats, and guardrails through which a language model acts on a repository. The authors show that redesigning this interface, without changing the model, materially changes how often the agent resolves real GitHub issues. Everything you build this week (rules, hooks, workflows, subagent roles) is an ACI decision.

### How to read it

Plan for **60 minutes**.

1. **Read the ACI section first.** List the design principles the authors state (for example: simple commands, concise feedback, guardrails against common mistakes). For each, write down which human-oriented tool it replaces and why the human version was a poor fit for a model.
2. **Study one concrete interface choice in depth.** The file viewer shows a limited window of lines; the edit command runs a linter and rejects syntactically broken edits. Explain what model failure each choice prevents.
3. **Read the ablations.** Which interface changes mattered most? Which did nothing? Note that the model is held constant, so the effect is attributable to the interface.
4. **Translate to your repository.** For the link shortener in this week's assignment, write three ACI-style rules you would put in `AGENTS.md` and one guardrail you would enforce with a hook rather than with text.
5. **Finish with a short evidence note (150–200 words).** State the claim, the evidence, one limitation (benchmark, model, and date), and one design decision for your own repo.

### What to take away

- An agent's behavior is a product of model *and* interface. You control the interface.
- Guardrails that run as code (a linter in the edit path, a test gate in a hook) are more reliable than guardrails stated as prose, because the model cannot skip them.
- Concise, structured feedback beats raw tool output. Design what the agent sees after each action, not only what it can do.

### Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?

- **Authors:** Thibaud Gloaguen et al. (2026)
- **Paper:** [arXiv:2602.11988](https://arxiv.org/abs/2602.11988) · [PDF](https://arxiv.org/pdf/2602.11988)
- **Why this paper:** It runs a controlled comparison of coding agents with no context file, with an LLM-generated context file, and with the developer-written one. The headline result is uncomfortable: context files generally did not improve task success, and they raised inference cost by more than 20% on average. Read it before you write an `AGENTS.md`, so that you write one that earns its tokens.

> **Evidence note:** This is one study on particular agents, benchmarks, and context files. It does not show that context files never help. It shows that *a context file is not automatically useful* and that its cost is real.

### How to read it

Plan for **45 minutes**.

1. **Identify the three conditions and the metrics.** What counts as success, and how is cost measured?
2. **Look for heterogeneity.** Do any kinds of instruction help? Does the size or specificity of the file matter? Record where the paper's data supports a positive claim and where it does not.
3. **Compare with the descriptive study.** *Agent READMEs* (below) reports what developers actually write: mostly test procedures and implementation details, rarely security or performance. Does this paper's result suggest those common contents are the wrong contents?
4. **Compare with the rules study.** *Guardrails Beat Guidance* (below) finds negative constraints help and positive directives hurt. Draft two sentences for your `AGENTS.md` that follow this pattern, and two that violate it.
5. **Finish with a design note (150–200 words).** What will your `AGENTS.md` contain, what will it deliberately leave out, and how would you measure whether it helped?

### What to take away

- A context file is context. It competes for the same attention budget as code and tool output (Week 4), so every line should change a decision the agent would otherwise get wrong.
- Constraints ("never edit `main` directly," "run `pytest` before you report done") have better evidence behind them than general guidance ("write clean code").
- Prefer enforcing a rule with a hook or a test over stating it in prose. Keep prose for what code cannot check: intent, scope, and where things live.

### Bring to class

Come prepared to answer:

> You have one hour to make a repository "agent-ready." Given this week's evidence, in what order would you spend it across `AGENTS.md`, a hook, a reusable workflow, and subagent roles, and how would you know afterwards that it worked?

---

## Practitioner companions

These explain the mechanisms (skills, tools, context files) as the people building them describe them. They are not evidence; they are vocabulary and design rationale.

1. **[agents.md](https://agents.md/)** — the cross-tool `AGENTS.md` convention referenced in the assignment. Read the format and the examples.
2. **[Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)** — Anthropic Engineering (October 16, 2025). Introduces `SKILL.md` and *progressive disclosure*: metadata loads at startup, the full skill loads when relevant, bundled files load only when needed.
3. **[Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** — Anthropic Engineering. Argues that tools should be designed for models, not copied from developer APIs: fewer, well-scoped tools with descriptions that prevent specific mistakes. Pairs with the SWE-agent ACI principles.

---

## Reference

### Agent READMEs: An Empirical Study of Context Files for Agentic Coding

- **Authors:** Worawalan Chatlatanagulchai et al. (2025)
- **Source:** [arXiv:2511.12884](https://arxiv.org/abs/2511.12884) · [PDF](https://arxiv.org/pdf/2511.12884)
- **Importance:** Analyzes thousands of real context files. Developers mostly specify functional context (test procedures, implementation details) and rarely non-functional requirements such as security or performance. Useful for seeing what the field does today and what it leaves out.

### Guardrails Beat Guidance: A Large-Scale Study of Rules, Skills, and Persistent Configuration for Coding Agents

- **Authors:** Xing Zhang et al. (2026)
- **Source:** [arXiv:2604.11088](https://arxiv.org/abs/2604.11088) · [PDF](https://arxiv.org/pdf/2604.11088)
- **Importance:** Finds that the *polarity* of a rule predicts its usefulness: negative constraints help, positive directives tend to hurt, largely independent of topic. The clearest empirical guidance available on how to phrase rules.

### On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents

- **Authors:** Jai Lal Lulla et al. (2026)
- **Source:** [arXiv:2601.20404](https://arxiv.org/abs/2601.20404) · [PDF](https://arxiv.org/pdf/2601.20404)
- **Importance:** Looks at efficiency rather than success: on real pull requests, repositories with an `AGENTS.md` showed lower median runtime and fewer output tokens with comparable completion. Read alongside *Evaluating AGENTS.md*; the two measure different things and partly disagree.

### Beyond the Prompt: An Empirical Study of Cursor Rules

- **Authors:** Shaokang Jiang and Daye Nam (2025)
- **Source:** [arXiv:2512.18925](https://arxiv.org/abs/2512.18925) · [PDF](https://arxiv.org/pdf/2512.18925)
- **Importance:** A taxonomy of developer-written rules from 401 repositories: conventions, guidelines, project information, LLM directives, and examples. A good checklist when deciding what belongs in a rules file.

### Agentless: Demystifying LLM-based Software Engineering Agents

- **Authors:** Chunqiu Steven Xia et al. (2024)
- **Source:** [arXiv:2407.01489](https://arxiv.org/abs/2407.01489) · [PDF](https://arxiv.org/pdf/2407.01489)
- **Importance:** The counterpoint to SWE-agent: a fixed three-phase pipeline (localize, repair, validate) with no autonomous tool use that was competitive on the same benchmark. Structure imposed by the harness can substitute for structure the agent discovers itself.

### NeMo Guardrails: A Toolkit for Controllable and Safe LLM Applications with Programmable Rails

- **Authors:** Traian Rebedea et al. (2023)
- **Source:** [arXiv:2310.10501](https://arxiv.org/abs/2310.10501) · [PDF](https://arxiv.org/pdf/2310.10501)
- **Importance:** An early, explicit treatment of guardrails as programmable, deterministic rails around a model rather than as prompt text. The same idea underlies this week's hook.

---

## Reading principle for this course

Treat every instruction you give an agent as a **hypothesis about its failure modes**. For each line in a context file, rule, or hook, be able to say:

1. **What mistake does this prevent?**
2. **Is it enforced by code or only stated in prose?**
3. **What does it cost in tokens and attention on every run?**
4. **What evidence would show it helped?**
