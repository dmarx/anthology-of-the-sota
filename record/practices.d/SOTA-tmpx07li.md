---
status: Proposed
promote_when: >-
  An independent comparison, on a derivative-supervised task (a PDE,
  an Eikonal SDF fit, or gradient-domain reconstruction), of SIREN against a
  ReLU network with a tuned Fourier-feature encoding (LIT-tmp0lo8a) at equal
  size, reporting error on the derivatives and not only on values. The
  source paper compares against ReLU with positional encoding only on an
  image fit, and never against Fourier features.
title: 'When an implicit representation will be supervised through its derivatives, use sine activations with the SIREN initialization rather than a ReLU network'
version: 1
tags:
- model-architecture
- model-stability
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-tmpe1y6b
introduced_by:
- LIT-tmpe1y6b
consensus: unreplicated
consensus_note: >-
  One group's paper, widely reused as a baseline. The one outside
  measurement in the record, Image-GS (LIT-511), tests value fitting at
  fixed size, where SIREN, Fourier features and ReLU MLPs all lose to
  explicit Gaussians. That bears on SOTA-205, not on this practice's
  derivative claim.
implementations:
- SIREN
summary: >-
  Sitzmann et al. (2020), [LIT-tmpe1y6b](../literature.d/LIT-tmpe1y6b.md) — a sine network's derivative is
  another sine network, so gradients and Laplacians of the fit are well
  behaved where a ReLU network's second derivative is zero. Initialize
  hidden weights U(±√(6/n)) and scale the first layer by ω₀ = 30 (tune it to
  the signal), or deep sine networks do not train. It fits images, video,
  SDFs and PDE solutions from derivative supervision.
explained_by:
- THEORY-tmpx6puj
---

<!-- inactive-ok-file: THEORY-tmpx6puj — Proposed, filed in this same contribution as the account of this practice's initialization -->

# SOTA-tmpx07li: When an implicit representation will be supervised through its derivatives, use sine activations with the SIREN initialization rather than a ReLU network

## Source

Sitzmann et al. (2020), [LIT-tmpe1y6b](../literature.d/LIT-tmpe1y6b.md) — SIREN. Read as [NOTE-tmpncb8j](../notes.d/NOTE-tmpncb8j.md). The
initialization account is [THEORY-tmpx6puj](../theory.d/THEORY-tmpx6puj.md).

## The practice

When the loss constrains the network's **gradients or higher derivatives**,
as in a signed distance function fit with an Eikonal term, a Poisson or
Helmholtz solve, or gradient-domain image editing:

- **Use `sin` as every hidden activation.** Any derivative of a SIREN is a
  SIREN, so the derivatives are as expressive as the fit. A ReLU network's
  second derivative is zero everywhere, and tanh's derivatives were "often
  not well behaved" in the paper's comparison
- **Initialize hidden weights `U(−√(6/n), √(6/n))`.** This holds
  pre-activations near N(0, 1) at every depth
- **Scale the first layer:** `sin(ω₀ · W₀x + b₀)`, with `ω₀ = 30` in every
  experiment in the paper. It sets the frequency range, so it belongs to the
  signal, and 30 is a starting point
- **Keep inputs in `[−1, 1]`**

## What was measured

- Image fitting (Figure 1): ReLU with positional encoding matches SIREN on
  the image and not on its gradient or Laplacian. ReLU, tanh and RBF-ReLU
  miss the image too
- Video, 300 frames at 512²: 29.90 dB against 25.12 dB for ReLU
- SDF from oriented points: much finer detail than a ReLU SDF, with a room
  fit by one 5-layer network
- Poisson reconstruction from gradients or Laplacians alone, and
  Helmholtz and wave solutions

## Conditions

- **The claim is about derivatives.** For fitting values alone, the record
  prefers explicit structures ([SOTA-205](SOTA-205.md)), and an outside same-size benchmark
  ([LIT-511](../literature.d/LIT-511.md)) has SIREN losing to them
- **No comparison against Fourier features**, the concurrent input-side fix
  ([LIT-tmp0lo8a](../literature.d/LIT-tmp0lo8a.md), [SOTA-tmpwa18v](SOTA-tmpwa18v.md)). Which is better for derivative supervision
  is open in the record
- **The initialization is not optional**, according to the authors, but its
  necessity is asserted, not ablated ([THEORY-tmpx6puj](../theory.d/THEORY-tmpx6puj.md))

## Known implementations

- SIREN reference implementation (Stanford)
