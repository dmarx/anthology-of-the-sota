---
status: Read
paper: LIT-tmpb9kuz
title: 'Cold Diffusion'
version: 1
date: '2026-09-23'
summary: >-
  Diffusion generalized to deterministic degradations (blur, masking,
  downsampling, snow) with a restorer and a sampler that is exact for
  degradations linear in severity. Conditional restoration works. Noiseless
  unconditional generation is far worse than noise diffusion, and adding a
  little noise recovers half the gap. Read §1–5.3; the appendix was not
  read.
---

<!-- inactive-ok-file: THEORY-tmpc9v4u THEORY-tmpyyfqg — the Rejected account this paper offered and the Proposed correction, both filed in this same contribution and named as such -->

# NOTE-tmpvd2bq: Cold Diffusion

## Contribution

A demonstration that the diffusion *procedure*, iterative restore and
re-degrade, runs with degradations other than Gaussian noise, and a sampler
that makes it stable for smooth deterministic degradations.

## Key insight

**Re-degrade the difference, not the estimate.** Adding back
`D(x̂₀, s−1) − D(x̂₀, s)` cancels the restorer's error to first order, since
for `D(x, s) = x + s·e` the `x̂₀` terms cancel exactly. That is why it works
for blur where the naive sampler drifts.

## Assumptions

- **`D` continuous in severity, with `D(x, 0) = x`**
- **Small images:** MNIST, CIFAR-10, CelebA, AFHQ at 128²
- **For unconditional blur generation**, a one-component GMM over the
  channel-wise mean as the prior, 300 steps with a 27×27 kernel

## Key results

- **Tables 1–4 (conditional):** sampling with Algorithm 2 improves FID over
  one-shot reconstruction at a small cost in RMSE and SSIM. CelebA deblurring
  FID 26.14 against 36.37, CIFAR-10 inpainting 8.92 against 9.97
- **Table 5 (unconditional FID):** CelebA 23.11 with noise (estimated),
  97.00 noiseless blur, 49.45 blur with σ = 0.002 noise. AFHQ 20.59 / 93.05 /
  54.68

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Algorithm 2 is exact for first-order degradations regardless of `R` | strong | derivation in §3.3 |
| C2 | Cold degradations support conditional restoration by iterative sampling | moderate | Tables 1–4, small datasets |
| C3 | Generative behaviour does not depend strongly on the degradation | weak | Table 5 contradicts it for unconditional generation |
| C4 | Noiseless blur generation lacks diversity because of correlated initial pixels | moderate | the σ = 0.002 fix halves FID |

## Concepts

- **Hot / cold diffusion** — with and without Gaussian noise in the
  degradation

## Connections

It relates to blurring diffusion and inverse heat dissipation, which it
does not compare against directly. Warm Diffusion ([LIT-tmphm11f](../literature.d/LIT-tmphm11f.md)) extends it
by mixing blur with noise and gives the account of why noise matters. The
fixed-noise variant is related to DDIM's deterministic sampling
(Appendix A.6).

## Recommendations

- **R1** — For a deterministic degradation, sample with Algorithm 2, not by
  re-degrading the estimate. *Strength:* strong for first-order
  degradations. Not filed as a practice. The record holds no practice that
  uses cold degradations

## Bearing on the record

- **[THEORY-tmpc9v4u](../theory.d/THEORY-tmpc9v4u.md)** files the paper's account, `Rejected`
- **[THEORY-tmpyyfqg](../theory.d/THEORY-tmpyyfqg.md)** (Warm Diffusion) is the correction

## Limitations

- **Unconditional generation is uncompetitive**, and only on CelebA and
  AFHQ
- **Small images and small models**
- **Algorithm 2's guarantee is first-order.** Far from `s = 0` it is a
  heuristic

## Open questions

- None the record holds open. Warm Diffusion takes up the noise question
