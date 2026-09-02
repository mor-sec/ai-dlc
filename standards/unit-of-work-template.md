---
owner: platform-enablement
audience: product owners, developers
reviewed: 2026-09-02
review-cadence: quarterly
---

# Unit of Work Template

The AI-DLC replacement for the epic: a business intent plus everything an agent and a pod need to execute it. Drafted by the AI during [Mob Elaboration](../playbook/01-ai-dlc-methodology.md#phase-1-inception), edited and approved by humans in the session, stored as the Jira Epic description ([Chapter 08](../playbook/08-github-jira.md)).

A Unit of Work is **ready** when an agent could start without asking who the actors are, and **right-sized** when it fits in 1–3 Bolts. Bigger → split; can't split → your context boundaries need work ([Chapter 04](../playbook/04-architecture.md)).

---

```markdown
# <PROJ-123> — <Outcome-oriented title, e.g. "Customers can retry failed payments">

## Intent

One paragraph: what business outcome, for whom, and why now. Written by product.
If this paragraph is ambiguous, everything downstream amplifies the ambiguity.

**Success looks like:** <observable result — a metric moves, a task becomes possible>

## Domain context

- Bounded context(s): <name> → docs/domain/<context>/model.md
- Key terms: <link to language.md entries the work touches>
- Events consumed/published: <event names + schema links>
- Relevant ADRs: <links — constraints the implementation must respect>
- ⚠ Cross-context? <if yes: which contexts, and why this isn't split — cross-context
  Units are the risky ones>

## Stories & acceptance criteria

### Story 1 — <actor> can <capability>
- AC1: Given <state>, when <action>, then <observable outcome>
- AC2: …

### Story 2 — …

(Every AC must be testable as written — tests will map to these 1:1.)

## Threat model summary

From the elaboration threat-model pass (see Chapter 06):
- Assets touched: <data, money, credentials>
- Trust boundaries crossed: <where>
- Top abuse cases: <2–5>
- Mitigations → carried as acceptance criteria: <AC references above>
- Security escalation: yes/no <auth, money, PII, crypto ⇒ security engineer named here>

## Risks & open questions

| Risk / question | Owner | Resolution needed by |
|---|---|---|
| … | … | plan gate / mid-Bolt / before merge |

## Out of scope

Explicitly not in this Unit (the agent will otherwise happily build it):
- …

## Execution notes

- Estimated Bolts: 1–3
- Material-change classification expected: routine / material / critical (Chapter 07)
- Feature flag: <name, if release is decoupled from deploy>
```

---

**Elaboration checklist** (the human gate before `Ready`):

- [ ] Intent unambiguous — the room agrees on what "done" means
- [ ] Every AC testable as written
- [ ] Domain links resolve (model, language, events, ADRs)
- [ ] Threat-model pass done; mitigations are ACs
- [ ] Right-sized (≤3 Bolts) and single-context, or the exception is justified
- [ ] Out-of-scope list exists (empty is a smell, not a virtue)
