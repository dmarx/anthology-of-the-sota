---
number: 9
status: Active
formerly:
- THEORY-tmp9dr37
title: "A wide two-layer network's training dynamics are a gradient flow on the distribution of its neurons, and that flow is convex"
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
source:
# Four groups, within about a year, by four routes. LIT-271 is primary:
# it gives the PDE, the finite-N error bound, and the global-convergence
# result for the noisy case.
- LIT-271
# The interacting-particle route, which also supplies the width scaling.
- LIT-365
# The law-of-large-numbers route.
- LIT-267
# The optimal-transport route, and the only one that states an initialization
# condition a practitioner could act on.
- LIT-298
summary: >-
  Scale a two-layer network's output by 1/N and the object that moves under
  SGD stops being the weights and becomes their empirical distribution, which
  follows a Wasserstein gradient flow of the population risk. The risk is
  convex as a functional of that distribution — so the non-convexity of the
  finite-width landscape, and the permutation symmetry that produces most of
  its apparent local minima, are both artefacts of the coordinates. Four
  groups reached this within about a year by four routes.
---

# THEORY-009: A wide two-layer network's training dynamics are a gradient flow on the distribution of its neurons, and that flow is convex

## The claim

Write a two-layer network as an average over its `N` hidden units rather than
a sum — output scaled by `1/N`, not `1/sqrt(N)`. Then as `N` grows, the
quantity that evolves under SGD is the empirical distribution `rho` of the
hidden units' parameters, and it evolves by a deterministic partial
differential equation: a Wasserstein gradient flow of the population risk,
with a diffusion term when the SGD noise is retained.

Two things follow that are not visible at finite width.

**The population risk is convex as a functional of `rho`.** Not convex in the
weights — it is famously not — but convex in the measure. The non-convexity
of the loss surface is a fact about a coordinate system in which a single
function has `N!` representations.

**The dimension of the problem stops growing with width.** The PDE does not
depend on `N`. [LIT-271](../literature.d/LIT-271.md) bounds the gap between the finite-`N` optimum and
the measure optimum by `K/N`, and gives sample complexity independent of the
number of hidden units.

## What rests on it

The parametrization is a choice, and the choice is what the theory is about:
`1/N` gives this limit and feature learning, `1/sqrt(N)` gives the neural
tangent kernel limit ([LIT-360](../literature.d/LIT-360.md)), in which the features do not move and
training is linear around initialization. These are two scalings of the same
network and they disagree about what training is. The record files both and
this document is the one it follows for wide two-layer networks.

It also explains why permutation symmetry is not a nuisance to be engineered
around but the reason the coordinates mislead — which is the connection to
<!-- inactive-ok-block: THEORY-010 — Proposed, and this paragraph is
     about the relationship between the two accounts -->
[THEORY-010](THEORY-010.md) and, through it, to averaging weights across workers.

## Why it is `Active`

**Four groups, four routes, about a year.** [LIT-271](../literature.d/LIT-271.md) reaches it through
propagation of chaos and a direct PDE limit; [LIT-365](../literature.d/LIT-365.md) through an
interacting particle system, and adds that the approximation error scales as
`O(1/n)` in width rather than `O(1/sqrt(n))`; [LIT-267](../literature.d/LIT-267.md) through a law of
large numbers for the empirical measure; [LIT-298](../literature.d/LIT-298.md) through optimal
transport, with a global-convergence result under a separation condition on
the initialization. Independent derivations of the same limit are the evidence
this record asks for and rarely gets.

## What it does not cover

**Two layers.** Every one of the four is about a single hidden layer. The
depth-`L` analogue is not established by anything in this record, and the
networks the record's practices are about are deep.

**Infinite width and, in three of the four, infinite data.** The results are
limits with finite-`N` corrections attached. `K/N` is a good bound at width
`10^4` and says little at width `8`.

**The noise is load-bearing and is not SGD's noise.** Global convergence in
[LIT-271](../literature.d/LIT-271.md) needs an explicit added diffusion term — entropy regularization,
Langevin-style. Whether ordinary SGD's gradient noise plays that role is
assumed rather than shown, and it is the assumption the whole Langevin branch
of this record's literature exists to interrogate.
