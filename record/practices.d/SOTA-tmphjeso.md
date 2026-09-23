---
status: Active
title: 'Isolate the emergent outlier feature dimensions into 16-bit and quantize the rest to int8'
version: 1
tags:
- numerics-and-precision
- inference-optimization
consensus: converged
consensus_note: >-
  This is what `load_in_8bit=True` does in `transformers`, and `vllm` serves
  it too — the sweep in #289 found `bitsandbytes` carried by both indexes
  and reading the row apart showed it was two techniques, this one and NF4
  (SOTA-230). Adoption, not evidence (DP-005): what is converged is that
  int8 inference at scale requires handling outliers separately, rather than
  that this particular decomposition is the best way.
date: '2026-09-23'
source:
- LIT-tmpt6fwq
introduced_by:
- LIT-tmpt6fwq
summary: >-
  Dettmers et al. (2022), [ARXIV-2208.07339](https://arxiv.org/abs/2208.07339). Quantize the projections
  vector-wise to int8, but pull the handful of systematically large feature
  dimensions out into a separate 16-bit multiplication — 99.9% of values in
  8-bit, no measured quality cost up to 175B.
---

# SOTA-tmphjeso: Isolate the emergent outlier feature dimensions into 16-bit and quantize the rest to int8

## Source

Dettmers et al. (2022), [LIT-tmpt6fwq](../literature.d/LIT-tmpt6fwq.md) — [ARXIV-2208.07339](https://arxiv.org/abs/2208.07339).

## What to do

For the feed-forward and attention projection matrices:

1. Quantize **vector-wise** — one normalization constant per inner product,
   not one per tensor.
2. Detect the feature dimensions whose magnitudes are far outside the rest,
   and route those columns into a separate 16-bit matrix multiplication.
3. Sum the two products.

More than 99.9% of values go through the 8-bit path.

## Why the decomposition is the whole method

Naive int8 works on small transformers and breaks on large ones, and for
years that read as "quantization gets harder with scale". The paper's
contribution is the diagnosis: **a small number of feature dimensions emerge
with very large magnitudes**, they recur across layers, and they dominate
attention and prediction. A per-tensor scale chosen to cover them destroys
the resolution of everything else.

So the fix is not a better global scale. It is to stop asking one scale to
cover two very different distributions.

## What it buys, and what it does not

Memory, and access. A 175B 16/32-bit checkpoint loads, converts and runs at
roughly half the memory — the stated payoff is OPT-175B or BLOOM on a single
server of consumer GPUs, not throughput. The extra 16-bit path and the
outlier detection cost time, and reports of int8 inference being *slower*
than 16-bit at small batch are consistent with this method rather than
evidence against it.

## The claim to watch

*"Without any performance degradation"* means *no degradation the authors
measured, on their evaluations, up to 175B*. It is a strong result and it is
an absence-of-evidence claim about a specific suite — the shape `DP-010`
names. The emergent-outlier characterization is the part later work has
built on; the no-degradation headline is the part a harder evaluation could
move, and this record holds no independent test of it.
