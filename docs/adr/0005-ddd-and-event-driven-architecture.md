# 0005 — Mandate DDD bounded contexts and event-driven integration for AI-built systems

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

An agent's competence is bounded by its context window and by the clarity of what is in it. Architecture decides how much context a task needs: a Unit of Work that touches one service, one model, and one vocabulary fits in a session; one that threads through six services does not. Agents also amplify whatever inconsistency they see most, so naming drift and implicit coupling degrade agent output faster than they degrade human output ([Chapter 04](../../playbook/04-architecture.md#why-this-architecture-specifically-for-ai-dlc)).

The playbook needed to choose whether to stay architecture-neutral, as most process methodologies do, or to mandate an architectural style because the method's effectiveness depends on it.

## Decision

We will mandate Domain-Driven Design at the strategic level (bounded contexts, context map, ubiquitous language, documented in `docs/domain/`) and event-driven integration between contexts (versioned past-tense events, schema registry, idempotent tolerant consumers), enforced by architecture tests in CI.

Tactical patterns beyond that (event sourcing, CQRS, sagas) are chosen per context where the domain demands them, recorded as ADRs, and otherwise avoided.

## Options considered

### Option A — Mandate DDD + event-driven  ← chosen

- Pros: bounded contexts size Units of Work to agent sessions; the glossary is shared human-agent vocabulary; event schemas are machine-readable contracts agents generate from; loose coupling limits the blast radius of agent mistakes.
- Cons: a learning curve for teams without DDD experience; strategic design work in Inception that feels slow to teams used to starting with CRUD.

### Option B — Architecture-neutral playbook

- Pros: broader applicability; no argument with teams that have an existing style.
- Cons: leaves the biggest lever on agent effectiveness unpulled; every pod rediscovers that agents thread synchronous calls through six services if allowed to.
- Rejected because: the method's core claim, that agents build reliably inside clear boundaries, is an architectural claim. Neutrality would make it a hope.

### Option C — Modular monolith with DDD, no events

- Pros: DDD benefits without distributed-systems cost; simpler operations.
- Cons: contexts share a deployment and often a database; the blast-radius argument weakens; legacy strangling ([Chapter 10](../../playbook/10-legacy-modernization.md)) needs an event backbone anyway.
- Rejected as the mandate, accepted as a valid starting shape: a modular monolith with context boundaries and events at the seams is compliant with this decision.

## Consequences

- Positive: Units of Work are single-context by default; the plan gate has something concrete to check plans against; architecture tests catch violations mechanically.
- Negative: event-storming and context mapping become required Inception activities for new areas; teams need the DDD learning path in [Chapter 11](../../playbook/11-learning-paths.md).
- Follow-ups: `event-storm` and `from-schema` skills; architecture-test setup in the paved road.

## Revisit when

Agent context windows and reliability grow to the point where whole-system context is routinely practical and the boundary argument no longer holds, or two consecutive quarterly reviews show pods choosing to violate the mandate for reasons the ADR did not anticipate.
