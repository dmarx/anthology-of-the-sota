---
status: Active
title: 'Gated Linear Attention Transformers with Hardware-Efficient Training'
version: 1
tags:
- attention-techniques
date: '2026-09-07'
published: '2023-12-01'
arxiv: '2312.06635'
first_author: 'Yang'
keywords:
- 'linear-attention'
- 'gating'
- 'chunkwise-parallel'
- 'io-awareness'
- 'length-generalization'
summary: >-
  Yang et al. (2023), [ARXIV-2312.06635](https://arxiv.org/abs/2312.06635). Linear attention was slower in practice
  than optimised softmax attention despite better asymptotics, because nobody
  had made it I/O-aware. FlashLinearAttention fixes that — faster than
  FlashAttention-2 as a standalone layer even at 1K — and the algorithm
  generalises to a data-dependent forget gate. The resulting GLA Transformer
  matches LLaMA-architecture baselines, beats Mamba on throughput at matched
  size, and generalises from 2K training to over 20K.
---

# LIT-tmprkx70: Gated Linear Attention Transformers with Hardware-Efficient Training

Yang et al., MIT and MIT-IBM Watson AI Lab (2023) — [ARXIV-2312.06635](https://arxiv.org/abs/2312.06635)

## Key takeaways

- **The practical problem it names.** Linear attention has better asymptotics
  and can be written as an RNN with a matrix-valued hidden state, so inference
  is linear-time. It was still *slower in wall-clock* than a good softmax
  kernel, because the existing implementations were not I/O-aware. That is a
  systems failure being mistaken for an architectural one.
- **FlashLinearAttention** is the fix: a chunkwise algorithm that trades
  memory movement against parallelism, with secondary chunking inside each
  chunk so the inter-sub-chunk part runs in half precision on tensor cores
  while the intra-sub-chunk part stays in full precision in log space. Faster
  than FlashAttention-2 as a standalone layer **even at 1K sequence length**,
  which is where the asymptotic argument has not begun to pay.
- **The gate.** Plain linear attention has no decay term, so it cannot forget;
  the paper cites that as a suspected cause of its instability on long
  contexts. RetNet-style fixes use a *global, non-data-dependent* decay. GLA
  makes the forget gate data-dependent and per-channel, and the chunkwise
  algorithm is generalised to carry the cumulative decay across chunks.
- **Results.** Competitive with a LLaMA-architecture Transformer and with
  RetNet and Mamba at moderate scale, with higher training throughput than a
  similarly-sized Mamba. The standout is length generalization: trained at 2K,
  no significant perplexity degradation past 20K.

## Standing in the anthology

One of the two parents of Gated DeltaNet ([LIT-137](LIT-137.md)), which the record has held
without either. Gated DeltaNet is, in its own title's terms, the delta rule of
[LIT-tmpx22aq](LIT-tmpx22aq.md) plus the data-dependent gate introduced here; reading [LIT-137](LIT-137.md)
without this note leaves the *gate* half unexplained.

It is also the origin of the FlashLinearAttention library that both parents
ship in and that Kimi K3 ([LIT-131](LIT-131.md)) names in its kernel work — so the line
this record carries as an architecture story is partly a kernel story, and
this is where that starts.

Filed via the reference pass in [#40](https://github.com/dmarx/anthology-of-the-sota/issues/40), from Kimi K3 §2.1.1.
