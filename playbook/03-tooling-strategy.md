---
owner: platform-enablement
audience: developers, architects
reviewed: 2026-09-02
review-cadence: quarterly
---

# 03 — Tooling Strategy

Tooling strategy for AI-DLC has one goal: **maximize the quality of context flowing to agents and the quality of validation flowing back**. This chapter sets Claude Code as the primary development agent, defines the context-engineering artifacts every repo must carry, and gives criteria for evaluating alternatives so the strategy outlives any single tool.

## The stack at a glance

| Layer | Standard | Purpose |
|---|---|---|
| Primary development agent | **Claude Code** | Plan-mode elaboration, agentic construction, review support |
| Steering / context | `CLAUDE.md` + skills + domain docs | Encode standards once, apply on every task |
| Repo & CI | GitHub + GitHub Actions | Source of truth, automation ([Chapter 07](07-devops-automation.md)) |
| Work tracking | Jira, integrated with GitHub | Units of Work, Bolts, traceability ([Chapter 08](08-github-jira.md)) |
| Prototyping platform | Snowflake (+ alternatives) | [Chapter 05](05-rapid-prototyping.md) |
| Docs | Markdown in git | [Chapter 09](09-documentation-standards.md) |
| Integrations | MCP servers | Agents reach Jira, Snowflake, AWS, observability |

## Why a primary agent (instead of letting everyone pick)

Standardizing on one primary agent is not about the tool being best at everything; it's that **steering artifacts, skills, and pod practices compound only when shared**. A CLAUDE.md tuned over six months is an organizational asset. Ten developers on ten tools produce zero shared assets. Choose one primary, allow personal secondaries, and review the choice annually against the evaluation criteria below. The decision of record is [ADR 0002](../docs/adr/0002-claude-code-as-primary-agent.md).

## Claude Code: the operating pattern

### Steering files (`CLAUDE.md`)

Every repo carries a `CLAUDE.md` — the standing instructions an agent loads on every session. It encodes: build/test commands, architecture summary and pointers to the domain model, coding standards, security constraints, and definition of done. Start from the [template](../standards/claude-md-template.md).

Rules of thumb:

- **Short and dense beats long and complete.** Aim under ~150 lines; link out to deeper docs rather than inlining them.
- **It's a living artifact.** Every Friday consolidation ([Chapter 02](02-ways-of-working.md)), fold the week's lessons in. If the agent made the same mistake twice, that's a missing steering line.
- **Constraints over descriptions.** "Never write directly to the ledger table; go through `LedgerService`" beats three paragraphs describing the ledger.

### Plan mode = the Bolt plan gate

Claude Code's plan mode maps 1:1 onto AI-DLC's plan-approval gate: the agent explores and proposes a plan while blocked from making changes; the pod approves before generation starts. **Make plan mode the default for any Unit of Work.** Direct execution is for trivial, bounded fixes. The plan the agent produces is captured in the [Bolt plan template](../standards/bolt-plan-template.md) and committed at `docs/bolts/<bolt-id>.md`, so the approved plan and the resulting diff are reviewable side by side.

### Skills

Skills are packaged procedures the agent invokes for recurring tasks. Build a shared skill library (its own repo, versioned) for things like: scaffolding a new service to house standards, generating a threat model from a Unit of Work ([Chapter 06](06-security-shift-left.md)), writing an ADR, producing a Snowflake prototype scaffold. A skill is worth writing when a procedure is (a) repeated, (b) has a right way, and (c) the agent gets it wrong from a cold start. The [skill template](../standards/skill-template.md) defines the anatomy; the [`threat-model` skill](../standards/skills/threat-model/SKILL.md) is the reference implementation to copy from.

### Hooks and permissions

- **Hooks** enforce mechanically what steering requests politely: run linters/formatters after edits, block edits to protected paths (migrations, auth config) without a flag, require tests before a commit skill completes.
- **Permissions**: default deny for destructive commands; pre-approve the read-only and routine commands pods use constantly (test runners, linters) so gates interrupt only when they should.

### Subagents and review

Use a second, context-clean agent session to review the first's diff ("fresh eyes" review) before human review — it reliably catches self-consistent nonsense the generating session can't see. This supplements, never replaces, the human review gate.

### MCP servers

Agents need tool access to be full lifecycle participants. Minimum viable set: **GitHub** (PRs, issues), **Jira** (Units of Work in/out), **Snowflake** (prototyping), **AWS** (docs/IaC), plus your observability stack for Operations-phase work. Treat MCP server configuration as part of repo onboarding, and review each server's permissions like you'd review a service account's.

## The context-engineering hierarchy

When agent output disappoints, fix context in this order — cheapest first:

1. **The prompt / Unit of Work** — was intent actually unambiguous?
2. **CLAUDE.md** — is a standing rule missing or stale?
3. **Skills** — is this a recurring procedure that deserves packaging?
4. **Domain docs** — does `docs/domain/` actually describe the bounded context? ([Chapter 04](04-architecture.md))
5. **The codebase itself** — inconsistent code teaches the agent inconsistency. Refactoring for clarity is now also agent-performance work.

## Model selection and token economics

Model choice is a per-task engineering decision, like picking an instance type — and the leverage-to-cost ratio differs sharply by AI-DLC phase. The principles below are stable; the current model names and prices live in the [model selection reference](../standards/model-selection.md), which is dated and reviewed quarterly because pricing goes stale in months while this logic doesn't.

### Match the tier to the task

| Task type | Tier | Why |
|---|---|---|
| Mob Elaboration, Bolt planning, architecture proposals | **Frontier** — the strongest model you can buy | A wrong plan wastes a pod-day; this is the worst place to economize. Plan quality compounds through everything downstream. |
| Code/adversarial review, threat-model drafts, incident investigation | **Frontier** | Validation quality is the throughput limit ([Chapter 02](02-ways-of-working.md)); never downgrade the reviewer below the generator. |
| Routine construction inside an approved plan | **Mid-tier** | The plan carries the intelligence; execution against it is well-bounded work. Escalate to frontier when the task fights back. |
| Bulk mechanical work: characterization-test generation ([Chapter 10](10-legacy-modernization.md)), scanner-finding triage, CI chores, doc sweeps, changelog drafts | **Small/fast** | High volume, low ambiguity, verified mechanically afterward. Volume pricing dominates here. |

Two standing rules:

1. **The review side never runs on a cheaper model than the generation side.** An expensive generator checked by a cheap reviewer inverts the whole validation economics of AI-DLC.
2. **Escalation beats pre-optimization.** Start routine work on the default mid-tier; escalate the session to frontier the moment output needs repeated correction. Two rounds of fixing cheap output costs more — in tokens *and* pod attention — than starting expensive.

### Unit economics: cost per validated Unit of Work

The metric that makes model spend governable is **cost per validated Unit of Work** — tokens + warehouse credits + CI minutes, rolled up per Unit via the [Jira traceability chain](08-github-jira.md). Not cost per seat, not cost per token: those numbers make the *expensive plan that prevented a wrong build* look wasteful and the *cheap agent that generated three days of rework* look efficient, which is exactly backwards.

This is the bridge to FinOps: pods see their own unit economics (showback per pod, per month), leadership budgets tokens the way it budgets cloud spend ([Chapter 11](11-learning-paths.md), Wave 1), and token-spend anomalies are an operational signal like any other cost anomaly ([Chapter 07](07-devops-automation.md)). Classic FinOps practices don't yet cover agent tokens — the playbook's position is: treat them as a first-class cloud cost with the Unit of Work as the allocation unit, rather than inventing a parallel process.

## Evaluating alternatives

Tool-agnostic criteria — score 1–5, review annually or when a pod escalates:

| Criterion | What to look for |
|---|---|
| Steerability | Persistent project instructions, plan/approve workflow, hookable lifecycle |
| Agentic depth | Multi-file, test-running, self-correcting execution — not just completion |
| Context handling | Large-codebase navigation, controllable context, subagent isolation |
| Integration | MCP or equivalent; CI usability (headless mode) |
| Governance | Permissions, audit logs, enterprise auth, data-handling guarantees |
| Model quality | Frontier-model access on your code's languages |

Current field notes: **Amazon Q Developer** — strongest for AWS-native shops and holds a specific niche in [legacy transform](10-legacy-modernization.md); **Kiro** — AWS's spec-driven IDE, philosophically closest to AI-DLC's plan-first stance, worth piloting; **GitHub Copilot** — ubiquitous completion plus improving agent mode, weakest steering story; **Cursor** — strong IDE UX, popular as a personal secondary. Any of these can be the primary if it wins on the criteria — the strategy is the criteria, not the brand.

## Anti-patterns

- **Tool sprawl.** Five agents, no shared steering, no compounding. Pick a primary.
- **Stale CLAUDE.md.** Worse than none — the agent confidently follows outdated rules. Assign ownership (the pod's domain anchor).
- **Prompt libraries as strategy.** Prompt collections rot instantly; steering files and skills are versioned, reviewed, and attached to the repo where they act.
- **Unbounded permissions for convenience.** One `rm -rf` story ends your rollout. Expand the allowlist deliberately, never wholesale.
- **Paying for seats, skipping enablement.** Tool licenses without the [learning program](11-learning-paths.md) yields Copilot-as-autocomplete usage patterns and disappointing metrics.

## Tips & tricks

- **Version steering artifacts like code**: PRs, reviews, CHANGELOG. A steering regression is a production regression waiting to happen.
- **Give the agent the *why*.** Steering lines with rationale ("use X because Y") generalize; bare rules get misapplied at the edges.
- **Headless agent in CI** for mechanical chores (changelog drafts, doc-link checks, first-pass PR review comments) — but CI agents comment, humans merge.
- **Watch your token economics** per Unit of Work, not per seat — an expensive plan that prevents a wrong build is the cheapest thing you bought all week. Details and the current tier table: [model selection reference](../standards/model-selection.md).

## References

- Previous: [Chapter 02 — Ways of Working](02-ways-of-working.md) · Next: [Chapter 04 — Architecture](04-architecture.md)
- Templates: [CLAUDE.md starter](../standards/claude-md-template.md)
- [Claude Code docs](https://docs.claude.com/en/docs/claude-code) · [Model Context Protocol](https://modelcontextprotocol.io)
