---
number: 16
status: 'Active'
title: 'Perform forward/backward passes in FP16'
version: 1
tags:
- training-optimization
date: '2026-08-24'
source:
- LIT-011
summary: >-
  Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).
extended_by:
- SOTA-013
- SOTA-014
---

# SOTA-016: Perform forward/backward passes in FP16

## Source

Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).

## Why FP16 for the passes and not for everything

The arithmetic is the point: half-precision matrix multiplies run on tensor
cores at several times the FP32 rate, and every activation stored for the
backward pass is half the size. On a transformer at large batch, activations
dominate memory, so this is where the saving actually comes from — not from
the weights, which [SOTA-014](SOTA-014.md) keeps in FP32 anyway.

What stays FP32 inside the pass is the *accumulation*. Tensor cores multiply
in FP16 and accumulate the dot product in FP32, which is what keeps a long
reduction from losing the small terms; a pure-FP16 accumulate loses accuracy
on exactly the layers that matter most. The same reasoning promotes
reductions and normalisation statistics to FP32 while leaving pointwise ops
in half precision.

## Conditions and cost

FP16 has about 10 bits of mantissa and a narrow exponent range, so the
practice does not stand alone: it needs FP32 master weights ([SOTA-014](SOTA-014.md)) and
loss scaling ([SOTA-013](SOTA-013.md)) to be safe, and those are what [LIT-011](../literature.d/LIT-011.md) contributes.
Without both, gradients underflow to zero and the run silently trains worse
rather than failing.

The alternative that has since arrived is bfloat16, which trades mantissa
bits for FP32's exponent range and so removes the need for loss scaling
entirely. Where the hardware supports it, that is the simpler recipe, and the
part of this practice that survives is the FP32 accumulation rather than the
FP16 storage format.
