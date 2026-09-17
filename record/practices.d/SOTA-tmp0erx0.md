---
status: Proposed
promote_when: >-
  A behavioural result rather than an attribution one: a model trained on a
  corpus containing a relation in one order only, evaluated in both
  directions, against one trained on a corpus carrying both orders. A
  pretraining or instruction-data report saying it deliberately generated the
  reverse direction of its factual statements would also move it. What would
  not move it: another influence-attribution study showing the same asymmetry,
  which restates the mechanism without testing the consequence.
title: 'State a relation in both orders in the training corpus if you want it usable in both directions'
version: 1
consensus: unassessed
consensus_note: >-
  One group, and the finding is an attribution result rather than a
  behavioural one, so there is nothing yet for the field to have agreed or
  disagreed with. No data report in this record says anything about the
  internal ordering of statements in its corpus, either way.
tags:
- data-pipeline
- analysis-and-evaluation
date: '2026-09-17'
source:
- LIT-tmpmgsal
introduced_by:
- LIT-tmpmgsal
implementations: []
summary: >-
  Grosse et al. (2023), [LIT-tmpmgsal](../literature.d/LIT-tmpmgsal.md) — a training sequence influences a
  completion only when the phrase related to the prompt comes before the
  phrase related to the completion. Identical content in the reverse order
  scores barely above an unrelated baseline.
---

# SOTA-tmp0erx0: State a relation in both orders in the training corpus if you want it usable in both directions

## Source

Grosse et al. (2023), [LIT-tmpmgsal](../literature.d/LIT-tmpmgsal.md) — [ARXIV-2308.03296](https://arxiv.org/abs/2308.03296).

## What was measured

Synthetic training sequences were constructed for two queries about fictional
entities — the first President of the Republic of Astrobia, and the
composition of a substance called Gleem — and for an English→Mandarin
translation query, and their influence on the model's completion was measured
directly.

**A sequence counts only when the prompt-related phrase precedes the
completion-related one.** Reversing the order while holding the content
*identical* collapses the influence: for the translation query, a
Mandarin-then-English sequence scores **0.030**, against **0.020** for a
sequence containing no English at all. The signal from the reversed sequence
is barely distinguishable from the signal from an unrelated one. Consistent
across model sizes.

## Why the corpus is where this has to be fixed

The effect is not a quirk of prompting, and it is not something a retrieval
step patches. If a sequence in the *training data* teaches only the direction
it was written in, then the ordering of statements inside documents is a
corpus property with consequences, and the only place to act on it is when the
corpus is built.

Concretely: a knowledge base rendered to text as `X is the Y of Z` throughout
teaches `X → Y of Z` and does not teach `Y of Z → X`. Generating the reverse
rendering is cheap and mechanical wherever the relation is structured, which
is exactly where this kind of systematic one-directionality arises.

## The gap between the evidence and the instruction

**Influence is not accuracy.** What was measured is which training sequences
the model's completion can be attributed to, not whether a model trained on a
one-directional corpus fails to answer the reverse question. The inference
from the first to the second is natural and is an inference, and the
`promote_when` above is what would close it.

**And the attribution estimate has its own caveat.** Per [THEORY-tmpz2g03](../theory.d/THEORY-tmpz2g03.md),
influence functions on neural networks estimate the proximal Bregman response
function rather than the effect of removing the sequence and retraining. The
asymmetry is a real property of that estimate. Whether it is a property of
what the model learned is the same question as the paragraph above, arrived at
from the method's side.

## Conditions

**Twenty-eight `data-pipeline` practices and none of them is about what is
inside a document.** <!-- inactive-ok-block: SOTA-239 — Proposed, and cited for the axis distinction this practice
     turns on: document order versus clause order. The distinction holds whatever status that
     practice settles at. -->
They govern what to include, in what proportion
(`SOTA-238`), and in what order the documents arrive (`SOTA-239`). This one is
about the order of clauses *within* a sequence, which is a fourth thing and
the reason it is filed separately rather than folded into the ordering
practice.

**The cost is not symmetric with the benefit.** Duplicating every factual
statement in both directions inflates a corpus and interacts with everything
the record says about deduplication and repetition — `SOTA-164`, `SOTA-171`.
The instruction is worth acting on where a relation is *structured and
generated*, and is not an argument for rewriting prose.

**Evidence is one model series, up to 52B, pretrained only.** No fine-tuning,
and MLP parameters only.
