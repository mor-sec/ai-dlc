# 0004 — Represent Bolts as labels in Jira, not as Sprints

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

A Bolt is an execution cycle of hours to days ([Chapter 01](../../playbook/01-ai-dlc-methodology.md#the-vocabulary)). Jira's native iteration construct is the Sprint: a fixed-length container, typically two weeks, with velocity reporting built around it. Teams adopting AI-DLC on Jira must decide whether to force Bolts into Sprints, which most Jira reporting expects, or to model them another way and lose some out-of-the-box charts.

The playbook's position on measurement is that story points and velocity are meaningless or corrupting under AI-DLC, and that throughput of validated Units of Work and lead time are the metrics that matter ([Chapter 08](../../playbook/08-github-jira.md#reporting-that-matches-the-method)).

## Decision

We will represent Bolts as a `bolt-id` label or custom field on the stories executed together, and not as Jira Sprints. Units of Work are Epics; workflow states are `Elaboration → Ready → In Bolt → In Review → Done`, transitioned by GitHub events wherever possible.

Where organizational reporting insists on Sprints, one-week Sprints may exist as a reporting shell only. They carry no planning ceremony and no velocity target.

## Options considered

### Option A — Bolt as label or field  ← chosen

- Pros: Bolts keep their natural length; reporting is built on Units of Work and lead time from day one; no ceremony imported with the container.
- Cons: Jira's Sprint burndown and velocity charts are unavailable; Bolt integrity must be reported from the label via a filter or dashboard gadget.

### Option B — Bolts as Jira Sprints

- Pros: native charts; familiar to project managers.
- Cons: a two-week container around a two-day cycle is pure friction; velocity charts invite story points back; within a quarter the team re-derives Scrum.
- Rejected because: the container brings its ceremony with it. This is the "sprint cosplay" anti-pattern.

### Option C — Drop Jira for Bolt tracking, use GitHub Projects only

- Pros: single system, no integration.
- Cons: loses the intent-to-deploy traceability chain that auditors and cost allocation depend on; product owners lose their working surface.
- Rejected because: Jira holds intent and GitHub holds execution; the value is in the link between them.

## Consequences

- Positive: reporting matches the method from the first week; Bolt integrity (stories per bolt-id finished ÷ started) is a cheap early signal of over-sized Units.
- Negative: dashboards for Bolt metrics need building; PMO reporting that assumes Sprints needs a conversation in Wave 1.
- Follow-ups: a shared Jira dashboard template for the [metrics reference](../../standards/metrics-reference.md) flow metrics.

## Revisit when

Jira ships a native short-cycle iteration construct without velocity semantics, or the organization's portfolio reporting is rebuilt around Units of Work so that the reporting shell is no longer requested.
