# Agentic Codebase Structure

Slides: [`lectures/04-agentic-codebase-structure/`](../../lectures/04-agentic-codebase-structure/) · Readings: [`resources/04-agentic-codebase-structure/papers-to-read.md`](../04-agentic-codebase-structure/papers-to-read.md)

The lecture's framing: a repository can be *designed for agents*. Each mechanism has a definition, types, how it works, anatomy and examples. Know which mechanism to reach for and, above all, **which ones merely guide the model and which ones actually enforce**.

## Skills

- **A skill teaches an agent how to perform a specific task.** Three parts: instructions (a repeatable procedure), resources (scripts, references, templates), storage (files tracked with the project). Open standard supported by multiple agents.
- **Types** (origin, location and invocation are separate axes): built-in or custom; project or user; automatic (selected by relevance) or explicit (`/skill-name`); nested project skills.
- **How they work:** discover → select (by name and description) → read (the skill's instructions enter context) → use resources (supporting files load when needed). `/skill-name` attaches to one message; a Custom Mode lasts the session.
- **Anatomy** (`.cursor/skills/add-endpoint/SKILL.md`): frontmatter (`name`, `description`), procedure (the body), supporting files (`scripts/`, `references/`, `assets/`). Optional fields: `paths`, `disable-model-invocation`.
- **Examples:** add-endpoint, fix-bug (reproduce, add a regression test), deploy-app, file-specific skill. *The lab skills prescribe a test-first procedure; they do not enforce compliance.*

## Rules

- **Rules supply reusable instructions in the agent's context:** project knowledge, relevant context, shared guidance. **A rule guides the model. It does not execute a check.**
- **Types:** project rules (`.cursor/rules/*.mdc`), user rules (personal, across projects), team rules (managed in a dashboard), `AGENTS.md` (plain Markdown; nested files combine with parent instructions).
- **How rules load:** always (every session), intelligent (agent selects by description), file-scoped (a matching file is in context), manual (`@rule-name`).
- **Anatomy** (`.cursor/rules/api.mdc`): `description`, `globs` (matches files/directories), `alwaysApply`. Project rules require `.mdc`; a plain `.md` in that folder is ignored.
- **Rules vs skills:** rules state constraints and conventions ("keep ticket error bodies consistent") and load always / by files / by relevance / by mention. Skills describe a task procedure ("follow the endpoint workflow"), load when selected or invoked, and can package resources. *Both guide the model. Neither guarantees the result satisfies the instructions.* Keep rules focused; use formatters and linters for mechanical style checks.

## Hooks

- **Hooks run at defined events in the agent's work:** observe (record what happened), act (run a script after an event), control (allow or block supported actions). The host invokes a registered hook when its event occurs.
- **Types:** execution — command-based (runs a program) or prompt-based (a model assesses a condition); event categories — agent events (during a session) and tab/application lifecycle events.
- **How they work:** event → input (host sends event data as JSON on stdin) → execution (the command reads and evaluates it) → response (the host handles the result on stdout).
- **Anatomy** (`.cursor/hooks.json`): the event (`stop` = completion), the `command`, options `timeout` and `loop_limit`. The event determines the script's input and allowed response fields.
- **Examples:** after a file edit → run formatting; before a shell command → check whether it is allowed; after a completed turn → run the validation script; on validation failure → request another attempt with `followup_message`. The lab caps follow-ups at two.
- **Rules vs hooks:** a rule is an instruction the model reads ("do not run `git push`") — compliance depends on the agent following it. A hook is event-triggered execution (a shell-permission hook *rejects* a prohibited command). Coverage and failure settings matter; permissions and access controls are still needed for security boundaries.

## Subagents

- **A subagent handles delegated work in a separate context:** assignment (a bounded task from the parent), separate work (its own instructions and context window), result (a final report to the parent). The parent supplies the relevant information.
- **Types:** built-in (Explore — searches and analyses code; Browser) and custom (project- or user-scoped); **foreground** (parent waits) vs **background** (work continues independently). Task type and execution mode are separate choices.
- **How they work:** assign → work → report → continue. Delegation may be automatic or explicit.
- **Anatomy** (`.cursor/agents/reviewer.md`): identity (`name`, `description`), execution (`model`, `readonly`, `is_background`), instructions (task and expected report, e.g. "return ACCEPT or REVISE with reasons").
- **Examples / patterns:** planner (identify affected files, tests, risks), reviewer (check the diff against requirements and evidence), verifier (run checks, report what passed), parallel investigation (independent questions in separate contexts). A focused assignment and a defined report make the result useful.

## MCP and external tools (as covered in this lecture)

- MCP connects agents to external tools and data through a shared protocol: client (the host's connection), server (exposes capabilities), external system (the underlying data or operation).
- **Connection types:** stdio (local process started with a command), server-sent events, streamable HTTP.
- **How it works:** connect (configure and authenticate) → discover (host receives capabilities) → call (agent selects a tool) → return (tool supplies a result). Cursor asks for tool approval by default.
- **Configuration** (`.cursor/mcp.json`, global `~/.cursor/mcp.json`): a server name inside `mcpServers`; local process = `command`, `args`, optional `env`; remote = `url` with headers/auth.
- **APIs vs MCP vs skills:** an API exposes operations your code calls; MCP is a server exposing capabilities through a common agent protocol; a skill is a task procedure explaining how to complete work with available tools. *A skill can use an MCP tool; that server may call an application's API.*
- Example servers: Jira/Linear (issues), Notion/Confluence (docs), Datadog/Sentry (monitoring), Redshift (databases), Context7 (library docs), Arize (experiment tracking). Choose trusted servers; give each connection only the access it needs.

## Cloud agents

- Environment setup comes before implementation work: configure → install → run.
- Access: secrets via the supported secret store (prefer short-lived identity tokens), network allow-list, avoid dependencies on unreachable services.
- `AGENTS.md` for project orientation (commands, links to testing/debugging notes); skills for detailed procedures. Commit project instructions and skills with the repository. Rules at user, team and repository level — place instructions at the level where they apply.
- Tools: identify required systems, provide connections (tools or MCP servers), allow the needed permissions, verify the agent can use each tool. Improve tools by observing how the agent uses them, finding missed arguments or distracting output, and adjusting the interface.

## Required readings

- **Yang et al. 2024, *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*.** Introduces the **agent-computer interface (ACI)**: the commands, feedback formats and guardrails through which a model acts on a repository. Redesigning the interface *without changing the model* materially changed how often real GitHub issues were resolved. Principles: simple commands, concise feedback, guardrails against common mistakes (e.g. a file viewer that shows a limited window; an edit command that runs a linter and rejects broken edits). *An agent's behaviour is a product of model and interface — you control the interface.*
- **Gloaguen et al. 2026, *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful?*** Controlled comparison of no context file vs LLM-generated vs developer-written. Headline: context files **generally did not improve task success** and raised inference cost by **more than 20%** on average. A context file is context — it competes for the same attention budget, so every line should change a decision the agent would otherwise get wrong.
- **Practitioner companions:** [agents.md](https://agents.md/) format; Anthropic *Agent Skills* (`SKILL.md`, progressive disclosure); Anthropic *Writing effective tools for agents* (fewer, well-scoped tools with descriptions that prevent specific mistakes).
- **Reference (know the one-line finding):** *Agent READMEs* — developers mostly write test procedures and implementation details, rarely security or performance. *Guardrails Beat Guidance* — **negative constraints help, positive directives tend to hurt**, largely independent of topic. *On the Impact of AGENTS.md* — repos with one showed lower median runtime and fewer output tokens (efficiency, not success; partly disagrees with Gloaguen). *Cursor Rules* taxonomy — conventions, guidelines, project information, LLM directives, examples. *Agentless* — a fixed localize/repair/validate pipeline with no autonomous tool use was competitive; harness structure can substitute for agent-discovered structure. *NeMo Guardrails* — programmable, deterministic rails around a model rather than prompt text.
- **Reading principle:** every instruction is a hypothesis about a failure mode. What mistake does it prevent? Is it enforced by code or only stated in prose? What does it cost in tokens? What evidence would show it helped?

---

[Back to the study guide index](README.md)
