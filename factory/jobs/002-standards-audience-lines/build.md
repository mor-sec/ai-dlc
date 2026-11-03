# Build — 002-standards-audience-lines

## Round 1

- What changed: one `Audience: …` sentence inserted after the first (or second) sentence of the opening paragraph in each file. The rest of each paragraph is unchanged.
  - `standards/adr-template.md`: "Audience: developers and architects who propose, draft, or approve a decision."
  - `standards/bolt-plan-template.md`: "Audience: developers, as the Driver who asks for the plan and the pod that reviews it."
  - `standards/claude-md-template.md`: "Audience: developers setting up or maintaining a repo's steering file."
  - `standards/model-selection.md`: "Audience: developers choosing a model for a task, and engineering leaders who own the cost and the quarterly review."
  - `standards/unit-of-work-template.md`: "Audience: product owners and developers who draft, approve, and execute Units of Work."
  - `standards/skills/README.md`: "Audience: platform engineers who ship skills in the baseline plugin, and developers who install or write one."
- AC1 met: `git diff HEAD~1` shows one changed line per file, each the opening paragraph after the H1, each now containing `Audience:`.
- AC2 met: each audience matches front-matter (developers+architects; developers as Driver/pod; developers; developers+engineering leaders; product owners+developers). `skills/README.md` has no front-matter; it names who ships (platform engineers, per the baseline-plugin sentence) and who installs or writes skills (developers), as the spec asks.
- AC3 met: `grep -L "Audience:" standards/*.md standards/skills/README.md` prints nothing.
- AC4 met: `git diff -U0 HEAD~1 | grep '^@@'` shows only line 10 (line 3 for the README) changed in each file, above every fenced template body.
- AC5 met: `git diff HEAD~1 -- standards/ | grep '^[-+]reviewed:'` prints nothing.
- AC6 partly met. Links: 0 broken of 105 files. Structure: 0 violations. Lint: 0 errors outside `prince2-7/` (`npx -y markdownlint-cli2 "**/*.md" "#prince2-7"` gives 0 errors over 79 files). The full repo lint reports 165 errors, all in `prince2-7/`. That folder was committed in 7338490 on main before this job, is not ignored by `.markdownlint-cli2.yaml`, and this job does not touch it. The failure exists on main already and is out of scope here; it needs its own job (fix the files, or add the folder to `ignores`).
- Blocking review findings: none (round 1).
- Checks: lint ✓ (changed files; the pre-existing `prince2-7/` failures are noted above) links ✓ structure ✓ mermaid skipped
- Commit: 7ad2637

Status: READY
