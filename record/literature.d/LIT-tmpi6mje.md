---
status: Active
title: 'RWKV-7 "Goose" with Expressive Dynamic State Evolution'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2025-03-01'
arxiv: '2503.14456'
first_author: 'Peng'
keywords:
- 'linear-attention'
- 'delta-rule'
- 'state-tracking'
- 'expressivity'
- 'constant-memory'
implementations:
- RWKV-7
summary: >-
  Peng et al. (2025), [ARXIV-2503.14456](https://arxiv.org/abs/2503.14456). A generalised delta rule with
  vector-valued gating and in-context learning rates — provably able to track
  state and recognise all regular languages, which Transformers under
  standard conjectures cannot.
---

# LIT-tmpi6mje: RWKV-7 "Goose" with Expressive Dynamic State Evolution

Peng et al. (2025) — [ARXIV-2503.14456](https://arxiv.org/abs/2503.14456)

## Key takeaways

- Constant memory and constant inference time per token, and a 2.9B model
  that sets a 3B state of the art on multilingual tasks and matches the 3B
  state of the art in English — **while trained on dramatically fewer
  tokens** than the models it is compared with.
- The mechanism is a generalised delta rule with **vector-valued gating** and
  **in-context learning rates**, plus a relaxed value-replacement rule. The
  vector-valued gate is the same move Kimi Delta Attention makes ([LIT-133](LIT-133.md)),
  arrived at independently.
- The expressivity result is the part worth carrying: RWKV-7 can perform
  **state tracking and recognise all regular languages** while remaining
  parallelisable to train — which, under standard complexity conjectures,
  **exceeds what Transformers can do**, since they are limited to TC⁰.
- Released with a 3.1T-token multilingual corpus and four models from 0.19B
  to 2.9B, Apache 2.0.

## Standing in the anthology

The other expressive linear recurrence, and the reason [SOTA-135](../practices.d/SOTA-135.md)'s sequence
is not a single lineage. The record's gated-delta line runs through NVIDIA's
Gated DeltaNet into Qwen and Kimi; RWKV arrived at vector-valued gating on
its own, from a recurrent-network tradition rather than from linear
attention.

Its complexity argument is the sharpest claim in the record's architecture
half and cuts against an assumption the rest of the corpus makes implicitly.
Every hybrid practice here ([SOTA-132](../practices.d/SOTA-132.md)) is justified by linear layers being
*cheaper* while global attention supplies capability that linear layers
lack. This says the expressivity gap runs the other way for state tracking —
the recurrence can do something attention provably cannot. Whether that
matters for language modelling at scale is not settled by a 2.9B model, and
the record should hold the claim without leaning on it.
