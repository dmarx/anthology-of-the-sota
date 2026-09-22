---
status: Read
paper: LIT-tmphm11f
title: 'Warm Diffusion'
version: 1
date: '2026-09-23'
summary: >-
  Blur and noise mixed in one forward process, with a two-headed model that
  denoises to the blurry image and deblurs the residual. A blur-to-noise
  ratio of 0.5, chosen from image and noise spectra, edges EDM on CIFAR-10
  (1.85 against 1.97). High ratios degrade sharply, which is the evidence
  that noise keeps samples on the manifold. Read in full (8 pages).
---

<!-- inactive-ok-file: THEORY-tmpc9v4u THEORY-tmpyyfqg — the Rejected account this paper corrects and the Proposed account it supports, both filed in this same contribution -->

# NOTE-tmp0qg1j: Warm Diffusion

## Contribution

A process family interpolating hot and cold diffusion, a parameterization
that splits the reverse step into denoising and deblurring, and an account
of the trade-off between them in terms of the data manifold.

## Key insight

**Noise and blur remove different things, and only noise fills the gaps.**
Blur deletes high frequencies deterministically, so many clean images share
one blurry image. The deblurring target is their mean, and stepping toward
it leaves the manifold unless noise has already made those samples
indistinguishable. Noise that dominates a band before blur removes it keeps
the process on the data manifold.

## Assumptions

- **EDM** architectures, training and Heun sampler, modified for two inputs
  and doubled outputs
- **CIFAR-10 32², FFHQ 64², LSUN-church 128²**
- **Natural image spectra close to `1/f²`**, for the BNR choice

## Key results

- **Table 3 (CIFAR-10, NFE 35):** FID 1.97 (BNR 0) → 1.85 (0.5) → 2.01 (1) →
  2.57 (2) → 11.97 (10)
- **Figure 5:** higher BNR needs more sampling steps to recover quality
- **Table 1:** improvements over EDM on CIFAR-10 and FFHQ. Best of three
  sampling rounds

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Removing noise from the process (high BNR) degrades generation | moderate | Table 3 sweep, one dataset |
| C2 | The degradation is caused by leaving the data manifold | weak | argued with an illustration, not measured |
| C3 | A moderate blur component improves on pure noise | weak | 0.12 FID, best of three, no variance |
| C4 | BNR = 0.5 can be chosen from spectra | weak | matches the sweep's best, but the sweep is coarse and on one dataset |

## Concepts

- **BNR** — blur level over noise level. 0 is hot diffusion, ∞ is cold
- **Spectral dependency** — the predictability of high-frequency detail
  from low-frequency structure in natural images

## Connections

It extends Cold Diffusion ([LIT-tmpb9kuz](../literature.d/LIT-tmpb9kuz.md)) and compares against EDM
([LIT-075](../literature.d/LIT-075.md)), Blurring Diffusion and inverse heat dissipation. Table 1's Cold
Diffusion entry quotes a deblurring FID as a generation FID (see the LIT
note).

## Bearing on the record

- **[THEORY-tmpyyfqg](../theory.d/THEORY-tmpyyfqg.md)** files its account, which corrects [THEORY-tmpc9v4u](../theory.d/THEORY-tmpc9v4u.md)
- **No practice filed.** The gain over EDM is too small and too thinly
  reported to recommend mixing in blur

## Limitations

- **Manifold departure is asserted from a diagram**, not measured (for
  example by a density or classifier score of intermediate states)
- **Best-of-three reporting**, no seeds
- **Small images only**

## Open questions

- Whether the cold-side degradation persists at higher resolution and in
  latent space, where spectra differ
