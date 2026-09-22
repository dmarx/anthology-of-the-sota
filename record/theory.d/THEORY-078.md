---
number: 78
status: Proposed
formerly:
- THEORY-tmpx6puj
promote_when: >-
  A training comparison, not a statistics check at initialization: deep
  sine networks under standard initializations (Xavier, Kaiming, or the
  uniform schemes earlier periodic networks used) against the SIREN scheme,
  at several depths, showing that the standard ones fail to train or
  converge badly and that the failure tracks the predicted drift in
  activation distribution or frequency. Another demonstration that SIREN
  trains well does not settle it. The claim is about why the others did not.
title: 'Deep sine networks train when initialization holds every pre-activation near a standard normal, which keeps each layer arcsine-distributed and frequency growth slow; that initialization is what earlier periodic networks lacked'
version: 1
tags:
- model-stability
- model-architecture
date: '2026-09-23'
source:
- LIT-551
explains:
- SOTA-332
summary: >-
  Sitzmann et al. (2020), [LIT-551](../literature.d/LIT-551.md) — with weights U(±√(6/n)), a sum of
  arcsine inputs is about N(0,1), and a unit normal through sin is arcsine
  again, so every layer sees the same distribution and few pre-activations
  exceed π. The mechanism is verified at initialization for 6 and 50
  layers. The historical claim, that this is why periodic activations
  "failed to robustly outperform" before, is not tested.
---

<!-- inactive-ok-file: SOTA-332 — Proposed, filed in this same contribution as the practice this account explains -->

# THEORY-078: Deep sine networks train when initialization holds every pre-activation near a standard normal, which keeps each layer arcsine-distributed and frequency growth slow; that initialization is what earlier periodic networks lacked

## Source

Sitzmann et al. (2020), [LIT-551](../literature.d/LIT-551.md) — read as [NOTE-295](../notes.d/NOTE-295.md). Filed for
`#163`'s question: why did people struggle to get periodic activations to
work?

## What it explains

| document | what it says | what this says it is |
|---|---|---|
| [SOTA-332](../practices.d/SOTA-332.md) | use sine activations with the SIREN initialization | the initialization is what makes the architecture trainable |

## The account

A sine is not like ReLU or tanh. Its output distribution depends sharply on
how many periods the input spans, and its frequency content multiplies
through depth when inputs are large. Two failure modes follow. If
pre-activations are too small, `sin` is nearly linear and the network
collapses toward a linear map. If they are too large, each layer folds the
signal many times, frequencies compound with depth, and the function is
noise.

The SIREN scheme puts every layer on a fixed point. Inputs that span more
than half a period of the sine come out arcsine-distributed. A dot product
of `n` such outputs with weights `U(±c/√n)` tends to `N(0, c²/6)`, which
has unit variance at `c = √6`. A unit normal through `sin` is arcsine
again. So the distribution is depth-invariant, and because few
pre-activations exceed `π`, each layer changes spatial frequency only
slightly. The first layer is the exception: scaled by `ω₀ = 30`, it is
where the signal's frequency range is chosen.

## What was actually shown

- **The fixed point is real.** Activation histograms match the predicted
  normal and arcsine laws layer by layer at 6 layers and 2048 width, and
  also at 50 layers. Gradient statistics stay constant with depth
  (supplement §1.4). This could have failed and did not
- **That the scheme trains well** is shown across every experiment in the
  paper

## What this does not say

**It does not show that other initializations fail.** The paper's only
evidence on that is one sentence: SIRENs built "with not carefully chosen
uniformly distributed weights yielded poor performance". There is no
training ablation. The second half of the title, that this is what earlier
work lacked, rests on the related-work framing, not on a test. Much of the
earlier work cited was shallow (single-hidden-layer Fourier networks) or
recurrent, where a depth-propagation argument may not be what went wrong.

**It does not formalize frequency growth.** The authors say that doing so
"proves to be a hard task and is out of the scope of this work". The
"grows only slowly" part is an empirical FFT at initialization.

**It says nothing about training dynamics beyond initialization.** The
distributions are shown at step zero.

## Why `Proposed`

The mechanism is derived and verified at initialization, which is
necessary for the claim and not enough for it. What the `#163` item asks,
why periodic activations struggled, is a claim about counterfactual
initializations, and nothing in the record has tested one.
