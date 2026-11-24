# Advanced Context Management

Slides: [`lectures/05-advanced-context-management/`](../../lectures/05-advanced-context-management/) · Readings: [`resources/05-advanced-context-management/papers-to-read.md`](../05-advanced-context-management/papers-to-read.md)

## Why context engineering

- **The same agent, the wrong output.** "Add an endpoint" → used Moment.js, skipped Zod validation, wrote a unit test instead of an integration test. *Each mistake traces to missing context, not a weak model.*
- **Prompt engineering vs context engineering.** Prompt engineering phrases one request well (one input, one interaction). Context engineering designs *everything the model sees* across the session and the team. Karpathy: "filling the context window with just the right information for the next step."
- **The attention problem.** Every token looks at every other token: n tokens → n × n pairs; at 100k tokens that is 10 billion pairs. Result: a slow decline, not a sudden drop.
- **Context rot.** Symptoms: repeats the same mistake, breaks a rule it agreed to, loses the original goal, code that fit two steps ago. Countermeasures: one session per task, reset between tasks, keep key facts in files, summarise before the window fills, restate key rules each session.
- **Human working-memory parallel:** about four items at once; the budget per item shrinks as context grows.
- **The right-time problem:** present-but-irrelevant context still competes for attention. Load it when the task needs it.
- **Two failure modes:** *too little* (the agent fills gaps with common patterns from training — fine in the abstract, wrong for your system) and *too much* (noise competes for attention; critical lines buried in the middle; slower, costlier, less accurate).
- **Only the user's query is mandatory.** For everything else ask: how often does it improve the output, and what breaks if it is absent? Rarely useful and nothing breaks → load on demand.

## A taxonomy of context components

- **Always on** (loaded before you type; costs tokens every session, so keep it short) vs **on demand** (full skill text, referenced files, retrieved data) vs **custom agents** (same parts packaged under a name: instructions, a chosen model, a restricted tool set).
- **System prompts: precision over volume.** Role and goals, rules, output format. The **"curse of instructions"**: if each rule is followed 95% of the time, all rules are followed 0.95^n — 5 rules → 77%, 10 → 60%, 20 → 36% (Harada et al., 2024). Write rules as testable statements: *when [trigger], the system shall [action].*
- **User input and `@` references:** the request sets the task and its boundary; references pull in exactly the slice you need. Retyping the same context for a recurring task → move it into a rule or skill.
- **Rules, style guides, constraints:** always on; a good rule states its reason ("use date-fns instead of moment.js, because Moment is deprecated and adds 70 KB"). Hierarchy: global preferences → project conventions → file-specific rules.
- **Agent Skills:** an open standard; a reusable package saved with your code that teaches an agent one kind of task. `AGENTS.md` is *always on* (project rules every session); a *skill* is *loaded when needed*. How skills work — **progressive disclosure**: (1) discover: load name + description at startup; (2) decide: load full `SKILL.md` when the task matches; (3) use: open scripts/references/assets only when a step needs them. Or invoke with `/skill-name`.
- **Tools are a context component** (name, parameters, description live in the window and cost tokens on every request; more tools → higher baseline) *and* a way to fetch context. Rule: give a task only the tools it needs; *if a human could not choose between two tools, neither can the agent.* **The model only sees the description** — vague ("reads a file") vs clear (what it does, when to use it, when not to). Anthropic's SWE-bench agent: more time went into tools than the prompt; requiring absolute paths removed a whole class of error.
- **`AGENTS.md`:** a README for agents — one plain Markdown file telling any coding agent how to work on your project. Open format (Agentic AI Foundation / Linux Foundation), 20+ agents, 60k+ projects.
- **Conversation history and memory:** *inside the window* — in-context memory (gone when the session ends, summarised when the window fills); *outside* — long-term memory through files (`PROGRESS.md`, `spec.md`, `tasks.md`), retrieved memory with RAG (searchable index), agent-generated memory (handoff notes).

## Context assembly and discovery

- **The assembly process:** a **fixed part** set before the first message (same in every session) plus what is **added during the session** (files read, test output, tool results, replies). 5,000 tokens of setup leave 5,000 fewer for real work.
- **When an agent ignores a constraint, check in order:** (1) was it loaded? (2) where did it sit — start and end get more attention than the middle; (3) did it stand out? (4) was it contradicted by another rule, tool description or earlier turn? (5) has it been summarised away?
- **Autonomous context discovery:** what you provide (rules, referenced files, system prompts) vs what the agent finds in the codebase before it writes.
  - *Code indexing / semantic search:* matched by meaning; finds related code you did not name; fails on a stale snapshot, mismatched wording, and cannot know what it does not know.
  - *CLI exploration* (`grep -r`, `git log --oneline -20`): best for structural questions, more precise than embeddings; cost — every result stays in the window.
  - *Language servers (LSP):* go to definition, find references, diagnostics; live and symbolic, safer renames; cost — a server per language, confused by runtime-generated code.

## The runtime pipeline and session management

- **The iterative loop** — Reason→Act→Observe, Plan→Execute→Reflect, Think→Do→See — ends when the goal is met, it can't resolve something, or it hits a budget / step limit.
- **Context cost compounds with every call.** Results stay in the window; design tools to return less (the relevant table, a page of results).
- **When to reset a session:** old mistakes return; answers get vague; the window is nearly full.
- **The handoff artifact:** before closing, have the agent write `PROGRESS.md` with three short lists — *Decided / Done / Next*; start the next session from it. Automatic summaries keep the thread but lose detail.
- Raschka: "A lot of apparent 'model quality' is really context quality."

## MCP fundamentals

- **What MCP is:** an open standard that gives LLMs a secure, standardised way to reach external data, applications and services. Introduced by Anthropic in **November 2024**; builds on tool use / function calling. Analogy: a **USB-C port** — one connector instead of a custom cable per device. Solves the **N × M problem** (every model-and-tool pair needing its own connection).
- **Components:** **host** (the AI app containing the LLM, where the user interacts), **client** (inside the host; translates between LLM and server; finds available servers), **server** (the external service supplying data or capabilities). Key idea: *the LLM asks, the client routes, the server acts.*
- **Server features:** resources, prompts, tools.
- **Transport:** messages are **JSON-RPC 2.0**. **stdio** for local resources (a local process started with a command); **SSE** / **Streamable HTTP** for remote endpoints.
- **Benefits:** reduced hallucinations (a clear route to reliable external sources), increased utility and automation, easier connections.
- **Security:** user consent and control; data privacy; **tool safety** (tools can run code — do not trust tool descriptions from unverified servers; ask permission before a tool runs); secure output handling; supply-chain security; monitoring and auditing. The spec says MCP *cannot enforce these at the protocol level* — they fall to the host, the server author and the user.

## Required readings

- **Liu et al. 2023, *Lost in the Middle*.** Multi-document QA and key-value retrieval. Accuracy is highest when the relevant passage is at the **start or end** of the prompt and drops when it is in the **middle** (a U-shaped curve). Longer windows raise the ceiling, not the floor. The single most important fact behind context *management* rather than context *stuffing*.
- **Anthropic Engineering, *Effective context engineering for AI agents* (Sept 2025).** Introduces **context rot**; argues for **just-in-time retrieval** over pre-loading; three techniques for long-horizon work — **compaction, structured note-taking, sub-agent architectures**; system-prompt "altitude"; tool-set design. First-party engineering writing, not a controlled study.
- **MCP specification and announcement.** Hosts, clients, servers; resources, prompts, tools; JSON-RPC transport; security and trust. A tool's description and schema are part of the model's context — writing them well *is* context engineering; descriptions from an untrusted server are untrusted input.
- **Reference (recognise the idea):** RAG (Lewis 2020 — knowledge in an index, not weights), MemGPT (context window as RAM, external storage as disk), RULER (advertised vs reliable context length differ), context-engineering survey, Agentic Context Engineering (the context itself is what gets optimised).

---

[Back to the study guide index](README.md)
