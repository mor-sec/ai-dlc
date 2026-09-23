# 0016 — Classify agent context by the organization's data classification, and record provenance of generated code

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

[Vendor governance](../../playbook/03-tooling-strategy.md#vendor-governance) ([ADR 0010](0010-vendor-governance-for-the-primary-agent.md)) records what the provider does with data: retention, inference region, and which repos are excluded. It does not say which data a pod may put into a session in an included repo, what happens to transcripts and logs that contain it, or whether real records may become test fixtures. [Chapter 06](../../playbook/06-security-shift-left.md) handled secrets but not personal or customer data.

The output side was also thin. License contamination had a scanner row, but nothing covered provenance of generated code, pasting third-party code into sessions, or the vendor's position on output ownership, which legal and audit functions ask about early.

## Decision

We will apply the organization's existing data classification to agent sessions: public and internal data as is, confidential only under recorded vendor terms, and restricted data never as real values. We will also require agent-assisted commits to carry a co-author trailer and record the vendor's output-ownership and indemnity terms in the vendor-terms ADR.

Session records inherit the classification of what the agent read; fixtures are synthetic by rule; third-party code enters context only when its license allows. Detail: [Chapter 06, Data in context and generated-code ownership](../../playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership).

## Options considered

### Option A — Reuse the existing classification, applied per session  ← chosen

- Pros: no new scheme to learn; data owners already understand the classes; masked MCP access lets agents work with restricted systems' structure.
- Cons: pods must know the classification of what they open in a session; synthetic fixtures take effort to make realistic.

### Option B — A separate AI data policy

- Pros: can be tailored to agent risks.
- Cons: a second classification that drifts from the first; data owners must learn it.
- Rejected because: the question is the same one the existing classification answers (who may see this?), and the model provider is one more recipient.

### Option C — Rely on vendor zero-retention terms alone

- Pros: simplest; the provider does not keep the data.
- Cons: transcripts, logs, tickets, and git keep it on our side; contracts with customers may forbid any third-party processing regardless of retention.
- Rejected because: most leakage paths are internal, and retention terms do not cover them.

## Consequences

- Positive: security and data-protection reviewers have a clear rule to audit; restricted data stays out of git history; provenance supports later audit and license questions.
- Negative: reproducing data-dependent bugs needs synthetic data work; masked MCP servers are new platform-pod work.
- Follow-ups: masked or metadata-only MCP servers for restricted stores; PII scanning on agent-authored diffs; a steering-eval golden task for synthetic fixtures.

## Revisit when

The organization changes its data classification scheme, a regulator issues guidance on AI processing of personal data that the rules do not meet, or the vendor's output-ownership terms change.
