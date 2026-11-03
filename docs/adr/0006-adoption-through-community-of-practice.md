# 0006 — Adopt AI-DLC through evidence-led pilots and a community of practice, not a Center of Excellence

- **Status:** Accepted
- **Date:** 2026-09-18
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook defines how to roll out AI-DLC in three waves and how people learn it ([Chapter 11](../../playbook/11-learning-paths.md#the-enablement-program-three-waves)). It did not say how the organization earns stakeholder commitment, how it explains the ideas to people outside the pilot, where innovation happens, or who looks after the practice once the enablement quarter ends. Chapter 11 asked for a signed pilot charter but no template existed.

Organizations usually fill that gap in one of three ways: a top-down mandate with licenses for everyone, a Center of Excellence (CoE) that owns the standards and approves teams' adoption, or a voluntary community of practice alongside a platform team. The choice decides whether adoption spreads by persuasion or by compliance, and whether the practice keeps improving after the people who launched it move on.

The playbook already gives the paved road and the merging of steering changes to the platform pod ([Chapter 02](../../playbook/02-ways-of-working.md#scaling-beyond-one-pod)), and already warns against big-bang rollout and enablement as a one-off event.

## Decision

We will recommend that AI-DLC is adopted through evidence-led pilots, each governed by a signed pilot charter, and sustained by a voluntary community of practice with rotating coordination and a champions network, which contributes to the paved road through normal PRs and holds no approval authority.

In practice: the new [Chapter 12](../../playbook/12-adoption-strategy.md) sets out five workstreams (innovate, adopt, socialize, buy in, community); the [pilot charter](../../standards/pilot-charter-template.md) and [community of practice charter](../../standards/community-of-practice-charter-template.md) templates join `standards/`; adoption and community metrics join the [metrics reference](../../standards/metrics-reference.md#adoption-and-community); "community of practice" enters the Chapter 01 vocabulary as the replacement for the CoE.

## Options considered

### Option A — Evidence-led pilots plus a community of practice  ← chosen

- Pros: buy-in is tied to agreed, measurable criteria; the practice scales with the number of practitioners rather than the size of a central team; skeptics are engaged in public rather than overruled; innovation is channelled through an experiment register instead of scattered.
- Cons: slower to show org-wide coverage than a mandate; depends on protected time for champions and the coordinator, which is the first thing cut under delivery pressure; the community's health has to be actively measured.

### Option B — Top-down mandate

- Pros: fast, visible coverage; simple to announce and budget.
- Cons: produces tool usage without the process change; usage becomes the metric; objections go underground.
- Rejected because: it reproduces the "AI-assisted Scrum" plateau the method exists to avoid, and the metrics it naturally generates are the ones the metrics reference forbids.

### Option C — Center of Excellence with approval authority

- Pros: consistent standards; a clear owner; familiar to PMO and governance functions.
- Cons: approval becomes a queue; the CoE owns both the standard and the gate and so cannot scale with the number of pods; teams route around it.
- Rejected because: the playbook already puts standards ownership in the platform pod and governs steering by PR, not committee. A CoE would add a second, slower authority over the same artifacts.

## Consequences

- Positive: Wave 1 has a concrete output template; stakeholder concerns are recorded and answered once; experiments and their kills are visible; community health has definitions.
- Negative: leaders must fund time budgets for champions and a coordinator that do not show up as delivery; the quarterly review may produce an "extend" or "stop" recommendation that is politically awkward, which is the point.
- Follow-ups: seed an FAQ and narrative in the steering repo during the first Wave 1; add an experiment register file to the platform pod's steering repo scaffold.

## Revisit when

The first two pilots have reached their quarterly review, or steering contributors outside the platform pod stay below a quarter of all contributors for two consecutive quarters, or the organization's governance function requires a formal approval body for AI tooling.
