# Highlight report

**Purpose:** reports stage (and project) status from the PM to the project board at the agreed interval, so the board can manage by exception without meetings. It is time-driven.

| | |
|---|---|
| **Created in** | Controlling a stage (CS): report highlights |
| **Prepared by** | Project manager |
| **Received by** | Project board, and others in the communication management approach |
| **Derived from** | Stage plan, project log, checkpoint reports, previous highlight report |

## Composition

1. Date and period covered
2. **Status summary**: one or two sentences, with an overall RAG rating and its definition
3. Work packages: authorised, in progress, completed
4. Products completed this period, and products planned for next period
5. Corrective actions taken this period
6. **Tolerance status**: project and stage forecast for each of the seven performance targets (from `prince2_check.py tolerance`)
7. Requests for change: raised, approved, rejected, pending
8. Key issues and risks: top items only, with owners
9. Lessons identified
10. **Decisions or support required from the board** (or "none")

## Quality criteria

- Short: one page, or one screen for small projects.
- The RAG rating follows from the tolerance status, not from optimism.
- Forecasts are given, not just actuals.
- Anything forecast outside stage tolerance is **not** in a highlight report; it needs an exception report now.
- Every risk or issue mentioned has an owner and a next action.

## Preparation steps (for Claude)

1. Run `prince2_check.py validate <project>` and fix or flag errors.
2. Run `prince2_check.py tolerance <project>`. If it exits with 2, stop and draft an **exception report** instead.
3. Run `prince2_check.py summary <project>` for counts and top risks.
4. Read the checkpoint reports and agent run summaries for the period.
5. Draft to the composition above, then put the board's decisions at the top if any are needed.
