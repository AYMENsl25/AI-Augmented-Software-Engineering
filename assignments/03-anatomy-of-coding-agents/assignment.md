# Week 3 — Prompting Techniques: The Support-Desk Assistant

**Estimated time: ~3 hours.**

## Overview
To understand how coding agents work, you need to understand the model at their core.
You'll complete **four** prompting techniques, running an open model **locally with
[Ollama](https://ollama.com/)** so you can see exactly how each prompt changes behavior.
Every task targets one domain: an **AI support-desk assistant** for a small online store.

Starter stubs are in [`starter/`](starter/) — you only edit the prompt (and one
retriever) in each file.

## Learning goals
- Run an open model locally and inspect its raw behavior.
- Implement and compare four prompting techniques.
- Build intuition for why LLMs handle structured tasks well — and where they need scaffolding.

---

## Setup
1. Install **Ollama** (`brew install --cask ollama` / see ollama.com) and run `ollama serve`.
2. Pull the model: `ollama pull llama3.1:8b`.
3. `cd starter && pip install ollama`.

> **Rule:** only edit the parts marked `TODO` (the prompt, and the retriever in `rag.py`).
> Don't change the model or post-process outputs to fake a pass.

## The four techniques (each has a starter file with a built-in PASS/FAIL check)
1. **`k_shot_prompting.py`** — classify a support ticket into
   `billing | shipping | returns | technical` using in-context examples.
2. **`chain_of_thought.py`** — decide refund eligibility from a policy, reasoning step
   by step and ending in `DECISION: YES/NO`.
3. **`tool_calling.py`** — make the model call `get_order_status(order_id)` and use the result.
4. **`rag.py`** — answer a customer question grounded **only** in `data/help_center.txt`,
   and refuse politely when the answer isn't there.

Iterate each prompt until its check passes (`python k_shot_prompting.py`, etc.).

## Deliverables
**Submit the GitHub repository link** for your `starter/` folder, containing:
1. All four files with `TODO`s resolved and their checks passing.
2. A `writeup.md` with, **per technique**: your final prompt, one sample input/output,
   and **what you learned** (one line on how that technique changed the result).
3. A closing paragraph: across all four, **what you learned** about why LLMs are good at
   structured tasks and where they need scaffolding.

## Evaluation (100 pts)
- 20 per technique (×4 = 80): prompt is well-designed and the check passes.
- 20 — Writeup with per-technique + closing "what you learned".
