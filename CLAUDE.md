# AI-DLC Playbook

Org-wide standards repo: the playbook chapters, the reusable templates, and the decisions behind them. Audience: humans and agents editing this repo. Everything here is markdown; `standards/markdown-style-guide.md` applies to this repo before any other.

## Commands

- Lint: `npx -y markdownlint-cli2 "**/*.md"`
- Links: `python3 scripts/check-links.py`
- Mermaid: `scripts/check-mermaid.sh`
- Structure (front-matter, chapter endings, README rows, glossary, ADR numbering): `python3 scripts/check-structure.py`
- All four run in CI on every PR (`.github/workflows/docs.yml`); run them before pushing.

## Layout

- `playbook/NN-slug.md` — the chapters, read in order. `playbook/appendix-*.md` — worked examples.
- `standards/` — templates and dated references that other repos copy. `standards/skills/` — reference skills.
- `docs/adr/` — decisions about the playbook itself. `docs/README.md` is the map.
- `README.md` is the front door; every new chapter or standard gets a row there. `START-HERE.md` is the one-page map: links only, no restated content; add a line when a new gate, template, or rule belongs on it.
- `GLOSSARY.md` defines every term. Read it first; when you introduce a term, add an entry.

## Working agreements

- Chapters end with Anti-patterns, Tips & tricks, References, and prev/next links. Keep that shape.
- Cross-reference by relative link; never restate another chapter's content — link to it.
- New vocabulary enters the Chapter 01 table first, then gets used elsewhere.
- Any change to a recommendation or a standard gets an ADR in `docs/adr/` (template: `standards/adr-template.md`).
- Dated facts (model names, vendor status, prices) live in `standards/` with a `reviewed:` front-matter date, never inline in a chapter.
- Every chapter and standard carries front-matter (`owner`, `audience`, `reviewed`). Bump `reviewed` when you substantively edit a file.
- Plan mode for anything touching more than one file; direct edits for typos and link fixes.

## Sharp edges

- Mermaid node labels need `<br/>` for line breaks, not `\n` (see commit 6809ebc).
- Templates in `standards/` wrap their copyable body in a fenced ` ```markdown ` block; headings inside the fence are content, not structure, so don't "fix" them.
- Chapter H1s use an em dash (`# 03 — Tooling Strategy`); anchors to them are awkward, so link to H2 sections instead.
