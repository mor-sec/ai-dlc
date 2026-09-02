---
owner: platform-enablement
audience: developers, product owners
reviewed: 2026-09-02
review-cadence: quarterly
---

# 02 — Ways of Working

This chapter turns the [methodology](01-ai-dlc-methodology.md) into a daily operating rhythm: who is in a pod, what a day looks like, what "done" means, and how review culture changes when an agent writes most of the code.

## The AI Pod

An AI Pod is 2–3 developers plus their agents, with named accountabilities rather than rigid roles:

| Accountability | What they own | Notes |
|---|---|---|
| **Driver** | Steers the agent: writes prompts and plans, approves generation steps | Rotates daily — prompt/steering skill must not concentrate in one person |
| **Navigator** | Reviews output as it lands: correctness, architecture fit, security | The continuous-review half of Mob Construction |
| **Domain anchor** | Owns the Unit of Work's intent; liaison to product | Often the most senior; also maintains the domain model docs |
| **QA** (part-time, shared across 2–3 pods) | Owns *verification of intent*: acceptance criteria are testable as written; the AC-mapping check has no gaps; exploratory testing in the ephemeral environment; adversarial review of generated tests | Present at every Mob Elaboration and at the merge gate; not a manual regression tester, that work is generated and automated |

A pod is complemented by part-time members who join Mob Elaboration: the product owner (always), QA (always, with the accountabilities above), a security engineer (for Units touching auth, money, or PII — see [Chapter 06](06-security-shift-left.md)).

**Why not one developer + agent?** Solo operators rubber-stamp their own agent's output. The pod exists to keep validation honest and to spread the new skills. Pairs are the floor; three is the sweet spot; four is a crowd.

## The weekly rhythm

There is no sprint. The rhythm is built from Bolts:

- **Monday morning — Elaboration block (up to half a day).** Mob Elaboration on the next 2–4 Units of Work. Product brings intent; AI drafts stories, questions, and risks; the room decides. Output: approved Units of Work in Jira ([Chapter 08](08-github-jira.md)).
- **Tuesday–Thursday — Bolts.** One Unit of Work at a time, plan-gate then Mob Construction. A typical Unit takes a half-day to two days. Merge and deploy as each completes — no release-day batching.
- **Friday — Consolidation.** Retro (30 min, focused on *how the collaboration with agents went*, not just team dynamics), steering-file and skill updates from the week's lessons, learning time ([Chapter 11](11-learning-paths.md)), and paying down any review debt.

This is a template, not a law. The invariants: elaboration is batched and synchronous, Bolts get uninterrupted pod attention, and lessons are folded back into steering files weekly.

## A day inside a Bolt

1. **Plan (30–60 min).** Driver gives the agent the Unit of Work and asks for an implementation plan. Pod reviews the plan — files touched, approach, test strategy, risks. Iterate until it's right. *This is the highest-leverage hour of the day.* The plan is written to the [Bolt plan template](../standards/bolt-plan-template.md) and committed with the PR; its stop conditions are what keep step 2 honest. The [`bolt-plan` skill](../standards/skills/bolt-plan/SKILL.md) produces the first draft, having read the domain docs and ADRs first.
2. **Generate & review loop (core hours).** Agent implements in slices; Navigator reviews each slice as it lands. Driver keeps the agent on-plan; deviations trigger a plan update, not silent drift.
3. **Verify (before merge).** Full test run, security scans, a human read of the complete diff. The agent drafts the PR description with a traceability line back to the Jira issue.
4. **Close (15 min).** Merge, watch the deploy, update the Unit of Work status, capture one lesson for the steering file.

## Definition of Done

A Unit of Work is done when:

- [ ] Acceptance criteria demonstrably met (tests map to criteria)
- [ ] All tests pass in CI — including new tests generated with the change, reviewed by a human
- [ ] Security scans (SAST, SCA, secrets) clean or triaged with written rationale
- [ ] A human has reviewed and approved the full diff — no unreviewed code merges, ever
- [ ] Documentation and ADRs updated in the same PR ([Chapter 09](09-documentation-standards.md))
- [ ] Deployed (or deployable behind a flag) through the pipeline
- [ ] Jira issue closed with traceability links (PR, deploy)

## Review culture: the biggest change

When agents write most code, **review becomes the primary engineering act**. Calibrate accordingly:

- **Review the plan hardest.** A wrong plan wastes a day; a wrong line wastes a minute. Invert the traditional attention ratio.
- **Never approve what you don't understand.** "The agent wrote it and tests pass" is not understanding. If the pod can't explain a diff, it doesn't merge.
- **Review tests as adversarially as code.** Agents happily generate tests that assert current behavior, including bugs. Ask: *what failure would this test catch?*
- **Distrust plausible names.** Agent code fails in a characteristic way: it looks idiomatic and confident while misusing an API or inventing one. Check the calls that matter against the docs.
- **Budget review capacity.** A pod can properly review roughly 500–1,000 changed lines per person-day. Generation capacity is effectively infinite; review capacity is your real throughput limit. Plan Bolts around it.

## Testing under AI-DLC

Test discipline appears throughout the playbook: tests generated with the code ([Chapter 01](01-ai-dlc-methodology.md)), contract tests over end-to-end suites ([Chapter 07](07-devops-automation.md)), characterization tests as the oracle for legacy ([Chapter 10](10-legacy-modernization.md)). This section is the strategy those pieces belong to, and it answers the question review culture raises: the agent wrote the tests, so what checks the tests?

**The pyramid tilts toward contracts.** Schema-driven contract tests first, because events are the seams between bounded contexts and the schema is machine-readable intent. Unit tests second, aimed at domain invariants in `docs/domain/<context>/model.md` rather than at coverage. One thin smoke-path end-to-end test. Nothing else, and delete what flakes.

**The generated-test problem.** The session that wrote a bug writes tests that pass with the bug in place. A green suite proves the code agrees with itself. Two mechanical checks make it prove more:

1. **Mutation testing on changed files** at the PR gate. Small faults are injected into new code and the suite must catch them; a generated suite that kills fewer than 70% of mutants on routine changes fails the gate, 85% for material and critical. This is the only check that scales with generation volume, because it does not depend on a human reading every assertion.
2. **Acceptance-criteria mapping.** Every test names the AC it serves; CI lists any AC with zero tests and fails on it. The Unit of Work becomes the test plan, mechanically.

**The human part** is the Navigator's per-slice review, which asks one question of every test: *what production failure would make this red?* QA reads the same checklist at the merge gate, with a different bias: the Navigator has watched the code being built and QA has not, which is the point. The full checklist is the [test review checklist](../standards/test-review-checklist.md), and it is loaded as steering for agents so the tests arrive already answering the question; the [`tests-from-acs` skill](../standards/skills/tests-from-acs/SKILL.md) packages the whole procedure, mutation run included.

## Sustainable pace

Bolts are described as intense, and review is the bottleneck. Put together, that makes the reviewer the person most likely to burn out, and a tired reviewer is the one failure mode the whole method cannot absorb: every gate in [Chapter 01](01-ai-dlc-methodology.md#the-validation-gates) is a person reading carefully. Generation does not get tired at 4pm. People do.

Review fatigue has a signature. Approval times collapse late in the day; comments shift from findings to nits; the "explain it back" ritual gets skipped "just this once". By the time a pod notices, a week of rubber-stamped diffs is in production. So pace is enforced by rule, not by feel:

- **Review budget is a daily cap, not a target.** The 500 to 1,000 lines per person-day above is the ceiling. When the Navigator hits it, generation stops for the day, or the Navigator rotates. A Bolt that needs more review than the pod has left is a Bolt that runs into tomorrow.
- **Rotate the Navigator mid-Bolt.** Two hours of continuous adversarial reading is the useful limit. Swap Driver and Navigator at the half-day; the Driver's job is lighter on attention.
- **Three Bolt days, then a consolidation day.** The Friday consolidation is not optional overhead to be skipped in a busy week; it is the recovery that makes Monday's elaboration honest. A pod that has run five Bolt days straight has reviewed nothing properly since Wednesday.
- **No Bolt starts after lunch.** A Bolt wants sustained attention; a half-Bolt ends with an unreviewed diff waiting overnight, and the temptation to approve it first thing.
- **Watch the fatigue metrics, not the output metrics.** Time-to-approve by hour of day and review depth by day of week ([metrics reference](../standards/metrics-reference.md)) show fatigue a week before defects do. A pod whose Thursday-afternoon approvals take two minutes is not fast; it is tired.

The pod, not the individual, owns pace. Rotation and caps are pod rules so that no one has to be the person who says they cannot read any more today.

## Scaling beyond one pod

Everything above describes one pod. At ten pods the failure mode changes: not a tired reviewer but a coordination layer that grows back into the meetings AI-DLC removed. The design principle is that **pods coordinate through artifacts, not ceremonies**, and the artifacts already exist.

- **The context map is the org chart.** Every bounded context has exactly one owning pod ([Chapter 04](04-architecture.md#the-ddd-core-operationalized)); a pod may own several. Who to talk to about anything is answered by `docs/domain/context-map.md`, never by a spreadsheet. A context with two owners, or none, is a bug in the map to fix that week.
- **Cross-context Units are sequenced through the map, not through meetings.** A Unit that needs a new event from another context is two Units: the producer's, elaborated and built by the owning pod against the schema, and the consumer's, which starts when the schema is published in the registry. The schema is the handoff. If two pods routinely need each other's events mid-Bolt, the boundary is wrong and the map review below fixes it.
- **A platform pod owns the paved road.** The steering baseline, skill library, reference pipeline, ephemeral-environment machinery, golden-path IaC modules, and the [steering evals](../standards/steering-evals.md) are a product with pods as customers. It runs on Units of Work and Bolts like any other pod, and its backlog is the friction the other pods report at consolidation.
- **Shared steering is governed by PR, not by committee.** Pods propose changes to the org baseline through [`lesson-to-steering`](../standards/skills/lesson-to-steering/SKILL.md) drafts; the platform pod reviews and merges within the week. A steering change that affects every repo is material and gets a named approver, exactly like a schema change.
- **One org-level ritual: the context-map review, biweekly, 45 minutes.** Domain anchors only. Agenda: contexts whose ownership changed, boundaries that Units kept crossing, events published this fortnight, dispositions from legacy carving ([Chapter 10](10-legacy-modernization.md#stage-2-carve-ddd-applied-to-the-past)). Output is a PR to the context map. That is the entire cross-pod meeting load.

What does not scale is the mob itself. A pod stays two or three people; growth means more pods and more contexts, never a bigger pod. Wave 3 of the [enablement program](11-learning-paths.md#the-enablement-program-three-waves) grows pods by seeding, one practitioner anchoring each new one.

## Metrics that matter (and ones that don't)

**Track:** Units of Work completed per week; lead time from intent to production; defects escaping to production; review depth (substantive findings per review); change failure rate and MTTR; steering-file update frequency (a proxy for organizational learning); cost per validated Unit of Work — tokens + warehouse credits + CI minutes ([Chapter 03](03-tooling-strategy.md#unit-economics-cost-per-validated-unit-of-work)).

**Don't track:** lines of code, number of prompts, "AI usage %", story points. All are either meaningless or actively corrupting under AI-DLC.

Definitions, source systems, and cadences for every metric above are in the [metrics reference](../standards/metrics-reference.md), so that two pods reporting the same number mean the same thing.

## Anti-patterns

- **The silent pod.** Everyone heads-down with their own agent, mob in name only. Symptom: three parallel branches. Fix: one shared screen during Construction, one Unit at a time.
- **Review theater.** Approvals within two minutes of PR creation. Track time-to-approve and comment substance.
- **Prompt hero.** One person becomes the only effective driver. Rotate daily and pair on steering.
- **Elaboration skipping under deadline pressure.** The moment you most need clear intent is exactly when you're tempted to skip it.
- **Friday deploys of material changes.** Risk-gates still apply to humans ([Chapter 07](07-devops-automation.md)).
- **The coordination layer.** A weekly cross-pod sync, then a dependencies board, then a release train. Each one is reasonable; together they are Scrum of Scrums with agents. If pods need a meeting to sequence work, fix the context map and the schema registry, which is where the sequencing already lives.
- **The heroic Bolt.** Twelve hours, one Navigator, a 2,000-line diff approved at 21:40 because "we were so close". The method's gates were all present and none of them was working. Cap the day, split the Bolt, and finish tomorrow.

## Tips & tricks

- **Keep a pod journal** (`docs/journal/`, one markdown file per week): what steering worked, what the agent got wrong, what to encode into [CLAUDE.md](../standards/claude-md-template.md). This becomes training material for the next pod.
- **"Explain it back" ritual:** before merging anything non-trivial, one pod member explains the diff to the others without the agent's help. Cheap comprehension insurance.
- **Name your validation gates in the PR template** so review checklists are in front of every reviewer.
- **Protect Bolt focus:** no meetings inside a Bolt. Elaboration Monday buys you meeting-free Bolts.

## References

- Previous: [Chapter 01 — Methodology](01-ai-dlc-methodology.md) · Next: [Chapter 03 — Tooling Strategy](03-tooling-strategy.md)
- Templates: [Unit of Work](../standards/unit-of-work-template.md)
