# Session log — 2026-09-29: bringing Anthropic's published practice into the playbook

A record of one working session between a playbook maintainer (Stephen Morleys) and Claude Code (Opus 5.5), for reviewers of the resulting PR and for anyone later asking why ADRs 0019 to 0025 exist. It records what was asked, what was decided, and what changed. It is not a source of truth: where it disagrees with a chapter, standard, or ADR, those win.

## Summary

The maintainer asked how the playbook could be improved and which aspects of Anthropic's practice for AI-assisted software development it should include. Anthropic has not published a named "AI SDLC"; the playbook itself is based on AWS's AI-DLC. The analysis instead mapped Anthropic's engineering guides, research, and Claude Code documentation onto the chapters, and produced seven recommendations. All seven were implemented in the same session, each with an ADR.

Outcome: seven ADRs (0019 to 0025), one new standard ([Agent Baseline](../../standards/agent-baseline.md)), and changes to 21 existing files. All four CI checks pass. Everything is uncommitted on the `playbook-gaps` branch, and every new ADR has status **Proposed**, because an agent is never a decider ([ADR template](../../standards/adr-template.md)).

## How the session ran

1. **The question.** Claude read the README, START-HERE, the headings of every chapter and standard, Chapters 02, 03, and 13 in full, and the security, operations, and Jira sections. It then checked Anthropic's published sources. It answered in the terminal with the gap analysis below.
2. **"Start with items 1 and 4, including ADRs."** Plan mode (this repo's `CLAUDE.md` requires it for changes to more than one file), plan approved, implementation, CI checks.
3. **"Now complete items 2, 3, 5, 6 and 7."** Before planning, Claude checked the Claude Code docs for exact setting keys (sandboxing, managed settings, plugin marketplaces, permission modes, hooks, output styles) and the skill-formation study. Then plan mode, plan approved, implementation, CI checks.
4. **"Capture this session and all the changes in a log."** The maintainer chose a repo file over a Claude Doc or a local file. This document.

## The gap analysis

The seven recommendations drawn from Anthropic's practice, in the priority order given, all implemented:

| # | Recommendation | Where it landed | ADR |
|---|---|---|---|
| 1 | Parallel agent sessions within one approved plan, instead of a strict single session per pod | [Chapter 02, Fan-out inside a Bolt](../../playbook/02-ways-of-working.md#fan-out-inside-a-bolt) | [0019](../adr/0019-fan-out-within-one-approved-bolt-plan.md) |
| 2 | Manage a session's live context; restart before escalating the model | [Chapter 03, Session hygiene](../../playbook/03-tooling-strategy.md#session-hygiene) | [0021](../adr/0021-restart-before-escalating-session-hygiene.md) |
| 3 | Tests written first; a mechanical check against agents editing tests | [Chapter 02, Testing under AI-DLC](../../playbook/02-ways-of-working.md#testing-under-ai-dlc), [test review checklist](../../standards/test-review-checklist.md) | [0022](../adr/0022-tests-first-with-a-test-integrity-check.md) |
| 4 | Steering evals run several trials and gate on all passing | [Steering evals](../../standards/steering-evals.md#trials-and-pass-criteria) | [0020](../adr/0020-steering-evals-run-multiple-trials.md) |
| 5 | Org-wide guardrails via managed settings and a sandbox; skills shipped as a plugin | [Agent baseline](../../standards/agent-baseline.md) | [0023](../adr/0023-org-agent-baseline-managed-settings-and-plugin.md) |
| 6 | Simplest AI-feature pattern first; tools designed for the model | [Chapter 13](../../playbook/13-building-ai-features.md#choose-the-simplest-pattern-that-works) | [0024](../adr/0024-simplest-pattern-first-and-tools-designed-for-the-model.md) |
| 7 | Protect the skills the gates depend on | [Chapter 11, Keeping skills while the agent codes](../../playbook/11-learning-paths.md#keeping-skills-while-the-agent-codes) | [0025](../adr/0025-keep-skills-while-agents-code.md) |

Four further improvements were suggested and **not** implemented; they are listed under [Open items](#open-items).

## Decisions

| ADR | Decision | Status |
|---|---|---|
| [0019](../adr/0019-fan-out-within-one-approved-bolt-plan.md) | Up to three lanes (parallel agent sessions in separate git worktrees) inside one approved Bolt plan. Shared contracts are built first as lane 0. A lane with an unreviewed slice stops, and all lanes share one review cap. The Bolt ends in one PR after integration review. No fan-out on critical changes. Still one Unit of Work per pod. | Proposed |
| [0020](../adr/0020-steering-evals-run-multiple-trials.md) | Each golden task runs *k* cold trials (3 on steering PRs, 5 on model changes and quarterly). Regression tasks gate on all *k* passing; capability tasks only report and graduate. A new line must beat a baseline run without it. Failed trials are triaged from transcripts. | Proposed; amends [0007](../adr/0007-steering-evals-gate-steering-changes.md) |
| [0021](../adr/0021-restart-before-escalating-session-hygiene.md) | Fresh session per task, exploration in subagents, a commit per reviewed slice. After two failed corrections, restart with what was learned, then escalate the model tier, then the pod. A Progress section in the Bolt plan. | Proposed |
| [0022](../adr/0022-tests-first-with-a-test-integrity-check.md) | Tests written from the ACs before the code and confirmed failing for the right reason, then committed as the red commit. A CI test-integrity check fails edits to existing tests or new skip markers without a `test-change-approved` label. An in-session hook as the early warning. | Proposed |
| [0023](../adr/0023-org-agent-baseline-managed-settings-and-plugin.md) | Guardrails delivered as managed settings no repo or user can loosen. Sandbox on, with no unsandboxed fallback for headless runs. Reference skills and hooks shipped as the `aidlc-baseline` plugin. Auto mode allowed at level 0 because deny rules, ask rules, and hooks still hold in it. | Proposed |
| [0024](../adr/0024-simplest-pattern-first-and-tools-designed-for-the-model.md) | AI features start at one call, then a fixed workflow; an agent loop only on eval evidence, recorded in the Unit of Work. Tools, including the org's MCP servers, designed for the model and evaluated. | Proposed; extends [0018](../adr/0018-ai-features-evals-adapter-kill-switch.md) |
| [0025](../adr/0025-keep-skills-while-agents-code.md) | Explanatory and Learning output styles for newcomers; concept before code; one hand-driven slice per developer per fortnight; explain-it-back until the first solo Bolt. Nothing measured per person. | Proposed |

## Changes by file

New files:

| File | What it is |
|---|---|
| `docs/adr/0019` to `0025` | The seven ADRs above |
| [`standards/agent-baseline.md`](../../standards/agent-baseline.md) | The layers (managed settings, org plugin, repo, user); a managed-settings example; the auto-mode position; sandbox settings by autonomy level; the org plugin layout; the test-integrity hook and its `hooks.json`; how the baseline changes. Dated, reviewed quarterly. |
| `docs/sessions/2026-09-29-anthropic-practices.md` | This log |

Modified files, with the items that drove each change:

| File | Items | Change |
|---|---|---|
| `playbook/01-ai-dlc-methodology.md` | 1, 3 | "One Unit at a time" tip points to fan-out; the Construction discipline now says tests are written first |
| `playbook/02-ways-of-working.md` | 1, 3 | New section "Fan-out inside a Bolt"; Bolt-day step 2 mentions lanes and failing tests first; "Tests come first" paragraph and a third mechanical check (test integrity); "silent pod" anti-pattern rewritten; new anti-pattern "Fan-out to beat the review cap"; ADRs 0019 and 0022 in References |
| `playbook/03-tooling-strategy.md` | 1, 2, 4, 5, 6 | New "Parallel sessions" H3; new "Session hygiene" H2; escalation rule 2 now restart-first; the "test it like code" line mentions trials; Skills section ships the library as a plugin; hooks and permissions bullets link the agent baseline; autonomy "Sandbox" control links the baseline; MCP servers follow Chapter 13's tool rules; ADRs 0019, 0020, 0021, 0023 in References |
| `playbook/06-security-shift-left.md` | 5 | Least-privilege item says the controls are managed settings that hold in every permission mode |
| `playbook/07-devops-automation.md` | 3 | Test integrity added to the pipeline diagram's static stage and as a stage note; ADR 0022 in References |
| `playbook/11-learning-paths.md` | 7 | New section "Keeping skills while the agent codes"; developer path stages 1 and 2 updated; anti-pattern "Onboarding by delegation"; ADR 0025 and the Anthropic study in References |
| `playbook/12-adoption-strategy.md` | 7 | New hard objection: "Will we forget how to code?" |
| `playbook/13-building-ai-features.md` | 6 | New sections "Choose the simplest pattern that works" and "Design tools for the model"; Inception row records the pattern; anti-pattern "The agent that should have been a workflow"; ADR 0024 and two Anthropic articles in References |
| `playbook/appendix-c-a-bolt-that-fails.md` | 3 | Link fix only: anchor renamed to `#the-mechanical-checks` |
| `standards/bolt-plan-template.md` | 1, 2 | Optional Fan-out section with a lane table; Progress section; stop condition for lanes; restart-first stop condition; plan-checklist item for lanes |
| `standards/claude-md-template.md` | 2, 3 | Working agreements: tests first and never edit committed tests; stop after two failed corrections; what survives compaction |
| `standards/model-selection.md` | 2 | Escalation row and standing rule 2 restart-first; change-log entry |
| `standards/skill-template.md` | 5 | Shared skills distributed by the baseline plugin, not copied |
| `standards/skills/README.md` | 3, 5 | `tests-from-acs` description; distribution through the plugin |
| `standards/skills/tests-from-acs/SKILL.md` | 3 | Rewritten into phase 1 (red, before implementation) and phase 2 (mutation, after); new rules on skip markers and separate sessions for material changes |
| `standards/steering-evals.md` | 3, 4 | `kind` front-matter; trials per occasion; new sections "Trials and pass criteria" and "Regression and capability tasks"; model-change procedure at five trials; new golden task `tests-fail-before-code` (nine starter tasks) |
| `standards/test-review-checklist.md` | 3 | "Tests came first" item; skip-marker clause; third mechanical check (test integrity); section renamed "The mechanical checks" |
| `docs/adr/0007-steering-evals-gate-steering-changes.md` | 4 | Status line only: "pass criterion amended by 0020" |
| `GLOSSARY.md` | all | New entries: Agent baseline, Agent loop, Fan-out, Hand-driven slice, Lane, Red commit, Session hygiene, Steering eval, Trial; Mob Construction entry updated |
| `README.md` | 4, 5 | Steering Evals row mentions trials; new Agent Baseline row |
| `START-HERE.md` | 1, 3, 5 | Loop step 3 mentions fan-out; the tests rule is now tests-first; "Setting up a repo" links the agent baseline |
| `docs/README.md` | log | New `sessions/` row |

Every substantively edited chapter and standard had its `reviewed` date bumped to 2026-09-29.

## Judgement calls made during implementation

- **ADRs are Proposed, not Accepted.** The maintainer accepts them by merging.
- **The steering-eval `kind` lives in `expected.md` front-matter,** not in `evals/regression/` and `evals/capability/` directories. Graduating a task is then a one-line diff, and the `evals/` namespace, already shared with Chapter 13's product evals, gets no deeper.
- **CI is the control of record for test integrity; the hook is the early warning.** A hook on file-editing tools cannot see changes made through shell commands.
- **Auto mode is allowed at level 0.** The Claude Code docs state that deny rules block in every mode and that ask rules and hook decisions still prompt in auto mode, so the playbook's controls do not depend on the classifier. Organizations that have not cleared auto mode through vendor governance can disable it.
- **`allowManagedPermissionRulesOnly` and `allowManagedHooksOnly` are deliberately left off.** Either would stop repos pre-approving their own test runners, and unanswerable prompt volume trains people to click through prompts.
- **Bolt progress lives in the Bolt plan** (a Progress section), not a separate progress file, so there is one artifact per Bolt.
- **Setting keys and JSON live only in the dated standard,** per the repo rule that vendor facts stay out of chapters.
- **The appendices were not rewritten.** Appendix A and Appendix C describe Bolts run before tests-first and fan-out existed; Appendix C's story (ad hoc tests, a refused `xfail`) is the motivating case for ADR 0022.
- **Wording corrected before the log:** ADR 0020's probability sentences were rewritten after a first draft garbled them.

## Verification

- `npx -y markdownlint-cli2 "**/*.md"`, `python3 scripts/check-links.py`, `scripts/check-mermaid.sh`, and `python3 scripts/check-structure.py` all pass: 0 lint errors, 0 broken links or anchors, 7 Mermaid diagrams, 0 structure violations. ADR numbering runs 0001 to 0025 with no gaps.
- The test-integrity hook was run against a scratch git repo on six cases, all as expected:

  | Case | Expected exit |
  |---|---|
  | Edit to a committed test | 2 (blocked) |
  | Write of a new test file | 0 |
  | New test with `xfail` | 2 |
  | JavaScript `it.skip` | 2 |
  | Skip marker in a non-test path | 0 |
  | Edit adding `@Disabled` | 2 |

  The copy in the standard was diffed against the tested script.
- The three JSON blocks in the agent baseline parse.
- Every setting key in the agent baseline was checked against the Claude Code documentation on 2026-09-29.

## Sources

Anthropic engineering and research:

- [Best practices for Claude Code](https://code.claude.com/docs/en/best-practices): context-window constraint, verification loops, restart after two corrections, parallel sessions and worktrees, writer and reviewer sessions
- [How Claude Code is used in practice](https://www.anthropic.com/research/claude-code-expertise): people make about 70% of planning decisions and 20% of execution decisions
- [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): trials, pass^k, capability versus regression evals, reading transcripts
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents): workflows versus agents, simplest solution first
- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents): tool design and evaluation
- [How AI assistance impacts the formation of coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills): quiz scores of 50% versus 67%, the largest gap on debugging, learning-preserving interaction patterns
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): background for session hygiene

Claude Code documentation: [sandboxing](https://code.claude.com/docs/en/sandboxing), [settings](https://code.claude.com/docs/en/settings), [managed settings](https://code.claude.com/docs/en/managed-settings), [plugins for organizations](https://code.claude.com/docs/en/plugins/org), [plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), [permission modes](https://code.claude.com/docs/en/permission-modes), [hooks](https://code.claude.com/docs/en/hooks), [output styles](https://code.claude.com/docs/en/output-styles).

## Open items

Before merge:

- Flip ADRs 0019 to 0025 from Proposed to Accepted.
- Decide the commit split. One commit per ADR is impractical, because Chapters 02 and 03, the glossary, and START-HERE mix changes from several ADRs. Options: a single commit, or two (items 1 and 4, then the rest).

Follow-ups the ADRs create:

- `evals/check.py` support for trials and passes/*k* reporting, and `kind` front-matter on the starter tasks' `expected.md` files (ADR 0020).
- The CI test-integrity script and its per-language marker patterns (ADR 0022).
- The org marketplace repo, the `aidlc-baseline` plugin, and a plugin seed in the headless runner image (ADR 0023).
- A review of existing MCP servers against the tool-design rules (ADR 0024).
- A hand-driven-slice note in the [consolidation template](../../standards/consolidation-template.md) (ADR 0025).

The four further improvements from the gap analysis, not done:

- [`standards/model-selection.md`](../../standards/model-selection.md) still names Opus 5 and Sonnet 5 as current, but Opus 5.5 and Sonnet 5.5 have shipped. The refresh needs its own steering-eval run.
- The other three:
  - runnable golden-task fixtures for the reference skills in this repo, which the playbook prescribes but does not ship;
  - an Appendix D walking an autonomy level 1 or 2 run end to end;
  - Claude Code's OpenTelemetry data as the source for the token and cost rows in the [metrics reference](../../standards/metrics-reference.md).
