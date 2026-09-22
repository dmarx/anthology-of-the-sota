---
status: Read
paper: LIT-tmp0lo8a
title: 'Fourier features'
version: 1
date: '2026-09-23'
summary: >-
  A coordinate MLP's NTK has fast spectral falloff, so it fits high
  frequencies too slowly to matter. A sinusoidal input mapping makes the
  composed kernel stationary and sets its bandwidth, and the NTK linear model
  predicts the trained networks' loss curves. Gaussian random frequencies are
  best on seven tasks, and only their scale matters. Read §1–7; the
  appendices were not read.
---

<!-- inactive-ok-file: THEORY-064 — Proposed, named as a separate account built on the same NTK spectral bias, not leaned on -->

# NOTE-tmpqp5q1: Fourier features

## Contribution

An explanation and a recipe for input encodings on coordinate networks. The
explanation turns "positional encoding helps" into "positional encoding sets
the kernel's bandwidth". The recipe replaces hand-set, log-spaced, on-axis
frequencies with sampled ones, with one scale hyperparameter.

## Key insight

**The input mapping is a kernel design knob.** Training in the NTK regime
is kernel regression, and a sinusoidal mapping turns the dot-product NTK
into a stationary convolution kernel whose width you choose. Choosing it is
a sampling-theory problem: wide enough to converge on the signal's
frequencies, narrow enough not to alias.

## Assumptions

- **The NTK regime:** infinite width, small learning rate, L2 loss, output
  near zero at initialization. The experiments use finite networks (4 layers,
  256–1024 channels, ReLU) and check the
  prediction against them
- **Low-dimensional, densely sampled inputs** (1–3D coordinates), where a
  shift-invariant kernel is the right prior
- **Per-task tuning of the scale** on held-out signals

## Key results

- **Figure 3 (1D, 32 training points, 4×1024 ReLU MLP):** the NTK linear
  model's predicted training and test loss match the observed curves. Train
  loss falls monotonically as the kernel widens, and test loss is best at an
  intermediate width (`p = 1`)
- **Figure 3c:** the high-frequency error component essentially never
  converges without a wide enough kernel
- **Figure 4:** test error against the standard deviation of the sampled
  frequencies falls on one curve for four distribution families, with
  underfitting on the left and overfitting on the right. Sixteen sampled
  features match a dense 1024-feature basis
- **Table 1:** Gaussian > positional encoding > basic > none on every task.
  3D shape IoU is 0.864 / 0.892 / 0.960 / 0.973, and MRI PSNR 26.14 / 28.58 /
  32.23 / 34.51

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Coordinate MLPs are spectrally biased because their NTK spectrum falls off fast | strong | NTK theory plus a matched prediction on trained networks (Figure 3) |
| C2 | A Fourier feature mapping makes the composed NTK stationary with a tunable bandwidth | strong | derivation (Eq. 6–8) |
| C3 | The scale of sampled frequencies, not the distribution's shape, decides performance | moderate | 1D sweeps over four families (Figure 4); higher-D in the appendix, not read |
| C4 | Gaussian RFF beats log-spaced positional encoding | moderate | Table 1, 7 tasks; the margin is small on NeRF (25.48 vs 25.28 PSNR) |

## Concepts

- **Spectral bias** — networks fit low-frequency components of a target
  before high-frequency ones
- **Stationary kernel** — `k(v₁, v₂) = h(v₁ − v₂)`, a convolution
- **Positional encoding** (in this paper) — log-linear, axis-aligned
  frequencies, the NeRF / Transformer form

## Connections

It builds on random Fourier features (Rahimi and Recht) and on NTK analyses
of spectral bias (Rahaman et al., Basri et al.). It explains NeRF's
positional encoding ([LIT-435](../literature.d/LIT-435.md)). YaRN ([LIT-193](../literature.d/LIT-193.md)) borrows its argument by
analogy for RoPE. [THEORY-064](../theory.d/THEORY-064.md) derives a transformer's low-sensitivity bias
from the same NTK spectral bias, in a different setting.

## Recommendations

- **R1** — Encode low-dimensional coordinates with sinusoids of sampled
  frequencies, and tune the scale on held-out data. *Topic:*
  representation-and-encoding. *Strength:* moderate. Filed as [SOTA-tmpwa18v](../practices.d/SOTA-tmpwa18v.md)

## Bearing on the record

- **[LIT-435](../literature.d/LIT-435.md)** (NeRF): this is the explanation for its "positional encoding
  is necessary" finding
- **[SOTA-205](../practices.d/SOTA-205.md)** replaces the coordinate MLP with explicit structures such as
  hash grids. Those are another way to give the network high-frequency
  capacity, and this paper's account covers why they are needed
- **[THEORY-tmpwobgx](../theory.d/THEORY-tmpwobgx.md)** is filed from this paper

## Limitations

- **The theory is kernel-regime.** It is checked on 1D toy signals at large
  width, and the real-task results are empirical
- **Per-task, per-dataset scale tuning**, which is the method's one
  hyperparameter and has to be searched
- **The NeRF task is simplified** (no hierarchical sampling, no view
  dependence), and there the gap over positional encoding is 0.2 dB

## Open questions

- How far the account carries outside the lazy regime, into networks whose
  features move
