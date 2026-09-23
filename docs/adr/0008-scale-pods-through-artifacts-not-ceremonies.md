# 0008 — Scale beyond one pod through the context map and a platform pod, not coordination ceremonies

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; recorded retroactively on 2026-09-23 for commit d4fb29a

## Context

[Chapter 02](../../playbook/02-ways-of-working.md) described one pod and [Chapter 11](../../playbook/11-learning-paths.md#the-enablement-program-three-waves) described rollout waves, but nothing covered ten pods working at once. At that scale the failure mode changes: not a tired reviewer but a coordination layer that grows back. A weekly cross-pod sync, then a dependencies board, then a release train, each reasonable alone, together reproduce Scrum of Scrums, the meetings AI-DLC removed.

The playbook already had the artifacts pods could coordinate through: the context map with one owner per bounded context, and the schema registry as the contract between contexts ([ADR 0005](0005-ddd-and-event-driven-architecture.md)). Shared steering and the paved road still had no owner.

## Decision

We will scale AI-DLC by having pods coordinate through artifacts: the context map decides ownership, the schema registry sequences cross-context work, a platform pod owns the paved road as a product, shared steering changes by PR, and the only org-level ritual is a biweekly 45-minute context-map review.

A Unit that needs another context's event becomes two Units, the producer's and the consumer's, with the published schema as the handoff. Pods stay two or three people; growth means more pods and more contexts. The detail is in [Chapter 02, Scaling beyond one pod](../../playbook/02-ways-of-working.md#scaling-beyond-one-pod).

## Options considered

### Option A — Artifacts plus a platform pod  ← chosen

- Pros: coordination scales with the number of contexts rather than with meeting hours; cross-pod friction points at the context map, where it can be fixed; the paved road has an accountable owner.
- Cons: depends on the context map being accurate and kept current; the platform pod is a standing cost that does not deliver features.

### Option B — A scaled-agile framework (Scrum of Scrums, release trains)

- Pros: familiar to PMOs; established training and tooling.
- Cons: planning cadences measured in weeks around work measured in hours; dependencies managed by conversation rather than by contract.
- Rejected because: it re-imposes the iteration overhead that Bolts replaced, and hides boundary problems that the context map would expose.

### Option C — Grow pods instead of adding them

- Pros: fewer seams between teams; no new coordination at all.
- Cons: mob work stops working past three people; one pod's context load grows past what a session can hold.
- Rejected because: the pod size is the method's unit of review and context. A bigger pod is a different method.

## Consequences

- Positive: one cross-pod meeting in total; ownership questions have a single answer in the repo; steering improvements from any pod reach every pod within a week.
- Negative: an out-of-date context map now causes coordination failures, not just documentation debt; organizations must fund a platform pod before they feel they need one.
- Follow-ups: platform pod charter and intake process; a check that every context in the map has exactly one owner.

## Revisit when

Pods repeatedly need a mid-Bolt conversation to sequence cross-context work despite a current context map, or the platform pod's steering review time regularly exceeds a week.
