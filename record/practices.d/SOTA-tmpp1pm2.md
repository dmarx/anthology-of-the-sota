---
status: Proposed
promote_when: >-
  A group other than rCM's distils one teacher of a billion parameters or
  more by continuous-time consistency with and without a DMD term,
  everything else held, and reports the pure-consistency arm as numbers: a
  quality metric (VBench, GenEval or FID) and a diversity metric such as
  recall or pairwise LPIPS, for both arms. rCM never tables its pure-sCM
  arm, and its diversity claim rests on samples. A paper that adopts the
  combined loss without the pure-consistency arm does not count.
consensus: unreplicated
consensus_note: >-
  One group (LIT-tmpkegvh, Tsinghua and NVIDIA). Pure sCM's failure at
  scale is shown in images and videos only, and the λ sweep stops at 0.001
  with no λ = 0 row. The diversity half has one measured precedent from
  another group: sCM's own precision-recall comparison (LIT-tmpt5h4h,
  Fig. 7, OpenAI), which shows the consistency term keeps diversity that
  distribution matching alone loses. DMAD (LIT-770) is a rival distiller
  that beats rCM in a human study, but it does not test the combination.
  Read as of 2026-10.
title: 'When distilling a large image or video model by continuous-time consistency, add a small DMD distribution-matching term'
version: 1
tags:
- generative-modeling
- few-step-generation
- inference-optimization
date: '2026-10-03'
source:
- LIT-tmpkegvh
- LIT-tmpt5h4h
# The mirror arrangement is older. DMD (LIT-643) put distribution matching
# first and added a regression loss onto the teacher's ODE outputs as the
# regularizer. rCM puts the ODE-following consistency term first and adds
# distribution matching as the regularizer, at weight 0.01. Only rCM states
# this weighting, so it is the origin.
introduced_by:
- LIT-tmpkegvh
implementations:
- 'Cosmos-Predict2 + rCM'
- 'Wan2.1 T2V + rCM'
summary: >-
  Zheng et al. (2025), [LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md). Pure sCM distillation of 2B–14B
  text-to-image and text-to-video teachers loses small text, texture and
  temporal coherence. Adding DMD's loss at weight 0.01, on the student's own
  1–4-step rollouts with a fake-score network updated 5–10 times per step,
  fixes it in samples. Four-step Wan2.1-1.3B VBench is 84.43 against a
  re-implemented DMD2's 84.56. sCM's own Fig. 7 ([LIT-tmpt5h4h](../literature.d/LIT-tmpt5h4h.md)) is why the
  consistency term stays primary: distribution matching alone loses recall.
explained_by:
- THEORY-tmpko5v1
---

<!-- inactive-ok-file: SOTA-394 — Proposed; named for its diversity condition, which this practice responds to, not cited as settled advice -->

# SOTA-tmpp1pm2: When distilling a large image or video model by continuous-time consistency, add a small DMD distribution-matching term

## Source

Zheng, Wang, Ma, Chen, Zhang, Balaji, Chen, Liu, Zhu and Zhang (2025),
[LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md) — rCM, §3.3, §4.1, Tables 1–2 and Fig. 7.

Lu and Song (2024), [LIT-tmpt5h4h](../literature.d/LIT-tmpt5h4h.md) — sCM, Fig. 7.

## What to do

Distil with the continuous-time consistency loss of sCM as the main
objective. Add DMD's distribution-matching loss as a regularizer:

- L = L_sCM + λ·L_DMD, with **λ = 0.01**.
- Compute L_DMD on the student's own samples, from a rollout of a random 1
  to 4 steps, not on noised real data.
- Train a fake-score network alongside, as in DMD, and update it several
  times per student update (5, and 10 at 14B). No GAN term is needed.
- Keep sCM's tangent normalization. At 10B parameters and above, and for
  video, keep the full JVP rather than a finite difference for the time
  derivative, and run the time-embedding layers in FP32.

The weighting matters in both directions. The consistency term follows the
teacher's ODE and keeps diversity. The distribution-matching term pulls the
student's samples toward the teacher's distribution and restores detail.
Make the second just strong enough to fix detail.

## Evidence

**Pure sCM fails at scale** ([LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md), §3.3, Fig. 3, App. E). On
Cosmos-Predict2 at 2B and 14B and on Wan2.1 at 1.3B, four-step sCM students
are sharp and close to the teacher on ordinary prompts. They break on small
text. In video, textures blur and objects interpenetrate across frames.
Scaling the model does not fix it. The authors attribute this to error
accumulation: the self-feedback term in the JVP dominates at large t, where
the teacher's supervision vanishes, and BF16 makes the JVP's error much
larger than the output's (Fig. 11). This evidence is images and videos, with
no table.

**The regularizer fixes it, and its weight has a floor** (Fig. 7,
Wan2.1-1.3B, 10K iterations at batch 64, four steps):

| λ | 1 | 0.1 | 0.01 | 0.001 |
|---|--:|--:|--:|--:|
| VBench | 84.32 | 84.57 | 84.43 | 82.68 |

Quality holds from λ = 1 down to 0.01 and drops at 0.001. The authors read
the samples, five seeds per λ, as trading diversity for quality as λ rises,
and pick 0.01 as "the smallest scale to preserve good quality".

**At full scale it matches DMD2 on quality** (Tables 1–2). Four-step GenEval
on Cosmos-Predict2 is 0.79, 0.81 and 0.83 at 0.6B, 2B and 14B, against
teachers at 0.81, 0.83 and 0.84 and a re-implemented DMD2 at 0.77 and 0.80
(0.6B and 2B). Four-step VBench on Wan2.1 is 84.43 at 1.3B, against DMD2's
84.56 and the teacher's 83.02, and 84.92 at 14B. One student also serves
one and two steps.

**Why keep consistency as the main term** ([LIT-tmpt5h4h](../literature.d/LIT-tmpt5h4h.md), Fig. 7). On one
EDM2-M backbone at ImageNet-512, sCM ran one-step VSD, which is DMD's
distribution-matching gradient without its regression loss, against
two-step sCD. As guidance rises, VSD's precision rises and its recall falls,
ending in "severe mode collapse". sCD's precision and recall stay close to
the teacher's. Read from the plot (no values are tabled): one-step sCD is plotted too, and at guidance 1.0 its recall is about 0.70 against about 0.65 for one-step VSD, so the gap is there at matched step count and before guidance is raised. The arm that sums the two losses at equal weight tracks VSD's recall, not sCD's. That is the record's one measurement
of the diversity argument, it comes from a different group from rCM, and
it is why the DMD term is added with a small weight rather than at parity.

The loss being added is DMD's ([LIT-643](../literature.d/LIT-643.md)): the gradient is a frozen real
score minus an online fake score, evaluated on noised generator samples,
normalized by the mean absolute denoising error. DMD needed a regression
loss onto teacher ODE outputs to train stably. DMD2 ([LIT-646](../literature.d/LIT-646.md)) replaced that
with several fake-score updates per generator step and recovered 2.61 FID
on ImageNet-64 without it (Table 3 there). rCM keeps DMD2's update ratio and
drops its GAN.

## Conditions

- **The comparison that matters is not tabled.** No λ = 0 row exists, and
  pure sCM against rCM is shown only in samples. The λ = 0.001 row (82.68)
  is the closest number, and it is a regularized run.
- **The diversity claim is from samples.** rCM's "notable advantages in
  diversity" over DMD2 rest on five videos per method (Fig. 1) and five seeds
  per λ (Fig. 7). No diversity metric is reported. sCM's Fig. 7 is the
  measured support for the direction, read from curves; its one-step sCD
  arm makes the comparison like for like.
- **The DMD2 baseline is a re-implementation**, with a discriminator
  branch on the fake-score network and no configuration or budget given. On
  1.3B VBench it is slightly ahead of rCM.
- **It is not free of tuning.** It keeps DMD2's fake-score network and its
  5 to 10 critic updates per student step. Learning rates and the sampling
  σ_max differ by model.
- **A rival distiller beats it with people.** DMAD ([LIT-770](../literature.d/LIT-770.md)) uses rCM's
  Wan2.1 rows as baselines, and its human study prefers DMAD to rCM on
  63.8% of prompts, ties counted as non-wins. That compares two distillers.
  It does not test whether the DMD term helps sCM.
- **Only at large scale.** Every rCM result is on 0.6B–14B text-conditioned
  teachers. Whether pure sCM's detail failures appear on small
  class-conditional models, where sCM reaches 1.88 FID at two steps on
  ImageNet-512 ([LIT-tmpt5h4h](../literature.d/LIT-tmpt5h4h.md)), is not tested.

## Beside the record's other practices

[SOTA-394](SOTA-394.md)'s diversity condition cites both sources: distribution matching on
its own costs diversity. This practice is the response that keeps
distribution matching for detail while letting a forward-direction term
carry diversity. [SOTA-206](SOTA-206.md) also cites rCM: one rCM student serves one, two
and four steps, and video needs two.

## Known implementations

- Cosmos-Predict2 and Wan2.1 T2V students distilled with rCM, the
  source's released models.
