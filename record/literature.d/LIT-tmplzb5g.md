---
status: Active
title: 'DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model'
version: 1
tags:
- attention-techniques
date: '2026-09-05'
published: '2024-05-01'
arxiv: '2405.04434'
first_author: 'DeepSeek-AI'
keywords:
- 'multi-head-latent-attention'
- 'kv-cache'
- 'mixture-of-experts'
- 'long-context'
- 'inference-efficiency'
implementations:
- DeepSeek-V2
summary: >-
  DeepSeek-AI (2024), [ARXIV-2405.04434](https://arxiv.org/abs/2405.04434). Where Multi-head Latent
  Attention comes from: compress the KV cache into a latent vector, cutting
  it 93.3% and raising maximum generation throughput 5.76×.
---

# LIT-tmplzb5g: DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model

DeepSeek-AI (2024) — [ARXIV-2405.04434](https://arxiv.org/abs/2405.04434)

## Key takeaways

- 236B total, 21B activated, 128K context, on 8.1T tokens — but the note is
  here for one component.
- **Multi-head Latent Attention** compresses the key-value cache into a
  *latent vector* rather than storing per-head keys and values. The KV cache
  is what makes long-context serving expensive, and this attacks its size
  directly rather than attacking how much of it attention reads.
- The numbers against DeepSeek 67B: 42.5% lower training cost, **93.3%
  smaller KV cache**, and 5.76× the maximum generation throughput.
- Paired with DeepSeekMoE ([LIT-tmpe49t1](LIT-tmpe49t1.md)) — sparse computation for training
  economy, compressed cache for inference economy, which is the division of
  labour the whole DeepSeek line keeps.

## Standing in the anthology

The origin of MLA, which [LIT-131](LIT-131.md), [LIT-133](LIT-133.md), [LIT-139](LIT-139.md) and [LIT-142](LIT-142.md) all name and none
defined. Kimi Linear's hybrid keeps MLA for the one layer in four that stays
global ([SOTA-132](../practices.d/SOTA-132.md)); Kimi K3 gates it; DeepSeek's own sparse-attention line
([LIT-143](LIT-143.md) → [LIT-142](LIT-142.md) → [LIT-139](LIT-139.md)) is built on top of it. Filing it closes the largest
single hole the architecture half of the record had.

Worth reading beside the linear-attention line ([LIT-137](LIT-137.md), [LIT-133](LIT-133.md)): both are
answers to the KV cache, and they differ in what they give up. MLA keeps
exact attention over all positions and compresses what is stored; a linear
recurrence keeps a fixed-size state and gives up exactness. The 3:1 hybrid
[SOTA-132](../practices.d/SOTA-132.md) records is the field declining to choose.
