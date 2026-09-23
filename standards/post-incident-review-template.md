---
owner: platform-enablement
audience: developers, on-call engineers, security engineers
reviewed: 2026-09-24
review-cadence: quarterly
---

# Post-Incident Review Template

The blameless review that closes an incident and feeds the Operations-phase loop back into steering ([Chapter 07](../playbook/07-devops-automation.md#ai-in-operations-the-third-ai-dlc-phase)). Audience: the pod that owns the affected context, the incident commander, and security engineering when the incident was a security finding ([Chapter 06](../playbook/06-security-shift-left.md#operations-continuous-verification)).

Where it lives: `docs/incidents/<yyyy-mm-dd>-<slug>.md` in the owning repo, the same file the [`incident-investigate`](skills/incident-investigate/SKILL.md) skill started as a timeline draft. Written within five working days of resolution, reviewed by PR with the incident commander and the owning pod's domain anchor.

The **class-level fix** section is what makes this document different from a standard post-mortem. Every incident ends with the question: *what change makes this whole class of incident impossible, not just this one?* The answer goes to the [`lesson-to-steering`](skills/lesson-to-steering/SKILL.md) skill.

---

```markdown
# Post-incident review — <yyyy-mm-dd> — <short title>

- Severity: <SEV1–4> · Duration: <detected → resolved> · Commander: <name>
- Contexts affected: <bounded contexts> · Customers affected: <number or scope>
- Units of Work and PRs involved: <PROJ-…, PR links>

## Summary

Three sentences: what users experienced, what caused it, what stopped it.

## Timeline

From the incident-investigate draft, corrected by the humans who were there.
Times in UTC.

| Time | Event | Source |
|---|---|---|
| <hh:mm> | <alert fired / deploy / hypothesis / action / resolution> | <link> |

## What the agent did

- First investigation note posted at: <time>, <minutes> after the alert
- Ranked hypotheses: <which was right, and its rank>
- Anything the agent missed or got wrong, and why (missing access, missing
  context, wrong assumption): <…>

## Contributing factors

No person is a root cause. List the conditions that let the fault reach
production and stay there, including agent-specific ones: a steering line
missing or ignored, a stop condition that did not fire, a test that passed
with the bug present, an autonomy level that was too high.

1. <factor> — <evidence>
2. …

## Class-level fix

The one change that prevents the class. Pick the cheapest effective level:
a steering line, a skill, a Semgrep rule or architecture test, a test
template, a golden task, an alert, or a paved-road module.

- The class: <stated generally, e.g. "handlers that emit an event before
  the transaction commits">
- The fix: <one line> — level: <…> — PR: <link, drafted with lesson-to-steering>
- Golden task guarding it: <name in evals/, or why none>

## Action items

| Action | Owner | Due | Jira |
|---|---|---|---|
| … | … | … | … |

## What went well

<Detection, rollback, communication: what to keep doing.>
```

---

**Review checklist** (before the PR merges):

- [ ] No contributing factor names a person as the cause
- [ ] The class-level fix is stated generally enough to prevent a *different* instance of the same class
- [ ] The fix PR exists as a draft, not an intention
- [ ] Every action item has an owner, a date, and a Jira key
- [ ] Restricted data (customer records, credentials) is referenced, not pasted ([Chapter 06](../playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership))
