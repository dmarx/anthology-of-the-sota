---
number: 13
status: 'Active'
title: 'Use dynamic loss scaling that doubles every 2000 successful steps'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2017-10-01'
source:
- LIT-011
summary: >-
  Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).
---

# SOTA-013: Use dynamic loss scaling that doubles every 2000 successful steps

## Source

Micikevicius et al. (2017), [LIT-011](../literature.d/LIT-011.md) — [ARXIV-1710.03740](https://arxiv.org/abs/1710.03740).

## What the source actually prescribes, and what the title adds

[LIT-011](../literature.d/LIT-011.md)'s argument is about *underflow*, not about a schedule. Gradient
magnitudes in FP16 sit near the bottom of the format's range — the paper's
histogram of activation gradients has a substantial fraction below the
smallest normal FP16 value, where they flush to zero. Multiplying the loss by
a constant S before the backward pass shifts the whole distribution into
representable range; the optimizer unscales by S before applying the update,
so the mathematics is unchanged.

The paper shows a single well-chosen constant is often enough. Dynamic
scaling is its automatic form: start high, halve on any step whose gradients
contain an inf or NaN and skip that step, and raise the factor again after a
run of successful ones.

**The specific constants in the title are an implementation's, not the
paper's.** Doubling after 2000 successful steps is the default growth
interval and growth factor in the Apex and PyTorch AMP scalers. They are
reasonable and widely used, and the record should not attribute them to
[LIT-011](../literature.d/LIT-011.md).

## Conditions

The practice is conditional on the format, not on the model: it exists to
work around FP16's exponent range, and bfloat16 removes the need for it
altogether. A run in bf16 that still carries a loss scaler is carrying a
skipped-step mechanism for a failure that cannot occur.

Cost: the skipped steps themselves. Each overflow throws away a full forward
and backward pass, which is why backing off aggressively and recovering
slowly is the safe asymmetry.
