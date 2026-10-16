# Week 3 Writeup — Inside a Coding Agent

**Name:** AYMENsl25
**Gemini CLI version (`gemini --version`):** 0.64.0
**OS / shell:** Windows + PowerShell
**Model(s) seen in trace:** `gemini-3.5-flash-lite` only
**Session commit:** `51756f4` (agent changes and trace); `79c3272` is a separate post-session boundary-test follow-up

> Evidence tags: `[OBSERVED]` = cite a timeline line, call number, or diff hunk.
> `[INFERRED]` = say what you're reasoning from.

---

## Part I — Session

**Narrative (one paragraph):** [OBSERVED] One prompt asked Gemini to read `TASK.md`, plan, and complete it. It first announced a reading phase and read the task (response #1), then inspected pricing, cart, requirements, tests, and catalog (responses #2–5). Its first `python -m pytest` could not find pytest in the shell environment; it installed `requirements.txt` and reran the tests (response #4). It announced an implementation phase (#6), made three `replace` calls to cart, pricing, and tests (#7–9), ran the full suite (#10), announced completion (#11), and answered (#12). The trace recorded five temporary `503` API errors that were retried; no tool call failed. The agent's suite ended at 18 passing tests. After the session, I independently ran the tests and added two boundary cases in a separate commit; the expanded suite has 20 passing tests.

| Metric | Value |
|---|---|
| User prompts | 1 (`session_timeline.txt`, summary) |
| Model calls | 12 successful responses; 5 retried API errors |
| Tool calls (failed) | 16 (0) |
| Final `pytest` result | Agent session: 18 passed; independent post-session check: 20 passed after two extra tests |
| Did you step in? When / what? | No extra prompt during the recorded session; the trace has one user prompt. Tool approvals are shown as decisions, not user prompts. |

---

## Part II — System prompt annotation

### Outline
1. Core Mandates — security, context economy, engineering quality, and progress updates.
2. Available Sub-Agents — when and how to delegate.
3. Available Agent Skills — available specialist instructions.
4. Hook Context — how to treat external hook text.
5. Primary Workflows — research, strategy, implementation, and validation.
6. Operational Guidelines — tone, safety, and tool behavior.
7. Interaction Details — CLI help and feedback commands.
8. Git Repository — restrictions on staging, committing, and pushing.

### Annotations (≥6)
#### Section: Tone and Style (tone and verbosity)
> "Aim for fewer than 3 lines of text output ... per response whenever practical." (`prompts/system.md`, line 183)
- **Behavior it produces:** Brief progress messages in the CLI.
- **Failure it prevents:** Long conversational replies drowning out the actionable information.

#### Section: Engineering Standards (when not to act / confirm)
> "If asked *how* to do something, explain first, don't just do it." (`prompts/system.md`, line 51)
- **Behavior it produces:** Distinguishes a request for advice from authorization to edit files.
- **Failure it prevents:** Changing code when the user only wanted an explanation.

#### Section: Development Lifecycle (workflow)
> "Research -> Strategy -> Execution" and "Plan -> Act -> Validate" (`prompts/system.md`, line 144)
- **Behavior it produces:** Reads and tests before making targeted changes, then verifies the result.
- **Failure it prevents:** Guessing at a fix without reproducing or checking it.

#### Section: Tool Usage (tool usage)
> "Do NOT make multiple calls to the `replace` tool for the SAME file in a single turn." (`prompts/system.md`, line 206)
- **Behavior it produces:** Serializes edits to one file.
- **Failure it prevents:** Two edits racing against different versions of the same file.

#### Section: Security & System Integrity
> "Never log, print, or commit secrets, API keys, or sensitive credentials." (`prompts/system.md`, line 6)
- **Behavior it produces:** Treats credentials and `.env` files as protected.
- **Failure it prevents:** Accidentally publishing an API key in the Git repository.

#### Section: Context Efficiency
> "Prefer using tools like grep_search to identify points of interest instead of reading lots of files individually." (`prompts/system.md`, line 24)
- **Behavior it produces:** Searches for relevant code before opening files.
- **Failure it prevents:** Filling the model's context with unrelated code and increasing the cost of later calls.

### Context injection (`GEMINI.md`)
[OBSERVED] The exported built-in prompt does not contain "All money is integer" (`prompts/system.md`). The first user-role model input extracted from the trace does: `submission/session_context.md` lines 37–41 show `# Project context`, the integer-cents rule, and the `python -m pytest -q` instruction from `run/GEMINI.md`. Thus the project file entered through session context, separate from the built-in system instructions.

---

## Part III — Tool design

### Inventory
| Category | Tools | Used in session (count) |
|---|---|---|
| File | `read_file`, `write_file`, `replace`, `list_directory` | `read_file` 7, `replace` 3 |
| Search | `glob`, `grep_search` | None |
| Shell | `run_shell_command`, `list_background_processes`, `read_background_output` | `run_shell_command` 3 |
| Web | `google_web_search`, `web_fetch` | None |
| Planning and narration | `update_topic`, `enter_plan_mode` | `update_topic` 3 |
| Delegation | `invoke_agent`, `activate_skill` | None |
| Other | `ask_user` | None |

[OBSERVED] These 16 declarations are in `submission/session_tools.md`, captured from the session's model-visible tool schemas. The usage counts come from `session_timeline.txt`.

### Tool A: `replace`
- **Source file:** [Gemini 3 declaration](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L355) and [implementation](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/edit.ts).
- **Schema:**
  ```
  replace({file_path: string, instruction: string, old_string: string,
           new_string: string, allow_multiple?: boolean})
  ```
- **Why each parameter:** `file_path` selects the target. `instruction` states the intent for review and possible edit correction. `old_string` supplies exact content to match. `new_string` supplies exact replacement content. `allow_multiple` explicitly permits replacing more than one match.
- **Description line that corrects a model mistake:** > "Do not use omission placeholders like '(rest of methods ...)'" ([declaration](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L395)). **Mistake:** Giving a partial replacement that deletes omitted code.
- **Deliberately does not:** Guess which occurrence to edit when `old_string` is ambiguous and `allow_multiple` is false. This protects unrelated code.

### Tool B: `run_shell_command`
- **Source file:** [Windows-aware declaration](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L36) and [implementation](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/shell.ts).
- **Schema:**
  ```
  run_shell_command({command: string, description?: string, dir_path?: string,
                     is_background?: boolean, delay_ms?: integer,
                     additional_permissions?: object})
  ```
- **Why each parameter:** `command` is the exact program to execute. `description` explains it to the user. `dir_path` selects an existing workspace directory. `is_background` and `delay_ms` support long-running processes. `additional_permissions` exists only when tool sandboxing is enabled and requests needed access.
- **Description line that corrects a model mistake:** > "Exact command to execute as `powershell.exe -NoProfile -Command <command>`" ([declaration](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts#L124)). **Mistake:** Writing Bash-only syntax in a Windows shell command.
- **Deliberately does not:** Silently run the command in an arbitrary directory; `dir_path` must already exist within the workspace. A modifying command also needs user confirmation in the default approval mode.

### Why old/new string edits?
[INFERRED] Exact matching limits edits to text the model actually saw and keeps diffs small enough to review. The one-match default forces a retry rather than choosing an ambiguous occurrence. [OBSERVED] Responses #7–9 each led to one successful `replace` call, and the session commit shows focused changes in three files. No ambiguous-string failure happened in this trace, so that safeguard was not exercised.

### Per-model tool descriptions
For `replace`, the [Gemini 3 description](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L355) is concise and emphasizes surgical edits. The [legacy description](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L349) gives a longer checklist: read the file first, match exact whitespace, include surrounding context, and use small atomic calls. The interface is similar, but the older model receives more explicit guardrails against imprecise edits.

---

## Part IV — Behavioral analysis

### 1. The loop
```text
#1 read TASK.md + update_topic → #2 pytest + read cart/pricing
→ #3 read requirements/tests → #4 install requirements + pytest
→ #5 read catalog → #6 update_topic → #7 replace cart.py
→ #8 replace pricing.py → #9 replace test_cart.py
→ #10 pytest → #11 update_topic → #12 final response
```
[OBSERVED] The agent decided it had completed the task: response #11 marked “Task Completion,” and response #12 was its final answer. The five `503` errors caused retries between these calls but did not end the session (`session_timeline.txt`).

### 2. Context growth
| Call | Input tokens | Cached tokens |
|---:|---:|---:|
| 1 | 11,677 | 0 |
| 2 | 12,284 | 10,147 |
| 3 | 13,556 | 10,136 |
| 4 | 14,436 | 2,024 |
| 5 | 15,559 | 0 |
| 6 | 16,137 | 12,149 |
| 7 | 18,270 | 14,185 |
| 8 | 20,896 | 0 |
| 9 | 22,992 | 0 |
| 10 | 26,196 | 22,336 |
| 11 | 26,959 | 24,364 |
| 12 | 27,283 | 0 |

[OBSERVED] These values come from `submission/session_calls.csv`. Input grew from 11,677 to 27,283 tokens as the task, file contents, test output, tool results, and edits accumulated. [INFERRED] A nonzero cached count means a repeated part of the prompt was reused rather than freshly processed; caching can lower cost and latency for that reused prefix. It does not mean the session stopped growing.

### 3. Planning
[OBSERVED] Gemini used `update_topic` three times: “Reading Task Requirements” after response #1, “Implementing Fixes and Shipping Rules” after #6, and “Task Completion” after #11. It did not call `enter_plan_mode` or `write_todos` (the latter was not in the 16 tool declarations). This follows the system prompt's Topic Updates guidance (`prompts/system.md`, lines 52–61). The implementation matched the announced scope: fix item quantity, discount-before-tax, shipping, and tests. The environment detour—installing requirements after pytest was unavailable—was not in the initial topic update.

### 4. Error recovery
> "No module named pytest"

[OBSERVED] The first `run_shell_command` was `python -m pytest` after response #2, and its output in the raw local trace contained this error. After response #4, Gemini called `pip install -r requirements.txt && python -m pytest -q`, then continued reading catalog code. That recovered well enough to make progress, although the cleaner setup would have been to activate the assignment's `.venv` before launching Gemini. Later, five API `503` failures were retried automatically; they were service errors, not failed tool calls (`session_timeline.txt`).

### 5. The tests
[OBSERVED] Gemini edited only the expected values and comments in three existing `Cart.total()` tests, which `TASK.md` expressly permits for shipping. For example, the session commit changes `assert cart.total() == 2160` to `assert cart.total() == 2759  # 2000 + 8% tax ($160) + $5.99 shipping (599 cents)` in `run/tests/test_cart.py`. It did not weaken the quantity or discount tests; instead it fixed the code and added four shipping tests. [OBSERVED] The agent's new cases missed the exact 5,000-cent boundary and a discount that crosses below it. I added those two cases after the recorded session in commit `79c3272`, separate from the agent commit. The expanded suite passes 20/20.

### 6. Models
[OBSERVED] Every `model` field in `submission/session_calls.csv` is `gemini-3.5-flash-lite` (12 responses). Calls #6 and #7 used the most thinking tokens, 2,004 and 2,003, respectively. They bracketed the move from reading files to the implementation topic and the first edit; [INFERRED] the agent was deciding how to apply the fixes and shipping rule. [INFERRED] The assignment describes an unpinned default that uses a smaller router model and a larger work model. A smaller router can make routing faster and cheaper, while the larger model may improve difficult coding decisions at greater latency and cost. Pinning `-m gemini-3.5-flash-lite` kept this trace to one model, so the default two-model behavior was not observed here.
