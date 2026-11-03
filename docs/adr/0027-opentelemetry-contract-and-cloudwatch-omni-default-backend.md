# 0027 — Make OpenTelemetry the instrumentation contract and CloudWatch Omni the default observability backend

- **Status:** Proposed
- **Date:** 2026-11-03
- **Deciders:** Playbook maintainers (Stephen Morleys)
- **Unit of Work:** none; drafted in a working session on 2026-11-03

## Context

[Chapter 07](../../playbook/07-devops-automation.md#observability-requirements) names three observability non-negotiables and OpenTelemetry for traces, but no backend. [Chapter 03](../../playbook/03-tooling-strategy.md#the-stack-at-a-glance) names a standard for every other layer of the stack and leaves observability as one word in the MCP row. The [`incident-investigate` skill](../../standards/skills/incident-investigate/SKILL.md) assumes "observability access via MCP", which is only true once a concrete server is configured. A pod adopting the playbook on a blank slate has nothing to copy.

The playbook has since put agents in the loop twice over, and neither place has a named home for its telemetry. The coding agent emits OpenTelemetry about tokens, cost, sessions, and tool calls; the [metrics reference](../../standards/metrics-reference.md#cost) wants that as the source of its cost rows but still names a billing export. Products built under [Chapter 13](../../playbook/13-building-ai-features.md#operating-ai-features) call models and must log, per request, the fields that explain an output, traced like any other call.

AWS released Amazon CloudWatch Omni in September 2026: an interface and set of workflows built on CloudWatch for applications and AI agents, which ingests existing CloudWatch agent, OTLP, and SDK telemetry with nothing reconfigured, adds agent observability and evaluation across named frameworks, and answers plain-language questions by writing the query. The adopting organization has no incumbent observability platform, and its production and infrastructure standard is AWS.

## Decision

We will make OpenTelemetry the instrumentation contract for every service and agent, and CloudWatch Omni the default backend for AWS-hosted workloads, with the facts that rot recorded in a dated standard.

- **The contract.** Services, AI features, and the agents themselves emit OTLP: structured logs with correlation IDs, traces across bounded-context hops, and metrics carrying the pod and the Unit of Work key as resource attributes. No vendor SDK in application code; the exporter is configuration. A backend that cannot take OTLP is not a candidate.
- **The backend.** CloudWatch Omni, enabled per organization behind existing SSO identities, with a space per account and Region as the product requires. Pods get access during repo onboarding, alongside the other MCP servers. Access, pricing model, framework coverage, and known gaps live in the [observability stack reference](../../standards/observability-stack.md), reviewed quarterly.
- **Agent telemetry.** The coding agent's OpenTelemetry export is switched on in the [agent baseline](../../standards/agent-baseline.md) and sent to the CloudWatch OTLP metrics endpoint with pod and Unit attributes. The metrics reference's token and cost rows move to that source once the spike in Follow-ups confirms the data lands.
- **Chapters stay vendor-neutral.** Chapter 07 keeps the requirements and gains a fourth, that the agents are instrumented too. Vendor names live in the standard and here.
- **Status Proposed.** An agent drafted this ADR; a named human accepts it.

## Options considered

### Option A — OpenTelemetry contract, CloudWatch Omni default  ← chosen

- Pros: matches the AWS stack, so telemetry stays inside the existing perimeter and agreement; telemetry already in CloudWatch appears with nothing to reconfigure; agent observability and evaluation are first-class, which is exactly the gap in Chapters 07 and 13; plain-language query and the investigation hand-off line up with the `incident-investigate` skill; nothing to host.
- Cons: generally available only since September 2026; a separate organization URL and identity surface to govern; Claude Code and the Claude Agent SDK are not on the named framework list, so agent-level views for the primary agent are unverified; no MCP server is documented, and the agent entry point is Omni's own skills; one space sees one account and Region, so cross-account views depend on centralization rules; Omni alerts are priced separately from classic CloudWatch alarms.

### Option B — Classic CloudWatch only, Omni not enabled

- Pros: the oldest and best-documented surface; a CloudWatch MCP server exists today for logs, metrics, and alarms; the coding-agent integration is documented against it.
- Cons: agent observability, evaluations, the application map, and plain-language query are the Omni surface; everything in this option is still available under Option A, because enabling Omni changes nothing already running.
- Rejected because: it withholds the one part that addresses the gap and buys no safety in return. Its MCP server and documented coding-agent path remain in use under Option A until Omni's own entry point is verified.

### Option C — A third-party platform over OpenTelemetry (Datadog, Grafana Cloud, Honeycomb)

- Pros: mature LLM and agent observability in some products; multi-cloud; strong query languages and MCP servers.
- Cons: a second vendor and data perimeter for telemetry that carries code paths, prompts, and ticket text, so [vendor governance](../../playbook/03-tooling-strategy.md#vendor-governance) applies in full; per-host or per-seat pricing; a procurement cycle before the first pod ships.
- Rejected because: on a blank slate inside an AWS perimeter there is no incumbent to justify the second vendor. Kept as the named alternative for organizations that already run one; the OpenTelemetry contract makes that swap configuration, not code.

### Option D — Self-hosted collector and open-source stack

- Pros: no vendor; full control of retention and cost.
- Cons: a platform to run, patch, and scale before the first pod ships, owned by the platform pod, which is the scarce resource.
- Rejected because: it spends the platform pod on undifferentiated hosting.

## Consequences

- Positive: every repo has one answer for where logs, traces, and agent telemetry go; the `incident-investigate` skill's input names a real server; the cost rows in the metrics reference gain a system of record once the spike passes; a backend change is exporter configuration.
- Negative: a bet on a product weeks past general availability; a second identity surface in onboarding and the agent baseline; per-GB ingestion means a looping agent costs money twice, in tokens and in telemetry; the Chapter 13 rule that restricted content is never logged raw now has a destination to enforce it at.
- Follow-ups: spike the coding agent's export against the CloudWatch OTLP endpoint and confirm the metrics appear in an Omni space with pod and Unit attributes, then record the result in the standard and, on success, change the Source column of the token and cost rows in the metrics reference; add the Omni domain, space, and metrics API key to repo onboarding and the agent baseline; decide whether the `incident-investigate` skill reaches the backend through the CloudWatch MCP server or Omni's skills, and record it in the standard; check what the coding agent's telemetry carries against the [data-in-context rule](../../playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership) before enabling it org-wide.

## Revisit when

The spike fails, or a quarter passes without the primary agent's telemetry showing agent-level views in Omni; the organization acquires an incumbent platform through a merger or an enterprise agreement, or moves production off AWS; Omni's pricing or access model changes materially, or an availability incident runs longer than a working day; or the quarterly review of the standard finds pods routing around Omni to a second tool.
