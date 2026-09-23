# The AI-DLC Playbook

**A practical playbook for AI-driven development, based on AWS's AI-Driven Development Lifecycle (AI-DLC).**

This playbook equips teams to rapidly prototype and build fullstack enterprise applications with AI as an active collaborator — not a code-completion sidekick. It covers the methodology, tooling, architecture, security, DevOps, documentation standards, legacy modernization, and the learning paths a team needs to succeed.

## Who this is for

- **Developers** joining an AI Pod and learning the new rituals
- **Architects** designing systems that AI agents can build reliably
- **Engineering leaders and champions** rolling out AI-DLC across an organization and building a community of practice around it
- **Product owners** who now work in Mob Elaboration sessions instead of backlog grooming

## Core ideas in one paragraph

AI-DLC replaces the traditional SDLC's human-does-everything model with a loop where **AI orchestrates and generates, humans validate and decide**. Epics become **Units of Work**; sprints become **Bolts** (hours-to-days cycles); teams shrink to **AI Pods** of 2–3 developers working mob-style with agents. Security shifts left into elaboration. DevOps is automated with risk-based gates. Documentation is markdown, written as code, versioned in git. Architecture follows Domain-Driven Design and event-driven patterns because clear boundaries and explicit contracts are exactly what make AI agents effective.

## The playbook

| # | Chapter | What you'll learn |
|---|---------|-------------------|
| 01 | [AI-DLC Methodology](playbook/01-ai-dlc-methodology.md) | The three phases, Mob Elaboration & Construction, Units of Work, Bolts, validation gates |
| 02 | [Ways of Working](playbook/02-ways-of-working.md) | AI Pod composition, daily rhythm, definition of done, review culture |
| 03 | [Tooling Strategy](playbook/03-tooling-strategy.md) | Claude Code as primary agent; steering files, skills, hooks, MCP; evaluating alternatives |
| 04 | [Architecture](playbook/04-architecture.md) | DDD and event-driven architecture as the backbone for AI-built systems |
| 05 | [Rapid Prototyping](playbook/05-rapid-prototyping.md) | Snowflake-first prototyping; alternatives; promoting prototypes to production |
| 06 | [Shift-Left Security](playbook/06-security-shift-left.md) | Threat modeling in elaboration, secure steering files, automated scanning, AI-specific risks |
| 07 | [DevOps Automation](playbook/07-devops-automation.md) | Risk-based CI/CD, IaC, ephemeral environments, AI-assisted operations |
| 08 | [GitHub + Jira Integration](playbook/08-github-jira.md) | Mapping Units of Work and Bolts to Jira; traceability from intent to deployment |
| 09 | [Documentation Standards](playbook/09-documentation-standards.md) | Markdown as the standard; ADRs; diagrams-as-code; the DocLang exploration |
| 10 | [Legacy Modernization](playbook/10-legacy-modernization.md) | AI-assisted COBOL and Java modernization: comprehend, extract, transform |
| 11 | [Learning Paths](playbook/11-learning-paths.md) | Role-based courses and knowledge; the org enablement program |
| 12 | [Adoption Strategy](playbook/12-adoption-strategy.md) | Innovating deliberately, stakeholder buy-in, socializing AI-DLC with the wider team, and running a community of practice |
| A | [Worked Example](playbook/appendix-a-worked-example.md) | One Unit of Work end to end: elaboration, threat model, Bolt plan, construction, PR, deploy, steering update |
| B | [Rules from Legislation](playbook/appendix-b-rules-from-legislation.md) | Business rules extracted from a (fictional) statute with a citation each, counsel's interpretation rulings, rule-traced tests, and an amendment impact analysis |

## Glossary

Every term with a specific meaning, one retrievable entry each, in [GLOSSARY.md](GLOSSARY.md).

## Standards & templates

Ready-to-use artifacts in [`standards/`](standards/):

- [Markdown Style Guide](standards/markdown-style-guide.md) — the writing standard
- [ADR Template](standards/adr-template.md) — architecture decision records
- [Unit of Work Template](standards/unit-of-work-template.md) — AI-DLC's replacement for epics
- [Bolt Plan Template](standards/bolt-plan-template.md) — what the agent proposes at the plan gate, with stop conditions
- [Steering Evals](standards/steering-evals.md) — golden tasks that regression-test steering files and skills on every change, cold
- [Test Review Checklist](standards/test-review-checklist.md) — reviewing agent-generated tests; mutation and AC-mapping gates
- [Skill Template](standards/skill-template.md) — anatomy of a skill, plus five [reference skills](standards/skills/README.md): threat-model, bolt-plan, tests-from-acs, lesson-to-steering, incident-investigate
- [CLAUDE.md Template](standards/claude-md-template.md) — starter steering file for new repos
- [Model Selection Reference](standards/model-selection.md) — current model-tier assignments and cost accounting (reviewed quarterly)
- [Metrics Reference](standards/metrics-reference.md) — one definition per metric: source, cadence, healthy direction, and the pilot baseline
- [Pilot Charter Template](standards/pilot-charter-template.md) — the signed Wave 1 contract: scope, baseline, success and stop criteria, budget, review date
- [Community of Practice Charter Template](standards/community-of-practice-charter-template.md) — roles, rituals, contribution flow, and health metrics for the community that sustains adoption

## How to use this playbook

1. **New to AI-DLC?** Read chapters 01–02 in order; they define every term the rest uses. Then [Appendix A](playbook/appendix-a-worked-example.md), which follows one Unit of Work from Monday's intent to Friday's steering update with every artifact filled in.
2. **Setting up a team?** Chapters 03, 08, and 11, then the templates.
3. **Starting a build?** Chapters 04–07 are the engineering core.
4. **Sitting on legacy, or building from legislation?** Chapter 10, after 04; then [Appendix B](playbook/appendix-b-rules-from-legislation.md) if the specification is law rather than code.
5. **Leading the rollout?** Chapter 12 for buy-in, socialization, and the community of practice, alongside Chapter 11's waves; start with the pilot charter template.

This repo dogfoods its own standards: everything is markdown, diagrams are Mermaid, changes go through PRs ([template](.github/pull_request_template.md)), decisions get [ADRs](docs/adr/), every file carries a `reviewed:` date, and [CI](.github/workflows/docs.yml) runs the markdownlint, link, and Mermaid checks that [Chapter 09](playbook/09-documentation-standards.md#enforced-in-ci) prescribes, plus a structure check for this repo's own conventions. The repo's own steering file is [CLAUDE.md](CLAUDE.md).
