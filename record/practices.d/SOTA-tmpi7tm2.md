---
status: Active
consensus: unreplicated
consensus_note: >-
  One paper, and a warmup schedule is the kind of detail that gets reproduced
  by implementation rather than by publication — every DGC implementation
  carries it, nobody has published a second measurement of it.
title: 'Ramp the sparsity ratio up over the first few epochs rather than starting at the target'
version: 1
tags:
- distributed-optimization
date: '2026-09-16'
source:
- LIT-056
introduced_by:
- LIT-056
extends:
- SOTA-214
implementations: []
summary: >-
  Lin et al. (2017), [LIT-056](../literature.d/LIT-056.md). Gradient sparsification delays the coordinates
  it drops; error feedback returns them, but it returns them late. Early in
  training the gradients are large and the trajectory is still choosing where
  to go, so a delay there costs more than the same delay later. Start at a
  low sparsity — the paper ramps 75%, 93.75%, 98.4375%, 99.6%, 99.9% over the
  first few epochs — and reach the target once the run has settled.
---

# SOTA-tmpi7tm2: Ramp the sparsity ratio up over the first few epochs rather than starting at the target

## What to do

When running gradient sparsification, do not begin at the sparsity you intend
to use. Ramp it up exponentially over the first few epochs. [LIT-056](../literature.d/LIT-056.md)'s schedule
is 75%, 93.75%, 98.4375%, 99.6%, then 99.9%.

This is one of two things [LIT-056](../literature.d/LIT-056.md) adds to plain sparsification, and the other
one is already filed: [SOTA-214](SOTA-214.md) is the error-feedback requirement, without
which high sparsity fails outright. This is the schedule on top of it.

## Why

Sparsification does not discard a coordinate; error feedback holds it locally
and sends it once it accumulates past the threshold. So the cost of dropping
a coordinate is a **delay**, not a loss — and a delay is not equally cheap at
every point in training.

Early gradients are large and the trajectory is still choosing a region. And
the delay is not small: [LIT-056](../literature.d/LIT-056.md) reports that at 99.9% sparsity "most of the
parameters are updated every 600 to 1000 iterations", which is long compared
to an epoch. A coordinate held back that long in the early phase arrives as a
step in a direction the optimizer has already left — the same defect as
staleness in an asynchronous scheme, and the paper's own framing is that these
accumulated early gradients "may outweigh the latest gradients and misguide
the optimization direction". Later, when updates are small and the region is
settled, the same delay costs much less.

The warmup is the schedule that makes the delay track that: pay for
communication when the information is worth the most.

## Conditions

**ResNet and LSTM on image and speech benchmarks, 2017.** The schedule is
reported with the momentum correction and the rest of the DGC apparatus and is
not ablated separately from them, so the record does not hold a measurement of
what this alone is worth.

**"A few epochs" presumes epochs.** For a single-pass pretraining run there is
no natural unit here, and the paper gives no rule in steps or tokens.

**The sparsity ramp travels with a learning-rate warmup.** [LIT-056](../literature.d/LIT-056.md)'s
"warm-up training" is both: a less aggressive learning rate *and* a less
aggressive sparsity over the same window. The learning-rate half is standard
and already in this record; what is filed here is the sparsity half, and the
paper does not separate their contributions.

**The warmup window is short and stated in epochs**: 4 of 164 for CIFAR-10, 1
of 40 for Penn Treebank, 1 of 80 for the speech models. [LIT-056](../literature.d/LIT-056.md) calls this
"the only hyper-parameter introduced by Deep Gradient Compression". Table 1
ablates the four techniques together with sparsification; it is not an
isolated measurement of the ramp.

## Known implementations

None recorded. Implementations of DGC carry the schedule because it is part of
the published method, which is adoption of a paper rather than evidence about
the schedule.
