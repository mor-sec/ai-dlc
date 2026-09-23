# 0018 — Build AI features behind a domain adapter, gated by eval sets with thresholds, with a fallback and kill switch

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook covered AI as the builder of software but hardly at all as part of the product. Chapter 05 prototyped LLM features on Cortex, and Chapter 06 listed prompt injection as a risk to development agents. Nothing said how to test a feature whose output is not deterministic, how to keep user content and retrieved documents from steering it, how to detect it getting worse in production, or how to change the model underneath it safely. Pods building these features were falling back on trying a few prompts by hand.

The playbook's own practices already had most of the pieces: hexagonal adapters and invariants (Chapter 04), numbered acceptance criteria and mapped tests (Chapter 02, [ADR 0013](0013-non-functional-requirements-as-acceptance-criteria.md)), steering evals as a model-change gate ([ADR 0007](0007-steering-evals-gate-steering-changes.md)), feature flags, and SLOs. They had not been put together for product AI.

## Decision

We will add [Chapter 13](../../playbook/13-building-ai-features.md) and require AI features to call the model through a domain adapter with validated structured output, to be gated by a versioned eval set whose thresholds are acceptance criteria, to have a non-AI fallback behind a kill-switch flag, and to be graded in production as an SLO.

Prompts and pinned model versions are code, changed by PR with an eval run. User content and retrieved documents are data; retrieval is authorized before the model sees it; tools run with the calling user's permissions; output is escaped and validated. Model upgrades are Units of Work.

The new chapter is appended as Chapter 13 rather than inserted among the engineering chapters, so that no existing chapter is renumbered and no link breaks.

## Options considered

### Option A — Evals as the test suite, adapter, fallback, online grading  ← chosen

- Pros: reuses the playbook's own mechanisms (ACs, gates, flags, SLOs, the lesson loop); makes quality measurable before and after release; contains injection and model churn at the adapter.
- Cons: building and maintaining eval sets and graders is real work; model graders need their own calibration; online grading adds cost.

### Option B — Treat AI features as ordinary code with ordinary tests

- Pros: no new practice; unit tests with mocked model responses are familiar.
- Cons: mocked responses test the parser, not the feature; model changes and input drift go undetected.
- Rejected because: the defects that matter are in the model's behaviour on real inputs, which mocks remove.

### Option C — Rely on the vendor's safety and quality features

- Pros: little effort; vendors invest heavily in both.
- Cons: the vendor does not know our correctness criteria, our tenants, or our authorization model.
- Rejected because: the vendor can make the model safer in general, but only we can define what correct means for our feature.

## Consequences

- Positive: AI features ship with evidence that they work, and regressions surface in the PR or the pass-rate SLO instead of in complaints; model upgrades become routine.
- Negative: slower first release of each feature; eval infrastructure and grader calibration become platform-pod work; product owners and QA must learn to write eval cases.
- Follow-ups: an eval-runner step in the reference pipeline; an `eval-set` skill that drafts cases from a Unit's ACs; a place for eval results in the PR template.

## Revisit when

A standard evaluation tool becomes part of the paved road and changes the mechanics, or pass-rate SLOs prove too noisy to alert on for a quarter.
