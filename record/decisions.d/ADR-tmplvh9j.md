---
status: Proposed
title: 'The practice vocabulary takes the kind-of-claim topics the reading list already has'
version: 1
tags:
- ontology
date: '2026-09-08'
---

# ADR-tmplvh9j: The practice vocabulary takes the kind-of-claim topics the reading list already has

## Context

[ADR-003](ADR-003.md) gave the `SOTA` scheme seven topics and the `LIT` scheme those seven
plus five more, on the ground that "the reading list covers ground the
<!-- inactive-ok: ADR-020 — Proposed, named as the decision this one continues; its status is not what is being relied on -->
practice registry does not". [ADR-020](ADR-020.md) then found that sentence true of two of
the five and false of two others, and scoped the recommendations by kind of
claim rather than by domain.

What neither decision did was look at whether the seven are enough. They are
not, and the evidence is already in the record rather than hypothetical.

<!-- inactive-ok-block: SOTA-023 — Superseded, and cited here as an example of where a serving claim was filed, which its status does not change -->
**Seven practices about serving, filed under four different topics:**

| practice | filed as | about |
|---|---|---|
| [SOTA-005](../practices.d/SOTA-005.md) | `model-stability` | running statistics at inference |
| [SOTA-023](../practices.d/SOTA-023.md) | `model-architecture` | multi-query attention for memory bandwidth |
| [SOTA-105](../practices.d/SOTA-105.md) | `attention-techniques` | PagedAttention for batch inference |
| [SOTA-113](../practices.d/SOTA-113.md) | `systems-optimization` | continuous batching |
| [SOTA-115](../practices.d/SOTA-115.md) | `systems-optimization` | prefill/decode overlap |
| [SOTA-163](../practices.d/SOTA-163.md) | `systems-optimization` | microscaling quantization formats |
| [SOTA-185](../practices.d/SOTA-185.md) | `systems-optimization` | error-compensating post-training quantization |

<!-- inactive-ok-block: SOTA-154 — Proposed, cited as an example of where an adaptation claim was filed, which its status does not change -->
**Six about adaptation, across four more:** [SOTA-038](../practices.d/SOTA-038.md) (`model-architecture`),
[SOTA-123](../practices.d/SOTA-123.md) (`data-pipeline`), [SOTA-151](../practices.d/SOTA-151.md) (`attention-techniques`), [SOTA-154](../practices.d/SOTA-154.md) and
[SOTA-184](../practices.d/SOTA-184.md) (`training-optimization`), and the preference-training pair.

A reader who wants to know what this record says about serving has to visit
four pages and guess. That is a category that exists in the corpus and not in
the list, which is the second test in [DP-tmpx90vz](../../docs/design-principles.md#dp-tmpx90vz).

The `LIT` scheme has had the right words for both since [ADR-003](ADR-003.md):
`inference-optimization` and `adaptation-and-tuning`.

## Decision

**Add `inference-optimization` and `adaptation-and-tuning` to
`record/practices.d/tags.yaml`**, taking the practice vocabulary from seven
topics to nine, and retag the thirteen practices above onto them.

Both words are already the `LIT` scheme's, which is the point: where the two
vocabularies name the same *kind of claim*, they should use the same word.
What stays `LIT`-only is `generative-modeling` and `vision-and-graphics`,
<!-- inactive-ok: ADR-020 — Proposed, named as the decision this one continues; its status is not what is being relied on -->
because those name a **domain** rather than a kind of claim, and [ADR-020](ADR-020.md)'s
argument against domain topics is unchanged — a topic spent naming the domain
is a topic not spent naming the claim.

**`analysis-and-evaluation` is not added.** It is the third kind-of-claim word
in the `LIT` extras, and there is no practice in the record that wants it: the
evaluation-adjacent notes (LPIPS, BIG-bench, the lottery-ticket pair) carry no
instruction. Adding a category to hold zero documents is [DP-008](../../docs/design-principles.md#dp-8)'s corollary
run backwards. It goes in the moment a document needs it.

## Alternatives considered

- **Leave the seven and let serving practices scatter.** What has been
  happening, and the scatter is the argument against it. It also produces the
  reverse error this decision is a response to: with no home for a serving
  claim, the reflex is to read a paper about serving as out of scope, which
  is [DP-tmpx90vz](../../docs/design-principles.md#dp-tmpx90vz)'s reading (1).
- **Add one broader topic — `deployment` or similar — covering both.**
  Fewer categories, and it merges two decisions that are made by different
  people at different times: how to adapt a trained model, and how to serve
  one. The `LIT` vocabulary already separates them and nothing has gone wrong
  with that.
- **Add `analysis-and-evaluation` too, for symmetry.** Rejected above: no
  documents.
- **Add a representation or encoding topic.** Deferred, and flagged rather
  than ignored: [LIT-064](../literature.d/LIT-064.md), [LIT-086](../literature.d/LIT-086.md) and [LIT-111](../literature.d/LIT-111.md) all carry input-encoding or
  representation claims with nowhere to go, and the record's existing encoding
  practices are scattered the same way serving was (RoPE under
  `attention-techniques`). The difference is that no practice has been *filed*
  on those yet, so the retagging evidence this decision rests on does not
  exist. The honest move is to file one and see where it wants to live.

## Consequences

`luria lint` enforces exactly one primary topic per practice, so the retagging
is mechanical and checkable, and the tag pages regenerate.

The two new pages will be small at first — seven and six entries — which is
the right size for a category that was already there implicitly.

This is the third decision in a row about the same vocabulary ([ADR-003](ADR-003.md) set it,
<!-- inactive-ok: ADR-020 — Proposed, named as the decision this one continues; its status is not what is being relied on -->
[ADR-020](ADR-020.md) stopped it being read as a domain boundary, this one widens it), and
that is worth naming as a pattern rather than a coincidence: a vocabulary
written once for a corpus of 119 practices is now governing 185 across a wider
subject, and the seven categories were transcribed from a 2024 document that
predates most of what the record now holds. Expect a fourth.
