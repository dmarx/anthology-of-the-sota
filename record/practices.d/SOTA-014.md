---
number: 14
status: 'Active'
title: 'Maintain master weights in FP32'
version: 1
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-011
extends:
- SOTA-016
summary: >-
  Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).
extended_by:
- SOTA-015
---

# SOTA-014: Maintain master weights in FP32

## Source

Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).

## Why a second copy of the weights

An FP16 weight has about 10 bits of mantissa, so an update smaller than
roughly 2⁻¹¹ of the weight it is applied to rounds away to nothing. Late in
training that is most of them: the update-to-weight ratio falls as the
learning rate decays, and a run that looked healthy stops moving. [LIT-011](../literature.d/LIT-011.md)
shows the case directly — the FP16-only run diverges from the FP32 baseline
in accuracy while the loss curve gives little warning.

So the optimizer keeps an FP32 master copy, applies the update there, and
casts down to FP16 for the next forward pass. The FP16 weights are a
derived, disposable view of the FP32 ones.

## Cost

An extra 4 bytes per parameter on top of the 2-byte FP16 copy. With Adam's
FP32 moments ([SOTA-015](SOTA-015.md)) the full accounting is 16 bytes per parameter, of
which 12 are optimizer state — which is the accounting [SOTA-028](SOTA-028.md) and its
line then attack by partitioning rather than by shrinking.

The saving survives that cost because activations, not weights, dominate
memory at large batch. At small batch or long context with few parameters,
the trade is much less favourable and the practice is closer to break-even.
