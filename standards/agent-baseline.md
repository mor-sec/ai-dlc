---
owner: platform-enablement
audience: platform pod, security engineers, developers setting up a repo
reviewed: 2026-09-29
review-cadence: quarterly
---

# Agent Baseline

The guardrails and shared assets every Claude Code session in the organization starts with, and where each one is configured. Audience: the platform pod that ships the baseline, security engineering that approves it, and developers who need to know which settings a repo may add. The principles are in [Chapter 03](../playbook/03-tooling-strategy.md#hooks-and-permissions) and [Chapter 06](../playbook/06-security-shift-left.md#securing-the-agents-themselves); this file holds the concrete configuration.

**This file goes stale by design.** Setting keys and their behaviour are the vendor's and change between Claude Code releases. The keys below were checked against the Claude Code documentation on the `reviewed` date. When it is more than a quarter old, check the keys against the current [settings reference](https://code.claude.com/docs/en/settings) before copying them.

## The layers

A control belongs at the lowest layer that cannot be bypassed for it. Guardrails that must hold everywhere go in managed settings, because no user, project, or command-line setting overrides them. Shared assets go in the org plugin, because a plugin updates everywhere at once. What differs per repo stays in the repo.

| Layer | Configured in | Owner | Holds |
|---|---|---|---|
| **Managed settings** | `managed-settings.json` on each machine, an MDM policy, or server-managed settings from the admin console | Platform pod; security approves | Deny and ask rules, bypass mode disabled, sandbox on, the marketplace allowlist, the org plugin enabled |
| **Org plugin** (`aidlc-baseline`) | The org's private plugin marketplace, a git repo | Platform pod | The [reference skills](skills/README.md), baseline hooks, the fresh-eyes reviewer subagent |
| **Repo settings** | `.claude/settings.json`, committed | The pod that owns the repo | Allow rules for the repo's own test, lint, and build commands; repo hooks such as format-on-edit; skills only this repo uses, in `.claude/skills/` |
| **User settings** | `~/.claude/settings.json` | Each developer | Personal preferences only: theme, output style, editor. Never a guardrail |

## Managed settings

The org-wide policy. Replace `<org>` and the paths with the organization's own.

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Bash(git push --force *)",
      "Bash(git push -f *)",
      "Bash(terraform apply *)",
      "Bash(kubectl delete *)"
    ],
    "ask": [
      "Edit(./migrations/**)",
      "Edit(./.github/workflows/**)",
      "Bash(git push *)"
    ],
    "disableBypassPermissionsMode": "disable"
  },
  "sandbox": {
    "enabled": true
  },
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "anthropics/claude-plugins-official" },
    { "source": "github", "repo": "<org>/claude-marketplace" },
    { "source": "skills-dir" }
  ],
  "extraKnownMarketplaces": {
    "<org>-marketplace": {
      "source": { "source": "github", "repo": "<org>/claude-marketplace" }
    }
  },
  "enabledPlugins": {
    "aidlc-baseline@<org>-marketplace": true
  },
  "disableSideloadFlags": true
}
```

What each part does, and why:

- **`deny`** blocks in every permission mode. It covers the things no session should do: read secrets files, force-push, apply infrastructure, delete cluster resources. Command patterns are a speed bump, not a wall, because a determined command can be phrased another way. The wall is that agent sessions hold no production credentials ([Chapter 06](../playbook/06-security-shift-left.md#securing-the-agents-themselves)).
- **`ask`** forces a prompt for protected paths and pushes, even in auto mode. This is the "explicit human approval per invocation" that Chapter 06 requires for migrations and CI workflows.
- **`disableBypassPermissionsMode`** removes the mode that skips all prompts and checks. No pod needs it, and one session in it defeats every rule above.
- **`sandbox.enabled`** runs shell commands under OS-level filesystem and network isolation, so routine commands need no prompt and a mistaken one cannot reach outside the boundary.
- **The marketplace keys** allow plugins only from the official marketplace, the org's marketplace, and plain repo skills. They register the org marketplace on every machine and install the org plugin. `disableSideloadFlags` stops plugins being loaded from an arbitrary directory or URL at startup.

Left off deliberately: `allowManagedPermissionRulesOnly` and `allowManagedHooksOnly`. Setting either would stop repos adding allow rules for their own test runners and their own hooks, and every prompt a repo cannot pre-approve teaches people to click through prompts.

## Permission modes at Level 0

Interactive sessions ([autonomy level 0](../playbook/03-tooling-strategy.md#agent-autonomy-levels)) may run in Manual mode or auto mode. In auto mode a classifier model approves routine actions instead of a person. That is acceptable because the controls of record do not depend on it: deny rules block in every mode, and ask rules and hook decisions still prompt in auto mode. The classifier is defence in depth on top of them.

An organization whose [vendor governance](../playbook/03-tooling-strategy.md#vendor-governance) review has not cleared auto mode removes it with the managed setting that disables it, and pods run in Manual mode with the sandbox.

## Sandbox by autonomy level

| Level | Sandbox settings | Why |
|---|---|---|
| 0 — Interactive | `enabled: true` (the managed default above) | A command that fails in the sandbox may retry outside it, and that retry goes through the normal permission prompt, with a person there to answer |
| 1 and 2 — Headless | The workflow's settings add the block below | Nobody is there to answer a prompt, so there is no escape from the sandbox and no silent fallback when it cannot start |

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "network": {
      "allowedDomains": ["github.com", "<private-registry-host>"]
    }
  }
}
```

Headless runners also get the org plugin without cloning at run time: build a plugin seed into the runner image and point `CLAUDE_CODE_PLUGIN_SEED_DIR` at it. The other unattended-run controls (bot identity, token and time caps, input hygiene) are in [Chapter 03](../playbook/03-tooling-strategy.md#agent-autonomy-levels).

## The org plugin

One plugin, versioned in the org marketplace repo, so a fix to a skill or hook reaches every repo on the next session start instead of waiting for each repo to copy it:

```text
claude-marketplace/
├── .claude-plugin/marketplace.json
└── plugins/aidlc-baseline/
    ├── .claude-plugin/plugin.json
    ├── skills/                  # the five reference skills, one folder each
    ├── agents/
    │   └── fresh-eyes-reviewer.md
    └── hooks/
        ├── hooks.json
        └── test-integrity.sh
```

Plugin skills are namespaced by the plugin (`/aidlc-baseline:bolt-plan`). A skill only one repo will ever use stays in that repo's `.claude/skills/` ([skill template](skill-template.md)).

## Baseline hooks

Hooks enforce what steering can only request. The baseline ships one; repos add their own (format-on-edit, architecture checks) in repo settings.

**Test integrity.** Blocks the agent from editing a test that is already committed, or adding a skip or xfail marker, during a session. It is the in-session early warning for the [test-integrity check](test-review-checklist.md#the-mechanical-checks) in CI, which remains the control of record because a hook on file-editing tools cannot see changes made through shell commands.

`hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/hooks/test-integrity.sh" }
        ]
      }
    ]
  }
}
```

`hooks/test-integrity.sh` (requires `jq`; adjust the path patterns to the repo's test layout):

```bash
#!/usr/bin/env bash
# PreToolUse hook (matcher: Edit|Write). Blocks edits to committed tests and new skip markers.
# The CI test-integrity check is the control of record; this is the early warning.
set -uo pipefail
input=$(cat)
cd "$(jq -r '.cwd' <<<"$input")" || exit 0
path=$(jq -r '.tool_input.file_path // empty' <<<"$input")
case "$path" in
  */tests/*|*/test/*|*_test.*|*.test.*|*.spec.*) ;;
  *) exit 0 ;;
esac
if git ls-files --error-unmatch "$path" >/dev/null 2>&1; then
  echo "Stop condition: $path is an existing test. Do not edit it; report to the pod." >&2
  exit 2
fi
if jq -r '.tool_input.content // .tool_input.new_string // empty' <<<"$input" |
   grep -Eq 'pytest\.mark\.(skip|xfail)|@Disabled|\b(it|describe|test)\.(skip|only)\(|\bxit\('; then
  echo "Skip and xfail markers are not allowed. Report the failing test instead." >&2
  exit 2
fi
exit 0
```

Exit code 2 blocks the tool call and returns the message to the agent, which then reports the stop condition instead of working around it. New test files are allowed until they are committed, which is what lets the red phase of [`tests-from-acs`](skills/tests-from-acs/SKILL.md) iterate on them before the red commit.

## Changing the baseline

The baseline is steering, and it changes the way steering does: by PR to the marketplace repo or the managed-settings source, with the [steering evals](steering-evals.md) run against it. Adding a deny or ask rule is routine. Removing or loosening one is a material change with a named approver from security engineering, recorded in the PR.

Decision of record: [ADR 0023](../docs/adr/0023-org-agent-baseline-managed-settings-and-plugin.md).
