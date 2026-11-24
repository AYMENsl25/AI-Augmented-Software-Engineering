# Papers to Read — Anatomy of Coding Agents

This week traces the technical lineage behind contemporary coding agents: the Transformer architecture; pretrained language representations; preference learning and reinforcement learning; and reasoning-oriented models. The goal is not to memorize every objective function. It is to develop a working mental model of why a coding agent can interpret context, generate code, use tools, revise a plan, and still fail in systematic ways.

## Start here — coding-agent companion resources

The following resources are also used in **CS146S: The Modern Software Developer, Stanford University, Fall 2026**, as Week 1 reading for *The Internals of Coding Agents*. They are not substitutes for the mandatory items below, but they give a practical systems-level view of how current coding agents are built.

**Strongly encouraged:** Complete all three Stanford companion resources before class. They will make the foundational papers much easier to connect to real coding-agent behavior.

1. **[Building a Coding Agent](https://youtube.com/watch?v=s7ZzkdvCMDY)** — video walkthrough of the systems and loops behind a coding agent.
2. **[Lessons from Building Claude Code](https://x.com/trq212/status/2027463795355095314)** — practitioner lessons from building an agentic coding product.
3. **[Dive into Claude Code](https://arxiv.org/pdf/2604.14228)** — paper on the design and operation of Claude Code.

Also watch this companion resource:

4. **[Visual representation of coding agents and their limitations](https://www.youtube.com/watch?v=k2qls2LiBRc)** — a visual model of agent loops, tool use, context limits, and failure modes.

---

## Mandatory

### 1. Attention Is All You Need

- **Authors:** Ashish Vaswani et al. (2017)
- **Source:** [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) · [PDF](https://arxiv.org/pdf/1706.03762)
- **Why it matters:** This paper introduced the Transformer architecture: self-attention, multi-head attention, positional information, and parallel sequence processing. Modern LLMs—and therefore coding agents—are built on this lineage. It is the right place to understand how a model can relate a token in a current edit to relevant tokens elsewhere in a prompt or code context.
- **Required reading:** Read the abstract, introduction, model architecture, and conclusion. Do not worry about reproducing every derivation; be able to explain what attention is buying compared with recurrence.

### 2. Visual representation of coding agents and their limitations

- **Resource:** [YouTube video](https://www.youtube.com/watch?v=k2qls2LiBRc)
- **Why it matters:** The Transformer explains the model inside the agent; this video focuses on the surrounding system: context gathering, planning, tool calls, feedback loops, and where those loops break down. Pair it with the attention paper to distinguish a language model from a coding agent.
- **Required viewing:** Watch before class and bring one example of a limitation that is primarily a **system/agent-loop** problem rather than a base-model knowledge problem.

### Questions to bring to class

1. In a coding-agent prompt containing an issue, repository files, terminal output, and tests, what could attention help the model relate—and what does it *not* guarantee?
2. Which parts of a coding agent are learned model behavior, and which are ordinary software engineering around the model?
3. Why can an agent with a strong model still make a bad patch after apparently reading the relevant code?

---

## Reference papers — chronological foundational sequence

These are reference readings, not surveys. They are ordered by first public year so the progression is explicit: **architecture → learning from preferences → pretraining and in-context learning → code specialization → reasoning/tool loops → preference optimization → reasoning-model RL**.

### 2017 — Attention / Transformers

#### Attention Is All You Need

- **Authors:** Ashish Vaswani et al. (2017)
- **Source:** [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) · [PDF](https://arxiv.org/pdf/1706.03762)
- **Importance:** The foundational Transformer paper. Its self-attention mechanism is the architectural basis for the large language models used by coding agents.

### 2017 — Learning from human preferences

#### Deep Reinforcement Learning from Human Preferences

- **Authors:** Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei (2017)
- **Source:** [arXiv:1706.03741](https://arxiv.org/abs/1706.03741) · [PDF](https://arxiv.org/pdf/1706.03741)
- **Importance:** The conceptual precursor to RLHF: learn a reward model from human comparisons rather than requiring a hand-written reward. It is not about language models, but it establishes the preference-learning pattern later adapted to instruction-following LLMs.

### 2018 — BERT and pretraining

#### BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding

- **Authors:** Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova (2018)
- **Source:** [arXiv:1810.04805](https://arxiv.org/abs/1810.04805) · [PDF](https://arxiv.org/pdf/1810.04805)
- **Importance:** BERT established the practical power of large-scale Transformer pretraining followed by task-specific adaptation. It is an encoder model rather than the autoregressive decoder family usually used for code generation, but it is essential context for understanding how pretrained representations changed NLP and software tooling.

### 2020 — Scaling and in-context learning

#### Language Models are Few-Shot Learners

- **Authors:** Tom B. Brown et al. (2020)
- **Source:** [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) · [PDF](https://arxiv.org/pdf/2005.14165)
- **Importance:** The GPT-3 paper demonstrated that sufficiently scaled autoregressive language models can perform new tasks from instructions and examples in context, without parameter updates. This is the foundation for prompt- and context-driven coding assistance.

### 2021 — Code-specialized language models

#### Evaluating Large Language Models Trained on Code

- **Authors:** Mark Chen et al. (2021)
- **Source:** [arXiv:2107.03374](https://arxiv.org/abs/2107.03374) · [PDF](https://arxiv.org/pdf/2107.03374)
- **Importance:** Introduces Codex and HumanEval. It is a key bridge from general language modeling to code generation, while also foregrounding a problem agents still face: measuring functional correctness rather than merely generating plausible-looking code.

### 2022 — Prompted reasoning

#### Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

- **Authors:** Jason Wei et al. (2022)
- **Source:** [arXiv:2201.11903](https://arxiv.org/abs/2201.11903) · [PDF](https://arxiv.org/pdf/2201.11903)
- **Importance:** Shows that prompts containing intermediate reasoning steps can substantially improve performance on multi-step problems. It is foundational for understanding why agents plan, decompose tasks, and expose intermediate scratch work—while also reminding us that a convincing rationale is not proof of correctness.

### 2022 — RLHF for instruction-following models

#### Training Language Models to Follow Instructions with Human Feedback

- **Authors:** Long Ouyang et al. (2022)
- **Source:** [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) · [PDF](https://arxiv.org/pdf/2203.02155)
- **Importance:** The InstructGPT paper is the landmark modern account of **reinforcement learning from human feedback (RLHF)**. It explains the supervised fine-tuning, human preference-data, reward-model, and policy-optimization pipeline that made general-purpose language models substantially more useful as instruction-following assistants.

### 2022 — Agent reasoning and acting loops

#### ReAct: Synergizing Reasoning and Acting in Language Models

- **Authors:** Shunyu Yao et al. (2022)
- **Source:** [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) · [PDF](https://arxiv.org/pdf/2210.03629)
- **Importance:** Establishes a simple but enduring agent pattern: interleave reasoning traces with actions and observations. This is a direct conceptual ancestor of coding-agent loops that inspect files, run commands/tests, observe outputs, and revise a plan.

### 2023 — Direct Preference Optimization (DPO)

#### Direct Preference Optimization: Your Language Model is Secretly a Reward Model

- **Authors:** Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea Finn (2023)
- **Source:** [arXiv:2305.18290](https://arxiv.org/abs/2305.18290) · [PDF](https://arxiv.org/pdf/2305.18290)
- **Importance:** DPO reformulates preference alignment so a model can be optimized directly from preference pairs, without separately fitting a reward model and running the usual RL policy-optimization loop. It became influential because it makes a major class of alignment training simpler and more stable to implement.

### 2024 — Group Relative Policy Optimization (GRPO)

#### DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models

- **Authors:** Zhihong Shao et al. (2024)
- **Source:** [arXiv:2402.03300](https://arxiv.org/abs/2402.03300) · [PDF](https://arxiv.org/pdf/2402.03300)
- **Importance:** Introduces **Group Relative Policy Optimization (GRPO)**, a PPO-style method that uses relative rewards within a group of sampled outputs and avoids a separate critic model. It matters because it made large-scale reinforcement learning for reasoning more memory-efficient and became a key ingredient in the DeepSeek reasoning-model line.

### 2024 — OpenAI reasoning-model sources

#### Learning to Reason with LLMs

- **Publisher:** OpenAI (2024)
- **Source:** [OpenAI](https://openai.com/index/learning-to-reason-with-llms/)
- **Importance:** The primary public introduction to the o1 reasoning-model approach. It frames test-time reasoning and reinforcement learning as ways to improve performance on difficult problems. It is a research/product article rather than a peer-reviewed paper, so treat its claims as first-party technical communication.

#### OpenAI o1 System Card

- **Publisher:** OpenAI (2024)
- **Source:** [arXiv:2412.16720](https://arxiv.org/abs/2412.16720) · [OpenAI system card](https://openai.com/index/openai-o1-system-card/)
- **Importance:** The most substantial public technical and safety documentation for o1. It describes the model family’s large-scale reinforcement-learning approach to chain-of-thought reasoning, as well as the safety evaluations and risk-management framing that should accompany reasoning-capable systems.

### 2025 — DeepSeek-R1

#### DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

- **Authors:** DeepSeek-AI et al. (2025)
- **Source:** [arXiv:2501.12948](https://arxiv.org/abs/2501.12948) · [PDF](https://arxiv.org/pdf/2501.12948)
- **Importance:** Documents the DeepSeek-R1/R1-Zero reasoning-training approach: large-scale RL, including a pure-RL experiment, followed by cold-start and multi-stage training for a more usable model. It is a central open account of how extended reasoning behaviors—such as checking, revising, and allocating more tokens to hard problems—can be induced and operationalized.

---

## How to read these papers

Use the same four questions for every item:

1. **What capability is being added?** For example: long-range token interaction, pretrained representations, following preferences, or allocating computation to reasoning.
2. **What is the training signal?** Next-token prediction, labels, human preference comparisons, verifiable rewards, or relative group rewards?
3. **What is the engineering trade-off?** Compute, memory, data quality, controllability, latency, transparency, or safety?
4. **What does this imply for coding agents?** Better code completion does not itself provide repository context, correct tool use, reliable verification, or accountable engineering judgment.

## Core takeaway

A coding agent is a system, not a single model: a Transformer-based language model is trained and aligned using particular objectives, then embedded in a loop that selects context, proposes actions, invokes tools, observes results, and tries again. Each layer introduces capability—and its own failure modes. The mandatory attention paper and visualization video anchor that distinction; the Stanford resources and reference papers explain how the stack evolved.
