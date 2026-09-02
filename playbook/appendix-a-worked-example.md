---
owner: platform-enablement
audience: developers, product owners, engineering leaders
reviewed: 2026-09-02
review-cadence: quarterly
---

# Appendix A — One Unit of Work, end to end

A single Unit of Work followed from Monday's intent to Friday's steering update, with every artifact filled in. Audience: anyone who has read [Chapters 01](01-ai-dlc-methodology.md) and [02](02-ways-of-working.md) and wants to see what the method looks like on a real Tuesday. Nothing here is new; it is the templates, used.

The scenario: the Payments pod (three developers, product owner Dana, QA Priya, security engineer Marcus on call) at a company whose checkout runs on an event-driven architecture per [Chapter 04](04-architecture.md). Names and numbers are illustrative; the shapes are exact.

## Monday 09:40 — Mob Elaboration

Dana brings the intent: "Customers whose card payment fails should be able to retry without re-entering details. Support tickets about failed payments are 11% of volume and most are just people trying again."

The Driver (Sam, rotating) opens a session in plan mode with the `jira-elaboration` skill and the intent paragraph. Within four minutes the agent has drafted a Unit of Work and asked its clarifying questions. The pod keeps the questions in the log ([Chapter 01](01-ai-dlc-methodology.md#tips--tricks)):

- Retry against the same payment method only, or allow switching to another card?
- Is a retry a new `Payment` aggregate or a state transition on the failed one?
- What happens when the original authorization hold has expired before the retry?
- Should a retry be possible from the email notification, or only in-app?

The room decides in eight minutes: same method only; a state transition on the existing aggregate (the invariant "one order, one payment" in `docs/domain/payments/model.md` settles it); an expired hold means a fresh authorization, which is a different Unit; in-app only for now. Each decision lands in the Out of scope list, which is the section the agent would otherwise fill for you.

### Threat-model pass (10 minutes)

Sam runs the `threat-model` skill against the draft. Marcus reviews on the shared screen:

```markdown
## Threat model summary

- Assets touched: stored card token (PCI scope), Payment state, order total
- Trust boundaries crossed: customer session → checkout API; checkout → payment provider
- Top abuse cases:
  1. Replaying retry to probe whether a stolen card token is still live
  2. Retrying after the order total changed (price-drop race)
  3. Retry of a payment the caller does not own (IDOR on payment id)
- Mitigations → carried as acceptance criteria: AC4 (rate limit), AC3 (total recheck), AC2 (ownership)
- Security escalation: yes — money movement. Reviewer at merge gate: Marcus
```

Priya notes that AC4 needs a negative test, not just the happy path. That line goes into the Unit of Work as written.

### The approved Unit of Work

```markdown
# PAY-482 — Customers can retry a failed card payment

## Intent

Customers whose card payment fails at checkout can retry with the same card,
without re-entering details. 11% of support volume is failed-payment tickets;
most resolve on a manual second attempt. Owner: Dana (product).

**Success looks like:** failed-payment tickets fall below 5% of volume within
30 days of release; retry success rate is visible on the payments dashboard.

## Domain context

- Bounded context: payments → docs/domain/payments/model.md
- Key terms: Payment, PaymentAttempt, AuthorizationHold (language.md)
- Events consumed: OrderTotalChanged v1. Published: PaymentRetryRequested v1 (new),
  PaymentSucceeded v2, PaymentFailed v2
- Relevant ADRs: 0007 (one Payment per Order), 0012 (idempotency keys on all commands)
- ⚠ Cross-context? No. Order total is read from the last OrderTotalChanged event.

## Stories & acceptance criteria

### Story 1 — Customer can retry a failed payment
- AC1: Given a Payment in state Failed, when the customer requests a retry,
  then a PaymentAttempt is created against the same method and
  PaymentRetryRequested v1 is published.
- AC2: Given a Payment the caller does not own, when a retry is requested,
  then 404 and no event is published.
- AC3: Given the order total has changed since the failed attempt, when a retry
  is requested, then the retry is rejected with RETRY_TOTAL_CHANGED and no
  event is published.
- AC4: Given three failed retries in 24 hours, when a fourth is requested,
  then 429 and no event is published.

### Story 2 — Ops can see retry history per order
- AC5: Given an order with retries, when ops opens the order in the back office,
  then each attempt shows timestamp, outcome, and provider reason code.

## Risks & open questions

| Risk / question | Owner | Resolution needed by |
|---|---|---|
| Provider rate-limits repeated auths on one token | Sam | plan gate |
| Dashboard metric needs a new Snowflake view | Priya | before merge of Story 2 |

## Out of scope

- Switching payment method on retry
- Retry after authorization-hold expiry (new Unit: PAY-483)
- Retry from email links
- Automatic (system-initiated) retries

## Execution notes

- Estimated Bolts: 2 (Story 1; Story 2)
- Material-change classification expected: material (money movement)
- Feature flag: payments.retry_enabled
```

Elaboration checklist ticked at 10:35. Dana moves PAY-482 to `Ready`. Total elaboration time: 55 minutes.

## Tuesday 09:00 — Bolt plan

Sam starts the Bolt with the Unit of Work as the session's task context, pulled from Jira via MCP, and asks for a plan in plan mode on the frontier tier. The agent reads `docs/domain/payments/`, ADRs 0007 and 0012, and the event schemas before proposing. First draft arrives at 09:14; the pod reviews it against the [plan review checklist](../standards/bolt-plan-template.md) and sends back two corrections: the plan had put the rate limiter inside the aggregate (it belongs in the application service, per the layering rule in `CLAUDE.md`), and the AC3 test row said "asserts total is rechecked" rather than naming a failure. Second draft approved at 09:41.

```markdown
# Bolt plan — PAY-482 (slice 1 of 2)

- Unit of Work: PAY-482 — Customers can retry a failed card payment
- Bolt id: B-2026-09-02-a
- Driver: Sam · Navigator: Lee · Domain anchor: Aisha
- Model tier: frontier for this plan; mid-tier for construction

## Scope of this Bolt

- In: Story 1, AC1–AC4
- Deferred to the next Bolt: Story 2 (AC5), Snowflake view
- Out of scope: see the Unit of Work

## Approach

Add a `retry()` transition to the Payment aggregate guarded by the Failed state
and the ADR-0007 invariant; put ownership, total recheck, and the 3-per-24h rate
limit in `RetryPaymentService` (application layer), keyed by the ADR-0012
idempotency key. Publish PaymentRetryRequested v1 from the existing outbox.
The arguable choice: the rate limit counts attempts per Payment, not per card
token — simpler, and the token-level limit already exists at the provider.

## Files

| Path | Change | Why |
|---|---|---|
| src/payments/domain/payment.py | modify | `retry()` transition + invariant check |
| src/payments/app/retry_payment_service.py | new | ownership, total recheck, rate limit, idempotency |
| src/payments/api/routes.py | modify | POST /payments/{id}/retry behind flag |
| schemas/payments/PaymentRetryRequested.v1.json | new | additive event; routine for consumers |
| src/payments/infra/outbox.py | modify | register new event type |
| tests/payments/test_retry_payment.py | new | AC1–AC4 |
| tests/contracts/test_payment_retry_requested_v1.py | new | generated from schema |
| docs/domain/payments/model.md | modify | Failed → Retrying transition |
| docs/domain/payments/events.md | modify | catalog entry |

## Test strategy

| AC | Test (name) | What production failure it catches |
|---|---|---|
| AC1 | test_retry_from_failed_creates_attempt_and_publishes | Retry silently no-ops; customer sees success with no charge |
| AC1 | test_retry_from_non_failed_state_rejected | Double-charging a Succeeded payment |
| AC2 | test_retry_other_customers_payment_is_404 | IDOR: charging someone else's card |
| AC3 | test_retry_after_total_changed_rejected | Charging the old (wrong) amount after a price change |
| AC4 | test_fourth_retry_in_24h_is_429_and_no_event | Card-probing via unbounded retries |
| AC4 | test_third_retry_in_24h_still_allowed | Off-by-one locks out legitimate customers |

Contract tests regenerate from schemas/payments/PaymentRetryRequested.v1.json.

## Risk and gate

- Classification: material (money movement) → gate: Marcus (security) + one pod reviewer
- Rollback: flip payments.retry_enabled off; no schema migration involved
- Threat-model mitigations carried as ACs: AC2, AC3, AC4

## Stop conditions

The agent halts and asks for a plan update — it does not proceed — if any of these occur:

- The diff passes ~500 changed lines
- A file outside the Files table needs editing
- An existing test must be changed rather than added
- A new dependency or a schema change is required
- An accepted ADR would be contradicted
- Two consecutive fixes fail the same test

## Approval

- [x] Pod approved: Sam, Lee, Aisha, 2026-09-02 09:41
- Deviations during the Bolt:
  - 13:55 — added idempotency-key dedupe in the outbox for PaymentRetryRequested
    after AC4's test exposed a double-emit on concurrent retries. One extra file
    (src/payments/infra/outbox_dedupe.py). Approved by Lee, Aisha.
```

## Tuesday 09:45 to 15:00 — Mob Construction

The session switches to the mid-tier model and implements in slices, one Files-table row group at a time. Lee, as Navigator, reviews each slice as it lands on the shared screen. Three moments worth recording:

- **11:20, a plausible-name catch.** The generated route handler called `payment.can_retry()`, a method that does not exist on the aggregate. It read perfectly. Lee caught it by checking the aggregate, not the handler ([Chapter 02](02-ways-of-working.md#review-culture-the-biggest-change), "distrust plausible names"). The fix was one line; the lesson went into the pod journal.
- **13:50, a stop condition fires.** The AC4 concurrency test failed twice in a row with a double-emitted event. Per the plan, the agent stopped and reported instead of trying a third fix. The pod took ten minutes, agreed the outbox needed a dedupe keyed on the idempotency key, and appended the deviation to the plan. The agent resumed against the updated plan.
- **14:30, a test review.** The agent's first version of `test_retry_after_total_changed_rejected` set up the changed total and asserted the rejection, but it also asserted the *exact* error message string. Lee had it assert the error code instead: a copy edit should not break a money-path test.

Diff at 15:00: 412 changed lines across ten files, inside the budget. The agent runs the full suite and the local hooks (lint, Semgrep, secrets), then drafts the PR.

## Tuesday 15:10 — The PR

```markdown
PAY-482 Customers can retry a failed card payment (slice 1/2)

Unit of Work: PAY-482 · Bolt plan: docs/bolts/B-2026-09-02-a.md
Classification: material (money movement) · Approvers: @marcus (security), @lee

## What and why
Adds a customer-initiated retry for payments in state Failed, same method only,
behind `payments.retry_enabled`. Intent and success metric in PAY-482.

## Acceptance criteria
- [x] AC1 — test_retry_from_failed_creates_attempt_and_publishes, test_retry_from_non_failed_state_rejected
- [x] AC2 — test_retry_other_customers_payment_is_404
- [x] AC3 — test_retry_after_total_changed_rejected
- [x] AC4 — test_fourth_retry_in_24h_is_429_and_no_event, test_third_retry_in_24h_still_allowed

## Deviation from plan
13:55 — outbox dedupe on idempotency key added after AC4 exposed a double-emit
under concurrent retries. One extra file. Re-approved in the plan's log.

## Rollback
Flip `payments.retry_enabled` off. No migration.

## Docs updated
docs/domain/payments/model.md (new transition), docs/domain/payments/events.md
(PaymentRetryRequested v1). No ADR needed: no recommendation changed.
```

CI runs the [reference pipeline](07-devops-automation.md#the-reference-pipeline-github-actions). Static checks and tests pass in six minutes. The ephemeral environment comes up; Priya walks the retry flow by hand and confirms the 429 on the fourth attempt. Semgrep raises one finding on the new route: a custom rule flags any handler touching `payments` that lacks the ownership decorator. The agent's triage note points out the check is inside the service, not the decorator; Marcus agrees but asks for the decorator anyway, for consistency with the rule. Five-line change, re-review, approved.

The path-based classifier labels the PR `material` because it touches `src/payments/`. Marcus's approval satisfies the named-approver gate at 16:40. Merge queue, canary, progressive rollout with the flag still off.

## Wednesday 10:00 — Release and the loop closing

Dana flips `payments.retry_enabled` to 10% of traffic. The deploy event from the previous evening is already on PAY-482 in Jira, posted by the GitHub for Jira integration:

```text
Deployed to production — v2026.09.02-3 — 2026-09-02 17:12 UTC — PR #1187
```

Lead time for the Unit's first slice, `Elaboration` timestamp to production deploy: 31 hours. Story 2 runs as Bolt B-2026-09-03-a on Wednesday and merges the same day.

## Friday 14:00 — Consolidation

Thirty-minute retro, focused on the agent collaboration. Two items reach the steering file, following the [context-engineering hierarchy](03-tooling-strategy.md#the-context-engineering-hierarchy):

1. **The plausible-name catch becomes a CLAUDE.md line** in the payments repo: "Before calling a method on an aggregate, read the aggregate. Do not infer methods from names; `Payment` has exactly the transitions listed in docs/domain/payments/model.md."
2. **The double-emit becomes a test template.** Every new command handler gets a concurrent-duplicate test generated from a skill, so the next pod does not rediscover it at 13:50.

The `questions the AI asked` log gains four entries. The pod journal for the week records the 11:20 and 13:50 moments and the fact that the plan's stop condition worked exactly once and paid for itself.

## What this example shows

- **The expensive hour was 09:00 to 09:41.** Two plan corrections cost 27 minutes; either one found in the diff would have cost the afternoon.
- **Every gate fired for a reason.** The plan gate caught a layering error, the stop condition caught a concurrency bug, human review caught an invented method, the pipeline caught a missing decorator. None of them was theater.
- **The artifacts are the audit trail.** Intent, threat model, plan, deviation, PR, deploy event: a reader with no memory of the week can reconstruct why the code is the way it is, and so can the next agent session.

## References

- Templates used: [Unit of Work](../standards/unit-of-work-template.md) · [Bolt plan](../standards/bolt-plan-template.md) · [CLAUDE.md](../standards/claude-md-template.md)
- Chapters exercised: [01](01-ai-dlc-methodology.md) · [02](02-ways-of-working.md) · [06](06-security-shift-left.md) · [07](07-devops-automation.md) · [08](08-github-jira.md)
- Back to the [README](../README.md)
