# Week 1 — Setup Environments

**Estimated time: ~2–3 hours.**

## Overview
Before we can practice AI-augmented software engineering, everyone needs a working
**coding agent** and a clean development environment. This week is pass/fail setup:
get your tools installed, verified, and ready to use for Week 2.

If you already use a coding agent (Claude Code, Cursor, GitHub Copilot, etc.), you
may keep it. **If you do not have one, you will set up Google Antigravity backed by a
free Gemini student account** (steps below).

## Learning goals
- Have a functioning coding agent you can invoke from your editor and/or terminal.
- Understand the difference between chat, inline completion, and agentic modes.
- Establish the Git + GitHub workflow we'll use all semester.
- Use GitHub CLI to open a pull request that improves shared course materials.

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

## Part 3 — Improve course materials with GitHub CLI

This week you will practice the Git workflow we will use all semester by proposing a
small improvement to the course materials.

### Install GitHub CLI

Install the GitHub CLI (`gh`) and authenticate:

```bash
# macOS
brew install gh

# Windows (via Winget)
winget install GitHub.cli

# Linux
# Visit https://github.com/cli/cli#installation

gh auth login
```

Follow the prompts and make sure `gh auth status` confirms you are logged in.

### Clone the course repo

```bash
git clone https://github.com/scottyUX/AI-Augmented-Software-Engineering.git
cd AI-Augmented-Software-Engineering
```

### What to improve

Read through **2-3 assignment files** in the `assignments/` folder. Pick one small
improvement that would make an assignment clearer for future students. Good options:

- Add a clarifying example.
- Fix confusing wording.
- Add a helpful resource link.
- Improve formatting.
- Suggest a better test case.
- Add a tip or common mistake to watch for.

Use your coding agent if helpful, but you are responsible for reviewing the final
change and making sure it is accurate.

### Create a branch, commit, and open a PR

Create a feature branch:

```bash
git checkout -b improve-assignment-clarity
```

Make your edit to the assignment file(s), then commit with a clear message:

```bash
git add assignments/
git commit -m "Clarify assignment requirements for better student understanding

- Rewrote confusing section about expected output
- Added example showing what not to do
- Fixed typo in code snippet"
```

Push your branch and open a PR:

```bash
git push -u origin improve-assignment-clarity
gh pr create \
  --title "Improve clarity in Assignment 2" \
  --body "Explains what I improved and why it helps future students."
```

After you submit, the instructor will review the PR. If it is useful and correct,
your suggestion may be merged into the official course materials.

## Submission
Your pull request appears on the course repo. The instructor will review it there.

## Evaluation (pass/fail, 20 pts)
- 10 — PR opened against the course repo from a feature branch.
- 10 — Improvement is thoughtful, scoped, and improves assignment clarity.

## Notes
- Tool links and student-verification flows change often; if a link or step has moved,
  find the current equivalent and **document what you actually did** in your writeup —
  adapting to changing tooling is part of being AI-native.
