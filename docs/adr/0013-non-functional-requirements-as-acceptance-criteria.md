# 0013 — Write non-functional requirements as numbered acceptance criteria, tested at a gate sized to their cost

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook's test strategy ([Chapter 02](../../playbook/02-ways-of-working.md#testing-under-ai-dlc)) covered contracts, unit tests on invariants, and one smoke path. Performance, load, and resilience were not mentioned; accessibility appeared only in the Chapter 04 frontend section. Agents build what the acceptance criteria describe and nothing more, so a story silent on latency or on a failing dependency produces code that is correct for one request and fails under load or on the first timeout.

Non-functional tests also cost more than functional ones. A full load test on every PR would break the Bolt cadence; running them only before a release would bring back the release-day batching that AI-DLC removes.

## Decision

We will require non-functional requirements to be written as acceptance criteria with numbers, mapped to tests like any other AC, and run a short performance smoke on every PR with full load and resilience runs nightly and on material and critical changes.

The Unit of Work template prompts for non-functional ACs; the test review checklist requires each to have a measuring test; [Chapter 07](../../playbook/07-devops-automation.md#the-reference-pipeline-github-actions) places the checks in the pipeline.

## Options considered

### Option A — Numbered NFR acceptance criteria, gate sized to cost  ← chosen

- Pros: agents implement and test budgets they can read; the AC-mapping check covers NFRs for free; routine PRs stay fast.
- Cons: someone must choose the numbers during elaboration, which product owners find hard at first; a nightly regression is found a day late.

### Option B — A separate performance-testing stage before release

- Pros: familiar; one environment set up for load.
- Cons: a batch stage in front of continuous deploys; regressions are found days after the Bolt that caused them.
- Rejected because: it reintroduces release batching and separates the finding from the pod that can fix it cheaply.

### Option C — Rely on production SLOs and post-deploy verification

- Pros: measures real traffic; already in the pipeline as auto-rollback.
- Cons: finds problems after customers do; says nothing about resilience paths that rarely fire.
- Rejected because: rollback limits the damage but does not prevent it, and failure-path behaviour is exactly what generated code gets wrong.

## Consequences

- Positive: budgets are explicit and reviewable at elaboration; performance regressions surface in the PR that caused them.
- Negative: ephemeral environments must be production-shaped enough for a meaningful smoke; nightly load infrastructure is a new cost for the platform pod.
- Follow-ups: a performance-smoke step in the reference pipeline; guidance for product owners on choosing budgets.

## Revisit when

Performance smokes on ephemeral environments prove too noisy to gate on for a quarter, or escaped performance incidents stay flat despite the change.
