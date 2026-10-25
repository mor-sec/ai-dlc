---
name: factory
description: Run a feature through the software factory loop (spec, build, four parallel reviews, approver, merge or needs-human), with factory/board.json as durable state for the dashboard. Use when the user types /factory.
argument-hint: <feature> | next | approve <job-id> | rework <job-id> <note>
disable-model-invocation: true
---

# Factory orchestrator

You are the orchestrator. You run the loop below, spawn every agent, and are the **only writer of `factory/board.json`**. You never write a spec, build, review, or decision yourself; agents do, one file each.

Arguments: `$ARGUMENTS`

## Commands

| Command | Does |
|---|---|
| `/factory <feature>` | Create a job for the feature text and run the loop |
| `/factory next` | Take the first `- [ ]` line in `factory/backlog.md`, rewrite it as `- [x] <text> — job <id>`, run the loop on its text |
| `/factory approve <job-id>` | The job must be `needs-human`. Merge it (see Merge), set `stage: merged`, `note: approved by human` |
| `/factory rework <job-id> <note>` | Write the note to `factory/jobs/<id>/round-<N>/review-human.md` (first line `VERDICT: CHANGES`, then the note). Append round N's verdicts plus `"human": "CHANGES"` to `history`, then resume the builder for round N+1 as in step 7's first bullet, whatever N is |

## Conventions every agent also follows

- Job id: `NNN-slug`, where `NNN` is one more than the highest existing job number (zero-padded) and `slug` is 2–4 kebab-case words from the feature.
- Job folder `factory/jobs/<id>/`, branch `factory/<id>`, build worktree `.claude/worktrees/factory-<id>` (from `main`).
- Spawn prompts carry **identifiers only**: `Job <id>, round <N>.` Agents read everything else from files. Never paste conversation context into a prompt.
- Agent types: `factory-spec-writer`, `factory-builder`, `factory-review-security`, `factory-review-ux`, `factory-review-ui`, `factory-review-code`, `factory-approver`.

## The loop

1. **Create.** Pick the id, create the job folder, add the board entry with `title` = the feature text exactly as given (the spec-writer reads it there), `stage: spec`, `round: 0`.
2. **Spec.** Spawn `factory-spec-writer`; wait. `spec.md` must exist.
3. **Build.** Set `stage: build`, `round: 1`. Spawn `factory-builder` with the name `builder-<id>` (use the Agent tool's name field if it has one, otherwise put the name in the description), prompt `Job <id>, round 1.` Store the returned agent id in the board as `builder`. Wait.
4. **Check the build.** Read the last `## Round N` section of `build.md`. If it ends `Status: BLOCKED`, set `stage: needs-human` with the reason as `note` and stop.
5. **Review.** Set `stage: review` and all four `reviews` to `pending`. Spawn the four reviewers **in one message** (prompt `Job <id>, round <N>.`), in the background. Each time one finishes, read line 1 of its file and update that chip on the board.
6. **WAIT FOR ALL.** The round is done only when `review-security.md`, `review-ux.md`, `review-ui.md`, and `review-code.md` all exist in `round-<N>/`. Check the folder, not the notifications. If a reviewer finished without writing its file, spawn it again once; if the file is still missing, set `needs-human`. Never resume the builder mid-round.
7. **Route.** A verdict is `PASS` only if line 1 is exactly `VERDICT: PASS`. Anything else counts as `CHANGES`.
   - **Any CHANGES, round < 2:** append the round's verdicts to `history`, set `round: N+1`, `stage: build`, reviews back to `pending`. Resume the same builder with SendMessage: `Round <N+1>. Reviews are in factory/jobs/<id>/round-<N>/.` Go to step 4.
   - **Any CHANGES, round ≥ 2:** set `stage: needs-human`, `note: round <N> still has CHANGES`. Stop. A `/factory rework` earns one more round.
   - **All PASS:** set `stage: approve`. Spawn `factory-approver`; wait. Line 1 of `decision.md`: `APPROVE` → Merge, `stage: merged`. Anything else → `stage: needs-human`, `note` = the decision's first reason.

If SendMessage to `builder` fails (for example, in a later session), spawn a fresh `factory-builder` named `builder-<id>` with the same `Round <N+1>…` prompt and store its id. It catches up from files.

## Board

Rewrite the whole file on every change, and stamp `updated` (ISO 8601 UTC) each time. Shape:

```json
{ "jobs": [ {
  "id": "003-rate-limiting", "title": "Add rate limiting", "branch": "factory/003-rate-limiting",
  "stage": "review", "round": 2,
  "reviews": { "security": "CHANGES", "ux": "PASS", "ui": "pending", "code": "PASS" },
  "history": [ { "security": "CHANGES", "ux": "PASS", "ui": "PASS", "code": "CHANGES" } ],
  "builder": "<agent id>", "note": "", "updated": "2026-10-25T14:03:00Z"
} ] }
```

`stage` is one of `spec`, `build`, `review`, `approve`, `merged`, `needs-human`. `history` holds the verdicts of finished rounds, oldest first; a human rework adds `"human": "CHANGES"` to the round it was written in.

## Merge

Local only; never push. Run from the repo root:

```bash
id=003-rate-limiting
wt=$(git worktree list --porcelain | grep -B2 '^branch refs/heads/main$' | sed -n 's/^worktree //p')   # no $<digit>: the skill loader substitutes those
if [ -z "$wt" ]; then wt=.claude/worktrees/factory-merge; git worktree add "$wt" main; tmp=1; fi
test -z "$(git -C "$wt" status --porcelain -- . ':!factory')" || { echo "main worktree is dirty"; exit 1; }   # factory/ is the orchestrator's own live state
git -C "$wt" merge --no-ff -m "Merge factory/$id" "factory/$id" || { git -C "$wt" merge --abort; exit 1; }
[ -n "$tmp" ] && git worktree remove "$wt"
git worktree remove ".claude/worktrees/factory-$id"
```

If any step fails, set `stage: needs-human` with the error as `note`, and leave the branch and worktree alone.

## Dashboard

```bash
cd factory && python3 -m http.server 8000   # open http://localhost:8000/dashboard.html
```
