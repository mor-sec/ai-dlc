---
name: tests-from-acs
description: Generate tests that map one-to-one to a Unit of Work's acceptance criteria, each stating the production failure it catches, then run the mutation check on the changed files. Use during Mob Construction when a slice's code exists and its tests do not, or when CI reports unmapped acceptance criteria. Not for characterization tests of legacy behaviour; use characterization-tests for that.
---

# Tests from acceptance criteria

Produces the tests an approved Bolt plan promised, in the shape the [test review checklist](../../test-review-checklist.md) demands, so the Navigator reviews tests that already answer "what failure does this catch?"

## Inputs

- The Bolt plan (`docs/bolts/<bolt-id>.md`): the Test strategy table is the contract this skill fulfils.
- The Unit of Work's stories and ACs, by Jira key.
- The code under test, as it stands in the working tree.
- `docs/domain/<context>/model.md` for the invariants the slice touches.
- The repo's test conventions from `CLAUDE.md` (runner, layout, fixtures) and the mutation tool it names.
- The [test review checklist](../../test-review-checklist.md). Read it; it is the standard the output is reviewed against.

## Outputs

- Test files in the paths the Bolt plan names, one test per Test strategy row at minimum, each with a docstring of the form `AC<n>: catches <production failure>`.
- Contract tests regenerated from their schema, untouched by hand.
- A mutation report for the changed files: score, surviving mutants, and for each survivor either a new test or a one-line reason it is acceptable.
- A note to the pod listing any AC for which no failure could be described.

## Steps

1. Read the checklist, then the plan's Test strategy table. Each row is a test to write; the third column is the docstring.
2. For each AC, read the code path it exercises before writing the test. The test asserts the contract (return values, error codes, event names, state transitions), never message strings or log lines.
3. Write the negative test for every AC with a "must not happen" clause: assert the forbidden outcome did not occur (no event published, no row written, no call made), not only that the error was returned.
4. Add one test per domain invariant the slice touches that attempts to violate it.
5. Regenerate contract tests from the schema with the repo's generator. If no generator exists, stop and tell the pod; do not hand-write a contract test.
6. Run the suite. A failing test is a finding, not a problem to make green: report it. Change the code only if the Navigator confirms the test is right and the code is wrong, and log that in the plan's deviations.
7. Run the mutation tool on the changed files only. For each surviving mutant, add a test that kills it or write one line explaining why it is acceptable (equivalent mutant, logging only). Repeat once. Report the final score against the class threshold in the checklist.
8. List any AC you could not write a meaningful failure for. That is a signal the AC is untestable as written and belongs back in elaboration.

## Rules

- Never assert a value copied from current output. If you do not know the expected value from the AC or the domain model, ask.
- Never modify an existing test. If one must change, that is a Bolt plan stop condition; halt and report.
- One reason to fail per test. Split a test that checks several things.
- Tests name their AC. A test with no AC is either an invariant test (say which invariant) or does not belong in this slice.
- Do not weaken a mutation threshold or exclude files to reach the score. Report the score you got.

## Verification

Before handing over:

- [ ] Every Test strategy row has a test; every test has an `AC<n>: catches …` docstring or an `Invariant: …` docstring
- [ ] Every "must not happen" AC has a negative test asserting the absence
- [ ] No test asserts a message string or log line
- [ ] Contract tests were generated, not written
- [ ] Mutation report attached with the score and each survivor dispositioned
- [ ] The unmapped-AC note is present, even if it says "none"

Tests are a draft until the Navigator has read each one and can name the failure it catches.
