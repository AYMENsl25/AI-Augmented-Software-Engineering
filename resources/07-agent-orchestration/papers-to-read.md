# Papers to Read — Agent Orchestration

This week's lecture moves from one agent to several: the generator–critic loop, the goal pattern, the Ralph loop, concurrent agents, and subagents. The readings are chosen so that each pattern arrives with its evidence and its failure mode. The first mandatory paper is the cleanest statement of iterative self-feedback, which is what a generator–critic loop automates. The second is a taxonomy of how multi-agent systems actually fail, drawn from traces of real frameworks. The practitioner pieces describe the orchestration patterns in production, including the one-line loop that gave the Ralph pattern its name. The reference papers include the strongest counter-evidence to self-correction, which you should read before you trust a critic that shares a model with its generator.

## Mandatory

### Self-Refine: Iterative Refinement with Self-Feedback

- **Authors:** Aman Madaan et al. (2023)
- **Paper:** [arXiv:2303.17651](https://arxiv.org/abs/2303.17651) · [PDF](https://arxiv.org/pdf/2303.17651)
- **Why this paper:** It formalizes the loop you will run in Part II of the assignment: generate, obtain feedback, revise, repeat. The same model plays generator and critic, no training is involved, and the authors measure improvement across several tasks including code. Read it to see exactly what the loop buys, on which tasks, and where it stalls.

### How to read it

Plan for **45 minutes**.

1. **Write the loop down.** Generator output → feedback prompt → refined output → stopping rule. Identify the stopping rule the paper uses and how many iterations it typically runs.
2. **Separate the tasks.** On which tasks did refinement help most, and which least? Form a hypothesis about what the helpful tasks have in common (for example: feedback that is specific and checkable).
3. **Inspect the feedback.** Look at the example feedback the paper shows. Is it actionable, or generic? Would a human reviewer have written it?
4. **Read it against the counter-evidence.** *Large Language Models Cannot Self-Correct Reasoning Yet* (below) argues that without external signal, self-correction can make answers worse. Decide which of Self-Refine's gains rely on the task having an external check (tests, a rubric) and which do not.
5. **Finish with a short evidence note (150–200 words).** State the claim, the evidence, one limitation, and the rubric you will give your critic agent so that its feedback is specific enough to act on.

### What to take away

- A generator–critic loop is only as good as the critic's signal. Specific, checkable feedback (a failing test, a rubric item) produces improvement; vague feedback produces churn.
- The stopping rule is part of the design. "Loop until the critic signs off" needs a critic that can say no and a cap on rounds.
- When generator and critic share a model, they share its blind spots. Add an external check wherever you can.

### Why Do Multi-Agent LLM Systems Fail?

- **Authors:** Mert Cemri et al. (2025)
- **Paper:** [arXiv:2503.13657](https://arxiv.org/abs/2503.13657) · [PDF](https://arxiv.org/pdf/2503.13657)
- **Why this paper:** The authors analyzed execution traces from several popular multi-agent frameworks and built a taxonomy of failure modes grouped into specification problems, inter-agent misalignment, and task verification. Many failures were organizational rather than model-level: unclear roles, lost context between agents, no one checking the final result. This is the paper to read before you run two agents at once and before you design a planner/implementer/reviewer split.

### How to read it

Plan for **45 minutes**.

1. **Learn the taxonomy.** Write down the three top-level categories and two or three failure modes under each, in your own words.
2. **Match failures to this week's patterns.** For each pattern in the lecture (generator–critic, goal, Ralph, concurrent agents, subagents), name the failure mode from the taxonomy it is most exposed to.
3. **Read the intervention results.** The authors try simple fixes (better role specification, verification steps). How much did they help? What does that say about how much of the problem is prompt design versus something deeper?
4. **Plan your Part I defenses.** For two agents working in parallel worktrees, list the failures you expect (duplicate work, conflicting edits, inconsistent interfaces) and how you will detect each before merging.

### What to take away

- Multi-agent systems fail for the same reasons teams fail: unclear roles, poor handoffs, no verification. The remedies are also familiar.
- Adding agents adds coordination cost and new failure surfaces. Use more than one agent when the task decomposes cleanly and a human or test can verify the result, not because it sounds more capable.
- Verification is a role. If no agent (or human) owns checking the final result, assume it is unchecked.

### Bring to class

Come prepared to answer:

> You ran a generator–critic loop for four rounds and the critic finally approved. The tests pass. Using this week's readings, what evidence would convince you the loop converged on a correct solution rather than on something the critic stopped objecting to, and what would you change in the loop to make that evidence appear automatically?

---

## Practitioner companions

These describe orchestration patterns as the people running them describe them. They are design rationale, not controlled evidence.

1. **[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)** — Anthropic Engineering (December 19, 2024). Names the workflow patterns this week's lecture builds on: prompt chaining, routing, parallelization, orchestrator–workers, and evaluator–optimizer (the generator–critic loop under another name). Its central advice is to start with the simplest pattern that works.
2. **[How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)** — Anthropic Engineering (June 2025). An orchestrator–worker system with parallel subagents and separate context windows, including the costs: far more tokens than a single agent, and a poor fit for tightly coupled work such as most coding. Read it for the honest trade-offs.
3. **[Ralph Wiggum as a "software engineer"](https://ghuntley.com/ralph/)** — Geoffrey Huntley (July 14, 2025). The source of the Ralph loop: a bash `while` loop that re-runs the same prompt against an agent until the work is done, with state kept in files rather than in the model's context. Read it alongside the Self-Refine stopping-rule discussion and ask what makes the loop terminate.

---

## Reference

### Large Language Models Cannot Self-Correct Reasoning Yet

- **Authors:** Jie Huang et al. (2023)
- **Source:** [arXiv:2310.01798](https://arxiv.org/abs/2310.01798) · [PDF](https://arxiv.org/pdf/2310.01798)
- **Importance:** The counterweight to Self-Refine. On reasoning tasks without external feedback, asking a model to review and revise its own answer often made it worse. The lesson for a generator–critic loop: give the critic something external to check against.

### Reflexion: Language Agents with Verbal Reinforcement Learning

- **Authors:** Noah Shinn et al. (2023)
- **Source:** [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) · [PDF](https://arxiv.org/pdf/2303.11366)
- **Importance:** An agent reflects on a failed attempt in natural language, stores the reflection, and tries again. The feedback comes from the environment (for code, from tests), which is why it works where pure self-correction does not. Close to the goal pattern in the lecture.

### ChatDev: Communicative Agents for Software Development

- **Authors:** Chen Qian et al. (2023)
- **Source:** [arXiv:2307.07924](https://arxiv.org/abs/2307.07924) · [PDF](https://arxiv.org/pdf/2307.07924)
- **Importance:** Role-playing agents (CEO, programmer, reviewer, tester) build small applications through structured chat. A readable example of role-based orchestration and of the failure modes the Cemri et al. taxonomy later catalogued.

### MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework

- **Authors:** Sirui Hong et al. (2023)
- **Source:** [arXiv:2308.00352](https://arxiv.org/abs/2308.00352) · [PDF](https://arxiv.org/pdf/2308.00352)
- **Importance:** Encodes standard operating procedures into agent roles and makes agents hand off structured artifacts (specs, designs) rather than free chat. The argument that structured handoffs reduce inter-agent error anticipates the failure taxonomy.

### AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation

- **Authors:** Qingyun Wu et al. (2023)
- **Source:** [arXiv:2308.08155](https://arxiv.org/abs/2308.08155) · [PDF](https://arxiv.org/pdf/2308.08155)
- **Importance:** A general framework for composing conversational agents, including human-in-the-loop agents. Useful for seeing orchestration as a programming model rather than as a fixed pipeline.

---

## Reading principle for this course

Treat every orchestration pattern as a **claim about where errors get caught**. For each loop, role, or parallel split, be able to say:

1. **What does each agent own, and what does it hand off?**
2. **Where does an external signal (test, rubric, human) enter the loop?**
3. **What makes it stop, and what stops it from stopping too early?**
4. **What does the pattern cost in tokens and time compared with one agent?**
