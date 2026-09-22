---
status: Active
promote_when: >-
  The same dissociation shown under a compression method rather than under
  deletion: smallest-decile directions represented at reduced precision
  instead of zeroed, with the damage curve against bit-width reported beside
  the curve against deletion. That would separate "these directions carry
  information" from "these directions cannot be removed", which are different
  instructions for anyone choosing a format. What would NOT meet it: another
  paper reporting that pruning small singular values hurts, or helps. Both
  are already held, and the order of operations that reconciles them is what
  this practice is about.
consensus: unreplicated
consensus_note: >-
  One group, and an unusually well-controlled one: the dissociation is shown
  by three instruments that agree — random-matrix departure, overlap with the
  activation covariance, and benchmark damage — and it reconciles two
  previously conflicting published results by varying only the order of
  pruning and fine-tuning. What no second group has done is repeat it. The
  neighbouring measurement in LIT-tmphxv7m is independent evidence that
  matrices differ, not evidence about this particular claim.
title: 'Do not rank singular directions by magnitude when deciding what to discard; check the small end, and check it after fine-tuning'
version: 1
tags:
- inference-optimization
- analysis-and-evaluation
date: '2026-09-22'
source:
- LIT-tmpmftzj
introduced_by:
- LIT-tmpmftzj
implementations: []
summary: >-
  Staats, Thamm and Rosenow (2024), [LIT-tmpmftzj](../literature.d/LIT-tmpmftzj.md) — in a
  transformer's **non-square** matrices, the smallest singular directions
  carry data directions and their removal is catastrophic: Llama-3 8B on
  GSM8K falls from 43.2% to **2.0%** when the smallest decile of the
  Down-Projection goes, against 40.0% for the same decile of the square
  Attention-Output. And the damage only appears if you prune *after*
  fine-tuning.
---

# SOTA-tmp6xtka: Do not rank singular directions by magnitude when deciding what to discard; check the small end, and check it after fine-tuning

## Source

Staats, Thamm and Rosenow (2024), [LIT-tmpmftzj](../literature.d/LIT-tmpmftzj.md) — read as
[NOTE-tmpsv1p1](../notes.d/NOTE-tmpsv1p1.md).

## When this applies

Whenever you drop or degrade singular directions and choose them by
magnitude: SVD pruning, truncated low-rank approximation, deciding which part
of a decomposition gets the cheap number format. The default assumption it
argues against is Eckart-Young's — that the smallest singular values are the
right ones to lose because losing them changes `‖W′ − W‖₂` least. That is
true about the norm and it is not an argument about the function.

## Do this

**Separate square from non-square matrices before you generalize.** For a
rectangular matrix the Marchenko-Pastur support has a lower edge strictly
above zero, so singular values can sit *below* the bulk as well as above it.
Square matrices cannot produce that, and the two behave differently.

**Measure damage per decile rather than assuming monotonicity.** Zero one
decile of one matrix type across all blocks and evaluate. For square matrices
the damage decreases monotonically from large to small. For non-square ones it
does not.

| Llama-3 8B, GSM8K 3-shot, 43.2% baseline | smallest decile removed |
|---|---|
| Down-Projection (non-square) | **2.0%** |
| Gate-Projection (non-square) | 34.1% |
| Attention-Output (square) | 40.0% |
| Query (square) | 40.3% |

On RULER at 8192 context, removing the smallest decile from all layers scores
**0.0** on all five tasks — indistinguishable from removing the largest.

**Test in the order you will deploy in.** Prune-then-fine-tune and
fine-tune-then-prune give opposite answers on the same model and the same
decile. On BERT across BoolQ, RTE and SST2, pruning first lets fine-tuning
recover the loss; fine-tuning first and then pruning degrades all three
significantly against a 3σ band from six unpruned runs. So a pruning result
measured on a base model does not transfer to an aligned or fine-tuned one.

## What this explains that was previously a contradiction

Two published results disagreed: one found small singular values essential,
another found removing them *improved* reasoning — GPT-J on CounterFact
13.3% → 24.1% off a single layer, [LIT-tmptsr98](../literature.d/LIT-tmptsr98.md). Both are
right. The first fine-tunes before pruning and the second evaluates a
pretrained model without fine-tuning. Varying only that order reproduces both
outcomes in one experiment, which makes the order of operations the finding
rather than either result.

The consequence worth carrying: **fine-tuning writes into the small singular
directions.** If alignment lives there, removing them can raise a task metric
and remove the alignment at the same time, and a reasoning benchmark will not
show you the second thing.

## Why `Active` on one paper

Three instruments inside it agree — departure from the Marchenko-Pastur
prediction, overlap with the activation covariance at 3σ, and benchmark
damage — and they are independent of each other. The instruction that follows
is to run a measurement rather than to adopt a technique, and the measurement
is cheap. A record that waits for replication before telling people to check
something is recommending they not check it.

## Conditions

**Zeroing is not quantizing, and this is the practice's real limit.** Every
result here removes directions outright. Methods that matter mostly represent
them at lower precision instead, and nobody has drawn the damage curve
against bit-width. Read this as "find out what the small end is doing", not
as "the small end cannot be compressed".

**The matrix-type findings are not identical across models.** Llama's
Down-Projection shows no increased activation overlap where Pythia's does; the
authors speculate about GLU placement and leave it open. Treat the square/
non-square split as the robust part and the per-matrix list as indicative.

**Three models, no seeds on the ablations.** BERT, Pythia-410M and
Llama-3.1-8B, one run per cell except the BERT fine-tuning experiment.

**It cuts against a convenience, not against Eckart-Young.** The truncated SVD
really is the optimal low-rank approximation in Frobenius norm. What this
says is that the quantity being optimized was chosen for tractability, and the
model's behaviour is ordered differently. [SOTA-tmpsbgvf](SOTA-tmpsbgvf.md) chooses *how
much* rank per matrix from the magnitude spectrum and is the right companion;
neither replaces the other.

## Known implementations

None. The analysis code is published; no compression pipeline in this record
is known to apply the check.
