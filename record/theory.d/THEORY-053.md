---
number: 53
status: Proposed
formerly:
- THEORY-tmphpdiq
promote_when: >-
  The projection reading shown to hold for a **learned** denoiser rather than
  an exact posterior-mean one — a measurement of how far `D(x)` sits from the
  nearest feasible point for a trained model on data whose feasible set is
  known independently, and whether the projected-gradient behaviour survives
  that gap. The authors name misspecification as future work and it is the
  entire distance between the theorem and the thing anyone runs. What would
  not settle it: another guidance method that works better and cites the
  denoiser-as-projection intuition, which is the explanation being tested
  rather than evidence for it.
title: 'The Stein posterior-mean denoiser acts as an approximate projection onto the learned data geometry'
version: 1
tags:
- generative-modeling
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-490
explains:
- SOTA-301
summary: >-
  Zhang et al. (2026), [LIT-490](../literature.d/LIT-490.md) — `D(x) = E[x₀ | x]` maps a noisy
  point toward the data support, and where the clean data lie on a linear
  subspace, inside a compact convex set, or on a compact smooth submanifold,
  the paper bounds its distance from the corresponding projection. The
  reverse process then reads as a time-varying inexact projected-gradient
  method rather than as sampling with a nudge.
---

<!-- inactive-ok-file: SOTA-301 — Proposed, filed in this same
     contribution; this theory declares `explains:` on it, so the citation is
     the relation itself and cannot wait on the practice being settled -->

# THEORY-053: The Stein posterior-mean denoiser acts as an approximate projection onto the learned data geometry

## Source

Zhang, Zhang, Zardini, Amin and Ozdaglar (2026), [LIT-490](../literature.d/LIT-490.md) §§3–6 —
read as [NOTE-239](../notes.d/NOTE-239.md).

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-301](../practices.d/SOTA-301.md) | apply the objective gradient before the denoiser, not after | you are not adding a prior to an optimizer, you are *running* an optimizer — the denoiser is the projection step, so the ordering is not a preference but the difference between projected and unprojected gradient descent |

## The account

A diffusion sampler already computes `D(x) = E[x₀ | x]` at every reverse
step, via Tweedie–Miyasawa from the score. If the clean data lie on or near a
structured set `C`, that expectation is pulled toward `C` — which is what a
projection does.

The paper makes the analogy quantitative in three cases and the cases were
chosen to span what "feasible set" usually means: a **linear subspace**
(latent structure), a **compact convex set** (explicit constraints, possibly
nonsmooth), and a **compact smooth submanifold** (the generic
low-dimensional-data story). In each it bounds the gap between `D` and the
corresponding projector.

**The consequence is a reclassification rather than a new algorithm.** With
`D` read as an inexact projection, the guided reverse process is a
time-varying inexact projected-gradient method, and the standard machinery
applies: geometric contraction for strongly convex objectives, a best-iterate
rate for smooth nonconvex ones. What had been a heuristic nudge acquires the
guarantees of an optimization method — and, more usefully, acquires an
explanation of when it fails, namely when the correction step is placed
where it cannot correct.

## Why `Proposed`

**Because the proofs assume the denoiser is exact.** They are about
`E[x₀ | x]`, and what anyone runs is a network trained to approximate it. The
paper is straightforward about this: projection-error terms can absorb
learned-score error, and a full treatment of misspecification is left to
future work. That gap is not a technicality — the whole claim is that this
particular operator has a geometric property, and the operator in the theorem
is not the operator in the code.

**Because the geometry is assumed to be represented faithfully.** The
feasible set is whatever the learned support says it is. If the model has
mass off the true feasible set, the "projection" projects onto the wrong
thing, and nothing in the analysis notices.

**Because the setting is narrow.** Deterministic DDIM, variance-exploding
diffusion, an exponentially decaying noise schedule. The paper says other
samplers require tracking their own relaxation and denoising errors, which is
an honest way of saying the result does not transfer as written to most
deployed configurations.

**Because the supporting evidence is indirect.** The experiments show the
*practice* works and that the alternative fails in the way this account
predicts. They do not measure the projection property itself.

## What it does not say

**It does not say the denoiser is a projection.** It bounds the distance
between them under stated conditions. The word "approximate" is carrying
weight, and how much depends on the noise level, the geometry's curvature
and the denoiser's error — all of which the bounds expose and none of which
is estimated for a real model here.

**It does not license reading every denoiser as a constraint mechanism.**
The argument needs the clean data to actually concentrate on a structured
set. For a diffusion model over natural images the "feasible set" is not a
manifold anyone has characterized, and the theory says nothing about that
case even though the intuition is often extended to it.

**It says nothing about whether the learned geometry is the one you want.**
Projection onto the training distribution's support is a feasibility
guarantee only to the extent that the training data were feasible — which is
an assumption about the dataset, not a property of the method.
