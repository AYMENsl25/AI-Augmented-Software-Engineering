# Papers to Read — Security in the Age of AI

This week's lecture covers two directions at once. AI tools help find and fix classic vulnerabilities faster (SAST, SCA, secret scanning, agent-assisted triage), and AI systems introduce a new class of vulnerability in which untrusted text becomes instructions. The two mandatory papers cover each direction. The first defined indirect prompt injection and showed it working against deployed systems. The second is a controlled user study on whether people write less secure code with an AI assistant, and whether they notice. The reference list adds the empirical baseline for AI-generated code security, the supply-chain and secret-leak evidence behind the scanning exercise, and the current defensive designs for agents.

## Mandatory

### Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection

- **Authors:** Kai Greshake et al. (2023)
- **Paper:** [arXiv:2302.12173](https://arxiv.org/abs/2302.12173) · [PDF](https://arxiv.org/pdf/2302.12173)
- **Why this paper:** It introduced *indirect* prompt injection: an attacker never talks to the model directly but plants instructions in data the model will later read (a web page, a document, a retrieved file). Once a model has tools, that turns a text-generation quirk into remote code execution by proxy. The paper's threat taxonomy (information gathering, fraud, intrusion, manipulated content, availability) is still the standard way to talk about agent attack surfaces, and the Part 3 exercise in this week's assignment is a direct instance of the attack class it describes.

### How to read it

Plan for **60 minutes**.

1. **Get the definition exact.** Write one sentence distinguishing direct from indirect injection, and one sentence on why the distinction matters more once the model can call tools.
2. **Study the threat taxonomy.** For each category, name one concrete attack from the paper and one that would apply to the coding agent you use (for example: a planted comment in a dependency's README telling the agent to run a command).
3. **Trace one end-to-end demonstration.** Where did the malicious text enter, how did it reach the model, what did the model do, and which component *could* have stopped it?
4. **Read the mitigations section skeptically.** The authors are candid that there was no complete defense. List what they propose and mark each as: reduces likelihood, reduces impact, or detects after the fact.
5. **Finish with a short evidence note (150–200 words).** State the claim, the evidence, one limitation (the systems tested are from 2023), and the mitigation you will implement in Part 3 with a sentence on what it does *not* protect against.

### What to take away

- Any text a model reads can carry instructions. There is no reliable in-band way to tell the model which text is data. Defenses therefore live in the architecture around the model: what it can read, what it can do, and what is checked before an action takes effect.
- Tool access turns a confidentiality problem into an integrity and availability problem. The blast radius of an injection equals the permissions of the agent.
- "Ignore the above and..." is the toy version. Real injections are indirect, hidden, and aimed at tools.

### Do Users Write More Insecure Code with AI Assistants?

- **Authors:** Neil Perry et al. (2022)
- **Paper:** [arXiv:2211.03622](https://arxiv.org/abs/2211.03622) · [PDF](https://arxiv.org/pdf/2211.03622)
- **Why this paper:** A controlled user study in which participants solved security-relevant programming tasks with or without an AI assistant. Participants with the assistant produced less secure solutions on most tasks and were *more* likely to believe their code was secure. The second finding is the important one for this course: the risk is not only in the generated code but in the confidence it induces. This is the human-factors half of the scanning exercise.

> **Evidence note:** The study is from 2022, uses an early code model, and has a modest sample. The direction of the effect is informative; the magnitude will differ with current tools. Read it for the design and the confidence finding, not for the exact percentages.

### How to read it

Plan for **40 minutes**.

1. **Identify the design.** Participants, tasks, languages, the treatment and control, and how security was judged.
2. **Separate the two results.** Record the security outcome and the confidence outcome separately. Which is more likely to persist as models improve, and why?
3. **Look for the behavioral mechanism.** How did participants interact with the assistant when they produced secure versus insecure code? What does that suggest about prompting, review, and trust?
4. **Compare with the Copilot security baseline.** *Asleep at the Keyboard?* (below) measured generated code without humans; this paper measures humans with the tool. What does each study miss that the other covers?

### What to take away

- AI-assisted code needs the same scanning and review as human code, and arguably more, because the author's confidence is less reliable as a signal.
- Deterministic scanners (SAST, SCA, secret detection) are the counterweight to over-confidence. They do not care how sure you are.
- Treat an agent's "this is secure" the way you would treat a junior engineer's: as a prompt to check, not as a verdict.

### OWASP Top 10 for LLM Applications 2025

- **Source:** [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/)
- **Why read it:** The current community taxonomy of LLM application risks, with prompt injection at LLM01. Several entries (improper output handling, excessive agency, supply chain, system prompt leakage) describe the vulnerable bookstore in this week's assignment. Skim the ten entries (20 minutes) and map each planted issue in the starter to an entry.

### Bring to class

Come prepared to answer:

> Your coding agent reads an issue from a public tracker and opens a pull request fixing it. Using the Greshake et al. taxonomy, list three ways an attacker who can only edit the issue text could harm you, and for each say which single architectural change (not a prompt change) would block it.

---

## Reference

### Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions

- **Authors:** Hammond Pearce et al. (2021)
- **Source:** [arXiv:2108.09293](https://arxiv.org/abs/2108.09293) · [PDF](https://arxiv.org/pdf/2108.09293)
- **Importance:** The first systematic measurement of vulnerabilities in AI-generated code, using CWE-based scenarios and static analysis. A substantial fraction of generated programs were vulnerable. The baseline every later "is AI code secure?" study is compared with.

### Examining Zero-Shot Vulnerability Repair with Large Language Models

- **Authors:** Hammond Pearce et al. (2021; revised 2022)
- **Source:** [arXiv:2112.02125](https://arxiv.org/abs/2112.02125) · [PDF](https://arxiv.org/pdf/2112.02125)
- **Importance:** The other half of the story: can models *fix* vulnerabilities? The answer is "sometimes, with good prompts and a way to verify," which is exactly the agent-assisted remediation loop in Part 2 of the assignment. Note how much the results depend on the prompt and on having tests.

### We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs

- **Authors:** Joseph Spracklen et al. (2024)
- **Source:** [arXiv:2406.10279](https://arxiv.org/abs/2406.10279) · [PDF](https://arxiv.org/pdf/2406.10279)
- **Importance:** Models recommend packages that do not exist, and attackers can register those names. This is the AI-specific supply-chain risk behind SCA scanning: your dependency list may contain names a model invented.

### How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories

- **Authors:** Michael Meli, Matthew R. McNiece, and Bradley Reaves (NDSS 2019)
- **Source:** [NDSS paper page](https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/) · [PDF](https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf)
- **Importance:** A large-scale, longitudinal measurement of API keys and private keys leaked to public GitHub, finding thousands of new unique secrets per day. The empirical reason secret scanning and pre-commit hooks exist, and relevant to the leak checks in this course's own submission instructions.

### Design Patterns for Securing LLM Agents against Prompt Injections

- **Authors:** Luca Beurer-Kellner et al. (2025)
- **Source:** [arXiv:2506.08837](https://arxiv.org/abs/2506.08837) · [PDF](https://arxiv.org/pdf/2506.08837)
- **Importance:** A catalogue of architectural patterns (for example: action-selector, plan-then-execute, dual LLM, context minimization) that constrain what an injected instruction can achieve, with case studies. The constructive follow-up to Greshake et al.

### Defeating Prompt Injections by Design

- **Authors:** Edoardo Debenedetti et al. (2025)
- **Source:** [arXiv:2503.18813](https://arxiv.org/abs/2503.18813) · [PDF](https://arxiv.org/pdf/2503.18813)
- **Importance:** CaMeL: a system that separates control flow from untrusted data using capabilities, so injected text cannot redirect actions even if it influences content. An example of defending at the architecture level rather than with prompt text.

### AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

- **Authors:** Edoardo Debenedetti et al. (2024)
- **Source:** [arXiv:2406.13352](https://arxiv.org/abs/2406.13352) · [PDF](https://arxiv.org/pdf/2406.13352)
- **Importance:** A benchmark for measuring how often agents with tools are hijacked and how much defenses cost in utility. Useful for calibrating claims about any defense, including the one you implement in Part 3.

### MCP Safety Audit: LLMs with the Model Context Protocol Allow Major Security Exploits

- **Authors:** Brandon Radosevich and John Halloran (2025)
- **Source:** [arXiv:2504.03767](https://arxiv.org/abs/2504.03767) · [PDF](https://arxiv.org/pdf/2504.03767)
- **Importance:** Demonstrates attacks through MCP servers and tools, connecting Week 4's protocol to this week's threat model. Tool descriptions and server outputs are untrusted input.

### Universal and Transferable Adversarial Attacks on Aligned Language Models

- **Authors:** Andy Zou et al. (2023)
- **Source:** [arXiv:2307.15043](https://arxiv.org/abs/2307.15043) · [PDF](https://arxiv.org/pdf/2307.15043)
- **Importance:** Automatically generated suffixes that make aligned models comply with harmful requests, transferring across models. Evidence that model-level refusal training is not a security boundary, which is why this week's defenses sit outside the model.

---

## Reading principle for this course

Treat every input to an agent as **potentially adversarial** and every agent action as **potentially attacker-controlled**. For each system you build or scan, be able to say:

1. **What untrusted text can reach the model, and from where?**
2. **What can the model do once it has read it?**
3. **Which check runs *after* the model and *before* the action takes effect?**
4. **What evidence shows the defense works against an attack you did not design?**
