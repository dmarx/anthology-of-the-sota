---
status: Active
title: 'RWKV: Reinventing RNNs for the Transformer Era'
version: 1
tags:
- model-architecture
- attention-techniques
date: '2026-09-18'
published: '2023-05-22'
arxiv: '2305.13048'
first_author: 'Peng'
keywords:
- 'rwkv'
- 'linear-attention'
- 'time-decay'
- 'parallel-training'
- 'recurrent-inference'
extends:
- LIT-tmpwt9mk
extended_by:
- LIT-tmpl2pn3
implementations:
- 'RWKV-4'
summary: >-
  Peng et al. (2023), [ARXIV-2305.13048](https://arxiv.org/abs/2305.13048). The paper the RWKV line starts from,
  and the first to take the architecture to 14B: AFT's position bias becomes
  an exponential decay over relative position, which makes the layer trainable
  in parallel and runnable as a constant-memory recurrence.
---

# LIT-tmpwlt08: RWKV: Reinventing RNNs for the Transformer Era

Peng et al. (2023) — [ARXIV-2305.13048](https://arxiv.org/abs/2305.13048)

## Key takeaways

- **`R`, `W`, `K`, `V`** — receptance, weight (the decay), key, value. The
  `W` is `LIT-tmpwt9mk`'s learned position bias restricted to a **decaying
  function of relative distance**, and that restriction is what buys the
  recurrence: a bias that depends only on how far back a token is can be
  accumulated incrementally
- **Train in parallel, run as an RNN.** The same layer has a
  sequence-parallel form for training and a step-at-a-time form for
  generation with state that does not grow — the property the line is
  organised around and that `LIT-tmphkp4g` first established was possible
- **Scaled to 14B**, which at the time was by a wide margin the largest
  recurrent language model trained, and the evidence that the construction
  was not confined to small scale

<!-- inactive-ok-file: SOTA-178 — Proposed, and the practice whose evidence base this note is
     about; that it is unsettled is consistent with resting on one model -->

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

This is the missing trunk `#161` named. The record held `LIT-173` (RWKV-7)
and nothing that led to it, which matters more than a gap usually does
because **`SOTA-178`'s entire evidence base is RWKV-7** — its own conditions
section says "RWKV-7 'Goose', 0.19B to 2.9B. Nothing else in the record."

A practice resting on one model of one architecture reads differently
depending on whether that architecture is a one-off or the current member of
a line that has been scaled and re-derived four times. It is the second, and
now the record can show it.

`SOTA-135` is the other document this changes. It observes that RWKV arrived
at a correction-style update "independently and a year earlier" than the line
it is filed beside — a claim about *when this lineage did something*, which
was being made against a record that held only the lineage's latest member.

Unread — no `NOTE`.
