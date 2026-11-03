ESCALATE

# Decision — 001-software-factory-vocabulary

- **It changes a recommendation, and the ADR that covers it needs a human to accept it.** The spec's own Conventions section says this change "touches a recommendation: the core method vocabulary and the autonomy rule 'No level merges'". `docs/adr/0026-software-factory-for-maintaining-this-repo.md` is `Status: Proposed` and names a human as Decider. That is correct. But if the factory merges it, an agent ends up deciding whether an agent-run merge fits ADR 0014's "No level merges" (`docs/adr/0014-agent-autonomy-levels.md`, `playbook/03-tooling-strategy.md` section "Agent autonomy levels"). This job is also the factory putting its own definition on record. A human should take that decision, not the loop being defined.
- The diff does what the spec asks and nothing more: three files (`playbook/01-ai-dlc-methodology.md`, `GLOSSARY.md`, the new ADR 0026), and nothing out of scope. `build.md` round 2 gives evidence for AC1 to AC8, and all four round-2 reviews pass with no blocking findings. Nothing else would stop an APPROVE.
- The ADR's argument has a gap worth a human look. `round-2/review-security.md` notes that the ADR's line "that push is where review happens" (ADR 0026, Decision, "Merge gate") is only true if the person pushing reads `git log origin/main..main` first. A habitual `git push` would send an agent-approved change to the remote without anyone reading it. The ADR's claim that the merge gate "stays human" depends on that habit, and nothing in the change writes the habit down.
- The change edits existing core guidance, though only slightly. "These six are the core" becomes "These seven". A repo-tooling term now sits in the method's core vocabulary table, which ADR 0026 itself lists as a Con (Option A) and a Negative consequence.
- Minor, does not decide this: `round-2/review-ui.md` notes the new What changed cell is about 65 words, against about 40 for the other cells.

## Question for a human

Do you accept ADR 0026? That means two things. (1) A repo-maintenance tool goes into the Chapter 01 core vocabulary table. (2) An agent merging into the local `main` counts as consistent with "No level merges", because your push is the gate. If yes, set ADR 0026 to `Accepted` and merge `factory/001-software-factory-vocabulary` yourself. You might also want the ADR to say that the pusher reviews `git log origin/main..main` before pushing. If no, say which part to change: drop the Chapter 01 row (that needs an exception to the "Chapter 01 first" rule), or reword the merge-gate reasoning.
