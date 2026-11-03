# 0026 — Define the software factory as core vocabulary, scoped to maintaining this repo, with a local-only merge

- **Status:** Accepted
- **Date:** 2026-10-25
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; factory job 001-software-factory-vocabulary

## Context

The repo now ships a software factory: the `/factory` skill ([SKILL.md](../../.claude/skills/factory/SKILL.md)), its agents in `.claude/agents/factory-*.md`, and its state in `factory/`. It runs one feature through spec, build, four parallel reviews (security, UX, UI, code), and an approver agent. The term appears in CLAUDE.md and in branch names (`factory/<id>`), but no chapter or glossary entry defines it. Readers and agents meet the word with nothing to look up.

Two things make the definition sensitive. First, it would sit in the core method vocabulary of [Chapter 01](../../playbook/01-ai-dlc-methodology.md#the-vocabulary), so a reader could take it as a new delivery practice for product pods. Second, the loop ends with an agent that approves and merges, and [Chapter 03](../../playbook/03-tooling-strategy.md#agent-autonomy-levels) says "No level merges." The definition has to square with that rule rather than quietly bend it.

## Decision

We will add "Software factory" to the Chapter 01 vocabulary table and the glossary, defined as tooling for maintaining this repo only, whose approver merges to the local `main` and never pushes.

- **Scope.** The factory maintains this repo. The playbook does not recommend it to product pods, and it adds no autonomy level. Either change needs its own Unit of Work and ADR.
- **Merge gate.** The approver agent merges only into the local `main`, or stops at `needs-human`; after at most two review rounds a human is asked. Nothing reaches the shared remote until a human pushes, and that push is where review happens. The merge gate therefore stays human, consistent with "No level merges" ([ADR 0014](0014-agent-autonomy-levels.md)).
- **Drafting.** An agent drafted this ADR; the deciders accepted it on 2026-11-03.

## Options considered

### Option A — Core vocabulary, scoped to this repo, local merge only  ← chosen

- Pros: the term is defined where CLAUDE.md says new vocabulary goes; the scope line stops it reading as a method change; the local-only merge keeps the human push as the gate.
- Cons: the Chapter 01 table now holds one term about repo tooling next to six about the method.

### Option B — Glossary entry only

- Pros: keeps the Chapter 01 table purely about the method.
- Cons: breaks the working agreement that new vocabulary enters the Chapter 01 table first, and the structure check expects the two to stay in step.
- Rejected because: the repo's own rule puts new terms in Chapter 01 first; a scoped row is cheaper than an exception to that rule.

### Option C — Recommend the factory to product pods as a new autonomy level

- Pros: would let pods use the same loop.
- Cons: needs evidence the playbook does not have yet, and a level that merges contradicts ADR 0014.
- Rejected because: this repo has no quarter of evidence for the loop, which ADR 0014 requires before a workflow moves up a level.

## Consequences

- Positive: "factory" in CLAUDE.md, branch names, and commits has one definition to look up.
- Positive: the boundary between repo tooling and recommended practice is written down.
- Negative: a reader skimming the Chapter 01 table may still miss the scope line and read the factory as method.
- Follow-ups: none.

## Revisit when

A pod asks to run a factory-style loop on a product repo, or the factory gains the ability to push. Either one reopens the scope and the merge-gate reasoning.
