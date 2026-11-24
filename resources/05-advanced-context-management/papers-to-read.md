# Papers to Read — Advanced Context Management

This week's lecture treats the context window as the agent's working memory: a finite, expensive, and surprisingly fragile resource. The readings approach it from three sides. The mandatory paper is an empirical study of how models actually use long contexts, and its result should make you suspicious of "just put everything in the prompt." The practitioner guide is the clearest current statement of how production agents assemble, trim, and refresh context. The protocol reading explains how the Model Context Protocol (MCP) standardizes the way context and tools reach a model, which is what you build in this week's assignment.

## Mandatory

### Lost in the Middle: How Language Models Use Long Contexts

- **Authors:** Nelson F. Liu et al. (2023)
- **Paper:** [arXiv:2307.03172](https://arxiv.org/abs/2307.03172) · [PDF](https://arxiv.org/pdf/2307.03172)
- **Why this paper:** It measures what happens when the information a model needs sits at different positions inside a long prompt. Performance is highest when the relevant passage is at the start or the end and drops when it is in the middle. This is the single most important fact behind context *management* as opposed to context *stuffing*: a larger window does not mean uniform attention over it.

### How to read it

Plan for **45–60 minutes**.

1. **Pin down the task.** The experiments use multi-document question answering and key-value retrieval. Write one sentence describing each task and why the authors chose tasks where the correct answer is unambiguous.
2. **Study the position experiment.** Identify the independent variable (where the relevant document sits), the dependent variable (accuracy), and the shape of the resulting curve. Sketch the curve from memory after reading.
3. **Read the model comparisons critically.** Which models were tested, and when? The paper predates most current long-context models. Decide which conclusions are about *those models* and which are about *architecture and training* in general.
4. **Connect it to an agent.** A coding agent's prompt contains a system prompt, context files, retrieved code, tool outputs, and the conversation so far. Which of these tends to land in the middle, and what does the paper predict about it?
5. **Finish with a short evidence note (150–200 words).** State the claim, the evidence, one limitation, and one design decision for an agent that follows from it.

### What to take away

- Context is not a flat array the model reads evenly. Position, ordering, and the amount of irrelevant material all change what the model effectively "sees."
- Longer windows raise the ceiling, not the floor. Retrieval quality, ordering, and pruning still decide whether the right facts influence the answer.
- An AI-native engineer manages context deliberately: what enters, in what order, when it is summarized or dropped, and how it is refreshed from a source of truth.

### Effective context engineering for AI agents

- **Publisher:** Anthropic Engineering (September 29, 2025)
- **Source:** [anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- **Why read it:** This is a practitioner account of how a production coding agent manages its window. It introduces *context rot* (recall degrades as the window fills), argues for *just-in-time* retrieval over pre-loading, and describes three techniques for long-horizon work: compaction, structured note-taking, and sub-agent architectures. It is the bridge between the empirical paper above and the assembly pipeline covered in lecture.

> **Evidence note:** This is first-party engineering writing, not a controlled study. Read it for its vocabulary and design patterns, then ask which claims the *Lost in the Middle* results support and which are untested.

### How to read it

Read it in **30–40 minutes** and build a two-column table:

| Technique or claim | What problem it solves, and what it costs |
| --- | --- |
| Just-in-time retrieval (keep file paths, load on demand) | Fewer wasted tokens; more tool calls and latency |

Add at least four more rows (compaction, structured notes, sub-agents, system-prompt "altitude," tool-set design). For each, mark whether you have seen the technique in the coding agent you use.

### Model Context Protocol: specification and announcement

- **Sources:** [MCP specification](https://modelcontextprotocol.io/specification/latest) · [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (Anthropic, November 25, 2024)
- **Why read it:** MCP is the standard your assignment implements. The specification defines hosts, clients, and servers; the three server features (resources, prompts, tools); JSON-RPC transport; and a short but important section on security and trust.
- **Required reading:** The announcement (10 minutes), then the specification's *Overview*, *Architecture*, and *Security and Trust & Safety* sections, plus the *Tools* page under Server Features (30–40 minutes). Skip the wire-level schema details unless you are debugging.

### How to read it

1. **Draw the topology.** Host, client, server. Where does your Week 4 server sit, where does the model sit, and which component decides whether a tool call is allowed?
2. **Separate the three server features.** For resources, prompts, and tools, write one sentence on who initiates the use of each (user, application, or model).
3. **Read the security principles as requirements.** The specification says MCP "cannot enforce these security principles at the protocol level." List what that leaves to the host, the server author, and the user.
4. **Map the spec onto your starter code.** Which parts of `server.py` correspond to the tool's name, description, input schema, and result? Which of the spec's error-handling expectations does the starter not yet meet?

### What to take away

- MCP standardizes *how* context and tools reach a model. It does not decide *which* context is worth the tokens; that remains the engineer's design job.
- A tool's description and schema are part of the model's context. Writing them well is context engineering.
- Tool safety is a host responsibility. Descriptions coming from an untrusted server are untrusted input.

### Bring to class

Come prepared to answer:

> Your agent's prompt is 150k tokens: a system prompt, three context files, forty retrieved code snippets, and twenty tool results. Using this week's readings, which items would you cut, reorder, summarize, or move behind a tool, and what evidence supports each decision?

---

## Reference

### Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

- **Authors:** Patrick Lewis et al. (2020)
- **Source:** [arXiv:2005.11401](https://arxiv.org/abs/2005.11401) · [PDF](https://arxiv.org/pdf/2005.11401)
- **Importance:** The paper that named RAG. It combines a retriever with a generator so that knowledge lives in an index rather than in model weights. Agentic search over a repository is a descendant of this idea, with the model choosing what to retrieve.

### MemGPT: Towards LLMs as Operating Systems

- **Authors:** Charles Packer et al. (2023)
- **Source:** [arXiv:2310.08560](https://arxiv.org/abs/2310.08560) · [PDF](https://arxiv.org/pdf/2310.08560)
- **Importance:** Frames the context window as main memory and external storage as disk, with the model paging information in and out. The compaction and note-taking patterns in this week's practitioner reading are concrete instances of this metaphor.

### RULER: What's the Real Context Size of Your Long-Context Language Models?

- **Authors:** Cheng-Ping Hsieh et al. (2024)
- **Source:** [arXiv:2404.06654](https://arxiv.org/abs/2404.06654) · [PDF](https://arxiv.org/pdf/2404.06654)
- **Importance:** A benchmark showing that the advertised context length and the length at which a model stays reliable are different numbers. Useful when a vendor's context-window figure tempts you to skip context management.

### A Survey of Context Engineering for Large Language Models

- **Authors:** Lingrui Mei et al. (2025)
- **Source:** [arXiv:2507.13334](https://arxiv.org/abs/2507.13334) · [PDF](https://arxiv.org/pdf/2507.13334)
- **Importance:** A broad map of the field: retrieval, memory, tool integration, and multi-agent context sharing. Use it to place the lecture's taxonomy in the wider literature, not as a first read.

### Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

- **Authors:** Qizheng Zhang et al. (2025)
- **Source:** [arXiv:2510.04618](https://arxiv.org/abs/2510.04618) · [PDF](https://arxiv.org/pdf/2510.04618)
- **Importance:** Treats the context itself as the thing to optimize: an agent revises its own instructions and notes across runs. A preview of Week 9's self-improving systems, and a reminder that context is a living artifact.

---

## Reading principle for this course

Treat the context window as a **budget you spend on behalf of the model**. For every piece of context an agent receives, be able to say:

1. **What decision does it inform?**
2. **Where did it come from, and is that source trusted?**
3. **When does it become stale, and how is it refreshed?**
4. **What evidence shows the model actually uses it?**
