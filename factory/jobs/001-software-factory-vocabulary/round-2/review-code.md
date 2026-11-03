VERDICT: PASS

# Code review — 001-software-factory-vocabulary, round 2

No findings.

Checks run in `.claude/worktrees/factory-001-software-factory-vocabulary` (HEAD 234c31a, on top of main 5727699):

- Lint: 0 errors (79 files).
- Links: 80 files, 0 broken.
- Structure: 0 violations. ADR numbering is contiguous through 0026.
- Mermaid: skipped, no diagram changed.

AC1 to AC8 are met:

- AC1: the `**Software factory**` row is on line 82 of `playbook/01-ai-dlc-methodology.md`, inside `## The vocabulary`.
- AC2: the row names every required stage and the this-repo-only scope, and links `../.claude/skills/factory/SKILL.md`.
- AC3: "These seven" appears and "These six" does not.
- AC4: `GLOSSARY.md` has Skill (200), Software factory (204), Stakeholder map (208), and the entry links `playbook/01-ai-dlc-methodology.md#the-vocabulary`.
- AC5: the row and the glossary entry agree.
- AC6: ADR 0026 follows the template (Status Proposed, Date 2026-10-25, Deciders Playbook maintainers (Stephen Morleys)). Chapter 01 References has the `Decisions:` link, in the same format as `playbook/11-learning-paths.md`.
- AC7: `reviewed: 2026-10-25` in both files.
- AC8: the checks above pass.

Round-1 blocking finding (rebase onto main and resolve conflicts): fixed.

Scope is clean. The diff touches only the three in-scope files.

- [note] `factory/jobs/001-software-factory-vocabulary/round-1/` has no `review-code.md`. Nothing from my lens was carried over, so there was nothing to re-check.
