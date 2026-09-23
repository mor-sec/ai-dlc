---
owner: platform-enablement
audience: everyone, including agents
reviewed: 2026-09-24
review-cadence: quarterly
---

# Glossary

Every term the playbook uses with a specific meaning, one per section so that each entry can be retrieved alone. Audience: humans looking something up, and agents loading definitions before a task. The defining chapter is linked from each entry; when a definition and a chapter disagree, fix the glossary.

## AI Pod

Two or three developers plus their agents, working mob-style on one Unit of Work at a time, with rotating accountabilities (Driver, Navigator, domain anchor) rather than fixed roles. Replaces the seven-person Scrum team. Pairs are the floor; four is a crowd. [Chapter 02](playbook/02-ways-of-working.md#the-ai-pod)

## AI-DLC

AI-Driven Development Lifecycle. AWS's methodology in which AI orchestrates and generates at each stage while humans validate and decide at explicit gates. Three phases: Inception, Construction, Operations. [Chapter 01](playbook/01-ai-dlc-methodology.md)

## Acceptance criterion (AC)

A testable statement in a story, written in Given/When/Then form, that a test will map to one-to-one. Threat-model mitigations are carried as ACs so they get implemented and tested without separate tracking. [Unit of Work template](standards/unit-of-work-template.md)

## Anti-corruption layer (ACL)

A translation boundary that keeps a legacy or foreign model from leaking into a bounded context; speaks the new ubiquitous language outward and the legacy's language inward. The bridgehead for strangler-fig modernization. [Chapter 10](playbook/10-legacy-modernization.md#stage-4-strangle-the-delivery-pattern)

## Architecture decision record (ADR)

A short, numbered document recording one significant decision, its context, options, and consequences. Under AI-DLC it doubles as steering: agents read the ADR log before proposing designs. A decision exists when its ADR merges. [ADR template](standards/adr-template.md)

## Autonomy level

The declared level at which an agent run operates: 0, interactive with a pod member driving; 1, headless commenter that may only comment; 2, headless author that may open routine-class PRs labelled `agent-authored`. No level merges. Each unattended run has a bot identity, a sandbox without production credentials, and a token cap; moving up a level takes an ADR. [Chapter 03](playbook/03-tooling-strategy.md#agent-autonomy-levels)

## Bolt

An intense execution cycle measured in hours to days that takes one Unit of Work, or a slice of one, from approved plan to reviewed, tested, deployable code. Replaces the two-week sprint. Identified by a Bolt id (`B-YYYY-MM-DD-a`) in Jira and in the committed Bolt plan. [Chapter 01](playbook/01-ai-dlc-methodology.md#the-vocabulary)

## Bolt plan

The artifact the agent proposes at the start of a Bolt and the pod approves before generation: scope, approach, files, test strategy, risk class, stop conditions. Committed at `docs/bolts/<bolt-id>.md` in the owning repo. [Bolt plan template](standards/bolt-plan-template.md)

## Bounded context

A DDD boundary inside which one domain model and one vocabulary apply. Under AI-DLC it is also the unit of agent context: a Unit of Work should fit inside one. Documented in `docs/domain/<context>/`. [Chapter 04](playbook/04-architecture.md#the-ddd-core-operationalized)

## Champion

A practitioner in each team or department, including teams not yet running AI-DLC, with about 5% of their time budgeted to hold office hours, carry the adoption narrative locally, and bring their team's questions and objections back to the community of practice. Volunteers, not appointees. [Chapter 12](playbook/12-adoption-strategy.md#roles)

## Business-rules extract

The markdown catalogue of rules a system must implement, extracted from an authoritative source (legacy code or legislation) with a pointer to the exact source for each rule: a program paragraph, or a statute subsection with a verbatim quote. Rules whose reason or meaning is unclear are flagged as questions, never guessed; for legislation, counsel's rulings are recorded separately as interpretations. [Chapter 10](playbook/10-legacy-modernization.md#stage-1-comprehend-ais-home-turf) · [Appendix B](playbook/appendix-b-rules-from-legislation.md)

## Characterization test

A test that captures a legacy system's current behaviour, including its oddities, before any transformation. The old system is the oracle; the test proves the new one matches. Never derived from the new code. [Chapter 10](playbook/10-legacy-modernization.md#stage-3-transform-tool-assisted-verification-led)

## Community of practice

The voluntary, cross-team network of AI-DLC practitioners that owns the practice: craft knowledge, the experiment register, guild hour, the digest, and outreach. Contributes to the paved road through normal PRs and holds no approval authority; replaces the Center of Excellence. Coordinated by a rotating coordinator under a written charter. [Chapter 12](playbook/12-adoption-strategy.md#the-community-of-practice)

## Consolidation

The Friday block in the weekly rhythm: retro on the agent collaboration, steering-file and skill updates from the week's lessons, learning time, review-debt paydown. The recovery day that makes Monday's elaboration honest. [Chapter 02](playbook/02-ways-of-working.md#the-weekly-rhythm)

## Context classification

Applying the organization's data classification to what an agent session may read: public and internal as is; confidential only under recorded vendor terms; restricted data (PII, PCI, credentials, customer data) never as real values, only synthetic, masked, or as metadata. Session records inherit the classification of what the agent read. [Chapter 06](playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership)

## Context engineering

The discipline of supplying agents with the intent, standards, and domain knowledge they need, through steering files, skills, domain docs, and the codebase itself. When output disappoints, fix context in that order, cheapest first. [Chapter 03](playbook/03-tooling-strategy.md#the-context-engineering-hierarchy)

## Cost per validated Unit of Work

Agent tokens plus warehouse credits plus CI minutes attributed to one Unit's Jira key. The unit-economics metric that makes model spend governable; not cost per seat or per token. [Chapter 03](playbook/03-tooling-strategy.md#unit-economics-cost-per-validated-unit-of-work)

## Definition of Done

The checklist a Unit of Work must satisfy: ACs demonstrably met, tests green and human-reviewed, scans clean or triaged, full diff human-approved, docs and ADRs updated in the same PR, deployed or deployable behind a flag, Jira closed with traceability links. [Chapter 02](playbook/02-ways-of-working.md#definition-of-done)

## Domain anchor

The pod accountability that owns the Unit of Work's intent, liaises with product, and maintains the domain model docs and the repo's CLAUDE.md. Often the most senior member. [Chapter 02](playbook/02-ways-of-working.md#the-ai-pod)

## Driver

The pod accountability that steers the agent: writes prompts and plans, approves generation steps. Rotates daily so prompting skill does not concentrate in one person. [Chapter 02](playbook/02-ways-of-working.md#the-ai-pod)

## Ephemeral environment

A short-lived, production-shaped environment provisioned per PR for integration tests, DAST, and human inspection, destroyed on merge or close. The highest-payoff automation investment under AI-DLC. [Chapter 07](playbook/07-devops-automation.md#the-reference-pipeline-github-actions)

## Expand/contract migration

The pattern for changing a schema without downtime: expand (add the new structure), migrate writers and backfill, switch readers, then contract (remove the old structure in a later deploy). Every step stays compatible with the code running beside it, so canary and rollback keep working. Agent-written migrations follow it by rule. [Chapter 07](playbook/07-devops-automation.md#data-and-schema-migrations)

## Experiment register

The single markdown file (`docs/experiments/register.md` in the steering repo) listing every adoption experiment with its written question, horizon (adopt, pilot, explore), owner, time limit, required evidence, and kill, keep-local, or adopt decision. Kills are published like wins. [Chapter 12](playbook/12-adoption-strategy.md#the-experiment-register)

## Hook

A mechanical enforcement point in the agent's lifecycle: run a formatter after edits, block edits to protected paths, require tests before a commit completes. Hooks enforce what steering requests. [Chapter 03](playbook/03-tooling-strategy.md#hooks-and-permissions)

## Material change

A change class in risk-based gating: schema migrations, authN/authZ, public API or event major versions, IaC touching network or IAM, new external dependencies. Needs a named approver and a stated rollback plan in addition to the routine gate. See also routine change, critical change. [Chapter 07](playbook/07-devops-automation.md#risk-based-gating)

## Mob Construction

The Construction-phase practice: the pod works together on one shared screen while agents generate code, tests, and IaC; the Navigator reviews continuously rather than at the end. [Chapter 01](playbook/01-ai-dlc-methodology.md#the-vocabulary)

## Mob Elaboration

The Inception-phase session where pod, product owner, and QA translate business intent into Units of Work, with the agent drafting stories, clarifying questions, risks, and the threat model in real time. Replaces backlog grooming. Timeboxed to 90 minutes per Unit. [Chapter 01](playbook/01-ai-dlc-methodology.md#phase-1-inception)

## Model tier

Frontier, mid-tier, or small/fast: the class of model chosen per task. Frontier for plans, review, and security judgment; mid-tier for construction inside an approved plan; small for bulk mechanical work. The reviewer never runs on a cheaper tier than the generator. Current assignments: [model selection reference](standards/model-selection.md)

## MCP server

A Model Context Protocol integration giving agents tool access to a system (GitHub, Jira, Snowflake, AWS, observability). Treated as a privileged integration: owned, scoped to a service identity, permission-reviewed. [Chapter 03](playbook/03-tooling-strategy.md#mcp-servers)

## Navigator

The pod accountability that reviews agent output as it lands: correctness, architecture fit, security, and the tests. The continuous-review half of Mob Construction, rotated at the half-day to prevent fatigue. [Chapter 02](playbook/02-ways-of-working.md#the-ai-pod)

## Open Bolt

A standing slot in which anyone may silently observe a pilot pod's Mob Construction for an hour and then ask questions. The main tool for moving stakeholders and skeptics from understanding AI-DLC to having seen it. [Chapter 12](playbook/12-adoption-strategy.md#socializing-the-ideas)

## Paved road

The shared foundation Wave 2 of enablement builds so a pilot pod can start on day one: steering-file baseline, skill library, reference pipeline, Jira integration, agent permissions and guardrails, golden-path IaC modules. [Chapter 11](playbook/11-learning-paths.md#the-enablement-program-three-waves)

## Pilot charter

The signed contract that ends Wave 1: pilot pods, scope, pre-pilot baseline, three to five success criteria with thresholds, stop criteria, budget, guardrails, stakeholders, and the review date. Success criteria are not edited after signing; changes are appended as amendments. [Pilot charter template](standards/pilot-charter-template.md)

## Plan gate

The validation gate between Bolt planning and generation: no significant generation without a pod-approved Bolt plan. Maps one-to-one onto Claude Code's plan mode. [Chapter 01](playbook/01-ai-dlc-methodology.md#the-validation-gates)

## Prototype

A working artifact built to answer a written question in at most three Bolts, cheaply enough to throw away. Ends with a decision: kill, keep-as-tool, or promote. Promotion is a rebuild against production standards, not a rename. [Chapter 05](playbook/05-rapid-prototyping.md)

## QA

The part-time pod accountability, usually shared across two or three pods, that verifies *intent* rather than behaviour: acceptance criteria are testable as written, every AC has a test, generated tests are read adversarially at the merge gate, and agent-built behaviour is explored by hand in the ephemeral environment. Not a manual regression tester. [Chapter 02](playbook/02-ways-of-working.md#the-ai-pod)

## Risk-based gating

Classifying every change as routine, material, or critical, by path-based rules and labels, and letting the class decide where humans appear in the pipeline. Uniform caution is risk-increasing because it spends review capacity on the wrong changes. [Chapter 07](playbook/07-devops-automation.md#risk-based-gating)

## Routine change

The lowest change class: code within one bounded context, additive event fields, docs, patch and minor dependency bumps. Gate: CI green plus one human review, then merge queue and auto-deploy. [Chapter 07](playbook/07-devops-automation.md#risk-based-gating)

## Skill

A packaged, versioned procedure an agent invokes for a recurring task, held in a `SKILL.md` with a trigger-style description, inputs, outputs, steps, rules, and verification. Worth writing when a procedure is repeated, has a right way, and the agent gets it wrong cold. [Skill template](standards/skill-template.md)

## Stakeholder map

The Wave 1 table of named stakeholders recording what each cares about, what they worry about, the evidence that would move them, what the program asks of them, and their rung on the buy-in ladder (aware, understands, has seen it, committed, advocate). Updated after every conversation. [Chapter 12](playbook/12-adoption-strategy.md#the-stakeholder-map)

## Steering file

The standing instructions an agent loads every session, held in the repo's `CLAUDE.md`: commands, architecture summary, standards, security constraints, definition of done. Under 150 lines, constraints over descriptions, updated every consolidation. [CLAUDE.md template](standards/claude-md-template.md)

## Stop condition

A rule in the Bolt plan naming the circumstances under which the agent halts and asks for a plan update rather than proceeding: diff size, files outside the plan, changed tests, new dependencies, contradicted ADRs, repeated failures. [Bolt plan template](standards/bolt-plan-template.md)

## Strangler fig

The delivery pattern for modernization: a facade routes each capability to old or new; new services consume legacy state through events; the legacy system shrinks capability by capability until retired or deliberately kept. [Chapter 10](playbook/10-legacy-modernization.md#stage-4-strangle-the-delivery-pattern)

## Threat-model pass

The ten-minute STRIDE-style pass inside Mob Elaboration that lists assets, trust boundaries, and abuse cases for a Unit of Work and writes each mitigation as an acceptance criterion. Run with the `threat-model` skill. [Chapter 06](playbook/06-security-shift-left.md#inception-threat-modeling-as-elaboration)

## Traceability chain

The unbroken, machine-readable thread from business intent to production: Initiative to Unit of Work to stories to branch to plan to commits to review to CI to deploy event. Serves managers, auditors, agents, and cost allocation alike. [Chapter 08](playbook/08-github-jira.md#traceability-the-audit-trail-for-free)

## Ubiquitous language

The DDD practice of one vocabulary per bounded context shared by code, docs, tickets, and conversation, recorded in `docs/domain/<context>/language.md`. Naming drift is context poison for agents. [Chapter 04](playbook/04-architecture.md#why-this-architecture-specifically-for-ai-dlc)

## Unit of Work

A business intent plus everything needed to execute it: stories with acceptance criteria, domain context, threat-model summary, risks, out-of-scope list. Replaces the epic. Ready when an agent could start without asking who the actors are; right-sized when it fits in one to three Bolts. [Unit of Work template](standards/unit-of-work-template.md)

## Validation gate

A point where a human reviews an AI-produced artifact before it becomes load-bearing: Unit of Work approval, Bolt plan approval, continuous code review, merge gate, deploy gate for material changes. The gates are the methodology; remove them and you have autopilot. [Chapter 01](playbook/01-ai-dlc-methodology.md#the-validation-gates)
