---
status: Active
title: 'Batch normalization helps by smoothing the optimization landscape, not by reducing internal covariate shift'
version: 1
tags:
- model-stability
date: '2026-09-15'
source:
- LIT-223
- LIT-002
explains:
- SOTA-020
- SOTA-006
corrects:
- THEORY-tmp69thf
summary: >-
  Santurkar et al. (2018), [LIT-223](../literature.d/LIT-223.md) — the distributional stability batch
  normalization was named after turns out not to be what it does. Injecting
  covariate shift back in after the BN layer costs nothing; what BN changes
  is the smoothness of the loss surface, and other normalisations that do
  nothing for covariate shift change it comparably.
---

# THEORY-tmpn1kz1: Batch normalization helps by smoothing the optimization landscape, not by reducing internal covariate shift

## Source

<!-- inactive-ok-block: THEORY-tmp69thf — Rejected, and named here as the
     account this one replaces; that is what the citation is for. -->
Santurkar, Tsipras, Ilyas and Madry (2018), [LIT-223](../literature.d/LIT-223.md). The account it replaces
is [THEORY-tmp69thf](THEORY-tmp69thf.md), published with the technique itself in [LIT-002](../literature.d/LIT-002.md).

## What was actually shown

The experiment that carries the paper is a subtraction. Take a network with
batch normalization, and immediately after each BN layer inject noise drawn
to be non-zero-mean and time-varying — deliberately restoring the
distributional instability BN was introduced to remove. If the received
explanation were right, this should undo the benefit. It does not: the
network trains about as well as the undisturbed one.

What the paper offers instead is a property of the objective rather than of
the activations. BN "makes the optimization landscape significantly smoother.
This smoothness induces a more predictive and stable behavior of the
gradients" — the gradient at a point remains a good guide over a longer step,
which is what makes a larger step safe.

The strongest part of the argument is the third result rather than the
second, because it separates the property from the technique: other
normalisations, including ones that do nothing at all for covariate shift,
produce comparable smoothing and comparable gains.

## What this explains, and how much

It is the mechanism under [SOTA-020](../practices.d/SOTA-020.md). Bjorck et al.'s claim is that permitting
a much larger learning rate is BN's central benefit; this says *why* a larger
rate becomes usable, and the two are the same finding approached from the
measurement and from the surface.

It bears on [SOTA-006](../practices.d/SOTA-006.md) more weakly and the difference is worth being explicit
about. That practice's argument for LayerNorm in sequence models is about
cross-example dependence and inference-time statistics, and stands on its own
without any of this. What the third result adds is the reassurance the
argument needs at its far end: substituting a normalisation that does nothing
for covariate shift is not giving up the thing BN was for, because covariate
shift was not the thing BN was for.

## What this does not say

It does not say the smoothing is proven to be the cause. The paper's evidence
is a refutation of one explanation plus a positive measurement consistent with
another, and a landscape property that correlates with trainability is the
same shape of claim as [SOTA-012](../practices.d/SOTA-012.md) — worth acting on, not a mechanism derived
from first principles.

It does not retire the technique or any practice that rests on it. Batch
normalization works; the record's position is that it works for a reason other
than the one it was published with, which is a thing [DP-003](../../docs/design-principles.md#dp-3) exists to let this
record say.
