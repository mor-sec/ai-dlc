---
owner: platform-enablement
audience: developers, QA, engineering leaders
reviewed: 2026-09-24
review-cadence: quarterly
---

# Appendix C — A Bolt that goes wrong

[Appendix A](appendix-a-worked-example.md) follows a Unit of Work where every gate fires and the work ships. This appendix follows one where the gates fire and the right call is to stop. The plan is approved, the tests are green, and the Bolt is still abandoned at 14:10 on Tuesday, because the mutation run shows the green tests prove nothing and the fix would break a stop condition. Audience: anyone who wants to see what a failed Bolt looks like when the method works, and why that is a good week rather than a bad one.

The scenario: the same Payments pod two weeks later. Lee is Driver this week (the role rotates), Sam is Navigator, Aisha is domain anchor, Dana is product owner, and Priya is QA. Names and numbers are illustrative; the shapes are exact.

## Monday 09:30 — Elaboration, briefly

Dana's intent: "Ops can refund part of a payment, for a damaged item or a missing line, instead of refunding everything and asking the customer to pay again." Elaboration runs as in Appendix A and produces PAY-491 with three ACs:

- AC1: Given a captured Payment, when ops issues a partial refund of an amount no greater than the refundable remainder, then a Refund is recorded and RefundIssued v1 is published.
- AC2: Given refunds already issued against a Payment, when ops requests a refund that would take the total refunded above the captured amount, then the request is rejected with REFUND_EXCEEDS_CAPTURE and no event is published.
- AC3: Given a refund request, when the provider returns a failure, then the Refund is recorded as failed and no ledger event is published.

Nobody asks how partial refunds relate to the full-refund feature the pod shipped last year, which stores a single `refunded_amount` field on the Payment. The agent does not ask either. `docs/domain/payments/model.md` does not mention `refunded_amount` at all; it was added before the pod kept domain docs. That gap is where the Bolt will fail.

## Tuesday 09:00 — The plan, approved

Lee asks for a plan with the [`bolt-plan`](../standards/skills/bolt-plan/SKILL.md) skill. The plan proposes a new `Refund` entity inside the Payment aggregate, a `refunds` list, and a `RefundPaymentService` that checks the remainder as `captured_amount - sum(refunds)`. The pod reviews it against the checklist, corrects one test row that named a behaviour instead of a failure, and approves at 09:35. The Files table lists seven files; the test strategy maps a test to each AC.

The plan is reasonable given the domain docs. It is wrong about the domain, because the docs are wrong. No plan review would have caught it without someone remembering `refunded_amount`.

## Tuesday 09:40 to 12:30 — Construction, green

Construction runs on the mid-tier model in slices. Sam reviews each one. By 12:30 the diff is 290 lines, every test passes, and the agent has drafted the PR. One detail matters later: the tests were generated inside the construction session by asking for "tests for the ACs", not with the [`tests-from-acs`](../standards/skills/tests-from-acs/SKILL.md) skill, because Lee wanted to save a step.

## Tuesday 12:40 — The mutation run

The PR pipeline runs diff-scoped mutation testing ([test review checklist](../standards/test-review-checklist.md#the-two-mechanical-checks)). Refunds move money, so the change is material and the gate is 85%.

```text
Mutation testing — changed files (material class, gate 85%)

src/payments/app/refund_payment_service.py   score 38%   (5 of 13 killed)
src/payments/domain/refund.py                score 50%   (3 of 6 killed)
Overall                                       41%         FAIL

Surviving mutants (selection):
  refund_payment_service.py:41   `<=` → `<`            survived
  refund_payment_service.py:39   `- sum(refunds)` → `` survived
  refund_payment_service.py:52   removed publish()     survived
```

Sam reads the tests with Priya. Every test starts from a Payment with no prior refunds, so removing the subtraction changes nothing they check. Two tests assert amounts copied from the code's own output rather than from the ACs. The test for AC3 checks the Refund's status but not that no event was published. The suite is green because it agrees with the code, not because it checks the intent. This is the generated-test problem from [Chapter 02](02-ways-of-working.md#testing-under-ai-dlc), found by the check that was designed to find it.

## Tuesday 13:05 — The real bug

Lee reruns test generation with the `tests-from-acs` skill. It writes AC2's negative path properly, starting from a Payment that already has a *full* refund from the old feature. That test fails: the new service ignores `refunded_amount`, so a payment that was fully refunded last month can be refunded again. In production that would be money leaving the company, one ticket at a time, with every existing test green.

The obvious fix is to fold `refunded_amount` into the new `refunds` list. That means a schema change and changing `test_full_refund_sets_refunded_amount`, an existing test. Both are stop conditions in the plan. The agent stops and reports, as it should.

## Tuesday 13:20 — The workaround, refused

The agent's report proposes a way to continue within the plan's file list: read both `refunded_amount` and `sum(refunds)` in the new service, and mark the old full-refund test `xfail` "until the model is unified in a follow-up." Sam catches it at once. An `xfail` on a money-path test is a disabled test, and a service that reads two sources for one fact is the bug moved elsewhere. The plan log records it:

```markdown
## Approval

- [x] Pod approved: Lee, Sam, Aisha, 2026-09-15 09:35
- Deviations during the Bolt:
  - 13:20 — Agent proposed dual-read of refunded_amount and refunds, with
    test_full_refund_sets_refunded_amount marked xfail. REFUSED by Sam, Aisha:
    disables a money-path test; two sources for one fact.
  - 14:10 — Bolt abandoned. Domain model does not state how full and partial
    refunds relate; fix needs expand/contract migration of refunded_amount.
    Unit re-sliced (see PAY-491 comments). Draft PR closed unmerged; branch kept
    for reference. Decided by Lee, Sam, Aisha; Dana informed 14:15.
```

## Tuesday 14:10 — Abandoning the Bolt

The pod spends fifty minutes on it and makes three decisions:

1. **Stop now.** Finishing today would mean a schema change, a backfill of every past full refund, and a domain question nobody in the room owns: is a full refund just a partial refund for the whole amount? That is a new plan, not a deviation from this one.
2. **Close the PR unmerged.** Nothing from the branch is cherry-picked. Construction is cheap, and the next attempt regenerates against the corrected domain model rather than inheriting code shaped by the wrong one.
3. **Re-slice the Unit.** Dana joins at 14:15 and confirms that a full refund is a partial refund for the whole amount. Aisha writes the invariant into `docs/domain/payments/model.md` in the same hour: *the sum of a Payment's refunds never exceeds its captured amount; `refunded_amount` is derived, never stored.*

| New Unit | Scope | Class |
|---|---|---|
| PAY-491a | Expand: add the Refund entity and table; write both representations for new full refunds | material |
| PAY-491b | Backfill: one Refund per historical full refund, as a separate idempotent job | critical |
| PAY-491c | Partial refunds on the new model: the original ACs, plus the invariant test | material |
| PAY-491d | Contract: stop writing `refunded_amount`, then drop it | material |

The sequence is the expand/contract pattern from [Chapter 07](07-devops-automation.md#data-and-schema-migrations). The cost of the abandoned Bolt: about five pod-hours and one afternoon's tokens.

## Wednesday and Thursday — The re-sliced work

PAY-491a is planned Wednesday morning with the corrected model in context; the migration is rehearsed on the masked production-scale snapshot in the ephemeral environment (four seconds, no table lock) and merges Wednesday afternoon. The backfill job runs Thursday morning in the change window the critical class requires: 18,412 Refund records created, each checked against `refunded_amount` before the job reports done. PAY-491c starts Thursday afternoon with tests from the `tests-from-acs` skill; its first mutation run scores 91%. PAY-491d waits for the next week, as contract steps should.

## Friday 14:00 — Consolidation

The pod fills in the [consolidation template](../standards/consolidation-template.md). The excerpt that matters:

```markdown
# Consolidation — Payments — 2026-W38

- Units completed: PAY-491a, PAY-491b · Bolts run: 4 · Bolts abandoned: 1

## What happened with the agents

- Tue 12:40 — generated tests green at 41% mutation score; tests started from
  no prior refunds and copied values from output — caught by mutation gate
- Tue 13:05 — new service ignored refunded_amount; fully refunded payments
  could be refunded again — caught by tests-from-acs negative path
- Tue 13:20 — agent proposed xfail on an existing money-path test — caught by
  Navigator, refused

## What reaches steering

| Lesson | Level of the fix | Change | PR | Golden task added? |
|---|---|---|---|---|
| Domain doc omitted a stored field that represents an existing fact | Domain docs | Invariant and derived-field note in payments/model.md; audit of payments aggregate fields against the doc | #1187 | no, because a doc change is verified by review |
| Tests generated ad hoc, not with tests-from-acs | CLAUDE.md | "Generate tests with the tests-from-acs skill; ad hoc test generation is not done" | #1188 | yes: tests-use-skill |
| Agent proposed disabling an existing test to stay within plan | CLAUDE.md | "Never mark an existing test skip or xfail; that is a stop condition, report it" | #1189 | yes: no-xfail-workaround |

## Review debt and pace

- Diffs merged with a review the pod would not stand behind: none
- Bolt integrity this week 0.75 (1 abandoned of 4); explained above, no action
```

Lee presents the abandoned Bolt at the next guild hour, with the mutation report and the refused deviation on screen. It is the most-watched recording of the month.

## What this example shows

- **The expensive mistake was in the docs, not the code.** The plan was right about the domain as written and wrong about the domain as built. The consolidation's first fix is to `model.md`, the fourth level of the [context-engineering hierarchy](03-tooling-strategy.md#the-context-engineering-hierarchy), because that is where the gap was.
- **Green tests were not evidence.** Only the mutation gate distinguished a suite that checks intent from one that agrees with the code. Without it, PAY-491 would have merged on Tuesday.
- **Stop conditions did their job twice.** Once when the agent halted rather than editing an existing test, and once when the pod refused the agent's way around the stop.
- **Abandoning was the cheap option.** Five pod-hours against refunds that could exceed captures in production. The Bolt-integrity dip is the metric working, not failing ([metrics reference](../standards/metrics-reference.md#flow)).
- **The bad week was published.** A failed Bolt shown at guild hour teaches every pod the same lesson for the price of one; hiding it would teach them to hide theirs ([Chapter 12](12-adoption-strategy.md#anti-patterns)).

## References

- Templates used: [Bolt plan](../standards/bolt-plan-template.md) · [Test review checklist](../standards/test-review-checklist.md) · [Consolidation](../standards/consolidation-template.md)
- Skills used: [`bolt-plan`](../standards/skills/bolt-plan/SKILL.md) · [`tests-from-acs`](../standards/skills/tests-from-acs/SKILL.md) · [`lesson-to-steering`](../standards/skills/lesson-to-steering/SKILL.md)
- Chapters exercised: [02](02-ways-of-working.md) · [03](03-tooling-strategy.md) · [07](07-devops-automation.md) · [12](12-adoption-strategy.md)
- Back to the [README](../README.md)
