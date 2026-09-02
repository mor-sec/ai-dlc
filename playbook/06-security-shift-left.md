---
owner: security-engineering
audience: security engineers, developers
reviewed: 2026-09-02
review-cadence: quarterly
---

# 06 — Shift-Left Security

Shift-left under AI-DLC means security enters at **Mob Elaboration** — before a line is generated — and is enforced continuously by automation thereafter. AI changes the security equation in both directions: agents apply security standards with perfect consistency *when steered*, and generate vulnerabilities at machine speed when not. This chapter makes the steering and the automation concrete.

## The threat picture under AI-DLC

Everything from the classic SDL still applies. New or amplified:

| Risk | Why it's new/worse | Primary control |
|---|---|---|
| Insecure generated code at volume | Agents reproduce insecure idioms confidently; volume swamps manual review | Secure steering + SAST on every PR + human review gate |
| Hallucinated / typosquatted dependencies | Agents may import plausible-but-wrong packages | Lockfiles, private registry/proxy with allowlist, SCA |
| Prompt injection | Anything an agent reads (tickets, docs, web pages, tool output) is an instruction channel | Least-privilege agent permissions; treat external content as data; human gates on consequential actions |
| Secrets exposure to/by agents | Agents read `.env`s and paste configs into context or output | Secrets manager only, never in repo/env files; secret scanning both directions |
| Agent-tool blast radius | MCP servers and CLI permissions are a new privilege surface | Review agent/MCP permissions like service accounts; default-deny |
| License contamination | Generated code may mirror copyleft sources | SCA with license policy in CI |

## Security in each phase

### Inception: threat modeling as elaboration

Every Unit of Work gets a **threat-model pass inside Mob Elaboration** — this is the actual "shift left":

- The AI drafts a lightweight STRIDE-style threat model from the Unit of Work: assets touched, trust boundaries crossed, abuse cases, proposed mitigations. Package this as a `threat-model` skill ([Chapter 03](03-tooling-strategy.md)) so it's a 10-minute ritual, not a workshop.
- The pod reviews; mitigations become **acceptance criteria in the Unit of Work** — which means agents implement them and tests verify them, for free, downstream.
- **Escalation rule:** Units touching authN/authZ, money movement, PII, or crypto get a security engineer in the elaboration session and a named security reviewer at the merge gate.

### Construction: secure steering + automated verification

**Steering (prevention):** `CLAUDE.md` carries the repo's security constraints — parameterized queries only, the approved authZ pattern, input validation at trust boundaries, the secrets-manager API, forbidden functions/libraries. One steering line ("all SQL through the query builder; never string-concatenate") prevents a vulnerability class *in every future generation* — the highest-ROI security control in the whole program. Maintain a shared security section in the [CLAUDE.md template](../standards/claude-md-template.md) owned by security engineering.

**Pipeline (detection)** — all blocking on PR, all with agent-triage before human triage:

| Control | Tool examples | Gate |
|---|---|---|
| SAST | Semgrep (custom rules for your patterns), CodeQL | Block on high+ |
| SCA + licenses | OSV/Dependabot/Renovate, Socket for supply-chain risk | Block on known-exploited; license policy |
| Secrets | gitleaks/trufflehog + push protection | Block, always, no exceptions |
| IaC scanning | Checkov/tfsec/cfn-nag | Block on high+ |
| Container scan | Trivy/ECR scanning | Block on critical |
| DAST (deployed envs) | ZAP baseline vs. ephemeral env ([Chapter 07](07-devops-automation.md)) | Report; block on new high |

**Agent-triage:** the agent gets first pass at scanner findings — clustering duplicates, proposing fixes, drafting false-positive rationales — and a human disposes. Triage rationale is written into the PR; "suppressed because noisy" without rationale fails review.

### Operations: continuous verification

- Runtime posture per normal enterprise practice (WAF, cloud posture management, detection); agents join incident response as first-line investigators ([Chapter 07](07-devops-automation.md)).
- **Feedback loop — the part most programs skip:** every production security finding triggers the question *"what steering line, Semgrep rule, or skill change makes this class impossible?"* Fold the answer into the shared steering/rules repo the same week. This is how the program compounds.

## Securing the agents themselves

1. **Least privilege:** agents run with default-deny permissions; destructive commands and protected paths (auth config, migrations, CI workflows) require explicit human approval per invocation. Hooks enforce this mechanically.
2. **MCP servers are privileged integrations:** each one gets an owner, a scoped service identity (never a human's personal token), and a permissions review at adoption + annually.
3. **Prompt-injection hygiene:** agents that read external content (web, third-party tickets, artifact comments) must not be able to silently take consequential actions — the human gate between "agent read something" and "agent did something irreversible" is the control.
4. **No secrets in context:** secrets live in the secrets manager; agents reference them by name in code and never see values. Secret-scan agent-authored diffs like any other.
5. **Auditability:** agent sessions, approvals, and tool invocations are logged. Under AI-DLC you get a bonus artifact: the full intent→plan→diff trail ([Chapter 08](08-github-jira.md)) is a security audit trail too.

## Anti-patterns

- **Scan-and-dump.** Turning on five scanners with no triage capacity; 400 findings, all ignored. Automate triage with agents, block only on tuned severities, expand gradually.
- **Security as the merge-gate surprise.** If the first security signal appears at PR time, elaboration failed. Mitigations belong in acceptance criteria.
- **"The AI wrote it, so it must follow our standards."** Steering raises the floor; it doesn't remove the need for verification. Trust the pipeline, not the vibe.
- **Blanket agent permissions to stop the prompting fatigue.** Fix fatigue by pre-approving *specific safe commands*, never by wildcarding.
- **Prototype exemptions** ([Chapter 05](05-rapid-prototyping.md)): real data gets real controls regardless of the repo's label.

## Tips & tricks

- **Write Semgrep rules from your own incidents** — a custom rule encoding *your* last vulnerability beats a hundred generic ones, and agents can draft the rule from the post-mortem.
- **Adversarial review prompt:** before merge, ask a fresh agent session to attack the diff ("find injection, authZ bypass, and data-exposure paths in this change"). Cheap red-team pass; catches what the generating session is blind to.
- **Threat-model the Unit, not the sprint:** small, per-Unit threat models stay honest; quarterly workshop-style models go stale in a week.
- **Track "vulnerability classes eliminated"** (via steering/rules) as your program metric, not raw finding counts — it measures compounding, which is the point.

## References

- OWASP: [Top 10](https://owasp.org/www-project-top-ten/), [LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/), ASVS
- [Wiz: AppSec under AI-DLC](https://www.wiz.io/academy/ai-security/ai-driven-development-lifecycle-ai-dlc)
- Previous: [Chapter 05 — Rapid Prototyping](05-rapid-prototyping.md) · Next: [Chapter 07 — DevOps Automation](07-devops-automation.md)
