# Spec — 001-software-factory-vocabulary: Add "software factory" to the Chapter 01 vocabulary table and GLOSSARY.md, describing the `/factory` loop in this repo

## Intent

The repo now ships a software factory (`/factory`, defined in `.claude/skills/factory/SKILL.md`, with agents in `.claude/agents/factory-*.md` and state in `factory/`). The term isn't defined anywhere a reader or agent would look. This change defines it once, where CLAUDE.md says new vocabulary goes: first a row in the Chapter 01 vocabulary table, then a glossary entry. A reader who meets "factory" in CLAUDE.md or on a branch name then learns what it is: an agent loop that runs one feature through spec, build, four parallel reviews, and an approver. It merges to the local `main` or stops at `needs-human`. It never pushes, so the human who pushes is still the merge gate. The definition must also say the factory is tooling for maintaining this repo, not a delivery practice the playbook recommends to product pods. Without that, the term reads as a change to the method. An ADR records that decision.

## Scope

- `playbook/01-ai-dlc-methodology.md`
  - Add one row to the table under `## The vocabulary`. The AI-DLC cell is exactly `**Software factory**`; the structure check parses that cell. The Traditional cell names the hand-run equivalent, for example "Hand-run PR cycle (author, reviewers, merge)".
  - The What changed cell describes the loop in one or two sentences: spec, build, four parallel reviews (security, UX, UI, code), approver, then a local merge or `needs-human`. It says that at most two review rounds run before a human is asked. It says the loop never pushes, and that it is used to maintain this repo only. It links to `../.claude/skills/factory/SKILL.md`.
  - Change "These six are the core" in the paragraph below the table to "These seven are the core".
  - Bump `reviewed:` to `2026-10-25`.
- `GLOSSARY.md`
  - Add a `## Software factory` entry between `## Skill` and `## Stakeholder map`, keeping alphabetical order.
  - The entry defines the term in the same register as its neighbours. It links to `playbook/01-ai-dlc-methodology.md#the-vocabulary`. The structure check requires every entry to link to a chapter or standard, so a link to the skill file alone fails.
  - It may also link to `.claude/skills/factory/SKILL.md`.
  - Bump `reviewed:` to `2026-10-25`.
- `docs/adr/0026-software-factory-for-maintaining-this-repo.md` (new, from `standards/adr-template.md`)
  - Records why the factory is core vocabulary, and that it is scoped to this repo.
  - Records that the approver agent merges only to the local `main`. A human push remains the merge gate, consistent with "No level merges" in `playbook/03-tooling-strategy.md` (section "Agent autonomy levels").
  - `Status: Proposed`, because an agent is never a decider. `Deciders: Playbook maintainers (Stephen Morleys)`. Date `2026-10-25`.
  - The Chapter 01 References section gets a `Decisions:` link to it, in the format other chapters use (see `playbook/11-learning-paths.md` References).

**Out of scope**

- Mentioning the factory in any other chapter, `START-HERE.md`, `README.md`, or `docs/README.md`. The factory is repo tooling, not a gate, template, or rule for product repos.
- Changing the factory's skill, agents, dashboard, or backlog.
- Recommending a factory-style loop to product pods, or adding a new autonomy level for it. Either one needs its own Unit of Work and ADR.
- Cleaning up the glossary's existing ordering slips ("Champion" before "Business-rules extract", "MCP server" after "Model tier").

## Acceptance criteria

- AC1: Chapter 01's vocabulary table has a row whose AI-DLC cell is `**Software factory**`. Check: `grep -n '| \*\*Software factory\*\* |' playbook/01-ai-dlc-methodology.md` returns one line, inside `## The vocabulary`.
- AC2: That row's What changed cell names all of these: spec, build, four parallel reviews, approver, local merge or `needs-human`, never pushes, and this-repo-only scope. It links to `../.claude/skills/factory/SKILL.md`. Check: read the row.
- AC3: The sentence below the table says "seven", not "six". Check: `grep -n 'These seven are the core' playbook/01-ai-dlc-methodology.md` returns one line, and `grep -n 'These six' playbook/01-ai-dlc-methodology.md` returns none.
- AC4: `GLOSSARY.md` has exactly one `## Software factory` heading, placed after `## Skill` and before `## Stakeholder map`. Its body links to `playbook/01-ai-dlc-methodology.md#the-vocabulary`. Check: `grep -n -A0 '^## S' GLOSSARY.md` shows the order. Reading the entry shows the link.
- AC5: The glossary entry and the Chapter 01 row agree. Both describe the same stages, the same local-merge-only behaviour, and the same scope, with no contradiction. Check: read them side by side.
- AC6: `docs/adr/0026-software-factory-for-maintaining-this-repo.md` exists. It follows `standards/adr-template.md` and has `Status: Proposed`, `Date`, and `Deciders` lines. It explains why the factory is scoped to this repo and why a local merge with a human push keeps the merge gate human. Chapter 01's References links to it. Check: `python3 scripts/check-structure.py` reports no ADR gap or missing field. `grep -n '0026' playbook/01-ai-dlc-methodology.md` returns the References link.
- AC7: `reviewed:` is `2026-10-25` in both `playbook/01-ai-dlc-methodology.md` and `GLOSSARY.md`. Check: `grep -n '^reviewed:' playbook/01-ai-dlc-methodology.md GLOSSARY.md`.
- AC8: All four checks in CLAUDE.md pass: `npx -y markdownlint-cli2 "**/*.md"`, `python3 scripts/check-links.py`, `scripts/check-mermaid.sh`, and `python3 scripts/check-structure.py`.

## Conventions that apply

- **Chapter 01 vocabulary first.** The term enters the Chapter 01 table, then the glossary.
- **Glossary entry.** Required for any new term. `scripts/check-structure.py` also fails if a Chapter 01 bolded term has no entry.
- **ADR.** Adding a core term that describes an agent which approves and merges touches a recommendation: the core method vocabulary and the autonomy rule "No level merges". `docs/adr/0026-…` covers it, with status Proposed.
- **`reviewed` bump.** Both edited files are edited substantively.
- **Cross-reference, don't restate.** The Chapter 01 row and glossary entry summarize the loop in one or two sentences and link to `.claude/skills/factory/SKILL.md` for the detail. They do not copy its steps.
- **README row.** None. No new chapter or standard.
