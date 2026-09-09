---
number: 100
status: 'Active'
title: 'Use learning rate warmup proportional to model size'
version: 1
tags:
- training-optimization
date: '2026-08-24'
published: '2020-02-01'
source:
- LIT-114
summary: >-
  Xiong et al. (2020), [LIT-114](../literature.d/LIT-114.md) — [ARXIV-2002.04745](https://arxiv.org/abs/2002.04745).
compared_against:
- SOTA-008
- SOTA-009
- SOTA-032
---

# SOTA-100: Use learning rate warmup proportional to model size

## Source

Xiong et al. (2020), [LIT-114](../literature.d/LIT-114.md) — [ARXIV-2002.04745](https://arxiv.org/abs/2002.04745).

## What warmup was compensating for

[LIT-114](../literature.d/LIT-114.md)'s contribution is an explanation rather than a technique. Under
post-norm — normalisation applied after the residual addition — the expected
gradient at the output layer grows with depth at initialisation, so a large
learning rate diverges immediately. Warmup exists to get past that window: it
keeps steps small until the parameters move somewhere the large rate is
survivable.

That is why the length scales with the model. A deeper, wider stack has a
worse initial gradient scale and needs longer at the small rate, which is what
"proportional to model size" is reaching for.

## And why the practice is largely historical

The same paper shows the compensation becomes unnecessary under pre-norm
([SOTA-032](SOTA-032.md)), which bounds those gradients by construction — warmup "can be
removed" is the paper's own finding, and pre-norm is what every model in this
record uses.

So the honest reading is: this describes a real dependency in an architecture
the field has left. Warmup survives in modern recipes for different reasons —
Adam's second-moment estimate is unreliable in the first few hundred steps,
and a schedule with a peak needs a ramp to it ([SOTA-008](SOTA-008.md), [SOTA-009](SOTA-009.md)) — and
those reasons do not scale with model size the way this one did.

Kept Active because the mechanism is correct and because the *reason* a
practice persists after its original justification lapses is exactly the kind
of thing this record exists to hold. But a reader should not size their warmup
from this practice.
