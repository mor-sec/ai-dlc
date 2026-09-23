# 0012 — Assign models by use case across four tiers, with effort as the first cost lever

- **Status:** Accepted
- **Date:** 2026-09-03
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; recorded retroactively on 2026-09-23 for commit 7a1f25b

## Context

The [model selection reference](../../standards/model-selection.md) had three tiers and listed the top one as "Opus 5 (Fable 5 where available)". Once a frontier-plus model shipped with materially different constraints (a data-retention requirement, turns that can run many minutes, a refusal stop reason), that entry no longer described a real choice. Pods also had no guidance on effort settings, although on the current generation effort changes cost as much as a change of tier and does not throw away the prompt cache.

Assigning models per tier also left the real question unanswered: which model and effort for a threat-model pass, a Bolt plan, a nightly doc sweep. Pods were deciding case by case, and cost varied between pods with no explanation.

## Decision

We will name four tiers by role (frontier-plus, frontier, mid-tier default, small/fast), assign every AI-DLC use case to a tier and an effort level in one table, and make effort the first lever when spend is high.

Standing rules added: effort before model; caches are model-scoped, so escalation means a new session; judge cost per completed task, not per request; non-interactive work goes through the Batch API; frontier-plus needs governance clearance first ([ADR 0010](0010-vendor-governance-for-the-primary-agent.md)). The reference records relative cost multipliers with a date, not absolute prices, and its change log records how many steering fixes each change needed. Current model names live only in the reference, which is reviewed quarterly.

## Options considered

### Option A — Four role-named tiers, per-use-case table with effort  ← chosen

- Pros: every pod makes the same choice for the same task; effort guidance cuts cost without a tier change; organizations under zero-retention terms can map the table with one substitution.
- Cons: a larger table to keep current; effort levels are judgement calls that need revisiting as models change.

### Option B — Keep three tiers and let pods choose per task

- Pros: simple; flexible.
- Cons: frontier-plus constraints are hidden inside the frontier tier; cost varies by pod habit rather than by task.
- Rejected because: the retention constraint alone makes frontier-plus a governance decision, not a per-task preference.

### Option C — One model for everything

- Pros: no selection overhead; one cache; one eval target.
- Cons: frontier cost on volume work, or mid-tier judgment on plans and threat models.
- Rejected because: the use cases differ by orders of magnitude in volume and in the cost of a wrong answer.

## Consequences

- Positive: spend is explainable per use case; the escalation path is written down; tier changes are gated by [steering evals](../../standards/steering-evals.md) ([ADR 0007](0007-steering-evals-gate-steering-changes.md)).
- Negative: the reference goes stale by design and needs a quarterly owner; the first eval run against a tier change was still pending when this was decided.
- Follow-ups: the first steering-eval run at the next tier change; cost per validated Unit in the [metrics reference](../../standards/metrics-reference.md).

## Revisit when

A provider changes its effort controls or pricing structure enough that effort is no longer the cheaper lever, a tier is added or retired, or showback data shows pods regularly overriding the table for the same use case.
