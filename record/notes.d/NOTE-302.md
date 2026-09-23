---
number: 302
status: Read
formerly:
- NOTE-tmp36vxd
paper: LIT-564
title: 'CycleGAN'
version: 1
date: '2026-09-23'
summary: >-
  Unpaired translation with two adversarial losses and a bidirectional
  cycle-consistency loss. It works for appearance changes and fails for
  geometric ones. The ablation supports the cycle term against GAN-only, but
  not strictly the bidirectional form over one direction. Read §1–6; the
  appendix was skimmed.
---

<!-- inactive-ok-file: SOTA-339 — Proposed, filed in this same contribution from this paper -->

# NOTE-302: CycleGAN

## Contribution

A way to learn image-to-image translation without paired data, by making
the translation invertible, and a demonstration across style transfer,
object transfiguration, season transfer and photo enhancement.

## Key insight

**Invertibility is a free constraint.** Without pairs, the adversarial loss
only says the output should look like the target domain. Requiring that the
input can be recovered forces the output to depend on it.

## Assumptions

- **A roughly bijective relation between domains.** Content survives and
  appearance changes
- **ResNet generator and 70×70 PatchGAN discriminator**, least-squares GAN
  loss, λ = 10, and a history buffer of generated images for the
  discriminators

## Key results

- **Tables 4 and 5** as in the LIT note. The full model is best photo →
  labels and second-best labels → photo
- **AMT maps ↔ aerial:** about 25% of trials fooled
- **Failure cases (§6):** dog → cat and other geometric changes

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Cycle consistency makes unpaired translation work where GAN-only does not | moderate | ablation on Cityscapes; qualitative across tasks |
| C2 | Both cycle directions are needed | weak | one direction beats both on labels → photo; instability shown qualitatively |
| C3 | It does not handle geometric change | moderate | stated by the authors, with examples |

## Connections

It is the unpaired counterpart of pix2pix. Projected GAN's related work
([LIT-562](../literature.d/LIT-562.md)) cites perceptual-discriminator variants that improve on it.

## Recommendations

- **R1** — For unpaired appearance translation, use a cycle-consistency
  loss. Filed as [SOTA-339](../practices.d/SOTA-339.md)

## Limitations

- **FCN score on Cityscapes** is the only quantitative ablation
- **Appearance only**

## Open questions

- Whether a weaker constraint than exact invertibility would allow
  geometric change
