# 0025 — Protect the skills the gates depend on: learning modes, conceptual questions, and hand-driven slices

- **Status:** Proposed
- **Date:** 2026-09-29
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

Every gate in AI-DLC is a person judging agent output ([Chapter 01](../../playbook/01-ai-dlc-methodology.md#the-validation-gates)), and [Chapter 02](../../playbook/02-ways-of-working.md#review-culture-the-biggest-change) makes review the primary engineering act. That only works while the people reviewing can do the work they review. The playbook acknowledged deskilling as a developer objection ([Chapter 12](../../playbook/12-adoption-strategy.md#the-stakeholder-map)) but had no answer beyond the "explain it back" tip.

Anthropic published a randomized trial of developers learning a new library. Those who used an AI assistant scored 50% on a follow-up quiz against 67% for those who coded by hand, with the largest gap on debugging, and they were not significantly faster. How the assistant was used mattered: participants who asked for explanations or asked conceptual questions kept their understanding, and those who delegated the code did worst. The recommendation is to design deliberately for engineers to keep learning as they work, including through learning modes. Claude Code ships two: an Explanatory output style and a Learning style that leaves design decisions for the developer to write.

Debugging is exactly the skill the gates need most. A Navigator who cannot debug cannot tell a plausible diff from a correct one.

## Decision

We will build skill retention into the enablement program. Developers new to a codebase use the Explanatory style for their first weeks. Developers in the first two stages of the learning path use the Learning style in practice sessions, and pods ask for the concept before delegating unfamiliar code. Every developer drives one slice by hand per fortnight in Friday learning time, where they write the code and the agent only explains and reviews. Until their first solo Bolt, a developer gives the explain-it-back on every merge they Navigate.

None of this is measured per person, consistent with the [metrics reference](../../standards/metrics-reference.md#what-is-not-measured). Detail: [Chapter 11, Keeping skills while the agent codes](../../playbook/11-learning-paths.md#keeping-skills-while-the-agent-codes).

## Options considered

### Option A — Learning modes, conceptual questions, and hand-driven slices  ← chosen

- Pros: acts on the specific interaction patterns the evidence says preserve understanding; small, scheduled, and inside time the method already reserves (Friday learning time); protects the skill the gates need most.
- Cons: hand-driven slices are slower than delegated ones; the Learning style lengthens sessions; the benefit is slow to show and hard to measure without measuring individuals.

### Option B — Rely on review and rotation to keep skills sharp

- Pros: no new practice; review and Driver rotation already expose people to code.
- Cons: reading code is not writing or debugging it; the trial found comprehension fell even among people who read the generated code.
- Rejected because: review is the thing being protected, so it cannot also be the protection.

### Option C — Periodic no-agent weeks

- Pros: unambiguous; everyone practises the full craft.
- Cons: a week of hand coding costs a week of throughput and is resented; it treats the agent as the problem rather than the way it is used.
- Rejected because: the evidence points at how the agent is used, not whether it is used, and a fortnightly slice keeps practice regular at a fraction of the cost.

## Consequences

- Positive: an answer to the deskilling objection that rests on evidence; newer developers build the debugging skill they will need as Navigators; the practice is visible in the consolidation record.
- Negative: some Friday learning time goes to hand-driven slices; Learning-style sessions cost more output tokens.
- Follow-ups: add the hand-driven slice to the consolidation template's learning notes; watch the pod-level review-depth metric for newer Navigators.

## Revisit when

Further research on AI assistance and skill formation changes the picture; or pods report that hand-driven slices displace the rest of Friday learning time without a visible gain in review depth.
