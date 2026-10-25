#!/usr/bin/env python3
"""PRINCE2 7 project log checker.

Standard library only. Works on a project folder laid out as:

    <project>/tolerances.json
    <project>/log/{daily_log,lessons_log,issue_register,risk_register,
                   quality_register,product_register}.csv

(If <project>/log/ doesn't exist, registers are read from <project>/ itself.)

Commands
    init <project>       create blank registers and a tolerances.json template
    validate <project>   schema / enum / date / hygiene checks   (exit 1 on errors)
    tolerance <project>  status per performance target           (exit 2 on forecast breach)
    summary <project>    highlight-report inputs

Use --json for machine-readable output, --today YYYY-MM-DD to fix "today",
--high-risk N to change the high-risk score threshold (default 15).
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

EXIT_OK, EXIT_INVALID, EXIT_EXCEPTION = 0, 1, 2

THREAT_RESPONSES = {"avoid", "reduce", "transfer", "share", "accept", "prepare_contingent_plans"}
OPPORTUNITY_RESPONSES = {"exploit", "enhance", "share", "accept", "prepare_contingent_plans"}
PERFORMANCE_TARGETS = ("benefits", "cost", "time", "quality", "scope", "sustainability", "risk")


@dataclass(frozen=True)
class Column:
    name: str
    required: bool = False
    enum: frozenset[str] | None = None
    kind: str = "text"  # text | date | int1to5


def col(name, required=False, enum=None, kind="text"):
    return Column(name, required, frozenset(enum) if enum else None, kind)


SCHEMAS: dict[str, list[Column]] = {
    "risk_register": [
        col("id", True), col("date_raised", True, kind="date"), col("raised_by", True),
        col("category"), col("risk_type", True, {"threat", "opportunity"}),
        col("cause", True), col("event", True), col("effect", True),
        col("probability", True, kind="int1to5"), col("impact", True, kind="int1to5"),
        col("proximity", enum={"imminent", "within_stage", "within_project", "beyond_project"}),
        col("response_category", enum=THREAT_RESPONSES | OPPORTUNITY_RESPONSES),
        col("response"), col("risk_owner"), col("risk_action_owner"),
        col("status", True, {"open", "closed", "occurred"}), col("review_date", kind="date"),
    ],
    "issue_register": [
        col("id", True), col("date_raised", True, kind="date"), col("raised_by", True),
        col("type", True, {"request_for_change", "off_specification", "problem", "concern",
                           "business_opportunity"}),
        col("description", True), col("priority", enum={"high", "medium", "low"}),
        col("severity", enum={"team_manager", "project_manager", "change_authority",
                              "project_board", "business_layer"}),
        col("status", True, {"open", "in_progress", "awaiting_decision", "closed"}),
        col("owner"), col("decision"), col("decision_by"), col("decision_date", kind="date"),
        col("target_date", kind="date"), col("closure_date", kind="date"), col("issue_report_ref"),
    ],
    "quality_register": [
        col("id", True), col("product_id", True), col("product_title"), col("method", True),
        col("producer"), col("reviewer"), col("approver"),
        col("planned_date", True, kind="date"), col("forecast_date", kind="date"),
        col("actual_date", kind="date"),
        col("result", True, {"pending", "pass", "pass_with_actions", "fail"}), col("records_ref"),
    ],
    "product_register": [
        col("product_id", True), col("title", True), col("type", True, {"management", "specialist"}),
        col("version"),
        col("status", True, {"planned", "in_development", "in_review", "approved", "baselined",
                             "handed_over", "withdrawn"}),
        col("owner"), col("location"), col("baseline_date", kind="date"), col("stage"), col("notes"),
    ],
    "daily_log": [
        col("id", True), col("date", True, kind="date"), col("entry", True),
        col("person_responsible"), col("target_date", kind="date"), col("result"),
    ],
    "lessons_log": [
        col("id", True), col("date_logged", True, kind="date"), col("logged_by", True),
        col("lesson_type", True, {"project", "corporate", "both"}), col("event", True),
        col("effect"), col("cause"), col("early_warning"), col("recommendation"),
        col("status", True, {"open", "actioned", "closed"}), col("applied_to"),
    ],
}
ID_COLUMN = {name: ("product_id" if name == "product_register" else "id") for name in SCHEMAS}

TOLERANCES_TEMPLATE = {
    "level": "stage",
    "name": "Stage 2",
    "as_of": "YYYY-MM-DD",
    "at_risk_threshold": 0.8,
    "targets": {
        "cost": {"unit": "AUD", "plan": 100000, "plus": 10000, "minus": 5000,
                 "actual_to_date": 0, "forecast": 100000},
        "time": {"unit": "working days", "plan": 40, "plus": 4, "minus": None, "forecast": 40},
        "benefits": {"unit": "% of target", "plan": 100, "plus": None, "minus": 10, "forecast": 100},
        "sustainability": {"unit": "tCO2e", "plan": 1.0, "plus": 0.2, "minus": None, "forecast": 1.0},
        "risk": {"type": "risk_register", "max_single_score": 15, "max_total_exposure": 100},
        "scope": {"type": "qualitative", "tolerance": "Could-have products may be deferred",
                  "status": "within", "note": ""},
        "quality": {"type": "qualitative", "tolerance": "Per product description quality tolerances",
                    "status": "within", "note": ""},
    },
}


# ---------------------------------------------------------------- loading

def log_dir(project: Path) -> Path:
    sub = project / "log"
    return sub if sub.is_dir() else project


def load_register(project: Path, name: str) -> tuple[list[str] | None, list[dict[str, str]]]:
    path = log_dir(project) / f"{name}.csv"
    if not path.exists():
        return None, []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        header = [h.strip() for h in (reader.fieldnames or [])]
        rows = [{(k or "").strip(): (v or "").strip() for k, v in row.items()} for row in reader]
    return header, rows


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def risk_score(row: dict[str, str]) -> int | None:
    try:
        return int(row["probability"]) * int(row["impact"])
    except (KeyError, ValueError):
        return None


# ---------------------------------------------------------------- validate

@dataclass
class Findings:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def err(self, reg, rid, msg):
        self.errors.append(f"{reg}[{rid}]: {msg}")

    def warn(self, reg, rid, msg):
        self.warnings.append(f"{reg}[{rid}]: {msg}")


def validate(project: Path, today: date, high_risk: int) -> Findings:
    f = Findings()
    data: dict[str, list[dict[str, str]]] = {}

    for name, schema in SCHEMAS.items():
        header, rows = load_register(project, name)
        if header is None:
            f.warnings.append(f"{name}: file missing (run `init` or create {name}.csv)")
            continue
        data[name] = rows
        missing = [c.name for c in schema if c.name not in header]
        if missing:
            f.errors.append(f"{name}: missing columns {missing}")
        unknown = [h for h in header if h not in {c.name for c in schema}]
        if unknown:
            f.warnings.append(f"{name}: unrecognised columns {unknown} (ignored)")

        id_col, seen = ID_COLUMN[name], set()
        for i, row in enumerate(rows, start=2):
            rid = row.get(id_col) or f"row {i}"
            if row.get(id_col):
                if row[id_col] in seen:
                    f.err(name, rid, "duplicate id")
                seen.add(row[id_col])
            for c in schema:
                v = row.get(c.name, "")
                if not v:
                    if c.required:
                        f.err(name, rid, f"'{c.name}' is required")
                    continue
                if c.enum and v not in c.enum:
                    f.err(name, rid, f"'{c.name}'={v!r} not in {sorted(c.enum)}")
                if c.kind == "date" and parse_date(v) is None:
                    f.err(name, rid, f"'{c.name}'={v!r} is not YYYY-MM-DD")
                if c.kind == "int1to5" and v not in {"1", "2", "3", "4", "5"}:
                    f.err(name, rid, f"'{c.name}'={v!r} must be 1-5")

    _hygiene(f, data, today, high_risk)
    return f


def _past(value: str, today: date) -> bool:
    d = parse_date(value) if value else None
    return d is not None and d < today


def _hygiene(f: Findings, data, today: date, high_risk: int) -> None:
    for r in data.get("risk_register", []):
        rid = r.get("id", "?")
        rtype, cat = r.get("risk_type"), r.get("response_category")
        if cat:
            allowed = THREAT_RESPONSES if rtype == "threat" else OPPORTUNITY_RESPONSES
            if rtype in {"threat", "opportunity"} and cat not in allowed:
                f.err("risk_register", rid, f"response '{cat}' is not valid for an {rtype}")
        if r.get("status") == "open":
            score = risk_score(r)
            if score is not None and score >= high_risk:
                if not r.get("risk_owner"):
                    f.err("risk_register", rid, f"high risk (score {score}) has no risk_owner")
                if not r.get("response"):
                    f.err("risk_register", rid, f"high risk (score {score}) has no response")
            if _past(r.get("review_date", ""), today):
                f.warn("risk_register", rid, f"review overdue (review_date {r['review_date']})")

    for r in data.get("issue_register", []):
        rid = r.get("id", "?")
        status = r.get("status")
        if status != "closed" and _past(r.get("target_date", ""), today):
            f.warn("issue_register", rid, f"open past target_date {r['target_date']}")
        if status == "closed":
            if r.get("type") in {"request_for_change", "off_specification"} and not r.get("decision_by"):
                f.err("issue_register", rid, "closed RFC/off-spec without decision_by")
            if not r.get("closure_date"):
                f.warn("issue_register", rid, "closed without closure_date")
        if status == "awaiting_decision" and not r.get("severity"):
            f.warn("issue_register", rid, "awaiting decision but no severity (who decides?)")

    products = {p.get("product_id") for p in data.get("product_register", [])}
    for q in data.get("quality_register", []):
        qid = q.get("id", "?")
        if products and q.get("product_id") and q["product_id"] not in products:
            f.warn("quality_register", qid, f"product_id {q['product_id']} not in product_register")
        if q.get("result") == "pending":
            due = q.get("forecast_date") or q.get("planned_date", "")
            if _past(due, today):
                f.warn("quality_register", qid, f"quality check overdue (due {due})")
        if q.get("result") in {"pass", "pass_with_actions", "fail"} and not q.get("actual_date"):
            f.warn("quality_register", qid, "result recorded without actual_date")
        if q.get("result") == "fail":
            f.warn("quality_register", qid, "failed: ensure an off_specification issue or re-review exists")

    for p in data.get("product_register", []):
        if p.get("status") in {"approved", "baselined", "handed_over"} and not p.get("baseline_date"):
            f.err("product_register", p.get("product_id", "?"), f"status {p['status']} needs baseline_date")

    for d in data.get("daily_log", []):
        if not d.get("result") and _past(d.get("target_date", ""), today):
            f.warn("daily_log", d.get("id", "?"), f"action past target_date {d['target_date']} with no result")

    for lesson in data.get("lessons_log", []):
        if lesson.get("status") == "actioned" and not lesson.get("applied_to"):
            f.warn("lessons_log", lesson.get("id", "?"), "actioned but applied_to is empty")


# ---------------------------------------------------------------- tolerance

def _num(v):
    return None if v is None or v == "" else float(v)


def assess_target(name: str, spec: dict, project: Path, threshold: float) -> dict:
    kind = spec.get("type", "numeric")
    out = {"target": name, "type": kind}

    if kind == "qualitative":
        status = spec.get("status", "unknown")
        if status not in {"within", "at_risk", "breach_forecast"}:
            status = "unknown"
        out.update(status=status, detail=spec.get("tolerance", ""), note=spec.get("note", ""))
        return out

    if kind == "risk_register":
        _, rows = load_register(project, "risk_register")
        threats = [r for r in rows if r.get("status") == "open" and r.get("risk_type") == "threat"]
        scores = [s for s in (risk_score(r) for r in threats) if s is not None]
        max_single, total = (max(scores) if scores else 0), sum(scores)
        lim_single, lim_total = spec.get("max_single_score"), spec.get("max_total_exposure")
        ratios = [v / lim for v, lim in ((max_single, lim_single), (total, lim_total)) if lim]
        worst = max(ratios, default=0)
        status = "breach_forecast" if worst > 1 else "at_risk" if worst >= threshold else "within"
        out.update(status=status,
                   detail=f"max open threat score {max_single}/{lim_single}; "
                          f"total exposure {total}/{lim_total} ({len(threats)} open threats)")
        return out

    plan, forecast = _num(spec.get("plan")), _num(spec.get("forecast"))
    plus, minus = _num(spec.get("plus")), _num(spec.get("minus"))
    unit = spec.get("unit", "")
    if plan is None or forecast is None:
        out.update(status="unknown", detail="plan and forecast are required for numeric targets")
        return out
    variance = forecast - plan
    side_tol = plus if variance >= 0 else minus
    if variance == 0:
        status = "within"
    elif side_tol is None:
        status = "within"  # no tolerance set on this side = unconstrained
    elif abs(variance) > side_tol:
        status = "breach_forecast"
    elif side_tol == 0 or abs(variance) >= threshold * side_tol:
        status = "at_risk"
    else:
        status = "within"
    used = None if not side_tol else round(abs(variance) / side_tol * 100)
    out.update(status=status, plan=plan, forecast=forecast, variance=variance,
               plus=plus, minus=minus, unit=unit,
               detail=f"forecast {forecast:g} vs plan {plan:g} {unit} "
                      f"(variance {variance:+g}; tolerance +{_fmt(plus)}/-{_fmt(minus)}"
                      + (f"; {used}% of tolerance used)" if used is not None else ")"))
    return out


def _fmt(v):
    return "n/a" if v is None else f"{v:g}"


def tolerance(project: Path) -> dict:
    path = project / "tolerances.json"
    if not path.exists():
        raise SystemExit(f"error: {path} not found (run `init` first)")
    cfg = json.loads(path.read_text(encoding="utf-8"))
    threshold = float(cfg.get("at_risk_threshold", 0.8))
    targets = cfg.get("targets", {})
    results = [assess_target(n, targets[n], project, threshold) for n in PERFORMANCE_TARGETS if n in targets]
    extra = sorted(set(targets) - set(PERFORMANCE_TARGETS))
    missing = [n for n in PERFORMANCE_TARGETS if n not in targets]
    return {
        "level": cfg.get("level"), "name": cfg.get("name"), "as_of": cfg.get("as_of"),
        "results": results, "missing_targets": missing, "unknown_targets": extra,
        "exception": any(r["status"] == "breach_forecast" for r in results),
    }


# ---------------------------------------------------------------- summary

def summary(project: Path, today: date, high_risk: int) -> dict:
    out: dict = {"as_of": today.isoformat()}
    _, risks = load_register(project, "risk_register")
    open_risks = [r for r in risks if r.get("status") == "open"]
    ranked = sorted(open_risks, key=lambda r: risk_score(r) or 0, reverse=True)
    out["risks"] = {
        "open": len(open_risks),
        "open_threats": sum(r.get("risk_type") == "threat" for r in open_risks),
        "open_opportunities": sum(r.get("risk_type") == "opportunity" for r in open_risks),
        "high": sum((risk_score(r) or 0) >= high_risk for r in open_risks),
        "top": [{"id": r.get("id"), "score": risk_score(r), "type": r.get("risk_type"),
                 "event": r.get("event"), "owner": r.get("risk_owner")} for r in ranked[:5]],
    }
    _, issues = load_register(project, "issue_register")
    open_issues = [i for i in issues if i.get("status") != "closed"]
    by_type: dict[str, int] = {}
    for i in open_issues:
        by_type[i.get("type", "?")] = by_type.get(i.get("type", "?"), 0) + 1
    out["issues"] = {
        "open": len(open_issues), "open_by_type": by_type,
        "awaiting_decision": [{"id": i.get("id"), "type": i.get("type"), "severity": i.get("severity"),
                               "description": i.get("description")}
                              for i in open_issues if i.get("status") == "awaiting_decision"],
    }
    _, quality = load_register(project, "quality_register")
    out["quality"] = {
        "pass": sum(q.get("result") in {"pass", "pass_with_actions"} for q in quality),
        "fail": sum(q.get("result") == "fail" for q in quality),
        "pending": sum(q.get("result") == "pending" for q in quality),
        "overdue": [q.get("id") for q in quality if q.get("result") == "pending"
                    and _past(q.get("forecast_date") or q.get("planned_date", ""), today)],
    }
    _, products = load_register(project, "product_register")
    by_status: dict[str, int] = {}
    for p in products:
        by_status[p.get("status", "?")] = by_status.get(p.get("status", "?"), 0) + 1
    out["products"] = by_status
    _, lessons = load_register(project, "lessons_log")
    out["lessons_open"] = sum(lesson.get("status") == "open" for lesson in lessons)
    if (project / "tolerances.json").exists():
        out["tolerance"] = tolerance(project)
    return out


# ---------------------------------------------------------------- output

ICON = {"within": "OK ", "at_risk": "AT RISK", "breach_forecast": "EXCEPTION", "unknown": "?"}


def print_tolerance(t: dict) -> None:
    print(f"## Tolerance status: {t.get('level')} '{t.get('name')}' as of {t.get('as_of')}")
    for r in t["results"]:
        print(f"- {r['target']:<14} {ICON.get(r['status'], r['status']):<9} {r.get('detail', '')}"
              + (f" — {r['note']}" if r.get("note") else ""))
    if t["missing_targets"]:
        print(f"- not set: {', '.join(t['missing_targets'])}")
    if t["unknown_targets"]:
        print(f"- ignored (not PRINCE2 7 targets): {', '.join(t['unknown_targets'])}")
    print("\nEXCEPTION: tolerance forecast to be exceeded; raise an exception report."
          if t["exception"] else "\nAll set targets are forecast within tolerance.")


def print_summary(s: dict) -> None:
    r, i, q = s["risks"], s["issues"], s["quality"]
    print(f"# Project log summary ({s['as_of']})\n")
    print(f"Risks: {r['open']} open ({r['open_threats']} threats, {r['open_opportunities']} opportunities), "
          f"{r['high']} high")
    for t in r["top"]:
        print(f"  - {t['id']} [{t['type']}, score {t['score']}] {t['event']} — owner: {t['owner'] or 'NONE'}")
    print(f"Issues: {i['open']} open " + (f"{i['open_by_type']}" if i["open_by_type"] else ""))
    for a in i["awaiting_decision"]:
        print(f"  - awaiting decision: {a['id']} ({a['type']}, decided by {a['severity'] or '?'}) "
              f"{a['description']}")
    print(f"Quality checks: {q['pass']} passed, {q['fail']} failed, {q['pending']} pending"
          + (f", overdue: {', '.join(q['overdue'])}" if q["overdue"] else ""))
    print(f"Products: {s['products'] or 'none registered'}")
    print(f"Open lessons: {s['lessons_open']}\n")
    if "tolerance" in s:
        print_tolerance(s["tolerance"])


# ---------------------------------------------------------------- commands

def cmd_init(project: Path) -> int:
    target = project / "log"
    target.mkdir(parents=True, exist_ok=True)
    created = []
    for name, schema in SCHEMAS.items():
        path = target / f"{name}.csv"
        if path.exists():
            continue
        with path.open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow([c.name for c in schema])
        created.append(str(path))
    tol = project / "tolerances.json"
    if not tol.exists():
        tol.write_text(json.dumps(TOLERANCES_TEMPLATE, indent=2) + "\n", encoding="utf-8")
        created.append(str(tol))
    print("\n".join(f"created {p}" for p in created) or "nothing to create; all files exist")
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["init", "validate", "tolerance", "summary"])
    ap.add_argument("project", type=Path)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--today", type=date.fromisoformat, default=date.today())
    ap.add_argument("--high-risk", type=int, default=15, help="P×I score treated as high (default 15)")
    a = ap.parse_args(argv)

    if a.command == "init":
        return cmd_init(a.project)
    if not a.project.is_dir():
        print(f"error: {a.project} is not a directory", file=sys.stderr)
        return EXIT_INVALID

    if a.command == "validate":
        f = validate(a.project, a.today, a.high_risk)
        if a.json:
            print(json.dumps({"errors": f.errors, "warnings": f.warnings}, indent=2))
        else:
            for e in f.errors:
                print(f"ERROR   {e}")
            for w in f.warnings:
                print(f"WARNING {w}")
            print(f"\n{len(f.errors)} error(s), {len(f.warnings)} warning(s)")
        return EXIT_INVALID if f.errors else EXIT_OK

    if a.command == "tolerance":
        t = tolerance(a.project)
        print(json.dumps(t, indent=2)) if a.json else print_tolerance(t)
        return EXIT_EXCEPTION if t["exception"] else EXIT_OK

    s = summary(a.project, a.today, a.high_risk)
    print(json.dumps(s, indent=2)) if a.json else print_summary(s)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
