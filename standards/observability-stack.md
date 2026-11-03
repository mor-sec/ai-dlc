---
owner: platform-enablement
audience: developers, architects, on-call responders
reviewed: 2026-11-03
review-cadence: quarterly
---

# Observability Stack Reference

The instrumentation contract every service and agent follows, the backend it ships to today, and the facts about that backend that go stale. Audience: developers instrumenting a service or an agent, architects reviewing a design, and on-call responders setting up the agent's access. **This file goes stale by design.** The stable requirements live in [Chapter 07](../playbook/07-devops-automation.md#observability-requirements) and the decision is [ADR 0027](../docs/adr/0027-opentelemetry-contract-and-cloudwatch-omni-default-backend.md); this file is reviewed quarterly (see front-matter). If `reviewed` is more than a quarter old, distrust the facts below and update them.

## The contract: OpenTelemetry

- Every service, AI feature, and agent emits OTLP: structured logs with correlation IDs, traces across bounded-context hops, and metrics. No vendor SDK in application code; the exporter is configuration, so the backend can change without a code change.
- Two resource attributes ride on every signal so that cost and incidents read one system: the pod as `team.id` (the attribute AWS's coding-agent dashboards already read) and the Unit of Work's Jira key as `aidlc.unit_of_work`. Both are this standard's convention; the [metrics reference](metrics-reference.md) allocates by the same key.
- Deploy markers come from GitHub deployment events, carrying the same key, so "what changed?" is answerable by a person or an agent.
- What an AI feature logs per request is listed in [Chapter 13](../playbook/13-building-ai-features.md#operating-ai-features), not here. Restricted inputs and outputs are never logged raw ([Chapter 06](../playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership)); the backend does not change that rule.

## Current backend (as of 2026-11-03)

| Signal | Destination | Notes |
|---|---|---|
| Application logs, metrics, and traces for AWS-hosted services | Amazon CloudWatch, viewed and queried in CloudWatch Omni | OTLP through the CloudWatch agent (built on the OpenTelemetry Collector) or CloudWatch's native OTLP endpoints. Telemetry already in CloudWatch appears in Omni with nothing reconfigured. |
| Coding-agent sessions (Claude Code) | CloudWatch's OTLP metrics endpoint, authenticated with a bearer token (a CloudWatch metrics API key) | Token usage, sessions, code edits, tool calls, and cost, with `team.id` and cost-centre attributes; populates the Claude Code tab of CloudWatch's Coding Agent Insights. **Unverified in Omni:** the spike in ADR 0027's follow-ups decides whether the metrics reference's cost rows move to this source. |
| Model calls made by AI features ([Chapter 13](../playbook/13-building-ai-features.md)) | The same OTLP pipeline; Omni's agent observability where the framework is supported | Frameworks named at launch: LangGraph, CrewAI, OpenAI Agents SDK, Vercel AI SDK, and Strands. The Claude Agent SDK is not named; treat its telemetry as plain OTLP traces until verified. |
| Agent access for the [`incident-investigate`](skills/incident-investigate/SKILL.md) skill | The CloudWatch MCP server (Logs Insights, metrics, alarms), read-only | Omni documents no MCP server as of this date; its agent-facing entry point is its own skills. Which one the skill uses is an open follow-up in ADR 0027. |

## Facts that rot (checked 2026-11-03)

- **Status.** Generally available since September 2026. AWS describes Omni as "an interface and set of workflows built on Amazon CloudWatch", not a replacement; enabling it changes nothing already running. Existing console pages, metrics, alarms, dashboards, Logs Insights queries, and APIs keep working.
- **Access.** A dedicated organization URL, `https://<domain>.cloudwatch-omni.global.app.aws`, with the identities the organization already manages, outside the AWS console. A *space* sees the telemetry of one account and one Region; cross-account views need CloudWatch centralization rules. Enabling needs an AWS account with permission to create the domain and space in the CloudWatch console. A playground needs no account.
- **What is inside.** An application map, the Omni agent (plain language to SQL or PromQL), Threads, Alerts, and Dashboards; an alert can hand off to the AWS DevOps Agent for investigation. A free extension for VS Code, Cursor, and Kiro instruments and evaluates agents locally without an account.
- **Where configuration stays.** Log groups, retention, and ingestion endpoints are still configured in the CloudWatch console.
- **Pricing model.** Standard CloudWatch rates for ingestion and storage, per GB. Queries are charged per GB scanned above an allowance tied to monthly log and span ingestion; queries made through the Omni UI are free. Agent evaluations are charged at Bedrock AgentCore Evaluations rates. Omni alerts are priced separately from classic CloudWatch alarms. A 30-day trial credit is applied when Omni is enabled and covers OpenTelemetry ingestion only. Absolute prices are not recorded here because they rot fast; read the [pricing page](https://aws.amazon.com/cloudwatch/omni/pricing/).
- **Sources.** [Omni documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-omni.html) · [Claude Code telemetry in CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/coding-agents-claude-code.html) · [AWS observability round-up, August to September 2026](https://aws.amazon.com/blogs/mt/this-month-in-aws-observability-august-september-2026/).

## Onboarding a pod

1. The organization's Omni domain exists and the pod's members are in its SSO group; a space exists for each account and Region the pod deploys to.
2. The service emits OTLP with the two resource attributes above, and the deploy workflow posts the deploy marker.
3. The coding agent's telemetry is switched on through the [agent baseline](agent-baseline.md), not per repo. The metrics API key is a credential: owned, scoped to metrics, rotated, and never in a repository, the same treatment an [MCP server](../playbook/03-tooling-strategy.md#mcp-servers) gets.
4. The observability MCP server is configured read-only for the `incident-investigate` skill, and the pod's first drill of that skill runs against it.

## Quarterly review

- Re-check every fact above against the sources and bump `reviewed`.
- Answer three questions and update the table: did the coding-agent spike pass; is the Claude Agent SDK on Omni's framework list; does Omni ship an MCP server.
- Read OpenTelemetry ingestion per pod against its baseline. A spike is the same signal as a token spike ([Chapter 07](../playbook/07-devops-automation.md#ai-in-operations-the-third-ai-dlc-phase)).
- Check the revisit triggers in [ADR 0027](../docs/adr/0027-opentelemetry-contract-and-cloudwatch-omni-default-backend.md).
