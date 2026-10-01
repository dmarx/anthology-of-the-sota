---
number: 72
status: 'Active'
title: 'Implement early warning system for NaNs'
version: 1
tags:
- model-stability
date: '2026-08-24'
source:
- LIT-054
introduced_by:
- LIT-054
summary: >-
  Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).
---

# SOTA-072: Implement early warning system for NaNs

## Source

Zeng et al. (2022), [LIT-054](../literature.d/LIT-054.md) — [ARXIV-2210.02414](https://arxiv.org/abs/2210.02414).

## The word doing the work is "early"

By the time a NaN reaches the loss it has already propagated through the
optimizer state, and Adam's moments will carry it forward across every
subsequent step: a single non-finite gradient poisons `v` and every later
update divides by a NaN. Detecting it at the loss means the last clean
checkpoint may be many steps back.

Early means at the gradient, before the optimizer step — which is a check
the mixed-precision loss scaler is already doing for its own purposes
([SOTA-013](SOTA-013.md)), and the cheapest place to reuse. A run in bf16 that dropped the
scaler dropped that check with it, which is a real and easily-missed
consequence of the switch.

The warning sign comes from LIT-054. Training GLM-130B with FP16 mixed
precision, the authors saw precision-related spikes, some of which "come with
a portent of suddenly soaring gradient norm and eventually a spike or even NaN
in loss". They found a collapse usually lags a gradient-norm spike by a few
training steps, so the gradient norm warns before the NaN appears. The paper
does not prescribe a NaN detector as such. Its own response was to shrink the
embedding-layer gradient, and it credits skipping data to OPT-175B, not to
GLM-130B. That differs from how the next section reads.

## What "system" should mean here

The detection is the easy half; the response is the practice. GLM-130B's
answer is the rehearsed one — rewind to the last checkpoint and skip the
batches ([SOTA-095](SOTA-095.md)) — which only works if checkpoints are frequent enough to
lose little ([SOTA-054](SOTA-054.md)) and if the data loader's position is restorable,
which the record still has no practice for.

Stated as "implement an early warning system", this is a component of that
procedure written up as though it were the whole of it.
