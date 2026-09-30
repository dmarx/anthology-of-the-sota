---
number: 15
status: 'Active'
title: 'Store optimizer states in FP32'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    The stochastic-rounding hedge qualified. This practice said stochastic
    rounding holds accuracy on many workloads; Gopher used it at 280B and
    reported afterwards that it does not fully recover mixed-precision
    performance. One large-scale negative result against a claim that was
    stated without a scale attached.
tags:
- numerics-and-precision
- training-optimization
date: '2026-08-24'
source:
- LIT-011
introduced_by:
- LIT-011
extends:
- SOTA-014
summary: >-
  Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).
---

# SOTA-015: Store optimizer states in FP32

## Source

Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).

## Condition

Same argument as [SOTA-014](SOTA-014.md), one level down: Adam's second moment is a running
average of squared gradients, so it spans a far wider dynamic range than the
weights do, and FP16 cannot hold it. The exponent range runs out before the
mantissa does — small squared gradients flush to zero, ε stops doing its job,
and the effective step size drifts.

## Cost, and what has changed since

8 bytes per parameter for Adam's two moments, on top of the 4 for the master
weights. That is the 12 bytes of optimizer state per parameter that dominates
the memory of a data-parallel run and that ZeRO ([LIT-027](../literature.d/LIT-027.md)) exists to
partition — the reason [SOTA-028](SOTA-028.md) buys as much as it does is that this practice
is being followed.

This is the part of the mixed-precision recipe most actively contested since.
Eight-bit optimizer states, and stochastic rounding in place of
round-to-nearest, both recover most of the memory while holding accuracy on
many workloads. The practice as stated is the conservative default, not a
settled bound.

**The stochastic-rounding half of that has a large-scale negative result
against it.** Gopher ([LIT-617](../literature.d/LIT-617.md)) trained its 7.1B and 280B models with
bfloat16 parameters updated by stochastic rounding, and reports: *"We
subsequently found that stochastic rounding does not fully recover mixed
precision training performance."* Its smaller models used float32 parameters
with bfloat16 activations, so the comparison is between the two recipes
inside one lineage.

That does not overturn "holds accuracy on many workloads" — it names a
workload where it did not, at a scale where the substitution is most
tempting, and the finding is one group's aside rather than an ablation. What
it does is put a scale on a sentence that had none. **A memory optimization
verified at one size is not verified at twenty times that size**, and this is
the specific case the record can now point at.
