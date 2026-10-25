---
owner: platform-enablement
audience: developers
reviewed: 2026-09-29
review-cadence: quarterly
---

# CLAUDE.md Template

Starter steering file for new repos. Audience: developers setting up or maintaining a repo's steering file. Copy the block below to the repo root as `CLAUDE.md`, replace the angle-bracket placeholders, delete what doesn't apply. Keep it **under ~150 lines, constraints over descriptions, link out for depth** — rationale in [Chapter 03](../playbook/03-tooling-strategy.md#steering-files-claudemd).

Ownership: the pod's domain anchor. Update cadence: every Friday consolidation — if the agent made the same mistake twice this week, a steering line is missing.

---

```markdown
# <service-name>

<One sentence: what this service does and which bounded context it implements.>
Part of the <context> bounded context — read docs/domain/<context>/model.md
before changing domain logic. Glossary: docs/domain/<context>/language.md.

## Commands

- Build: `<command>`
- Test: `<command>`          # run before every commit
- Single test: `<command>`
- Lint/format: `<command>`   # hooks run this on edit; fix rather than suppress
- Local run: `<command>`

## Architecture

- <Stack: language, framework, runtime — one line.>
- Layering: domain core has no framework/persistence imports; all persistence
  via repositories in `<path>`; HTTP/handlers in `<path>` stay thin.
  Architecture tests enforce this — don't fight them, fix the design.
- Events: schemas live in <registry/repo>. Generate producers/consumers from
  the schema; never freehand an event shape. Consumers are idempotent and
  must ignore unknown fields.
- Decisions of record: docs/adr/ — read before proposing designs; don't
  relitigate accepted ADRs, supersede them.

## Working agreements

- Plan mode for any Unit of Work; direct edits only for trivial bounded fixes.
  Plans follow the Bolt plan template and are committed at docs/bolts/<bolt-id>.md;
  honour the plan's stop conditions — halt and ask, never drift.
- Small slices: keep diffs reviewable; if a change grows past ~500 lines,
  stop and split.
- Tests come first: write them from the Unit of Work's acceptance criteria,
  confirm they fail, commit them, then implement. Never edit a committed test
  or add a skip/xfail marker; if one must change, halt and ask. A test that
  merely asserts current behavior is not done — state what failure it catches.
  Checklist: standards/test-review-checklist.md.
- After two failed corrections on the same problem, stop and say so; the
  Driver restarts the session with what was learned.
- When compacting, keep the Bolt id, the list of modified files, and the test
  commands.
- Update docs in the same PR as the change (docs/, ADRs, event catalog).
- PR title and branch start with the Jira key (PROJ-###).

## Security (non-negotiable)

- All SQL through <query builder/ORM>; never string-concatenate queries.
- AuthZ via <pattern/module>; never inline permission checks.
- Secrets only via <secrets manager>; never in code, config files, or output.
- Validate input at trust boundaries: <where>.
- Never edit without explicit approval: migrations/, .github/workflows/,
  <auth config path>.
- Do not add dependencies outside the private registry allowlist.

## Known sharp edges

- <The 2–4 things that repeatedly burn people/agents in this repo, with the
  why: "X must be called before Y because Z".>
```

---

## Writing good steering lines

| Weak | Strong |
|---|---|
| "Follow security best practices" | "All SQL through the query builder; never string-concatenate" |
| "The ledger is important" | "Never write to `ledger_entries` directly; go through `LedgerService` — it enforces double-entry invariants" |
| "Write good tests" | "Every AC in the Unit of Work gets a test naming it; contract tests regenerate from schemas, don't hand-edit them" |

A steering line earns its place when it (a) prevents a repeated mistake, (b) states a constraint with its *why*, or (c) saves the agent a discovery cost every session (commands, paths). Everything else is bloat that dilutes the lines that matter.
