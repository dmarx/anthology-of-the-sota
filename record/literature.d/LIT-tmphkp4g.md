---
status: Active
title: 'Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention'
version: 1
tags:
- attention-techniques
- model-architecture
- inference-optimization
date: '2026-09-18'
published: '2020-06-29'
arxiv: '2006.16236'
first_author: 'Katharopoulos'
keywords:
- 'linear-attention'
- 'kernel-feature-map'
- 'autoregressive-inference'
- 'recurrence'
extended_by:
- LIT-tmpwt9mk
implementations:
- 'linear transformer'
summary: >-
  Katharopoulos et al. (2020), [ARXIV-2006.16236](https://arxiv.org/abs/2006.16236). Where linear attention comes
  from, and the identity the record argues about in twelve documents without
  being able to cite it: drop the softmax for a kernel feature map,
  associativity reorders the product to O(N), and the autoregressive case is
  then literally an RNN.
---

# LIT-tmphkp4g: Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention

Katharopoulos et al. (2020) — [ARXIV-2006.16236](https://arxiv.org/abs/2006.16236)

## Key takeaways

- **Replace `softmax(QKᵀ)V` with `φ(Q)(φ(K)ᵀV)`.** Once the similarity is a
  kernel rather than a softmax, matrix associativity lets the `K`–`V` product
  be formed first, and the sequence-length term drops from quadratic to
  linear
- **The autoregressive case is an RNN, exactly.** The running `φ(K)ᵀV` sum is
  a fixed-size state carried forward one token at a time — which is the
  paper's title and the reason every later recurrent-attention architecture
  can call itself both things without equivocating
- **Up to 4000× faster autoregressive inference** at long context, because
  generation stops re-reading the prefix and reads a state instead
- **The state is fixed-size, and that is the whole trade.** A quadratic layer
  keeps every past token addressable; this keeps a summary. What later work
  argues about is what to put in that summary and how to let it forget

<!-- inactive-ok-file: SOTA-167 — Proposed, and cited for the position it takes on linear
     attention rather than for its standing; the quote is the point -->

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032` for the category, though
this is a method paper rather than a benchmark: the recommendation it would
support is *use linear attention*, and the record's position on that is
`SOTA-167`'s, which is that "linear attention won" is not the right summary.
What it is here for is that the record **argues about linear attention in
twelve documents and could not cite its source**.

That is `DP-007` in its purest form: the identity above is assumed by
`LIT-194` ("linear attention has no decay term, so it cannot forget"),
`LIT-176` ("efficient and compromises recall over long contexts"),
`LIT-195` ("lacks precise associative recall"), `SOTA-132`, `SOTA-153` and
`LIT-165` — every one of which is a claim about *what this paper's
construction gives up*. Agreement has no author, so the thing they all agree
on went unfiled while six documents discussed its consequences.

It is also the root of two lines the record already holds separately. The
delta-rule and SSM papers (`LIT-195`, `LIT-137`, `LIT-161`, `LIT-162`) fix
the forgetting problem from one direction; `LIT-tmpwt9mk` and the RWKV line
fix it from another. Both are answers to the same fixed-size state.

Unread — no `NOTE`.
