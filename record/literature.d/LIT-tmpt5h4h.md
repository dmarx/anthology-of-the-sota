---
status: Active
title: 'Simplifying, Stabilizing and Scaling Continuous-Time Consistency Models'
version: 1
tags:
- generative-modeling
- few-step-generation
- inference-optimization
- model-stability
- numerics-and-precision
- attention-techniques
- flows-and-transport
date: '2026-10-03'
published: '2024-10-14'
arxiv: '2410.11081'
first_author: 'Lu'
keywords:
- 'continuous-time-consistency-models'
- 'trigflow'
- 'tangent-normalization'
- 'adaptive-weighting'
- 'flash-attention-jvp'
- 'consistency-distillation'
- 'consistency-training'
extends:
- LIT-093
compared_against:
- LIT-067
- LIT-075
- LIT-643
- LIT-646
- LIT-714
- LIT-tmpnrsms
- LIT-tmp7ppws
- LIT-tmpkkjv3
summary: >-
  Lu and Song, OpenAI (2024), [ARXIV-2410.11081](https://arxiv.org/abs/2410.11081). Continuous-time consistency
  models had been unstable. A trigonometric flow parameterization, identity
  time input with positional embeddings, normalized tangents, learned loss
  weights and a Flash Attention JVP make them train to 1.5B parameters.
  Continuous time beats every discrete step count tried. Two-step FID is 2.06
  on CIFAR-10, 1.48 on ImageNet-64 and 1.88 on ImageNet-512, against teachers
  at 2.01, 1.33 and 1.73. Every model, "consistency training" included,
  starts from the pretrained diffusion model.
extended_by:
- LIT-tmpkegvh
---
<!-- inactive-ok-file: SOTA-204 — Proposed; named as the practice this paper's continuous-time result argues against, not as settled advice -->

# LIT-tmpt5h4h: Simplifying, Stabilizing and Scaling Continuous-Time Consistency Models

Lu and Song, OpenAI (2024), ICLR 2025 — [ARXIV-2410.11081](https://arxiv.org/abs/2410.11081). Known as "sCM".
Read at v2 (1 Mar 2025), main text and Appendices A–G; v1 is 14 Oct 2024.

## Key takeaways

- **TrigFlow** (§3, Eqs. 3–5). x_t = cos(t)·x₀ + sin(t)·z on t ∈ [0, π/2],
  with the consistency model f = cos(t)·x_t − sin(t)·σ_d·F_θ, a single Euler
  step of the probability-flow ODE. It keeps EDM's unit-variance
  coefficients, and is a special case of flow matching and of v-prediction.
- **Where the instability came from** (§4.1, Eq. 7, Fig. 4). The training
  signal is the tangent df/dt along the ODE. The unstable part is the time
  derivative ∂_t F, through the time transform and the embedding. EDM's
  log-tan time transform blows up near t = π/2, and Fourier embeddings at
  scale 16 oscillate. The fixes are c_noise(t) = t, positional embeddings,
  and "adaptive double normalization" in place of AdaGN.
- **Controlling the gradient** (§4.2, Eq. 8, Fig. 5a–b). The tangent is
  normalized by ‖df/dt‖ + 0.1 (clipping works too). A learned per-time
  weight, as in EDM2, replaces hand-set weighting. The tangent's unstable
  term is warmed up over 10K iterations. Each change improves one- and
  two-step FID in ImageNet-512 distillation curves.
- **Continuous beats discrete** (Fig. 5c, App. E). Discrete-time models
  improve as the step count N rises to 1,024 and degrade beyond it, from
  numerical precision. The continuous-time model beats every N.
- **Results** (Tables 1–2). CIFAR-10, one / two steps: sCT 2.85 / 2.06, sCD
  3.66 / 2.52. ImageNet-64: sCT 2.04 / 1.48, sCD 2.44 / 1.66. ImageNet-512,
  1.5B parameters: sCD 2.28 / 1.88, sCT 4.29 / 3.76. The teacher is 1.73 at
  63 × 2 evaluations.
- **Distillation scales with the teacher** (Fig. 6). sCD's FID ratio to its
  teacher is roughly constant across five model sizes, and smaller at two
  steps than one. sCT is more compute-efficient at 64 px and less so at
  512 px. sCD reaches the teacher's quality in under 20% of the teacher's
  training compute; 20K iterations already give good samples (§5.2).
- **Against score distillation on diversity** (Fig. 7, EDM2-M on
  ImageNet-512). One-step VSD, the DMD objective, raises precision and
  lowers recall as guidance increases, ending in "severe mode collapse".
  VSD is the objective DMD descends.
  Two-step sCD's precision and recall stay close to the teacher's across
  guidance scales. This is a figure without tabled values.
- **Engineering for scale** (§5.1, App. F). The JVP is rearranged to avoid
  FP16 overflow near t = 0 and π/2. A Flash-Attention-style kernel computes
  attention and its JVP in one pass.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Consistency training (CT), by contrast, trains CMs from scratch"**
  (§2.2). In this paper it does not. "We always initialize the CM from the
  EMA parameters of the teacher diffusion model", for sCT as well as sCD
  (App. G). On ImageNet-512 that diffusion model trained 376K–1,048K
  iterations at batch 2,048 before sCT's 100K (Table 5). sCT here is
  fine-tuning a diffusion model without using its ODE. Later tables that
  file sCT under "from scratch" (IMM, MeanFlow) misread it.
- **"Narrowing the gap … to within 10%"** (abstract). On CIFAR-10 it is 2%
  (2.06 against 2.01) and on ImageNet-512 9% (1.88 against 1.73). On
  ImageNet-64 it is 11% (1.48 against 1.33).
- **The ImageNet-512 teachers are re-trained here**, with TrigFlow and a
  corrected latent normalization (Table 2, App. G). At XL and XXL they beat
  published EDM2 (1.80 against 1.85, 1.73 against 1.81). sCD students are
  conditioned on the guidance scale and scored "under optimal guidance
  scales", chosen per step count (Table 6).
- **Most ablations are curves on one setting** (Fig. 5, ImageNet-512
  distillation, 50K iterations). The positional-embedding and normalization
  fixes are shown through gradient norms on CIFAR-10 (Fig. 4), not FID.
- **No seeds or intervals.** The diversity comparison is the only precision
  and recall reported, as curves.

## Which comparisons are like for like

- **sCD against its own teacher** is matched: same architecture, same
  batch, initialized from it.
- **The VSD comparison** (Fig. 7) is run here at EDM2-M size with tuned
  weighting and proposal distributions (§5.2). It is the paper's one
  controlled comparison against another distillation method. VSD here is
  one-step, sCD two-step.
- **Tables 1 and 2** are mostly copied rows, including DMD2 at 1.28 and the
  CD, PD and iCT rows.

## Standing in the anthology

It extends Consistency Models ([LIT-093](LIT-093.md)), whose Remark 10 derived the
continuous-time gradient this paper finally makes trainable (§2.2, Eq. 2).
[LIT-093](LIT-093.md) and iCT had both found that limit unstable. The iCT paper
([LIT-tmpnrsms](LIT-tmpnrsms.md)) is its main baseline. sCT beats iCT-deep at one step on
ImageNet-64, 2.04 against 3.25, and keeps iCT's dropout placement. Unlike
iCT, which trains from random weights, it starts from a diffusion model.

Its teachers are EDM ([LIT-075](LIT-075.md)) on CIFAR-10, the 2.01 its "within 10%"
compares against, and EDM2 ([LIT-714](LIT-714.md)) on ImageNet, re-trained in TrigFlow
form. Its ImageNet-64 table carries progressive distillation ([LIT-067](LIT-067.md)) at
10.70 and 4.70, as re-implemented by Heek et al., and DMD2 ([LIT-646](LIT-646.md)) at
1.28 in one step, ahead of sCD's 2.44. The VSD arm of Fig. 7 is DMD's
([LIT-643](LIT-643.md)) distribution-matching gradient without the regression loss. The
recall drop it shows is the record's first measurement of that objective's
diversity cost against a forward-direction distiller on one backbone.

The score-regularized consistency paper ([LIT-tmpkegvh](LIT-tmpkegvh.md)) scales this method
to 14B-parameter video models. It finds pure sCM fails on fine detail
there, and adds a DMD term.

Two from-scratch models later set their CIFAR-10 numbers against sCT's.
Inductive Moment Matching ([LIT-tmp7ppws](LIT-tmp7ppws.md)) reports two-step 1.98 against
sCT's 2.06, and MeanFlow ([LIT-tmpkkjv3](LIT-tmpkkjv3.md)) one-step 2.92 against 2.97. Both
file sCT as trained from scratch, which by App. G here it is not: it starts
from the pretrained diffusion model.

**On [SOTA-206](../practices.d/SOTA-206.md) it is support.** sCD and sCT sample at one or two steps from
one model, and two steps close most of the gap to the teacher at every
size.

**On [SOTA-204](../practices.d/SOTA-204.md) it is the strongest evidence against.** Fig. 5c removes the
discretisation rather than annealing it, and the continuous-time model beats
every fixed N tried. It is one setting, a distillation run started from a
pretrained diffusion model, so it does not test training from random
weights, which is where iCT found the curriculum mattered.

Filed without a NOTE: the takeaways come from one full reading of v2's main
text and appendices. Figs. 5–7 have no tabled values and are described,
not quantified.
