---
status: 'Active'
title: 'Use SwiGLU activation for transformers'
version: 1
tags:
- model-architecture
date: '2026-08-24'
published: '2020-02-01'
source:
- LIT-030
summary: >-
  Noam et al. (2020), [LIT-030](../literature.d/LIT-030.md) — [ARXIV-2002.05202](https://arxiv.org/abs/2002.05202).
implementations:
- llama2
---

# SOTA-034: Use SwiGLU activation for transformers

## Source

Noam et al. (2020), [LIT-030](../literature.d/LIT-030.md) — [ARXIV-2002.05202](https://arxiv.org/abs/2002.05202).

## Variations

**SiTU-GLU** ([LIT-131](../literature.d/LIT-131.md)), the first replacement in the record. The
objection is about range, not quality: both of SwiGLU's multiplicative
factors are unbounded, so coincident large coordinates produce activation
outliers and raise the overflow risk in low-precision arithmetic. The
original GLU's sigmoid gate is bounded but gives up the approximately linear
positive regime that Swish has. SiTU-GLU applies a scaled `tanh` soft cap to
the linear factor of the Swish gate and, independently, to the up branch —
near-linear at the origin, bounded far from it — with a different cap
constant per branch. Kimi K3 ships it at 2.8T.

One group, one model, no ablation: the report gives the motivation and the
functional form and does not measure SiTU-GLU against SwiGLU anywhere. So
this is recorded as a variation rather than a competing practice, and what
it establishes is that a frontier lab found SwiGLU's unboundedness worth
engineering around at trillion scale.

## Known implementations

- llama2; Kimi K3 (SiTU-GLU)
