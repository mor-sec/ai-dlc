---
owner: platform-enablement
audience: engineering leaders, champions, community of practice coordinators
reviewed: 2026-09-24
review-cadence: quarterly
---

# FAQ Template

The shape of the organization's AI-DLC FAQ: the written answers to the questions and objections people actually raise, held once and linked to rather than re-argued. Audience: the champions and coordinator who maintain it, and everyone who reads it. Why it exists and how it is used: [Chapter 12, Handling the hard objections](../playbook/12-adoption-strategy.md#handling-the-hard-objections).

Where it lives: `docs/faq.md` in the steering repo, next to the narrative and the experiment register, so an agent can answer from it too. Anyone may propose an entry by PR; the coordinator merges.

The rule that makes it work: **every entry quotes a question someone actually asked** ([Chapter 12](../playbook/12-adoption-strategy.md#tips--tricks)). An invented FAQ answers questions nobody has and misses the ones they do. Chapter 12's objections are the right starting point only because they are asked in almost every organization; replace them with your own askers' wording as soon as you hear it.

---

```markdown
# AI-DLC FAQ — <organization>

Last reviewed: <yyyy-mm-dd> by <coordinator>. Ask a new question in
<channel>; any answer given twice there becomes an entry here.

## <Theme, e.g. "Jobs and roles">

### "<The question, verbatim, as it was asked>"

- Asked by: <role or team, not a name, unless they agree> · <yyyy-mm-dd> · <where: brown bag, 1:1, channel>
- Times asked since: <n>

<The answer in plain language, three to six sentences. Say what the program
intends and what it does not; if something is undecided, say that. Link to
the evidence rather than asserting it.>

Evidence: <links to playbook chapters, the pilot charter, metrics, ADRs>
Answer owner: <who can speak to this with authority, e.g. the sponsor>

### "<Next question>"

…

## Questions we cannot answer yet

| Question | Why not yet | Who is deciding | Expected by |
|---|---|---|---|
| "<verbatim>" | <…> | <…> | <date> |
```

---

**Seed themes**, each linked to where the playbook already answers it, to be replaced with local wording:

| Theme | Where the playbook answers it |
|---|---|
| Headcount and roles | [Chapter 12, Handling the hard objections](../playbook/12-adoption-strategy.md#handling-the-hard-objections); [QA's role](../playbook/02-ways-of-working.md#the-ai-pod) |
| Quality of AI-written code | [The validation gates](../playbook/01-ai-dlc-methodology.md#the-validation-gates); [Testing under AI-DLC](../playbook/02-ways-of-working.md#testing-under-ai-dlc) |
| "We tried a tool and got 10%" | [Chapter 01 anti-patterns](../playbook/01-ai-dlc-methodology.md#anti-patterns) |
| Regulated or legacy domains | [Chapter 10](../playbook/10-legacy-modernization.md); [Appendix B](../playbook/appendix-b-rules-from-legislation.md) |
| Data and IP | [Data in context and generated-code ownership](../playbook/06-security-shift-left.md#data-in-context-and-generated-code-ownership); [Vendor governance](../playbook/03-tooling-strategy.md#vendor-governance) |
| Agents acting unattended | [Agent autonomy levels](../playbook/03-tooling-strategy.md#agent-autonomy-levels) |
| How performance is measured | [Metrics reference, what is not measured](metrics-reference.md#what-is-not-measured) |

**Maintenance checklist** (coordinator, monthly):

- [ ] Every entry has a real asker and a date
- [ ] Entries asked again this month have their counts updated; the top five appear in the monthly digest
- [ ] "Cannot answer yet" rows past their date are chased with the named decider
- [ ] Answers still match the playbook; broken or stale links fixed
