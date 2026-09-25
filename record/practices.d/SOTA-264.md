---
number: 264
status: Proposed
formerly:
- SOTA-tmpc0pb9
promote_when: >-
  A second group learning a continuous-time noise schedule against estimator
  variance and reporting the optimization speedup, or a training framework
  exposing the schedule as a learnable object rather than a configuration
  constant. What would not move it: a paper proposing a better hand-designed
  schedule, which is the activity this practice says is aimed at the wrong
  target.
consensus: unreplicated
consensus_note: >-
  One group, 2021, and the field went the other way — the diffusion practice
  the record holds concentrates training noise for perceptual reasons rather
  than learning a schedule for variance. That is a divergence of purpose
  rather than a contradiction. The same lab later ran the two together
  (LIT-tmpqjbx0: a perceptual weighting with a variance-motivated adaptive
  schedule, equal FID, faster in about half the runs). That is not the
  second group the promote_when asks for.
title: 'Fix the noise schedule''s endpoints against the bound and choose its shape to minimise the loss estimator''s variance'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    "Nobody has run the comparison" was no longer true once LIT-tmpqjbx0 was
    filed. It is the same lab, so the consensus stays unreplicated.
tags:
- generative-modeling
date: '2026-09-20'
source:
- LIT-446
introduced_by:
- LIT-446
implementations: []
summary: >-
  Kingma et al. (2021), [LIT-446](../literature.d/LIT-446.md) — in continuous time the bound
  depends on the schedule only through its endpoints, so the shape is free.
  Spend it: optimise the endpoints against the VLB and the shape against the
  variance of the loss estimator. Same bound, faster optimisation, and a
  low-discrepancy sampler for the time variable cuts the variance further.
explained_by:
- THEORY-027
compared_against:
- SOTA-412
---

# SOTA-264: Fix the noise schedule's endpoints against the bound and choose its shape to minimise the loss estimator's variance

## Source

Kingma et al. (2021), [LIT-446](../literature.d/LIT-446.md) — [ARXIV-2107.00630](https://arxiv.org/abs/2107.00630).

## The practice follows from the theorem

[THEORY-027](../theory.d/THEORY-027.md) says the continuous-time variational bound sees the noise
schedule only through its endpoint signal-to-noise ratios. Everything between
them is free.

**A free parameter should be spent on something.** The two endpoints get
optimized against the bound, because that is what they affect. The shape gets
optimized against the **variance of the Monte Carlo estimator of the loss** —
a target that exists only because the bound itself is indifferent to it.
Lower estimator variance means faster optimization at the same bound.

A low-discrepancy sequence for sampling the time variable, rather than i.i.d.
uniform draws, cuts the variance further and costs nothing.

## The endpoints turn out to matter a lot

The clearest evidence that this is not bookkeeping is the Fourier-feature
result. Appending high-frequency channels of the input to the denoiser buys
large likelihood improvements — **but only with a learned schedule**. Under
Ho et al.'s fixed schedule the maximum log-SNR is pinned near 8 and the
likelihood stalls above 4 bits per dimension; learning the endpoints takes it
to about 13.3 and the fine-scale features become usable.

So a hand-designed schedule was capping what the architecture could express,
in a way nobody would have found by looking at the architecture.

## Why the field did not take this up

[SOTA-188](SOTA-188.md) is the recommendation that actually propagated: concentrate the
training noise in the middle of the range, because the extremes teach little.
That is also a use of the freedom this practice establishes, aimed at a
different target — where perceptual quality comes from, rather than how fast
the bound converges.

The two are not in conflict and nobody has run them against each other. It is
an open question whether the variance-minimizing schedule and the
compute-allocating one land in the same place; two different arguments both
conclude "spend effort in the middle", which is suggestive and is not a
measurement.

## Conditions, and why this is `Proposed`

**Continuous time and the unweighted bound.** The invariance the practice
rests on is a statement about a limit. Every practical recipe the record
holds uses a weighted loss and finitely many steps, where the schedule's
shape does affect what is optimized.

Likelihood is the objective throughout — CIFAR-10 and ImageNet 64×64, bits
per dimension. The record's other diffusion practices are about perceptual
generation, where likelihood is known to be a poor proxy, and nothing here
says a variance-minimizing schedule improves samples.

One group, 2021, and no implementation in this record learns a schedule. The
variance-minimizing target is also specific to *this* estimator; how much of
the gain survives a different time-sampling strategy is unexamined, which
matters because the low-discrepancy sampler is itself one such change.

## Known implementations

- None in the record. Every diffusion model it holds uses a fixed schedule.
