---
number: 58
status: Proposed
formerly:
- THEORY-tmppkfku
promote_when: >-
  The saturation mechanism isolated from the estimator: activation histograms
  tracked alongside the information estimate across training, in networks
  matched on everything but how fast the nonlinearity saturates, under an
  estimator held fixed and *placed adaptively* so it cannot itself
  manufacture the effect. That would separate "activity piles into extreme
  bins" from "these bins were in the wrong place". What would NOT meet it:
  another paper reporting that `tanh` compresses and ReLU does not under one
  binning scheme. That is the observation this is an account of, and the
  record already holds it.
title: 'Apparent compression in the information plane is saturating activations collapsing into extreme bins, not information being discarded'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-21'
source:
- LIT-509
explains:
- SOTA-312
summary: >-
  Saxe et al. (2018), [LIT-509](../literature.d/LIT-509.md) — a `tanh` unit must grow its
  weights to compute anything nonlinear, and as it does its activity piles
  into the saturation regions. Under a fixed binning that is a distribution
  collapsing into two bins — about **1 bit** — which the information plane
  draws as a compression phase. `Proposed`, because
  [LIT-507](../literature.d/LIT-507.md) shows compression in *some* non-saturating networks
  once the bins are placed adaptively.
---


# THEORY-058: Apparent compression in the information plane is saturating activations collapsing into extreme bins, not information being discarded

## Source

Saxe, Bansal, Dapello, Advani, Kolchinsky, Tracey and Cox (2018),
[LIT-509](../literature.d/LIT-509.md) — read as [NOTE-253](../notes.d/NOTE-253.md).

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-312](../practices.d/SOTA-312.md) | state the noise or binning assumption and show the conclusion survives changing it | there is a concrete, understood mechanism by which the assumption and the activation function jointly manufacture a phase that nothing in the learning corresponds to |

## The account

A `tanh` network initialized with small weights is, near the origin, a linear
network. To compute anything nonlinear it **must** grow its weights until some
inputs drive units into the saturating regions — this is not a training
accident but a requirement of the function class, and the paper argues it from
norm-based capacity bounds as well as from the histograms.

Now put a fixed grid of bins across the activation range. Early in training,
activity sits in the central, near-linear band and spreads across many bins:
high entropy. Late in training, a large fraction of inputs map to values near
`±1`, and because `tanh` is flat there, a wide range of net inputs lands in
the *same* bin. The distribution of the binned variable `T` collapses toward
two atoms — roughly a coin flip, about **1 bit**.

Since the map is deterministic, `H(T|X) = 0` and `I(T;X) = H(T)` exactly. So
the measured information falls. Nothing was discarded; the ruler stopped being
able to tell the values apart.

The minimal model makes this exact. With `X ~ N(0,1)` and `h = f(w₁X)`,
`I(T;X)` as a function of `w₁` rises then falls for `tanh` and rises without
bound for ReLU, where half the inputs land in the zero bin and the rest spread
with the weight. The ordering across four activations follows the shape of the
nonlinearity rather than anything about learning: `tanh` compresses, softsign —
double-saturating but gentler — compresses modestly, ReLU and softplus do not.

It also explains a detail the original paper reported as a separate fact: that
training slows as the compression phase begins. Saturated units pass small
gradients.

## Why `Proposed`

**[LIT-507](../literature.d/LIT-507.md) contests exactly this mechanism**, and its criticism
is specific enough to take seriously: with bins placed adaptively per layer
and epoch, some ReLU initializations do compress, so saturation would not be
necessary. That its own 50-initialization average shows no phase weakens the
objection considerably — but it does not dispose of it, because the averaging
mixes runs that compress with runs that do not, and *why* a given
initialization does either is unidentified in both papers.

**The mechanism is demonstrated in a three-neuron model and read off
histograms in the full network.** What is missing is the intermediate: the
saturation fraction tracked against the information estimate across training,
which would show the two moving together rather than merely both being
present.

**It is entangled with the very estimator dependence it is meant to explain.**
The account says a fixed binning cannot resolve the saturation region — which
is true, and is also why a differently placed binning removes the effect
([LIT-509](../literature.d/LIT-509.md)'s own Appendix C). Distinguishing "saturation caused
this" from "this binning was in the wrong place" needs the control the
`promote_when` asks for, and neither paper ran it.

## What it does not say

**It does not say representations never discard input information.** They
demonstrably do: partition the input into task-relevant and task-irrelevant
dimensions and the information about the irrelevant subspace falls during
training. What fails is the claim that this appears as a second phase in
*total* input information — it happens concurrently with fitting, while
`I(X;T)` overall rises.

**It does not explain generalization, and does not need to.** The
compression-causes-generalization claim is refuted independently, by a
dissociation in all four combinations and — separately and from the other
side of the argument — by [LIT-507](../literature.d/LIT-507.md) finding no significant
correlation between hidden-layer compression and generalization.

**It is not [SOTA-200](../practices.d/SOTA-200.md)'s mechanism.** There, a real underlying quantity
is made to look discontinuous by a thresholding metric. Here the underlying
quantity is infinite and the reported one is an artifact in full. Both are
instances of a measurement producing the finding, and they are not the same
thing happening twice — [DP-009](../../docs/design-principles.md#dp-9).

**It does not refute the information bottleneck principle.** The principle is
more general than the scheme tested here, and the source says so explicitly.
Where a network is genuinely stochastic, the mutual information is a property
of the model and this account has no purchase on it.
