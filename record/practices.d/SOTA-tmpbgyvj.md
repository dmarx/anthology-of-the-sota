---
status: Proposed
promote_when: >-
  An independent group reporting an ablation in which a coarse-to-fine
  discretisation schedule is compared against a fixed discretisation on the
  same training run, in a setting other than consistency training, with the
  bias/variance account tested rather than assumed.
title: 'Anneal a discretisation from coarse to fine over training rather than fixing it'
version: 1
tags:
- training-optimization
date: '2026-09-10'
source:
- LIT-093
summary: >-
  Song et al. (2023), [LIT-093](../literature.d/LIT-093.md). Where a training loss approximates a
  continuous target through a step count, that count is a bias/variance dial:
  few steps give a biased but low-variance target early, many steps a faithful
  but noisy one later.
---

# SOTA-tmpbgyvj: Anneal a discretisation from coarse to fine over training rather than fixing it

## Source

Song et al. (2023), [LIT-093](../literature.d/LIT-093.md) — Consistency Models, where the schedules
`N(.)` and `mu(.)` are reported as necessary for good performance when training
in isolation, with the bias/variance reasoning given explicitly (Fig. 3d,
Appendix C).

## The claim

When a training objective approximates a continuous target by discretising it
into steps, the number of steps is not a constant to be tuned once. It sets a
**bias/variance trade that moves over training**:

- **Coarse early.** Few steps give a target that is biased but cheap and
  low-variance, which is what an untrained model can use.
- **Fine late.** More steps give a faithful target whose extra variance a
  converged model can absorb.

Fixing the count picks one point on that trade for the whole run.

## Why this is `Proposed`

The mechanism is general — the argument names nothing specific to consistency
training, and the same shape applies anywhere a loss approximates a target
through a step count. But the evidence is **one paper, one setting**, and the
schedules there are reported as necessary rather than isolated against a
well-tuned fixed count.

The record's other schedule practices are all about learning rates
([SOTA-140](SOTA-140.md)) and batch sizes. A schedule on a *discretisation* is a
different object, and this is the only instance the record holds. One instance
of a general-looking mechanism is how an over-general practice gets filed, so
it waits.
