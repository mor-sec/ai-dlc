# 0017 — Add standard templates for the Friday consolidation, post-incident reviews, and the FAQ

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

Three recurring artifacts were prescribed by the playbook but had no template. The Friday consolidation and pod journal ([Chapter 02](../../playbook/02-ways-of-working.md#the-weekly-rhythm)) were described in prose, so each pod recorded them differently, and the monthly digest had nothing consistent to draw from. Post-mortems were said to feed steering ([Chapter 07](../../playbook/07-devops-automation.md#ai-in-operations-the-third-ai-dlc-phase)), and the `incident-investigate` skill drafts their timeline, but no document said where the class-level question is asked. [Chapter 12](../../playbook/12-adoption-strategy.md#handling-the-hard-objections) told organizations to keep a FAQ and to write it only from real questions, but gave no shape for it.

A threat-model template was also considered. It already exists as the *Threat model summary* section of the [Unit of Work template](../../standards/unit-of-work-template.md), which the `threat-model` skill fills, so a separate one would duplicate it.

## Decision

We will add three templates to `standards/`: a consolidation template that is also the pod journal, a post-incident review template whose central section is the class-level fix handed to `lesson-to-steering`, and a FAQ template in which every entry quotes a real question with who asked and when.

Each follows the existing template shape (front-matter, where it lives, a fenced copyable body, a checklist) and is linked from the chapter that prescribes the artifact.

## Options considered

### Option A — Three templates, linked from their chapters  ← chosen

- Pros: consistent artifacts across pods; the digest, the steering loop, and the FAQ get predictable inputs; each template carries the one rule that matters most (steering changes, class-level fix, real questions).
- Cons: three more files to keep current.

### Option B — Leave them as prose in the chapters

- Pros: fewer files.
- Cons: pods invent their own formats; the class-level question is skipped under incident fatigue; FAQs fill with invented questions.
- Rejected because: these are the artifacts that close the learning loop, and the loop is where adoption programs most often fail silently.

### Option C — A single "rituals" template covering all three

- Pros: one file.
- Cons: three audiences (the pod, the incident commander, the community coordinator) with different cadences.
- Rejected because: a template that serves three rituals serves none of them well.

## Consequences

- Positive: consolidation always produces a list of what reaches steering; incidents end with a drafted fix PR; the FAQ stays grounded in real questions.
- Negative: more template maintenance for the platform pod; pods that already keep journals must convert.
- Follow-ups: the digest rota reads journals in the new shape; the `incident-investigate` skill's timeline draft should use the template's file path.

## Revisit when

Pods consistently leave a section of a template empty for a quarter, which means the section is wrong, or the digest writer reports the journals are still not comparable.
