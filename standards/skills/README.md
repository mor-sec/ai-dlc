# Reference skills

Skills the playbook prescribes, in Claude Code's native layout: one folder per skill, a `SKILL.md` inside, copyable straight into a repo's `.claude/skills/`. How to write one: [skill template](../skill-template.md).

| Skill | Does | Used in |
|---|---|---|
| [`threat-model`](threat-model/SKILL.md) | Drafts the threat-model summary of a Unit of Work during Mob Elaboration, with mitigations as acceptance criteria | [Chapter 06](../../playbook/06-security-shift-left.md), [Appendix A](../../playbook/appendix-a-worked-example.md) |
| [`bolt-plan`](bolt-plan/SKILL.md) | Produces the Bolt plan from a Unit of Work at the plan gate, reading domain docs and ADRs first; stops before implementation | [Chapter 02](../../playbook/02-ways-of-working.md#a-day-inside-a-bolt), [Bolt plan template](../bolt-plan-template.md) |
| [`tests-from-acs`](tests-from-acs/SKILL.md) | Generates tests mapped one-to-one to acceptance criteria, each naming the failure it catches, then runs the mutation check | [Chapter 02](../../playbook/02-ways-of-working.md#testing-under-ai-dlc), [Test review checklist](../test-review-checklist.md) |
| [`lesson-to-steering`](lesson-to-steering/SKILL.md) | Turns a post-mortem, finding, or journal entry into the one steering change that prevents the class, as a draft PR | [Chapter 06](../../playbook/06-security-shift-left.md#operations-continuous-verification), [Chapter 07](../../playbook/07-devops-automation.md#ai-in-operations-the-third-ai-dlc-phase) |
| [`incident-investigate`](incident-investigate/SKILL.md) | First-line incident investigation: ranked hypotheses with evidence and a timeline draft; never remediates | [Chapter 07](../../playbook/07-devops-automation.md#ai-in-operations-the-third-ai-dlc-phase), [Post-incident review template](../post-incident-review-template.md) |
