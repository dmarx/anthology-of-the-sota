---
status: Active
title: 'Diffusion Models With Learned Adaptive Noise'
version: 1
tags:
- generative-modeling
- training-optimization
date: '2026-09-25'
published: '2023-12-20'
arxiv: '2312.13236'
first_author: 'Sahoo'
keywords:
- 'learned-noise-schedule'
- 'multivariate-noise-schedule'
- 'auxiliary-latent'
- 'variational-lower-bound'
- 'density-estimation'
- 'schedule-invariance'
implementations:
- 'MuLAN (github.com/s-sahoo/MuLAN)'
extends:
- LIT-446
compared_against:
- LIT-446
summary: >-
  Sahoo, Gokaslan, De Sa and Kuleshov (NeurIPS 2024),
  [ARXIV-2312.13236](https://arxiv.org/abs/2312.13236). MuLAN replaces VDM's scalar learned schedule with a
  **per-pixel schedule conditioned on a learned auxiliary latent**. At equal
  steps and architecture the bound moves 2.65 → 2.60 bits/dim on CIFAR-10,
  and it reaches VDM's 2.65 in 2M steps instead of 10M. Its own ablations
  confirm VDM's invariance where VDM claimed it. A scalar schedule
  conditioned on the input buys nothing, and a multivariate schedule
  conditioned on time only is "comparable to that of VDM". The headline
  2.55 is a different estimator.
---

<!-- inactive-ok-file: SOTA-tmp61nli SOTA-264 — both Proposed; named as the practice this
     paper sources and the rival practice it competes with for the same objective -->

# LIT-tmp1jb6n: Diffusion Models With Learned Adaptive Noise

Sahoo, Gokaslan, De Sa and Kuleshov (2023; NeurIPS 2024) — [ARXIV-2312.13236](https://arxiv.org/abs/2312.13236)

## Key takeaways

**The target is likelihood, and the paper says so.** "our primary focus is
density estimation and probabilistic modeling rather than sample quality."
It uses VDM's U-Net, settings and datasets, on 32×32 pixels only, with no
augmentation. The added encoder is about 10% of parameters.

**Three components, and only all three together help.**
1. A **multivariate schedule**, `N(α_t x_0, diag(σ_t²))`, with a monotone
   degree-5 polynomial in `t` per dimension. The endpoints stay pinned at
   VDM's values (`γ_min = −13.30`, `γ_max = 5.0`) and are **not learned**.
2. **Conditioning the schedule on context.** Conditioning directly on `x_0`
   fails, because the reverse process cannot see it. So a discrete latent
   `z ~ q_φ(z|x_0)` conditions both directions, with a prior used at
   generation time.
3. **The auxiliary latent** costs an extra KL term in the bound.

From the ablation (Fig. 2a; CIFAR-10, batch 64, 2.5M steps, one run each,
shown only as a figure): a multivariate schedule conditioned only on time
"becomes comparable to that of VDM", and an input-conditioned *scalar*
schedule "doesn't offer any advantage over the scalar schedule used in VDM".

**The controlled result** (Table 1, noise parameterization, same
architecture):

| | CIFAR-10 steps | bits/dim | ImageNet-32 steps | bits/dim |
| --- | --- | --- | --- | --- |
| VDM | 10M | 2.65 | 2M | 3.72 |
| + MuLAN | 2M | 2.65 | 1M | 3.72 |
| + MuLAN | 10M | **2.60** | 2M | **3.71** |

At equal steps the gain is 0.05 bits/dim on CIFAR-10 and 0.01 on
ImageNet-32. The larger effect is **speed to VDM's number**: 5× fewer steps
on CIFAR-10 and about 3× less wall-clock (10 days against 30 on 4 V100s),
and 2× fewer steps on ImageNet-32.

**How it squares with VDM's invariance (§3.5, App. E.5).** Written in
SNR-space, the continuous-time loss is a line integral along the schedule's
path. A scalar schedule confines that path to the diagonal, so every shape
between the same endpoints is a reparameterization of one path, and VDM's
endpoint-only dependence follows. That is the paper's own reduction. A
per-dimension schedule can take many paths between the same endpoints, and
the integral is path-independent only for a conservative field. That this
"is rarely the case for a diffusion process" is **asserted by citation and
an analogy (airplanes and cyclones), not proved** for this loss.

**The swap test agrees with VDM.** "We replace the noise schedule in the
trained denoising model with two alternatives: MuLAN with scalar noise
schedule, and a linear noise schedule … For both the noise schedules the
likelihood reduces to the same value as that of the VDM: 2.65."

## Traps

- **The headline 2.55 is not the controlled number.** Table 2's 2.55 / 3.67 is
  a probability-flow ODE with an importance-weighted (K=20) dequantization
  estimator, at 8M steps with v-parameterization. VDM's figure in the same
  table is a variational bound. The like-for-like comparison is **2.59 against
  2.65**, and the controlled one is **2.60 against 2.65**. The table's "±1e-3" is
  the estimator's confidence interval, not variation across seeds.
- **"Our work dispels this assumption" overstates it.** The abstract says the
  ELBO's invariance to the noise process is dispelled, and App. C.5 says it
  "contradicts Kingma et al." The body is accurate: invariance is "only true
  for the simplest types of univariate Gaussian noise". VDM never claimed
  more, and MuLAN's own scalar ablation and swap test reproduce VDM's result.
  This is a boundary on VDM's claim, not a correction of it.
- **"Multivariate" alone does nothing measurable.** §3.2.1 says a multivariate
  schedule "is sufficient to make the ELBO no longer invariant", but the
  time-only multivariate arm matches VDM. Whether the theory holds and fails
  to show in training, or whether the latent does the work, is not settled.
- **EMA.** §4.4 says MuLAN does not use tricks such as exponential moving
  averages, while App. G.3 maintains an EMA at 0.9999. FID is mixed: on
  ImageNet-32 it is worse at 1M steps (15.00 against 14.26) and better at 2M.
- **The learned schedules are uninterpretable.** "none of these experiments
  revealed human-interpretable patterns in the learned schedule".

## Standing in the anthology

Filed from the reading-time triage of 2026-09-25 as the successor of
[LIT-446](LIT-446.md) (VDM), which is among the feed's most-read works.

- **It bounds [THEORY-027](../theory.d/THEORY-027.md) and does not contest it.** That
  theory's invariance is now scoped to *scalar* schedules. MuLAN's scalar
  ablation and swap test re-measure it and agree.
- **It sources `SOTA-tmp61nli`**: when the target is likelihood, learn a
  per-dimension schedule conditioned on a learned latent. That practice is a
  rival to [SOTA-264](../practices.d/SOTA-264.md) for the same objective. [SOTA-264](../practices.d/SOTA-264.md)
  says to spend the free shape of a *scalar* schedule on estimator variance.
  MuLAN spends a multivariate shape on the bound itself, and gets 5× fewer
  steps to the same number.
- **No bearing on perceptual generation.** [SOTA-188](../practices.d/SOTA-188.md) and
  [SOTA-266](../practices.d/SOTA-266.md) are about sample quality, where this paper
  reports only a weak FID at 32×32.
