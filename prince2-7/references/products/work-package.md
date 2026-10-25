# Work package

**Purpose:** the formal agreement between the PM and a team manager (or team) to deliver specific products within tolerance. It is the main delegation mechanism, and the hand-off point to agents.

| | |
|---|---|
| **Created in** | Controlling a stage (CS): authorise a work package |
| **Accepted in** | Managing product delivery (MP) |
| **Prepared by** | PM, agreed with the team manager |
| **Derived from** | Stage plan, product descriptions, quality management approach |

## Composition
1. Date, PM and team manager or person authorised
2. **Work package description**: the work to be done
3. Techniques, processes and procedures to use
4. Development interfaces: people and systems to work with
5. Operations and maintenance interfaces: what the products must fit into
6. Configuration and version requirements: how products are versioned, stored and handed back
7. Joint agreements on effort, cost, start and end dates, and key milestones
8. **Tolerances**: time, cost, scope, and others as relevant (quality, risk, sustainability)
9. Constraints
10. **Reporting arrangements**: checkpoint frequency and content
11. **Problem handling and escalation**: what to do when tolerance is forecast to breach
12. Extracts or references: the relevant parts of the stage plan, product descriptions and approaches
13. Approval method: who confirms completion, and how

## Quality criteria
- Every product in the package has a product description with quality criteria.
- Tolerances are explicit and achievable, and the escalation route is clear.
- The team manager or team has agreed the package, and has the capability and capacity to do it.
- Reporting cadence suits the package's risk.

## Agent-executable work package (AI SDLC template)
Use this when the work goes to a coding agent. Keep it short; link out for detail.

```yaml
id: WP-<stage>-<n>
products: [PD-012, PD-013]          # product description IDs
objective: <one sentence>
inputs: [specs/..., designs/...]
scope_allow: [src/billing/**, tests/billing/**]
scope_deny: [infra/**, secrets/**]
tolerances:
  time: { plan_hours: 6, plus: 2 }
  cost: { plan_usd: 40, plus: 10 }  # model/compute spend
  scope: "Must: PD-012. Could: PD-013"
  quality: "All acceptance tests + eval suite X >= 0.92; no new high-severity scan findings"
quality_method: [ci:tests, ci:evals, human-review:team-manager]
reporting: checkpoint on completion and every 2h of elapsed run time
on_forecast_breach: stop, write an issue (type=problem), notify <team manager>
human_gates: [design approval before code generation, merge]
data_rules: see digital and data management approach §AI
```

**AWS AI-DLC note:** one AI-DLC unit of work usually maps to one or a few work packages. The unit's construction plan supplies items 2, 3 and 12. The work package adds the tolerances, scope allow-list and escalation rule that make manage-by-exception enforceable.
