---
name: lesson-to-steering
description: Turn a lesson (a post-mortem, a production security finding, a pod journal entry, a repeated agent mistake) into the steering change that makes that class of problem impossible, as a draft PR against the steering repo. Use at Friday consolidation, at the end of every post-mortem, and whenever an agent has made the same mistake twice. Not for one-off bugs with no repeatable class.
---

# Lesson to steering

The compounding loop Chapters 06 and 07 say most programs skip: every lesson becomes a steering line, a Semgrep rule, a test template, a hook, or a skill, the same week. This skill classifies the lesson, picks the cheapest control that prevents the class, and drafts the change.

## Inputs

- The lesson, in any of its forms: a post-mortem document, a security finding with its triage note, a pod journal entry, or a short description of a mistake plus the diff where it happened.
- The current `CLAUDE.md` of the affected repo, and the org baseline in the steering repo.
- The skills directory and the Semgrep rules repo, to check what already exists.
- The [context-engineering hierarchy](../../../playbook/03-tooling-strategy.md#the-context-engineering-hierarchy) and the [CLAUDE.md template's](../../claude-md-template.md) guidance on strong steering lines.

## Outputs

- A draft PR (branch, diff, description) against the steering repo or the affected repo, containing exactly one of:
  - a steering line in `CLAUDE.md`, with its why
  - a Semgrep rule with a test case that reproduces the original finding
  - a test template or fixture added to the relevant skill
  - a hook that blocks the action mechanically
  - a new or amended skill
- A one-paragraph note: the class of problem, the control chosen, why the cheaper options were rejected, and how to tell in a quarter whether it worked.

## Steps

1. Name the class, not the instance. "The agent called `payment.can_retry()`, which does not exist" is an instance; "the agent infers aggregate methods from names instead of reading the aggregate" is the class. If no class exists, stop: this is a bug fix, not a lesson.
2. Check whether a control already exists for the class. Search `CLAUDE.md`, the rules repo, and the skills. If one exists and failed, the fix is to strengthen it, not add a second.
3. Choose the control by walking the hierarchy, cheapest first, and picking the first that actually prevents the class:
   - **Steering line** when the agent lacked a rule and would follow one ("before calling a method on an aggregate, read the aggregate").
   - **Semgrep rule** when the mistake is a code pattern that can be matched mechanically and must block at PR time.
   - **Test template** when the class is a missing test (concurrent duplicates, negative paths) that a skill should generate every time.
   - **Hook** when the class is an action that must never happen regardless of instructions (editing migrations without a flag).
   - **Skill change** when a procedure exists and has a gap in its steps.
   Prefer the control that acts earliest: a steering line prevents generation of the problem; a rule catches it after; a hook blocks a consequence.
4. Draft the change. A steering line follows the template's strong form: constraint, then why. A Semgrep rule ships with a test file containing the original bad code and a good variant. A hook is scoped to the narrowest path that covers the class.
5. Write the PR description: class, instance that triggered it, control chosen, rejected alternatives, and the metric that shows it worked (zero new findings of the class for a quarter; the mistake absent from pod journals).
6. Stop. **Do not merge.** The steering repo's owner reviews; a steering regression is a production regression waiting to happen.

## Rules

- One lesson, one control, one PR. A PR with four steering lines will get three of them rubber-stamped.
- Never add a steering line that restates a rule already present. Stale or duplicated steering is worse than none.
- Steering lines carry their why. Bare rules get misapplied at the edges.
- Semgrep rules must have a failing test before the rule and a passing one after; a rule that matches nothing is noise with a name.
- Do not weaken an existing control to make the new one fit.
- Keep `CLAUDE.md` under ~150 lines. If the line does not fit, the file needs pruning first, and that is a separate PR for the domain anchor.

## Verification

Before handing over:

- [ ] The class is stated in one sentence and is not an instance
- [ ] Existing controls for the class were searched and cited
- [ ] Exactly one control is proposed, with the cheaper options rejected in writing
- [ ] The change is in the strong form (constraint + why, or rule + test, or hook + narrow path)
- [ ] The PR names the metric that will show it worked
- [ ] Nothing was merged

The draft is a proposal until the steering repo's owner approves it.
