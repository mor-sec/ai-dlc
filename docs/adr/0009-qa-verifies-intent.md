# 0009 — Define QA as a shared pod accountability for verifying intent, not a manual testing stage

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; recorded retroactively on 2026-09-23 for commit 86a16ea

## Context

QA was named throughout the playbook and defined nowhere. Under AI-DLC the agent generates both the code and the tests, so behaviour is verified by generated tests on every change, and a manual regression stage has nothing left to do. What remains open is the question behind review culture: the agent wrote the tests, so what checks the tests? The Navigator reviews them per slice ([Chapter 02](../../playbook/02-ways-of-working.md#testing-under-ai-dlc)), but the Navigator watched the code being built and shares its blind spots.

Organizations arriving at AI-DLC mostly have QA engineers already. The playbook had to say what they do, or they would either keep running a manual stage in front of every deploy or be quietly removed.

## Decision

We will define QA as a part-time accountability shared across two or three pods that owns verification of intent: acceptance criteria that are testable as written, a gap-free AC-mapping check, exploratory testing in the ephemeral environment, and an adversarial cold reading of generated tests at the merge gate.

QA attends every Mob Elaboration and every merge gate, reads the same [test review checklist](../../standards/test-review-checklist.md) as the Navigator with a different bias, and owns the mutation thresholds for their pods. Chapter 11 gains a QA learning path with a practicum.

## Options considered

### Option A — QA verifies intent, shared across pods  ← chosen

- Pros: a second reader who did not watch the build; QA effort moves to where generated tests are weakest (wrong assertions, missing ACs); keeps experienced testers' judgment in the loop.
- Cons: requires QA engineers to learn to read code and tests adversarially; sharing one QA across pods creates a queue at the merge gate if pods deploy at the same moment.

### Option B — Keep a dedicated QA stage before release

- Pros: familiar; a clear sign-off point.
- Cons: a handoff and a wait on every Bolt; duplicates what generated tests already cover.
- Rejected because: multiple deploys per pod per day ([Chapter 07](../../playbook/07-devops-automation.md)) cannot pass through a manual stage.

### Option C — No QA role; developers and generated tests cover verification

- Pros: smallest pods; no extra dependency.
- Cons: the only reader of generated tests is the person who prompted them.
- Rejected because: tests that pass with the bug present are the characteristic failure of agent-written tests, and catching them needs a reader with a different bias.

## Consequences

- Positive: generated tests get an independent reviewer; ACs are checked for testability before construction starts, where fixing them is cheap.
- Negative: existing QA staff need retraining; if the shared QA is overloaded, the merge gate becomes the bottleneck.
- Follow-ups: QA learning path and practicum in [Chapter 11](../../playbook/11-learning-paths.md); a glossary entry for QA.

## Revisit when

Merge-gate wait time attributable to QA exceeds the pod's review-latency target for a quarter, or mutation and AC-mapping checks reach a maturity where the adversarial reading stops finding defects the checks miss.
