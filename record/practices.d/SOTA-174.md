---
status: Active
formerly:
- SOTA-tmpvbrwt
consensus: converged
consensus_note: >-
  Every code model in the record ships an infilling capability and none
  argues for the transformation — Qwen2.5-Coder, Falcon-H1-Tiny, and the
  reference recipes the FIM literature describes. The paper's own claim is
  that it costs nothing, and nobody has published a contradiction.
title: 'Train autoregressive models with fill-in-the-middle by default: it is a data transformation, and it is free'
version: 1
tags:
- data-pipeline
date: '2026-09-08'
published: '2022-07-01'
source:
# The paper that ran the ablations and established the "for free" claim.
# The models that ship FIM cite it without re-measuring, so they are
# adoption and live in consensus_note (ADR-017).
- LIT-124
extended_by:
- SOTA-128
implementations: []
summary: >-
  Bavarian et al. (2022), [LIT-124](../literature.d/LIT-124.md) — cut a document into prefix, middle and
  suffix, move the middle to the end with sentinel tokens, and the model
  learns to infill. Transforming a large fraction of the training data does
  not harm left-to-right perplexity or sampling quality across a wide range
  of scales, so infilling is an added capability rather than a trade.
---

# SOTA-174: Train autoregressive models with fill-in-the-middle by default: it is a data transformation, and it is free

## Source

Bavarian et al. (2022), [LIT-124](../literature.d/LIT-124.md) — [ARXIV-2207.14255](https://arxiv.org/abs/2207.14255).

A data transformation, not an architecture: cut a document into prefix,
middle and suffix, move the middle to the end with sentinel tokens, and the
model learns to infill from the surrounding context. Nothing about the model
changes.

**FIM-for-free is the claim that makes it a default.** Transforming a large
fraction of the training data does not harm left-to-right perplexity or
sampling quality, across a wide range of scales. Infilling is therefore an
added capability rather than a trade, and the paper's own recommendation is
to train autoregressive models with FIM by default.

## The knobs it settles, and the one it does not

Ablated here:

- **The transformation rate** — what fraction of documents to transform.
- **PSM against SPM ordering** — prefix-suffix-middle or
  suffix-prefix-middle.
- **How the span is chosen** — character-level random spans rather than token
  or line boundaries.
- **Where the transform applies** — at the context level rather than the
  document level.

Left unstated: whether to mask the loss on the prefix and suffix, as one
would mask a prompt in SFT. That is [SOTA-128](SOTA-128.md), which extends this and answers
it with two 90M runs — compute the loss on every token.

## Filed late, and the inversion is the point

The record has carried `SOTA-128` — a *footnote* to this practice, about one
knob this paper leaves unstated — since before it carried the practice
itself. That is the same shape as the hyper-connections trunk and the
matrix-preconditioner class: the thing somebody published a refinement of got
filed, and the thing being refined did not.

## Known implementations

- Qwen2.5-Coder, Falcon-H1-Tiny, and the reference recipes the FIM
  literature describes.
