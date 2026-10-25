VERDICT: PASS

# UI design review — 001-software-factory-vocabulary, round 2

No round-1 UI review exists (only `review-human.md`, whose one blocking finding, rebase onto main, is fixed). The ADR, the table row, and the glossary entry follow the house format: sentence-case H2s, no code blocks or Mermaid touched, and no callouts added.

- [note] `playbook/01-ai-dlc-methodology.md:82` — the Software factory What changed cell runs to about 65 words and four clauses. Other cells top out around 40. It still renders as a single readable row and carries the scope line the spec requires, so it is not worth a round. If the row grows again, move detail into the glossary and the skill link.
- [note] `docs/adr/0026-software-factory-for-maintaining-this-repo.md:1` — the H1 is long (about 20 words) and wraps on GitHub. ADR 0025 is similarly long, so it is consistent with the log. The References link text in `playbook/01-ai-dlc-methodology.md:169` shortens the title, as the other chapters do.
