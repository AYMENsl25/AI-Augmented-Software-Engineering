# Starter — Prompting Techniques

Fill-in-the-prompt stubs for four techniques. You only edit the `TODO` parts (the
prompt, and the retriever in `rag.py`).

## Setup
1. Install Ollama and start it: `ollama serve` (see https://ollama.com).
2. Pull the model: `ollama pull llama3.1:8b`.
3. Install the client: `pip install ollama`.

## Run each technique
Each file has a built-in PASS/FAIL check:
```bash
python k_shot_prompting.py
python chain_of_thought.py
python tool_calling.py
python rag.py
```
Iterate the prompt until the check passes.

## Files
- `k_shot_prompting.py` — ticket classification
- `chain_of_thought.py` — refund eligibility
- `tool_calling.py` — order lookup via a tool call
- `rag.py` — answer grounded only in `data/help_center.txt`
