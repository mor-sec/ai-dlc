---
owner: platform-enablement
audience: developers, engineering leaders
reviewed: 2026-09-03
review-cadence: quarterly
---

# Model Selection Reference

The current mapping of model tiers to actual models, and of every AI-DLC use case to a tier and an effort level. **This file goes stale by design.** The stable principles live in [Chapter 03](../playbook/03-tooling-strategy.md#model-selection-and-token-economics); this table is reviewed quarterly (see front-matter) and updated whenever a provider ships, reprices, or retires a model. If `reviewed` is more than a quarter old, distrust the table and update it. Any change to it is a steering event: run the [steering evals](steering-evals.md) against the new assignment before merging.

## Current tier assignments (as of 2026-09-03)

| Tier | Model | Relative input cost (Haiku = 1x, as of 2026-09-03) | Constraints that affect assignment |
|---|---|---|---|
| **Frontier-plus** | Claude Fable 5.1 | 10x | Requires 30-day data retention; unavailable under zero-retention terms until the [vendor governance](../playbook/03-tooling-strategy.md#vendor-governance) review clears it. Single turns on hard tasks can run many minutes. May end a turn with a `refusal` stop reason, so harnesses run with fallbacks enabled. No priority tier. |
| **Frontier** | Claude Opus 5 | 5x | Thinking on by default; effort `low` to `max`. Fast mode (research preview) runs the same model faster at frontier-plus pricing, for moments when the pod is waiting on the shared screen. |
| **Mid-tier** (default) | Claude Sonnet 5 | 2x | Effort `low` to `max`; 1M context. The workhorse; most tokens land here. |
| **Small/fast** | Claude Haiku 4.5 | 1x | 200K context and no effort parameter. Not for whole-repo tasks. Always paired with mechanical verification. |

Relative multipliers are recorded because they rot slowly; absolute prices are not, because they rot fast. Check the provider's pricing page for numbers. Zero-retention organizations have no frontier-plus tier: Opus 5 at effort `xhigh` is their frontier, and every row below still holds with that substitution.

## Use case to model

Effort is the setting that controls how much the model thinks per request; `n/a` means the model has no effort parameter.

### Inception

| Use case | Model | Effort | Why |
|---|---|---|---|
| Mob Elaboration for a new or cross-context area; event-storming; context-map proposals | Fable 5.1 (Opus 5 `xhigh` under zero retention) | `high` | The worst place to economise: a wrong decomposition costs weeks, not a pod-day |
| Mob Elaboration for a routine Unit inside a known context | Opus 5 | `high` | Frontier judgment without the long-turn model |
| Threat-model pass ([`threat-model`](skills/threat-model/SKILL.md)) | Opus 5 | `high` | Security judgment inside a ten-minute ritual; frontier-plus turns are too long for it |
| Bolt plan, single context ([`bolt-plan`](skills/bolt-plan/SKILL.md)) | Opus 5 | `xhigh` | Plan quality compounds through everything downstream |
| Bolt plan, cross-context or legacy carve | Fable 5.1 | `high` | The riskiest plans in the method |

### Construction

| Use case | Model | Effort | Why |
|---|---|---|---|
| Routine construction inside an approved plan | Sonnet 5 | `medium`; raise to `high` when output needs correction | The plan carries the intelligence |
| Construction that fights back after two corrections | Opus 5, in a new session | `xhigh` | The escalation rule; a new session because caches are model-scoped |
| Tests from acceptance criteria; mutation-survivor analysis ([`tests-from-acs`](skills/tests-from-acs/SKILL.md)) | Sonnet 5 | `high` | Bounded by the plan's test table |
| Fixtures, producers, consumers, and contract tests generated from a schema | Haiku 4.5 | n/a | Mechanical; the schema verifies it |
| Fresh-eyes and adversarial review | Opus 5 | `xhigh` | The reviewer never runs below the generator |
| Scanner triage: clustering duplicate findings | Haiku 4.5 | n/a | Volume work |
| Scanner triage: disposition and false-positive rationale | Sonnet 5 | `medium` | Needs judgment, not frontier judgment |
| PR descriptions, changelog entries, same-PR doc updates | Haiku 4.5 | n/a | Cheap, and a human reads every word |
| CI headless chores; nightly doc-staleness sweep | Haiku 4.5 via the Batch API | n/a | Non-interactive work at half price |
| Prototype build: Streamlit, Snowpark ([Chapter 05](../playbook/05-rapid-prototyping.md)) | Sonnet 5 | `high` | Bounded, fast, throwaway |

### Operations

| Use case | Model | Effort | Why |
|---|---|---|---|
| Incident investigation, first note within ten minutes ([`incident-investigate`](skills/incident-investigate/SKILL.md)) | Opus 5 | `high` | The time-box rules out frontier-plus turn lengths |
| Post-incident root cause when the first pass failed | Fable 5.1 | `max` | Correctness over cost, and no time-box |
| Post-mortem timeline draft; monthly journal digest | Sonnet 5 | `low` | Summarisation |
| Lesson to steering ([`lesson-to-steering`](skills/lesson-to-steering/SKILL.md)) | Opus 5 | `high` | Choosing the right control is judgment |
| Cost-anomaly and log clustering | Haiku 4.5 | n/a | Volume work, alert-verified |

### Legacy modernization

| Use case | Model | Effort | Why |
|---|---|---|---|
| Comprehend: per-program summaries at scale | Haiku 4.5 via the Batch API | n/a | Thousands of programs; sample-verified by veterans |
| Comprehend: business-rules extract with code pointers | Sonnet 5 | `high` | Precision matters; volume is moderate |
| Carve dispositions (rewrite, transform, wrap, retire) | Fable 5.1 | `high` | Multi-year consequences |
| Characterization-test generation | Sonnet 5, Haiku 4.5 for the bulk | `medium` | The old system is the oracle; verification is mechanical |
| Java upgrades and framework migrations | Sonnet 5 | `high` | Well-specified, high-verification |
| Parallel-run discrepancy analysis | Opus 5 | `high` | Every discrepancy is a business rule |

### Learning and steering

| Use case | Model | Effort | Why |
|---|---|---|---|
| Steering evals ([steering-evals.md](steering-evals.md)) | The model under test, at its assigned effort | as assigned | The suite validates the assignment, so it runs on it |
| Onboarding Q&A over the playbook | Sonnet 5, with the playbook as a cached prefix | `low` | The cache does the work |

## Standing rules (from Chapter 03 — repeated because they get violated)

1. **Reviewer ≥ generator.** The review side never runs on a cheaper model than the generation side.
2. **Escalate, don't pre-optimize.** Default mid-tier; escalate to frontier when output needs repeated correction.
3. **Frontier for anything whose failure costs a pod-day** — plans, architecture, security judgment. Frontier-plus for anything whose failure costs weeks.
4. **Effort is the first lever, model the second.** Before dropping a tier, measure the assigned model at a lower effort on real tasks. On the current generation, lower effort often matches the previous generation at high effort, at a fraction of the cost.
5. **Caches are model-scoped.** Escalation means a new session, never a mid-session model swap, and a pod does not alternate models inside one Bolt.
6. **Cost per completed task, never per request.** A cheaper model that needs two more rounds is the expensive one.
7. **Non-interactive work goes through the Batch API.** Nightly sweeps, bulk comprehension, mass test generation: half price, no one is waiting.
8. **Frontier-plus needs governance first.** Its retention requirement is cleared in the vendor governance review before any pod assigns it.

## Cost accounting

- **Allocation unit:** the Unit of Work (Jira key). Tokens + warehouse credits + CI minutes roll up via the [traceability chain](../playbook/08-github-jira.md).
- **Showback:** each pod sees its own cost per validated Unit of Work, monthly ([metrics reference](metrics-reference.md)).
- **Anomaly watch:** token spend per pod is baselined; spikes alert like any cloud-cost anomaly ([Chapter 07](../playbook/07-devops-automation.md)).
- **What we don't do:** per-seat cost caps, per-prompt quotas, or downgrading review models to save money — all three optimize the number while degrading the system that makes the number cheap.

## Change log

| Date | Change | Steering fixes needed |
|---|---|---|
| 2026-09-03 | Added the frontier-plus tier (Claude Fable 5.1), the use-case table with effort levels, rules 4–8, and relative cost multipliers | Evals not yet in place; first run due with the next tier change |
| 2026-08-30 | Initial version: Claude 5 family tier assignments | — |
