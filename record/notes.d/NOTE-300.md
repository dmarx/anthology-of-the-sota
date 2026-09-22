---
number: 300
status: Read
formerly:
- NOTE-tmp508h6
paper: LIT-559
title: 'StyleGAN3'
version: 1
date: '2026-09-23'
summary: >-
  Aliasing in the generator glues fine detail to pixel coordinates.
  Continuous-signal design, with 2×-upsampled filtered nonlinearities,
  Fourier input and no noise, gives translation- and rotation-equivariant
  generators at StyleGAN2's FID. Read §1–3.2 and Figure 3; the internal
  representation analysis and the appendices were skimmed.
---

<!-- inactive-ok-file: SOTA-335 SOTA-336 — Proposed, filed in this same contribution; the first from this paper, the second named because this paper qualifies it -->

# NOTE-300: StyleGAN3

## Contribution

An account of texture sticking as aliasing, and a generator that removes
it by construction. Equivariance becomes a measured property (EQ-T, EQ-R)
instead of a visual impression.

## Key insight

**A pointwise nonlinearity is where new frequencies come from, so it is
where to filter.** In continuous terms a nonlinearity commutes with
geometric transforms. Discretely it aliases unless the signal is briefly
represented at higher resolution and band-limited afterward.

## Assumptions

- **Features are samples of bandlimited continuous signals.** Every
  operation is judged by what it does to that signal
- **Infinite spatial extent**, approximated by a 10-pixel margin cropped
  after each layer, because border padding leaks absolute position
- **The discriminator is unchanged** from StyleGAN2

## Method

- Input: fixed Fourier features, with frequencies sampled in a disc at the
  4×4 band, replacing the learned constant
- Per-pixel noise removed. Mixing and path-length regularization disabled.
  Output skips removed and replaced by dividing features by an EMA of their
  RMS
- Resampling: Kaiser-windowed sinc filters (n = 6), which need far stronger
  stopband attenuation (the paper says over 100 dB) than common filters give
- Nonlinearity: upsample m = 2, leaky ReLU, low-pass, downsample, fused into
  a custom kernel. For rotation, radially symmetric (jinc) filters and 1×1
  convolutions
- Per-layer cutoffs follow a geometric progression, which sets how much new
  frequency each layer may add

## Key results

- **Figure 3:** StyleGAN2 FID 5.14. StyleGAN3-T 4.62 with EQ-T 63.0 dB.
  StyleGAN3-R 4.50 with EQ-T 66.7 and EQ-R 40.5
- **Intermediate configurations lose FID** (6.35 at filtered
  nonlinearities) before non-critical sampling recovers it. The changes
  interact, and the path is not monotone

## Recommendations

- **R1** — For content that must move with the scene, build the generator
  alias-free. Filed as [SOTA-335](../practices.d/SOTA-335.md)

## Bearing on the record

- **[SOTA-336](../practices.d/SOTA-336.md)** (no progressive growing, output skips): StyleGAN3
  keeps the fixed topology but drops the output skips, which it believes
  were mainly fixing gradient-magnitude dynamics
- **[SOTA-335](../practices.d/SOTA-335.md)** is filed from this paper

## Limitations

- **FFHQ-U at 256²** for the main ablation
- **Equivariance is measured under synthetic transforms of one image**, not
  on video
