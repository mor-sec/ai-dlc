# Project log (PRINCE2 7)

PRINCE2 7 groups the project's records into a single **project log** containing six records:
- daily log and lessons log;
- issue, risk, quality and product registers.

Records are created in SU (daily log, lessons log) and IP (the registers), and maintained throughout by the PM or project support. Team managers update the quality register for their products.

The schemas below are what `scripts/prince2_check.py` creates (`init`) and validates (`validate`). They are CSV, so agents, spreadsheets and git diffs all work. Files live in `<project>/log/`.

Conventions:
- Dates are ISO `YYYY-MM-DD`.
- IDs are unique per register (`R-001`, `I-001`, `Q-001`, `L-001`, `D-001`; product IDs as in product descriptions, for example `PD-012`).
- Enum values are lower_snake_case.
- Multiple values are separated with `;`.

## risk_register.csv
| Column | Req | Values / notes |
|---|---|---|
| id | ✓ | R-### |
| date_raised | ✓ | date |
| raised_by | ✓ | |
| category | | e.g. strategic, commercial, technical, data_ai, people, sustainability |
| risk_type | ✓ | `threat`, `opportunity` |
| cause | ✓ | the source of the risk |
| event | ✓ | the uncertain event |
| effect | ✓ | the impact on objectives |
| probability | ✓ | 1–5 |
| impact | ✓ | 1–5 (score = P×I, computed) |
| proximity | | `imminent`, `within_stage`, `within_project`, `beyond_project` |
| response_category | | threat: `avoid`, `reduce`, `transfer`, `share`, `accept`, `prepare_contingent_plans`. Opportunity: `exploit`, `enhance`, `share`, `accept`, `prepare_contingent_plans`. |
| response | | the actions |
| risk_owner | | required when open and score ≥ the high threshold (default 15) |
| risk_action_owner | | |
| status | ✓ | `open`, `closed`, `occurred` (if a risk occurs, raise an issue) |
| review_date | | date |

## issue_register.csv
| Column | Req | Values / notes |
|---|---|---|
| id | ✓ | I-### |
| date_raised | ✓ | |
| raised_by | ✓ | |
| type | ✓ | `request_for_change`, `off_specification`, `problem`, `concern`, `business_opportunity` |
| description | ✓ | |
| priority | | `high`, `medium`, `low` |
| severity | | the level that can decide: `team_manager`, `project_manager`, `change_authority`, `project_board`, `business_layer` |
| status | ✓ | `open`, `in_progress`, `awaiting_decision`, `closed` |
| owner | | |
| decision | | e.g. approved, rejected, deferred, granted_concession |
| decision_by | | required when a closed issue is a request_for_change or off_specification |
| decision_date | | |
| target_date | | |
| closure_date | | |
| issue_report_ref | | link if a formal issue report exists |

Informal problems handled by the PM can stay in the daily log. Use the register for anything needing formal management.

## quality_register.csv
| Column | Req | Values / notes |
|---|---|---|
| id | ✓ | Q-### |
| product_id | ✓ | should exist in product_register |
| product_title | | |
| method | ✓ | e.g. review, test, eval, inspection, ci |
| producer | | |
| reviewer | | |
| approver | | |
| planned_date | ✓ | |
| forecast_date | | |
| actual_date | | |
| result | ✓ | `pending`, `pass`, `pass_with_actions`, `fail` |
| records_ref | | link to evidence (CI run, review notes, eval report) |

## product_register.csv
Replaces v6 configuration item records and the product status account.

| Column | Req | Values / notes |
|---|---|---|
| product_id | ✓ | |
| title | ✓ | |
| type | ✓ | `management`, `specialist` |
| version | | |
| status | ✓ | `planned`, `in_development`, `in_review`, `approved`, `baselined`, `handed_over`, `withdrawn` |
| owner | | |
| location | | path, URL or repo ref (for AI work, include model IDs, prompt and dataset versions) |
| baseline_date | | required when approved, baselined or handed_over |
| stage | | |
| notes | | |

## daily_log.csv
| Column | Req | Notes |
|---|---|---|
| id | ✓ | D-### |
| date | ✓ | |
| entry | ✓ | problem, action, event or comment |
| person_responsible | | |
| target_date | | |
| result | | |

## lessons_log.csv
| Column | Req | Values / notes |
|---|---|---|
| id | ✓ | L-### |
| date_logged | ✓ | |
| logged_by | ✓ | |
| lesson_type | ✓ | `project`, `corporate`, `both` |
| event | ✓ | what happened |
| effect | | positive or negative |
| cause | | root cause or trigger |
| early_warning | | indicators that could have been seen |
| recommendation | | |
| status | ✓ | `open`, `actioned`, `closed` |
| applied_to | | where the lesson was applied (e.g. CLAUDE.md, the org standard, the next stage plan) |

## Maintenance rules
- When a risk occurs, close it as `occurred` and raise an issue that references it.
- A `fail` in the quality register must lead to an issue (`off_specification`) or a re-review row.
- Review open risks at least every highlight period. The script warns when `review_date` has passed.
- Agents write to the log only through append-or-edit commits with a clear message. Humans review the log diffs at checkpoints.
