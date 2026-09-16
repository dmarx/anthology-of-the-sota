---
status: Proposed
title: 'A note has no topics of its own: it derives them from its paper'
version: 1
tags:
- record
- taxonomy
date: '2026-09-16'
issue: '#142'
summary: >-
  `NOTE.tags` and `NOTE.primary_topic` are derived from the paper the note
  reads. A note and its paper are the same object, so a second copy of the
  subject was a second copy free to disagree — and four of the 158 were.
  Rejected: asserting the agreement with `invariant: tags` on `NOTE.paper`,
  which reports the disagreement instead of making it impossible; and
  declaring an invariant on the other five cross-scheme relations, which join
  a claim to a paper or an explanation and which [ADR-026](ADR-026.md)'s filing rule expects
  to differ.
---

# ADR-tmpvv2d8: A note has no topics of its own: it derives them from its paper

<!-- inactive-ok-file: ADR-026, ADR-035, ADR-036 — all Proposed, and all three
     are the reasoning this one continues rather than rules it leans on being
     in force: ADR-026 is the filing rule the survey below measures against,
     ADR-035 chose `tags` over `primary_topic` for an edge, and ADR-036 read
     the same-scheme findings through and named the four categories. -->

## Context

luria 0.23.0 made it possible to assert a shared field across a scheme
boundary, and this record has six relations that cross one. The first version
of this decision declared `invariant: tags` on `NOTE.paper` and left the other
five alone, on the argument that a note and its paper are **the same object**
while the other five join two things filed on different axes.

The argument was right and the mechanism was wrong. Review:

> given that a note and its paper are the same object, rather than specifying
> an invariant (an "at least one" similarity), I feel like it would be more
> appropriate to use a derived field.

If the two ends are the same object, the note should not *assert* a similarity
to its paper. It should not have a subject of its own at all. `NOTE.published`
has been derived from `paper` since [#119](https://github.com/dmarx/anthology-of-the-sota/issues/119) for exactly this reason, and the
argument does not stop at the date.

## Decision

**`NOTE.tags` and `NOTE.primary_topic` are derived from `paper`.**

    tags:
      derive: '{tags}'
      from: paper
      many: true
    primary_topic:
      derive: '{tags[0]}'
      from: paper

A note carries no `tags:` line; writing one is a lint violation, like
`published:`. To change what a reading is filed under, retag the paper.

Three details that are load-bearing rather than incidental:

- **`many` says this holds the paper's whole list**, and luria checks it
  against LIT. Omitting it used to be silent — the value resolved as a list
  against a contract saying one value, which reads as *no* values, and every
  `docs/notes/tags/*.md` page stopped being written. That is [LU-#276](https://github.com/dmarx/luria/issues/276), fixed in
  0.24.0, and this record is the case it was found on.
- **`primary_topic` follows `paper` too**, not this document's own derived
  `tags`. Derivations do not chain — one hop, reading written frontmatter — so
  a primary derived from a derived list resolves to nothing on every note.
- **`NOTE.paper` declares no `invariant`.** With the tags derived it could
  never fire, and a check that cannot fire is worse than none.

**No cross-scheme relation in this record asserts an invariant**, and the
survey is why. Measured over all six before any change:

| relation | joins | unbound on `tags` |
|---|---|---|
| `NOTE.paper` | a reading → the paper read | 4 / 158 (3%) |
| `SOTA.introduced_by` | a practice → the paper that first stated it | 45 / 220 (20%) |
| `THEORY.source` | an explanation → its paper | 4 / 19 (21%) |
| `SOTA.source` | a practice → its evidence | 67 / 298 (22%) |
| `SOTA.contested_by` | a practice → a paper against it | 4 / 13 (31%) |
| `SOTA.explained_by` | a practice → why it works | 7 / 15 (47%) |

The other five join **two things this record files on different axes on
purpose**. [ADR-026](ADR-026.md)'s rule: a practice takes the topic of *the claim it
makes*, a paper takes the topic of *what it is about*. A practice extracted
from a vision paper about a training technique is `training-optimization`
under a `vision-and-graphics` source, and that is the rule working.

`explained_by` settles it at 47%: a THEORY is pulled toward
`analysis-and-evaluation` by the vocabulary itself — *"theory, interpretability
and debugging belong here too"* — while the practice it explains is filed by
subject. [ADR-036](ADR-036.md) already named this as the third of its four categories over
the same-scheme chains, and all seven findings are that.

## Alternatives considered

- **Assert the agreement with `invariant: tags` on `NOTE.paper`.** What this
  decision replaced. It reports a disagreement that should not have been
  possible, and it leaves the note's tags as a second home for a fact with one
  source — which is [ADR-089](https://github.com/dmarx/luria/blob/main/record/decisions.d/ADR-089.md)'s argument upstream and the reason `published:`
  is already derived. A report is the right shape for a judgement call; this
  is not one.
- **Derive the tags and keep the invariant as belt and braces.** It can never
  fire, so it would say the record checks something it does not.
- **Declare an invariant on `source` and `introduced_by` too.** 20-22% is not
  an absurd rate, and these are the relations the unbound-lineage report was
  imagined for. It loses on what the findings *are*: read individually in
  [LU-#272](https://github.com/dmarx/luria/issues/272) they were four kinds — multi-topic model reports, practices resting
  on analysis papers, the domain-vs-kind filing rule working as designed, and
  a minority of genuine mis-filings. A check whose majority finding is the
  record doing what it decided to do trains the reader to skip the report,
  which costs the minority that were real.
- **Declare it on `contested_by` alone.** The best constructional argument of
  the five — a paper cannot contest a practice without being about the same
  thing. Thirteen edges cannot distinguish a 31% rate from a 15% one, so the
  honest answer is not enough evidence. Revisit if it grows.
- **Use `primary_topic` rather than `tags` for the derivation.** Both are
  derived, so this is a question about what a note's tag *list* is. The paper's
  whole list, because a note's index entry should sit under everything its
  paper does — anything narrower would make browsing the readings disagree
  with browsing the papers, which is the class of disagreement this decision
  is removing.
- **Status quo.** The note keeps its own tags, four of them contradict their
  papers, and nothing says so.

## Consequences

`tags:` is dropped from all 158 notes and from `record/notes.d/_template.md`.
The reading list's tag pages are now a projection of the papers', which is
what they always claimed to be.

**The four disagreements had to be resolved in this contribution, not after
it.** Under the invariant they were findings that could wait; under the
derivation the note simply adopts the paper's tag and the evidence
disappears — and two of them are the only reason anyone noticed the *paper*
was wrong. Each is fixed by reading the record's own note, and each keeps the
old topic rather than replacing it:

- **[LIT-014](../literature.d/LIT-014.md)** *Visualizing the Loss Landscape* — `model-stability` added
  beside `analysis-and-evaluation`. [NOTE-008](../notes.d/NOTE-008.md) filed it under stability and the
  paper is both: filter normalization is a measurement method, and what it
  establishes is why skip connections are needed at depth. [THEORY-011](../theory.d/THEORY-011.md) reads
  it as the stability result.
- **[LIT-024](../literature.d/LIT-024.md)** multi-query attention — `attention-techniques` made primary,
  `model-architecture` kept second. [NOTE-016](../notes.d/NOTE-016.md) filed it under attention and
  [ADR-026](ADR-026.md)'s rule agrees: the claim is most about an attention variant.
- **[LIT-096](../literature.d/LIT-096.md)** *Segment Anything* — `data-pipeline` added beside
  `vision-and-graphics`. [NOTE-018](../notes.d/NOTE-018.md) says why in its own words: *"nothing in the
  loop is about masks"*. The model is the segmentation contribution, the
  three-stage data engine is the transferable one.
- **[LIT-112](../literature.d/LIT-112.md)** vLLM and PagedAttention — `inference-optimization` made
  primary, `attention-techniques` kept second. The blurb names serving-time
  cache layout in as many words, and the title says serving.

Two of the four are reorderings and two are additions, and the rule is the
same one for both: [ADR-026](ADR-026.md)'s — the topic the claim is most about goes first.
Applied honestly to each, it agrees with what the reader of that paper
independently chose in exactly the two cases where the paper was wrong read
alone, which is the evidence rather than a coincidence.

This is not [#101](https://github.com/dmarx/anthology-of-the-sota/issues/101)'s move. That bound a pair by giving both documents a
`flash-attention` tag invented for the purpose, which [ADR-036](ADR-036.md) calls
*satisfying the check rather than answering it*. Here every added topic is one
of the thirteen, chosen independently by a reader of that paper before any
check existed.

**`docs/reports/unbound-lineage.md` goes back to 22 unbound relations** — the
two same-scheme chains', unchanged — and the `NOTE.paper` rows are gone
because the disagreement they reported is now unrepresentable.

Left open: a note can no longer say the paper is filed wrong. That was never
its job, and it was doing it by accident, but it was the only mechanism the
record had for noticing — and four of 158 is a rate worth having had. What
replaces it is that retagging a paper now moves its reading automatically,
so the cost of fixing one is lower than the cost of noticing one used to be.
