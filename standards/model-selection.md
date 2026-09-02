---
owner: platform-enablement
audience: developers, engineering leaders
reviewed: 2026-08-30
review-cadence: quarterly
---

# Model Selection Reference

The current mapping of model tiers to actual models and indicative costs. **This file goes stale by design** — the stable principles live in [Chapter 03](../playbook/03-tooling-strategy.md#model-selection-and-token-economics); this table is reviewed quarterly (see front-matter) and updated whenever a provider ships or reprices. If `reviewed` is more than a quarter old, distrust the table and update it.

## Current tier assignments (as of 2026-08-30)

| Tier | Model | Use for | Indicative cost posture |
|---|---|---|---|
| Frontier | Claude Opus 5 (Fable 5 where available) | Elaboration, Bolt planning, review, threat models, incident investigation | Highest per-token; cheapest per avoided mistake |
| Mid-tier (default) | Claude Sonnet 5 | Routine construction inside an approved plan; prototype builds | The workhorse — most tokens land here |
| Small/fast | Claude Haiku 4.5 | Bulk mechanical work: test-mass generation, triage, CI chores, doc sweeps | Volume pricing; always paired with mechanical verification |

Any change to this table is a steering event: run the [steering evals](steering-evals.md) against the new model before merging, and record how many steering fixes it needed in the change log below.

Check current pricing at the provider's page rather than recording numbers here — recorded prices are the part that rots fastest. What belongs in this file is the *assignment*: which model currently occupies which tier.

## Standing rules (from Chapter 03 — repeated because they get violated)

1. **Reviewer ≥ generator.** The review side never runs on a cheaper model than the generation side.
2. **Escalate, don't pre-optimize.** Default mid-tier; escalate to frontier when output needs repeated correction.
3. **Frontier for anything whose failure costs a pod-day** — plans, architecture, security judgment.

## Cost accounting

- **Allocation unit:** the Unit of Work (Jira key). Tokens + warehouse credits + CI minutes roll up via the [traceability chain](../playbook/08-github-jira.md).
- **Showback:** each pod sees its own cost per validated Unit of Work, monthly.
- **Anomaly watch:** token spend per pod is baselined; spikes alert like any cloud-cost anomaly ([Chapter 07](../playbook/07-devops-automation.md)).
- **What we don't do:** per-seat cost caps, per-prompt quotas, or downgrading review models to save money — all three optimize the number while degrading the system that makes the number cheap.

## Change log

| Date | Change |
|---|---|
| 2026-08-30 | Initial version: Claude 5 family tier assignments |
