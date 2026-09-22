---
number: 323
status: Proposed
formerly:
- SOTA-tmpaocvh
title: 'Test a claim about what pretraining produces on a model trained with the pretraining objective, not one trained on the task family you are testing'
version: 1
tags:
- analysis-and-evaluation
- in-context-learning
- adaptation-and-tuning
date: '2026-09-22'
source:
- LIT-536
introduced_by:
- LIT-536
contested_by: []
explained_by:
- THEORY-067
promote_when: >-
  A second dispute outside in-context learning is resolved the same way —
  a claim about an emergent capability that survived while the evidence came
  from models trained on the target task, and changed sign or lost support
  once the same measurement was run on models trained only on the general
  objective.
summary: >-
  Shen, Mishra and Khashabi (2023), [LIT-536](../literature.d/LIT-536.md) — "there exist weights such
  that" and "pretraining produces weights such that" are different claims, and
  training a model on the task family you are about to test collapses them.
  Their separation of these as Hypothesis 2 and Hypothesis 1 is what let them
  show that a literature everyone read as evidence about pretrained language
  models had tested neither the models nor the objective.
---

# SOTA-323: Test a claim about what pretraining produces on a model trained with the pretraining objective, not one trained on the task family you are testing

<!-- inactive-ok-file: SOTA-324 — Proposed, the sibling practice filed in this same contribution and named as its counterpart; it is new, not retired. -->

## Source

Shen, Mishra and Khashabi (2023), [LIT-536](../literature.d/LIT-536.md) — ICML 2024. Read as
[NOTE-276](../notes.d/NOTE-276.md).

## The practice

When the claim is *pretraining on a general objective produces a model that
does `X`*, the model you measure must be one trained on that general
objective. If instead you train on sequences drawn from the task family that
`X` names, you have changed two things at once — the space of tasks and, with
it, the inductive bias of the resulting model — and a positive result is
compatible with the claim being false.

State which of the two you are testing:

- **the expressivity claim** — *there exist weights for which the model does
  `X`* — which a construction or a purpose-trained model can establish, and
  which says nothing about what training on the general objective yields;
- **the emergence claim** — *weights arising from the general objective do
  `X`* — which needs a model that was never shown the task family.

Both are worth establishing. Only the second is usually what a reader takes
away, and it is the one that almost never gets tested.

## Why it is `Proposed`

**One source, and the discipline is general while the evidence is one
dispute.** The argument is clean and it is supported by measurements — a
sparsity requirement the constructions need and real models do not have, and
an accuracy-flat/parameters-moving checkpoint sweep showing the capability
belongs to a family of weights rather than a point. But it has been applied
once, to in-context learning, and a methodological practice earns `Active`
by working somewhere its author was not looking. The `promote_when` asks for
exactly that and not for a second paper agreeing with this one, which would
not add evidence ([DP-005](../../docs/design-principles.md#dp-5)).

## Scope

This is not an argument against training a model on a task family to study
it. [LIT-534](../literature.d/LIT-534.md)'s setup is how the mechanism question became answerable at
all, and the results in it are real results about transformers. The practice
is about what a result in that setup licenses you to say about a model
pretrained on text.

Nor is it specific to language models or to in-context learning. The shape —
*capability observed in the wild, reproduced in a purpose-built setting, then
explained from the purpose-built setting* — is common, and each step is
reasonable while the composition quietly substitutes one model family for
another.

## How to tell whether it bit you

The test that made it visible here was not about the objective at all: it was
Theorem 1's observation that in-context learning is sensitive to the order of
its demonstrations and batch gradient descent is not, so no argument about
weights was needed to know the two cannot be equivalent. Look for a property
the claimed mechanism *must* have, check whether the real phenomenon has it,
and do that before building the apparatus that would confirm the mechanism.
That half of the method is filed separately as [SOTA-324](SOTA-324.md).
