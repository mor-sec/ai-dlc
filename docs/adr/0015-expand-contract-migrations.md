# 0015 — Require expand/contract, rehearsed, reversible migrations and separate backfill jobs for agent-written data changes

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook classified schema migrations as material and backfills as critical ([Chapter 07](../../playbook/07-devops-automation.md#risk-based-gating)), protected `migrations/` from unapproved edits, and made a schema change a Bolt plan stop condition. It said nothing about how a migration should be written. Agents write migrations that are correct on an empty database: a one-step rename, a column added with a default that rewrites the table, a backfill inside the migration. These pass every test in CI and fail in production under load, or break the old code still running during a canary.

Data changes are also the one thing the pipeline's automatic rollback cannot undo.

## Decision

We will require agent-written data changes to follow expand/contract across separate deploys, never edit applied migrations, ship a down step or a written forward fix, be rehearsed on a production-scale masked snapshot with timing and locks reported in the PR, and run backfills as separate idempotent, batched jobs.

The rules live in [Chapter 07, Data and schema migrations](../../playbook/07-devops-automation.md#data-and-schema-migrations) and belong in each repo's steering file; hooks block edits to applied migrations.

## Options considered

### Option A — Expand/contract with rehearsal and separate backfills  ← chosen

- Pros: every step is compatible with the code beside it, so canary and rollback keep working; lock and duration problems appear in the PR, not in production.
- Cons: a rename becomes four deploys across two or more Units; production-scale snapshots in ephemeral environments cost storage and time.

### Option B — Keep the gate only: a named approver reviews each migration

- Pros: no new rules; relies on experienced reviewers.
- Cons: the reviewer sees SQL, not the lock it takes on a hot table; review quality varies.
- Rejected because: the defects that matter depend on data size and concurrent traffic, and a diff shows neither.

### Option C — Maintenance windows for schema changes

- Pros: simple; allows breaking changes.
- Cons: batches changes into windows, against the continuous-deploy cadence; downtime.
- Rejected because: it brings back release batching for the most common kind of material change.

## Consequences

- Positive: zero-downtime schema change becomes the default; migration risk is measured before approval.
- Negative: more, smaller Units for structural changes; the platform pod must provide masked production-scale snapshots.
- Follow-ups: a migration-lint step (lock and rewrite detection) in the reference pipeline; steering lines in the CLAUDE.md template.

## Revisit when

The database platform offers online schema change that removes lock and rewrite risk, or rehearsal cost in ephemeral environments exceeds its value for a quarter.
