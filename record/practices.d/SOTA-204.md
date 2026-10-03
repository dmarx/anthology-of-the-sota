---
number: 204
status: Proposed
formerly:
- SOTA-tmpbgyvj
promote_when: >-
  An independent group reporting an ablation in which a coarse-to-fine
  discretisation schedule is compared against a fixed discretisation on the
  same training run, in a setting other than consistency training, with the
  bias/variance account tested rather than assumed.
consensus: contested
contested_by:
- LIT-tmpt5h4h
consensus_note: >-
  Contested by sCM (LIT-tmpt5h4h). Its continuous-time consistency model
  removes the step count instead of scheduling it, and beats every fixed
  discretisation N it tried. That is one setting, distillation started from
  a pretrained diffusion model. A second instance, iCT (LIT-tmpnrsms),
  compares the doubling curriculum against constant N and four other shapes
  and finds it best. It shares the source's first author and method, so the
  practice is still one line's finding. Read as of 2026-10.
title: 'Anneal a discretisation from coarse to fine over training rather than fixing it'
version: 2
history:
- version: 2
  date: '2026-10-03'
  note: >-
    iCT (LIT-tmpnrsms) added as a second source: it runs the curriculum
    against a constant step count and other shapes, which the original
    lacked. sCM (LIT-tmpt5h4h) recorded under contested_by: continuous time
    beats every fixed N, so the count need not be scheduled at all.
    Consensus set to contested. promote_when is not met, because iCT is the
    same author and the same method. Status unchanged.
tags:
- training-optimization
- generative-modeling
date: '2026-09-10'
source:
- LIT-093
- LIT-tmpnrsms
introduced_by:
- LIT-093
summary: >-
  Song et al. (2023), [LIT-093](../literature.d/LIT-093.md). Where a training loss approximates a
  continuous target through a step count, that count is a bias/variance dial:
  few steps give a biased but low-variance target early, many steps a faithful
  but noisy one later.
---

# SOTA-204: Anneal a discretisation from coarse to fine over training rather than fixing it

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
different object, and until 2026-10 this was the only instance the record
held. One instance of a general-looking mechanism is how an over-general
practice gets filed, so it waits. The second instance, below, is the same
method from the same author, so it still waits.

## The comparison it lacked, and a counter

iCT ([LIT-tmpnrsms](../literature.d/LIT-tmpnrsms.md)) runs the comparison the source did not. In consistency
training from random weights on CIFAR-10, a curriculum that doubles N from
10 to 1,280 at fixed intervals beats a constant N and four other shapes
(square-root, linear, square and cosine) with the same endpoints (its Fig.
3c). FID improves as a power law in N until it saturates. It is one setting,
curves, one run each, and its bias/variance reasoning is carried over from
the source rather than tested. Song is first author of both.

sCM ([LIT-tmpt5h4h](../literature.d/LIT-tmpt5h4h.md)) contests the premise. Its continuous-time consistency
model removes the discretisation rather than annealing it. Discrete-time
models improve as N rises to 1,024 and then degrade from numerical
precision, and the continuous-time model beats every N tried (its Fig. 5c,
App. E). If the continuous target is trainable, there is no step count to
schedule. Its run is a distillation started from a pretrained diffusion
model, in one setting, so it does not test training from random weights,
which is where iCT found the curriculum mattered. It compares against fixed
N, not against a schedule.
