---
number: 215
status: Proposed
formerly:
- SOTA-tmpb5sfm
promote_when: >-
  The freeze-then-compress structure reproduced on a transformer pretraining
  run by a group other than the authors, or shipped in a mainstream training
  framework. What would not satisfy this: another compressor that works under
  SGD, which says nothing about the adaptive case.
consensus: unreplicated
consensus_note: >-
  One paper, one lab, one model family. The negative half — that naive
  compression of an Adam update fails — is the better-established half,
  because it is a failure the authors had to explain rather than a result they
  set out to get.
title: "Freeze Adam's variance term after a warmup before compressing its update, and never compress the update directly"
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
source:
- LIT-278
introduced_by:
- LIT-278
extends:
- SOTA-214
implementations: []
summary: >-
  Error-compensated compression assumes the residual it carries forward still
  means the same thing next step. Adam's update divides by a running variance,
  which is a non-linearity the correction does not survive — compressing it
  directly corrupts the error cancellation and badly harms convergence. The
  workaround is structural rather than a tuning fix: Adam's variance
  stabilises early, so freeze it after a warmup and the update becomes linear
  enough to compress.
---

# SOTA-215: Freeze Adam's variance term after a warmup before compressing its update, and never compress the update directly

## What to do

Do not apply 1-bit or error-compensated compression to an Adam update as it
stands. Run Adam uncompressed for a warmup period, then **stop updating the
second-moment estimate** and treat it as a fixed preconditioner for the rest
of training; compress what remains, which is a momentum SGD update under a
constant diagonal scaling and does admit error compensation.

Two settings, both from [LIT-278](../literature.d/LIT-278.md): the warmup must be at least as long as
the learning-rate warmup, and the variance-norm ratio
`||v_t||_1 / ||v_{t-delta}||_1 >= 0.96` is usable as an automatic stopping
criterion for it.

## Why

**The failure is about where the compressor sits, not how hard it squeezes.**
Error feedback ([SOTA-214](SOTA-214.md)) carries a residual forward on the assumption
that adding it back next step undoes the loss. Adam divides by a running
`sqrt(v)` that changes between those two steps, so the residual is added back
under a different scaling than the one it was subtracted under, and the
cancellation the method depends on does not happen. This is why the fix is not
a smaller compression ratio.

**The observation that makes it work is empirical and cheap to check.** Adam's
variance term changes rapidly early and then stabilises; after that, freezing
it costs little. The paper reports allreduce consuming 80–94% of step time for
BERT on Ethernet clusters above 8 nodes, which is the regime where this is
worth doing at all.

## What this does not settle

**One lab, one model family, one network fabric.** BERT-scale models on
Ethernet. Whether the variance stabilises the same way in a long
transformer pretraining run, where the data distribution shifts, is untested
here.

**Freezing the variance changes the optimizer.** The practice is presented as
a communication optimization, and it is also a change to what is being
optimized. [LIT-278](../literature.d/LIT-278.md) reports matched convergence; nothing in this record
checks what it does to a run long enough for the preconditioner to go stale.

**The record has a practice this contradicts in spirit.** [SOTA-218](SOTA-218.md) says
not to assume a metaparameter transfers. Freezing `v` is exactly such an
assumption, made deliberately, and it is measured rather than assumed — but
the measurement is one paper's.
