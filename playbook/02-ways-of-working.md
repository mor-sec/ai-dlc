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

A pod is complemented by part-time members who join Mob Elaboration: the product owner (always), QA (always), a security engineer (for Units touching auth, money, or PII — see [Chapter 06](06-security-shift-left.md)).

**Why not one developer + agent?** Solo operators rubber-stamp their own agent's output. The pod exists to keep validation honest and to spread the new skills. Pairs are the floor; three is the sweet spot; four is a crowd.

## The weekly rhythm

There is no sprint. The rhythm is built from Bolts:

- **Monday morning — Elaboration block (up to half a day).** Mob Elaboration on the next 2–4 Units of Work. Product brings intent; AI drafts stories, questions, and risks; the room decides. Output: approved Units of Work in Jira ([Chapter 08](08-github-jira.md)).
- **Tuesday–Thursday — Bolts.** One Unit of Work at a time, plan-gate then Mob Construction. A typical Unit takes a half-day to two days. Merge and deploy as each completes — no release-day batching.
- **Friday — Consolidation.** Retro (30 min, focused on *how the collaboration with agents went*, not just team dynamics), steering-file and skill updates from the week's lessons, learning time ([Chapter 11](11-learning-paths.md)), and paying down any review debt.

This is a template, not a law. The invariants: elaboration is batched and synchronous, Bolts get uninterrupted pod attention, and lessons are folded back into steering files weekly.

## A day inside a Bolt

1. **Plan (30–60 min).** Driver gives the agent the Unit of Work and asks for an implementation plan. Pod reviews the plan — files touched, approach, test strategy, risks. Iterate until it's right. *This is the highest-leverage hour of the day.*
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

## Metrics that matter (and ones that don't)

**Track:** Units of Work completed per week; lead time from intent to production; defects escaping to production; review depth (substantive findings per review); change failure rate and MTTR; steering-file update frequency (a proxy for organizational learning); cost per validated Unit of Work — tokens + warehouse credits + CI minutes ([Chapter 03](03-tooling-strategy.md#unit-economics-cost-per-validated-unit-of-work)).

**Don't track:** lines of code, number of prompts, "AI usage %", story points. All are either meaningless or actively corrupting under AI-DLC.

## Anti-patterns

- **The silent pod.** Everyone heads-down with their own agent, mob in name only. Symptom: three parallel branches. Fix: one shared screen during Construction, one Unit at a time.
- **Review theater.** Approvals within two minutes of PR creation. Track time-to-approve and comment substance.
- **Prompt hero.** One person becomes the only effective driver. Rotate daily and pair on steering.
- **Elaboration skipping under deadline pressure.** The moment you most need clear intent is exactly when you're tempted to skip it.
- **Friday deploys of material changes.** Risk-gates still apply to humans ([Chapter 07](07-devops-automation.md)).

## Tips & tricks

- **Keep a pod journal** (`docs/journal/`, one markdown file per week): what steering worked, what the agent got wrong, what to encode into [CLAUDE.md](../standards/claude-md-template.md). This becomes training material for the next pod.
- **"Explain it back" ritual:** before merging anything non-trivial, one pod member explains the diff to the others without the agent's help. Cheap comprehension insurance.
- **Name your validation gates in the PR template** so review checklists are in front of every reviewer.
- **Protect Bolt focus:** no meetings inside a Bolt. Elaboration Monday buys you meeting-free Bolts.

## References

- Previous: [Chapter 01 — Methodology](01-ai-dlc-methodology.md) · Next: [Chapter 03 — Tooling Strategy](03-tooling-strategy.md)
- Templates: [Unit of Work](../standards/unit-of-work-template.md)
