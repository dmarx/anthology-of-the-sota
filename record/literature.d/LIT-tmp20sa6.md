---
status: Active
title: 'Understanding Optimization in Deep Learning with Central Flows'
version: 1
tags:
- training-optimization
date: '2026-09-20'
published: '2024-10-01'
arxiv: '2410.24206'
first_author: 'Cohen'
keywords:
- 'edge-of-stability'
- 'central-flow'
- 'sharpness'
- 'adaptive-optimizers'
- 'implicit-regularization'
implementations: []
summary: >-
  Cohen et al. (2024), [ARXIV-2410.24206](https://arxiv.org/abs/2410.24206). The trajectory an optimizer
  actually takes oscillates at the edge of stability; its time-average is a
  differential equation — the central flow — that predicts the real
  trajectory numerically. Reading it: at the edge of stability the learning
  rate does not set the step size, and adaptive optimizers do not merely
  adapt to curvature, they steer away from it so they can take larger steps.
---

# LIT-tmp20sa6: Understanding Optimization in Deep Learning with Central Flows
<!-- inactive-ok-file: THEORY-013 — Rejected, and named to say the record's only prior account of optimizer dynamics is one it does not believe -->
<!-- inactive-ok-file: THEORY-tmpmurnt — Proposed, and filed in this same contribution from this note -->

## Key takeaways

- **The object of study is the time-average, and that is the contribution.**
  Full-batch training oscillates at the edge of stability, and the
  oscillations have resisted fine-grained analysis for years. Modelling the
  *smoothed* trajectory as a differential equation turns out to predict the
  real long-run trajectory of generic networks to high numerical accuracy.
  The oscillations affect the macroscopic path only through their covariance,
  not their detail.
- **At the edge of stability the learning rate does not set the step size.**
  For Scalar RMSProp the oscillatory dynamics drive the effective step size
  to the largest stable value at the current weights — a quantity set by the
  current *sharpness*. The learning rate's only role in the time-averaged
  trajectory is to modulate the strength of an implicit sharpness penalty.
- **Acceleration via regularization.** Adaptive optimizers implicitly
  penalise curvature, which steers the trajectory into low-curvature regions
  where larger steps are stable. Ablating the curvature-shaping while
  keeping the step-size adaptation makes the optimizer **slower**: it
  navigates into sharper regions and takes smaller steps. So a larger
  learning rate accelerates through an indirect route — it does not buy a
  bigger step now, it buys a flatter region later.
- **Oscillatory first-order methods are implicitly second-order.** When a
  first-order optimizer oscillates it picks up second-order information for
  free, at no extra gradient queries. The authors offer this as a partial
  explanation for a standing puzzle: why no explicitly second-order optimizer
  has consistently beaten the first-order adaptive ones.
- **Third-order Taylor expansions are necessary.** Second-order expansions
  cannot see the negative feedback by which oscillation triggers curvature
  reduction, and cannot see acceleration via regularization either.
- Full-batch (deterministic) training throughout.

## Standing in the anthology

**The record has 29 explanations and almost nothing about what an optimizer's
trajectory does.** The nearest thing was [THEORY-013](../theory.d/THEORY-013.md), which is `Rejected` —
it claimed the SGD noise scale selects minima that generalise, and a 35-workload
sweep found the effect disappears once metaparameters are retuned. So the
record's only account of optimizer dynamics is one it does not believe, and
it was about the stationary distribution rather than the path in any case.

Edge of stability is among the most-replicated empirical findings about
neural optimization of the last five years and there was no document for it.

**It reframes what a learning rate is**, which touches a large part of the
registry. Every schedule practice the record holds — warmup, decay,
warmup-stable-decay — treats the learning rate as setting how far the
optimizer moves. At the edge of stability it does not: sharpness does, and
the learning rate sets how hard the trajectory is pushed toward flatness.
Neither reading makes the schedules wrong; they make them advice about a
different quantity than their prose says. [THEORY-tmpmurnt](../theory.d/THEORY-tmpmurnt.md) is that account.

**It bears on the optimizer line the record spent a week on.** [THEORY-024](../theory.d/THEORY-024.md)
says orthogonalising the update is dualising it, and that muP and Shampoo
approximate one duality map. This says something adjacent and independent:
that first-order methods pick up second-order information by oscillating, for
free. Both are answers to "why does the second-order story keep almost
working", from different directions, and neither cites the other.

What it does not cover is stochastic training. Everything here is full-batch,
and the record's practices are not — which is the boundary [THEORY-tmpmurnt](../theory.d/THEORY-tmpmurnt.md)
has to state rather than blur.
