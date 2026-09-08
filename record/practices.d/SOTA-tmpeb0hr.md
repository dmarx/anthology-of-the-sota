---
status: Proposed
promote_when: >-
  A released model built this way, or an independent group running a
  single-layer hybrid against a 3:1 layer interleave at matched parameters
  and reporting both quality and the serving cost the uniformity is supposed
  to save. What would not move it: another intra-layer hybrid design, which
  is a fourth answer rather than evidence about this one.
consensus: unreplicated
consensus_note: >-
  One group, no frontier deployment, against a layer-interleaved practice
  with two independent production lines behind it. Nobody disputes the
  design; nobody has run it at scale either.
title: 'Hybridise inside the layer: long-term slots, a sliding window, and one softmax over both, with the window size as the only dial'
version: 1
tags:
- attention-techniques
date: '2026-09-08'
published: '2025-10-01'
source:
- LIT-176
implementations: []
summary: >-
  Du et al. (2025), [LIT-176](../literature.d/LIT-176.md) — long-term context in key-value slots updated by
  a linear RNN, short-term context from a sliding window, and a *single*
  softmax attending over both together, so the long/short weighting is
  per-token, per-head and content-dependent with no fusion parameters. Every
  layer stays structurally identical and one hyperparameter slides from
  purely linear to full attention.
---

# SOTA-tmpeb0hr: Hybridise inside the layer: long-term slots, a sliding window, and one softmax over both, with the window size as the only dial

## Source

Du et al. (2025), [LIT-176](../literature.d/LIT-176.md) — [ARXIV-2510.07019](https://arxiv.org/abs/2510.07019).

The trade-off is the record's own: full attention is quadratic, linear
attention is efficient and compromises recall over long contexts. Every
hybrid in the record is an arrangement for having some of both. This one
changes *where* the arrangement lives.

- **Long-term context** sits in key-value slots updated by a linear RNN.
- **Short-term context** comes from a sliding window.
- **One softmax attention operates over all of them together**, so the
  weighting between long and short term is per-token, per-head and
  content-dependent — with no extra fusion parameters to learn.

Inter-layer behaviour is then controlled by a single hyperparameter, the
sliding-window size, which slides smoothly from purely linear to full
attention while **every layer stays structurally identical**.

## The argument that is not about quality

A 3:1 interleave makes every fourth layer different, and that difference
propagates: every serving stack, cache manager and pipeline schedule has to
know about it. The infrastructure sections of the frontier reports in this
record are largely about managing exactly that. A uniform stack with a dial
moves the complexity out of the schedule and into a number.

Whether that is worth anything depends on costs the paper does not measure
and the record cannot supply, which is part of why this is `Proposed`. But it
is a real argument and it is not a quality argument, so a comparison that
reports only benchmark scores will not settle it either way.

## Against the interleave, which it does not displace

[SOTA-132](SOTA-132.md) records the layer-interleaved hybrid — three linear layers per
global one — and contrasts it with the parallel-head layout that puts both
head types side by side in one block. This is a third position, and the
record now holds all three: mix by *layer*, mix by *head*, or mix *inside one
attention*.

It reports beating Transformers and other hybrid baselines on
recall-intensive and commonsense tasks, and pretrained models can be
structurally hybridised into it after the fact — which is the cheapest path
to trying it that any of the three offers.

The relation is deliberately not declared. `compared_against` records a
comparison somebody ran between two things the record recommends, and this
paper's baselines are its own, not `SOTA-132`'s specific 3:1 global layout.

## Known implementations

- None in the record.
