---
status: Active
title: 'Cold Diffusion: Inverting Arbitrary Image Transforms Without Noise'
version: 1
tags:
- generative-modeling
- analysis-and-evaluation
date: '2026-09-23'
published: '2022-08-01'
arxiv: '2208.09392'
first_author: 'Bansal'
keywords:
- 'cold-diffusion'
- 'deterministic-degradation'
- 'blur-diffusion'
- 'sampling'
implementations: []
summary: >-
  Bansal et al. (2022), [ARXIV-2208.09392](https://arxiv.org/abs/2208.09392). Train a network to invert blur,
  masking, downsampling or snow at every severity, then sample by alternating
  restoration and re-degradation, and something generative happens without
  Gaussian noise. The durable result is the sampler,
  `x_{s−1} = x_s − D(x̂₀, s) + D(x̂₀, s−1)`, which is exact for degradations
  linear in severity whatever the restorer's errors. The headline, that noise
  is not needed, is contradicted by its own Table 5: noiseless blur
  generation is FID 97.00 on CelebA against 23.11 with noise, and a
  σ = 0.002 noise sprinkle brings it to 49.45.
extended_by:
- LIT-tmphm11f
---

<!-- inactive-ok-file: THEORY-tmpc9v4u THEORY-tmpyyfqg — the Rejected account this paper offered and the Proposed correction, both filed in this same contribution and named as such -->

# LIT-tmpb9kuz: Cold Diffusion: Inverting Arbitrary Image Transforms Without Noise

Bansal, Borgnia, Chu, Li, Kazemi, Huang, Goldblum, Geiping, Goldstein,
University of Maryland and NYU (2022) — [ARXIV-2208.09392](https://arxiv.org/abs/2208.09392)

## Key takeaways

- **Generalized diffusion:** any degradation `D(x₀, t)`, continuous in `t`
  with `D(x₀, 0) = x₀`, and a restorer `R(x_t, t) ≈ x₀` trained with an ℓ₁
  loss
- **The naive sampler fails for smooth degradations.** Re-degrading the
  estimate, `x_{s−1} = D(R(x_s), s−1)`, compounds errors (Figure 2)
- **Algorithm 2** adds back only the change in degradation between steps.
  For `D(x, s) ≈ x + s·e`, the first-order Taylor form of any smooth
  degradation, it reproduces `D(x₀, s−1)` exactly *for any `R`*. For blur,
  each step adds back a difference-of-Gaussians band of the frequencies
  removed at that step
- **Conditional restoration works:** deblurring, inpainting,
  super-resolution and desnowing on MNIST, CIFAR-10 and CelebA improve FID
  over direct one-shot reconstruction
- **Unconditional generation is much weaker** (Table 5, FID):

  | | CelebA | AFHQ |
  |---|--:|--:|
  | hot, fixed noise | 59.91 | 25.62 |
  | hot, estimated noise | 23.11 | 20.59 |
  | cold blur, noiseless | 97.00 | 93.05 |
  | cold blur, σ = 0.002 noise added | 49.45 | 54.68 |

## Standing in the anthology

**Filed from `#163`** ("[theory] cold diffusion"). The account it offers,
that diffusion's generative behaviour does not depend on the noise, is filed
as [THEORY-tmpc9v4u](../theory.d/THEORY-tmpc9v4u.md) and is `Rejected` on the paper's own numbers and on Warm
Diffusion's sweep ([LIT-tmphm11f](LIT-tmphm11f.md)). The corrected account is [THEORY-tmpyyfqg](../theory.d/THEORY-tmpyyfqg.md).

**The sentence that travelled and the one that should have.** The abstract's
"generative behavior of diffusion models is not strongly dependent on the
choice of image degradation" is the one quoted. The paper's own remedy for
its noiseless model's lack of diversity is to add Gaussian noise, which
halves its FID. The authors attribute the collapse to perfectly correlated
pixels in the initial sample, which is another way of saying the noise was
doing work ([DP-010](../../docs/design-principles.md#dp-10)).

**The sampler is the keeper.** Algorithm 2's exactness under first-order
degradations is a real and general property, and it is the part that
Warm Diffusion builds on.

Read — [NOTE-tmpvd2bq](../notes.d/NOTE-tmpvd2bq.md).
