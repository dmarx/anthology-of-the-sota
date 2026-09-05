---
status: Proposed
title: 'At a fixed tiny parameter budget, spend parameters on depth and SSM state width before MLP width'
version: 1
tags:
- model-architecture
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source: LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. 24–27 layers × 512 hidden and a large SSM state dimension won every ablation at 90M; 50 layers gained MMLU but halved throughput.
---

# SOTA-125: At a fixed tiny parameter budget, spend parameters on depth and SSM state width before MLP width

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

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

Conditions: one architecture family, one scale, loss curves and noisy 90M
benchmarks as the evidence; hence *Proposed*. The depth finding echoes the
authors' Falcon-H1-1.5B-Deep result at a larger scale. The trade the deep
option loses on is throughput, which is the reason to state this as a
parameter-budget rule rather than a compute-budget one.
