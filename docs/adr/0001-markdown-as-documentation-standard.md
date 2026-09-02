# 0001 — Author all documentation in Markdown, in git

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook needs a documentation standard that serves two readers at once: the humans who write and review it, and the agents that load it as context. Options in use across the organization today include Confluence pages, Word documents, slide decks, and markdown scattered in repos. Each tool holds a different copy of the truth, and none of them is diffable, reviewable in a PR, or readable by an agent without an integration.

An AI-native alternative, DocLang, is emerging under an LF AI & Data working group. It offers higher structural fidelity than markdown but is an XML vocabulary with no mainstream authoring tools yet. [Chapter 09](../../playbook/09-documentation-standards.md) sets out the full comparison.

This repo also claims to dogfood its own standards, so the decision has to apply here first.

## Decision

We will author all engineering and product-adjacent documentation as GitHub-Flavored Markdown, versioned in git next to the code it describes, updated in the same PR as the change.

Diagrams are Mermaid inside the markdown. Other formats for executive audiences are exports from the markdown source, never the source. Writing rules live in the [Markdown Style Guide](../../standards/markdown-style-guide.md), and CI enforces markdownlint, relative-link checking, and Mermaid validation.

## Options considered

### Option A — Markdown in git  ← chosen

- Pros: token-native for agents; diffable and PR-reviewable; same traceability as code; zero tooling to author; same-PR doc updates become possible and therefore enforceable.
- Cons: minimal structure; no geometry or provenance; wiki-style discoverability has to be built with README maps and links.

### Option B — Confluence (or equivalent wiki) as the system of record

- Pros: familiar to non-engineers; rich editor; built-in search and permissions.
- Cons: docs drift from code because they cannot land in the same PR; agent access is second-class through an API; not diffable.
- Rejected because: freshness is the property that matters most under AI-DLC, and same-PR updates are the only mechanism that has ever kept docs fresh.

### Option C — DocLang or another structured XML format for authoring

- Pros: precise structure, provenance, and multi-modal support; designed to map to LLM tokens.
- Cons: no authoring ergonomics today; no native consumption by mainstream agent tooling; XML is a tax on every human writer.
- Rejected because: authored engineering prose does not need the fidelity, and the ecosystem is not ready. Retained as a pilot at the ingestion boundary only.

## Consequences

- Positive: one source of truth per repo; docs enter the review loop; agents read docs with a file read; this repo's CI can enforce the standard mechanically.
- Negative: executive-facing formats need an export step; teams used to wikis need templates and skills that make the markdown path genuinely easier, or a shadow wiki grows.
- Follow-ups: pilot Docling/DocLang conversion for ingested legacy documents ([Chapter 09](../../playbook/09-documentation-standards.md#the-doclang-exploration)); record the pilot's outcome as a new ADR.

## Revisit when

Major agent tooling consumes DocLang natively and editors make it as writable as markdown. Both must hold; either alone is not enough. Otherwise, reassess at the 2027-09 quarterly review of Chapter 09.
