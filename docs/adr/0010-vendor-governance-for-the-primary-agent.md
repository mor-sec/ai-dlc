# 0010 — Govern the primary-agent vendor with recorded data terms, a written degraded mode, and an annual review agenda

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; recorded retroactively on 2026-09-23 for commit b5ede75

## Context

[ADR 0002](0002-claude-code-as-primary-agent.md) standardizes on one primary agent, which concentrates risk in one vendor and one model family. Its only mitigation was a governance row in the Chapter 03 evaluation table and a promise to re-score annually. Nothing said what data leaves the perimeter, what pods do when the agent is down, how a model deprecation is absorbed, or what the annual review actually examines.

Every prompt carries code, documents, ticket text, and whatever the agent reads. That makes data-handling terms a precondition for adoption, not something to look at after a pilot.

## Decision

We will require, before any pilot starts, an ADR recording the provider's data-retention terms, where inference runs, and which repos are excluded from agent access; a written degraded mode for outages; model changes gated by the steering evals; and a fixed agenda for the annual review.

Zero-retention or enterprise no-training terms are the requirement. In an outage, the pod's approved secondary agent becomes primary for the day with the same steering, and plan gates still apply. No model-tier change merges without a green [steering eval](../../standards/steering-evals.md) run ([ADR 0007](0007-steering-evals-gate-steering-changes.md)). The annual review re-scores the field, reads the availability and incident log, re-confirms data terms, counts steering fixes caused by model changes, and checks the fallback drill ran. Its output amends or supersedes ADR 0002. Detail: [Chapter 03, Vendor governance](../../playbook/03-tooling-strategy.md#vendor-governance).

## Options considered

### Option A — Recorded terms, degraded mode, eval-gated model changes, fixed review agenda  ← chosen

- Pros: the organization knows its exposure before it depends on the vendor; outages cost a slower day rather than a stopped one; switching cost is measured rather than guessed.
- Cons: a fallback drill and an annual review take time that shows no delivery; the secondary agent must stay good enough to use.

### Option B — Multi-vendor by default

- Pros: no single point of failure; bargaining power.
- Cons: shared steering and skills stop compounding, which is the reason ADR 0002 chose one primary.
- Rejected because: it trades a governable concentration risk for guaranteed tool sprawl.

### Option C — Leave vendor risk to procurement and legal

- Pros: no engineering effort; those functions own contracts already.
- Cons: procurement sees the contract, not the repos excluded from agent access, the fallback drill, or the cost of a model deprecation.
- Rejected because: most of the risk is operational, and only engineering can measure it.

## Consequences

- Positive: data-handling questions from security and legal have a recorded answer; the first model deprecation is a measured event, not a quarter of rework.
- Negative: pilots cannot start until the data-terms ADR exists; some model tiers stay unavailable to organizations whose terms rule them out.
- Follow-ups: the data-terms ADR in each adopting organization; a yearly fallback drill; the availability log.

## Revisit when

The primary vendor changes its data-handling or retention terms, an outage longer than one working day occurs, or the organization adopts a second primary agent for any class of work.
