# Papers to Read — Specs-Driven Development

These readings introduce the lecture’s central claim: when an AI coding agent can produce code quickly, the durable engineering work moves toward defining, testing, reviewing, and evolving the **specification**. Complete the required book chapter before the mandatory paper. The optional paper supplies a foundational critique of idealized design processes that remains highly relevant when an agent generates an apparently coherent solution from an incomplete request.

## Required book preparation — complete before the paper

### Chapter 5, “Spec-Driven Development” — *AI-Native Software Engineering*

- **Author:** Alfonso Graziano
- **Publisher:** O’Reilly Media, Inc.
- **Required this week:** Read **Chapter 5: “Spec-Driven Development”** before reading the mandatory paper below.
- **Access:** Register at [O’Reilly Learning](https://learning.oreilly.com/). Registration starts a **10-day free trial** during which the online copy is accessible without charge.

### Reading guidance

Use the trial deliberately: consume as much of *AI-Native Software Engineering* as you reasonably can during the 10-day access window. The book’s ideas will be revisited throughout this course, so early familiarity with its broader argument will make later lectures, exercises, and discussions more useful.

For this week, Chapter 5 is non-negotiable. As you read, note:

1. What makes a specification useful to an AI coding agent rather than merely descriptive to a human reader?
2. Which parts of the specification establish behavior, constraints, verification, and boundaries?
3. Where can a specification still be ambiguous, incomplete, or wrong—and what should the engineer do about it?

---

## Mandatory

### Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants

- **Author:** Deepak Babu Piskala (2026)
- **Paper:** [arXiv:2602.00180](https://arxiv.org/abs/2602.00180) · [PDF](https://arxiv.org/pdf/2602.00180) · [HTML](https://arxiv.org/html/2602.00180v1)
- **Why this paper:** It gives a current practitioner-oriented account of specs-driven development (SDD): specifications become the source of truth, while code is generated or verified against them. It distinguishes **spec-first**, **spec-anchored**, and **spec-as-source** workflows, and connects the idea to AI-assisted tooling such as GitHub Spec Kit.

> **Evidence note:** This is a recent position/practitioner paper submitted to AIWare 2026, not a controlled study demonstrating that SDD improves outcomes. Read it for its concepts, workflow patterns, examples, and decision framework—not as causal proof that every team should adopt SDD.

### How to read it

Plan for **45–60 minutes**. Focus on the abstract, the definition and workflow sections, the three levels of rigor, case studies, and decision framework.

1. **Define the proposed inversion.** In your own words, explain what changes when the specification—not source code—is treated as the primary artifact. What remains the engineer’s responsibility?
2. **Compare the three levels of rigor.** Make a small table for **spec-first**, **spec-anchored**, and **spec-as-source**. For each, record: the source of truth, how code relates to it, a suitable use case, and one risk.
3. **Trace one workflow end to end.** Choose a feature you know. Write its user outcome, acceptance criteria, non-goals, constraints, and at least two failure or edge cases. Identify which of those an AI agent could otherwise invent incorrectly.
4. **Separate artifacts from guarantees.** A specification, plan, task list, generated patch, and passing tests are different artifacts. For each one, ask: *what uncertainty does it reduce, and what uncertainty remains?*
5. **Evaluate the decision framework.** Name one task where SDD’s extra structure is worth its cost and one small exploratory task where it would be overkill. State the trade-off rather than assuming “more specification” is always better.
6. **Finish with a short spec note (150–200 words).** Describe a feature boundary, its observable acceptance criteria, one explicit non-goal, and one ambiguity that needs a product decision before implementation begins.

### What to take away

- Specs-driven development does **not** mean writing a long document and handing it to an agent. It means maintaining inspectable, testable statements of intended behavior through planning, implementation, review, and change.
- A useful specification captures more than the happy path: outcomes, constraints, interfaces, data rules, acceptance criteria, non-goals, and unresolved decisions.
- AI increases the value of clear boundaries. If a requirement is vague, an agent can produce a plausible but incorrect interpretation at high speed.
- SDD has a cost. Match its rigor to the risk, reversibility, domain complexity, team coordination needs, and expected lifetime of the work.

### Bring to class

Come prepared to answer:

> A coding agent has implemented every task in its generated plan and all tests pass. What evidence would convince you that it built the *right* feature rather than merely a consistent interpretation of an incomplete specification?

---

## Optional

### A Rational Design Process: How and Why to Fake It

- **Authors:** David L. Parnas and Paul C. Clements (1986)
- **Paper:** *IEEE Transactions on Software Engineering*, 12(2), 251–257 · [IEEE Xplore](https://ieeexplore.ieee.org/document/6312940) · [PDF mirror](https://www.cs.tufts.edu/~nr/cs257/archive/david-parnas/fake-it.pdf)
- **Why read it:** This classic paper argues that real design is messy, iterative, and shaped by imperfect information, even though a finished system should be documented as a rational design. It provides a sharp counterweight to linear “specify → plan → implement” narratives and helps us reason about how specifications must evolve without becoming post-hoc fiction.

### How to read it

Read it in **30–40 minutes** and keep two questions in view:

1. What is the difference between the **actual** path by which a team discovered a design and the **rational** explanation/documentation of the resulting design?
2. When does revising a specification record legitimate learning, and when does it hide an unexamined decision or erase accountability?

Make a three-column note:

| Situation | What the specification should record | What the team should not pretend |
| --- | --- | --- |
| A user requirement changes after a prototype | The new decision, rationale, scope impact, and updated acceptance criteria | That the original requirement was always clear |

Add two more examples from AI-assisted development, such as an agent discovering an API constraint or a test exposing an unstated business rule.

### What to take away

- Specification-first does not require pretending that requirements arrive complete and stable. Good engineering makes changes, assumptions, alternatives, and resulting decisions visible.
- An AI-generated plan can look rational even when it rests on missing context. Review must challenge the premises, not only the syntax and test results.
- Traceability is useful when it links a decision to evidence and an observable behavior—not when it creates paperwork detached from how the system is actually built.

---

## Reading principle for this course

Treat a specification as a **living contract for shared reasoning**, not as a prompt-shaped artifact or a ceremonial document. For every requirement, plan, implementation, and test, be able to say:

1. **What user or system outcome is intended?**
2. **What behavior would demonstrate that outcome?**
3. **What constraints, non-goals, and edge cases bound the solution?**
4. **What is still unknown, who must decide it, and how will the decision be recorded?**
5. **What evidence would show that the implementation satisfies the specification?**
