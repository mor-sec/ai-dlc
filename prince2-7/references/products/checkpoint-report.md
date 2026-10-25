# Checkpoint report

**Purpose:** reports the status of a work package from the team manager to the PM, at the frequency agreed in the work package. It is time-driven.

| | |
|---|---|
| **Created in** | Managing product delivery (MP) |
| **Prepared by** | Team manager (or an agent on its behalf) |
| **Received by** | Project manager (feeds CS: review work package status) |
| **Derived from** | Work package, team plan, quality register, previous checkpoint |

## Composition
1. Date, period covered and work package ID
2. Follow-ups from the previous report
3. Products completed this period, and products in development
4. Products planned for next period
5. Quality management activities this period (with references to quality register rows)
6. **Tolerance status**: for each work package tolerance, the forecast against the limit
7. Issues and risks: new, changed, and any raised to the PM
8. Lessons identified

## Quality criteria
- It is prepared at the agreed frequency.
- Facts are traceable to products and quality records, not just activity descriptions.
- Tolerance status uses forecasts, not only actuals to date.
- Anything forecast to breach is flagged, and an issue has already been raised.

## Agent run summary form
An agent should end each work package run (or interval) with this. It doubles as a PR description.

```
WP: WP-2-03 | Period: 2026-10-25 09:00–11:30 | Status: in progress / complete / stopped (tolerance)
Done: PD-012 v0.3 – billing adapter (tests 48/48 pass; eval billing-v2 0.94 ≥ 0.92)  [Q-031]
In progress: PD-013 – reconciliation job (60%)
Next: finish PD-013; request team manager design review
Tolerances: time 3.5h/6h (+2) ✓ | cost $22/$40 (+10) ✓ | scope must-haves on track ✓
Issues/risks: I-014 raised – upstream API rate limits (problem, PM decision needed)
Lessons: test fixtures for currency rounding saved ~1h; propose adding to CLAUDE.md
Evidence: <CI run link>, <PR link>
```
