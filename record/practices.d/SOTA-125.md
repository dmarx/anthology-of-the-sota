---
number: 125
status: Proposed
promote_when: >-
  The same parameter-budget trade run on a hybrid from another group, or at
  a second tiny scale. What would settle this is another ablation in the 90M
  class, not a result at a size where the trade does not bind.
consensus: unreplicated
consensus_note: >-
  One architecture family, on loss curves and noisy 90M benchmarks — and
  since #58 named LIT-120 in the source list, at two scales rather than one:
  the depth half echoes the same authors' Falcon-H1-1.5B-Deep result. Two
  scales from one group is still one group.
title: 'At a fixed tiny parameter budget, spend parameters on depth and SSM state width before MLP width'
version: 3
history:
- version: 2
  date: '2026-09-07'
  note: >-
    Sourced to LIT-120 as well as LIT-119. The depth half of the finding is
    corroborated at a larger scale by the authors' own Falcon-H1-1.5B-Deep
    result, which is exactly the kind of second source ADR-010 made the field
    able to count. The recommendation is unchanged.
- version: 3
  date: '2026-09-07'
  note: >-
    consensus_note corrected. It read "at one scale" while the source list,
    since #58, names LIT-119 at 90M and LIT-120 at 1.5B. The value does not
    move: `unreplicated` is about one group, and two scales from the same
    group is still one group. This is what a support list changing under a
    consensus reading looks like when the reading survives it.
tags:
- model-architecture
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source:
# LIT-120 corroborates the depth half at a larger scale — the authors' own
# Falcon-H1-1.5B-Deep result — which is what ADR-010 made the list able to
# count.
- LIT-119
- LIT-120
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. 24–27 layers × 512 hidden and a large SSM state dimension won every ablation at 90M; 50 layers gained MMLU but halved throughput.
compared_against:
- SOTA-190
---

# SOTA-125: At a fixed tiny parameter budget, spend parameters on depth and SSM state width before MLP width

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

## The ablations

Holding a hybrid Mamba/attention model at 90M parameters and moving
parameters between axes, on a STEM-heavy mix:

- Depth vs width (200 GT): the mid-depth 27-layer, 512-hidden configuration
  beat the shallow one on commonsense tasks by a wide margin (HellaSwag);
  the 50-layer configuration gained further on MMLU and MMLU-Pro but cost
  about 2× in training throughput, and was not chosen. The release uses 24
  layers to land on 90M.
- MLP factor vs SSM dimension (70 GT, loss as the proxy): every variant that
  grew the MLP by shrinking the SSM state dimension descended slower.
  "SSM capacity is more valuable than large feed-forward width for a tiny
  model." For a fixed SSM dimension there is an optimal hidden-size to MLP
  ratio, and it sat near hidden 512.
- KV heads: more KV heads, paid for out of the MLP, helped up to a point;
  the baseline remained best.

## Why this is Proposed

The evidence is one architecture family, one scale, loss curves and noisy
90M benchmarks. The depth finding echoes the
authors' Falcon-H1-1.5B-Deep result at a larger scale ([LIT-120](../literature.d/LIT-120.md)). The trade the deep
option loses on is throughput, which is the reason to state this as a
parameter-budget rule rather than a compute-budget one.
