---
status: Active
title: 'Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence'
version: 1
tags:
- model-architecture
- attention-techniques
date: '2026-09-18'
published: '2024-04-08'
arxiv: '2404.05892'
first_author: 'Peng'
keywords:
- 'rwkv'
- 'matrix-valued-state'
- 'data-dependent-decay'
- 'multilingual'
extends:
- LIT-tmpwlt08
extended_by:
- LIT-173
implementations:
- 'RWKV-5'
- 'RWKV-6'
summary: >-
  Peng et al. (2024), [ARXIV-2404.05892](https://arxiv.org/abs/2404.05892). RWKV-5 and RWKV-6, and the two
  changes the line is still built on: the state becomes matrix-valued rather
  than vector-valued, and the decay becomes a function of the input rather
  than a learned constant.
---

# LIT-tmpl2pn3: Eagle and Finch: RWKV with Matrix-Valued States and Dynamic Recurrence

Peng et al. (2024) — [ARXIV-2404.05892](https://arxiv.org/abs/2404.05892)

## Key takeaways

- **Eagle (RWKV-5) makes the state matrix-valued.** `LIT-tmpwlt08` carried a
  vector per channel; a matrix state holds associations rather than a running
  sum, which is the capacity the recall criticisms of linear attention were
  about
- **Finch (RWKV-6) makes the decay data-dependent.** The `W` stops being a
  learned constant per channel and becomes a function of the token — the
  layer can decide what to forget and when, which a fixed decay cannot
- Both released with a **multilingual corpus and tokenizer**, and the
  multilingual result is where the line's headline numbers have come from
  since

<!-- inactive-ok-file: SOTA-178 — Proposed, and the practice this note makes legible; that it is
     unsettled is consistent with the narrow evidence base described -->

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

It is the step that makes `LIT-173` legible. RWKV-7's contribution is
*vector-valued gating and in-context learning rates* on top of a generalised
delta rule — each of those is an increment on something introduced here, and
`SOTA-178` states the practice in exactly those comparative terms without the
record holding the thing being compared to.

**The data-dependent decay is also the convergence point.** `SOTA-178`'s own
body notes that "two lines converging on per-channel gating is worth" saying
— and this is where the RWKV side of that convergence happens, a year before
the delta-rule line (`LIT-137`, `LIT-162`) reached the same place from
linear attention. `LIT-194` records the same observation about timing. Both
claims are about this paper, made while it was absent.

Unread — no `NOTE`.
