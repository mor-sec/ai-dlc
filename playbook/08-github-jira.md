# 08 — GitHub + Jira Integration

Jira holds **intent** (Units of Work, Bolts, business traceability); GitHub holds **execution** (code, review, CI, deploys). The integration's job is to make the thread from business intent to production deploy unbroken and machine-readable — for managers, auditors, and agents alike.

## Mapping AI-DLC onto Jira

Keep native issue types; change their semantics. Renaming (Epic→Unit of Work) is optional cosmetics; the semantics below are not.

| AI-DLC concept | Jira construct | Conventions |
|---|---|---|
| Business intent / initiative | Initiative (or Epic at portfolio level) | Owned by product; links to the intent doc |
| **Unit of Work** | Epic | Body follows the [Unit of Work template](../standards/unit-of-work-template.md); carries intent, acceptance criteria, threat-model summary, domain-context links |
| Story / slice | Story under the Epic | Generated during Mob Elaboration; acceptance criteria testable as written |
| **Bolt** | Fixed-length *iteration* is gone — represent Bolts as a `bolt-id` label or field on the stories executed together | Don't force Bolts into Jira Sprints; a two-week container around a two-day cycle is pure friction. If your reporting insists on Sprints, use one-week sprints as a *reporting shell* only. |
| Ops / incident follow-ups | Bug/Task linked to the incident ticket | Feed the next Mob Elaboration |

**Workflow states — few and honest:** `Elaboration → Ready → In Bolt → In Review → Done`. Transitions are automated by the integration wherever possible (below); a state a human must remember to update will be wrong by Thursday.

## The integration itself

Use the official **GitHub for Jira** app (two-way sync of branches, commits, PRs, deploys into Jira's development panel) plus Jira Automation rules:

1. **Issue key everywhere** — this is the one human discipline the whole system rests on:
   - Branch: `feature/PROJ-123-short-slug` (branch created from the Jira issue or by the agent, so the key is never mistyped)
   - Every commit message and PR title starts with `PROJ-123`
   - Enforce with a CI check (regex on PR title + branch), not with nagging
2. **Automation rules:**
   - Branch created → issue to `In Bolt`
   - PR opened (non-draft) → `In Review`; PR merged → `Done` when acceptance criteria checklist is complete
   - Deploy to production (via GitHub deployment events) → comment on the issue with version/environment — closing the intent→production loop
   - Issue moved to `Ready` without template-mandated fields → bounce back with a comment
3. **Smart commits** (`PROJ-123 #comment ...`) are fine for comments; avoid using them for transitions (state changes should come from PR/deploy events — objective, not typed).

## Agents in the loop

Via the Jira MCP server ([Chapter 03](03-tooling-strategy.md)):

- **Elaboration:** the agent drafts the Unit of Work (stories, acceptance criteria, risks) directly into Jira during the mob session; humans edit and approve in the room. No transcription step.
- **Bolt start:** the agent pulls the Unit of Work from Jira as its primary task context — meaning Jira quality *is* agent context quality; a lazy ticket now costs machine time, not just human time.
- **Bolt end:** the agent updates the issue — work summary, PR links, deviations from plan — and drafts the PR description with the issue key and an acceptance-criteria checklist.
- **Guardrail:** agents comment and update fields; **state transitions and closure remain event-driven or human**. An agent declaring its own work "Done" is a self-graded exam.

## Traceability: the audit trail for free

With the conventions above, every production change answers, mechanically:

```
Why?  Jira Initiative → Unit of Work (intent, approver)
What? → Stories → acceptance criteria → threat model
How?  → Branch → agent plan (in PR description) → commits → human review
Proof → CI checks → security scans → deploy event → version in production
```

This satisfies most audit and change-management regimes (separation of concerns: agent proposes, named human approves, pipeline verifies, deploy event recorded) without a single manually-written change record. Export-friendly: everything is API-queryable from two systems.

## Reporting that matches the method

- **Throughput:** Units of Work done per week per pod (Epic completion) — not story points ([Chapter 02](02-ways-of-working.md)).
- **Lead time:** Jira `Elaboration` timestamp → GitHub production-deploy event. The one metric leadership should watch.
- **Bolt integrity:** stories per `bolt-id` started vs. finished — detects Units sliced too large.
- **Elaboration quality:** rework rate (issues reopened / PRs reverted) per Unit — the earliest signal that Mob Elaboration is being skipped or rushed.

## Anti-patterns

- **Jira as a second codebase.** Duplicating design detail into tickets that lives better in `docs/` — link, don't copy. The ticket holds intent and acceptance; the repo holds truth.
- **Sprint cosplay.** Forcing Bolts into two-week sprints with velocity charts; you'll re-derive Scrum within a quarter and lose the cadence.
- **Manual state hygiene.** Weekly "please update your tickets" — automate the transition or delete the state.
- **The unlinked hotfix.** Emergency changes bypassing issue keys destroy the audit trail exactly where auditors look first. Make the hotfix path create its issue automatically (agent drafts it retroactively within the hour).
- **Two sources of "done."** Jira says Done, the deploy failed. Tie `Done` to deploy events, not merge alone, for anything user-facing.

## Tips & tricks

- **Dev-panel first:** train the team to read the Jira development panel (branches, PRs, deploys inline) instead of tab-switching; it sells the integration on day one.
- **A `jira-elaboration` skill** that takes a raw intent paragraph and produces the templated Unit of Work + child stories in one shot is the single best onboarding artifact for product owners.
- **Label agent-authored issues** (`ai-drafted`) — makes review-before-Ready visible and lets you measure how much elaboration drafting has shifted to agents.
- **Quarterly link audit:** sample 10 production deploys, walk each back to intent. Any break = a process bug to fix that week.

## References

- [GitHub for Jira](https://github.com/marketplace/jira-software-github) · [Jira Automation docs](https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/)
- Previous: [Chapter 07 — DevOps](07-devops-automation.md) · Next: [Chapter 09 — Documentation Standards](09-documentation-standards.md)
