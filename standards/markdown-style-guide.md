# Markdown Style Guide

The writing standard for all documentation. Audience: everyone who writes docs — humans and agents (this file is loaded as steering context for documentation work). Rationale for markdown-as-standard: [Chapter 09](../playbook/09-documentation-standards.md).

## File conventions

- GitHub-Flavored Markdown, `.md`, UTF-8, kebab-case filenames (`payment-retry-design.md`)
- One document, one purpose. If you're writing "Part 2 of…", split the file.
- Every docs folder has a `README.md` that orients a new reader in under two minutes.
- Optional front-matter for machine handling:

```yaml
---
owner: payments-pod
audience: developers
reviewed: 2026-08-29
---
```

## Structure

1. **One H1**, matching the document's purpose. Heading levels never skip (H2 → H4 is a lint error).
2. **Line one states the audience and purpose.** "Runbook for on-call responding to payment-queue backlog." If you can't write this line, you don't know why the doc exists.
3. **Sentence case headings** ("Handling retries", not "Handling Retries").
4. **Self-contained sections.** Each H2 should make sense retrieved alone — descriptive headings, no "see above" references. This serves skimming humans and agents pulling single sections into context.
5. **End with links onward** (related docs, next steps) rather than trailing off.

## Prose

- **Lead with the point.** Conclusion first, rationale after — in the doc, in each section, in each paragraph.
- Short sentences, active voice, no filler ("it should be noted that" → delete).
- Spell out a term before abbreviating it, once, then use the abbreviation.
- Use the ubiquitous language of the bounded context ([Chapter 04](../playbook/04-architecture.md)) — the glossary in `docs/domain/<context>/language.md` wins every naming dispute.
- Dates are absolute and ISO (`2026-08-29`), never "last month".

## Elements

| Element | Rule |
|---|---|
| Tables | For enumerable facts only; reasoning goes in prose. No 5-paragraph cells. |
| Code blocks | Always language-tagged (` ```java `). Runnable > illustrative. |
| Diagrams | Mermaid in the document. Binary images only for screenshots of external systems. |
| Links | Relative links within the repo (they survive renames and work in agents' file reads); descriptive text, never "click here". |
| Lists | Bullets for unordered, numbers only when order matters. One idea per bullet. |
| Callouts | Blockquote with a bold lead: `> **Warning:** …`. Use sparingly — three warnings per page is zero warnings. |
| Emphasis | Bold for the load-bearing phrase a skimmer must catch. Italics rarely. No ALL CAPS. |

## Written by agents, reviewed by humans

- Agent-drafted docs follow this guide automatically (this file is in their context); the human reviewer checks *truth and emphasis*, not formatting.
- Wholly generated reference docs (API refs, event catalogs) open with: `> Generated from <source> — edit the source, not this file.`

## Enforced mechanically

CI runs markdownlint (config in the repo), a relative-link checker, and Mermaid syntax validation — so reviews never spend human attention on what a machine can check. See [Chapter 09](../playbook/09-documentation-standards.md#enforced-in-ci).
