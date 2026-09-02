---
owner: platform-enablement
audience: developers, architects, product owners, engineering leaders
reviewed: 2026-09-02
review-cadence: quarterly
---

# 09 — Documentation Standards

Under AI-DLC, documentation is not a record-keeping chore — it is **agent context**. Every doc is read by two audiences now: humans and the agents that build the system. That single fact drives the whole standard: markdown, in git, next to the code, updated in the same PR as the change it describes.

## The standard: markdown, as code

**All engineering and product-adjacent documentation is Markdown (GitHub-Flavored), versioned in git.** Word documents, wiki pages, and slide decks are not documentation of record; when they exist (for an executive audience), they are *exports* from a markdown source.

Why this is non-negotiable under AI-DLC:

1. **Agents read and write it natively.** Markdown is effectively the token-native prose format of current LLMs; a Confluence page behind an API is second-class context at best.
2. **Docs-as-code gets docs into the loop:** PR review, diffability, CI checks (link checking, linting), and the same traceability as code ([Chapter 08](08-github-jira.md)).
3. **Same-PR updates become possible** — and therefore mandatory: a change and its documentation land in one reviewed diff. This is the only doc-freshness mechanism that has ever worked.

### Where things live

| Content | Location |
|---|---|
| Repo/service docs, runbooks, pipeline docs | `docs/` in the owning repo |
| Domain models, glossaries, event catalogs | `docs/domain/` ([Chapter 04](04-architecture.md)) |
| Architecture decisions | `docs/adr/` — [ADR template](../standards/adr-template.md) |
| Steering | `CLAUDE.md` (+ skills) — [template](../standards/claude-md-template.md) |
| Org-wide standards (this playbook) | Dedicated repo, same rules |
| Diagrams | **Mermaid in the markdown** — diagrams-as-code, no binary diagram files; draw.io XML only when Mermaid genuinely can't express it |

Writing rules are in the [Markdown Style Guide](../standards/markdown-style-guide.md); the short version: one H1, sentence-case headings, tables for enumerable facts, prose for reasoning, every doc opens with who it's for and links onward. **Write for retrieval:** self-contained sections with descriptive headings serve both a skimming human and an agent pulling context.

### Enforced in CI

- Link check (no dead relative links), markdownlint, Mermaid syntax check
- PR template asks "docs updated?" — reviewers treat a `No` on a behavior change as a failing check
- A nightly agent job flags docs whose subject code changed recently without them (staleness candidates for Friday consolidation, [Chapter 02](02-ways-of-working.md))

## The DocLang exploration

### What it is

[DocLang](https://github.com/doclang-project) is an emerging **AI-native document markup format**, developed by a [LF AI & Data Foundation working group launched in June 2026](https://lfaidata.foundation/press-release/2026/06/09/lf-ai-data-foundation-launches-doclang-specification-working-group-to-advance-an-open-standard-for-ai-native-documents/), founded by IBM, NVIDIA, and Red Hat with ABBYY and HumanSignal, with the stated aim of becoming an ISO standard. It grew out of the Docling ecosystem's work on document conversion for AI.

Its pitch: PDF/HTML/LaTeX were designed for *rendering* and lose structure when tokenized; markdown is token-friendly but **under-expressive** — it can't carry geometry (where on the page), rich semantic hierarchy, provenance, or non-text modalities. DocLang is an unambiguous XML vocabulary designed to map 1-to-1 to LLM tokens while preserving precise structure, tables, formulas, and code — and extending to audio/video (transcripts, speakers, timestamps).

### Our assessment: markdown and DocLang solve different problems

- **Markdown** is a format humans *author* in. Its weakness (minimal structure) is mostly a feature for prose that people write and review.
- **DocLang** is a format machines *convert into* — the interchange representation for documents that were born elsewhere (PDFs, scans, contracts, decks, recordings) and are headed into AI pipelines. Its strength is fidelity, which is exactly what authored engineering prose doesn't need and ingested enterprise documents desperately do.

So the question is not "markdown vs. DocLang" but **where each sits in the pipeline**.

### Adoption posture: adopt markdown now, pilot DocLang at the ingestion boundary

| Horizon | Action |
|---|---|
| **Now** | Markdown for all authored docs (this chapter). No change. |
| **Pilot (next 1–2 quarters)** | Use Docling/DocLang-aware conversion where we ingest *external/legacy* documents into AI workflows: contract analysis, legacy system documentation for [Chapter 10](10-legacy-modernization.md) modernization (scanned specs, mainframe docs!), and RAG over enterprise document stores (a natural Snowflake Cortex Search pairing, [Chapter 05](05-rapid-prototyping.md)). Measure retrieval/extraction quality vs. naive PDF-to-markdown. |
| **Watch** | Spec ratification progress, tokenizer-level support in major models, and authoring tools. **Trigger to reassess as an authoring standard:** major agent tooling consumes DocLang natively *and* editors make it as writable as markdown. Until both, authoring in XML is a tax with no payer. |

Record the decision as an ADR when the pilot concludes; this section states the default posture, not a verdict for eternity.

## Documentation the agent writes

Agents draft; humans review — same as code:

- **Generated-and-maintained:** API references from code, event catalogs from schemas, changelog entries, PR descriptions, runbook drafts from incident timelines ([Chapter 07](07-devops-automation.md)).
- **Agent-drafted, human-owned:** ADRs, domain model updates, Unit of Work write-ups.
- **Human-first:** intent, product rationale, anything political. An agent polishing prose is fine; an agent inventing *why* is how orgs gaslight themselves.

Label wholly-generated reference docs as such, with the generation source, so readers know to fix the source rather than the output.

## Anti-patterns

- **The wiki shadow-economy.** Confluence pages sprouting because "it's easier" — within a quarter agents and humans disagree about which copy is true. Kill by policy *and* by making the markdown path genuinely easier (templates, skills).
- **Doc debt as backlog.** "Documentation sprint" = documentation bankruptcy. Same-PR updates or it didn't happen.
- **Screenshot architecture.** Diagrams as PNGs exported from someone's head. Not diffable, not readable by agents, stale on arrival. Mermaid or it doesn't merge.
- **Premature DocLang.** Rewriting authored docs into XML for AI-ness points. You'd be trading author ergonomics for fidelity no authored doc needs.
- **Docs nobody addresses.** Every doc names its audience in line one, or it's a diary.

## Tips & tricks

- **`docs/README.md` as the map:** every repo's docs folder opens with a two-minute orientation — agents use it to navigate, humans to onboard.
- **Front-matter for machines:** a small YAML header (`owner`, `reviewed`, `audience`) on each doc makes staleness sweeps and steering-file pointers trivial.
- **Let the agent be the first reader:** after writing a doc, ask a fresh session to perform the task the doc describes. Where it stumbles, humans would too. Cheapest doc QA in existence.
- **Export, don't author, for execs:** `md → slides/pdf` via Marp/pandoc keeps the single source while meeting the audience where it is.

## References

- [Markdown Style Guide](../standards/markdown-style-guide.md) · [ADR template](../standards/adr-template.md)
- [DocLang project](https://github.com/doclang-project) · [LF AI & Data announcement](https://lfaidata.foundation/press-release/2026/06/09/lf-ai-data-foundation-launches-doclang-specification-working-group-to-advance-an-open-standard-for-ai-native-documents/) · [Docling](https://docling-project.github.io/docling/)
- Previous: [Chapter 08 — GitHub + Jira](08-github-jira.md) · Next: [Chapter 10 — Legacy Modernization](10-legacy-modernization.md)
