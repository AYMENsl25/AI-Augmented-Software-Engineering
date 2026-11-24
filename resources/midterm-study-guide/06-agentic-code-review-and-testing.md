# Week 6 — Agentic Code Review and Testing

Slides: [`lectures/06-agentic-code-review-and-testing/`](../../lectures/06-agentic-code-review-and-testing/) · Readings: [`resources/06-agentic-code-review-and-testing/papers-to-read.md`](../06-agentic-code-review-and-testing/papers-to-read.md)

The lecture's question: *the agent wrote the code — how do we know it is correct?* This is the Test stage of the SDLC, after Plan, Design and Implement.

## Why verification matters

- **Agent-generated work is growing fast.** Agent-authored PRs on GitHub went from ~7.7M in January to ~71.7M in August 2026 (~9×). More changes means more work to verify.
- **Delivery gains are real** (Faros AI, 22,000 developers, two years of telemetry, lowest vs highest AI adoption): +16.2% PR merges, +33.7% task throughput, +66% epics completed per developer.
- **Quality costs rise too:** code churn +861%, incidents per PR +242.7%, bugs per developer +54%. These are *observational* figures: they show association, not causation, and churn can include useful refactoring.
- **Review capacity is under pressure:** median time in review +441.5%; **+31.3% PRs merged with no human or agent review**.

## The verification bottleneck

- **The bottleneck has moved** (Theory of Constraints; Osmani 2026). AI makes producing code cheap; reading speed and accountability do not scale at the same rate, so the constraint shifts to *verification*.
- **Why manual review doesn't scale:** 5 PRs a day → ~1 hour per review; 25 PRs a day → ~5 minutes and "LGTM". *A rubber stamp is not a safety net. It is the illusion of one.*
- **The verification stack — five layers**, each assuming the ones below are running. Cheap and fast at the bottom (catch the most); slower and pricier at the top:
  1. **L1 Deterministic guardrails** — linters, types, tests, scanners: a hard yes or no.
  2. **L2 LLM-based review** — architecture fit, spec alignment, security intent.
  3. **L3 Deploy-time safety** — feature flags, canaries, blue-green: limit the blast radius.
  4. **L4 Runtime safety** — observability, anomaly detection, AI incident analysis.
  5. **L5 Focused human review** — intent and fit: is this the right thing to build?
- **The two big questions.** *Before merge:* how do you know this code is safe to ship? *After merge:* how fast can you tell production has broken, and fix it?
- **Harness validations and self-check loops.** The agent runs your gates (lint → types → tests → build, e.g. one `ci` script) *before* it opens a PR. A failing test becomes an observation the agent can act on (reason, act, observe, adjust).

## Layer 1 — Deterministic guardrails

Fast, automatic, same answer every time. Pick the checks your project's risk needs (internal tool: secrets scanning and tests; public API: contracts and dependency scanning).

| Check | Why it matters for AI code | Example tools |
| --- | --- | --- |
| Lint and format | Each agent session writes in a slightly different style; linters catch unused variables, un-awaited promises | Prettier, gofmt; ESLint, Ruff |
| Dead code and unused dependencies | Agents abandon an approach and leave its code and packages behind | Knip, vulture |
| Type checks | Models get the shape right but **invent methods and fields** | TypeScript strict, mypy, pyright |
| Test suite | When one agent writes the code *and* its tests, "all green" is worth less. **Coverage theater:** 100% line coverage, zero behaviour verified. Ask "are they checking behaviour?", not "do they pass?" | — |
| **Mutation testing** | Changes the code (e.g. `>=` → `>`). *Killed* = a test went red; *survived* = no test checked that logic. Slow: run on touched files; hold a score on payments, auth, core logic | Stryker, PIT, mutmut; Meta's LLM-generated mutants |
| **Property-based testing** | Agents handle the cases you describe and miss the ones you don't. Good properties sound like laws: `decode(encode(x)) == x`, money is conserved, running twice = running once | Hypothesis, fast-check |
| SAST | Models learned from public code, much of it insecure (SQL injection → use parameterised queries; XSS, unsafe deserialisation, path traversal) | Semgrep, SonarQube |
| Dependency, secrets, IaC scanning | Agents pick packages from memory and hardcode keys to get unblocked; a public S3 bucket "works" in every demo | Trivy, Gitleaks, Checkov |
| **Architecture fitness functions** | Tests for *structure*, not behaviour: "domain must not import infrastructure", no circular dependencies. The wiki rule becomes a failing build | dependency-cruiser, ArchUnit |
| Performance and query budgets | Agents add more than they delete and write the naive query (the **N+1 query**: 101 queries vs one join) | Lighthouse CI, benchmark gates |
| Accessibility and i18n | AI frontend code skips labels and alt text and hardcodes English | axe; a lint rule for hardcoded strings |
| PR size and scope | Ask for one feature, get 2,000 lines. No human meaningfully reviews 2,000 lines; one logical change per PR (Google, *Small CLs*) | A bot that flags large PRs |

## Layer 2 — LLM-based review

- **Deterministic gates say** the code is well-formed (a hard yes or no). **An LLM reviewer asks** whether it does the right thing (an opinion — it can be wrong). It can run locally (fresh session), on the PR (a bot), or in the cloud (a managed service).
- **Adversarial review before the PR.** The agent that just wrote the code is a poor judge of it — it mostly agrees with itself (**sycophancy**). Use a **fresh session with a hostile brief** ("assume it has bugs"), and ideally a **different model**.
- **How it works:** inputs are the diff, surrounding files and PR text / ticket / spec; output is line comments plus a one-line summary. Tools (CodeRabbit, Copilot code review, Claude Code GitHub Actions, PR-Agent) turn over fast: *chase the capability, not the product*.
- **Two ways to organise it:** a team of specialists (security, performance, architecture… plus a coordinator — sharp focus, higher cost) vs **a single reviewer with a checklist — start here**; specialise only where it pays off (usually security).
- **What to look for:** correctness and fit (architecture, every acceptance criterion and nothing extra, meaningful tests), risk and compliance (OWASP Top 10 and LLM Top 10, PII, cost), completeness and hygiene (docs, leftover debug code). LLM security review *backs up* SAST; it is weak at tracing data across many files.
- **Tuning the reviewer:** a reviewer prompt with role, concrete conventions ("money is integer cents"), past incidents, what *not* to review, and a fixed output format (`file:line, blocker | warning | nit`, verdict). *Every wrong comment is an edit to this file* — context engineering aimed at the reviewer.

## Layer 3 — Safe deployment strategies

- **Feature flags as the default.** Deploy dark (flag off), release while watching, turn off instantly with no new deploy. **Deployment and release become two decisions.** Watch for *flag debt*.
- **Blue-green:** two copies of production; flip the router to the new one, flip back on trouble. Instant way back, but a hidden bug reaches everyone at once.
- **Canary:** 1% → 5% → 25% → 100%, checking errors and latency at each step. Slower, but a bug reaches only a small slice.
- **Progressive delivery by segment:** internal → beta cohort → one region → everyone (most to least forgiving).
- **SLO and error budget:** an SLO is a health target as a number (99.9% of requests succeed); the error budget is the 0.1% of failures you allow. **Automated rollback** when a deploy burns the budget too fast.
- **Data safety: you can roll back code, not data.** Rename a column in three steps — **add** (new column, copy data) → **switch** (code uses the new column; still reversible) → **remove** (weeks later; no way back).

## Layer 4 — Runtime safety and AI-powered ops

- **Three pillars:** logs (timestamped events), metrics (numbers over time), traces (one request across services). **OpenTelemetry:** vendor-neutral — instrument once, send anywhere, readable by an agent.
- **Error budgets drive decisions:** budget to spare → ship fast; budget gone → stop and fix stability. **Reduce alert fatigue:** symptom-based alerts ("checkout is failing", not "CPU at 80%"), burn-rate alerts, multiwindow (Google SRE Workbook).
- **The "AI SRE":** detect (anomaly detection — mature), compare (post-deploy analysis — emerging), analyse (root cause, drafts a timeline, *a human confirms*), triage (dedupe, ticket with repro steps, route to owner).
- **Closing the loop:** production error → AI SRE files evidence → coding agent drafts a fix *plus a regression test* → Layers 1–2 → human approves → ships behind a flag / canary. *Every escape leaves a new test behind.* Fully hands-off is still aspirational.

## Layer 5 — The human in the loop

- **Two mechanisms decide what needs a human:** (1) a **deterministic path gate** — changes to protected paths (`payments/**`, `auth/**`, `migrations/**`, `infra/**`, `.github/workflows/**`) or risky content (`DROP`/`DELETE`, credential shapes) *always* get a human; it only catches dangers you can name in advance. (2) an **AI risk scorer** for the rest — low → automerge; medium, high or unsure → human.
- **The risk scorer must fail safe:** when unsure, round up to a human. It weighs blast radius, reversibility, test coverage, diff size and fragile files. **It can add a human; it can never override the gate.**
- **How human review is changing:** from line by line (null checks, off-by-ones) to **intent and fit**. Route to the right human (`CODEOWNERS`). **Review the reviewer:** log every override — humans forcing reviews the scorer waved through means it is too loose; humans merging what it flagged means it is crying wolf.

## Putting it together

- **Reference pipeline:** seconds (local harness loop, Layer 1 gates on every PR) → minutes (fresh-session LLM review, path gate + risk scorer) → rationed human time (domain reviewer only if routed) → hours (flag off → canary + SLO watch → 100%). *Cheap checks first; human attention last.*
- **Adopt bottom up:** (1) deterministic gates — about a week; (2) one checklist LLM reviewer; (3) risk scoring and routing, once you trust the gates and reviewer; (4) AIOps, which needs instrumentation, SLOs, flags and a fix path first.
- **Metrics for the system itself** (they trade against each other): PR cycle time ↓, escape rate ↓, revert rate ↓, false-positive rate ↓, human time per PR ↓. *The trap:* automerge everything and cycle time hits zero while escapes and reverts spike.
- **Failure modes that look like success:** bot fatigue, rubber stamping (payments change approved in 12 seconds), alert flood, flag debt, ignored findings, AI overconfidence.
- **The trust ladder:** rung 1 shadow mode (it suggests, a human decides — **start here**) → rung 2 advisory (enforces rules you wrote) → rung 3 autonomous on low-risk paths → rung 4 autonomous on critical paths (**default: no**). Move up when the metrics earn it; move down the moment they don't.
- **Takeaways:** the bottleneck moved; cheap checks first; layers lean on each other; humans judge intent. *The human stays in the loop, just not in front of every diff.*

## Readings (background)

- **Alshahwan et al. 2024, *Automated Unit Test Improvement using Large Language Models at Meta* (TestGen-LLM).** The model proposes tests; a generated test is kept *only if* it builds, passes reliably and increases coverage — "assured" LLM-based SE. *The model proposes, deterministic filters decide.* "Builds and passes" is necessary, not sufficient.
- **Frömmgen et al. 2024, *Resolving Code Review Comments with Machine Learning* (Google).** A model proposes the edit that resolves a *human* reviewer's comment; the human stays the source of judgment. An industry experience report: acceptance rate is the honest metric, and *where* the suggestion appears in the workflow changes its usefulness.
- **Reference (recognise the idea):** EvalPlus (tests are a weaker oracle than they look), LLM-as-a-Judge (known judge biases), SWE-bench (real GitHub issues as a benchmark), Sharma et al. 2023 on **sycophancy**.

---

[Back to the study guide index](README.md)
