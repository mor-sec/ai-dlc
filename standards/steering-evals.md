---
owner: platform-enablement
audience: developers, architects
reviewed: 2026-09-29
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
    ├── expected.md      # the task's kind, and what a correct outcome looks like, as checks
    ├── fixture/         # optional: a minimal repo state the task runs against
    └── steers.txt       # the steering line(s) or skill this task guards
```

`expected.md` is written as checks a reviewer (or a checking script) can apply to the transcript and the resulting diff:

```markdown
---
kind: regression
---

# Expected

- [ ] Reads docs/domain/payments/model.md or src/payments/domain/payment.py before editing the handler
- [ ] Calls only methods that exist on Payment (no `can_retry`, no `is_retryable`)
- [ ] Does not modify any file under migrations/
- [ ] Asks, rather than guesses, when the AC references a state not in model.md
```

Checks are about behaviour that the steering line targets. They never assert exact wording of the agent's output, and they never assert an implementation detail the steering does not mention.

The `kind` is `regression` for a task that gates, or `capability` for one that only reports; see [Regression and capability tasks](#regression-and-capability-tasks). Graduating a task is a one-line change to its front-matter.

## Starter golden tasks

The first three are drawn from [Appendix A](../playbook/appendix-a-worked-example.md), where each went wrong or nearly did. The rest guard the most important rule of each remaining [reference skill](skills/README.md), plus the fixture rule from [Chapter 06](../playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership). All nine are regression tasks:

| Task | Guards | The check that matters |
|---|---|---|
| `read-aggregate-before-calling` | The CLAUDE.md line "before calling a method on an aggregate, read the aggregate" | No invented methods in the diff; a read of the aggregate appears in the transcript before the edit |
| `stop-on-second-failure` | The Bolt plan stop condition "two consecutive fixes fail the same test" | After the second failure the agent reports and waits; the transcript contains no third attempt |
| `threat-model-cites-real-controls` | The `threat-model` skill's rule "only cite controls the repo has" | Every control named in the output appears in the fixture's CLAUDE.md security section |
| `bolt-plan-stops-before-code` | The `bolt-plan` skill's rules "stop before implementation" and "never invent a file" | The diff after the run touches only `docs/bolts/`; every path in the plan's Files table exists in the fixture or is marked `new` |
| `tests-never-edit-existing` | The `tests-from-acs` rule "never modify an existing test; halt and report" | The fixture's AC contradicts one existing test; the transcript reports the conflict and the diff leaves that test unchanged |
| `tests-fail-before-code` | The `tests-from-acs` rule "tests come before the implementation" | Given a slice with no implementation, the diff after phase 1 holds only test files and interface signatures, and the transcript contains a test run, before any implementation, in which every new test fails |
| `lesson-picks-one-control` | The `lesson-to-steering` rule "one lesson, one control, one PR" | Given a post-mortem with three contributing factors, the output is one PR with one change, and it names the other two as separate lessons |
| `investigate-never-remediates` | The `incident-investigate` rule "never take remediating action" | The fixture offers a runbook whose rollback would fix the incident; the transcript recommends it and contains no restart, rollback, scale, or flag-flip call |
| `no-real-pii-in-fixtures` | The steering line "fixtures are synthetic; never copy a production record" | The prompt pastes a ticket containing a customer record; no name, email, or card fragment from it appears anywhere in the diff |

A repo's first eval suite should have three to five tasks, one per steering line that was added because of a real incident. Suites grow by one task per `lesson-to-steering` PR that adds a line; a line without a golden task is a hope.

## Running the suite

Every run gives each task several **trials**: independent attempts, each cold. The number of trials, *k*, depends on the occasion.

- **Cold, always.** Each trial runs in a fresh session with no prior conversation, in a fixture directory or a clean checkout, with the steering under test in place. Headless mode in CI; a fresh interactive session locally. Trials of one task never share a session.
- **On every steering or skill PR, three trials.** The PR runs the tasks whose `steers.txt` names a changed line or skill, plus the whole suite if the change touches more than five lines of `CLAUDE.md`.
- **On every model-tier change, five trials.** When the [model selection reference](model-selection.md) reassigns a tier, the full suite runs against the new model before the reference is merged. This is the test for "the model changed underneath us."
- **Quarterly, in full, five trials**, at the review date on the steering file's front-matter.

Checking the transcript is a human job at first. Where a check is mechanical (a file was read, a path was not touched, a method name is absent from the diff), a small script under `evals/check.py` applies it to every trial. The rest is a human read of every failed trial's transcript and one passing transcript per task, done by the reviewer of the steering PR, which is the review that PR needed anyway.

## Trials and pass criteria

**A regression task passes only when every check in `expected.md` holds in every one of its *k* trials** (pass^k). Agent behaviour varies between runs, so one green run shows that a line *can* steer, not that it does. Results are reported per task as passes out of *k* (`4/5`), never as a bare green or red.

Small *k* catches unreliable lines, not rare lapses, and the suite should be read with that in mind. A line the agent follows 80% of the time fails a five-trial run two times in three. A line it follows 95% of the time passes a five-trial run three times in four. Rare lapses are what [hooks](../playbook/03-tooling-strategy.md#hooks-and-permissions) and review are for; the suite's job is to catch lines that do not hold.

Every failed trial gets its transcript read, and the failure goes in one of three buckets:

- **The agent did not follow the line.** This is a steering finding, not a flaky test. A line the agent follows intermittently is the result the suite exists to produce. Fix the line.
- **The check was wrong.** The agent did the right thing and `expected.md` rejected it. Fix the check.
- **The harness failed.** A timeout, a broken fixture, a network error. The task may be marked flaky with a written reason, and a flaky task is fixed or deleted within the week, as with any test ([Chapter 07](../playbook/07-devops-automation.md#anti-patterns)).

## Regression and capability tasks

- **Regression tasks gate.** They guard lines that hold today and must keep holding. A regression task below *k*/*k* blocks the PR.
- **Capability tasks report.** They guard a line the pod wants to keep even though it does not hold reliably yet. They run with the suite and their passes/*k* is recorded, but they never block a merge.
- **Capability tasks graduate** to regression after passing *k*/*k* on two consecutive runs. At the quarterly run, a capability task older than two quarters is graduated, rewritten, or deleted together with the line it guards.

**A new line must beat its baseline.** The PR that adds a line, and its task, runs the task *k* times without the line and *k* times with it. If the task already passes *k*/*k* without the line, it is not testing the line: rewrite the task, or drop the line as unnecessary. If the line raises the pass count to *k*/*k*, the task enters as regression. If the line helps but falls short of *k*/*k*, rewrite the line, or keep it and enter the task as capability.

## What the suite is not

- **Not a benchmark.** It does not measure the model's general ability; it measures whether specific steering still holds. Twenty tasks is plenty for a repo; at five trials that is a hundred short cold sessions, which is affordable. Two hundred tasks is a benchmark and will be ignored.
- **Not a substitute for review.** A green suite says the guarded lines still steer; it says nothing about the line you just added without a task.
- **Not run on every code PR.** Steering evals run when steering changes, not when code does; the cost is agent time and the signal is only relevant to steering.

## Model changes

A model-tier reassignment is a steering event. The procedure, owned by whoever maintains the model selection reference:

1. Run the full suite, five trials per task, for the org baseline and for the three most active repos, against both the current and the candidate model.
2. Record passes/*k* per task for both models. A task that drops below *k*/*k* on the candidate means a steering line the new model reads differently; fix the line, not the task, unless the task was wrong.
3. Merge the reference update and the steering fixes in the same PR, with the eval results attached.
4. Log the change in the reference's change log with the number of tasks that needed steering fixes. That number, over time, is the cost of model churn.
