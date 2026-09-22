---
status: Proposed
title: 'Training and test loss disagree as functions of weight norm, and shrinking the norm through the gap is what takes so long'
version: 1
tags:
- model-stability
- analysis-and-evaluation
- training-optimization
date: '2026-09-22'
source:
- LIT-tmpkn1i6
promote_when: >-
  The LU picture is shown to hold along an actual optimization trajectory
  rather than on a landscape reduced by minimizing over angular directions at
  each norm — and, in the same work, reconciled with a grokking run in which
  the parameter norm rises (LIT-tmp069e7), either by showing that run is not
  LU-type or by showing the reduced landscape still governs it.
summary: >-
  Liu, Michaud and Tegmark's "LU mechanism" ([LIT-tmpkn1i6](../literature.d/LIT-tmpkn1i6.md)). Reduce training and
  test loss by minimizing over angular directions at each weight norm: training
  loss is L-shaped, falling and then flat near zero, while test loss is
  U-shaped with a minimum at a critical norm. A model initialized above that
  norm fits immediately and generalizes only as regularization walks the norm
  back down, which is slow — hence the delay. `Proposed`: it predicts the
  right dependence on weight decay, and [LIT-tmp069e7](../literature.d/LIT-tmp069e7.md) exhibits grokking in which
  the norm goes the other way.
corrected_by:
- THEORY-tmplnntp
---

# THEORY-tmpz9vjh: Training and test loss disagree as functions of weight norm, and shrinking the norm through the gap is what takes so long

## The account

Write any loss as a function of the weight norm `w = ‖w‖₂` and an angular
direction, and define the *reduced* loss by minimizing over directions at fixed
norm. Then:

- **Reduced training loss is "L"-shaped.** It falls as the norm grows and then
  stays near zero, because at any sufficiently large norm an overparameterized
  network can fit a small training set.
- **Reduced test loss is "U"-shaped**, with a minimum at a critical norm `w_c`
  — the "Goldilocks zone".

Above `w_c` the two disagree: training loss says done, test loss says no. A
model initialized there fits fast and sits. Only weight decay — or implicit
regularization — moves the norm back toward `w_c`, and that walk is slow.
Grokking is the walk.

With weight decay `γ`, the reduced training landscape becomes
`l̃_train(α) + γα²C²`, which gives the quantitative signature: **time to fit is
independent of `γ`, time to generalize is inversely proportional to it.**

## What supports it

- The `γ`-dependence is measured and matches, in the teacher–student model at
  large initialization `α = 2.0`.
- Small initializations (`α = 0.5`) generalize fast at every `γ`, as the
  picture requires — there is no gap to cross.
- At `α = 2.0`: `γ = 0` never generalizes, small `γ` groks, large `γ`
  generalizes quickly.
- The picture predicts where to look to *make* grokking happen, and the
  predictions worked on MNIST, IMDb and QM9. That the recipe was derived from
  the mechanism is the account's best argument.
- [LIT-085](../literature.d/LIT-085.md) independently reports the weight norm rising during memorization and
  then dropping below its initial value as the model generalizes.

## Why it is `Proposed`

**A landscape is not a trajectory.** The reduced loss minimizes over angular
directions at each norm. That is a well-defined object; it is not the path the
optimizer takes, and the inference from the shape of one to the timing of the
other is the step carrying the argument.

**And there is a counterexample.** [LIT-tmp069e7](../literature.d/LIT-tmp069e7.md) groks on modular arithmetic
with a two-layer MLP, **no weight decay**, and a weight norm that *rises*
through the transition. If there is no regularization there is no walk down,
and if the norm increases the model is moving away from `w_c` rather than
toward it. The account cannot be the general mechanism.

It is not `Rejected`, and the distinction matters. The counterexample shows the
LU walk is not *necessary* for grokking. It does not touch the runs where the
norm does come down — which [LIT-085](../literature.d/LIT-085.md) observed independently — nor the
`γ`-dependence, nor the induce-and-eliminate experiments, which no one
disputes and which are filed under [THEORY-tmpdlyut](THEORY-tmpdlyut.md) rather than here.
