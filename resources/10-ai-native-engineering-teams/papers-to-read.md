# Papers to Read — AI-Native Engineering Teams

The final week zooms out from the individual engineer to the team and its infrastructure: how AI-native teams work, what a standardized team stack looks like, and how model calls are routed and paid for. The readings return to the question the course opened with in Week 1, now with better evidence. The first mandatory paper is the foundational treatment of model routing and cost, which is what you implement in the assignment. The second is a randomized controlled trial of experienced developers using early-2025 AI tools on their own repositories, and its result contradicts the Week 1 Copilot study. The reference list adds the largest field experiments to date, the industry survey most teams cite, and the routing literature that followed the first paper.

## Mandatory

### FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

- **Authors:** Lingjiao Chen, Matei Zaharia, and James Zou (2023)
- **Paper:** [arXiv:2305.05176](https://arxiv.org/abs/2305.05176) · [PDF](https://arxiv.org/pdf/2305.05176)
- **Why this paper:** It frames model selection as an engineering problem with a budget. The authors describe three families of technique (prompt adaptation, model approximation such as caching, and LLM cascades that try a cheap model first and escalate on low confidence) and show large cost reductions at matched quality. Your gateway with an easy model, a hard model, and a fallback is a two-stage cascade. Read this to understand what you are building and how to evaluate it honestly.

### How to read it

Plan for **45–60 minutes**.

1. **Learn the three strategy families.** For each, write one sentence on what it saves, what it risks, and which part of your `gateway_app.py` corresponds to it (or could).
2. **Study the cascade.** What decides whether to escalate to the next model? Why is a *scorer* needed, and what happens to the cost argument if the scorer itself is expensive or wrong?
3. **Read the cost–quality plots.** What is held constant when the authors report a cost reduction? What quality metric is used, and would it be the right one for your sentiment and bug-explanation tasks?
4. **Find the hidden costs.** Latency of a two-stage call, the cost of the failed first attempt, the maintenance of per-task thresholds. Which of these did the paper account for?
5. **Finish with a short evidence note (150–200 words).** The claim, the evidence, one limitation (the models and prices are from 2023), and the routing policy you will test, stated as a falsifiable prediction about cost and quality.

### What to take away

- Routing is a measurable trade-off, not a configuration detail. The right policy depends on the task's error tolerance and on an honest quality metric.
- Caching, cascades, and prompt trimming are the same idea at different layers: spend expensive tokens only where they change the answer.
- A fallback is a cascade in reverse (escalate on failure rather than on low confidence). Both need loop guards and both need measurement.

### Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity

- **Authors:** Joel Becker et al. (METR, 2025)
- **Paper:** [arXiv:2507.09089](https://arxiv.org/abs/2507.09089) · [PDF](https://arxiv.org/pdf/2507.09089)
- **Why this paper:** A randomized controlled trial in which experienced maintainers worked on real issues in their own large repositories, with or without AI tools. Developers using AI took *longer* on average, while predicting and later believing that they had been faster. Set against the Week 1 Copilot experiment, this is the clearest demonstration in the course that the answer to "does AI make developers faster?" depends on who, on what, and measured how.

> **Evidence note:** This is a well-designed study with a specific population (expert maintainers on familiar, mature codebases) and a specific moment (early 2025 tools). It does not show that AI slows all developers. It shows that self-reported speed is unreliable and that context matters.

### How to read it

Plan for **60 minutes**.

1. **Lay out the design.** Participants, repositories, task assignment, randomization unit, outcome measure, and how AI use was allowed or forbidden.
2. **Record the result with its uncertainty.** Note the point estimate and the interval, and the gap between measured time and the developers' own estimates.
3. **Read the mechanisms section.** The authors list factors that plausibly explain the slowdown (familiarity with the codebase, tool reliability, time spent reviewing output). Which of these are properties of the tools, and which are properties of the setting?
4. **Reconcile with Week 1 and with Cui et al.** The Copilot experiment found a large speedup on a greenfield task; the three field experiments (below) found more completed tasks across thousands of developers. Build a table: study, population, task type, outcome measure, result. What pattern explains all of them?
5. **Finish with a short evidence note (150–200 words).** What this study licenses you to say about AI on your own team, and the one measurement you would set up before deciding team-wide policy.

### What to take away

- Perceived productivity and measured productivity can diverge in opposite directions. A team that relies on how fast it *feels* will mislead itself.
- Effects depend on the setting: expertise, codebase maturity, task type, and tool reliability. A policy that is right for onboarding juniors on a new service may be wrong for senior maintainers of a legacy core.
- An AI-native team instruments its own work. Cost per request from the gateway and cycle time from the tracker are both infrastructure.

### Bring to class

Come prepared to answer:

> Your team lead asks for one slide: "Should we standardize on AI tooling and route everything through a gateway?" Using the Week 1 Copilot study, the three field experiments, the METR trial, and your Week 10 measurements, write the three sentences you would put on that slide, including what you would measure for the next quarter.

---

## Reference

### The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers

- **Authors:** Zheyuan (Kevin) Cui, Mert Demirer, Sonia Jaffe, Leon Musolff, Sida Peng, and Tobias Salz (2024; *Management Science*, 2025)
- **Source:** [SSRN 4945566](https://papers.ssrn.com/abstract=4945566) · [Management Science](https://pubsonline.informs.org/doi/10.1287/mnsc.2025.00535)
- **Importance:** Randomized rollouts of an AI coding assistant at Microsoft, Accenture, and a Fortune 100 firm covering thousands of developers, with a pooled estimate of roughly a quarter more completed tasks and larger gains for less experienced developers. The largest field evidence available and the natural counterpart to the METR trial.

### DORA 2025: State of AI-assisted Software Development

- **Publisher:** Google Cloud DORA (September 2025)
- **Source:** [DORA report page](https://cloud.google.com/devops/state-of-devops) · [Google Research listing](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/)
- **Importance:** A survey of several thousand practitioners that frames AI as an amplifier of existing team strengths and dysfunctions, and introduces a capabilities model for AI adoption. Survey evidence with self-selection; useful for the vocabulary teams use and for the practices it associates with good outcomes.

### RouteLLM: Learning to Route LLMs with Preference Data

- **Authors:** Isaac Ong et al. (2024)
- **Source:** [arXiv:2406.18665](https://arxiv.org/abs/2406.18665) · [PDF](https://arxiv.org/pdf/2406.18665)
- **Importance:** Trains a router to send each query to a strong or weak model using human preference data, reporting large cost savings at small quality loss. The learned-router successor to FrugalGPT's cascades, and an open-source reference implementation.

### Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing

- **Authors:** Dujian Ding et al. (2024)
- **Source:** [arXiv:2404.14618](https://arxiv.org/abs/2404.14618) · [PDF](https://arxiv.org/pdf/2404.14618)
- **Importance:** Routes by predicted query difficulty with an explicit quality tolerance, which is exactly the policy decision the assignment asks you to make. Read for how to define "acceptable quality" before measuring cost.

### The Impact of Generative AI on Collaborative Open-Source Software Development: Evidence from GitHub Copilot

- **Authors:** Fangchen Song, Ashish Agarwal, and Wen Wen (2024)
- **Source:** [arXiv:2410.02091](https://arxiv.org/abs/2410.02091) · [PDF](https://arxiv.org/pdf/2410.02091)
- **Importance:** Looks beyond individual speed to project-level effects on open-source collaboration: contribution volume, coordination, and the shift from coding to project management work. Team-level evidence for a team-level week.

### The SPACE of Developer Productivity

- **Authors:** Nicole Forsgren, Margaret-Anne Storey, Chandra Maddila, Thomas Zimmermann, Brian Houck, and Jenna Butler (ACM Queue, 2021)
- **Source:** [ACM Queue article](https://queue.acm.org/detail.cfm?id=3454124) · [DOI 10.1145/3454122.3454124](https://doi.org/10.1145/3454122.3454124)
- **Importance:** Argues that productivity has five dimensions (satisfaction, performance, activity, communication, efficiency) and that no single metric captures it. The framework to use when the Week 1, Cui et al., and METR studies disagree: they measure different dimensions.

---

## Reading principle for this course

Treat every claim about team productivity or model cost as a **measurement with a population, a task, and a metric attached**. For each study, dashboard, or vendor number, be able to say:

1. **Who was measured, doing what, under which tools?**
2. **What was the outcome metric, and which dimensions of productivity does it miss?**
3. **What did it cost, in money and in attention, to get the result?**
4. **What would you measure on your own team before changing policy?**
