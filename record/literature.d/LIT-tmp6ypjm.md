---
status: Active
title: 'Mamba-3: Improved Sequence Modeling using State Space Principles'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2026-03-01'
arxiv: '2603.15569'
first_author: 'Lahoti'
keywords:
- 'state-space-models'
- 'state-tracking'
- 'mimo'
- 'inference-efficiency'
- 'complex-valued-state'
implementations:
- Mamba-3
summary: >-
  Lahoti et al. (2026), [ARXIV-2603.15569](https://arxiv.org/abs/2603.15569). Three changes from an
  inference-first view — a more expressive discretised recurrence, a
  complex-valued state update for state tracking, and a MIMO formulation that
  buys accuracy without decode latency.
---

# LIT-tmp6ypjm: Mamba-3: Improved Sequence Modeling using State Space Principles

Lahoti et al. (2026) — [ARXIV-2603.15569](https://arxiv.org/abs/2603.15569)

## Key takeaways

- The framing is *inference-first*, and the critique is aimed at its own
  family: many recent linear models trade quality and capability for
  algorithmic efficiency, **failing on tasks such as state tracking**, and
  their theoretically linear inference is often hardware-inefficient in
  practice. Linear is not automatically fast and not automatically enough.
- Three improvements, each from the SSM view of linear models: a **more
  expressive recurrence** derived from SSM discretisation; a
  **complex-valued state update** that enables richer state tracking; and a
  **multi-input multi-output (MIMO)** formulation that improves quality
  without increasing decode latency.
- At 1.5B, +0.6 downstream accuracy over the next best model — named as Gated
  DeltaNet — and the MIMO variant +1.2 further, for +1.8 total.
- Across state-size experiments it matches Mamba-2's perplexity at **half the
  state size**, which is the efficiency claim that matters for a fixed-memory
  architecture.

## Standing in the anthology

The current end of the state-space line the record now holds from the start:
Mamba's selectivity ([LIT-tmp2w5r0](LIT-tmp2w5r0.md)) → the duality and Mamba-2 ([LIT-tmp3kn36](LIT-tmp3kn36.md)) →
gated delta rule ([LIT-137](LIT-137.md)) → channel-wise gating ([LIT-133](LIT-133.md)) → here.

It is the only note in that line that measures against **Gated DeltaNet** as
the incumbent, which is a useful correction of perspective: the record's
hybrid practice ([SOTA-132](../practices.d/SOTA-132.md)) treats GDN and KDA as the modules to build with,
and this says the SSM family kept moving in parallel and is ahead at 1.5B.
Nothing in the record ships Mamba-3, so it stays a note; what it changes is
that "linear attention won" is not the right summary of the last two years.
