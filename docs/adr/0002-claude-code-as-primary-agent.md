# 0002 — Standardize on Claude Code as the primary development agent

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

AI-DLC depends on context-engineering artifacts, steering files, skills, hooks, and MCP configuration, that only compound when a whole organization shares them. Ten developers on ten tools produce ten private prompt libraries and zero shared assets. The playbook therefore needs one primary agent, with the choice reviewable against tool-agnostic criteria so the strategy outlives the brand ([Chapter 03](../../playbook/03-tooling-strategy.md#evaluating-alternatives)).

The method also puts hard requirements on the agent: a plan-then-approve workflow that maps onto the Bolt plan gate, persistent project instructions, a hookable lifecycle for mechanical enforcement, subagent isolation for fresh-eyes review, headless operation in CI, and MCP or equivalent for Jira, GitHub, Snowflake, and AWS access.

## Decision

We will make Claude Code the primary development agent for all pods, with personal secondaries allowed, and re-score the choice annually against the Chapter 03 criteria.

Every repo carries a `CLAUDE.md`; skills live in a shared library; plan mode is the default for any Unit of Work; hooks and permissions enforce the security constraints of [Chapter 06](../../playbook/06-security-shift-left.md).

## Options considered

### Option A — Claude Code  ← chosen

- Pros: plan mode maps one-to-one onto the plan gate; `CLAUDE.md`, skills, hooks, and subagents cover the whole steering hierarchy; MCP support; headless CI mode; frontier-model access.
- Cons: terminal-first, which some developers resist; single-vendor dependency on the model side.

### Option B — Kiro (AWS spec-driven IDE)

- Pros: philosophically closest to AI-DLC's plan-first stance; native to the AWS stack most pods deploy to.
- Cons: younger ecosystem for skills and hooks at the time of decision; fewer integration paths outside AWS.
- Rejected because: steering depth and integration breadth decide compounding, and Claude Code led on both. Kiro stays a pilot candidate.

### Option C — GitHub Copilot agent mode

- Pros: ubiquitous, already licensed in many organizations, IDE-native.
- Cons: weakest steering story of the field; plan/approve workflow and lifecycle hooks are thin.
- Rejected because: an agent that cannot be steered per repo cannot carry the method.

### Option D — Let each developer choose

- Pros: no adoption friction.
- Cons: no shared steering, no shared skills, no shared metrics; the enablement program has nothing to teach.
- Rejected because: this is the "tool sprawl" anti-pattern by design.

## Consequences

- Positive: one steering baseline, one skill library, one set of practices to teach; enablement content is reusable across pods.
- Negative: vendor concentration. Mitigated by the annual re-scoring, the tool-agnostic criteria, and the vendor governance section of Chapter 03.
- Follow-ups: steering regression suite (`standards/steering-evals.md`) so that steering survives model and tool changes; annual review recorded as a new ADR or an amendment here.

## Revisit when

The annual scoring shows another tool ahead on steerability and agentic depth combined, or Claude Code loses plan mode, hooks, or headless operation, or the vendor's data-handling terms change materially.
