---
owner: platform-enablement
audience: developers, domain anchors, QA
reviewed: 2026-09-24
review-cadence: quarterly
---

# Consolidation Template

The record of a pod's Friday consolidation ([Chapter 02](../playbook/02-ways-of-working.md#the-weekly-rhythm)): the retro on how the collaboration with agents went, the steering and skill changes that came out of it, and the week's journal entry. Audience: the pod, the person writing the monthly digest ([Chapter 11](../playbook/11-learning-paths.md#the-knowledge-system-how-learning-compounds)), and agents, which read past journals as context.

Where it lives: `docs/journal/<yyyy>-w<ww>.md` in the pod's main repo, one file per week, merged by PR before the pod leaves on Friday. This file *is* the pod journal; there is no separate one.

The **what reaches steering** section is the one that matters. A consolidation that produces no steering, skill, test-template, or domain-doc change either had a perfect week or did not look hard enough. The second is more common.

---

```markdown
# Consolidation — <pod name> — <yyyy>-W<ww>

- Units completed: <PROJ-123, PROJ-124> · Bolts run: <n> · Bolts abandoned: <n>
- Present: <names> · Facilitator (rotating): <name>

## What happened with the agents

Three to five moments from the week, each one line with a link to the PR,
Bolt plan, or transcript. Include at least one where the agent went wrong
and how it was caught (or was not).

- <day time> — <what happened> — caught by <plan gate / stop condition /
  Navigator / QA / pipeline / production> — <link>

## What reaches steering

Each lesson goes to the cheapest fix that prevents the class, in the order
of the context-engineering hierarchy (Chapter 03): prompt/Unit of Work,
CLAUDE.md, skill, domain docs, codebase.

| Lesson | Level of the fix | Change | PR | Golden task added? |
|---|---|---|---|---|
| <the class of mistake, not the instance> | CLAUDE.md / skill / domain doc / test template / codebase | <one line> | <link> | yes / no, because <reason> |

Draft each change with the lesson-to-steering skill; one PR per lesson.

## Questions the AI asked

New entries for the log, with the Unit they came from. A question that
recurs across Units is a missing line in the Unit of Work template or in
docs/domain/.

- <PROJ-123> — "<question, verbatim>" — <answered how>

## Review debt and pace

- Diffs merged with a review the pod would not stand behind: <none / list, with a plan to re-review>
- Review budget exceeded on: <days, or none>
- Time to approve by hour of day, review depth by day of week: <link to the dashboard; one sentence on the trend>
- Rotation held? <yes / no, and why not>

## Next week

- Units lined up for Monday's elaboration: <PROJ-…>
- One thing the pod will do differently: <one line>
```

---

**Consolidation checklist** (before the PR merges):

- [ ] Every agent failure listed has a row in *What reaches steering*, or a written reason why no fix is possible
- [ ] Each steering change is a separate PR, drafted and linked
- [ ] Review debt is either empty or has a named re-reviewer and a date
- [ ] Nothing in this file is confidential beyond the repo's own classification ([Chapter 06](../playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership)); link to transcripts rather than pasting them
