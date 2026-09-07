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

**[The record](tags/record.md)** (11) — what the schemes hold, and the rules between them:
[001](../../record/decisions.d/ADR-001.md) · [002](../../record/decisions.d/ADR-002.md) · [004](../../record/decisions.d/ADR-004.md) · [009](../../record/decisions.d/ADR-009.md) · [010](../../record/decisions.d/ADR-010.md) · [011](../../record/decisions.d/ADR-011.md) · [012](../../record/decisions.d/ADR-012.md) · [013](../../record/decisions.d/ADR-013.md) · [014](../../record/decisions.d/ADR-014.md) · [015](../../record/decisions.d/ADR-015.md) · [016](../../record/decisions.d/ADR-016.md)

**[Taxonomy](tags/taxonomy.md)** (1) — the topic vocabulary and what enforces it:
[003](../../record/decisions.d/ADR-003.md)

**[Mechanism](tags/mechanism.md)** (9) — identifiers, generation, the lint:
[005](../../record/decisions.d/ADR-005.md) · [007](../../record/decisions.d/ADR-007.md) · [009](../../record/decisions.d/ADR-009.md) · [010](../../record/decisions.d/ADR-010.md) · [011](../../record/decisions.d/ADR-011.md) · [012](../../record/decisions.d/ADR-012.md) · [014](../../record/decisions.d/ADR-014.md) · [015](../../record/decisions.d/ADR-015.md) · [016](../../record/decisions.d/ADR-016.md)

**[Migration](tags/migration.md)** (3) — moving off the YAML registry, and what happens to it:
[001](../../record/decisions.d/ADR-001.md) · [006](../../record/decisions.d/ADR-006.md) · [008](../../record/decisions.d/ADR-008.md)

**[Workflow](tags/workflow.md)** (1):
[013](../../record/decisions.d/ADR-013.md)

**By status:** [Active](statuses/Active.md) (13) · [Proposed](statuses/Proposed.md) (2) · [Deferred](statuses/Deferred.md) (0) · [Superseded](statuses/Superseded.md) (1) · [Rejected](statuses/Rejected.md) (0)

## Chronological

What the status column means in this scheme — the words are luria's, the meanings are this project's.

| Status | | Means |
|---|---|---|
| `Active` |  | In force — the current answer, and what a citation should normally point at |
| `Proposed` |  | Not in force yet — an open question, so citing it as settled is what the reference report catches |
| `Deferred` |  | Not in force and not being worked on; the question is real and the answer waits on something |
| `Superseded` |  | No longer in force because something replaced it; the successor is named in the field, not in the prose |
| `Rejected` |  | No longer in force and nothing replaced it — kept because a rejection is worth being able to point at |

| # | Title | Summary | Status |
|---|---|---|---|
| [ADR-001](../../record/decisions.d/ADR-001.md) | Keep the anthology in a Luria record rather than in YAML the build reads | The YAML already modelled a knowledge record — statuses, supersession, an attic, a topic taxonomy — but nothing checked any of it, and three of the four were provably inert. Adopting Luria keeps the model and attaches the checks. Rejected: writing bespoke validators against the existing schema, which is the same work without the generated views or the citation graph. | Active |
| [ADR-002](../../record/decisions.d/ADR-002.md) | Separate papers from practices, so each can have its own status | `attic` and `experimental` were fields on a paper, but what they qualified was a recommendation — so a paper could not be sound while its advice was stale, or retired while a practice drawn from it still held. Two schemes, two status fields, and the relationship between them a citation the lint can follow. Rejected: one scheme with a `kind:` field, which keeps the collision. | Active |
| [ADR-003](../../record/decisions.d/ADR-003.md) | Apply the topic consolidation and let the config enforce one primary topic | A 2024 document specified a 22-to-7 topic consolidation with real rules, was never applied, and could not be cited. It becomes this decision; the seven categories become `tags.yaml`; the one-primary-topic rule becomes a `tag_groups` constraint the lint checks. The reading list gets five extra categories the practice registry never needed. | Active |
| [ADR-004](../../record/decisions.d/ADR-004.md) | Retire work by changing its status, never by deleting it | The attic was already this idea, held in a nested `attic:` mapping that nothing could resolve or check. It becomes the `Rejected` and `Superseded` statuses, with the reason kept and the successor named as a followable code. Rejected: deleting retired entries, which is what makes a "living document" quietly unfalsifiable. | Active |
| [ADR-005](../../record/decisions.d/ADR-005.md) | Replace the derived MLR identifiers with sequential codes | `MLR-2014-Kingma001-0001` was computed from author, year and position, so it was stable only while those were, and `topic_id` was a slug of the recommendation's first five words — an identity that changed when you fixed a typo. Sequential codes with the title in frontmatter instead. | Active |
| [ADR-006](../../record/decisions.d/ADR-006.md) | Generate the registry from the record instead of checking it in | `registry.yaml` and `REGISTRY.md` are already derived from `research.yaml` and committed as though they were sources. Once the record is ground truth they should be built from it as artifacts for the frontend. Proposed, not Active: the inversion is phase 4 and the frontend contract has not been checked yet. | Superseded — by [ADR-008](../../record/decisions.d/ADR-008.md); by [ADR-008](../../record/decisions.d/ADR-008.md), which retires the pipeline rather than inverting it |
| [ADR-007](../../record/decisions.d/ADR-007.md) | One workflow commits generated files, and it marks its commits to skip CI | Two workflows regenerated and committed to the same branch, and the second one landed after the job that linted the first — leaving the branch tip unchecked and opening a gated run nobody approves. Generation is now one job whose commit carries the skip marker. Rejected: keeping both and marking the generated files unscannable, which treats the symptom. | Active |
| [ADR-008](../../record/decisions.d/ADR-008.md) | Retire the registry pipeline and publish the record itself | [ADR-006](../../record/decisions.d/ADR-006.md) proposed generating registry.yaml from the record so the frontend could keep consuming it. Publishing the record directly is simpler and removes the projection rather than inverting it: luria stages the record as a site, so the registry builder, REGISTRY.md and the bespoke frontend all retire together. Supersedes [ADR-006](../../record/decisions.d/ADR-006.md). | Active |
| [ADR-009](../../record/decisions.d/ADR-009.md) | Require a source of any kind for a note, not an arXiv identifier | `LIT` required `arxiv:`, and the first technical report worth filing had never been posted there. The requirement is now a field group — at least one of `arxiv:`, `doi:`, `url:` — with a DOI remote so the second kind resolves like the first. Rejected: filing the report under its parent paper's id, which cites the wrong document; and dropping the requirement, which is [DP-001](../../docs/design-principles.md#dp-1)'s failure mode. | Active |
| [ADR-010](../../record/decisions.d/ADR-010.md) | A practice names every source it rests on, not one | `source:` held a single code while practices routinely leaned on several papers — [SOTA-132](../../record/practices.d/SOTA-132.md)'s body cites seven and its field named one — so the structured field disagreed with the prose and only the prose was true. It is now a list. Rejected: keeping one source and a `see also` convention, which is the state that hid 39 unsourced practices; and a separate `corroborated_by:`, which asks filers to grade evidence they have not weighed. | Active |
| [ADR-011](../../record/decisions.d/ADR-011.md) v2 | Lineage between documents is a field, not a paragraph repeated in every note | Ten named chains — schedule, residual, Muon, sparse-attention — are the record's most-cited content and exist only as prose, re-described in each participating note, so they drift: two notes both claimed a comparison did not exist and both were wrong on the same day. Proposes `extends:` and `compared_against:` alongside the existing `superseded_by:`, with the chain as a generated view. | Active |
| [ADR-012](../../record/decisions.d/ADR-012.md) | A practice declares its altitude, and one with no body cannot claim to be a design decision | "Pin memory for CPU-GPU transfers" and "Use Muon in place of AdamW" are both `SOTA` documents with equal standing, and 103 of 144 practices have no body at all — the registry's apparent weight is mostly one synthetic note's bullet lists. Proposes a `kind:` field and a lint tying substance to altitude. | Proposed |
| [ADR-013](../../record/decisions.d/ADR-013.md) | Codes are allocated at merge, not at filing | Two branches open the same afternoon both minted [LIT-144](../../record/literature.d/LIT-144.md) and [LIT-145](../../record/literature.d/LIT-145.md) for different papers, and the collision was caught by hand. Luria has `allocate = "merge"` and temporary codes for exactly this; the record adopts it. Rejected: reserving ranges per contributor, and merging often enough to avoid overlap. | Active |
| [ADR-014](../../record/decisions.d/ADR-014.md) v2 | A provisional status must say what would change it, and the condition names a kind of evidence | Four of 144 practices state a promotion condition, all in prose, none of them re-read when the evidence arrived. Two practices filed a day apart carried near-identical conditions, both were satisfied by the same paper on the same day, and only one promoted — because the condition counted papers when what mattered was what the papers were about. Adopts a required `promote_when:` on every non-active practice, phrased as a kind of result rather than a count of them. | Active |
| [ADR-015](../../record/decisions.d/ADR-015.md) | What the field thinks is a second axis, and this record's endorsement is not it | mHC is shipped at 1.6T in a production model, attacked by two independent groups within a month, and `Proposed` here — three facts crushed into one field, because `status:` is this record's editorial position and has no room for the field's. Adds a defaulted `consensus:` vocabulary, orthogonal to status, and declares practice-level lineage so an agreed trunk and its disputed forks stop rendering identically. | Active |
| [ADR-016](../../record/decisions.d/ADR-016.md) | Contested is a claim about specific other work, so it must name it | [ADR-015](../../record/decisions.d/ADR-015.md) gave the record a way to say the field is arguing about a practice and no way to say who is arguing. The reason lived in `consensus_note:`, which is rendered nowhere and so — by Luria's own rule for what counts as prose — carries bare, unlinkable codes. Adds `contested_by:`, a checked LIT reference required exactly when `consensus: contested`, on the ground that contested is the only value on the axis that asserts a specific other document exists. | Proposed |

