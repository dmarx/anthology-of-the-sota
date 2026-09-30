---
number: 363
status: Active
formerly:
- SOTA-tmpv2jq0
consensus: emerging
consensus_note: >-
  Split, and the split is the interesting part. The **slow key encoder**
  converged — BYOL, DINO and their descendants all carry an EMA target, and
  the `#304` units still to file are where that gets confirmed or broken. The
  **queue** did not: SimCLR (LIT-591) dropped it for a large batch,
  CLIP (LIT-588) uses in-batch negatives at batch 32,768, and where accelerator
  memory is plentiful the queue is often skipped. So this is one practice with
  a converged half and a contested half, filed as `emerging` rather than
  averaging two different readings into one. Read as of 2026-09.
title: 'Decouple the negative set from the batch with a queue, and keep the encoder that fills it slow'
version: 1
tags:
- representation-and-encoding
- training-optimization
date: '2026-09-23'
source:
- LIT-590
introduced_by:
- LIT-590
extends:
- SOTA-360
implementations: []
---

# SOTA-363: Decouple the negative set from the batch with a queue, and keep the encoder that fills it slow

## Source

He et al. (2019), [LIT-590](../literature.d/LIT-590.md) — [ARXIV-1911.05722](https://arxiv.org/abs/1911.05722).

## The claim

If the contrastive loss needs many negatives ([SOTA-360](SOTA-360.md)), the obvious move is
a bigger batch, and the obvious move is expensive. Instead keep a **queue**
of previously encoded keys — enqueue the current mini-batch, dequeue the
oldest — and encode the keys with a **slowly moving copy** of the query
encoder:

    θ_k ← m·θ_k + (1 − m)·θ_q          gradients flow only to θ_q

The two pieces are not separable, and the paper's framing says why. A good
dictionary must be **large** and **consistent**; a queue buys size, and
without something to buy consistency the size is worthless, because keys
written several hundred steps ago were written by a different model.

## The number that carries it

| momentum `m` | 0 | 0.9 | 0.99 | 0.999 |
| --- | --- | --: | --: | --: |
| ImageNet linear probe | **fails to train** | 55.2 | 57.8 | 59.0 |

`m = 0` is "just copy the query encoder each step", which is the
implementation anyone would write first. It does not work at all. The
requirement is not that the key encoder track the query encoder — it is that
it track it **slowly**, so that keys written at different times remain
comparable.

The corroborating measurement: at equal `K`, a memory bank is 2.6% worse,
because its keys were written by encoders spread over a whole past epoch.
Size without consistency underperforms; consistency is what the momentum
buys.

## What it costs and what it saves

MoCo trains at **batch 256 on 8 GPUs** with `K = 65536`. The alternative —
in-batch negatives — caps `K` at the batch size, and the paper notes the
cap is not just memory: their end-to-end ablation loses about 2% at batch
1024 without linear learning-rate scaling, and "optimizing with a larger
mini-batch is harder".

## Conditions

- **The queue and the momentum have diverged in practice, and the consensus
  note says so.** The slow encoder generalised past contrastive learning
  entirely — it is the EMA teacher. The queue is a memory-budget trade, and
  at CLIP's scale in-batch negatives won instead.
- **Stale keys are wrong keys.** The queue length is bounded by how fast the
  encoder moves; the eviction order is not arbitrary, it removes the least
  consistent entry.
- **This assumes the negatives can be encoded once and reused.** Anything
  making the key depend on the current query — a cross-attention scorer, a
  reranker — breaks the premise, because the cached key is no longer the
  thing being scored.
- **`m` is not a tuning knob in the usual sense.** The ablation spans a
  catastrophic failure and a 4-point range over three orders of magnitude of
  `1 − m`; the useful region is the high end.

## Known implementations

-
