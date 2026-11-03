# Product description (and project product description)

**Purpose:** defines a product clearly enough to be built, assessed for quality and accepted. Agree it *before* work starts (focus on products).

## Product description

| | |
|---|---|
| **Created** | IP (for the project plan) or SB (for the stage plan); optionally MP |
| **Prepared by** | PM, with specialist and user input |
| **Approved by** | Board or the delegated role, as part of the plan approval |

### Composition

- Identifier and title
- Purpose
- Composition: its parts
- Derivation: what it is derived from
- Format and presentation
- Development skills required
- **Quality specifications**: measurable criteria the product must meet
- **Quality tolerance**: acceptable range per specification
- **Quality method**: how each specification is checked (review, test, eval, inspection)
- Quality skills required
- Quality responsibilities: producer, reviewer(s), approver(s)

## Project product description

| | |
|---|---|
| **Created in** | SU (in the project brief); refined in IP |
| **Approved by** | Project board |

### Composition (project product)

- Title and purpose
- Composition: the major products the project delivers
- Derivation
- Development skills required
- **Customer quality expectations**: in the users' words
- **Acceptance criteria**: prioritised and measurable, covering performance, usability, maintainability, security, sustainability and so on
- Project-level quality tolerances
- Acceptance method and acceptance responsibilities: who confirms acceptance at closure

## Quality criteria (both)

- Every quality specification is measurable and has a method and a responsible reviewer.
- The purpose explains why the product is needed, not just what it is.
- Acceptance criteria are prioritised (for example MoSCoW).
- The author and the approver are not the same person.

**AI notes:**

- A product description doubles as the spec or prompt context for an agent. Write the quality specifications as executable checks where possible: tests, evals, lint rules or schema validation.
- For AI-model products, specify eval datasets, metrics, thresholds, and the conditions under which the model must not be used.
