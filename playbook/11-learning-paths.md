---
owner: platform-enablement
audience: engineering leaders, developers
reviewed: 2026-09-18
review-cadence: quarterly
---

# 11 — Learning Paths & Enablement

Tool licenses without enablement produce autocomplete users and disappointing metrics. This chapter defines the org rollout program and role-based learning paths — what each role must know, in what order, and how skill is verified (by doing, not by certificates of attendance).

## The enablement program (three waves)

Mirrors AWS's recommended AI-DLC adoption path:

1. **Executive alignment (2–4 weeks).** Leadership internalizes what actually changes: team shapes (AI Pods), metrics (Units of Work and lead time, not story points or LOC), budget shape (tokens and enablement, fewer seats — budgeted like cloud spend, with showback per pod at cost per validated Unit of Work, [Chapter 03](03-tooling-strategy.md#unit-economics-cost-per-validated-unit-of-work)), and the review-capacity bottleneck. Output: a signed-off [pilot charter](../standards/pilot-charter-template.md) naming pods, scope, and success criteria; how to earn the signatures is [Chapter 12](12-adoption-strategy.md#earning-stakeholder-buy-in). Skipping this wave is how pilots succeed and programs still die.
2. **Technical enablement (4–6 weeks, overlapping).** Architects and senior engineers build the shared foundations the pods will stand on: steering-file baseline, skill library seeds, [reference pipeline](07-devops-automation.md), [Jira integration](08-github-jira.md), agent permissions and [security guardrails](06-security-shift-left.md). Output: a "paved road" a pilot pod can walk on day one.
3. **Pilot pods (one quarter).** 1–2 pods on real, low-blast-radius work — [legacy Java upgrades](10-legacy-modernization.md) and [prototypes](05-rapid-prototyping.md) are ideal first Bolts (low ambiguity, high verifiability). Pods keep journals ([Chapter 02](02-ways-of-working.md)); Friday lessons flow into the shared steering repo. Output: measured before/after (baseline captured per the [metrics reference](../standards/metrics-reference.md#the-pilot-baseline) *before* the pilot starts), refined playbook, and — most importantly — the first cohort of practitioners who train the next.

Scale by **seeding**: each pilot pod member anchors a new pod next quarter. Practitioner-to-practitioner transfer beats any course catalog.

## Role-based learning paths

Each path = curriculum + a **practicum** (the verification). Nobody is "enabled" by watching videos.

### Developer (pod member)

| Stage | Content | Practicum |
|---|---|---|
| 1. Method | Playbook ch. [01](01-ai-dlc-methodology.md)–[02](02-ways-of-working.md); Anthropic's [Claude Code docs](https://docs.claude.com/en/docs/claude-code) and agentic-coding best practices | Shadow a working pod for two Bolts |
| 2. Craft | Context engineering (ch. [03](03-tooling-strategy.md)): steering files, plan mode, skills, hooks; reviewing agent output (the [Chapter 02](02-ways-of-working.md) review disciplines) | Drive a Bolt under supervision; write one steering improvement + one skill |
| 3. Depth | DDD & event-driven fundamentals (ch. [04](04-architecture.md)); shift-left security practices (ch. [06](06-security-shift-left.md)) | Lead a Mob Elaboration; pass the "explain it back" ritual on a non-trivial merge |

External anchors: Evans/Vernon for DDD; OWASP secure-coding; AWS Skill Builder's AI-DLC and Q Developer modules where AWS tooling is in play.

### Architect

Playbook ch. [04](04-architecture.md), [07](07-devops-automation.md), [10](10-legacy-modernization.md) deep; event-storming facilitation; designing for agent-buildability (context boundaries sized to sessions); golden-path construct/module authorship. **Practicum:** run a real event-storming session; author one paved-road module adopted by ≥2 pods; write the ADRs for one carve of the legacy estate.

### Product owner

Ch. [01](01-ai-dlc-methodology.md), [02](02-ways-of-working.md), [08](08-github-jira.md); writing unambiguous intent; acceptance criteria as testable statements; working *in* Mob Elaboration (deciding live, not queueing tickets). **Practicum:** bring two Units of Work through elaboration to production; rework rate on their Units becomes their feedback metric.

### QA engineer

Ch. [01](01-ai-dlc-methodology.md), [02](02-ways-of-working.md) (the QA accountability and the testing section), [07](07-devops-automation.md) (ephemeral environments and gates); writing acceptance criteria that are testable as written; the [test review checklist](../standards/test-review-checklist.md) as an adversarial reader; exploratory testing of agent-built behaviour in ephemeral environments; owning the AC-mapping check and the mutation thresholds for their pods. The shift to internalise: QA under AI-DLC verifies *intent*, not *behaviour*. Behaviour is verified by generated tests; whether the tests verify the right thing is the QA question. **Practicum:** find, in generated tests across two Units, three tests that pass with the bug present and get them rewritten; run the exploratory pass on one material change and log the findings in the PR.

### Security engineer

Ch. [06](06-security-shift-left.md) as owner, not reader; steering-as-control authorship; Semgrep rule writing; agent/MCP permission review; threat-modeling-in-elaboration facilitation. **Practicum:** eliminate one vulnerability class via steering + rule + test template, demonstrated across pods.

### Engineering leader

Wave-1 content plus: reading the new metrics ([ch. 02](02-ways-of-working.md), [08](08-github-jira.md)), budgeting tokens vs. seats against the [model selection reference](../standards/model-selection.md), and the discipline of *not* reintroducing Scrum ceremonies when a quarter gets bumpy. **Practicum:** run a quarter's pilot review against the charter's success criteria, in writing.

## The knowledge system (how learning compounds)

Courses bootstrap; the running system sustains:

- **The steering repo is the curriculum.** Every lesson a pod learns lands in CLAUDE.md baselines, skills, or Semgrep rules the same week — new pods inherit it automatically. Measure updates/week; zero for a month means learning has stalled ([ch. 02 metrics](02-ways-of-working.md)).
- **Pod journals → monthly digest.** One person (rotating) distills all pod journals into a monthly "what we learned" markdown digest; 30 minutes to read, org-wide.
- **Guild hour, biweekly:** one pod demos a real Bolt — plan, steering, failures included. Live failure analysis teaches more than any polished talk. Guild hour and the digest are the core rituals of the [community of practice](12-adoption-strategy.md#the-community-of-practice), which keeps them running after the enablement quarter.
- **Everything is markdown in git** ([Chapter 09](09-documentation-standards.md)) — which means the enablement corpus itself is agent context: "how do we do X here?" is answerable by an agent reading the playbook. This playbook is the onboarding bot's brain.

## Anti-patterns

- **Certification theater.** Attendance certificates without practica. If skill verification isn't "did a thing under observation," it isn't verification.
- **Training the tool, not the method.** A day of "prompt tips" without ways-of-working change reproduces the autocomplete plateau.
- **Big-bang rollout.** Forty teams on day one means forty teams improvising badly in parallel and no seeding cohort. Waves or nothing.
- **Enablement as an event.** A launch quarter with no guild, no digest, no steering cadence — knowledge stops compounding the day the trainers leave.
- **Ignoring the skeptics' data.** Veterans' objections are usually real edge cases; run their example through a Bolt publicly. Convert or learn — both are wins.

## Tips & tricks

- **Pair veterans with enthusiasts** in pilot pods: enthusiasm without judgment ships slop; judgment without enthusiasm ships nothing.
- **Make the first Bolt a guaranteed win:** pre-flighted repo, warm steering file, well-elaborated Unit. First impressions of the method are set in one afternoon.
- **Track time-to-first-solo-Bolt** per developer as the enablement metric (typical: 2–4 weeks inside a pod).
- **Budget 20% of pilot-quarter capacity for enablement work itself** (steering, skills, journals). It feels like overhead; it's the compounding principal.

## References

- [AWS Skill Builder](https://skillbuilder.aws) · [Anthropic Academy / Claude Code training](https://www.anthropic.com/learn) · [DDD reading path: Evans, Vernon](04-architecture.md#references)
- Previous: [Chapter 10 — Legacy Modernization](10-legacy-modernization.md) · Next: [Chapter 12 — Adoption Strategy](12-adoption-strategy.md)
