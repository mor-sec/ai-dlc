---
owner: platform-enablement
audience: developers, including agents
reviewed: 2026-09-02
review-cadence: quarterly
---

# Test Review Checklist

The Navigator's per-slice checklist for tests an agent generated, plus the two mechanical checks that back it. Audience: the Navigator reviewing during Mob Construction, QA reading the same tests cold at the merge gate ([Chapter 02](../playbook/02-ways-of-working.md#the-ai-pod)), and agents, since this file is loaded as steering for test-writing tasks. Rationale: [Chapter 02, Testing under AI-DLC](../playbook/02-ways-of-working.md#testing-under-ai-dlc).

The problem this solves: the agent that wrote the code wrote the tests, in the same session, with the same misunderstanding. A test suite that passes proves the code agrees with itself. These checks establish that it agrees with the *intent*.

## Per test

- [ ] **Name the failure.** What production failure would turn this test red? If the reviewer cannot say it in one sentence, the test is deleted or rewritten. "Asserts the function returns the total" is not a failure; "charges the pre-discount amount after a price change" is.
- [ ] **No snapshot of the present.** No assertion copies a value from the current output without a stated reason. An agent that reads the code's behaviour and asserts it has encoded the bug, if there is one.
- [ ] **Negative path exists.** Every acceptance criterion with a "must not happen" clause has a test that would fail if it did happen. Agents write happy paths by default.
- [ ] **Assert the contract, not the prose.** Error codes, event names, and state transitions, never message strings or log lines. A copy edit must not break a money-path test.
- [ ] **One reason to fail.** A test that checks five things reports the first failure and hides the other four.

## Per slice

- [ ] **Every AC has a test that names it**, in the docstring or test name, and CI's AC-mapping check reports no unmapped criteria.
- [ ] **Every domain invariant touched** (from `docs/domain/<context>/model.md`) has a test that tries to violate it.
- [ ] **Contract tests were regenerated** from the schema, not hand-edited. A hand-edited contract test is a schema change hiding in a test.
- [ ] **No existing test was changed** unless the Bolt plan's stop condition fired and the pod approved the change with a reason.
- [ ] **Mutation score on changed files is above the gate** (see below), or the PR states which surviving mutants are acceptable and why.

## The two mechanical checks

| Check | What it does | Gate |
|---|---|---|
| **Mutation testing** on changed files (mutmut or cosmic-ray for Python, Stryker for JS/TS, PIT for Java) | Introduces small faults into the new code and counts how many the suite catches. Directly measures whether generated tests detect anything. | Routine class: mutation score ≥ 70% on new and modified files, or a written waiver in the PR. Material and critical classes: ≥ 85%. |
| **AC mapping** (a small CI script over the PR's Unit of Work and test files) | Lists every AC in the Unit of Work and the tests that name it. | Any AC with zero tests fails the check. |

Mutation testing is slow on whole codebases and fast on diffs; run it only against changed files, in the PR pipeline, after unit tests pass ([Chapter 07](../playbook/07-devops-automation.md#the-reference-pipeline-github-actions)).

## For agents writing tests

Read this file before generating tests. For each test you write, put the failure it catches in the docstring, and name the AC. If an AC has no failure you can describe, say so in the PR rather than writing a test that asserts nothing.
