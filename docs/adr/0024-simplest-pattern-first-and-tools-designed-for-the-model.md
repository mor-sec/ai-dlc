# 0024 — Build AI features with the simplest pattern that passes the eval set, and design their tools for the model

- **Status:** Proposed
- **Date:** 2026-09-29
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

[ADR 0018](0018-ai-features-evals-adapter-kill-switch.md) settled how AI features are contained and tested: the model behind a domain adapter, eval sets as the test suite, a fallback and a kill switch. It did not say what shape the model's part should take. [Chapter 13](../../playbook/13-building-ai-features.md) caps loops where the model calls tools and decides again, but says nothing about when a loop is warranted, and nothing about how the tools it calls should be designed.

Anthropic's guidance on building agents draws the line that matters. In a workflow, code decides the sequence of model calls; in an agent, the model decides its own next step. The advice is to find the simplest solution that works and add agentic complexity only when it measurably improves results, because agents trade latency and cost for flexibility and their errors compound. Its guidance on tools for agents adds that tools are an interface for a model, not a thin wrapper over an API: fewer, task-shaped tools; responses that spend tokens on meaning rather than identifiers; errors that say how to fix the call; and evaluation with realistic tasks.

The same tool-design rules apply inside the method. The organization builds MCP servers for its development agents ([Chapter 03](../../playbook/03-tooling-strategy.md#mcp-servers)), and a Jira server that returns raw API payloads fills a session's context with fields no task needs.

## Decision

We will start every AI feature at the simplest pattern (one model call with retrieval, then a fixed workflow) and move to an agent loop only when the steps cannot be known in advance and the eval set shows the simpler pattern falls short, with the reason recorded in the Unit of Work. Tools that a model calls, in product features and in the organization's own MCP servers, are designed for the model and evaluated with realistic multi-step tasks.

Detail: [Chapter 13, Choose the simplest pattern that works](../../playbook/13-building-ai-features.md#choose-the-simplest-pattern-that-works) and [Design tools for the model](../../playbook/13-building-ai-features.md#design-tools-for-the-model). This extends ADR 0018 and changes none of it.

## Options considered

### Option A — Simplest pattern first, escalation on eval evidence  ← chosen

- Pros: most features stay cheap, fast, and easy to evaluate; agent loops are used where they earn their cost; the decision is evidence, like a model-tier escalation.
- Cons: some features are built twice, first as a workflow and then as an agent; the eval set must be good enough to show the gap.

### Option B — Agent loops by default

- Pros: one architecture for every feature; flexible when requirements are unclear.
- Cons: higher latency and cost per action; compounding errors; harder to evaluate, because behaviour depends on the path the model chose.
- Rejected because: most product features are a known sequence of steps, and paying for flexibility they never use is waste.

### Option C — No guidance on patterns or tools

- Pros: teams choose freely.
- Cons: tools get generated as one-per-endpoint API wrappers, which is what agents write when nobody says otherwise; pattern choices go unrecorded.
- Rejected because: the eval set can say whether a feature works, but not why it costs three times what it should.

## Consequences

- Positive: lower cost and latency per AI feature; eval sets that are easier to write and read; MCP servers that spend a development agent's context on what the task needs.
- Negative: an extra decision recorded per AI Unit of Work; tool design becomes review material for the architect.
- Follow-ups: review the organization's existing MCP servers against the tool-design rules.

## Revisit when

Eval evidence across several features shows agent loops routinely beating workflows at similar cost, which would make the default the wrong way round; or the provider's tooling changes the cost and latency of loops materially.
