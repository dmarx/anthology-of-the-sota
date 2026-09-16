---
number: 214
status: Active
formerly:
- SOTA-tmp5wyoh
consensus: emerging
consensus_note: >-
  Three papers, three compressors, three mechanisms, one requirement. PowerSGD
  ships in PyTorch's DistributedDataParallel, which is adoption evidence as
  well as measurement; DGC and 1-bit Adam each report the failure directly.
title: 'Pair any gradient compressor with error feedback, and correct the momentum it is applied under'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
source:
# LIT-337 is primary: it states the requirement most sharply -- rank-4
# PowerSGD fails to reach acceptable accuracy on a simple task WITHOUT error
# feedback, and matches uncompressed SGD with it.
- LIT-337
# LIT-056 is the same requirement at extreme sparsity, under a different name:
# momentum correction is error feedback applied to the momentum buffer rather
# than the gradient.
- LIT-056
# LIT-278 is the negative case -- what happens when the compressor is put
# somewhere error feedback cannot reach.
- LIT-278
introduced_by:
- LIT-056
implementations: []
summary: >-
  Compression is lossy and the loss accumulates. Every scheme in this record
  that survives high compression ratios keeps the residual locally and adds it
  back to the next step, and every report of a compressor "not converging"
  that the record holds is a report of that step being skipped: rank-4
  PowerSGD fails on Cifar10 without it, and gradient sparsification at 99.9%
  degrades badly without the momentum-buffer version of it.
extended_by:
- SOTA-215
- SOTA-tmpi7tm2
---

# SOTA-214: Pair any gradient compressor with error feedback, and correct the momentum it is applied under

## What to do

Keep the part of the gradient the compressor threw away. After compressing,
store `residual = g - decompress(compress(g))` locally, and add it to the
next step's gradient before compressing again. When the optimizer has a
momentum buffer, apply the correction to the buffer rather than to the raw
gradient — sparsification delays the coordinates it drops, and delayed
coordinates arrive with stale momentum already applied to them.

Set the rank or ratio second. [LIT-337](../literature.d/LIT-337.md) reports rank 2 sufficient for
convolutional networks and rank 4 for LSTMs; [LIT-056](../literature.d/LIT-056.md) reaches 99.9%
sparsity. Neither number means anything without the residual.

## Why

**The requirement is reported three times, by three compressors, in three
forms.** Low-rank projection: rank-4 PowerSGD "fails to converge to
acceptable accuracy even on simple tasks" without error feedback, and matches
uncompressed SGD with it. Sparsification: Deep Gradient Compression reports
that at 99.9% sparsity, momentum SGD without momentum correction degrades
significantly — because a coordinate held back for hundreds of steps is
applied against a momentum buffer that has moved on. Sign-based compression
with Adam: [LIT-278](../literature.d/LIT-278.md) finds that applying error-compensated
compression to Adam directly "corrupts error cancellation and severely harms
convergence", because Adam's variance division is non-linear and the residual
no longer means what the correction assumes.

That third case is the one that shows what the practice is really about. Error
feedback is not a trick that makes compression work; it is the statement that
the compressor must sit somewhere the residual is still meaningful. Where it
<!-- inactive-ok-block: SOTA-215 — Proposed, and named here as the
     remedy for the one case this practice cannot cover -->
does not, the fix is to move the compressor, which is [SOTA-215](SOTA-215.md).

**It is cheap and it is local.** The residual is one buffer the size of the
gradient, never communicated. There is no coordination cost and no
hyperparameter.

## What this does not settle

**The ranks and ratios are per-architecture and mostly pre-transformer.**
[LIT-337](../literature.d/LIT-337.md)'s own limitations say transformer language models may need
rank 32 or more, and its measurements are ResNet18 and an LSTM on 16 GPUs.
The requirement generalizes; the numbers should not be assumed to.

**Whether compression pays at all is a separate question.** [LIT-314](../literature.d/LIT-314.md)
gives a lower-bound construction showing unbiased compression cannot improve
the uplink and downlink terms simultaneously, which bounds what any of this
buys. This practice says what to do *if* you compress.
