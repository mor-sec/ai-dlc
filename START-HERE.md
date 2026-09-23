---
owner: platform-enablement
audience: everyone new to AI-DLC, including leaders and product owners who will not read every chapter
reviewed: 2026-09-24
review-cadence: quarterly
---

# Start Here

AI-DLC on one page: what happens, when, which artifact to use, and where to read more. Every line links to the chapter or template that owns it; this page does not replace them. The terms are defined in the [glossary](GLOSSARY.md).

## The loop

1. **Intent** from the business becomes a **Unit of Work** in Mob Elaboration, drafted by the agent and decided by people ([Chapter 01](playbook/01-ai-dlc-methodology.md#phase-1-inception)).
2. A **Bolt** starts with a plan the pod approves before anything is generated ([Chapter 02](playbook/02-ways-of-working.md#a-day-inside-a-bolt)).
3. In **Mob Construction** the agent writes code, tests, and IaC in slices while the Navigator reviews each one.
4. The change deploys through **risk-based gates**: routine changes flow, material ones wait for a named approver ([Chapter 07](playbook/07-devops-automation.md#risk-based-gating)).
5. Lessons from the week, from incidents, and from production go back into **steering** ([Chapter 03](playbook/03-tooling-strategy.md#the-context-engineering-hierarchy)).

## The week

| When | What | Record |
|---|---|---|
| Monday morning | Mob Elaboration on the next 2–4 Units | [Unit of Work](standards/unit-of-work-template.md) |
| Tuesday–Thursday | Bolts: plan, construct, merge, deploy, one Unit at a time | [Bolt plan](standards/bolt-plan-template.md) |
| Friday | Consolidation: retro, steering changes, learning | [Consolidation](standards/consolidation-template.md) |

Details and the pace rules: [Chapter 02](playbook/02-ways-of-working.md#the-weekly-rhythm).

## The gates, and what you bring to each

| Gate | Who decides | Artifact or tool |
|---|---|---|
| Unit of Work approval | Product and pod | [Unit of Work template](standards/unit-of-work-template.md), with the [`threat-model`](standards/skills/threat-model/SKILL.md) skill |
| Bolt plan approval | Pod | [Bolt plan template](standards/bolt-plan-template.md), drafted by the [`bolt-plan`](standards/skills/bolt-plan/SKILL.md) skill |
| Continuous review | Navigator | [Test review checklist](standards/test-review-checklist.md); tests from the [`tests-from-acs`](standards/skills/tests-from-acs/SKILL.md) skill |
| Merge | Reviewer, QA, and CI | The [reference pipeline](playbook/07-devops-automation.md#the-reference-pipeline-github-actions): scans, mutation, AC mapping, evals for AI features |
| Deploy (material and critical) | Named approver | A stated rollback in the PR ([Chapter 07](playbook/07-devops-automation.md#risk-based-gating)) |

Why the gates are the method: [Chapter 01](playbook/01-ai-dlc-methodology.md#the-validation-gates).

## Which template when

| Moment | Use |
|---|---|
| Setting up a repo | [CLAUDE.md template](standards/claude-md-template.md) |
| Recording a decision | [ADR template](standards/adr-template.md) |
| Writing a skill | [Skill template](standards/skill-template.md) and the [reference skills](standards/skills/README.md) |
| Changing steering or a model tier | [Steering evals](standards/steering-evals.md) and the [model selection reference](standards/model-selection.md) |
| After an incident | [Post-incident review](standards/post-incident-review-template.md), then [`lesson-to-steering`](standards/skills/lesson-to-steering/SKILL.md) |
| Starting a pilot | [Pilot charter](standards/pilot-charter-template.md) |
| Starting a community of practice | [Community charter](standards/community-of-practice-charter-template.md) and the [FAQ template](standards/faq-template.md) |
| Reporting numbers | [Metrics reference](standards/metrics-reference.md) |

## Rules that do not bend

- No significant generation without an approved plan ([Chapter 01](playbook/01-ai-dlc-methodology.md#phase-2-construction)).
- No unreviewed code merges, and no agent merges anything at any [autonomy level](playbook/03-tooling-strategy.md#agent-autonomy-levels).
- The agent halts on a stop condition; the pod does not help it route around one ([Appendix C](playbook/appendix-c-a-bolt-that-fails.md)).
- Tests name the failure they catch, and the mutation gate checks that they do ([Chapter 02](playbook/02-ways-of-working.md#testing-under-ai-dlc)).
- Restricted data never enters agent context as real values ([Chapter 06](playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership)).
- Review budget is a daily cap, not a target ([Chapter 02](playbook/02-ways-of-working.md#sustainable-pace)).
- No metric targets an individual ([metrics reference](standards/metrics-reference.md)).

## Where to go next

| You are | Read |
|---|---|
| A developer joining a pod | Chapters [01](playbook/01-ai-dlc-methodology.md) and [02](playbook/02-ways-of-working.md), then [Appendix A](playbook/appendix-a-worked-example.md) and [Appendix C](playbook/appendix-c-a-bolt-that-fails.md) |
| An architect | [Chapter 04](playbook/04-architecture.md), then [07](playbook/07-devops-automation.md); [13](playbook/13-building-ai-features.md) if the product calls a model |
| A product owner | [Chapter 01](playbook/01-ai-dlc-methodology.md), the [Unit of Work template](standards/unit-of-work-template.md), and Monday of [Appendix A](playbook/appendix-a-worked-example.md) |
| QA | The QA row in [Chapter 02](playbook/02-ways-of-working.md#the-ai-pod), the [test review checklist](standards/test-review-checklist.md), and [Appendix C](playbook/appendix-c-a-bolt-that-fails.md) |
| A security engineer | [Chapter 06](playbook/06-security-shift-left.md), then [autonomy levels](playbook/03-tooling-strategy.md#agent-autonomy-levels) |
| Leading the rollout | [Chapter 12](playbook/12-adoption-strategy.md) with [Chapter 11](playbook/11-learning-paths.md)'s waves; start with the [pilot charter](standards/pilot-charter-template.md) |
| Working on legacy or legislation | [Chapter 10](playbook/10-legacy-modernization.md) and [Appendix B](playbook/appendix-b-rules-from-legislation.md) |

The full table of contents is the [README](README.md).
