---
owner: platform-enablement
audience: engineering leaders, pod members
reviewed: 2026-09-02
review-cadence: quarterly
---

# Metrics Reference

The one definition of every metric the playbook mentions, with its source system, cadence, and the direction that means health. Audience: engineering leaders reading dashboards, pods reading their own showback, and anyone building the reporting. Chapters [02](../playbook/02-ways-of-working.md#metrics-that-matter-and-ones-that-dont), [03](../playbook/03-tooling-strategy.md#unit-economics-cost-per-validated-unit-of-work), [07](../playbook/07-devops-automation.md#tips--tricks), [08](../playbook/08-github-jira.md#reporting-that-matches-the-method), and [11](../playbook/11-learning-paths.md) say *why* each matters; this file says *what it is*, so two pods reporting the same number mean the same thing.

Two rules apply to all of them. First, the allocation unit is the Unit of Work, identified by its Jira key; anything that cannot be attributed to a Unit is overhead and is reported as such. Second, no metric here is a target for individuals. They describe the system; using them to rank people corrupts every one of them within a quarter.

## Flow

| Metric | Definition | Source | Cadence | Healthy direction |
|---|---|---|---|---|
| **Units of Work completed** | Epics reaching `Done` per pod per calendar week. `Done` requires the deploy event for user-facing Units ([Chapter 08](../playbook/08-github-jira.md#anti-patterns)). | Jira | weekly | Up, then stable. A jump with rising rework rate means Units got smaller, not faster. |
| **Lead time** | Timestamp of the Epic entering `Elaboration` to the first production deploy event carrying its key. Report median and p90. | Jira + GitHub deployment events | per Unit, reviewed weekly | Down. The one number leadership watches. |
| **Bolt integrity** | Stories per `bolt-id` finished ÷ started. | Jira | per Bolt | Near 1.0. Persistent < 0.8 means Units are sliced too large. |
| **Time to first human review** | PR marked ready-for-review to first substantive review comment or approval-with-comment. Report p90. | GitHub | per PR, weekly | Down. The AI-DLC-specific bottleneck: generation waits on review, never the reverse. |

## Quality

| Metric | Definition | Source | Cadence | Healthy direction |
|---|---|---|---|---|
| **Rework rate** | (Issues reopened + PRs reverted) ÷ Units completed, per pod. | Jira + GitHub | monthly | Down. The earliest signal that elaboration is being skipped or rushed. |
| **Defects escaping to production** | Bugs linked to a Unit and opened after its deploy event, per Unit. | Jira | monthly | Down. |
| **Change failure rate** | Deploys causing a rollback, hotfix, or incident ÷ total deploys. | Deploy events + incident tickets | monthly | Down. DORA definition, unchanged. |
| **MTTR** | Incident open to resolved, median. | Incident tooling | monthly | Down. DORA definition, unchanged. |
| **Review depth** | Substantive findings per review, where substantive means it changed the diff or the plan. Nits and approvals without comment count zero. | GitHub review comments with a `finding` label or reaction | weekly | Stable and non-zero. Zero for a pod for two weeks is review theater, not perfect code. |

## Learning and security

| Metric | Definition | Source | Cadence | Healthy direction |
|---|---|---|---|---|
| **Steering updates per week** | Merged PRs touching `CLAUDE.md`, `.claude/skills/`, or the Semgrep rules repo, org-wide. | GitHub | weekly | Non-zero every week. Zero for a month means learning has stalled ([Chapter 11](../playbook/11-learning-paths.md#the-knowledge-system-how-learning-compounds)). |
| **Vulnerability classes eliminated** | Count of finding types that now have a steering line, a Semgrep rule, and a test template, and have produced zero new findings for a quarter. | Security engineering register | quarterly | Up. Measures compounding; raw finding counts do not. |
| **Time to first solo Bolt** | A developer's start date in a pod to the first Bolt they drive without a supervising Driver. | Pod journal | per person | 2 to 4 weeks. Longer means the paved road is not paved. |
| **Questions-log growth** | New entries in the "questions the AI asked" log per Unit. | Elaboration notes | monthly | Falling slowly over a year, as intent-writing improves. |

## Cost

| Metric | Definition | Source | Cadence | Healthy direction |
|---|---|---|---|---|
| **Cost per validated Unit of Work** | Agent tokens + warehouse credits + CI minutes tagged to the Unit's Jira key, ÷ 1, reported per Unit and as a pod median. | Provider billing export, warehouse query history, CI usage API, joined on the key | monthly showback per pod | Trend, no target. Compare against rework rate: cheap Units with high rework are the expensive ones. |
| **Token spend per pod** | Daily agent tokens per pod against a 30-day baseline. | Provider billing export | daily anomaly alert | Within baseline. A spike means an agent looping or a Unit sliced too large ([Chapter 07](../playbook/07-devops-automation.md#ai-in-operations-the-third-ai-dlc-phase)). |
| **Cost per answered prototype question** | Warehouse credits + tokens for a prototype Unit, from its first Bolt to its kill/keep/promote decision. | As above, filtered to `prototype` repos | per prototype | Visible. Makes the kill outcome look cheap and the immortal prototype look expensive ([Chapter 05](../playbook/05-rapid-prototyping.md#tips--tricks)). |

## What is not measured

Lines of code, prompts per developer, "AI usage %", story points, individual review counts. Each is either meaningless under AI-DLC or actively corrupting, and dashboards that show them will be optimised for.

## The pilot baseline

[Chapter 11](../playbook/11-learning-paths.md#the-enablement-program-three-waves) asks for a measured before-and-after. Before Wave 3 starts, capture for the pilot pod's previous quarter under the old process:

1. Lead time (median, p90), from ticket creation to production, using whatever timestamps exist
2. Change failure rate and MTTR
3. Rework rate, approximated as reopened tickets ÷ closed tickets
4. Escaped defects per quarter
5. Total delivery cost for the quarter: seats + cloud + CI, since tokens did not exist yet

Record them in the pilot charter with the method used, so the after-numbers are computed the same way. A pilot that cannot show its baseline cannot show anything.
