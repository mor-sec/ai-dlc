---
name: prince2-7
description: Run and document projects using PRINCE2 7th edition (2023), including governing AI-driven delivery such as coding agents or AWS AI-DLC. Use when asked to draft or review a PRINCE2 management product (project brief, business case, PID, management approaches, stage/project/exception plans, work packages, product descriptions, highlight/checkpoint/exception/end stage/end project/lessons/issue reports), maintain the project log (risk, issue, quality, product registers, daily and lessons logs), check tolerances or decide whether something is an exception, tailor PRINCE2 for a project, or govern AI-assisted or AI-product delivery with PRINCE2 controls.
---

# PRINCE2 7 project management

Work to **PRINCE2 7th edition (2023)** terminology. Never fall back to 6th edition (2017) terms. The common slips:

| Say (v7) | Not (v6) |
|---|---|
| practices | themes |
| five integrated elements (incl. **people**) | four elements |
| **seven** performance targets incl. **sustainability** | six tolerance areas |
| project log (holds six records) | separate logs/registers |
| issue management approach | change control approach |
| change management approach = how people **adopt** outputs | (no v6 equivalent) |
| product register | configuration item records / product status account |

If the user explicitly works to 6th edition, say so once and translate.

## Routing

Identify what the user wants, then read only the files you need.

| Request | Read |
|---|---|
| Explain or apply principles, practices, processes, roles, "who decides?" | `references/method-core.md` |
| "Is this an exception?", tolerance checks, escalation | `references/method-core.md` § Tolerances, then run `scripts/prince2_check.py tolerance` |
| Tailor PRINCE2 (small project, agile, inside a programme, supplier-side) | `references/tailoring.md` |
| AI-assisted delivery, coding agents, AWS AI-DLC (intents, units of work, bolts, Mob Elaboration), building an AI/ML product, governing agents | `references/ai-sdlc.md` |
| Explain how PRINCE2 and AI-DLC fit together, for a board or team | `assets/prince2-governs-aidlc-delivers.svg` (one-page infographic; PNG alongside) plus `references/ai-sdlc.md` |
| Draft or review a specific management product | `references/products/<product>.md` (index below) |
| Create or check registers / project log | `references/products/project-log.md`, then `scripts/prince2_check.py` |

### Management product index (`references/products/`)

Baselines:
- `project-brief.md` (output of Starting up)
- `business-case.md` (outline in brief, full in PID, updated at every stage boundary)
- `pid.md` (project initiation documentation: the project baseline)
- `management-approaches.md` (all nine approaches)
- `plan.md` (project, stage, exception and team plans)
- `product-description.md` (includes the project product description)
- `work-package.md`

Records: `project-log.md` (daily log, lessons log, issue, risk, quality and product registers)

Reports:
- `checkpoint-report.md` (team manager → project manager, time-driven)
- `highlight-report.md` (project manager → project board, time-driven)
- `exception-report.md` (event-driven, forecast tolerance breach)
- `end-stage-report.md`
- `end-project-report.md`
- `lessons-report.md`
- `issue-report.md`

## How to draft a management product

1. **Locate it in the method.** Which process creates or updates it, who approves it, and what it is derived from (each product file lists this).
2. **Gather inputs first.** Pull from what exists: earlier products, the project log, repo history, tickets, meeting notes. Ask only for gaps that would change the content, such as tolerances, the executive's name, or the funding source. Don't invent facts; mark unknowns as `TBC – <owner>`.
3. **Draft to the composition** in the product file, tailored to the project's scale. A small project's highlight report can be five lines. Drop or merge sections when tailoring allows, and note what you merged.
4. **Run the quality criteria** listed in the product file against your draft and fix failures before presenting it.
5. **State the decision needed.** Every report or baseline ends with what the reader must decide or approve, and by when.

## Rules that hold regardless of tailoring

- The seven principles cannot be tailored away. If a project isn't applying them, it isn't a PRINCE2 project. Say so plainly.
- Decisions belong to roles: the project board authorises, the project manager manages within stage tolerance, and the team manager delivers within work package tolerance. Draft decisions for the right role; never record a decision as made unless the user confirms it was made.
- An **issue** has happened. A **risk** might happen. An **exception** is a *forecast* breach of tolerance, escalated one level up. Keep these distinct in every product.
- Distinguish outputs, outcomes and benefits. Benefits are measurable and owned by the senior user, and they are often realised after closure.
- When AI agents do any of the work, apply `references/ai-sdlc.md`: humans hold every approval, and agent work runs inside work package tolerances.

## Script

`scripts/prince2_check.py` (Python 3.9+, standard library only). It works on a project folder of CSV registers plus `tolerances.json`:

```
python scripts/prince2_check.py init <dir>        # create blank project log CSVs + tolerances.json
python scripts/prince2_check.py validate <dir>    # schema, enum, date and hygiene checks
python scripts/prince2_check.py tolerance <dir>   # status per performance target; exit 2 on forecast breach
python scripts/prince2_check.py summary <dir>     # counts and top items to paste into a highlight report
```

Add `--json` for machine-readable output. Exit codes: 0 means OK, 1 means validation errors, 2 means a forecast tolerance breach (exception). This lets CI or an agent loop gate on it. Run `validate` before drafting any report that draws on the log, and run `tolerance` before writing a highlight or exception report.
