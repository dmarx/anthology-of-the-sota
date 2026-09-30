---
number: 332
status: Proposed
formerly:
- SOTA-tmpx07li
promote_when: >-
  An independent comparison, on a derivative-supervised task (a PDE,
  an Eikonal SDF fit, or gradient-domain reconstruction), of SIREN against a
  ReLU network with a tuned Fourier-feature encoding (LIT-550) at equal
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
- LIT-551
introduced_by:
- LIT-551
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
  Sitzmann et al. (2020), [LIT-551](../literature.d/LIT-551.md) — a sine network's derivative is
  another sine network, so gradients and Laplacians of the fit are well
  behaved where a ReLU network's second derivative is zero. Initialize
  hidden weights U(±√(6/n)) and scale the first layer by ω₀ = 30 (tune it to
  the signal), or deep sine networks do not train. It fits images, video,
  SDFs and PDE solutions from derivative supervision.
explained_by:
- THEORY-078
---

<!-- inactive-ok-file: THEORY-078 — Proposed, filed in this same contribution as the account of this practice's initialization -->

# SOTA-332: When an implicit representation will be supervised through its derivatives, use sine activations with the SIREN initialization rather than a ReLU network

## Source

Sitzmann et al. (2020), [LIT-551](../literature.d/LIT-551.md) — SIREN. Read as [NOTE-295](../notes.d/NOTE-295.md). The
initialization account is [THEORY-078](../theory.d/THEORY-078.md).

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
  ([LIT-550](../literature.d/LIT-550.md), [SOTA-331](SOTA-331.md)). Which is better for derivative supervision
  is open in the record
- **The initialization is not optional**, according to the authors, but its
  necessity is asserted, not ablated ([THEORY-078](../theory.d/THEORY-078.md))

## Known implementations

- SIREN reference implementation (Stanford)
