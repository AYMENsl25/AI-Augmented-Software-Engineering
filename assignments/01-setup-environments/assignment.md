# Week 1 — Setup Environments

**Estimated time: ~2–3 hours.**

## Overview
Before we can practice AI-augmented software engineering, everyone needs a working
**coding agent** and a clean development environment. This week is pass/fail setup:
get your tools installed, verified, and pushed to a repo so you're ready for Week 2.

If you already use a coding agent (Claude Code, Cursor, GitHub Copilot, etc.), you
may keep it. **If you do not have one, you will set up Google Antigravity backed by a
free Gemini student account** (steps below).

## Learning goals
- Have a functioning coding agent you can invoke from your editor and/or terminal.
- Understand the difference between chat, inline completion, and agentic modes.
- Establish the Git + GitHub workflow we'll use all semester.

---

## Part 1 — Base development environment

1. **Git** — install and configure:
   ```bash
   git --version
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```
2. **GitHub account** — sign up (use your student email) and add an SSH or HTTPS
   credential so you can push. Students: apply for the
   [GitHub Student Developer Pack](https://education.github.com/pack).
3. **A terminal + editor** — VS Code is recommended (Antigravity is a VS Code–based
   editor, so this transfers directly).
4. **A language runtime** for later weeks — install **Python 3.12** (Miniconda/Anaconda
   or `uv` are both fine). Verify:
   ```bash
   python --version
   ```

## Part 2 — Get a coding agent

### Option A — You already have one
Confirm it works: open your editor, start the agent, and have it make a trivial
edit (e.g. add a comment to a file) end-to-end. Note which agent and version you're
using in your writeup.

### Option B — Set up Google Antigravity + Gemini student account
Use this path if you don't already have a coding agent.

1. **Claim a free Gemini / Google AI Pro student plan.**
   - Go to the [Google AI for students offer](https://gemini.google.com/students)
     and sign in with your **student Google account**.
   - Follow the verification steps (student email / SheerID) to activate the free
     plan. This gives you access to the Gemini models Antigravity uses.
2. **Download and install Google Antigravity** (Google's agentic development platform):
   - Get it from [antigravity.google](https://antigravity.google/) and install for
     your OS (macOS / Windows / Linux).
3. **Sign in** to Antigravity with the same Google account you used in step 1.
4. **Verify the agent works.** In Antigravity:
   - Open the **Agent / Agent Manager** panel.
   - Give it a simple task, e.g. *"Create a file `hello.py` that prints Hello,
     AI-native world and run it."*
   - Confirm the agent plans, edits the file, and you can review the result before
     accepting.

> If SheerID/student verification is pending, you can still install Antigravity and
> sign in with a standard (free-tier) Google account to complete the setup task, then
> attach the student plan once it's approved. Note this in your writeup.

## Part 3 — Prove it end-to-end
1. Create a new GitHub repo named `ai-native-week1` (public or private — if private,
   add the instructor as a collaborator).
2. Clone it locally and open it in your editor/agent.
3. Using **your coding agent** (not by hand), have it generate a small program of your
   choice (e.g. a CLI that reverses a string, a FizzBuzz, a temperature converter).
4. Review the agent's output line-by-line, fix anything wrong, then commit and push.

## Deliverables
Submit a link to your `ai-native-week1` repo containing:
1. The small program your agent generated.
2. A `writeup.md` with:
   - Which coding agent you set up (Antigravity + Gemini, or your existing tool) and
     the version.
   - A screenshot of your agent completing a task.
   - The exact prompt(s) you gave it, and any corrections you had to make by hand.
   - **What you learned:** 2–3 sentences on what surprised you about working *through*
     an agent instead of typing the code yourself.

## Evaluation (pass/fail, 20 pts)
- 10 — Working coding agent, demonstrated with a screenshot.
- 5 — Repo set up correctly with the agent-generated program committed and pushed.
- 5 — `writeup.md` complete (agent name/version, prompts, corrections, reflection).

## Notes
- Tool links and student-verification flows change often; if a link or step has moved,
  find the current equivalent and **document what you actually did** in your writeup —
  adapting to changing tooling is part of being AI-native.
