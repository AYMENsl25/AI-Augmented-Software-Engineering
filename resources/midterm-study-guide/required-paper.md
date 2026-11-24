# How to Read a Research Paper — with *Lost in the Middle*

**The required paper:** Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) · [PDF](https://arxiv.org/pdf/2307.03172)

This is the one paper you must read for the midterm. This page teaches you *how* to read a research paper and uses *Lost in the Middle* as the worked example. You get the exam content and a skill you will use for every paper after this course.

**Time:** about 1.5–2 hours across three passes. Do not try to read it once, front to back, in a single sitting.

---

## 1. What a paper is

A research paper is an **argument**: a claim plus the evidence for it. Your job is not to absorb every sentence. It is to answer four questions, which are the same ones the course uses for every reading:

1. **What is the claim?**
2. **What evidence supports it?**
3. **Where does that evidence apply, and where does it not?**
4. **What would change your mind?**

Most empirical papers in computer science follow the same layout. Knowing it tells you where to look:

| Section | What it gives you | How closely to read it |
| --- | --- | --- |
| Title and abstract | The claim, compressed | Closely, twice |
| Introduction | The problem, why it matters, and the contributions (often a bulleted list) | Closely |
| Figures and tables | The evidence | Very closely: often the most important part |
| Method / experimental setup | What exactly was done | Closely on the second pass |
| Results and analysis | What happened and the authors' explanation | Closely on the second pass |
| Related work | How it fits with other papers | Skim |
| Limitations and conclusion | What the authors admit and conclude | Closely |
| Appendix | Extra detail and extra results | Only when you need something specific |

---

## 2. The three-pass method

This method comes from S. Keshav's short note *How to Read a Paper* (ACM SIGCOMM Computer Communication Review, 2007). Each pass goes deeper, and you can stop after any pass once you have what you need.

### Pass 1 — The bird's-eye view (10–15 minutes)

**Read only:** the title, the abstract, the introduction, every section heading, every figure with its caption, and the conclusion. Skip everything else.

**Then answer the "five Cs" in a sentence each:**

- **Category:** What kind of paper is it? (A controlled experiment, a new system, a survey, a vision or position piece?)
- **Context:** What problem or earlier work does it respond to?
- **Correctness:** Do the assumptions look reasonable at first sight?
- **Contributions:** What does it claim is new?
- **Clarity:** Is it well written enough to keep reading?

**Worked example: *Lost in the Middle*, pass 1**

- **Category:** An *empirical* paper made of controlled experiments. It does not propose a new model.
- **Context:** Language models were getting much longer context windows, but it was unclear how well they *use* everything in those windows.
- **Correctness:** The tasks have one right answer, so accuracy is easy to measure. That is a sound design choice.
- **Contributions:** When the information a model needs moves around inside a long input, performance changes a lot. It is highest at the **start or end** and lowest in the **middle**, which gives a **U-shaped curve**.
- **Clarity:** Short, readable, and built around a few clear figures.

> **Tip:** Figure 1, the U-shaped curve on the first pages, is the whole paper in one picture. If you only remember one thing, remember its shape.

### Pass 2 — Grasp the content (45–60 minutes)

**Read the body,** but skip fine detail such as exact prompts and appendix tables. Your goal is to be able to explain the paper to a classmate.

**For every experiment, write down three things:**

- **Independent variable:** what the authors changed on purpose.
- **Dependent variable:** what they measured.
- **Controls:** what they kept fixed so the comparison is fair.

**Read every figure on its own:** What is on each axis? What are the lines? Where is the baseline? What would the figure look like if the claim were false?

**Mark anything you don't understand** and keep going. Look it up after the pass, not in the middle of it.

**Worked example: *Lost in the Middle*, pass 2**

*Experiment A — multi-document question answering.*
- The model gets a question plus several documents. Exactly one document contains the answer and the others are distractors.
- **Independent variables:** where the answer document sits (first, middle, last…) and how many documents there are in total.
- **Dependent variable:** accuracy.
- **Result:** accuracy is highest when the answer document is first or last and drops when it is in the middle. In some settings, a model given the answer in the middle did *worse* than when it was given no documents at all and answered from memory (the "closed-book" baseline).

*Experiment B — key-value retrieval.*
- A synthetic task: a long list of random key-value pairs, and the model must return the value for one key.
- **Why it exists:** it strips out language understanding and tests *only* whether the model can find information at a given position.
- **Result:** some models handle it almost perfectly, but others show the same position effect.

*The "why" analysis.* The authors test possible explanations: model architecture, putting the question both before *and* after the documents ("query-aware contextualization"), and instruction tuning. **Note what each one did and did not fix.** For example, putting the question on both sides nearly solved the synthetic task but barely helped the question-answering task.

*The case study: is more context always better?* In a realistic retrieval setup, retrieving more documents keeps raising the chance that the answer is *somewhere* in the input, but the model's accuracy levels off much earlier. More context is not free.

*Which models?* Several open and closed models available in 2023, including GPT-3.5-Turbo and Claude 1.3, some in extended-context versions. **Write the date down.** It matters in pass 3.

### Pass 3 — Challenge it (30+ minutes; optional, but this is where understanding comes from)

**Try to rebuild the paper in your head:** if you had to run these experiments yourself, what would you do? Then compare your version with theirs. The differences show you hidden assumptions.

**Questions to ask any paper:**

- What did they *not* test?
- Would the result hold for a different task, a different model, or a later year?
- Is there a simpler explanation for the result?
- What would a follow-up experiment look like?

**Worked example: *Lost in the Middle*, pass 3**

- **Scope:** both tasks are *retrieval* tasks. A coding agent also has to reason, edit and use tools. Would you expect the same U-shape there? Why or why not?
- **Time:** these are 2023 models. Newer long-context models may do better on simple lookup. But later benchmarks (see RULER in the Week 4 references) suggest that the context length a model can *reliably* use is often shorter than the advertised one. Does that strengthen or weaken the paper's point?
- **A simpler explanation?** Training text often puts important information at the start, such as titles and introductions, and at the end, such as conclusions. Could the models have learned that habit?
- **Follow-up:** how would you test the effect inside a real coding session, for example by moving a key rule around in an `AGENTS.md` file?

---

## 3. Write an evidence note

Finish every paper with a short note, 150–200 words, under four headings. This is how you check you understood it. It is also the kind of thinking the exam rewards.

```
Claim:       one sentence
Evidence:    which experiments, which models, what result
Limits:      where the evidence does not reach
So what:     one design decision for working with agents that follows from it
```

**Example (yours should be in your own words):**

> **Claim:** Language models use information at the start and end of a long input much better than information in the middle.
> **Evidence:** Controlled experiments on multi-document QA and synthetic key-value retrieval, across several 2023 models, show a U-shaped accuracy curve as the relevant item moves through the input. Extended-context models show the same pattern.
> **Limits:** Retrieval-style tasks only; 2023 models; it does not test multi-step reasoning or coding agents directly.
> **So what:** Keep agent context short and deliberate, put the most important rules at the start or end, restate them in long sessions, and load material when the task needs it instead of up front.

---

## 4. Common traps

- **Reading the abstract and stopping.** The abstract is the authors' sales pitch. The figures are the evidence.
- **Treating "the model" as all models.** Results describe the models, tasks and dates tested.
- **Confusing a vision paper with evidence.** *Lost in the Middle* is a controlled experiment. A position or vision paper, such as SE 3.0, argues for an idea but does not test it.
- **Getting stuck on one paragraph.** Mark it, move on, and come back on the next pass.
- **Taking the authors' explanation as proven.** "Why" sections often contain hypotheses, not conclusions.

---

## 5. Why this paper matters for the course

- **Week 3:** the context window is a budget, and a larger window does not mean even attention across it.
- **Context Management:** this result is why the course talks about *managing* context instead of *stuffing* it. It also explains one item on the "agent ignored a constraint" checklist: *where did the constraint sit?*
- **Codebase Structure:** every line of `AGENTS.md`, every rule and every tool description competes for the same attention. That helps explain why longer context files do not reliably help.

---

## 6. Check yourself

1. What kind of paper is *Lost in the Middle*: a new system, a controlled experiment, or a vision piece?
2. In the multi-document QA experiment, what is the independent variable and what is the dependent variable?
3. What shape does accuracy take as the relevant document moves from the start of the input to the end?
4. Did models with extended context windows avoid the problem?
5. Why did the authors include a synthetic key-value task alongside question answering?
6. Name one setting where you would be careful about applying the paper's result, and say why.
7. Name one practical rule for writing agent context that follows from the paper.

<details>
<summary>Answers</summary>

1. A controlled experiment (an empirical study). It does not propose a new model.
2. Independent: the position of the document that contains the answer (and the number of documents). Dependent: accuracy.
3. A U-shape: highest at the start and end, lowest in the middle.
4. No. Extended-context versions showed the same pattern. A longer window raises how much fits, not how well the middle is used.
5. To isolate pure retrieval by position from language understanding.
6. For example: multi-step reasoning or coding tasks, or newer models, because the paper tested retrieval tasks on 2023 models.
7. For example: put the most important instructions at the start or end, keep context short, restate key rules in long sessions, or load material only when it is needed.

</details>

---

## Further reading on reading papers

- S. Keshav, *How to Read a Paper*, ACM SIGCOMM Computer Communication Review, 2007 — the three-pass method used above (two pages).

[Back to the study guide index](README.md)
