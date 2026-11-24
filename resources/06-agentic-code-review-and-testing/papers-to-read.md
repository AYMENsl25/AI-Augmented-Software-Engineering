# Papers to Read — Agentic Code Review and Testing

This week's lecture pairs two kinds of check: **deterministic guardrails** (compilers, linters, tests, coverage gates) that give a yes/no answer every time, and **LLM-based review** that can reason about intent but can also be confidently wrong. The readings are two industrial studies in which both kinds of check were combined at scale, plus reference work on why tests are a weaker oracle than they look and on the known biases of models acting as judges. Together they should leave you with a working rule for when to trust an AI review and when to demand a test.

## Mandatory

### Automated Unit Test Improvement using Large Language Models at Meta

- **Authors:** Nadia Alshahwan et al. (2024)
- **Paper:** [arXiv:2402.09171](https://arxiv.org/abs/2402.09171) · [PDF](https://arxiv.org/pdf/2402.09171)
- **Why this paper:** It describes TestGen-LLM, a system deployed at Meta that asks a model to extend existing unit tests and then keeps a generated test *only if* it builds, passes reliably, and increases coverage. The authors call this *assured* LLM-based software engineering: the model proposes, deterministic filters decide. The paper reports how many candidates survived each filter and how many of the surviving recommendations engineers accepted. It is the clearest published example of the guardrail-plus-LLM architecture this week's assignment asks you to build in miniature.

### How to read it

Plan for **45–60 minutes**.

1. **Draw the pipeline.** Model generates candidate tests → build filter → pass/flakiness filter → coverage filter → human review. Note which stages are deterministic and which involve judgment.
2. **Read the funnel numbers carefully.** What fraction of candidates built, passed, and improved coverage? What fraction of surviving recommendations did engineers accept? Record the numbers with their denominators; do not reduce the paper to one percentage.
3. **Ask what the filters cannot catch.** A test that builds, passes, and adds coverage can still assert the wrong behavior. Where in the pipeline does that error get caught, if at all?
4. **Study the human step.** Why did the authors keep an engineer in the loop after three automated filters? What did reviewers reject, and why?
5. **Finish with a short evidence note (150–200 words).** State the claim, the evidence, one limitation (codebase, language, task type), and one filter you would add for your own project.

### What to take away

- Deterministic filters turn an unreliable generator into a reliable system. The model does not need to be right every time if a cheap, exact check runs after it.
- "Builds and passes" is necessary, not sufficient. Coverage and human review address different failure modes, and none of the three alone is enough.
- Measure the funnel. The value of an AI testing or review tool is in the acceptance rate after filtering, not in how much it generates.

### Resolving Code Review Comments with Machine Learning

- **Authors:** Alexander Frömmgen, Jacob Austin, Peter Choy, Elena Khrapko, Marcus Revaj, and Satish Chandra (Google, ICSE-SEIP 2024)
- **Paper:** [research.google publication page](https://research.google/pubs/resolving-code-review-comments-with-machine-learning/) · [ICSE 2024 SEIP listing](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-in-practice/35/Resolving-Code-Review-Comments-with-Machine-Learning)
- **Why this paper:** Google deployed a model that reads a human reviewer's comment and proposes the code edit that resolves it. The paper reports how often authors actually applied the suggestion and how the rollout changed over time (suggestions first appeared after review, then at review time). It shows LLM-based review working *inside* an existing human review process rather than replacing it, which is the configuration you will use with an AI reviewer on your two pull requests.

> **Evidence note:** This is an industry experience report with a single company's data and tooling. The acceptance rate it reports is informative about that setting; treat it as a benchmark for your own measurement, not as a universal number.

### How to read it

Plan for **30–40 minutes**.

1. **Locate the human in the loop.** Who writes the comment, who proposes the fix, who decides? What does the model never do on its own?
2. **Read the acceptance metric.** What fraction of reviewer comments ended with the author applying the suggested edit? What does that imply about the other comments?
3. **Note the rollout decisions.** Why did surfacing suggestions *during* review rather than after change the outcome? What does that say about where review tooling should sit?
4. **Compare with your AI reviewer.** Your tool comments on the diff unprompted. Google's tool acts on a human's comment. Which is more likely to be accepted, and which is more likely to find something a human missed?

### What to take away

- The most reliable deployments of LLM review so far keep a human as the source of judgment and use the model to reduce mechanical work.
- Acceptance rate is the honest metric for review tooling. Volume of comments is not.
- Where a suggestion appears in the workflow (before, during, or after review) changes how useful it is.

### Bring to class

Come prepared to answer:

> An AI reviewer leaves twelve comments on your pull request. Three are about naming, two are about a missing null check, one claims a test is wrong, and six are style. Using this week's readings, which comments do you act on without a test, which do you turn into a test, and which do you ignore, and how would you measure whether your policy was right over a semester?

---

## Reference

### Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation

- **Authors:** Jiawei Liu et al. (2023)
- **Source:** [arXiv:2305.01210](https://arxiv.org/abs/2305.01210) · [PDF](https://arxiv.org/pdf/2305.01210)
- **Importance:** Introduces EvalPlus, which adds many more test inputs to a standard benchmark and finds that a meaningful share of "passing" generated programs were actually wrong. Tests are an oracle only as strong as their inputs. Read this before trusting a green check.

### Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

- **Authors:** Lianmin Zheng et al. (2023)
- **Source:** [arXiv:2306.05685](https://arxiv.org/abs/2306.05685) · [PDF](https://arxiv.org/pdf/2306.05685)
- **Importance:** The standard reference on using a model to evaluate outputs. It documents position bias, verbosity bias, and self-enhancement bias. An AI code reviewer is an LLM judge; these biases apply to it.

### Automating Code Review Activities by Large-Scale Pre-training

- **Authors:** Zhiyu Li et al. (2022)
- **Source:** [arXiv:2203.09095](https://arxiv.org/abs/2203.09095) · [PDF](https://arxiv.org/pdf/2203.09095)
- **Importance:** CodeReviewer, a model pretrained on review data for three tasks: predicting whether a change needs review, generating the review comment, and refining code from a comment. A useful decomposition of what "AI code review" actually consists of.

### Large Language Models are Few-shot Testers: Exploring LLM-based General Bug Reproduction

- **Authors:** Sungmin Kang, Juyeon Yoon, and Shin Yoo (2022)
- **Source:** [arXiv:2209.11515](https://arxiv.org/abs/2209.11515) · [PDF](https://arxiv.org/pdf/2209.11515)
- **Importance:** Uses a model to turn a bug report into a failing test. The failing test is a deterministic artifact a human can verify, which makes it a safer output than a proposed fix.

### SWE-bench: Can Language Models Resolve Real-World GitHub Issues?

- **Authors:** Carlos E. Jimenez et al. (2023)
- **Source:** [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) · [PDF](https://arxiv.org/pdf/2310.06770)
- **Importance:** The benchmark most agent results are reported on. Its scoring is test-based, which makes the EvalPlus critique above directly relevant: a resolved issue means the hidden tests pass, not that the patch is the one a maintainer would merge.

---

## Reading principle for this course

Treat every check on agent output as having a **known failure mode**. For each guardrail or review step, be able to say:

1. **What does it catch deterministically?**
2. **What can it miss, and what would catch that?**
3. **What does it cost per run, and who pays attention to its output?**
4. **What acceptance or defect data would tell you it is working?**
