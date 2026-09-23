---
owner: platform-enablement
audience: community of practice coordinators, sponsors, champions
reviewed: 2026-09-18
review-cadence: quarterly
---

# Community of Practice Charter Template

The founding document of an AI-DLC community of practice: why it exists, who does what, which rituals it runs, how contributions reach every pod, and how its health is judged. Audience: the coordinator who writes it in Wave 2, and the champions and members who hold the community to it. Design rationale: [Chapter 12](../playbook/12-adoption-strategy.md#the-community-of-practice).

Where it lives: `docs/community/charter.md` in the steering repo, alongside the experiment register (`docs/experiments/register.md`), the FAQ, and the digests. Revised at the community's quarterly retrospective by PR.

The **what we are not** section matters more than it looks. It is what stops the community turning into an approval gate.

---

```markdown
# <Organization> AI-DLC community of practice — charter

- Sponsor: <name, role>
- Coordinator: <name> (term: <YYYY-MM-DD> to <YYYY-MM-DD>) · Successor shadowing: <name>
- Chartered: <YYYY-MM-DD> · Last revised: <YYYY-MM-DD>
- Channel: <chat channel> · Calendar: <link>

## Purpose

One or two sentences. For example: practitioners help each other get better at
AI-driven development, share what works and what does not, and turn lessons into
steering that every pod inherits within a week.

## What we are not

- Not an approval gate. We do not sign off any team's steering, tools, or experiments.
- Not the platform pod. The platform pod owns and merges the paved road; we
  contribute to it through normal PRs.
- Not a training department. Learning paths and practica are in playbook chapter 11;
  we are where practitioners keep learning afterwards.

## Roles

| Role | Current holder(s) | Time budget | Responsibilities |
|---|---|---|---|
| Sponsor | | 1 hour/month | Protect time budgets; remove blockers; receive the quarterly report |
| Coordinator | | ~10% | Calendar, experiment register hygiene, digest rota, quarterly report |
| Champions | <name — team> (one per team or department) | ~5% | Office hours, local narrative, bring objections back |
| Members | Open to anyone | Voluntary | Attend, ask, contribute |

Time budgets are agreed with each person's manager and recorded here.

## Rituals

| Ritual | Cadence | Length | Owner | Output |
|---|---|---|---|---|
| Guild hour | Biweekly | 60 min | Rotating pod | Recording + notes in the digest |
| Office hours | Weekly | 60 min | Champions (rota) | FAQ entries for repeated questions |
| Open Bolt slots | Weekly per pilot pod | 75 min | Pod domain anchor | Observer questions logged |
| Monthly digest | Monthly | 30 min read | Rotating author | `docs/digest/<yyyy-mm>.md` |
| Innovation day | Quarterly | 1 day | Coordinator | One written finding per experiment |
| Community retrospective | Quarterly | 45 min | Coordinator | PR revising this charter |

## How contributions flow

1. Untested idea: add a row to the experiment register with a question, horizon,
   owner, time limit, and the evidence that would change the paved road.
2. Finding or tested lesson: draft with the `lesson-to-steering` skill, run steering
   evals, open a PR to the steering repo; the platform pod reviews within a week.
3. Killed experiment: finding published in the next digest.
4. Any question answered twice in the channel becomes a FAQ entry or a steering PR.

## Health

Reviewed at the quarterly retrospective and reported to the sponsor, using the
adoption and community metrics in standards/metrics-reference.md:

| Metric | Last quarter | This quarter | Note |
|---|---|---|---|
| Steering contributors outside the platform pod | | | |
| Experiment decisions (kill / keep / adopt) | | | |
| Guild hour attendance from outside pilot pods | | | |
| Teams with a champion | | | |
| Pods seeded | | | |

We do not report member counts, message volume, or AI usage percentages.

## Lifecycle

Current stage: Seed | Grow | Sustain | Renew or retire

Retire or merge criteria: <for example, AI-DLC is the default way of working in all
engineering teams for two consecutive quarters and the rituals have been absorbed
into the engineering practice forum>.
```

---

**Why a written charter for a voluntary community:** without one, the community's shape is whatever its most energetic member wants, and it either dies when that person moves on or grows into the approval gate nobody wanted. The charter makes rotation, time budgets, and the "not a gate" rule explicit before they are tested.
