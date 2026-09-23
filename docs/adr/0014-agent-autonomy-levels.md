# 0014 — Declare an autonomy level for every agent run; unattended agents may author routine changes but never merge

- **Status:** Accepted
- **Date:** 2026-09-24
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; predates Jira tracking for this repo

## Context

The playbook assumed a human in every agent session, apart from one tip in [Chapter 03](../../playbook/03-tooling-strategy.md#tips--tricks): "CI agents comment, humans merge." Agents now run headless in CI, on schedules, and from issue triggers, and pods want to use them for chores such as changelog drafts, dependency migrations, and first-pass review. Nothing said what such a run may touch, which credentials it holds, or how a workflow earns more latitude.

The main safeguard against prompt injection ([Chapter 06](../../playbook/06-security-shift-left.md#securing-the-agents-themselves)) is a human gate between an agent reading something and doing something irreversible. An unattended run removes that gate unless its permissions put it back.

## Decision

We will require every agent run to declare one of three autonomy levels (0 interactive, 1 headless commenter, 2 headless author of routine-class PRs), with no level permitted to merge, and require an ADR with a quarter of evidence to move a workflow up a level.

Each unattended run gets a dedicated bot identity, a sandbox with no production credentials, a per-run token and time cap, and treats all external input as data; runs triggered by untrusted input start at level 1. Detail: [Chapter 03, Agent autonomy levels](../../playbook/03-tooling-strategy.md#agent-autonomy-levels).

## Options considered

### Option A — Three declared levels, no merge at any level  ← chosen

- Pros: unattended work is useful but always ends at a human gate; permissions are visible in the workflow file; promotion is based on evidence.
- Cons: routine agent PRs still consume review capacity; an ADR per promotion is overhead for small workflows.

### Option B — Allow auto-merge for narrowly defined classes (patch dependencies, generated docs)

- Pros: removes review load for truly mechanical changes; common practice for dependency bots.
- Cons: a compromised dependency or an injected instruction reaches `main` with no human in the loop; "narrowly defined" widens over time.
- Rejected because: the routine gate in [Chapter 07](../../playbook/07-devops-automation.md#risk-based-gating) already requires one human review, and agent-authored changes should not be the exception. This can be revisited with evidence.

### Option C — No unattended agents

- Pros: simplest; no new attack surface.
- Cons: gives up cheap automation of chores; pods will run unattended agents anyway, without controls.
- Rejected because: an ungoverned practice is worse than a governed one.

## Consequences

- Positive: security can review agent automation the way it reviews service accounts; runaway runs are capped; injection through issue text cannot reach a merge.
- Negative: review capacity is spent on agent-authored routine PRs; each workflow needs a bot identity and sandbox configuration.
- Follow-ups: a reusable workflow in the paved road that sets identity, sandbox, and caps; a label-based metric for acceptance of agent-authored PRs.

## Revisit when

Agent-authored routine PRs are accepted unchanged at a high rate for two consecutive quarters, making a narrow auto-merge class worth an ADR of its own, or an incident is traced to an unattended run.
