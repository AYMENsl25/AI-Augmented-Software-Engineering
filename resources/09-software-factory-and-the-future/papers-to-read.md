# Papers to Read — Software Factory and the Future of Software Engineering

This week asks where the discipline is going when generating a working application takes minutes and agents can run, evaluate, and revise their own work. The readings are deliberately a mix of vision, measurement, and caution. The first mandatory paper is a research roadmap for *agentic software engineering* from the same group whose SE 3.0 vision you read in Week 1; read it as the sequel. The second is a measurement of how the length of task that AI systems can complete has been growing, which is the main quantitative argument behind "software factory" claims and which deserves a careful reading of what exactly was measured. The reference papers show self-improving systems that already exist, the evaluation problems that make their results hard to interpret, and a forty-year-old warning about what automation does to the humans left supervising it.

## Mandatory

### Agentic Software Engineering: Foundational Pillars and a Research Roadmap

- **Authors:** Ahmed E. Hassan et al. (2025)
- **Paper:** [arXiv:2509.06216](https://arxiv.org/abs/2509.06216) · [PDF](https://arxiv.org/pdf/2509.06216)
- **Why this paper:** In Week 1 you read the SE 3.0 vision. This paper is the follow-up: it proposes the structures (environments, roles, artifacts, governance) needed for humans and agents to engineer software together, and lists open research problems. Read it as a map of the next five years from people who work on the problem, and as a test of the Week 1 vision against what has happened since.

### How to read it

Plan for **60 minutes**.

1. **Recover the Week 1 claims.** Before reading, write down two claims from the SE 3.0 paper. After reading, note whether this roadmap keeps, revises, or quietly drops each one.
2. **Learn the pillars.** The paper organizes agentic SE around a few foundational structures. Name each in one sentence and say which existing artifact or practice it extends (for example: a spec, a CI pipeline, a code review).
3. **Separate the three tenses.** For each pillar, mark what is *current practice*, what is a *near-term engineering problem*, and what is an *open research question*. Vision papers blur these; your job is to un-blur them.
4. **Find the human.** Where does the paper place human judgment, accountability, and sign-off? Compare with what the Week 2 and Week 6 readings said about specifications and review.
5. **Finish with a short evidence note (150–200 words).** One claim you find well supported, one you find speculative, and one research question you would want answered before adopting the proposed structure on a real team.

### What to take away

- "Software factory" is a proposal about organization, not only about model capability: who specifies, who verifies, who is accountable, and how the artifacts between them are structured.
- Roadmaps are hypotheses. The useful move is to identify which parts you could test on your own project this semester.
- The engineering role in these proposals shifts toward intent, context, verification, and governance, consistent with Weeks 1, 2, and 6.

### Measuring AI Ability to Complete Long Software Tasks

- **Authors:** Thomas Kwa et al. (METR, 2025)
- **Paper:** [arXiv:2503.14499](https://arxiv.org/abs/2503.14499) · [PDF](https://arxiv.org/pdf/2503.14499)
- **Why this paper:** It introduces the *50% task-completion time horizon*: the length of task, measured in how long it takes skilled humans, that a model completes with 50% success. The authors estimate this horizon has been doubling on a timescale of months. This is the most-cited quantitative basis for claims that agents will soon run long software projects autonomously. It is also a paper where the measurement details matter enormously.

> **Evidence note:** The trend is real on the tasks measured. Whether it extrapolates depends on how representative those tasks are of real engineering work, which the authors discuss. Read the limitations with the same care as the headline.

### How to read it

Plan for **45–60 minutes**.

1. **Define the metric precisely.** What is being measured, how is "human time" established, and why 50% rather than 90% or 99%?
2. **Study the task suite.** What kinds of tasks are included, how were they chosen, and how do they differ from a week of work on a real codebase (ambiguity, coordination, legacy context, changing requirements)?
3. **Read the trend plot critically.** How many models, over what period? What would the plot look like if the task mix changed? Which assumptions does extrapolation require?
4. **Connect the horizon to reliability.** A 50% success rate on an eight-hour task is not an eight-hour autonomous agent. What success rate would you require before leaving an agent unsupervised for that long, and what does the paper say about longer horizons at higher reliability?
5. **Finish with a short evidence note (150–200 words).** The claim, the evidence, two limitations, and what you would measure on your own Week 9 generated app to estimate how long you can leave an agent alone with it.

### What to take away

- Capability trends are measurable and the measured trend is steep. That is a fact about benchmarks that should update your expectations.
- The gap between a benchmark horizon and an unsupervised production deployment is reliability, ambiguity, and accountability, none of which the horizon metric captures.
- Evidence literacy from Week 1 applies: separate the result from the conditions under which it was obtained before using it to plan.

### Bring to class

Come prepared to answer:

> Your Week 9 app was generated in minutes and you found two real defects in it. If the same system were asked to improve itself with minimal human input, which of this week's readings predicts what would break first, which guardrail from Weeks 5 to 8 would you add, and what would you measure to know whether the self-improvement was real?

---

## Reference

### AlphaEvolve: A coding agent for scientific and algorithmic discovery

- **Authors:** Alexander Novikov et al. (Google DeepMind, 2025)
- **Source:** [arXiv:2506.13131](https://arxiv.org/abs/2506.13131) · [PDF](https://arxiv.org/pdf/2506.13131)
- **Importance:** An evolutionary loop in which a model proposes code changes and an automated evaluator scores them, producing new results in mathematics and improvements to production systems. A working self-improving pipeline, and a clear illustration that it works where a *reliable automatic evaluator* exists.

### Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents

- **Authors:** Jenny Zhang et al. (2025)
- **Source:** [arXiv:2505.22954](https://arxiv.org/abs/2505.22954) · [PDF](https://arxiv.org/pdf/2505.22954)
- **Importance:** A coding agent that edits its own code and keeps the variants that score better on coding benchmarks. Read for the mechanism, for the large reported gains, and for the safety section, which documents the agent gaming its own evaluation.

### The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery

- **Authors:** Chris Lu et al. (2024)
- **Source:** [arXiv:2408.06292](https://arxiv.org/abs/2408.06292) · [PDF](https://arxiv.org/pdf/2408.06292)
- **Importance:** An end-to-end pipeline from idea to experiment to paper to automated review. Useful as an existence proof of a full "factory" loop, and for its frank catalogue of failure modes, including the system editing its own execution limits.

### Voyager: An Open-Ended Embodied Agent with Large Language Models

- **Authors:** Guanzhi Wang et al. (2023)
- **Source:** [arXiv:2305.16291](https://arxiv.org/abs/2305.16291) · [PDF](https://arxiv.org/pdf/2305.16291)
- **Importance:** An agent that writes code for new skills, verifies them in the environment, and stores them in a growing library. The skill-library idea anticipates Week 5's skills and shows self-improvement as accumulation of verified, reusable code.

### AI Agents That Matter

- **Authors:** Sayash Kapoor et al. (2024)
- **Source:** [arXiv:2407.01502](https://arxiv.org/abs/2407.01502) · [PDF](https://arxiv.org/pdf/2407.01502)
- **Importance:** Argues that agent benchmarks ignore cost, overfit, and lack reproducibility, so reported gains often do not translate to practice. Read it before interpreting any of the results above or any vendor's agent demo.

### Ironies of Automation

- **Author:** Lisanne Bainbridge (1983)
- **Source:** *Automatica*, 19(6), 775–779 · [DOI 10.1016/0005-1098(83)90046-8](https://doi.org/10.1016/0005-1098%2883%2990046-8) · [annotated copy at Fermat's Library](https://fermatslibrary.com/p/028c7a80)
- **Importance:** The classic argument that automating the routine parts of a job leaves humans with the hardest parts, while eroding the skills and attention needed to do them. Written about industrial control rooms, it reads as a description of an engineer supervising a software factory. The strongest single counterweight to this week's optimism.

---

## Reading principle for this course

Treat every claim about autonomous or self-improving software as a claim about an **evaluator**. For each system, be able to say:

1. **What signal tells it that a change was an improvement?**
2. **How could that signal be gamed, and who would notice?**
3. **What is the human's job once the routine work is automated, and are they equipped to do it?**
4. **What would you measure before trusting it with less supervision?**
