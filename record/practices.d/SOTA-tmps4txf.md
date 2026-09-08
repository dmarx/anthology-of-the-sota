---
status: Proposed
promote_when: >-
  A released model built on Mamba-3 blocks, or an independent group running
  the three changes against Gated DeltaNet in its own harness at 1.5B or
  above. Separating the three would be better still: the MIMO readout is
  reported as a further +1.2 on top of +0.6, so a result isolating which of
  discretisation, complex state and MIMO carries the gain is what would let
  this be stated as more than a bundle.
consensus: unreplicated
consensus_note: >-
  One group, one paper, one scale. Nobody has disagreed and nobody has
  rebuilt it; the record's hybrid practice treats Gated DeltaNet and KDA as
  the modules to build with, and this is the first result saying the
  state-space family kept moving in parallel and is ahead.
title: 'Build linear-attention layers from the state-space view: expressive discretisation, complex-valued state, and a MIMO readout'
version: 1
tags:
- model-architecture
date: '2026-09-08'
published: '2026-03-01'
source:
- LIT-165
implementations: []
summary: >-
  Lahoti et al. (2026), [LIT-165](../literature.d/LIT-165.md) — three changes derived from the SSM view: a
  more expressive recurrence from the discretisation, a complex-valued state
  update for state tracking, and a MIMO formulation that adds quality without
  decode latency. +1.8 downstream at 1.5B over Gated DeltaNet, and Mamba-2's
  perplexity at half the state size.
---

# SOTA-tmps4txf: Build linear-attention layers from the state-space view: expressive discretisation, complex-valued state, and a MIMO readout

## Source

Lahoti et al. (2026), [LIT-165](../literature.d/LIT-165.md) — [ARXIV-2603.15569](https://arxiv.org/abs/2603.15569).

The framing is inference-first and the critique is aimed at its own family:
many recent linear models trade quality and capability for algorithmic
efficiency — **failing on tasks such as state tracking** — and their
theoretically linear inference is often hardware-inefficient in practice.
Linear is not automatically fast and not automatically enough.

Three changes, each read off the state-space view of linear models:

- **A more expressive recurrence**, derived from SSM discretisation.
- **A complex-valued state update**, which is what enables richer state
  tracking.
- **A multi-input multi-output (MIMO) formulation**, which improves quality
  without increasing decode latency.

## What it measured

At 1.5B, **+0.6** downstream accuracy over the next best model — named as
Gated DeltaNet — and the MIMO variant **+1.2** further, for +1.8 total.
Across state-size experiments it matches Mamba-2's perplexity at **half the
state size**, which is the efficiency claim that matters for an architecture
with a fixed memory budget.

## What it changes about the record's own summary

[SOTA-132](SOTA-132.md) interleaves linear-attention layers with global attention and
treats Gated DeltaNet and KDA as the modules to build with. This is the only
note in the state-space line that measures against Gated DeltaNet **as the
incumbent**, and it is ahead at 1.5B. So "linear attention won" is not the
right summary of the last two years: the SSM family kept moving in parallel,
and which module a hybrid should use is open again.

The line: Mamba's selectivity ([LIT-161](../literature.d/LIT-161.md)) → the duality and Mamba-2
([LIT-162](../literature.d/LIT-162.md)) → gated delta rule ([LIT-137](../literature.d/LIT-137.md)) → channel-wise gating ([LIT-133](../literature.d/LIT-133.md)) →
here.

## Conditions, and why this is Proposed

One group, one paper, 1.5B, and nothing in the record ships it. The three
changes are also reported as a bundle plus one ablation (MIMO), so a reader
adopting this is adopting all three on one team's word — which is what
`promote_when:` asks somebody to unpick.

## Known implementations

- None in the record.
