# docs

Orientation for this folder. Audience: anyone, human or agent, navigating the playbook repo's supporting documents. Two minutes.

| Folder | Holds | Rules |
|---|---|---|
| `adr/` | Decisions about the playbook itself: what we recommend and why we changed it | One file per decision, sequentially numbered, from the [ADR template](../standards/adr-template.md). Never edit an accepted ADR's substance; supersede it. |
| `sessions/` | Dated records of working sessions that changed the playbook: what was asked, decided, and changed, with the verification run | One file per session, named `YYYY-MM-DD-slug.md`. A record, not a source of truth: chapters, standards, and ADRs win any disagreement. Not edited after merge except for link fixes. |
| `assets/` | Binary files, only where Mermaid genuinely cannot express the diagram | Currently empty. Keep it that way unless [Chapter 09](../playbook/09-documentation-standards.md) says otherwise. |

The playbook content lives in [`../playbook/`](../playbook/); reusable templates and dated references in [`../standards/`](../standards/); the front door is the [README](../README.md).
