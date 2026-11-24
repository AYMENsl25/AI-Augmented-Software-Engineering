# Week 3 — Inside a Coding Agent: Dissecting Gemini CLI

**Estimated time: ~2.5 hours.**

## Overview
You've been using coding agents as a black box. This week you open one up.
[**Gemini CLI**](https://github.com/google-gemini/gemini-cli) is a production coding agent
whose source is **open (Apache 2.0)**. That means you can read its real system prompt,
read its tool code, and record every model call it makes.

You'll run Gemini CLI on a small, deliberately buggy repo, capture a full telemetry trace,
and take it apart: the system prompt, the tools, the agent loop, and how context grows.

You build almost nothing. The work is **observing carefully and backing every claim with
evidence**.

## Learning goals
- See the **agent loop** concretely: one user message → many model calls and tool calls.
- Read a production **system prompt** and explain what each part is for.
- Understand **tool design**: schemas, descriptions, and deliberate limits.
- Watch **context grow** across a session, measured in tokens.

---

## What's in this folder
```
gemini-cli-dissection/
├── assignment.md        # this file
├── writeup.md           # template you copy into work/ and fill in
├── tools/summarize_log.py  # turns a raw telemetry log into a timeline + token table
├── starter/             # the repo the agent works on — don't fix it yourself!
│   ├── TASK.md          # what you'll ask the agent to do
│   ├── GEMINI.md        # project context file the agent loads
│   ├── .gemini/settings.json  # turns on local telemetry
│   ├── shopcart/        # small Python library (has bugs on purpose)
│   └── tests/
└── work/                # YOU create this; everything you submit goes here
```

> **Don't read the `shopcart/` code closely or fix anything before Part I.** The point is
> to watch the agent find and fix the problems. You'll analyze the code afterwards.

---

## Setup (~25 min)

### 1. Fork the course repo and make a branch
You'll submit this lab as a **pull request** to the course repo. It won't be merged; the
PR *is* your submission, and it's practice for the PR workflow you'll use for the rest of
the course.

1. On GitHub, **fork** https://github.com/scottyUX/AI-Augmented-Software-Engineering
   to your account.
2. Clone your fork and create a branch:
   ```bash
   git clone https://github.com/<your-username>/AI-Augmented-Software-Engineering.git
   cd AI-Augmented-Software-Engineering
   git checkout -b week3-<your-username>
   cd assignments/03-anatomy-of-coding-agents/gemini-cli-dissection
   ```

> Forks of a public repo are public, and so is your PR. To keep your personal email off
> your commits, turn on GitHub's **"Keep my email addresses private"** setting and use
> your `@users.noreply.github.com` address
> (`git config user.email <id>+<username>@users.noreply.github.com`).

> **Windows users:** run every command in this lab in **Git Bash** (it comes with Git for
> Windows, which you installed in Week 1), opened as a tab in **VS Code's terminal** or **Windows
> Terminal**. Don't use the standalone Git Bash window: Gemini CLI's interactive screen
> doesn't work well there. The commands below are bash, and most of them **won't work in
> PowerShell or cmd** as written. If you must use PowerShell, see
> [PowerShell equivalents](#appendix-powershell-equivalents) at the end of this file.
> If Git Bash says `python: command not found` and your Python came from Miniconda, run
> `conda init bash` once and reopen the terminal.

### 2. Install Gemini CLI (pinned version)
Gemini CLI needs **Node.js 20 or newer** (`node --version`). If you don't have it,
install the LTS version: `brew install node` (macOS), `winget install OpenJS.NodeJS.LTS`
(Windows, then reopen your terminal), or download it from https://nodejs.org.
```bash
npm install -g @google/gemini-cli@0.64.0
gemini --version   # record this in your writeup
```
Use the **exact pinned version**. The system prompt and tools change between releases, and
your answers have to match the version you analyzed.

### 3. Get a free Gemini API key and sign in with it
Gemini CLI signs in with an **API key**. Since June 18, 2026, it no longer accepts
"Sign in with Google" for personal accounts. That includes the Google AI Pro student plan,
which fails with *"This client is no longer supported for Gemini Code Assist for
individuals."* The free API key works fine, and you don't need a credit card.

**Get the key (~2 min):**
1. Go to https://aistudio.google.com/apikey and sign in with a **personal** Google
   account. University accounts may have AI Studio turned off.
2. Accept the terms if asked, then click **Create API key**. If it asks for a project,
   let it create a default one.
3. Copy the key, which starts with `AIza…`. Treat it like a password.

**Use it:**
```bash
export GEMINI_API_KEY="AIza...your key..."
gemini
```
- When Gemini CLI asks how to authenticate, choose **Use Gemini API key**. If you tried
  Google sign-in before, type `/auth` inside Gemini CLI to switch.
- Type `/quit` once you reach the input prompt.
- `export` lasts only for the current terminal. Run it again in every new terminal before
  `gemini`. You can also add the line to `~/.zshrc` or `~/.bashrc`, which live in your home
  folder and are **not** in the repo.

**Use `gemini-3.5-flash-lite` for this lab.** Start Gemini CLI with
`gemini -m gemini-3.5-flash-lite` every time (the commands below already do). The free tier
has tight limits, set **per model**:

| Model | Free-tier limit (approx.) |
|---|---|
| `gemini-3.8-flash` (the CLI's default) | 20 requests **per day** |
| `gemini-3-flash-preview` | 20 requests per day, 5 per minute |
| `gemini-3.5-flash-lite` | 250,000 input tokens per minute; enough for this lab |

One agent session uses about **20–25 requests**, so the default model can run out halfway
through. Gemini 2.5 models don't work with new API keys.

- **`429` / "exhausted your daily quota":** switch models. Type `/model` inside Gemini CLI,
  or restart with `-m <model>`. A short "retrying after 30s" message is normal; wait for it.
- **`503` / "high demand":** temporary. Gemini CLI retries automatically.
- **Check your usage:** https://ai.dev/rate-limit. Limits reset daily (midnight Pacific).
- On the free tier, Google may use your prompts to improve its products. That's fine for
  this starter repo, but don't paste anything private into the agent.

> **Never commit your API key.** Don't put it in any file inside the repo, including
> `TASK.md`, `GEMINI.md`, notes, or a `.env` in your working copies. If a key ever gets
> pushed, delete it at https://aistudio.google.com/apikey immediately and create a new one.

### 4. Make your working copy
Never run the agent in `starter/` itself. Work in a copy under `work/`, so your PR shows
exactly what the agent changed. From the `gemini-cli-dissection/` folder:
```bash
mkdir -p work/prompts work/submission
cp -r starter work/run
cp writeup.md work/writeup.md
git add work && git commit -m "Week 3: add working copy of starter"
```

### 5. Create a Python virtual environment
Still in `gemini-cli-dissection/`:
```bash
python -m venv .venv
source .venv/bin/activate        # Windows (Git Bash): source .venv/Scripts/activate
python -m pip install -r starter/requirements.txt
```
`.venv/` is already gitignored, so it won't end up in your PR.

> **Activate the environment in every new terminal before starting `gemini`**
> (`source .venv/bin/activate` from `gemini-cli-dissection/`). The agent's shell commands
> inherit your environment. Without it, the agent's `python -m pytest` fails with
> `No module named pytest`, and that noise ends up in your trace.

Check that the tests fail before the agent touches anything:
`(cd work/run && python -m pytest -q)`.

**Commit after every step below.** The agent's work then shows up as its own commit in
your PR, so the reviewer can see exactly what it changed. Your writeup can cite that
commit.

### 6. Export the real system prompt
```bash
cd work/run
GEMINI_WRITE_SYSTEM_MD=../prompts/system.md gemini -m gemini-3.5-flash-lite
```
When Gemini CLI asks whether to **trust this folder**, say yes. If the folder isn't
trusted, the CLI ignores `.gemini/settings.json` and nothing gets logged. Type `/quit` as
soon as it starts. `work/prompts/system.md` now holds the built-in system prompt for your
CLI version. Clear the log this short session wrote, then commit:
```bash
rm -f ../telemetry.log
git add ../prompts && git commit -m "Week 3: export Gemini CLI system prompt"
```

---

## Part I — Capture a session (15 pts)
In `work/run/`, start `gemini -m gemini-3.5-flash-lite` and send **exactly** this prompt:

```text
Read TASK.md and complete all of it. First write out your plan, then carry it out without waiting for my confirmation.
```

Rules, so everyone's sessions are comparable:
- **Approve** tool calls when asked. Don't use `--yolo`.
- **Don't help.** Type nothing else unless the agent is truly stuck for 3+ turns. If you
  step in, record exactly what you typed and when; it's part of your data.
- When the agent says it's done, run `python -m pytest -q` yourself, then `/quit`.

Save the results and commit the agent's changes (still in `work/run/`):
```bash
python ../../tools/summarize_log.py ../telemetry.log --out ../submission/session_timeline.txt --csv ../submission/session_calls.csv --system ../submission/session_system.md
git add . ../submission && git commit -m "Week 3: Gemini CLI session (agent's changes)"
```

> The raw `work/telemetry.log` contains your account email and full prompt payloads. It's
> written outside `run/` on purpose, so the agent can't search its own trace, and it's
> already gitignored; **never force-add it.** Commit only the generated files above, and
> quote short excerpts in your writeup.

In `writeup.md`: your CLI version, a one-paragraph narrative of the session, the counts
(user prompts, model calls, tool calls, failed tool calls), whether the final tests passed,
and any time you stepped in.

## Part II — System prompt annotation (25 pts)
Use `prompts/system.md`, and `submission/session_system.md` if it was captured.

1. **Outline.** Split the prompt into its sections and give each a one-line label.
2. **Annotate at least 6 sections.** For each one: *what behavior it produces* and *what
   failure it prevents*. Quote the specific line or lines. You must include:
   - one section about **tone and verbosity**,
   - one about **when not to act, or when to ask or confirm** (safety and destructive actions),
   - one about **workflow** (understand → plan → implement → verify),
   - one about **tool usage**.
3. **Context injection.** Is `GEMINI.md`'s content in the exported `system.md`? If not,
   where and how does it reach the model? Show evidence from the trace, or point to the
   source file and line in the Gemini CLI repo. (You'll go deep on context files in Week 4.
   Here, just find where the content enters.)

## Part III — Tool design (25 pts)
The tool source is in **Gemini CLI's GitHub repo**, not this course repo. Use the
`v0.64.0` tag so the code matches the version you ran:
- Schemas and descriptions the model sees:
  [`packages/core/src/tools/definitions/`](https://github.com/google-gemini/gemini-cli/tree/v0.64.0/packages/core/src/tools/definitions)
- Per-model description sets:
  [`definitions/model-family-sets/`](https://github.com/google-gemini/gemini-cli/tree/v0.64.0/packages/core/src/tools/definitions/model-family-sets)
- Tool implementations:
  [`packages/core/src/tools/`](https://github.com/google-gemini/gemini-cli/tree/v0.64.0/packages/core/src/tools) (e.g. `edit.ts`, `shell.ts`)

The copy that `npm` installed is a minified bundle and isn't readable. To browse locally
instead, run `git clone --depth 1 --branch v0.64.0 https://github.com/google-gemini/gemini-cli.git`
somewhere **outside** your course repo.

1. **Inventory.** Run `/tools` in the CLI. List every built-in tool and group them as
   **file** (read/write/edit), **search** (find files or text), **shell** (run commands,
   background processes), **web**, **planning and narration** (e.g. `update_topic`,
   `enter_plan_mode`), **delegation** (sub-agents, skills), or other. Which ones did your
   session actually use, and how many times each?
2. **Compare two tools in depth.** Pick two that work very differently. Suggested pair: the
   file-edit tool (`replace`) and `run_shell_command`. Where to look for those two:

   | | `replace` | `run_shell_command` |
   |---|---|---|
   | Name and parameter names | [`base-declarations.ts` L64–69](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L64-L69) | [`base-declarations.ts` L56–58](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/base-declarations.ts#L56-L58) |
   | Description + schema the model sees | [`gemini-3.ts` L356](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/gemini-3.ts#L356) | [`dynamic-declaration-helpers.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/dynamic-declaration-helpers.ts) (`getShellToolDescription` L36, `getShellDeclaration` L85); differs on Windows vs Mac/Linux |
   | Older-model version (for Q4) | [`default-legacy.ts` L349](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L349) | [`default-legacy.ts` L338](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/definitions/model-family-sets/default-legacy.ts#L338) |
   | What runs when it's called | [`edit.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/edit.ts) (`EditToolInvocation` L460, `validateToolParamValues` L1176) | [`shell.ts`](https://github.com/google-gemini/gemini-cli/blob/v0.64.0/packages/core/src/tools/shell.ts) (`ShellToolInvocation` L102, `validateToolParamValues` L1220) |

   For each tool:
   - Reproduce its **parameter schema** and justify every parameter.
   - Quote one line of its **description** that exists to stop a specific model mistake,
     and name that mistake.
   - State something the tool deliberately **does not** do, and why.
3. **Design question.** Why does the edit tool take an exact **old string / new string**
   instead of line numbers or a whole new file? Give two reasons, and point to a moment in
   your trace where it mattered (or explain why it never came up).
4. **Per-model tool descriptions.** `definitions/model-family-sets/` has more than one
   version of the tool descriptions (e.g. `gemini-3.ts` vs `default-legacy.ts`). Diff one
   tool across the two. What changed, and why would an agent describe the same tool
   differently to different models?

## Part IV — Behavioral analysis (25 pts)
Answer from your trace. **Tag every claim `[OBSERVED]`** (cite a line in
`session_timeline.txt`, a call number, or the session commit's diff) **or
`[INFERRED]`** (say what you're reasoning from).

1. **The loop.** Draw the actual loop for your session (e.g. `call#1 → read_file → call#2 →
   …`). What ended it: the agent deciding it was done, a limit, or you?
2. **Context growth.** Chart `input_token_count` per call from `session_calls.csv`
   (any tool; include the image or a table). Why does it grow? What does
   `cached_content_token_count` tell you, and why does caching matter for cost and speed?
3. **Planning.** How did the agent plan and track its progress: in plain text, with the
   `update_topic` tool (which splits the work into named phases), with `write_todos`, or by
   entering plan mode? Check the system prompt's "Topic Updates" section. Did the plan match what it actually did? Point to where it
   departed from the plan.
4. **Error recovery.** Find the first failure (a failing test run, a failed tool call, or a
   wrong fix). Quote it, then describe exactly what the agent did next. Was the recovery
   good?
5. **The tests.** Did the agent edit any existing test? Was each edit allowed by
   `TASK.md`? Quote the diff.
6. **Models.** You ran everything on `gemini-3.5-flash-lite`. Confirm it from the `model`
   field. Then use the `thoughts` column (`thoughts_token_count` in `session_calls.csv`):
   which calls had the most "thinking", and what was the agent deciding at those points?
   Without `-m`, Gemini CLI's default setup uses **two** models: `gemini-3.5-flash-lite` to
   route each request and `gemini-3.8-flash` to do the work. Why would a CLI split the job
   this way, and what would you expect to change (speed, cost, quality) if the whole session
   ran on a bigger model? (Connects to the lecture's model landscape.)

---

## Deliverables: open a pull request
Everything you submit lives in `gemini-cli-dissection/work/`:
1. `writeup.md`, with every `TODO` filled in.
2. `prompts/system.md`.
3. `submission/`: `session_timeline.txt`, `session_calls.csv`, and `session_system.md`
   (if captured).
4. `run/` with the agent's changes committed as their own commit.
5. Your context-growth chart (image file or table in the writeup).

**Before you push**, check for leaks and redact any hits like this: `[REDACTED: email]`.
```bash
git grep -niE "AIza|@gmail|@ucsc|email|api[_-]?key" -- work   # searches only files git tracks
git grep -nE "/Users/|/home/|C:\\\\Users\\\\" -- work      # your home-folder path and username
git status --ignored work | grep telemetry   # must show as ignored, never staged
```
The exported `system.md` lists your home-folder paths and every agent skill installed on
your machine. Redact your username (e.g. `/Users/[REDACTED]/...`); the rest can stay.

**Open the PR:**
1. `git push -u origin week3-<your-username>`
2. On GitHub, open a pull request from your fork's branch **into
   `scottyUX/AI-Augmented-Software-Engineering:main`**.
3. **Title:** `Week 3: <Your Name>`
4. **Description:** one or two sentences on the most surprising thing you found, the
   final `pytest` result of the agent's session, and a link to `work/writeup.md` on your
   branch.
5. **Submit the PR link** on Canvas. The PR won't be merged; it's your submission.
   Leave it open. You can keep pushing fixes until the deadline.

**Only touch `work/`.** Don't edit `starter/`, `tools/`, or any other file in the
course repo. The "Files changed" tab of your PR should show only `work/`.

## Evaluation (100 pts)
- 10 — Pull request: opened against the course repo; only `work/` changed; one commit per
  step with clear messages; descriptive title and body; no raw logs or leaked identifiers.
- 15 — Part I: clean session capture, correct counts, narrative.
- 25 — Part II: accurate outline; ≥6 well-evidenced annotations; context-injection answer.
- 25 — Part III: complete inventory; two tool analyses grounded in source; design question;
  per-model comparison.
- 25 — Part IV: every answer evidenced and tagged; context-growth chart.

Claims without evidence get no credit, even if they're true.

## Appendix: PowerShell equivalents
Use these only if you can't use Git Bash. Run them from the same folders as the bash
versions.

| Step | PowerShell |
|---|---|
| Make working copy (Setup 4) | `New-Item -ItemType Directory -Force work\prompts, work\submission`<br>`Copy-Item -Recurse starter work\run`<br>`Copy-Item writeup.md work\writeup.md` |
| Python environment (Setup 5) | `python -m venv .venv`<br>`.venv\Scripts\Activate.ps1`<br>`python -m pip install -r starter\requirements.txt` |
| Export system prompt (Setup 6) | `$env:GEMINI_WRITE_SYSTEM_MD = "..\prompts\system.md"; gemini; Remove-Item Env:GEMINI_WRITE_SYSTEM_MD` |
| Delete the log | `Remove-Item -Force ..\telemetry.log` |
| Leak check (Deliverables) | `git grep -niE "AIza\|@gmail\|@ucsc\|email\|api[_-]?key" -- work`<br>`git grep -nE "/Users/\|/home/\|C:\\Users" -- work`<br>`git status --ignored work` (`telemetry.log` must be listed as ignored) |

- **Always run the `Remove-Item Env:...` part.** A `$env:` variable stays set for the
  rest of the PowerShell session. A leftover `GEMINI_WRITE_SYSTEM_MD` would rewrite
  `system.md` every time you start `gemini`.
- If `gemini` fails with *"running scripts is disabled on this system"*, run
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or run `gemini.cmd`
  instead.
- In Windows PowerShell 5.1, `&&` doesn't exist. Run chained commands one at a time.

## References
- Gemini CLI source: https://github.com/google-gemini/gemini-cli
- System prompt export (`GEMINI_WRITE_SYSTEM_MD`):
  https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/system-prompt.md
- Telemetry: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/telemetry.md
- Built-in tools: https://github.com/google-gemini/gemini-cli/tree/main/docs/tools
- Inspired by Stanford CS146S, Week 1 ("Trace Dissection of a Claude Code Session").
