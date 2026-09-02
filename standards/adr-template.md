---
owner: platform-enablement
audience: developers, architects
reviewed: 2026-09-02
review-cadence: quarterly
---

# ADR Template

Copy into `docs/adr/NNNN-short-title.md` (sequential number). One decision per ADR. The agent drafts during the Bolt; a human approves; the decision exists when the ADR merges. Context: [Chapter 04](../playbook/04-architecture.md#architecture-decisions-adrs).

Statuses: `Proposed → Accepted | Rejected`, later possibly `Superseded by NNNN` or `Deprecated`. Never edit an accepted ADR's substance — supersede it.

---

```markdown
# NNNN — <Decision as a short assertive title, e.g. "Use EventBridge for cross-context events">

- **Status:** Proposed | Accepted | Rejected | Superseded by [NNNN](NNNN-x.md)
- **Date:** YYYY-MM-DD
- **Deciders:** <named humans — an agent is never a decider>
- **Unit of Work:** <Jira key>

## Context

What forces are at play? The problem, the constraints (technical, organizational,
cost), and why a decision is needed now. 2–4 paragraphs maximum. Write it so a
reader (or agent) with no memory of this month understands the situation.

## Decision

"We will <decision>." One sentence, active voice, no hedging.
Then the essential how — a paragraph or a short list, not a design doc.

## Options considered

### Option A — <name>  ← chosen
- Pros: …
- Cons: …

### Option B — <name>
- Pros: …
- Cons: …
- Rejected because: <the actual reason, not a platitude>

## Consequences

- Positive: what gets easier.
- Negative: what gets harder, what debt is accepted, what we're betting on.
- Follow-ups: <Jira keys for work this decision creates>

## Revisit when

The trigger that should reopen this decision (a scale threshold, a vendor event,
a date). ADRs with no revisit trigger quietly become dogma.
```

---

**Why ADRs matter doubly under AI-DLC:** agents read the ADR log before planning ([Chapter 03](../playbook/03-tooling-strategy.md)) — a good log stops them relitigating settled questions or silently violating them; a missing log means every session re-decides your architecture from scratch.
