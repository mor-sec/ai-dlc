# Spec — 002-standards-audience-lines: Give every file in `standards/` a first line that states its audience and purpose, where one is missing

## Intent

`standards/markdown-style-guide.md` (Structure, rule 2) says line one of a document states its audience and purpose. Most files in `standards/` already do, using the house form: the first paragraph after the H1 says what the file is, then `Audience: <who>.` Six files state a purpose but never name a reader. This change adds the missing `Audience:` clause to those six, so a reader landing on any standard learns in one line whether it is for them. The audience named must agree with the file's `audience:` front-matter, where it has one.

## Scope

Edit the opening paragraph (the first paragraph after the document's H1, outside any fenced template body) of each of these files:

- `standards/adr-template.md` (front-matter: developers, architects)
- `standards/bolt-plan-template.md` (front-matter: developers; the text already mentions the Driver and the pod, so name them)
- `standards/claude-md-template.md` (front-matter: developers)
- `standards/model-selection.md` (front-matter: developers, engineering leaders)
- `standards/unit-of-work-template.md` (front-matter: product owners, developers)
- `standards/skills/README.md` (no front-matter; name whoever installs or writes reference skills)

Add one `Audience: …` sentence to the existing paragraph, or fold the audience into its first sentence. Keep the rest of the paragraph as it is.

**Out of scope**

- Files whose opening paragraph already contains `Audience:`: `agent-baseline.md`, `community-of-practice-charter-template.md`, `consolidation-template.md`, `faq-template.md`, `markdown-style-guide.md`, `metrics-reference.md`, `pilot-charter-template.md`, `post-incident-review-template.md`, `skill-template.md`, `steering-evals.md`, `test-review-checklist.md`.
- The `SKILL.md` bodies under `standards/skills/*/`. Agents load them, and they follow `standards/skill-template.md`, whose first body line is "the job this skill does and for whom". Their `description` front-matter already does the routing.
- Anything inside a fenced ` ```markdown ` template body. Those headings and lines are content that teams copy, not this file's own opening line.
- Adding front-matter to `standards/skills/README.md`, rewording purpose sentences, and adding a check script that enforces the rule.

## Acceptance criteria

- AC1: For each of the six files in Scope, the first paragraph after the H1 contains `Audience:`. Check: open each file and read the paragraph after the H1. Or run `grep -c "Audience:"` on each file and confirm the count is at least 1, with the match on that opening paragraph's line.
- AC2: Every audience named in AC1 agrees with that file's `audience:` front-matter value: the same groups, possibly reworded or more specific, and none added or dropped without reason. Check: compare the two lines in each file.
- AC3: After the change, every non-`SKILL.md` file in `standards/` has `Audience:` in its opening paragraph. Check: `grep -L "Audience:" standards/*.md standards/skills/README.md` prints nothing.
- AC4: No template body changed. Check: `git diff` shows no changed lines between a ` ```markdown ` fence and its closing fence.
- AC5: No `reviewed:` front-matter value changed. Check: `git diff -- standards/ | grep '^[-+]reviewed:'` prints nothing.
- AC6: All four checks in CLAUDE.md pass.

## Conventions that apply

- ADR: none. This applies an existing rule from the style guide. It does not change any recommendation or standard.
- `reviewed` bump: none, on purpose. Adding an audience clause is not a substantive edit. For `standards/model-selection.md` in particular, `reviewed` records when the dated model table was last checked, and bumping it would falsely claim the table had been re-verified.
- README row, `START-HERE.md` line, Chapter 01 vocabulary, glossary entry: none. No new files or terms.
