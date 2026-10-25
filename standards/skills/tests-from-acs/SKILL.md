---
name: tests-from-acs
description: Write a slice's tests from the Unit of Work's acceptance criteria before its implementation exists, confirm each fails for the reason its AC names, and prepare the red commit; after implementation, run the mutation check on the changed files. Use at the start of every slice in Mob Construction, before any implementation code, and again when the slice's implementation is green; also when CI reports unmapped acceptance criteria. Not for characterization tests of legacy behaviour; use characterization-tests for that.
---

# Tests from acceptance criteria

Produces the tests an approved Bolt plan promised, before the code they test, in the shape the [test review checklist](../../test-review-checklist.md) demands, so the Navigator reviews tests that already answer "what failure does this catch?" and the implementation is written to pass them rather than the other way round.

## Inputs

- The Bolt plan (`docs/bolts/<bolt-id>.md`): the Test strategy table is the contract this skill fulfils, and the Approach names the interfaces the tests call.
- The Unit of Work's stories and ACs, by Jira key.
- `docs/domain/<context>/model.md` for the invariants the slice touches.
- The repo's test conventions from `CLAUDE.md` (runner, layout, fixtures) and the mutation tool it names.
- The [test review checklist](../../test-review-checklist.md). Read it; it is the standard the output is reviewed against.
- In phase 2 only: the implementation, as it stands in the working tree.

## Outputs

- Phase 1: test files in the paths the Bolt plan names, one test per Test strategy row at minimum, each with a docstring of the form `AC<n>: catches <production failure>`, and a run showing every new test failing for its stated reason. A proposed red commit message: `<PROJ-123> tests for AC<n>–AC<m> (red)`.
- Phase 1: contract tests regenerated from their schema, untouched by hand.
- Phase 2: a mutation report for the changed files: score, surviving mutants, and for each survivor either a new test or a one-line reason it is acceptable.
- A note to the pod listing any AC for which no failure could be described.

## Steps

### Phase 1 — before the implementation (red)

1. Read the checklist, then the plan's Test strategy table. Each row is a test to write; the third column is the docstring.
2. For each AC, write the test against the interface the plan's Approach names (the aggregate method, the handler, the port). If the interface does not exist yet, add only its signature, raising "not implemented"; write no behaviour. The test asserts the contract (return values, error codes, event names, state transitions), never message strings or log lines.
3. Write the negative test for every AC with a "must not happen" clause: assert the forbidden outcome did not occur (no event published, no row written, no call made), not only that the error was returned.
4. Add one test per domain invariant the slice touches that attempts to violate it.
5. Regenerate contract tests from the schema with the repo's generator. If no generator exists, stop and tell the pod; do not hand-write a contract test.
6. Run the new tests. Every one must fail, and fail for the reason its AC names: an assertion about the missing behaviour, not an import error, a collection error, or a fixture that does not load. Fix a test that fails for the wrong reason. A test that passes before the implementation exists is testing nothing: rewrite it, or report that the behaviour already exists.
7. Hand the failing run to the Navigator for review against the checklist. After approval, the tests are committed as the slice's red commit. Stop here; implementation is not part of this skill.

### Phase 2 — after the implementation is green

1. Run the suite. A failing test is a finding, not a problem to make green: report it. The committed tests are not edited to pass; if one is wrong, that is a stop condition for the pod.
2. Run the mutation tool on the changed files only. For each surviving mutant, add a new test that kills it or write one line explaining why it is acceptable (equivalent mutant, logging only). Repeat once. Report the final score against the class threshold in the checklist.
3. List any AC you could not write a meaningful failure for. That is a signal the AC is untestable as written and belongs back in elaboration.

## Rules

- Tests come before the implementation. Never write a slice's tests by reading its implementation.
- Never assert a value copied from current output. If you do not know the expected value from the AC or the domain model, ask.
- Never modify a committed test, and never add a skip or xfail marker. If one must change, that is a Bolt plan stop condition; halt and report. The CI test-integrity check and the baseline hook enforce this.
- For material and critical classes, the session that implements the slice is not the session that ran phase 1.
- One reason to fail per test. Split a test that checks several things.
- Tests name their AC. A test with no AC is either an invariant test (say which invariant) or does not belong in this slice.
- Do not weaken a mutation threshold or exclude files to reach the score. Report the score you got.

## Verification

Before handing over phase 1:

- [ ] Every Test strategy row has a test; every test has an `AC<n>: catches …` docstring or an `Invariant: …` docstring
- [ ] Every "must not happen" AC has a negative test asserting the absence
- [ ] No test asserts a message string or log line
- [ ] Contract tests were generated, not written
- [ ] The run shows every new test failing, each for the reason its AC names
- [ ] The diff contains test files and interface signatures only, no behaviour

Before handing over phase 2:

- [ ] No committed test was changed; new tests were added only to kill mutants
- [ ] Mutation report attached with the score and each survivor dispositioned
- [ ] The unmapped-AC note is present, even if it says "none"

Tests are a draft until the Navigator has read each one and can name the failure it catches.
