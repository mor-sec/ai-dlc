VERDICT: PASS

# Security review — 001-software-factory-vocabulary, round 2

No security review was written in round 1 (that round had only `review-human.md`), so there are no earlier blocking findings to re-check. The round-2 diff only adds the rebase resolution of the `reviewed:` lines, which carries no security risk.

- [note] `docs/adr/0026-software-factory-for-maintaining-this-repo.md:19` says "that push is where review happens". That holds only if the person pushing actually reads the diff of `main` against the remote first. A local merge followed by a habitual `git push` would let an agent-approved change reach the shared remote with no human looking at it. The claim is consistent with `.claude/skills/factory/SKILL.md:63` ("Local only; never push"), and the ADR is `Proposed` for a human to accept, so this doesn't need another round. A later job could add one line asking the pusher to review `git log origin/main..main` before pushing.
- [note] `docs/adr/0026-software-factory-for-maintaining-this-repo.md:4` names the maintainer as Decider. That is personal data, but every existing ADR does the same and the spec requires it. Fine.
- [note] The text in all three changed files matches the skill: never pushes (`SKILL.md:63`), and a human is asked at round 2 or later (`SKILL.md:40`). Nothing in the change weakens `standards/agent-baseline.md` or Chapter 06. The merge-gate tension with ADR 0014 is recorded in an ADR, as `CLAUDE.md` requires. The change has no secrets, hostnames, or copyable commands.
