---
status: Active
title: 'Nemotron 3 Nano: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2025-12-01'
arxiv: '2512.20848'
first_author: 'NVIDIA'
keywords:
- 'hybrid-architecture'
- 'mixture-of-experts'
- 'mamba'
- 'agentic-reasoning'
- 'long-context'
implementations:
- Nemotron 3 Nano
summary: >-
  NVIDIA (2025), [ARXIV-2512.20848](https://arxiv.org/abs/2512.20848). A 30B-A3B MoE hybrid
  Mamba-Transformer on 25T tokens: more accurate than its predecessor at
  under half the activated parameters, and up to 3.3× the inference
  throughput of comparable open models.
---

# LIT-tmptcwix: Nemotron 3 Nano: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning

NVIDIA (2025) — [ARXIV-2512.20848](https://arxiv.org/abs/2512.20848)

## Key takeaways

- 30B total, 3B activated: a mixture-of-experts **hybrid Mamba-Transformer**,
  which is the record's two architectural axes combined in one released
  model — sparsity for training economy, an SSM-plus-attention mixer for
  sequence economy.
- Pretrained on 25T tokens, including more than 3T new unique tokens over
  Nemotron 2, then SFT and large-scale RL across diverse environments.
- More accurate than the previous generation **while activating less than
  half the parameters per forward pass**, and up to **3.3× higher inference
  throughput** than similarly sized open models, named as GPT-OSS-20B and
  Qwen3-30B-A3B-Thinking-2507.
- Context up to 1M tokens; base and post-trained checkpoints both released.

## Standing in the anthology

A third independent adopter of the hybrid layout, from a laboratory with no
connection to the two the record already holds — Kimi's KDA-plus-MLA
interleave and Qwen's Gated-DeltaNet-plus-gated-attention. [SOTA-132](../practices.d/SOTA-132.md) rests on
two independent adopters; this is a third, using Mamba rather than a linear
attention as the cheap layer, which widens the practice's claim from "the
3:1 interleave works" toward "a hybrid of a fixed-state mixer and periodic
global attention works, and the mixer's family is a second-order choice".

It is also the record's only note where MoE and the hybrid mixer are
combined *and* the data pipeline is by the same group ([LIT-tmpqhulf](LIT-tmpqhulf.md)), so the
25T-token corpus and the long-horizon filtering argument are the same
laboratory's two halves.
