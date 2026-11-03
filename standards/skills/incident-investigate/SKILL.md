---
name: incident-investigate
description: First-line investigation of a production alert or incident. Correlate logs, traces, metrics, recent deploys, and open changes into a ranked hypothesis with an evidence bundle, and draft the timeline for the post-mortem. Use the moment an alert fires or an incident is declared, before the human responder joins. Never use it to take remediating action; that is a runbook or a human.
---

# Incident investigation

Gives the on-call human a hypothesis and the evidence for it instead of a blank dashboard. The agent investigates; the human decides; pre-approved runbooks act.

## Inputs

- The alert or incident: alert name, SLO or symptom, time of first breach, affected service or bounded context.
- Observability access via MCP: structured logs with correlation IDs, traces across context boundaries, metrics and SLO burn rates, deploy markers ([Chapter 07](../../../playbook/07-devops-automation.md#observability-requirements)); the current backend and server are in the [observability stack reference](../../observability-stack.md).
- GitHub deployment events and open PRs for the affected repos in the last 24 hours; feature-flag changes in the same window.
- `docs/domain/<context>/events.md` and the context map, to know which upstream contexts feed the affected one.
- The runbook index, to recognise a known failure class.
- The incident channel or ticket, for what humans have already observed.

## Outputs

- An **investigation note** posted to the incident ticket, in this shape:
  - Symptom: what is breaching, since when, blast radius (users, contexts, regions)
  - What changed: deploys, flag flips, config or IaC changes, upstream schema versions in the window, each with a link
  - Hypotheses, ranked, each with the evidence for and against and a one-line test that would confirm it
  - Recommended next action for the human: which runbook if a class matches, or which hypothesis to test first
  - What was ruled out and why
- A **timeline draft** (`docs/incidents/<date>-<slug>.md` or the incident tool), appended as the incident proceeds, for the post-mortem.

## Steps

1. Establish the symptom precisely before looking for causes: which SLO, which percentile, which cohort, from which minute. Pull the burn-rate chart and the first breaching trace.
2. Build the change window: every deploy marker, flag change, IaC apply, and upstream event-schema version bump in the affected and upstream contexts for the last 24 hours. Order them. Most incidents sit within an hour of a change.
3. Follow one correlation ID from a failing request end to end across contexts. Note where latency or errors first appear; that is usually the boundary to look at, not the service that alerted.
4. Form hypotheses. For each, write the evidence for, the evidence against, and the cheapest confirming test (a query, a trace filter, a comparison with the previous deploy). Rank by evidence, not by plausibility.
5. Check the runbook index. If the symptom and top hypothesis match a runbook, say so by name; the human triggers it.
6. Post the note. Keep investigating while the human acts, and append to the timeline: each action taken, by whom, at what time, and what the metrics did after.
7. When the incident is resolved, finish the timeline with the resolving action and hand off to `lesson-to-steering` with the question Chapter 07 asks: what steering line, test template, alert, or module change makes this class impossible?

## Rules

- **Never take remediating action.** No restarts, rollbacks, scaling, flag flips, or config changes. Recommend; the human or a pre-approved runbook acts. Read-only tool access is the norm for this skill.
- Evidence before narrative. Every claim in the note links to a log query, a trace, a metric, or a deploy event. A hypothesis with no evidence is listed as untested, not omitted.
- Report absence honestly. "No deploy in the window" and "no correlation ID reached the payment provider" are findings.
- Do not anchor on the alerting service. The alert fires where the symptom is measured, which is often downstream of the cause.
- Time-box the first note to ten minutes from the alert. A partial note in ten minutes beats a complete one in forty. Say what is still being checked.
- Never paste secrets, tokens, or full PII records from logs into the note. Reference by correlation ID.

## Verification

Before posting the first note:

- [ ] Symptom stated with SLO, cohort, and start time
- [ ] Change window listed with links, or an explicit "no changes found in window"
- [ ] At least one end-to-end trace followed and its first anomaly named
- [ ] Hypotheses ranked, each with for, against, and a confirming test
- [ ] A recommended next action, and a named runbook if one matches
- [ ] No action taken; access was read-only

The note is a hypothesis until the human confirms it.
