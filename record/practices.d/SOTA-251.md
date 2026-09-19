---
number: 251
status: Proposed
formerly:
- SOTA-tmpzrzg8
consensus: unreplicated
consensus_note: >-
  One paper, one measurement, one domain. It is filed Proposed rather than
  Active because the 8x figure is video-specific and nobody has run the same
  trade on text sequence length, which is where it would matter most to this
  record.
title: 'Train at low resolution and raise it only during the decay phase of a warmup-stable-decay schedule'
version: 1
tags:
- training-optimization
- vision-and-graphics
date: '2026-09-19'
promote_when: >-
  Somebody runs the same trade on a second axis or in a second lab — text
  sequence length being the obvious one for this record, since SOTA-151
  already treats context extension as a separate later stage. One projected
  8x in one video recipe is a reason to try it, not yet a reason to
  recommend it.
source:
- LIT-215
introduced_by:
- LIT-215
extends:
- SOTA-140
implementations:
- V-JEPA 2
summary: >-
  Assran et al. (2025), [LIT-215](../literature.d/LIT-215.md) — [ARXIV-2506.09985](https://arxiv.org/abs/2506.09985). Spend warmup and
  the constant phase on short, low-resolution clips; raise resolution and clip
  length only in the final decay. Up to 8x less pretraining compute than
  training at full resolution throughout, for the same end state.
---

# SOTA-251: Train at low resolution and raise it only during the decay phase of a warmup-stable-decay schedule

## Source

Assran et al. (2025), [LIT-215](../literature.d/LIT-215.md) — [ARXIV-2506.09985](https://arxiv.org/abs/2506.09985).

## The rule

The expensive axis of an input — resolution, frames per clip, sequence
length — does not have to be constant across training. Hold it low through
warmup and the constant phase, then raise it during the decay.

Measured: **252K iterations at 16 frames and low resolution, then 12K
cooldown iterations at raised resolution.** Against the projected cost of
training at full resolution throughout, that is **up to an 8x speedup** in
GPU-days for a ViT-g.

## Why the decay phase specifically

This is what makes it a rule rather than a trick, and it is why the practice
extends [SOTA-140](SOTA-140.md) rather than standing alone. A warmup-stable-decay schedule
already concentrates the *learning-rate* commitment into a short final
window: the constant phase explores, the decay converges. The observation
here is that the decay phase is also the right place to pay for input
fidelity — the model spends most of its steps learning what to look for at
low cost, and the expensive representation is trained only where the weights
are settling.

The dependency runs the right way: without a schedule that has a decay phase,
there is no principled place to put the resolution increase, which is why
this is stated against `SOTA-140` and not against cosine.

## What else that paper's sweep says, and what it does not license

The same section attributes its gains separately, which is unusually clean:

| change | gain |
|---|---|
| data 2M → 22M videos | +1.0 |
| model 300M → 1B (ViT-g/16) | +1.5 |
| training 90K → 252K iterations | +0.8 |
| spatial resolution and clip length ↑ | to 88.2%, +4.0 cumulative |

Those are reasons to believe the resolution axis matters, **not** evidence
for this scheduling rule — they are about the end state, and the rule is
about how to get there cheaply. The 8x is the number this practice rests on.

A second simplification from the same recipe is deliberately **not** filed:
fixed teacher EMA and weight-decay coefficients in place of ramp-up
schedules, reported as having "minimal impact". A null result about two
hyperparameters in one recipe is not a recommendation.

## Conditions

- **Video pretraining, one model family, one lab.** The 8x is ViT-g on A100s
  under V-JEPA 2's recipe
- **Needs a schedule with a distinct decay phase** — see above
- **Untested on text.** The obvious analogue is sequence length, where the
  record already recommends long-context extension as a separate later stage
  ([SOTA-151](SOTA-151.md)). Whether that is the same rule or a different one is open, and
  is the reason this is `Proposed`
