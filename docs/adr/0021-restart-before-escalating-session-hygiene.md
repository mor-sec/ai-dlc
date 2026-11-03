# 0021 — Manage session context deliberately; restart a session before escalating its model

- **Status:** Accepted
- **Date:** 2026-09-29
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook engineers standing context carefully: steering files, skills, domain docs, and the [context-engineering hierarchy](../../playbook/03-tooling-strategy.md#the-context-engineering-hierarchy) for fixing them. It says nothing about the live context of a session. A session accumulates every file it read, every command output, and every failed attempt, and Anthropic's Claude Code guidance names this as the constraint most practice follows from: performance degrades as the context window fills. The same guidance observes that after two failed corrections, the context is cluttered with failed approaches, and a clean session with a better prompt almost always beats continuing.

The playbook's answer to a struggling session was to escalate the model tier ([model selection reference](../../standards/model-selection.md)) and then the pod. That skips the cheapest fix. An escalation carries the same cluttered history into a more expensive model, or throws the history away without writing down what was learned.

Bolts also span sessions: across the Driver rotation at the half-day, across days, and across lanes ([ADR 0019](0019-fan-out-within-one-approved-bolt-plan.md)). Nothing said where the state of a Bolt lives between sessions except in the heads of the people who were there.

## Decision

We will treat a session's context as a managed resource. Pods start a new session between Bolts and unrelated tasks, run broad exploration in subagents, and commit each reviewed slice. When a problem survives two corrections, they restart the session with what was learned before escalating the model tier. The Bolt plan gains a Progress section that any new session resumes from.

The escalation ladder becomes: restart with a better prompt, then a stronger tier in a new session, then the pod. The Bolt plan's stop condition and the model selection reference change to match. Detail: [Chapter 03, Session hygiene](../../playbook/03-tooling-strategy.md#session-hygiene).

## Options considered

### Option A — Session hygiene, restart before escalating  ← chosen

- Pros: the cheapest fix is tried first; what was learned is written into the new prompt instead of buried in a long transcript; the Progress section makes Driver rotation and multi-day Bolts resumable.
- Cons: restarting loses the session's prompt cache; the Driver has to write a good restart prompt, which is a skill.

### Option B — Escalate the tier first, as before

- Pros: one rule, already written; a stronger model sometimes recovers a cluttered session.
- Cons: pays frontier prices to read the clutter; hides a prompt problem behind a model upgrade.
- Rejected because: the escalation rule's own reasoning ("effort before model", [Chapter 03](../../playbook/03-tooling-strategy.md#model-selection-and-token-economics)) says to try the cheaper lever first, and a clean restart is cheaper than a tier change.

### Option C — Leave session management to individual judgement

- Pros: no new rules; experienced Drivers already do most of this.
- Cons: the practice stays with whoever discovered it; new Drivers correct the same session five times.
- Rejected because: the Driver rotates daily, so a practice that lives in one person's habits does not survive the rotation.

## Consequences

- Positive: fewer wasted escalations; Bolts that survive a change of Driver or a day boundary; steering can name what compaction must preserve.
- Negative: one more section to maintain in the Bolt plan; restart prompts are a new thing to review in consolidation.
- Follow-ups: the golden task `stop-on-second-failure` still guards the stop itself; consolidation records note restarts that worked, so the restart-prompt pattern can become a skill if it repeats.

## Revisit when

Consolidation records show restarts rarely resolving what two corrections did not, which would make the extra rung on the ladder a delay rather than a saving; or context windows and compaction improve enough that long sessions stop degrading.
