# Session log — 2026-11-03: observability decision, ADR acceptance, and repo housekeeping

A record of one working session between a playbook maintainer (Stephen Morleys) and Claude Code (Fable 5.1), for anyone later asking why ADR 0027 exists, why ten ADRs flipped to Accepted on one day, and what the first green CI run fixed. Chapters, standards, and ADRs win any disagreement with this file.

## Summary

The maintainer asked where observability fits in the playbook, whether to decide on a technology, and whether to start with Amazon CloudWatch Omni. The answer was that Chapter 07 already held the vendor-neutral requirements, that the missing pieces were a named backend and the agents' own telemetry, and that the playbook's existing pattern for dated technology choices applies: an ADR plus a `standards/` reference with a `reviewed:` date. The maintainer confirmed Omni lands on a blank slate, with no incumbent platform, and approved that shape.

Outcome, all pushed to `main` with CI green:

- [ADR 0027](../adr/0027-opentelemetry-contract-and-cloudwatch-omni-default-backend.md): OpenTelemetry as the instrumentation contract, CloudWatch Omni as the default backend for AWS-hosted work.
- [Observability stack reference](../../standards/observability-stack.md): the contract, the current backend, the facts that rot, pod onboarding, and the quarterly review.
- Chapter 07 gained a fourth observability requirement, that the agents are instrumented too; Chapter 03 gained a stack-table row; README, START-HERE, and the `incident-investigate` skill link the standard.
- Ten ADRs (0006, 0019 to 0027) flipped from Proposed to Accepted.
- `prince2-7/` passes markdownlint, which turned repo-wide lint from 165 errors to 0 and gave the repo its first green CI run.
- The docs workflow's actions moved to v5, clearing the Node.js 20 deprecation.
- Factory job 002 (audience lines in `standards/`) was retried, reviewed, approved, and merged.

## Decisions

| Decision | Where |
|---|---|
| OpenTelemetry is the contract; the backend is configuration | ADR 0027, Chapter 07 |
| CloudWatch Omni is the default backend; classic CloudWatch, third-party platforms, and self-hosting were considered and rejected | ADR 0027 |
| Dated Omni facts (access model, pricing model, framework list, open gaps) live in the standard, reviewed quarterly | `standards/observability-stack.md` |
| The coding agent's telemetry rides the same pipeline, tagged with pod and Unit of Work key | Chapter 07 requirement 4 |
| The maintainer accepts agent-drafted ADRs by flipping the status; 0026 and 0027 record the acceptance date | ADRs 0026, 0027 |

## Changes by commit

| Commit | What |
|---|---|
| `2b86e26` | ADR 0027, the observability stack standard, Chapter 07 and 03 edits, README, START-HERE, incident skill link |
| `4474fde` | `prince2-7/`: blank lines from `markdownlint --fix` across 18 files, three fence languages, two list blank lines, one renamed duplicate heading |
| `d684ee5` | ADRs 0006 and 0019 to 0027 set to Accepted |
| `316034d` | `actions/checkout` and `actions/setup-node` to v5 |
| `2ff16e0` | Merge of `factory/002-standards-audience-lines` after the code review and approver passed |
| This session's last two commits | Factory state for jobs 001 and 002; this record, the PR template's structure check, two CLAUDE.md layout lines, the root images moved or removed |

## Judgement calls

- ADR 0027 was written as Proposed, following ADR 0026, and flipped the same day on the maintainer's instruction.
- The two resource attribute names in the observability standard, `team.id` for the pod and `aidlc.unit_of_work` for the Unit, are the standard's own convention, not AWS's.
- To retry factory job 002, `main` was merged into the job branch first, because the code reviewer runs the four checks inside the job's worktree and the branch predated the lint fix. The factory skill has no step for this; it is an open item below.
- `prince2-7/SKILL.md` was read-only on disk. It was made writable for three small edits and set back.
- The duplicate PRINCE2 poster at the repo root was removed; `prince2-7/assets/` holds the identical file. The AI-DLC one-pager moved to `docs/assets/`.

## Verification

All four checks from CLAUDE.md pass locally and in CI on every push of the session: markdownlint over 100 files, the link checker over 114 files, seven Mermaid diagrams, and the structure check over 16 playbook and 17 standards files. CI runs 41555303675, 41555612479, and 41556180149 completed with success.

Not verified: that Claude Code's OpenTelemetry export appears in a CloudWatch Omni space. That is ADR 0027's first follow-up, and the metrics reference keeps its billing-export source until it passes.

## Sources

- [CloudWatch Omni documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-omni.html) · [Omni pricing](https://aws.amazon.com/cloudwatch/omni/pricing/) · [Claude Code telemetry in CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/coding-agents-claude-code.html) · [AWS observability round-up, August to September 2026](https://aws.amazon.com/blogs/mt/this-month-in-aws-observability-august-september-2026/)

## Open items

From the gap sweep at the end of the session, in rough priority:

- Run the ADR 0027 spike and move the metrics reference's cost rows to the agent's telemetry if it passes.
- Refresh [`standards/model-selection.md`](../../standards/model-selection.md), which still names Opus 5, Sonnet 5, and Haiku 4.5, with its own steering-eval run.
- Ship the skills the playbook names but does not have: `jira-elaboration`, `snowflake-prototype`, `event-storm`, `from-schema`, `eval-set`; and an `evals/` folder with golden tasks for this repo's own steering.
- Define what a prompt version is and give prompt changes a risk class; both are undefined in Chapters 07 and 13.
- Add a review-cadence staleness check to `scripts/check-structure.py`, with a review rota before it turns red on 2026-12-02.
- Move the dated DocLang facts in Chapter 09 to a `standards/` reference.
- Glossary entries for golden task, showback, risk class, correlation ID, test integrity, deploy marker, degraded mode, and critical change.
- Factory skill: a `retry` command for a missing review file, and a merge of `main` at the start of every builder round.
- Decide whether the playbook needs a regulatory section (GDPR, DPIA, EU AI Act), and where `prince2-7/` ultimately lives.
