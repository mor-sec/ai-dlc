---
name: threat-model
description: Draft a STRIDE-lite threat model from a Unit of Work during Mob Elaboration, writing mitigations as acceptance criteria. Use when a Unit of Work has been drafted and before it moves to Ready. Not for reviewing a finished diff; use an adversarial review prompt for that.
---

# Threat model (elaboration pass)

Produces the "Threat model summary" section of a Unit of Work, with each mitigation written as a testable acceptance criterion, so security enters before generation and gets implemented and tested for free downstream.

## Inputs

- The Unit of Work markdown: intent, domain context, stories with acceptance criteria. From the Jira Epic description, or the draft in the current session.
- The repo's `CLAUDE.md` security section: the controls that actually exist (query builder, authZ pattern, secrets manager, validation points).
- `docs/domain/<context>/model.md` and `events.md` for the bounded context(s) named in the Unit of Work.

## Outputs

- The filled `## Threat model summary` section, in the shape the [Unit of Work template](../../unit-of-work-template.md) defines, inserted into the Unit of Work.
- New or amended acceptance criteria in the stories, one per mitigation, in Given/When/Then form.
- A `Security escalation: yes/no` line, with the reviewer field left blank for a human.

## Steps

1. Read the inputs. Do not start listing threats before reading the security section of `CLAUDE.md` and the domain model; the point is to cite real controls and real invariants.
2. List **assets touched**: data classes (PII, payment instruments, credentials, money balances), aggregates whose invariants the stories change, and any external system called.
3. Trace each story's flow and mark every **trust boundary crossed**: user session → API, service → service, service → data store, anything leaving the perimeter (provider, email, webhook).
4. At each boundary, ask the six STRIDE questions (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege). Keep a threat only if it has a plausible actor and a concrete path through *this* Unit's stories. Target **2 to 5 abuse cases**. Twenty is a workshop, not an elaboration pass.
5. For each abuse case, write **one mitigation as an acceptance criterion**: `Given <state>, when <action>, then <observable outcome> and <what must not happen>`. Include the negative outcome ("and no event is published") so the test cannot pass by accident.
6. Set **escalation**: if assets include authN/authZ, money movement, PII, or cryptography, write `Security escalation: yes` and leave `Reviewer at merge gate:` blank. Otherwise `no`.
7. Insert the section into the Unit of Work. **Do not transition the Jira issue** and do not mark the checklist item done; the pod does both in the room.

## Rules

- Only cite controls the repo has. An invented WAF or rate limiter in a mitigation creates false assurance; if a control is missing, say so as a risk and propose the AC anyway.
- Mitigations are criteria, not advice. "Validate input" is not an AC; "Given a retry request with a non-UUID payment id, when submitted, then 400 and no lookup is performed" is.
- Prefer the domain invariant over a new check. If `model.md` already forbids the state, the mitigation is a test of the invariant, not new code.
- Never weaken an existing AC to fit a mitigation. Add, do not edit.
- Ten minutes of pod time. If the pass needs longer, the Unit is too big or crosses contexts; flag that instead of finishing.

## Verification

Before handing over, check:

- [ ] Every abuse case has exactly one AC, and every new AC names the abuse case it mitigates
- [ ] Every AC includes a negative outcome (what must not happen)
- [ ] Every cited control appears in `CLAUDE.md` or `docs/domain/`
- [ ] Escalation line present; reviewer field blank
- [ ] Section ends with `Reviewed by: ___`

Output is a draft until a human signs it.
