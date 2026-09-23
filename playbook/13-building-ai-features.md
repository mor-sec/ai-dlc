---
owner: platform-enablement
audience: architects, developers, product owners, QA
reviewed: 2026-09-24
review-cadence: quarterly
---

# 13 — Building AI Features

Chapters 01 to 12 are about AI building the software. This chapter is about software that contains AI: a product feature that calls a language model to summarize, classify, extract, search, answer, or act. Everything else in the playbook still applies to these features, including the bounded contexts, the gates, and the security controls. This chapter covers what is different, because the usual tools of correctness (a deterministic function and an assertion on its output) do not hold. Prototyping these features on governed data is in [Chapter 05](05-rapid-prototyping.md); this chapter is for building and running them in production.

## Why AI features are different

- **The prompt is code.** It decides behaviour as much as any function does, so it lives in the repo, is reviewed in PRs, and belongs to the bounded context that owns the feature. The model identifier and its parameters are configuration, pinned and changed in the same PR as the prompt they were tested with.
- **Behaviour is a distribution, not a value.** The same input can produce different outputs, and a single correct run proves little. Tests assert properties over a set of cases, not exact strings for one case.
- **Three things change underneath you.** The model (the provider ships a new version), the data (the documents retrieved, what users type), and usage (new kinds of requests). Each can break a feature with no change to the code.
- **Failure is quiet.** A wrong answer written fluently throws no exception and trips no error-rate alert. Unless something checks outputs, the first signal is a customer complaint.

## Keep the model behind the domain

The architecture rules of [Chapter 04](04-architecture.md) contain the model the way they contain any other external dependency:

- **The model call is an adapter.** The domain calls a port named in the ubiquitous language (`SummarizeClaim`, `ClassifyTicket`); the adapter owns the prompt, the model configuration, and the parsing. The domain never handles raw model text, and swapping models is a change to one adapter.
- **Structured output, validated.** The adapter asks for output that matches a schema and validates it; invalid output is retried once, then handled by the fallback. Downstream code only ever sees a valid domain object.
- **Code for what code can do.** Arithmetic, dates, eligibility rules, and anything with a legal or financial answer are computed in code, where they can be tested exactly ([Appendix B](appendix-b-rules-from-legislation.md) shows rules extracted this way). The model handles language: reading, drafting, classifying, summarizing.
- **Every AI feature has a fallback and a kill switch.** A non-AI path (a manual queue, a simpler rule, "not available right now") and a feature flag that switches to it without a deploy ([Chapter 07](07-devops-automation.md#gitops-and-environments)).
- **The product's agents follow the same gate as ours.** A feature that lets a model call tools keeps a human confirmation between reading content and taking a consequential action, the same control [Chapter 06](06-security-shift-left.md#securing-the-agents-themselves) puts on development agents.

## Evals are the test suite

An **eval set** is to an AI feature what the unit tests are to a function: the definition of correct, run on every change. It supplements the ordinary tests of the code around the model; it does not replace them.

- **Where it lives:** `evals/<feature>/` in the owning repo, versioned with the prompt. Start with 50 to 300 cases drawn from realistic inputs (synthetic or masked under the [context classification rules](06-security-shift-left.md#data-in-context-and-generated-code-ownership)), covering common inputs, edge cases, and adversarial ones. Each case has the input, what a correct output must satisfy, and tags for slicing results.
- **Graders, cheapest first.** A **grader** decides whether one output passes one case. Use code first: the output parses, the required fields are present, the cited source exists, no PII appears. Next, comparison against a reference answer. Use a model-graded rubric only for what code cannot judge, such as tone or faithfulness to a source. A model grader is itself checked: record its agreement rate with human labels on a sample, and run it on a model tier at least as strong as the feature's, for the same reason the reviewer never runs below the generator ([Chapter 03](03-tooling-strategy.md#match-the-tier-to-the-task)).
- **Thresholds are acceptance criteria.** "At least 95% of the eval set extracts the correct due date" and "no case returns another customer's data" go in the Unit of Work like any other AC, with numbers ([Chapter 02](02-ways-of-working.md#testing-under-ai-dlc)). Safety and data-leak cases have a threshold of zero failures.
- **The eval gate.** Any PR that touches the prompt, the model configuration, the retrieval, or the parser runs the eval set in CI and attaches the results. The gate blocks on a drop below threshold, or a drop beyond a stated tolerance from `main`. The full set also runs nightly, and in full on any model change.
- **Evals grow from production.** Every bad output a user reports, or online grading flags, becomes a case. This is the same loop as [`lesson-to-steering`](../standards/skills/lesson-to-steering/SKILL.md), applied to the product.

Product evals and [steering evals](../standards/steering-evals.md) are different things. Steering evals test whether the development agent still follows the repo's steering; product evals test whether the feature does its job for users. Both run on model changes; neither substitutes for the other.

## Untrusted input and output in user flows

The prompt-injection row in the [Chapter 06 threat table](06-security-shift-left.md#the-threat-picture-under-ai-dlc) applies to the product as well as to development agents, and a product has more attackers:

- **User content and retrieved documents are data, never instructions.** Injection arrives directly (text a user types) and indirectly (an email, a PDF, a web page, or a support ticket the feature reads). The prompt separates instructions from content, and nothing a document says can widen what the feature may do.
- **Retrieval respects authorization before the model sees anything.** Search results are filtered by the calling user's permissions first. A retrieval index that mixes tenants or permission levels leaks data the first time someone asks the right question.
- **Tools run with the user's permissions.** A feature that calls APIs does so as the calling user, never as a service-wide identity, and actions that move money, delete data, or send messages on the user's behalf need the user's explicit confirmation, handled outside the model's control.
- **Output is untrusted too.** Escape model output before rendering it (it can contain script), validate it before acting on it, and never pass it into SQL, a shell, or a template engine.
- **The threat-model pass adds AI abuse cases.** For any Unit with a model in it: direct and indirect injection, data exfiltration through the answer, cost exhaustion through long or looping requests, and content that breaks policy. Each abuse case becomes an eval case with a zero-failure threshold.

## Operating AI features

- **Log what explains an output.** Per request: prompt version, model identifier, token counts, latency, retrieval sources, grader flags, and the correlation ID ([Chapter 07](07-devops-automation.md#observability-requirements)). Content itself is logged according to its classification; restricted inputs and outputs are not logged raw.
- **Grade production, not just CI.** A sample of live traffic runs through the code graders and, where affordable, the model graders. The pass rate is an SLO with a burn-rate alert, like latency or errors.
- **Capture user feedback as data.** Ratings, edits to generated drafts, and overrides of a classification are the best signal of quality in production. They feed the eval set and the drift alerts.
- **Watch three kinds of drift.** Input drift (new kinds of documents or questions, visible in the tags of failing samples), model drift (a provider update, prevented by pinning versions), and retrieval drift (a stale or growing index). Each has an owner and a signal.
- **Model upgrades are Units of Work.** Pinned model versions are upgraded deliberately: the eval set runs against the candidate, the thresholds must hold, and the change ships behind the feature flag. Provider deprecation dates are tracked under [vendor governance](03-tooling-strategy.md#vendor-governance).
- **A harmful or wrong output at scale is an incident.** Flip the kill switch first, investigate second, and close with a [post-incident review](../standards/post-incident-review-template.md) whose class-level fix is usually a new set of eval cases.

## Cost and latency budgets

Each AI feature has a latency budget and a cost budget per user action, written as non-functional ACs with numbers ([ADR 0013](../docs/adr/0013-non-functional-requirements-as-acceptance-criteria.md)). When a feature is over budget, use the levers in this order:

1. **Shorter, cacheable context.** Put stable instructions first so they can be cached, retrieve less, and summarize history.
2. **Lower effort on the same model**, then a smaller tier for narrow tasks such as classification and extraction. The tier logic is in [Chapter 03](03-tooling-strategy.md#model-selection-and-token-economics); current models and relative costs are in the [model selection reference](../standards/model-selection.md). The eval set decides whether a cheaper configuration is good enough, not a spot check.
3. **Batch what is not interactive.** Overnight enrichment, backfills, and re-indexing go through batch processing.

A product feature that lets the model loop (call a tool, read the result, decide again) caps steps and tokens per user action, for the same reasons as the [autonomy-level caps](03-tooling-strategy.md#agent-autonomy-levels) on development agents. An uncapped loop is a denial-of-service against your own budget. Cost per feature appears in showback next to [cost per validated Unit of Work](03-tooling-strategy.md#unit-economics-cost-per-validated-unit-of-work).

## Where it fits in AI-DLC

| Phase | What changes for an AI feature |
|---|---|
| Inception | The Unit of Work carries eval thresholds as ACs, the fallback behaviour, and AI abuse cases from the threat-model pass. The product owner and QA write the first 20 eval cases in Mob Elaboration, because they know what a good answer looks like. |
| Construction | The Bolt plan's test strategy names the eval set, the graders, and the thresholds. The adapter, prompt, and parser are built together; the eval gate runs on the PR alongside mutation testing and contract tests. |
| Operations | Online grading, feedback capture, drift alerts, and model upgrades as Units. The kill switch is tested like rollback. |
| Prototype | [Chapter 05](05-rapid-prototyping.md) prototypes answer whether the feature is worth building. Promotion requires an eval set with thresholds; a prototype that was only ever tried by hand has no evidence that it works. |

## Anti-patterns

- **Vibe testing.** Five prompts tried in a playground, the output looked good, shipped. The first unusual input finds the failure. No eval set, no merge.
- **The prompt in the admin panel.** Prompts stored in a database and edited live by whoever has access, with no review and no eval run. A prompt change is a code change.
- **The grader nobody checked.** A model grader reporting 97% that agrees with humans 70% of the time. Record grader agreement, and recheck it when either model changes.
- **Model output straight into HTML, SQL, or a shell.** Injection with extra steps. Output is untrusted input.
- **Tenant-mixed retrieval.** One index for all customers, filtered in the prompt ("only answer about this customer's data"). Authorization is enforced before retrieval, in code.
- **The floating model alias.** A configuration that points at "the latest" model, so the provider changes the feature's behaviour overnight. Pin versions; upgrade on purpose.
- **Language models doing arithmetic.** Totals, dates, and eligibility computed by the model because it was convenient. Compute in code, explain in language.

## Tips & tricks

- **Seed the eval set in elaboration.** Twenty cases written by the product owner and QA before any prompt exists define "good" better than a page of requirements, and the agent can build to them.
- **Keep a worst-outputs file.** The ten worst real outputs, with what should have happened. It is the fastest way to explain a feature's risks to a new pod member or a stakeholder.
- **Compare evals case by case, not only in aggregate.** A stable pass rate can hide twenty cases that flipped each way. The PR comment lists the flips.
- **Tag cases by slice** (language, document type, customer segment) so a regression in one slice is visible even when the total holds.
- **Make the fallback good.** Users will see it whenever the kill switch flips or the model is unavailable. A fallback nobody would want to use means the kill switch will never be pulled.

## References

- Decisions: [ADR 0018 — Build AI features with evals, a domain adapter, and a kill switch](../docs/adr/0018-ai-features-evals-adapter-kill-switch.md)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Previous: [Chapter 12 — Adoption Strategy](12-adoption-strategy.md) · Back to the [README](../README.md)
