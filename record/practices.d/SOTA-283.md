---
number: 283
status: Proposed
formerly:
- SOTA-tmpjdocv
promote_when: >-
  A group sharing no author with LIT-211 reporting quantized fine-tuning with
  an error-feedback accumulator, on a task other than Countdown, with repeats
  or error bars — the last because this source's own numbers vary by more than
  the effects it discusses. Another result from inside the Qiu line is not it.
consensus: unreplicated
consensus_note: >-
  One paper, and not an independent one: its corresponding author is
  `LIT-211`'s first author. The underlying device — error feedback on a
  coarsely quantized channel — is well established from 1-bit SGD onward, but
  nobody outside this line has applied it to the parameter lattice of a
  quantized model.
title: 'To fine-tune a model that is already quantized, bank the part of each update that is smaller than the lattice spacing, and rebuild the accumulator from seeds rather than storing it'
version: 1
tags:
- numerics-and-precision
- adaptation-and-tuning
- training-optimization
date: '2026-09-21'
source:
- LIT-473
introduced_by:
- LIT-473
extends:
- SOTA-154
implementations: []
explained_by:
- THEORY-042
---

<!-- inactive-ok-file: THEORY-006 — Proposed, and named in 'What is not claimed
     here' to say this practice is not evidence for it -->

# SOTA-283: To fine-tune a model that is already quantized, bank the part of each update that is smaller than the lattice spacing, and rebuild the accumulator from seeds rather than storing it

## Source

Xu, Miikkulainen and Qiu (2026), [LIT-473](../literature.d/LIT-473.md) — read as
[NOTE-222](../notes.d/NOTE-222.md). Countdown, Qwen2.5 at 1.5B and 3B, INT4, INT8 and
W8A8.

## When this applies

Only when the model is quantized and you intend to keep it that way, and only
when you are already fine-tuning with evolution strategies rather than
policy-gradient RL — which is [SOTA-154](SOTA-154.md), and is what makes this a
descendant rather than a standalone recommendation. If you can hold FP16
weights, this problem does not arise.

## The claim

Two moves, and they are needed together.

**Bank the remainder.** An ES update `η · ĝ` on an integer lattice of spacing
`Δ` is routinely smaller than `Δ/2`, so rounding it discards it. Keep an FP16
residual, add it to the update before rounding, and carry forward what is left
over. Small signals then integrate until they cross a grid point and move the
weight. This is error feedback — the Delta-Sigma device from 1-bit SGD — and
the paper credits it as such.

**Do not store the residual.** An FP16 accumulator over all parameters costs
more than the quantized weights, which would cancel the reason you quantized.
It does not need storing: it is a deterministic function of the random seeds
and scalar rewards you already keep. Rebuild it on demand by replaying the
last `W` steps. Optimizer-state memory falls from `O(d)` to `O(W·P)` — a few
kilobytes — at the price of `W` noise reconstructions per update.

The second move is the practice. Error feedback alone yields a memory-hungry
method in a setting chosen for having no memory.

## Settings that are known to work

Decay `γ = 0.90` with a replay window `W` between 10 and 50; accuracy is flat
across that range (13.05% at `W`=10 to 16.15% at `W`=30). **Do not scale the
decay down with the window.** Shrinking `W` to 10 with `γ = 0.58` collapses
performance to 4.55% — the ablation separates these, and it is the aggressive
decay that breaks it, not the short history.

`W` is a throughput knob: halving it costs about a point of accuracy and 60%
of the reconstruction cost.

## Conditions

**The reported variance is larger than the reported effects.** QES beats its
own full-residual oracle at INT8 on both model sizes and loses to it by 10
points at W8A8 on 3B. An approximation cannot beat what it approximates, so
those gaps are run-to-run noise — and no repeats or error bars are given
anywhere. Treat every margin in the source as provisional, including the
favourable ones. The one comparison large enough to survive this is against
QuZO at INT4 on the 1.5B model, 5.25% against 16.00%.

**One task, one model family, two sizes.** Countdown on Qwen2.5 at 1.5B and
3B, which is the task and the family this line is already most argued on.

**Not independent.** The corresponding author is `LIT-211`'s first author.
`SOTA-154`'s consensus note keeps an explicit count of results from inside
that line; this belongs on that side.

**Uniform integer lattices only.** INT4, INT8 and W8A8. The cancellation the
accumulator fixes gets worse as `Δ` grows, so sub-4-bit and non-uniform
formats are where this would be most useful and are exactly what is untested.

**Memory is a complexity argument.** `O(d) → O(W·P)` is correct as stated and
is not accompanied by measured peak memory.

## What is not claimed here

The source's closing section suggests that trading precision for parameters
and needing only inference-sized memory could allow training models one or
two orders of magnitude larger on fixed hardware. That is the authors' future
work and nothing tests it; it does not belong in a recommendation.

Nor does this move [SOTA-154](SOTA-154.md) or support [THEORY-006](../theory.d/THEORY-006.md). It is a
post-training method that works, from inside the line, which is precisely
what that account's promotion condition says is not evidence for it.

## Known implementations

- `dibbla/Quantized-Evolution-Strategies` — the authors' released source
