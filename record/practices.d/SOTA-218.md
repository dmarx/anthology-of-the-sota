---
number: 218
status: Active
formerly:
- SOTA-tmpntee6
consensus: unreplicated
consensus_note: >-
  One paper, but an unusually large one: 71 million training runs across seven
  workloads and four optimizers, built to answer this question and no other.
  Nobody has replicated it at that scale and nobody needs to; what is missing
  is not a second measurement but a second workload family — it predates
  transformer language models.
title: 'Retune the learning rate, momentum and schedule at every batch size you compare, never by a scaling heuristic'
version: 1
tags:
- training-optimization
date: '2026-09-15'
source:
- LIT-058
introduced_by:
- LIT-058
implementations: []
summary: >-
  Linear scaling and square-root scaling are not batch-size rules; they are
  guesses about where the optimum moved, and they hold over a narrower range
  than the comparisons people use them for. A curve of steps-to-target against
  batch size drawn with transferred metaparameters is not a measurement of
  batch size at all — it is a comparison between one tuned configuration and
  several untuned ones, and the point where it bends is the point where the
  heuristic failed.
---

# SOTA-218: Retune the learning rate, momentum and schedule at every batch size you compare, never by a scaling heuristic

## What to do

When comparing batch sizes — for a scaling study, a hardware decision, or a
claim that large batches hurt generalization — tune the learning rate,
momentum and the full schedule *independently at each batch size*. Do not
transfer them by linear scaling, square-root scaling, or holding them fixed.

The corollary for reading other people's curves: a steps-to-result curve that
bends at some batch size is evidence about batch size only if the paper says
it retuned. If it scaled the learning rate linearly instead, the bend is
where linear scaling stopped being right.

## Why

**The heuristics fail, and they fail in the region people use them.** [LIT-058](../literature.d/LIT-058.md)
sweeps seven workloads and four optimizers, and finds no scaling rule that
holds across them: the maximum useful batch size varies from 2^4 to beyond
2^16, and cannot be predicted from any property of the workload it could
identify — not model size, not dataset size, not architecture family.

**Two of its other findings only exist because it retuned.** SGD with momentum
extends the perfect-scaling regime to larger batch sizes than plain SGD —
which is invisible if momentum is held fixed while the batch grows. And the
best batch size depends entirely on which resource is constrained: larger when
the budget is wall-clock steps, smaller when it is epochs. Both are statements
about the tuned optimum moving, and neither survives a heuristic that assumes
it moved somewhere specific.

**This record has practices that were written from papers that did not.**
Several batch-size and warmup entries here descend from work that scaled the
learning rate with the batch and reported the result. They are not thereby
wrong, but their evidence is weaker than it reads, and the reason is this
paper.

## What this does not settle

**It predates transformer language-model pretraining.** The workloads are
image classification, an LSTM and a small transformer on LM1B. The claim is
methodological and should carry; the specific ranges should not be assumed to.

**Retuning is expensive, and the paper is what makes it expensive.** Its own
method — independent tuning at every batch size — is why it needed 71 million
runs. It gives no cheaper procedure, and [LIT-337](../literature.d/LIT-337.md)'s contrary claim, that a
learning rate tuned for SGD transfers unchanged to a compressed variant, is
the kind of thing this practice says to check rather than assume.

**It is in tension with a practice this record does not hold.** LAMB claims
batch-size scaling *without* per-batch-size retuning. That paper is filed and
unreconciled with this one; whichever is right, they cannot both be applied.
