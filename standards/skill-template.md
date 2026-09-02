---
owner: platform-enablement
audience: developers, security engineers
reviewed: 2026-09-02
review-cadence: quarterly
---

# Skill Template

What a skill file contains, and how to know one is worth writing. Audience: anyone packaging a recurring procedure for agents ([Chapter 03](../playbook/03-tooling-strategy.md#skills)). A worked reference implementation is [`skills/threat-model/SKILL.md`](skills/threat-model/SKILL.md).

A skill is a folder holding a `SKILL.md` and optionally supporting files (a checklist, an output template, a script). Claude Code loads it from `.claude/skills/<name>/` in the repo, or from the shared skill library; the agent reads the `description` to decide when the skill applies, then follows the body. Skills earn their place when a procedure is (a) repeated, (b) has a right way, and (c) the agent gets it wrong from a cold start. Anything else is a steering line or nothing.

Where they live: the shared skill library repo, versioned and reviewed like code ([Chapter 03](../playbook/03-tooling-strategy.md#tips--tricks)); each consuming repo copies or symlinks the folders it needs into `.claude/skills/`. A skill that only one repo will ever use can live in that repo directly.

---

```markdown
---
name: <kebab-case-name>
description: <One or two sentences the agent matches against the task. Say WHAT it
  does and WHEN to use it, in the words a task would use: "Use when a Unit of Work
  is drafted and before it moves to Ready." Weak: "Helps with security."
---

# <Skill title>

<One line: the job this skill does and for whom.>

## Inputs

- <What the agent needs in context before starting: a file, a Jira key, a schema.
  Say where to find each.>

## Outputs

- <Exactly what the skill produces: which file or section, in which format.
  Link the template it must follow.>

## Steps

1. <Numbered, imperative, one action each. Read before write.>
2. <Where a step has a judgment call, state the criterion, not "use judgment".>
3. <Name the stop point: what the agent must NOT do (transition a ticket, merge,
   delete) and who does it instead.>

## Rules

- <Constraints with their why: "Only cite controls the repo has — check
  CLAUDE.md first — because invented controls create false assurance.">
- <Limits: length, count, scope. "Target 2–5 abuse cases, not 20.">

## Verification

- <How the agent checks its own output before handing over: a checklist, a
  command, a template diff.>
- Ends with a line the human completes: `Reviewed by: ___`. Skill output is a
  draft until a human signs it.
```

---

## Writing a skill that works cold

- **Test it in a fresh session.** The skill's whole value is that an agent with no memory of the last conversation does the procedure right. If it only works after you explained things, the explanation belongs in the skill.
- **Description is the trigger.** The agent chooses skills by matching the description against the task. Write it the way a task would be phrased, name the artifact it acts on, and say when *not* to use it if there is a close sibling.
- **Under ~100 lines.** Longer skills mean the procedure has two skills in it, or the steps are describing rather than instructing. Move reference material into a supporting file the steps point at.
- **Steps read files before they write them.** The most common cold-start failure is an agent inventing what it could have looked up. Make the lookup an explicit step.
- **Version and change-log it.** A skill regression is a process regression across every pod that uses it. Skills go through PRs, with a reviewer who runs it cold, and with a golden task in the [steering evals](steering-evals.md) suite that guards its most important rule.

## Skills the playbook expects

| Skill | Chapter | Status |
|---|---|---|
| `threat-model` | [06](../playbook/06-security-shift-left.md) | Reference implementation in [`skills/threat-model/`](skills/threat-model/SKILL.md) |
| `bolt-plan` | [02](../playbook/02-ways-of-working.md) | Reference implementation in [`skills/bolt-plan/`](skills/bolt-plan/SKILL.md) |
| `tests-from-acs` | [02](../playbook/02-ways-of-working.md) | Reference implementation in [`skills/tests-from-acs/`](skills/tests-from-acs/SKILL.md) |
| `lesson-to-steering` | [06](../playbook/06-security-shift-left.md), [07](../playbook/07-devops-automation.md) | Reference implementation in [`skills/lesson-to-steering/`](skills/lesson-to-steering/SKILL.md) |
| `incident-investigate` | [07](../playbook/07-devops-automation.md) | Reference implementation in [`skills/incident-investigate/`](skills/incident-investigate/SKILL.md) |
| `jira-elaboration` | [08](../playbook/08-github-jira.md) | To write; draft the Unit of Work + child stories from an intent paragraph |
| `snowflake-prototype` | [05](../playbook/05-rapid-prototyping.md) | To write; scaffold Streamlit app, grants, warehouse config, `PROTOTYPE.md` |
| `write-adr` | [04](../playbook/04-architecture.md) | To write; draft an ADR from a decision made in a Bolt |
| `scaffold-service` | [03](../playbook/03-tooling-strategy.md) | To write; new service housing the standards from day one |
