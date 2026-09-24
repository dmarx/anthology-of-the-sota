---
status: Active
title: 'Improved Distribution Matching Distillation for Fast Image Synthesis'
version: 1
tags:
- generative-modeling
- inference-optimization
- vision-and-graphics
- training-optimization
date: '2026-09-24'
published: '2024-05-01'
arxiv: '2405.14867'
first_author: 'Yin'
keywords:
- 'distribution-matching-distillation'
- 'two-time-scale-update-rule'
- 'gan-loss'
- 'backward-simulation'
- 'multi-step-generator'
- 'fake-diffusion-critic'
implementations:
- 'CausVid'
extends:
- LIT-tmp8mirn
compared_against:
- LIT-062
- LIT-067
- LIT-075
- LIT-093
- LIT-566
summary: >-
  Yin et al., MIT and Adobe (2024), [ARXIV-2405.14867](https://arxiv.org/abs/2405.14867). DMD2 drops DMD's
  regression loss. It stabilizes training by updating the fake score five
  times per generator step, adds a GAN loss on real images, and trains
  multi-step students on their own simulated inputs. The ImageNet ablation
  is clean: removing the loss costs 2.62 → 3.48 FID, and the update rule
  restores 2.61. The student is slightly less diverse than its teacher (LPIPS
  diversity 0.61 against 0.64). The paper does not attribute this to the
  reverse KL.
extended_by:
- LIT-631
---
<!-- inactive-ok-file: SOTA-394, SOTA-395 — Proposed practices this paper bears on; named as what the paper informs, not as settled advice -->


# LIT-tmpcjcg4: Improved Distribution Matching Distillation for Fast Image Synthesis

Yin, Gharbi, Park, Zhang, Shechtman, Durand and Freeman, MIT and Adobe
Research (2024) — [ARXIV-2405.14867](https://arxiv.org/abs/2405.14867). Known as "DMD2". Read at v2.

## Key takeaways

- **The regression loss can go** (Table 3, one-step ImageNet-64 from EDM).
  DMD with regression gets 2.62 FID. Removing it gives 3.48, and brightness
  oscillates without converging (§4.2, App. C, Fig. 8). With the fake score
  updated 5 times per generator update (TTUR) it gets 2.61, with no paired
  dataset. The authors blame a fake critic that lags the generator. Fig. 9
  compares 1, 5 and 10 updates and a 5× critic learning rate, as curves
  only. It also shows TTUR converging faster than DMD with regression.
- **A GAN loss adds the most** (Table 3). A classifier head on the fake
  denoiser's bottleneck (App. F.1) scores noised real images against noised
  generator outputs (Eq. 4). Adding it takes 2.61 to 1.51. GAN alone gets
  2.56, and GAN with TTUR 2.52. The standard setup is 200K iterations at
  batch 280 on 7 A100s with GAN weight 3e-3 (App. F.2). The DMD row is the
  original paper's number, and the paper does not say whether the other
  rows share one budget.
- **Backward simulation** feeds a multi-step student its own noised
  outputs during training, not noised real images (§4.5, Fig. 4). The only
  ablation is 4-step SDXL on 10K COCO prompts (Table 4). Without it: FID
  20.66, patch FID 24.21, CLIP 0.332. With it: 19.32, 20.86, 0.332.
- **The SDXL ablation** (Table 4, same setup): without the GAN term, FID
  26.90 and "oversaturated and oversmoothed" images. Without distribution
  matching, FID 13.77, the best in the table, with CLIP 0.307, the worst.
  The authors read FID as rewarding a pure GAN for matching the unguided
  real distribution.
- **Headline results.** ImageNet-64: 1.51 in one step, 1.28 with longer
  training, against EDM's 2.32 (ODE) and 1.36 (SDE) (Table 1). COCO-30k from
  SD v1.5: 8.35 against DMD's 11.49 (App. Table 5). SDXL, 4 steps: 19.32 FID
  against 19.36 for the teacher at guidance 6 and 20.39 at guidance 8
  (Table 2).
- **Diversity is measured, once** (App. B, Table 6). The score is mean
  pairwise LPIPS over 4 images per prompt on 128 PartiPrompts. It is 0.61
  for DMD2 against 0.64 for the SDXL teacher at guidance 6 or 8. LCM gets
  0.61, SDXL-Turbo 0.58 and SDXL-Lightning 0.63. §6 calls it "a slight
  degradation".

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"We eliminate the regression loss"** (abstract). The one-step SDXL model
  was first pretrained with a regression loss on 10K pairs, with a timestep
  shift to 399 (App. F.4). The authors call this possibly "specific to
  SDXL".
- **"Surpassing the original teacher"** (abstract). On ImageNet, the
  standard 1.51 beats the ODE teacher but not the SDE teacher (1.36). Only
  the 550K-iteration two-stage run (1.28, App. F.2) beats both. On COCO,
  8.35 beats the 50-step ODE teacher (8.59) but not 200-step SDE sampling at
  guidance 2 (7.21, Table 5). The student's real score used guidance 1.75
  against the teacher's 3 (App. F.3), and FID favours lower guidance, as
  Table 4's pure-GAN row shows.
- **"Outperforms its teacher in image quality for 24% of samples"** (§5.2).
  Fig. 5 shows 62.0% against 38.0%, so 24 is the margin in points, not a
  share of samples. Prompt alignment is 50.5% against 49.5%. Each pair was
  rated by 5 evaluators on 128 prompts (§5.2, App. H).
- **The diversity loss is not given a cause.** The paper never uses "reverse
  KL" or "mode". It argues SDXL-Lightning's higher score is "partially due
  to random outputs". It says a larger GAN weight would raise diversity by
  pulling toward "the more diverse unguided distribution". That is not
  measured (App. B). The real score runs at guidance 8 (App. F.4), so
  guidance is as live a suspect as the KL direction. No ImageNet diversity
  or recall is reported after the regression loss is removed.
- **The update ratio is per dataset.** It is 5 on ImageNet and SDXL and 10
  on SD v1.5 (App. F). The authors advise the smallest ratio that keeps
  "pixel brightness" stable (App. C).

## Standing in the anthology

CausVid ([LIT-631](LIT-631.md)) is a direct descendant. [NOTE-343](../notes.d/NOTE-343.md) records it using "a DMD2
update ratio of 5". Its four fixed timesteps [999, 748, 502, 247] are
close to §4.4's 999, 749, 499, 249. Self Forcing ([LIT-629](LIT-629.md)) runs DMD inside its
rollout framework. [SOTA-394](../practices.d/SOTA-394.md)'s condition that "the record does not hold DMD
or DMD2" is answered by this filing and the DMD note.

On [SOTA-394](../practices.d/SOTA-394.md)'s diversity condition, this is the only measurement in the line:
a 4-step image student loses 0.03 LPIPS diversity against its teacher, with
competing distillers on both sides. It does not separate the reverse-KL
objective from real-score guidance. The practice's "characteristic of
reverse KL" is CausVid's explanation, and neither DMD paper tests it.

Backward simulation is the image-distillation form of [SOTA-395](../practices.d/SOTA-395.md)'s
self-rollout training, published a year before Self Forcing. Its evidence is
one SDXL ablation row, measured by patch FID.

The TTUR is borrowed from Heusel et al. ([LIT-611](LIT-611.md)), who proposed it for GAN
discriminators. SDXL ([LIT-566](LIT-566.md)) is the main teacher.

Filed without a `NOTE`: the takeaways come from one full reading done for
this filing, of the main text and Appendices A–I, with Fig. 5 read from the
rendered page. Figs. 8–9 have no numeric values, so the TTUR frequency
comparison is described, not quantified.
