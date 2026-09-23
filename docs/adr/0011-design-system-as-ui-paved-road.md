# 0011 — Make the design system the paved road for agent-built UI, with accessibility as acceptance criteria and visual verification

- **Status:** Accepted
- **Date:** 2026-09-02
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; recorded retroactively on 2026-09-23 for commit d91b0d5

## Context

[Chapter 04](../../playbook/04-architecture.md) was entirely service-side, yet agents build user interfaces too, and UI work differs in three ways. Consistency matters more than invariants. Review of generated markup does not work, because nobody can tell from 400 lines of JSX whether a screen looks right. And an unconstrained agent asked for a screen writes its own styles and its own fetch calls, so the product ends up with three date pickers and endpoints that bypass the domain.

Accessibility has the same problem as security: left to review comments, it arrives late or not at all.

## Decision

We will treat a component library with design tokens as the paved road for UI, write accessibility as Given/When/Then acceptance criteria on every story with a UI surface, verify UI visually and behaviourally in the ephemeral environment, and keep UI state behind the bounded context's commands and events.

Agents compose library components and never add styles, colours, or spacing values; a missing component is a Unit of Work for the platform pod. Axe checks run in CI; Playwright drives the ACs; screenshot diffs flag unintended visual change. Backend-for-frontend layers stay thin and stateless. Promoting a UI prototype means rebuilding it. Detail: [Chapter 04, Frontend and UX under AI-DLC](../../playbook/04-architecture.md#frontend-and-ux-under-ai-dlc).

## Options considered

### Option A — Design system as paved road, accessibility ACs, visual verification  ← chosen

- Pros: consistency and accessibility are enforced where the agent works, not at review; reviewers judge the screen, which is what users see; the domain boundary from [ADR 0005](0005-ddd-and-event-driven-architecture.md) holds for UI too.
- Cons: requires a component library before pods build UI at speed; screenshot diffs need upkeep; the platform pod becomes a dependency for new components.

### Option B — Code review of generated UI, with style guides as documentation

- Pros: no new tooling; works with any front-end stack.
- Cons: reviewers cannot see layout, focus order, or contrast in a diff; written style guides are ignored by agents unless they are steering.
- Rejected because: the review cannot detect the defects that matter in UI.

### Option C — Leave front-end architecture out of scope for the playbook

- Pros: keeps Chapter 04 focused; front-end choices vary widely between teams.
- Cons: the most visible part of every product gets no steering at all.
- Rejected because: agents build UI whether or not the playbook covers it, and the bespoke-UI failure is the result.

## Consequences

- Positive: UI built by different pods looks and behaves the same; accessibility defects are caught as failing tests rather than audit findings.
- Negative: organizations without a design system must build one first; visual-diff noise must be managed so reviewers do not learn to ignore it.
- Follow-ups: component-library steering lines in the [CLAUDE.md template](../../standards/claude-md-template.md); axe and screenshot-diff steps in the reference pipeline.

## Revisit when

Agents can reliably verify visual output against a design reference without screenshot diffs, or pods repeatedly wait more than a Bolt for a missing component from the platform pod.
