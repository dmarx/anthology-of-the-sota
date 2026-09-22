---
status: Active
title: "A coordinate MLP learns high frequencies slowly because its tangent kernel's spectrum falls off fast, and a sinusoidal input mapping works by making that kernel stationary with a bandwidth you choose"
version: 1
tags:
- representation-and-encoding
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmp0lo8a
explains:
- SOTA-tmpwa18v
summary: >-
  Tancik et al. (2020), [LIT-tmp0lo8a](../literature.d/LIT-tmp0lo8a.md) — in the NTK regime, error along each
  kernel eigenvector decays at a rate set by its eigenvalue, and a coordinate
  MLP's eigenvalues fall off fast with frequency. Sinusoids of the input give
  a stationary composed kernel whose bandwidth the frequencies set. The
  linear model predicts trained networks' loss curves. It is a kernel-regime
  account of an input encoding, not of feature learning.
---

<!-- inactive-ok-file: SOTA-179 — Proposed, named as a practice this account deliberately does not explain -->

# THEORY-tmpwobgx: A coordinate MLP learns high frequencies slowly because its tangent kernel's spectrum falls off fast, and a sinusoidal input mapping works by making that kernel stationary with a bandwidth you choose

## Source

Tancik et al. (2020), [LIT-tmp0lo8a](../literature.d/LIT-tmp0lo8a.md) — read as [NOTE-tmpqp5q1](../notes.d/NOTE-tmpqp5q1.md).

## What it explains

| document | what it says | what this says it is |
|---|---|---|
| [SOTA-tmpwa18v](../practices.d/SOTA-tmpwa18v.md) | encode coordinates with sampled sinusoids, tune the scale | choosing the composed kernel's bandwidth |
| [LIT-435](../literature.d/LIT-435.md) (NeRF) | without positional encoding the result is oversmoothed | the high-frequency eigen-directions never converge |

## The account

Linearize training around initialization. With L2 loss, the training error
expressed in the NTK's eigenbasis decays componentwise, as `e^{−ηλ_i t}`. A
component with a small eigenvalue is learned slowly, and for a plain MLP on
a few input dimensions the eigenvalues fall off rapidly with frequency. So
the fine detail of an image or scene sits in directions the network, in
practice, never fits.

Now feed the MLP `γ(v)`, a vector of `cos` and `sin` of `2πb_jᵀv`. Their
inner product is `Σ a_j² cos(2πb_jᵀ(v₁ − v₂))`, which depends only on the
difference. The composed kernel is therefore **stationary**: a convolution
over the input domain, whose spectrum the `b_j` place. Wider frequencies give
a wider spectrum, faster convergence on detail, and past a point aliasing.
That is a reconstruction-filter choice, the kind signal processing already
knows how to make.

## What was actually shown

The part that could have failed: Figure 3 predicts training and test loss
from the NTK linear model and compares them with trained 4-layer,
1024-channel ReLU networks on a 1D signal. They match, including the
interior optimum of the test loss at an intermediate bandwidth, and the
per-frequency error curves decay log-linearly as Eq. 4 says. Separately,
Figure 4's collapse of four sampling distributions onto one curve against
frequency scale is what a bandwidth account predicts and a
"these particular frequencies are special" account does not.

## What this does not say

**It is not an account of feature learning.** The argument lives in the
lazy regime that [THEORY-076](THEORY-076.md) separates from feature learning. It works here
because the mapping acts on the input before anything is learned, and
because the check was made at large width. It does not say how the encoding
interacts with features that move.

**It does not transfer to attention by default.** YaRN ([LIT-193](../literature.d/LIT-193.md)) borrows it
to motivate treating RoPE's high and low frequencies differently when
extending context. That is an analogy: RoPE rotates query–key pairs inside
attention and is not an MLP's input on a dense low-dimensional domain. This
account is not listed as explaining [SOTA-151](../practices.d/SOTA-151.md) or [SOTA-179](../practices.d/SOTA-179.md).

**It does not say MLPs are the right representation.** [SOTA-205](../practices.d/SOTA-205.md) replaces the
coordinate MLP with explicit grids. The same spectral argument is one reason
those exist.

## Why `Active`

The mechanism is derived, not argued. It made a quantitative prediction
about trained networks that was checked and held, and a qualitative one
(shape does not matter, scale does) that was checked across four
distributions. It also accounts for a finding the record already holds,
NeRF's ablation. What it does not cover is listed above.
