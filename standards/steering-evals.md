---
owner: platform-enablement
audience: developers, architects
reviewed: 2026-09-02
review-cadence: quarterly
---

# Steering Evals

How steering files and skills are regression-tested. Audience: anyone changing a `CLAUDE.md`, a skill, or the model tier assignments. Rationale: [Chapter 03](../playbook/03-tooling-strategy.md#steering-files-claudemd) says to version steering like code, and a steering regression is a production regression waiting to happen; this is the CI that makes the claim true.

The problem: a steering line is only known to work when an agent with no memory of the conversation that produced it follows it. Nobody checks that. Steering accumulates, some of it contradicts, and when the model underneath changes, lines that worked stop working silently. Skills fail the same way. The fix is the same as for code: a small suite of golden tasks, run cold, on every change.

## What a golden task is

A golden task is a realistic task the agent should perform correctly *because of* a specific steering line or skill, plus a checkable definition of correct. It is not a unit test of the model; it is a test that the steering still steers.

Each golden task lives in `evals/<task-name>/` in the repo whose steering it tests, or in the shared steering repo for the org baseline:

```text
evals/
└── read-aggregate-before-calling/
    ├── prompt.md        # the task, exactly as a Driver would phrase it
    ├── expected.md      # what a correct outcome looks like, as checks
    ├── fixture/         # optional: a minimal repo state the task runs against
    └── steers.txt       # the steering line(s) or skill this task guards
```

`expected.md` is written as checks a reviewer (or a checking script) can apply to the transcript and the resulting diff:

```markdown
# Expected

- [ ] Reads docs/domain/payments/model.md or src/payments/domain/payment.py before editing the handler
- [ ] Calls only methods that exist on Payment (no `can_retry`, no `is_retryable`)
- [ ] Does not modify any file under migrations/
- [ ] Asks, rather than guesses, when the AC references a state not in model.md
```

Checks are about behaviour that the steering line targets. They never assert exact wording of the agent's output, and they never assert an implementation detail the steering does not mention.

## Three golden tasks to start with

Drawn from [Appendix A](../playbook/appendix-a-worked-example.md), where each of these went wrong or nearly did:

| Task | Guards | The check that matters |
|---|---|---|
| `read-aggregate-before-calling` | The CLAUDE.md line "before calling a method on an aggregate, read the aggregate" | No invented methods in the diff; a read of the aggregate appears in the transcript before the edit |
| `stop-on-second-failure` | The Bolt plan stop condition "two consecutive fixes fail the same test" | After the second failure the agent reports and waits; the transcript contains no third attempt |
| `threat-model-cites-real-controls` | The `threat-model` skill's rule "only cite controls the repo has" | Every control named in the output appears in the fixture's CLAUDE.md security section |

A repo's first eval suite should have three to five tasks, one per steering line that was added because of a real incident. Suites grow by one task per `lesson-to-steering` PR that adds a line; a line without a golden task is a hope.

## Running the suite

- **Cold, always.** Each task runs in a fresh session with no prior conversation, in a fixture directory or a clean checkout, with the steering under test in place. Headless mode in CI; a fresh interactive session locally.
- **On every steering or skill PR.** The PR runs the tasks whose `steers.txt` names a changed line or skill, plus the whole suite if the change touches more than five lines of `CLAUDE.md`.
- **On every model-tier change.** When the [model selection reference](model-selection.md) reassigns a tier, the full suite runs against the new model before the reference is merged. This is the test for "the model changed underneath us."
- **Quarterly, in full**, at the review date on the steering file's front-matter.

Pass criteria: every check in `expected.md` holds. A task may be marked flaky only with a written reason, and a flaky task is fixed or deleted within the week, as with any test ([Chapter 07](../playbook/07-devops-automation.md#anti-patterns)).

Checking the transcript is a human job at first. Where a check is mechanical (a file was read, a path was not touched, a method name is absent from the diff), a small script under `evals/check.py` applies it; the rest is a five-minute read by the reviewer of the steering PR, which is the review that PR needed anyway.

## What the suite is not

- **Not a benchmark.** It does not measure the model's general ability; it measures whether specific steering still holds. Twenty tasks is plenty for a repo. Two hundred is a benchmark and will be ignored.
- **Not a substitute for review.** A green suite says the guarded lines still steer; it says nothing about the line you just added without a task.
- **Not run on every code PR.** Steering evals run when steering changes, not when code does; the cost is agent time and the signal is only relevant to steering.

## Model changes

A model-tier reassignment is a steering event. The procedure, owned by whoever maintains the model selection reference:

1. Run the full suite for the org baseline and for the three most active repos against the candidate model.
2. Record failures. A failing task means a steering line the new model reads differently; fix the line, not the task, unless the task was wrong.
3. Merge the reference update and the steering fixes in the same PR, with the eval results attached.
4. Log the change in the reference's change log with the number of tasks that needed steering fixes. That number, over time, is the cost of model churn.
