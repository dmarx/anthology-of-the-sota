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
# CORRECTED. Was `introduced_by: LIT-054`, which passed only because it is
# also the source. GLM-130B observes that a gradient-norm spike precedes the
# NaN; it recommends no detector, and its response is embedding gradient
# shrink. The check this practice means by "early" -- non-finite values caught
# in the gradients before the update -- is stated in Mixed Precision Training
# (2017) §3.2: overflow puts infinities and NaNs in the weight gradients that
# "will irreversibly damage the weights after an update", it "can be
# efficiently detected by inspecting the computed weight gradients", and the
# update can be skipped. Not the origin either, as the record reads them:
# PaLM (LIT-069, via SOTA-095) rewinds and skips batches after a spike, and
# OPT-175B, as GLM-130B reports it, skipped data and adjusted hyperparameters.
introduced_by:
- LIT-011
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

That check is where the practice starts, and it is older than the source.
[LIT-011](../literature.d/LIT-011.md), the mixed-precision training paper, names the hazard this section
opens with: an overflow during backpropagation puts infinities and NaNs in the
weight gradients, which "will irreversibly damage the weights after an
update". Its answer is to inspect the weight gradients for overflow, which it
says can be done efficiently, and skip the update when one is found; its
conclusion suggests driving the loss scale from the same check, which is what
dynamic loss scaling became. So detection at the gradient, before the
step, was published five years before GLM-130B as part of making fp16
training safe.

The warning sign comes from [LIT-054](../literature.d/LIT-054.md). Training GLM-130B with FP16 mixed
precision, the authors saw precision-related spikes, some of which "come with
a portent of suddenly soaring gradient norm and eventually a spike or even NaN
in loss". They found a collapse usually lags a gradient-norm spike by a few
training steps, so the gradient norm warns before the NaN appears. The paper
does not prescribe a NaN detector as such. Its own response was to shrink the
embedding-layer gradient, and it credits skipping data to OPT-175B, not to
GLM-130B. That differs from how the next section reads.

## What "system" should mean here

The detection is the easy half; the response is the practice. The rehearsed
answer is PaLM's, not GLM-130B's: rewind to the last checkpoint and skip the
batches ([SOTA-095](SOTA-095.md)). It only works if checkpoints are frequent enough to
lose little ([SOTA-054](SOTA-054.md)) and if the data loader's position is restorable,
which the record still has no practice for.

Stated as "implement an early warning system", this is a component of that
procedure written up as though it were the whole of it.
