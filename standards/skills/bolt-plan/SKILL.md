---
name: bolt-plan
description: Produce the Bolt plan for a Unit of Work at the start of a Bolt, in plan mode, before any generation. Use when the Driver starts a Bolt or when a stop condition has fired and the plan needs updating. Not for trivial bounded fixes that skip the plan gate.
---

# Bolt plan

Turns an approved Unit of Work into the plan the pod approves before construction: scope, approach, files, tests, risk class, stop conditions. The plan is the highest-leverage artifact of the day, so this skill spends its effort on reading before proposing.

## Inputs

- The Unit of Work, by Jira key, pulled from Jira (MCP) or the draft in context: intent, stories and ACs, domain context, threat-model summary, out-of-scope list, execution notes.
- The repo's `CLAUDE.md`: commands, layering rules, security constraints, protected paths.
- `docs/domain/<context>/model.md`, `language.md`, and `events.md` for every context the Unit names.
- Every ADR the Unit lists, plus a scan of `docs/adr/` titles for any it missed.
- The [Bolt plan template](../../bolt-plan-template.md), and the previous slice's plan if this is slice 2 or later (`docs/bolts/`).

## Outputs

- `docs/bolts/<bolt-id>.md`, in the template's shape, with the Approval section unticked and the deviations log empty.
- A short list of open questions for the pod, if any input was ambiguous. Ask them before finishing the plan; do not guess in the plan.

## Steps

1. Read all inputs before writing anything. Note every aggregate, event, and ADR the stories touch; these must appear by name in the Approach.
2. Choose the slice. If the Unit's execution notes estimate more than one Bolt, take the first story group that delivers a testable outcome on its own. State what is deferred.
3. Write the Approach in three sentences maximum, naming the one design choice a reviewer would want to argue about. If there is no arguable choice, say so.
4. Build the Files table by tracing each AC to the code path it changes. Every row has a "why"; every row maps to at least one AC or to a docs update the Definition of Done requires (`docs/domain/`, event catalog).
5. Build the Test strategy table with one row per AC minimum, and a row for the negative path of every AC with a "must not happen" clause. Each row's last column names a production failure, not a behaviour. Contract tests are listed as regenerated from their schema.
6. Classify the change using Chapter 07's classes: any touch to migrations, auth, IAM, network IaC, public contracts, or money paths is at least material. Name the approver the class requires. Write the rollback as one action.
7. Copy the standard stop conditions from the template verbatim, then add any Unit-specific ones (a named file that must not change, a query that must stay under a limit).
8. Estimate the diff size from the Files table. If it is likely to exceed ~500 lines, split the slice now and say so.
9. Write the file. Stop. **Do not begin implementation**; the pod approves the plan and ticks the Approval box.

## Rules

- Never invent a file, method, or event. Every path in the Files table exists or is explicitly marked `new`; every event is in `events.md` or marked as a new schema.
- Respect accepted ADRs. If the natural design contradicts one, say so as a question for the pod; do not route around it silently.
- Prefer the domain invariant over new code. If `model.md` already forbids a state, the plan tests the invariant rather than adding a check.
- Frontier tier for this skill. Plans are the worst place to economise.
- On a re-plan after a stop condition: change only what the stop condition requires, append to the deviations log with the time and reason, and leave the rest of the plan untouched so the diff of the plan is reviewable.

## Verification

Before handing over:

- [ ] Every AC in scope appears in the Test strategy table at least once
- [ ] Every Files row has a why, and none is outside the named bounded context without a stated reason
- [ ] Approach names aggregates, events, and ADRs explicitly
- [ ] Classification matches the paths touched (protected paths are never routine)
- [ ] Rollback is a single action
- [ ] Stop conditions present, standard set intact
- [ ] Approval box unticked; the plan ends with `Pod approval pending`

The plan is a proposal until the pod ticks the box.
