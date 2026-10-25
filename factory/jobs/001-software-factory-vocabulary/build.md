# Build — 001-software-factory-vocabulary

## Round 1

- What changed, file by file (worktree `.claude/worktrees/factory-001-software-factory-vocabulary`, branch `factory/001-software-factory-vocabulary`, from `main` at b3249a4):
  - `playbook/01-ai-dlc-methodology.md`: added a `**Software factory**` row to the `## The vocabulary` table. Its Traditional cell reads "Hand-run PR cycle (author, reviewers, merge)". "These six" becomes "These seven". Added a `Decisions:` link to ADR 0026 under References. `reviewed:` is now 2026-10-25.
  - `GLOSSARY.md`: added a `## Software factory` entry between `## Skill` and `## Stakeholder map`. It links to `playbook/01-ai-dlc-methodology.md#the-vocabulary` and `.claude/skills/factory/SKILL.md`. `reviewed:` is now 2026-10-25.
  - `docs/adr/0026-software-factory-for-maintaining-this-repo.md` (new, from the ADR template): Status Proposed, Date 2026-10-25, Deciders "Playbook maintainers (Stephen Morleys)". It covers the this-repo-only scope, the local-merge-only approver, and why a human push keeps the merge gate human, consistent with ADR 0014 "No level merges". It rejects two alternatives: a glossary-only entry, and offering the factory to pods as a new autonomy level.
- AC1 met: `grep -n '| \*\*Software factory\*\* |'` returns line 35, inside `## The vocabulary` (lines 25–38).
- AC2 met: the row names spec, build, four parallel reviews (security, UX, UI, code), approver, local merge to `main` or `needs-human`, at most two review rounds, never pushes, and this-repo-only scope. It links `../.claude/skills/factory/SKILL.md`.
- AC3 met: `These seven are the core` is on line 37. `grep -c 'These six'` returns 0.
- AC4 met: `grep -n '^## S' GLOSSARY.md` shows Skill (172), Software factory (176), Stakeholder map (180). The entry links `playbook/01-ai-dlc-methodology.md#the-vocabulary`.
- AC5 met: both texts give the same stages, the same local-merge-only behaviour, the same two-round limit, and the same scope. The glossary entry uses the Chapter 01 wording almost word for word.
- AC6 **not met**: the ADR file exists, has all fields, and Chapter 01 links to it (`grep -n 0026` returns line 122). But `python3 scripts/check-structure.py` reports `docs/adr: gap in numbering, no 0019` … `no 0025` (7 violations). The worktree is built from `main`, and `main` only has ADRs 0001–0018. ADRs 0019–0025 exist only as untracked files in the main working tree, on branch `playbook-gaps`.
- AC7 met: `grep -n '^reviewed:'` shows 2026-10-25 in both files.
- AC8 **not met**, for the same reason: the structure check fails on the ADR gap. With those 7 violations excluded, it passes; the glossary-to-Chapter 01 term check is clean.
- Checks: lint ✓ (0 errors). Links ✓ (71 files, 0 broken; run on a copy in the scratchpad, because `check-links.py` skips every path containing `worktrees` and checks 0 files inside the worktree). Structure ✗ (only the ADR gap 0019–0025). Mermaid skipped (no Mermaid touched).
- Commit: eaf7167

Status: BLOCKED — the spec requires ADR number 0026, but `main` ends at 0018, so the structure check fails with gaps 0019–0025 (AC6, AC8). ADRs 0019–0025 are uncommitted on `playbook-gaps`. A human needs to choose one of two fixes. (a) Land 0019–0025 on `main` first, then this branch passes unchanged; rebase it if needed. (b) Renumber this ADR to 0019 now; it will then collide with the uncommitted 0019 later.

## Round 2

- What changed: I rebased `factory/001-software-factory-vocabulary` onto `main` at 5727699. That commit now includes ADRs 0019–0025 (0097a41) and the link checker's worktree fix. No content changed beyond conflict resolution.
  - `GLOSSARY.md`, `playbook/01-ai-dlc-methodology.md`: the only conflicts were the front-matter `reviewed:` lines (`main` had 2026-09-29 and 2026-09-30). Both now read 2026-10-25, as AC7 requires.
  - `docs/adr/0026-software-factory-for-maintaining-this-repo.md`: applied cleanly. 0026 now follows 0025.
- AC1 met: the `**Software factory**` row is on line 82, inside `## The vocabulary` (lines 72–85).
- AC2 met: the row is unchanged from round 1. It names spec, build, four parallel reviews, approver, local merge or `needs-human`, never pushes, and this-repo-only scope, and links to `../.claude/skills/factory/SKILL.md`.
- AC3 met: `These seven are the core` is on line 84, and `These six` doesn't appear. The table has seven body rows.
- AC4 met: `grep -n '^## S' GLOSSARY.md` lists Session hygiene (196), Skill (200), Software factory (204), Stakeholder map (208).
- AC5 met: the glossary entry and the Chapter 01 row are unchanged from round 1 and still agree.
- AC6 met: `check-structure.py` reports 0 violations. `grep -n 0026` returns the References `Decisions:` link on line 169.
- AC7 met: both files have `reviewed: 2026-10-25`.
- AC8 met: all four checks pass (results below).
- Blocking finding "rebase onto main and resolve conflicts" (review-human.md): fixed. Rebased, and resolved the two `reviewed:` conflicts in favour of 2026-10-25.
- Checks: lint ✓ (0 errors). Links ✓ (80 files, 0 broken; now run in place, because `main`'s fix makes the checker scan the worktree). Structure ✓ (0 violations). Mermaid skipped (no Mermaid touched).
- Commit: 234c31a (the round-1 commit rebased; no new commit needed)

Status: READY
