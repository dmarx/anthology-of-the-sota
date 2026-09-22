---
number: 331
status: Active
formerly:
- SOTA-tmpwa18v
title: 'Pass low-dimensional coordinate inputs through sinusoids of sampled frequencies before an MLP, and tune the frequency scale rather than the distribution'
version: 1
tags:
- representation-and-encoding
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-550
- LIT-435
introduced_by:
- LIT-550
consensus: converged
consensus_note: >-
  Converged for the general move: sinusoidal encoding of coordinate inputs
  is standard in coordinate networks after NeRF (LIT-435), which found it
  necessary, and the record's diffusion notes carry the same idea on other
  inputs (LIT-446). The specific instruction, random Gaussian frequencies
  over log-spaced axis-aligned ones, rests on this paper's Table 1, where
  the margin over positional encoding is sometimes small.
implementations:
- NeRF
summary: >-
  Tancik et al. (2020), [LIT-550](../literature.d/LIT-550.md), with NeRF ([LIT-435](../literature.d/LIT-435.md)) — an MLP on raw
  coordinates never fits high frequencies. Map the input to
  `[cos 2πBv, sin 2πBv]` with `B ~ N(0, σ²)` and tune `σ` on held-out data:
  too small blurs, too large aliases, and the distribution's shape does not
  matter. Gaussian features beat no mapping and log-spaced positional
  encoding on all seven image, shape, CT, MRI and view-synthesis tasks
  tested.
explained_by:
- THEORY-077
---

<!-- inactive-ok-file: SOTA-179 — Proposed, named as a practice this paper is not evidence for -->

# SOTA-331: Pass low-dimensional coordinate inputs through sinusoids of sampled frequencies before an MLP, and tune the frequency scale rather than the distribution

## Source

Tancik et al. (2020), [LIT-550](../literature.d/LIT-550.md) — read as [NOTE-296](../notes.d/NOTE-296.md). NeRF
([LIT-435](../literature.d/LIT-435.md)), from an overlapping group and published first, is the ablation
showing that the network without an encoding oversmooths. Explained by [THEORY-077](../theory.d/THEORY-077.md).

## The practice

When a network takes a **low-dimensional, densely sampled coordinate**
(pixel position, a 3D point, a time) and has to represent fine detail over
it:

- **Encode the coordinate** as `γ(v) = [cos(2πBv), sin(2πBv)]`, with the
  rows of `B` sampled from `N(0, σ²)`. The paper uses 256 frequencies. In 1D,
  16 sampled frequencies matched a dense basis
- **Tune `σ` on held-out data, per task.** It is the only thing that
  matters: Gaussian, uniform, log-uniform and Laplacian samplings give the
  same error curve against the frequencies' standard deviation. Too small
  and high frequencies never converge. Too large and the fit aliases
- **Prefer sampled frequencies to NeRF-style log-spaced, axis-aligned
  ones.** Axis-aligned frequencies favour content along the axes. Gaussian
  won every task in Table 1, though on simplified NeRF only by 0.2 dB

| task | none | basic | positional enc. | Gaussian |
|---|--:|--:|--:|--:|
| 2D natural images (PSNR) | 19.32 | 21.71 | 24.95 | 25.57 |
| 3D shape (IoU) | 0.864 | 0.892 | 0.960 | 0.973 |
| 3D MRI (PSNR) | 26.14 | 28.58 | 32.23 | 34.51 |
| simplified NeRF (PSNR) | 22.41 | 23.16 | 25.28 | 25.48 |

## Conditions

- **Low input dimension.** The argument and the evidence are for 1–3D
  inputs, where the data is dense and a shift-invariant kernel is the
  right prior. It says nothing about token embeddings or high-dimensional
  features
- **It is not a reason to keep a large coordinate MLP.** [SOTA-205](SOTA-205.md)
  recommends replacing one with an explicit structure and a small decoder,
  which is another way of buying high-frequency capacity. This practice is
  about the encoding when an MLP does read coordinates
- **Not evidence for RoPE practices.** YaRN's analogy between RoPE and
  Fourier features does not make this paper a source for [SOTA-151](SOTA-151.md) or
  [SOTA-179](SOTA-179.md)

## Known implementations

- NeRF (log-spaced positional encoding, the form this generalizes)
