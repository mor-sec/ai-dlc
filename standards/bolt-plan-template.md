---
owner: platform-enablement
audience: developers
reviewed: 2026-09-29
review-cadence: quarterly
---

# Bolt Plan Template

The artifact behind AI-DLC's plan-approval gate ([Chapter 01](../playbook/01-ai-dlc-methodology.md#the-validation-gates)): what the agent proposes, and the pod approves, before any significant generation starts. The Driver asks for it in plan mode at the start of every Bolt ([Chapter 02](../playbook/02-ways-of-working.md#a-day-inside-a-bolt)); reviewing it is the highest-leverage hour of the day, so it is short enough to review properly.

Where it lives: `docs/bolts/<bolt-id>.md` in the owning repo, committed in the Bolt's PR so the plan is traceable from the Jira key and diffable against what was actually built. Bolt ids are `B-<date>-<letter>` (`B-2026-09-02-a`); the same id goes in the Jira `bolt-id` field ([Chapter 08](../playbook/08-github-jira.md#mapping-ai-dlc-onto-jira)).

The **stop conditions** section is the part that makes "plan then execute" a mechanism rather than an intention: it tells the agent, in advance, exactly when to halt and re-plan instead of silently drifting.

---

```markdown
# Bolt plan — <PROJ-123> (slice <n> of <N>)

- Unit of Work: <PROJ-123 — title>
- Bolt id: B-YYYY-MM-DD-a
- Driver: <name> · Navigator: <name> · Domain anchor: <name>
- Model tier: frontier for this plan; <mid-tier> for construction (standards/model-selection.md)

## Scope of this Bolt

- In: <Story 1, AC1–AC3>
- Deferred to the next Bolt: <Story 2>
- Out of scope: see the Unit of Work; anything not listed here is not built.

## Approach

<Three sentences maximum. Name the aggregates, events, and ADRs this touches,
and the one design choice a reviewer would want to argue about.>

## Files

| Path | Change | Why |
|---|---|---|
| <path> | new / modify / delete | <one clause> |

## Test strategy

| AC | Test (name) | What production failure it catches |
|---|---|---|
| AC1 | <test_name> | <the failure, not the behaviour> |

Contract tests regenerate from <schema>; nothing hand-edited.

## Fan-out

Optional. Delete this section for a single-session Bolt, and always for a
critical-class Bolt. At most three lanes run at once (Chapter 02, Fan-out
inside a Bolt). Lane 0 holds anything the other lanes share and is reviewed
before they start. No file appears in two lanes.

| Lane | Files (rows from the Files table) | Starts after | Tests (rows from Test strategy) |
|---|---|---|---|
| 0 — shared contract | <schema, port signature, migration> | plan approval | <contract tests> |
| A | <paths> | lane 0 reviewed | <AC refs> |
| B | <paths> | lane 0 reviewed | <AC refs> |

## Risk and gate

- Classification: routine / material / critical (Chapter 07) → gate: <who approves>
- Rollback: <one line — a routing change, a flag flip, a revert>
- Threat-model mitigations carried as ACs: <AC refs>

## Stop conditions

The agent halts and asks for a plan update — it does not proceed — if any of these occur:

- The diff passes ~500 changed lines
- A file outside the Files table needs editing
- An existing test must be changed rather than added
- A new dependency or a schema change is required
- An accepted ADR would be contradicted
- Two consecutive fixes fail the same test (restart the session with what was learned,
  then escalate the model tier, then the pod)
- A lane needs a file owned by another lane, or a change to lane 0

## Progress

Updated at the end of every session, so the next session, the next Driver, or
tomorrow's pod resumes from here rather than from memory.

- Done and reviewed: <slices or lanes, with commit refs>
- Next: <the slice the next session starts>
- Open: <questions waiting on the pod or product>

## Approval

- [ ] Pod approved: <names>, <YYYY-MM-DD HH:MM>
- Deviations during the Bolt (appended as they happen, each re-approved):
  - <time> — <what changed and why> — approved by <name>
```

---

**Plan review checklist** (the pod, before ticking Approval):

- [ ] Scope maps to named ACs in the Unit of Work; nothing in Files lacks an AC or a "why"
- [ ] Approach names the aggregates and events, and respects the ADRs listed in the Unit of Work
- [ ] Every test row states a *failure it catches*, not a behaviour it asserts
- [ ] Classification is right for the paths touched (migrations, auth, IAM, public contracts are never routine)
- [ ] Rollback is a real, one-line action
- [ ] The plan fits in one Bolt; if not, split the slice now, not at 4pm
- [ ] If the plan fans out: no file is in two lanes, everything the lanes share is in lane 0, and the Bolt is not critical-class

A plan that fails this checklist costs an hour to fix. The same mistake found in the diff costs a day.
