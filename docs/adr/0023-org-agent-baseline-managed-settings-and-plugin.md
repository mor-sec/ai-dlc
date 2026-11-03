# 0023 — Deliver the agent guardrails as managed settings and the shared assets as an org plugin

- **Status:** Accepted
- **Date:** 2026-09-29
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

[Chapter 06](../../playbook/06-security-shift-left.md#securing-the-agents-themselves) requires default-deny agent permissions, human approval for protected paths, and hooks that enforce both. [Chapter 03](../../playbook/03-tooling-strategy.md#hooks-and-permissions) says the same. Neither says where those settings live, so in practice they live in each repo's `.claude/settings.json`, where any repo can omit them, loosen them, or fall behind. The shared skill library had the same problem: each consuming repo copied or symlinked the skill folders it needed, so a fix to a skill reached a repo only when someone copied it again.

Claude Code now supports three mechanisms that close these gaps. Managed settings are applied above every other level, so no user, project, or command-line setting overrides them. An OS-level sandbox isolates shell commands' filesystem and network access, so routine commands can run without prompts and without widening permissions. A private plugin marketplace distributes skills, hooks, and subagents as one versioned unit that managed settings can require on every machine.

Interactive sessions also gained auto mode, in which a classifier model approves routine actions instead of a person. The playbook needs a position on it, because "per-invocation approval" in Chapter 06 was written for a person answering every prompt.

## Decision

We will deliver the organization's agent guardrails as managed settings owned by the platform pod and approved by security engineering, and deliver the reference skills, baseline hooks, and shared subagents as one plugin (`aidlc-baseline`) from the organization's marketplace.

- Managed settings hold the deny and ask rules, disable bypass mode, turn the sandbox on, allow plugins only from the official and org marketplaces, and enable the org plugin.
- Repos keep their own allow rules and hooks; the baseline does not set the keys that would forbid them.
- Auto mode is allowed at autonomy level 0, because deny rules block in every mode and ask rules and hooks still prompt in it. Deny rules, ask rules, and hooks are the controls of record; the classifier is defence in depth.
- Headless runs (levels 1 and 2) run sandboxed with no unsandboxed fallback.

The configuration is in [standards/agent-baseline.md](../../standards/agent-baseline.md), dated and reviewed quarterly because the keys belong to the vendor.

## Options considered

### Option A — Managed settings plus an org plugin  ← chosen

- Pros: guardrails hold on every machine, whatever a repo contains; a skill or hook fix reaches every repo at the next session start; permissions are reviewable in one place, like a service account.
- Cons: the platform pod owns another deployable; a bad baseline change reaches everyone at once; machines outside management (contractors' laptops) need server-managed settings or do not get the baseline.

### Option B — Per-repo settings from a template, as today

- Pros: no central deployment; each pod controls its own setup.
- Cons: guardrails are only as good as the least careful repo; drift is invisible; skill fixes propagate by copying.
- Rejected because: a guardrail that a repo can omit is a default, not a control.

### Option C — Managed settings that also forbid repo rules and hooks

- Pros: one source of truth for every permission rule and hook; nothing a repo does can surprise security.
- Cons: every repo's test runner and linter prompt on every run until the platform pod adds them centrally; prompt fatigue teaches people to approve without reading.
- Rejected because: a prompt nobody reads is weaker than an allow rule somebody reviewed.

## Consequences

- Positive: Chapter 06's permission controls become mechanical everywhere; the sandbox cuts prompts without widening permissions; skills are versioned and updated like any other dependency.
- Negative: baseline changes need the same care as a shared library release; the managed file or server-managed policy has to reach every machine; auto mode adds classifier token cost on some plans.
- Follow-ups: the org marketplace repo and the `aidlc-baseline` plugin; a plugin seed in the headless runner image; the steering evals run against baseline changes.

## Revisit when

The vendor changes how managed settings or plugins are delivered or enforced; an incident is traced to a gap between the baseline and a repo's needs; or auto mode's classifier is shown to approve an action a deny or ask rule should have caught, which would move it from defence in depth to a risk.
