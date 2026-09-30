# Papers to Read — The AI-Native Software Engineer

These readings frame the first lecture's central question: **what changes when AI becomes part of a software engineer's everyday workflow?** The Copilot study is a controlled experiment on developer speed. The SE 3.0 paper is a forward-looking companion for students who want to explore the "AI-native" idea in more depth.

## The Impact of AI on Developer Productivity: Evidence from GitHub Copilot

- **Authors:** Sida Peng, Eirini Kalliamvakou, Peter Cihon, and Mert Demirer (2023)
- **Paper:** [arXiv:2302.06590](https://arxiv.org/abs/2302.06590) · [PDF](https://arxiv.org/pdf/2302.06590)
- **Why this paper:** It reports a controlled experiment in which developers implemented a JavaScript HTTP server, comparing participants with and without GitHub Copilot. It gives us a concrete starting point for discussing claims about AI-assisted developer productivity.

### How to read it

Plan for **45–60 minutes**. Do not read it as a source of a single headline number.

1. **Start with the abstract and introduction.** Write down the research question in your own words. What does the paper mean by *productivity*?
2. **Study the experiment before the results.** Identify the participants, the task, the treatment, the comparison group, and the outcome measure. Ask: *what exactly was tested?*
3. **Read the results with the method in mind.** The reported result is that the Copilot group completed this task 55.8% faster. Record the result precisely, including the task and population; do not generalize it to all programming work.
4. **Read the limitations and discussion critically.** List at least two reasons why the result may not transfer directly to a team, codebase, programming language, or long-running project you know.
5. **Finish with a short evidence note (150–200 words).** State the claim, the evidence, one limitation, and one question the study leaves open.

### What to take away

- AI assistance can improve speed on a well-defined programming task, but the study does **not** prove a universal productivity gain for every developer or every type of software work.
- “Developer productivity” is a measurement choice. Completion time is useful, yet it omits dimensions such as code quality, maintainability, review effort, collaboration, learning, security, and user value.
- An AI-native engineer needs evidence literacy: distinguish a result from the conditions under which that result was obtained, and ask what would need to be measured in a real engineering setting.

### Bring to class

Come prepared to answer:

> If you repeated this study for a real repository over four weeks, what would you measure in addition to task-completion time, and why?

---

## Towards AI-Native Software Engineering (SE 3.0): A Vision and a Challenge Roadmap

- **Authors:** Ahmed E. Hassan et al. (2024)
- **Paper:** [arXiv:2410.06107](https://arxiv.org/abs/2410.06107) · [PDF](https://arxiv.org/pdf/2410.06107)
- **Why read it:** This vision paper proposes *Software Engineering 3.0*—intent-centric, conversation-oriented development in which AI moves from a task-level copilot toward a teammate. It is useful for challenging and extending the empirical perspective of the Copilot study.

### How to read it

Read the **abstract, introduction, proposed SE 3.0 vision/stack, and challenge roadmap** first (about 30–45 minutes). Create a two-column note:

| Vision claim | Evidence or assumption needed to support it |
| --- | --- |
| AI as a teammate rather than a tool | What capabilities, reliability, governance, and human oversight would be required? |

Add at least three claims from the paper. Mark each as one of: **current capability**, **plausible near-term direction**, or **open research challenge**.

### What to take away

- “AI-native” is not merely using a code-completion tool; it is a proposed redesign of how people express intent, collaborate, and validate software.
- Vision papers offer valuable language and possible futures, but they are not causal evidence. Evaluate their assumptions against empirical studies such as the Copilot experiment.
- The engineering role shifts toward specifying intent, supplying context, evaluating outputs, managing risk, and retaining accountability for outcomes.

---

## Reading principle for this course

Treat papers as arguments supported by particular forms of evidence—not as facts to memorize. For every reading, be able to say:

1. **What is the claim?**
2. **What evidence supports it?**
3. **Where does that evidence apply—and where might it not?**
4. **What would change your mind?**
