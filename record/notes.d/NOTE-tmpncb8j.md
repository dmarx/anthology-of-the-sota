---
status: Read
paper: LIT-tmpe1y6b
title: 'SIREN'
version: 1
date: '2026-09-23'
summary: >-
  Sine-activated MLPs whose derivatives are well behaved, trainable
  because weights U(±√(6/n)) keep pre-activations standard normal and
  outputs arcsine at every depth, with ω₀ = 30 on the first layer. They fit
  signals and derivatives that ReLU, tanh and positional encoding do not.
  Read §1–4.2 and supplement §1; the later experiments were skimmed.
---

<!-- inactive-ok-file: SOTA-tmpx07li THEORY-tmpx6puj — both Proposed, filed in this same contribution from this paper; new, not retired -->

# NOTE-tmpncb8j: SIREN

## Contribution

A coordinate-network architecture that represents a signal's derivatives,
not only its values. That opens up fitting from derivative supervision
(Poisson, Eikonal, Helmholtz, wave). Also an initialization that makes
deep sine networks trainable, with a distributional argument for it.

## Key insight

**A sine network's statistics can be made depth-invariant.** Uniform input
through `sin` spanning more than half a period gives an arcsine output. A
weighted sum of many arcsine variables is approximately normal. With
`c = √6` (the paper writes "c = 6" and then uses `√(6/n)`), that normal
has unit variance, and a unit normal through `sin` is
arcsine again. So each layer sees the same distribution, and since few
pre-activations exceed `π`, each layer adds little new frequency.

## Assumptions

- **Width large enough for the CLT step.** Checked at 2048 units
- **Inputs normalized to `[−1, 1]`**
- **Adam** is the optimizer for all experiments
- **`ω₀ = 30` is tuned by hand** "for all the applications in this work"

## Key results

- **Figure 1 (image fit):** only ReLU with positional encoding and SIREN
  reproduce the image, and only SIREN reproduces its gradient and Laplacian
- **Video (Figure 2):** 29.90 ± 1.08 dB against 25.12 ± 1.16 dB for ReLU
- **SDFs from oriented point clouds (Figure 4):** far more detail than a
  ReLU SDF, and a whole room fit by one 5-layer network
- **Supplement §1.4:** at initialization, activations after linear layers
  match N(0, 1) and after sines match arcsine, at 6 and 50 layers, with
  constant gradient statistics

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | SIRENs represent derivatives of the fitted signal that ReLU and tanh networks do not | strong | Figure 1, Poisson reconstruction, SDF experiments |
| C2 | The initialization keeps activation distributions constant across depth | strong | derivation and a direct check at 6 and 50 layers |
| C3 | Without it, SIRENs train poorly | weak | one sentence, no ablation shown |
| C4 | Frequency grows only slowly with depth | moderate | empirical FFT at initialization; the authors say formalizing it is out of scope |
| C5 | Earlier periodic networks failed for lack of this initialization | weak | implied by the framing; not tested |

## Method

`Φ(x) = W_n(φ_{n−1} ∘ … ∘ φ_0)(x) + b_n` with `φ_i(x) = sin(W_i x + b_i)`.
Initialize `W_i ~ U(−√(6/n), √(6/n))` for hidden layers, and use
`sin(ω₀ W_0 x + b_0)` with `ω₀ = 30` for the first. The supplement notes
that factoring `W = ω₀ Ŵ` in all layers keeps the same distribution and
speeds training.

## Concepts

- **Implicit neural representation** — a network mapping coordinates to a
  signal, possibly defined only through constraints on its derivatives

## Connections

It is concurrent with Fourier features ([LIT-tmp0lo8a](../literature.d/LIT-tmp0lo8a.md)) and NeRF's
positional encoding ([LIT-435](../literature.d/LIT-435.md)), which address the same high-frequency
failure from the input side. SIREN addresses it through the activation, and
adds derivatives. Image-GS ([LIT-511](../literature.d/LIT-511.md)) later benchmarks SIREN and Fourier
features at fixed size for image fitting.

## Recommendations

- **R1** — When the fit will be supervised through its derivatives, use
  sine activations with this initialization. Filed as [SOTA-tmpx07li](../practices.d/SOTA-tmpx07li.md)
- **R2** — If you use periodic activations at all, initialize so
  pre-activations are about N(0, 1) and set the first-layer frequency to
  the signal. Part of [SOTA-tmpx07li](../practices.d/SOTA-tmpx07li.md)

## Bearing on the record

- **[SOTA-205](../practices.d/SOTA-205.md)** (explicit structures over coordinate MLPs) is about fitting
  values efficiently, and SIREN does not contest it there. Image-GS
  ([LIT-511](../literature.d/LIT-511.md)) has all the coordinate MLPs losing on value fitting
- **[THEORY-tmpx6puj](../theory.d/THEORY-tmpx6puj.md)** files the initialization account at `Proposed`

## Limitations

- **No initialization ablation** in the main text or the supplement parts
  read
- **`ω₀` is a signal-dependent hyperparameter**, set by hand
- **No comparison against Fourier features** (concurrent work)

## Open questions

- Would Xavier- or Kaiming-initialized sine networks fail in the way the
  account predicts, and at what depth?
