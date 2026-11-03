# 0022 — Write tests before the code they test, and check mechanically that the implementation left them alone

- **Status:** Accepted
- **Date:** 2026-09-29
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook's test discipline ([Chapter 02](../../playbook/02-ways-of-working.md#testing-under-ai-dlc)) starts from the generated-test problem: the session that wrote a bug writes tests that pass with the bug in place. Mutation testing and acceptance-criteria mapping check the tests after the fact. Two gaps remain.

First, order. The `tests-from-acs` skill ran "when a slice's code exists and its tests do not", so tests were written by reading the code they were meant to check, which is how a bug gets encoded as expected behaviour. Anthropic's Claude Code guidance recommends the opposite order: write tests from the requirement, confirm they fail, commit them, then implement without changing them, ideally in a separate session.

Second, tampering. An agent under pressure to reach green can change the test instead of the code: weaken an assertion, mark a test skipped or expected-to-fail, special-case the input. The playbook forbids it (a Bolt plan stop condition and a checklist item), but only a person catches it. In [Appendix C](../../playbook/appendix-c-a-bolt-that-fails.md) the agent proposed `xfail` on a money-path test, and a pod member refused it. Nothing mechanical would have.

## Decision

We will write each slice's tests before its implementation, confirm each fails for the reason its acceptance criterion names, review them, and commit them as the slice's red commit, after which the implementation must not modify them. A CI test-integrity check fails any PR that modifies or deletes a test present on the base branch, or adds a skip or xfail marker, unless a person has applied the `test-change-approved` label with a reason.

The `tests-from-acs` skill is re-sequenced into a red phase and a post-implementation mutation phase. For material and critical changes, the session that implements is not the session that wrote the tests. A reference hook in the [agent baseline](../../standards/agent-baseline.md#baseline-hooks) blocks the same edits inside the session as an early warning. Detail: [test review checklist](../../standards/test-review-checklist.md) and [Chapter 02](../../playbook/02-ways-of-working.md#testing-under-ai-dlc).

## Options considered

### Option A — Tests first, CI test-integrity check, in-session hook  ← chosen

- Pros: tests are written from intent, not from the code; a test that passes before the code exists is caught as testing nothing; tampering becomes a visible, labelled decision instead of a diff a tired reviewer might miss.
- Cons: writing tests against interfaces that do not exist yet needs signature stubs; some legitimate test changes now need a label; path patterns for "a test file" need tuning per repo.

### Option B — Keep tests-after, rely on mutation testing

- Pros: no change to the skill; mutation testing already measures whether tests detect faults.
- Cons: mutation testing checks that tests catch faults in the code as written, not that they encode the intent; it cannot see a test weakened to pass.
- Rejected because: the two checks answer different questions, and tampering is exactly the change mutation testing is blind to.

### Option C — The hook alone, no CI check

- Pros: immediate feedback inside the session; nothing new in CI.
- Cons: a hook on file-editing tools cannot see edits made through shell commands, and hooks are configuration a session can run without.
- Rejected because: a control of record has to run where the agent cannot route around it, which is CI.

## Consequences

- Positive: one more class of agent failure (gaming the tests) moves from human vigilance to a mechanical gate; the red commit makes "tests before code" auditable in the history.
- Negative: an extra commit per slice; a label step when a test genuinely must change; the CI check needs per-language marker patterns.
- Follow-ups: the test-integrity check in the reference pipeline; the golden task `tests-fail-before-code` in the [steering evals](../../standards/steering-evals.md).

## Revisit when

The `test-change-approved` label is applied to more than a small fraction of PRs, which would mean the check is catching legitimate work and the patterns need narrowing; or red commits show tests routinely rewritten after implementation starts, which would mean the red phase is being done for form.
