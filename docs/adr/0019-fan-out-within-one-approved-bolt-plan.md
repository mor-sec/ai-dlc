# 0019 — Allow fan-out into parallel lanes within one approved Bolt plan; still one Unit of Work per pod

- **Status:** Accepted
- **Date:** 2026-09-29
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook allows one agent session per pod at a time. [Chapter 01](../../playbook/01-ai-dlc-methodology.md#tips--tricks) says "one pod, one Unit of Work at a time", and [Chapter 02](../../playbook/02-ways-of-working.md#anti-patterns) names parallel branches as the symptom of a silent pod. Both rules protect the same thing: the pod reviews together, and nobody rubber-stamps their own agent's output.

The single session also serializes generation that does not need to be serial. Once the plan is approved, the slices of a Bolt that touch different files wait for each other while the agent works through them one by one, and the Navigator waits with them. Anthropic's published practice for Claude Code runs several sessions in parallel, each in its own git worktree, and its research on real sessions finds that people make about 70% of the planning decisions but only about 20% of the execution decisions. Planning is where the pod's judgment is needed. Execution inside an approved plan is where the agent works alone anyway.

Pods with capable tools will run parallel sessions whether or not the playbook allows it. The same argument settled [ADR 0014](0014-agent-autonomy-levels.md): a practice that is governed is better than one that happens without controls.

## Decision

We will allow the Driver to fan a Bolt's construction out into at most three parallel lanes, each an agent session in its own git worktree, when the approved Bolt plan declares lanes with disjoint files. The pod still works on one Unit of Work at a time.

- Anything the lanes share (a schema, a port signature, a migration) is lane 0. It is built first in a single session and reviewed before the other lanes start.
- A lane with an unreviewed slice stops generating. All lanes count against the one daily review cap.
- A lane halts if it needs another lane's file or a change to lane 0. A stop condition that changes the plan pauses every lane.
- Reviewed lanes merge into the Bolt branch in plan order. The integrated diff then gets the full test run, mutation testing, and a fresh-eyes review before the one PR for the Bolt.
- No fan-out on critical-class Bolts.

Detail: [Chapter 02, Fan-out inside a Bolt](../../playbook/02-ways-of-working.md#fan-out-inside-a-bolt). Plan format: the Fan-out section of the [Bolt plan template](../../standards/bolt-plan-template.md).

## Options considered

### Option A — Lanes within one approved plan  ← chosen

- Pros: the gates that need the pod (Unit approval, plan approval, per-slice review, merge) are unchanged; generation stops being serial where the plan shows it does not need to be; back-pressure from review keeps the review cap binding.
- Cons: plans take longer to write and review, because lane boundaries must be right; integration adds a step; token spend per Unit rises.

### Option B — Keep a single session per pod

- Pros: simplest; no integration step; the rule already exists.
- Cons: generation sits idle behind itself; pods will run parallel sessions anyway, without lane boundaries or back-pressure.
- Rejected because: the risk the rule guards against is unreviewed work, and Option A controls that directly instead of banning parallel generation.

### Option C — Parallel Units, one per developer

- Pros: the most throughput on paper; each developer drives their own agent.
- Cons: brings back handoffs between people working on different intents; each developer reviews their own agent's output alone; the pod stops being a mob.
- Rejected because: it removes the reason the pod exists ([Chapter 02](../../playbook/02-ways-of-working.md#the-ai-pod)). Parallelize slices of one plan, never Units.

## Consequences

- Positive: shorter wall-clock time for Bolts with independent slices; the Navigator's review time is used rather than spent waiting; lane boundaries in the plan make coupling visible before any code exists.
- Negative: more tokens per Unit, visible in [cost per validated Unit of Work](../../playbook/03-tooling-strategy.md#unit-economics-cost-per-validated-unit-of-work); an integration step per fan-out Bolt; one more thing to get right at the plan gate.
- Follow-ups: the Fan-out section of a committed Bolt plan identifies fan-out Bolts, so lead time, rework rate, and escaped defects can be compared with single-session Bolts at consolidation.

## Revisit when

A quarter of consolidation records shows fan-out Bolts gaining no lead time over single-session Bolts, or raising rework rate or escaped defects; or a pod brings a quarter of evidence that width above three holds the review cap.
