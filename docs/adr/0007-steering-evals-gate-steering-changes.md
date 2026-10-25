# 0007 — Regression-test steering files and skills with golden tasks, run cold

- **Status:** Accepted; pass criterion amended by [0020](0020-steering-evals-run-multiple-trials.md)
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; recorded retroactively on 2026-09-23 for commit 1f968a2

## Context

[Chapter 03](../../playbook/03-tooling-strategy.md#the-context-engineering-hierarchy) tells pods to version steering like code, but nothing tested it. A steering line is only known to work when an agent with no memory of the conversation that produced it follows it. Steering accumulates, some of it contradicts, and when the model underneath changes, lines that worked stop working without anyone noticing. Skills fail the same way, and a skill regression is a process regression in every pod that uses it.

[ADR 0002](0002-claude-code-as-primary-agent.md) concentrates the organization on one agent and one model family, so model deprecations and tier changes reach every repo at once. The playbook needed a way to answer "does our steering still steer?" before, not after, such a change.

## Decision

We will require a small suite of golden tasks per repo, each guarding a named steering line or skill, run cold on every steering or skill PR, on every model-tier change, and quarterly in full.

A golden task is a realistic prompt, checks on the transcript and diff, an optional fixture, and the line it guards; the format and the three starter tasks are in [standards/steering-evals.md](../../standards/steering-evals.md). The suite grows by one task per `lesson-to-steering` PR that adds a line. No model-tier reassignment merges without a green run, and the number of steering fixes it needed is logged.

## Options considered

### Option A — Golden tasks per steering line, run cold  ← chosen

- Pros: tests the thing that actually fails (a specific line in a cold session); cheap enough to run on every steering PR; turns model churn into a counted cost.
- Cons: transcript checks start as human reading; the suite only covers lines someone wrote a task for.

### Option B — Rely on review of steering PRs

- Pros: no new machinery; reviewers already read the diff.
- Cons: a reviewer can judge whether a line is sensible, not whether a cold session obeys it; model changes arrive with no PR to review.
- Rejected because: the failure is silent and behavioural, and reading text cannot detect it.

### Option C — A general benchmark suite for the agent

- Pros: broad coverage; comparable across tools.
- Cons: measures the model's general ability, not whether our steering holds; large suites get ignored.
- Rejected because: it answers a vendor-selection question, not a steering-regression one. The annual re-scoring in ADR 0002 covers vendor selection.

## Consequences

- Positive: steering changes and model changes have an acceptance test; the steering-fix count gives the vendor review a real switching cost.
- Negative: agent time on every steering PR; the platform pod owns another piece of CI; flaky tasks must be fixed or deleted within the week.
- Follow-ups: `evals/check.py` for the mechanical checks; one golden task per reference skill.

## Revisit when

Tooling for automated transcript assertions matures enough to replace the human check, or the suite's pass rate stays at 100% across two model changes with zero steering fixes, which would suggest the tasks are too easy to catch anything.
