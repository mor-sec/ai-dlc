---
owner: platform-enablement
audience: engineering leaders, executive sponsors
reviewed: 2026-09-18
review-cadence: quarterly
---

# Pilot Charter Template

The contract that ends Wave 1 of the [enablement program](../playbook/11-learning-paths.md#the-enablement-program-three-waves): which pods, on what work, measured how, with what budget and guardrails, reviewed when. Audience: the sponsor who signs it and the stakeholders who hold them to it. How to earn the signatures: [Chapter 12](../playbook/12-adoption-strategy.md#earning-stakeholder-buy-in).

Where it lives: `docs/pilots/<yyyy-qn>-charter.md` in the steering repo, merged by PR with every signatory as a reviewer. Once merged, the success criteria and baseline are not edited; changes during the quarter are appended under **Amendments** with a date and a reason, so the review reads results against what was agreed up front.

The **success criteria** and **baseline** sections are the ones that matter most. A charter without them lets anyone decide afterwards what success meant.

---

```markdown
# Pilot charter — <yyyy-qn> — <short name>

- Sponsor: <name, role>
- Program owner: <name>
- Review date: <YYYY-MM-DD> (end of quarter)
- Status: Draft | Signed | Under review | Closed

## Why this pilot

Two or three sentences in the sponsor's words: the business outcome sought and why
now. Use the organization's AI-DLC narrative (playbook chapter 12).

## Pods and people

| Pod | Members (Driver/Navigator rotation) | Domain anchor | QA | Security engineer | Released from |
|---|---|---|---|---|---|
| <pod name> | <names> | <name> | <name, share> | <name> | <team; manager who agreed> |

Include at least one respected skeptic across the pilot pods.

## Scope

- In: <services, bounded contexts, or legacy carve; named repos>
- First Units of Work: <Jira keys or intents>
- Out of scope: <payments core, production data classes, anything with high blast radius>
- Why this scope is low blast radius and still real work: <one paragraph>

## Baseline (captured before the pilot starts)

Per standards/metrics-reference.md, "The pilot baseline", for <team>'s previous quarter:

| Metric | Value | Method and source |
|---|---|---|
| Lead time, median / p90 | | |
| Change failure rate | | |
| MTTR | | |
| Rework rate (approximation) | | |
| Escaped defects per quarter | | |
| Total delivery cost (seats + cloud + CI) | | |

## Success criteria

Stated as thresholds against the baseline, agreed before the start. Three to five, no more.

| # | Criterion | Threshold | Measured by |
|---|---|---|---|
| S1 | Lead time median improves | <e.g. at least 30% lower than baseline> | Jira + deploy events |
| S2 | Quality does not regress | <change failure rate and escaped defects at or below baseline> | As baseline |
| S3 | Review stays real | <review depth non-zero every week> | GitHub findings label |
| S4 | Learning compounds | <steering updates merged every week> | GitHub |
| S5 | People can repeat it | <each pod member completes a solo Bolt> | Pod journal |

**Stop criteria:** conditions under which the sponsor pauses the pilot early, for example
a security incident attributable to agent access, or change failure rate above
<threshold> for two consecutive weeks.

## Budget

| Item | Amount | Notes |
|---|---|---|
| Agent tokens | <per month> | Showback per pod; daily anomaly alert |
| Seats and licenses | | |
| Enablement time | 20% of pilot capacity | Steering, skills, journals, community rituals |
| Platform pod (Wave 2) | <people × weeks> | |

## Guardrails

- Vendor governance ADRs merged: <links> (data retention, excluded repos, degraded mode)
- Agent permissions and hooks: <link to paved-road baseline>
- Risk-based gating in the pipeline: <link>
- No metric in this charter is used to evaluate individuals.

## Stakeholders and communication

| Stakeholder | Named person | What they asked to see | How and when they see it |
|---|---|---|---|
| Finance | | | Monthly leadership update |
| Security and risk | | | |
| Architecture | | | |
| People and HR | | | |

Open Bolt slots: <day, time, how to book>. Guild hour: <day, time>.

## Review

At the review date the program owner reports each success criterion as met, not met, or
inconclusive, with the numbers, in writing, and recommends one of: scale (name next
quarter's seeded pods), extend (one more quarter, with the reason), or stop.

## Signatures

| Role | Name | Date |
|---|---|---|
| Executive sponsor | | |
| Engineering manager(s) releasing people | | |
| Security | | |
| Finance | | |

## Amendments

- <YYYY-MM-DD> — <change> — <reason> — <approved by>
```

---

**Why a charter and not a slide deck:** a deck persuades once and is then forgotten. A charter in git has reviewers, a history, and a review date, so the quarter ends with a decision against criteria rather than a debate about what the pilot was meant to show.
