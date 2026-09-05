---
status: Active
title: 'Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2024-05-01'
arxiv: '2405.21060'
first_author: 'Dao'
keywords:
- 'state-space-models'
- 'attention'
- 'state-space-duality'
- 'semiseparable-matrices'
- 'mamba'
implementations:
- Mamba-2
summary: >-
  Dao and Gu (2024), [ARXIV-2405.21060](https://arxiv.org/abs/2405.21060). SSMs and attention variants are
  two decompositions of the same class of structured semiseparable matrices;
  the duality yields Mamba-2, whose core layer is 2–8× faster.
---

# LIT-tmp3kn36: Transformers are SSMs: Generalized Models and Efficient Algorithms Through Structured State Space Duality

Dao and Gu (2024) — [ARXIV-2405.21060](https://arxiv.org/abs/2405.21060)

## Key takeaways

- The theoretical claim is the title: state-space models and variants of
  attention are **closely related**, connected through decompositions of a
  well-studied class of **structured semiseparable matrices**. Two research
  communities had been building the same object from different ends.
- That framework — **state space duality** — is not only interpretive. It
  says which algorithmic tricks from each side transfer to the other, which
  is what makes the paper productive rather than merely tidy.
- Mamba-2 falls out of it: a refinement of Mamba's selective SSM whose core
  layer is **2–8× faster** while staying competitive with Transformers on
  language modelling.

## Standing in the anthology

The pivot the record's whole hybrid half rests on, and the reason a "hybrid"
is a coherent thing to build rather than two architectures bolted together.
Falcon-H1 ([LIT-120](LIT-120.md)) puts Mamba-2 heads and attention heads side by side in
one block and tunes the channel split; Kimi Linear ([LIT-133](LIT-133.md)) and the Qwen
line ([LIT-136](LIT-136.md), [LIT-135](LIT-135.md), [LIT-152](LIT-152.md)) interleave layers at 3:1 ([SOTA-132](../practices.d/SOTA-132.md)). Both
layouts presuppose the two mechanisms are commensurable, which is what this
establishes.

The record's linear-attention sequence now reads: Mamba's selectivity
([LIT-tmp2w5r0](LIT-tmp2w5r0.md)) → the duality and Mamba-2 here → gated delta rule ([LIT-137](LIT-137.md)) →
channel-wise gating in KDA ([LIT-133](LIT-133.md)), with [LIT-tmp6ypjm](LIT-tmp6ypjm.md) as the 2026
continuation and [LIT-tmpi6mje](LIT-tmpi6mje.md) as the other family's answer.
