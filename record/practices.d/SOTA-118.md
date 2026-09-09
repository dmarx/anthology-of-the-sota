---
number: 118
status: 'Active'
title: 'Employ mixed precision to reduce memory usage'
version: 1
tags:
- distributed-optimization
date: '2026-08-24'
published: '2023-04-01'
source:
- LIT-083
extends:
- SOTA-116
summary: >-
  Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).
---

# SOTA-118: Employ mixed precision to reduce memory usage

## Source

Zhao et al. (2022), [LIT-083](../literature.d/LIT-083.md) — [ARXIV-2304.11277](https://arxiv.org/abs/2304.11277).

## What this adds beyond the mixed-precision practices

The FP16/BF16 recipe in [SOTA-014](SOTA-014.md) and [SOTA-016](SOTA-016.md) is about the weights and the
arithmetic. Under sharding there is a second consumer: every parameter
all-gather and gradient reduce-scatter moves *bytes over the network*, and
halving the dtype halves them. On a job whose step time is the collectives —
which is the job that reached for FSDP in the first place ([SOTA-116](SOTA-116.md)) — that
is often the larger effect.

## The parameter worth naming

The reduction dtype is a separate choice from the compute dtype, and it is
where accuracy is actually at risk: gradients are summed across the group, so
a low-precision reduction accumulates error proportional to the group size.
Keeping the reduce in FP32 while the gather stays in half precision is the
usual compromise, and it costs back half the saving on the reduce alone.

That trade is invisible from the title, which is the argument for the
practice naming the dtypes it means rather than "mixed precision" as a mode.
