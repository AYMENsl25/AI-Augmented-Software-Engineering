# Week 3 — Anatomy of Coding Agents

Slides: [`lectures/03-anatomy-of-coding-agents/`](../../lectures/03-anatomy-of-coding-agents/) · Readings: [`resources/03-anatomy-of-coding-agents/papers-to-read.md`](../03-anatomy-of-coding-agents/papers-to-read.md)

## How LLMs work

- An **LLM** is a neural network with billions of parameters trained on huge amounts of text and code to **predict the next token**. It stores statistical patterns, not its training text.
- **Tokens, not words.** `getUserById(userId)` ≈ 7 tokens; ~3–4 characters per token in English prose; a 600-line TypeScript file ≈ 4–5k tokens.
- **One token at a time.** No planning pass, no going back — early mistakes carry through.
- **Attention.** Each token looks at every other token and weights the relevant ones ("it" → "animal" when *tired*, → "street" when *wide*). The **Transformer** (Vaswani et al., 2017, "Attention Is All You Need"): text → tokens → vectors → dozens of attention + feed-forward layers → scores for every possible next token; the chosen token is appended and the pipeline runs again. It won because it reads all tokens in parallel, so it trains at huge scale.
- **Training:** hide the next word, model guesses a probability for each candidate, compare to the real word, nudge billions of weights; repeat for trillions of tokens. The weights are then **frozen** at a cutoff date.
- **Post-training with human preference feedback (RLHF):** generate alternatives → a person picks the better one → a reward model learns the preference → the LM learns to score higher. *Preference does not guarantee correctness.*
- **Post-training with verifiable feedback:** attempt the task → run tests/compilers/formal checks → reward passing results → the model learns strategies that produce verifiable success.
- **Two kinds of knowledge.** *In-weights (parametric):* learned during training, always available, fixed at the cutoff, may be stale or wrong. *In-context (non-parametric):* supplied with the request (prompt, files, docs, tool results), current and authoritative when trusted, uses the context window, not retained.
- **The context window is a budget.** Simple "needle in a haystack" lookup is solid up to the advertised window; harder multi-step reasoning degrades well before the limit.
- **Models are probabilistic.** Same prompt, different equally-correct outputs — even at temperature 0 outputs can vary across runs and hardware. **Test behaviour, not strings** (does it parse, do tests pass, is the edge case handled, does lint pass).

## The model landscape

- **Openness levels:** *fully open* (weights, data, code — most auditable, usually lower ceiling), *open weights* (Llama, Mistral, Qwen, DeepSeek — self-host and fine-tune; training data private), *closed* (GPT, Claude, Gemini — API only; can run in your cloud, never on your own servers). Choose by hard constraints: where data may go, fine-tuning needs, ops effort, vendor lock-in.
- **Kinds of models:** pre-trained (raw foundation), fine-tuned (adapted with task-specific data), reasoning (RL-trained to spend extra compute on step-by-step logic before answering), specialised (e.g. BioBERT, legal).
- **Reasoning models:** chain of thought by default; more tokens and compute (**test-time compute**); slower and costlier (hidden thinking tokens are billed). Use standard models for routine, well-specified work; reasoning models for ambiguous, multi-step, high-stakes work (a race condition, a schema with many invariants).
- Frontier models (Oct 2026) have context windows around **~1M tokens**.

## Why LLMs are good at coding (four reasons)

1. Seen it millions of times (GitHub, Stack Overflow, docs, tutorials).
2. It runs or it doesn't — strict rules give a clear training signal.
3. Boilerplate is predictable (CRUD endpoints, test setup, config files).
4. Code and docs together (source, README, docs and Q&A about the same library). Strongest for widely used languages and frameworks; weaker for internal, one-company frameworks.

## Coding agents under the hood

- **The messages array:** system / user / assistant roles. The API is **stateless** — no memory between calls; your app resends the full history every time, so cost grows with each turn. The **system prompt** is read first on every call — your highest-leverage input.
- **What is an agent?** A language model combined with **tools, context and a loop** — able to pursue a goal over several steps without approval at each step.
- **The agentic loop:** reason → act → observe, until the goal is reached or the run must stop. **ReAct** (Yao et al., 2022): a visible reasoning trace connects each decision to an action and its result.
- **Agent = Model + Harness.** Six components of a coding harness:
  1. **Live repo context** — turns a changing repository into stable prompt context.
  2. **The system prompt.**
  3. **Tool access and use** — read and search (Read, Glob, Grep), change files (Edit, Write), run (Bash), look things up (WebSearch, WebFetch), plan and delegate (Plan Mode, Agent).
  4. **Context reduction** — clip long outputs (first + last lines), dedupe repeated reads (latest only), compress older turns into a summary.
  5. **Session memory** — the model retains nothing between calls; the harness stores state on disk: a full **transcript** (append) and a distilled **working memory** (rewrite).
  6. **Delegation to subagents** — side questions run in parallel in their own context while the main agent keeps working.

## Required readings

- **Vaswani et al. 2017, *Attention Is All You Need*.** Self-attention, multi-head attention, positional information, parallel sequence processing. Be able to explain what attention buys compared with recurrence.
- **Video: *Visual representation of coding agents and their limitations*.** The system *around* the model: context gathering, planning, tool calls, feedback loops, and where they break. Distinguish a **model** failure (knowledge) from a **system / agent-loop** failure.
- **Stanford companions:** *Building a Coding Agent* (video), *Lessons from Building Claude Code*, *Dive into Claude Code*.
- **Reference lineage (know what each adds):** Transformers (2017) → learning from human preferences (Christiano 2017) → BERT pretraining (2018) → GPT-3 in-context learning (2020) → Codex / HumanEval and functional correctness (2021) → chain-of-thought prompting (Wei 2022) → InstructGPT / RLHF (Ouyang 2022) → ReAct (2022) → DPO, optimising directly from preference pairs without a separate reward model (2023) → GRPO, group-relative rewards without a critic (DeepSeekMath 2024) → o1 and test-time reasoning (2024) → DeepSeek-R1 reasoning via RL (2025).
- **Core takeaway:** a coding agent is a *system*, not a single model. Each layer (architecture, training, alignment, loop, tools) adds capability and its own failure modes.

---

[Back to the study guide index](README.md)
