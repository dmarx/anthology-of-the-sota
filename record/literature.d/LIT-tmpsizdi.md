---
status: 'Active'
title: 'PowerSGD: Practical Low-Rank Gradient Compression for Distributed Optimization'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
published: '2019-05-01'
arxiv: '1905.13727'
first_author: 'Vogels'
keywords:
- 'gradient-compression'
- 'low-rank'
- 'error-feedback'
- 'power-iteration'
implementations: []
summary: >-
  Vogels et al. (2019), [ARXIV-1905.13727](https://arxiv.org/abs/1905.13727). PowerSGD compresses the gradient to
  a rank-k factorization found by one power-iteration step, which is all-
  reducible, and error feedback is what makes it converge.
---
# LIT-tmpsizdi: PowerSGD: Practical Low-Rank Gradient Compression for Distributed Optimization

Vogels et al. (2019) — [ARXIV-1905.13727](https://arxiv.org/abs/1905.13727)

## Key takeaways

PowerSGD introduces a low-rank gradient compressor based on a single step of
warm-started power (subspace) iteration that is linear and therefore
compatible with efficient all-reduce aggregation. It is the first
compression method demonstrated to achieve consistent wall-clock speedups
over standard SGD with highly optimized NCCL communication on commodity GPU
hardware.

- **Wall-clock speedup (CNN).** Rank-2 PowerSGD achieves 23% faster per-
  batch training than uncompressed SGD on ResNet18/Cifar10 with no accuracy
  loss.
  *Holds when:* 16 GPUs, NCCL backend, rank r=2.
- **Wall-clock speedup (LSTM).** Rank-4 PowerSGD reduces total training time
  by 55% while matching SGD perplexity on Wikitext-2.
  *Holds when:* 16 GPUs, NCCL backend, rank r=4.
- **Convergence with error feedback.** PowerSGD with error feedback and
  post-compression momentum matches or exceeds the final accuracy of
  uncompressed SGD across all evaluated architectures.
  *Holds when:* Rank r in {2, 4, 7}; ResNet18, LSTM; with warm-start and
  error feedback enabled.

## What the evidence does not cover

- Compression rank must be manually tuned per architecture; transformer
  language models may require much higher rank (32+) than CNNs.
- Compression and decompression add non-trivial compute overhead (matrix
  multiplications and Gram-Schmidt), which limits gains for small models.
- The generalization gap with large batch sizes is an orthogonal issue
  PowerSGD does not solve.
- The theoretical convergence rate assumes a fixed compressor quality; the
  warm-start heuristic lacks a complete convergence proof for varying
  gradients.

## Standing in the anthology

Read — the reading is [NOTE-tmpwkc41](../notes.d/NOTE-tmpwkc41.md). Arrived in the imported batch, which
brought in the communication-compression branch.
