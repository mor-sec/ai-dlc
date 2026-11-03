# 0020 — Run each steering eval task several times and gate on every trial passing

- **Status:** Accepted
- **Date:** 2026-09-29
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

[ADR 0007](0007-steering-evals-gate-steering-changes.md) made golden tasks the acceptance test for steering and model changes, with the pass criterion "every check holds" on a single cold run. The playbook already knows that is too weak for anything a model does: [Chapter 13](../../playbook/13-building-ai-features.md#why-ai-features-are-different) says the same input can produce different outputs and that a single correct run proves little. The steering suite ignored its own advice.

A single run fails in both directions. A line the agent follows 60% of the time passes a single run with probability 0.6, so it often merges as "working". A task that fails once is either marked flaky, hiding the evidence that the line holds only sometimes, or deleted.

Anthropic's guidance on agent evals ("Demystifying evals for AI agents") addresses this directly. It runs each task several times as independent **trials**, measures pass^k (the probability that all *k* trials succeed) where reliability matters, and separates regression evals, which should pass nearly 100% of the time, from capability evals, which start low and graduate. It also tells readers to read the transcripts of failed trials, because only the transcript shows whether the agent failed or the grader did.

## Decision

We will run every steering eval task as *k* independent cold trials (three on steering PRs; five on model-tier changes and the quarterly run), and a regression task passes only if every trial passes.

- Tasks are `regression` (gate) or `capability` (report only), recorded in `expected.md` front-matter. Capability tasks graduate after *k*/*k* on two consecutive runs; after two quarters they are graduated, rewritten, or deleted with their line.
- A new line's task runs *k* times without the line and *k* times with it. A task that passes without the line is not testing the line.
- Every failed trial's transcript is read and classified: agent (fix the line), check (fix the check), or harness (fix or delete within the week). Intermittent obedience is a steering finding, never flakiness.
- Results are reported as passes/*k* per task, and model changes record them for both the current and the candidate model.

This amends ADR 0007's pass criterion and leaves the rest of it standing. Detail: [standards/steering-evals.md](../../standards/steering-evals.md#trials-and-pass-criteria).

## Options considered

### Option A — *k* trials, pass^k for regression tasks, a capability tier  ← chosen

- Pros: catches lines that hold only sometimes; separates agent variance from harness flakiness; the baseline run proves each new line changes behaviour; capability tasks let a pod keep a useful but imperfect line without blocking every PR.
- Cons: three to five times the agent time per run; more transcripts to read when things fail; small *k* still misses rare lapses.

### Option B — Keep a single run

- Pros: cheapest; no change to tooling.
- Cons: a line that holds 60% of the time passes a single run more often than not; every intermittent failure looks like flakiness.
- Rejected because: agent behaviour varies between runs, so one pass says little about whether a line steers.

### Option C — A pass-rate threshold, such as 80% of trials

- Pros: tolerant of occasional variance; familiar from product eval sets.
- Cons: a steering line exists to hold every time. A line that holds four times in five is broken on the fifth pod-day, and a threshold hides that in an average.
- Rejected because: pass-rate thresholds suit product eval sets of hundreds of cases ([Chapter 13](../../playbook/13-building-ai-features.md#evals-are-the-test-suite)). A golden task guards one line, and the question it answers is whether that line holds.

## Consequences

- Positive: "green" means the line held every time it was tried; model changes show per-task drift as passes/*k*, not only pass or fail; the suite stops accumulating tasks that test nothing.
- Negative: agent time per steering PR roughly triples; the platform pod's runner needs trial support and per-task reporting; reviewers read more failed transcripts at first.
- Follow-ups: trial count and passes/*k* reporting in `evals/check.py` and the CI workflow; front-matter `kind` added to the starter tasks' `expected.md` files.

## Revisit when

Trial cost becomes a material share of steering-PR cycle time, or tooling for automated transcript assertions matures enough to raise *k* cheaply, or two consecutive model changes pass every task at *k*/*k* with no steering fixes.
