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
# LIT-011 supplies the mechanism and prescribes no schedule; the constants
# come from NVIDIA's mixed-precision guide, which reports them as one tested
# setting rather than a recommendation.
- LIT-011
- LIT-tmpsalf8
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

**The constants in the title are not the paper's, and they are not
anonymous either.** They come from NVIDIA's *Train With Mixed Precision*
guide, [LIT-tmpsalf8](../literature.d/LIT-tmpsalf8.md), whose dynamic-scaling section reports:

> We successfully trained networks with N = 2000, increasing scaling factor
> by 2, decreasing scaling factor by 0.5

All three numbers in one sentence, from the organisation that employed
[LIT-011](../literature.d/LIT-011.md)'s authors. From there they became defaults rather than
recommendations: PyTorch's `torch.amp.GradScaler` ships
`growth_interval=2000`, `growth_factor=2.0`, `backoff_factor=0.5` and
`init_scale=65536.0`, and NVIDIA's own Apex carried them first.

**The same sentence says "many other settings are valid as well."** So the
honest standing of 2000 is *tested once, then adopted everywhere as a
default* — not a measured optimum. Nobody in the record has shown what the
interval should be, and the reason almost everyone runs 2000 is that it is
what the library does. That is a weaker claim than the title makes, and a
more useful one.

## Conditions

The practice is conditional on the format, not on the model: it exists to
work around FP16's exponent range, and bfloat16 removes the need for it
altogether. A run in bf16 that still carries a loss scaler is carrying a
skipped-step mechanism for a failure that cannot occur.

Cost: the skipped steps themselves. Each overflow throws away a full forward
and backward pass, which is why backing off aggressively and recovering
slowly is the safe asymmetry.
