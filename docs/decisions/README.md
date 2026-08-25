# Decisions

How this anthology is built and why — as opposed to what it says about
training models, which is [the practices](../practices/README.md).

Most of these were made years ago and written down for the first time during
the record migration. That is the honest account: the attic existed, the
identifier scheme existed, the topic consolidation had been specified and
never applied. None of them could be cited, so none of them could be
argued with.

A decision whose **choice** changes is superseded by adding a new one and
flipping the old one's status — not by rewriting its body. Values these cite
live in [design-principles.md](../design-principles.md).

File one with `luria new adr`.

<!-- GENERATED below this line by `luria index` — edit README.stub instead. -->

## By tag

**[The record](tags/record.md)** (3) — what the schemes hold, and the rules between them:
[001](../../record/decisions.d/ADR-001.md) · [002](../../record/decisions.d/ADR-002.md) · [004](../../record/decisions.d/ADR-004.md)

**[Taxonomy](tags/taxonomy.md)** (1) — the topic vocabulary and what enforces it:
[003](../../record/decisions.d/ADR-003.md)

**[Mechanism](tags/mechanism.md)** (1) — identifiers, generation, the lint:
[005](../../record/decisions.d/ADR-005.md)

**[Migration](tags/migration.md)** (2) — moving off the YAML registry, and what happens to it:
[001](../../record/decisions.d/ADR-001.md) · [006](../../record/decisions.d/ADR-006.md)

## Chronological

| # | Title | Summary | Status |
|---|---|---|---|
| [ADR-001](../../record/decisions.d/ADR-001.md) | Keep the anthology in a Luria record rather than in YAML the build reads | The YAML already modelled a knowledge record — statuses, supersession, an attic, a topic taxonomy — but nothing checked any of it, and three of the four were provably inert. Adopting Luria keeps the model and attaches the checks. Rejected: writing bespoke validators against the existing schema, which is the same work without the generated views or the citation graph. | Active |
| [ADR-002](../../record/decisions.d/ADR-002.md) | Separate papers from practices, so each can have its own status | `attic` and `experimental` were fields on a paper, but what they qualified was a recommendation — so a paper could not be sound while its advice was stale, or retired while a practice drawn from it still held. Two schemes, two status fields, and the relationship between them a citation the lint can follow. Rejected: one scheme with a `kind:` field, which keeps the collision. | Active |
| [ADR-003](../../record/decisions.d/ADR-003.md) | Apply the topic consolidation and let the config enforce one primary topic | A 2024 document specified a 22-to-7 topic consolidation with real rules, was never applied, and could not be cited. It becomes this decision; the seven categories become `tags.yaml`; the one-primary-topic rule becomes a `tag_groups` constraint the lint checks. The reading list gets five extra categories the practice registry never needed. | Active |
| [ADR-004](../../record/decisions.d/ADR-004.md) | Retire work by changing its status, never by deleting it | The attic was already this idea, held in a nested `attic:` mapping that nothing could resolve or check. It becomes the `Rejected` and `Superseded` statuses, with the reason kept and the successor named as a followable code. Rejected: deleting retired entries, which is what makes a "living document" quietly unfalsifiable. | Active |
| [ADR-005](../../record/decisions.d/ADR-005.md) | Replace the derived MLR identifiers with sequential codes | `MLR-2014-Kingma001-0001` was computed from author, year and position, so it was stable only while those were, and `topic_id` was a slug of the recommendation's first five words — an identity that changed when you fixed a typo. Sequential codes with the title in frontmatter instead. | Active |
| [ADR-006](../../record/decisions.d/ADR-006.md) | Generate the registry from the record instead of checking it in | `registry.yaml` and `REGISTRY.md` are already derived from `research.yaml` and committed as though they were sources. Once the record is ground truth they should be built from it as artifacts for the frontend. Proposed, not Active: the inversion is phase 4 and the frontend contract has not been checked yet. | Proposed |

