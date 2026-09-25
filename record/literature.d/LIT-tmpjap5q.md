---
status: Active
title: 'Efficient Diffusion Training via Min-SNR Weighting Strategy'
version: 1
tags:
- generative-modeling
- training-optimization
date: '2026-09-25'
published: '2023-03-16'
arxiv: '2303.09556'
first_author: 'Hang'
keywords:
- 'min-snr-gamma'
- 'diffusion-loss-weighting'
- 'multi-task-learning'
- 'pareto-optimality'
- 'convergence-speed'
- 'prediction-target'
implementations:
- 'diffusers (--snr_gamma)'
- 'kohya-ss sd-scripts (--min_snr_gamma)'
extends:
- LIT-036
compared_against:
- LIT-067
- LIT-075
- LIT-448
summary: >-
  Hang et al. (ICCV 2023), [ARXIV-2303.09556](https://arxiv.org/abs/2303.09556). Weight each timestep's
  x0-space loss by `min(SNR(t), γ)`, γ = 5, which is `min(γ/SNR, 1)` on an
  ε loss and `min(SNR, γ)/(SNR+1)` on a v loss. The headline "3.4× faster" is
  against an x0-prediction baseline with constant weight, on one ViT-B run. Against the
  ε-prediction default most people train, the UNet gain is 8.55 → 7.32 FID at
  200K iterations and 4.21 → 4.14 at 1M. It speeds early training much more
  than it moves the end point. The "conflicting gradients between timesteps"
  explanation rests on one fine-tuning probe and a proxy objective.
---

# LIT-tmpjap5q: Efficient Diffusion Training via Min-SNR Weighting Strategy

Hang et al. (2023; ICCV 2023) — [ARXIV-2303.09556](https://arxiv.org/abs/2303.09556)

## Key takeaways

**The weighting.** Write the loss in x0-space, where DDPM's ε-MSE carries
an implicit weight of `SNR(t) = α²/σ²` (App. B). Replace that weight with
`min(SNR(t), γ)`, capping it so the low-noise steps stop dominating. On the
other targets the same weighting is `min(γ/SNR, 1)` for ε and
`min(SNR, γ)/(SNR + 1)` for v. γ = 5 is the default.

**The comparison it ran** (ImageNet 256 latent, ViT-B, Fig. 5), against the
record's existing advice. It covers constant, SNR, [LIT-067](LIT-067.md)'s truncated
`max(SNR, 1)` and Min-SNR-5, each under x0, ε and v. Min-SNR-5 converges
fastest under all three targets. **With ε output, constant and
`max(SNR, 1)` weighting diverge.** Both put weight `1/SNR` on the ε loss,
unbounded at the noisy end. The 3.4× is time-to-FID-10 for **x0 + Min-SNR-5
against x0 + constant**, which is the weakest baseline in the figure.

**Against the ε default, the gain is mostly early** (UNet, Table 1):

| iterations | 200K | 400K | 600K | 800K | 1M |
| --- | --- | --- | --- | --- | --- |
| ε baseline (ε-MSE) | 8.55 | 5.43 | 4.64 | 4.35 | 4.21 |
| ε + Min-SNR-5 | 7.32 | 4.98 | 4.48 | 4.24 | 4.14 |
| x0 baseline | 25.93 | 15.41 | 11.54 | 9.52 | 8.33 |
| x0 + Min-SNR-5 | 7.99 | 5.34 | 4.69 | 4.41 | 4.28 |

Table 1 does not state the baselines' weighting. Read as the plain loss on
each target, which Fig. 5's curves suggest, the large effect is on
x0-prediction, which was badly weighted to begin with. For the ε-MSE that DDPM made standard, the end-of-training gain is 0.07 FID,
single runs.

**γ barely matters below 20** (Table 2). UNet-ε gives 4.30 / 4.14 / 4.14 /
4.12 at γ = 1 / 5 / 10 / 20, so its best value there is 20, not 5.

**On EDM** (App. D.1.1, Fig. 9). Multiplying EDM's loss by `min(SNR, 5)/SNR`
converges faster over the first 200M training images. The authors stop there
"due to the limit of compute budget", short of EDM's full schedule.

**The headline FIDs are system results, not weighting results.** 2.06 on
ImageNet 256 is a ViT-XL at ~7M iterations with x0 + Min-SNR-5,
classifier-free guidance at 1.5 and EDM's Heun sampler at 50 steps. It is
compared with [LIT-448](LIT-448.md)'s published 2.27. The "3.3× faster than DiT" (2.08 at
2.1M iterations) sets their run against DiT's reported one. It is not a
re-run.

## Traps

- **"3.4× faster" does not mean "3.4× faster than what you are doing".** It is
  measured against constant-weighted x0-prediction. Against ε-prediction with
  plain MSE, the table above is the evidence.
- **The explanation is weaker than the recipe.** "Conflicting gradients across
  timesteps" rests on two things. Fig. 2 fine-tunes on three timestep bins
  and watches the loss at others move. Fig. 4 shows Min-SNR-5 scores near the
  per-iteration Pareto solver on a regularized min-norm objective, Eq. 11. That
  is a proxy the authors chose, and nothing ties it to FID independently.
- **Min-SNR is not a monotone weighting.** In [LIT-692](LIT-692.md)'s frame it is
  `sech(λ/2)·min(1, γe^{−λ})`, so [THEORY-107](../theory.d/THEORY-107.md)'s noise-augmented-likelihood
  reading does not apply to it.
- **ViT runs use AdamW β = (0.99, 0.99)**, from U-ViT, and a vanilla ViT with
  the timestep and class as tokens. Nobody should copy the absolute FIDs to a
  different backbone.

## Standing in the anthology

Filed from `#290`'s catalogue triage. The record already named it twice: in
[LIT-692](LIT-692.md)'s weighting table and in [THEORY-107](../theory.d/THEORY-107.md)'s list of non-monotone
weightings, without holding the paper. It is the one direct comparison the
record has of [LIT-067](LIT-067.md)'s truncated-SNR weighting against an alternative.
[SOTA-195](../practices.d/SOTA-195.md)'s weighting paragraph now says so. No practice recommends
Min-SNR, and this filing does not add one. The instruction is clear, but the
evidence is one group, and for ε-prediction the gain is mostly in the first
few hundred thousand iterations.
