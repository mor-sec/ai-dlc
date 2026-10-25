VERDICT: PASS

# UX review — 001-software-factory-vocabulary, round 2

Round 1 had one blocking finding (review-human.md: rebase onto main). Fixed: the branch is on main at 5727699, and `check-structure.py` reports 0 violations in the worktree.

- [note] `playbook/01-ai-dlc-methodology.md:82` — the What changed cell leads with the point ("The agent loop that maintains this repo, not a practice for product pods"), states scope up front, and links to the skill for detail instead of restating steps. A reader gets it on first read.
- [note] `GLOSSARY.md:204` — same register as its neighbours, in the right alphabetical slot, links back to Chapter 01 `#the-vocabulary` and to the skill. The factory is deliberately absent from README, START-HERE and docs/README (out of scope in the spec), so a reader finds it through the glossary, CLAUDE.md, or Chapter 01 only. That is intended.
- [note] `playbook/01-ai-dlc-methodology.md:169` — the `Decisions:` link text ("A software factory for maintaining this repo") is a shortened form of the ADR H1. It matches how ADR 0025 is linked from Chapter 11 and is fine.
