---
status: Active
title: 'Mean Flows for One-step Generative Modeling'
version: 1
tags:
- generative-modeling
- few-step-generation
- flows-and-transport
- inference-optimization
- vision-and-graphics
date: '2026-10-03'
published: '2025-05-19'
arxiv: '2505.13447'
first_author: 'Geng'
keywords:
- 'meanflow'
- 'average-velocity'
- 'meanflow-identity'
- 'jacobian-vector-product'
- 'one-step-generation'
- 'classifier-free-guidance-in-target'
extends:
- LIT-630
compared_against:
- LIT-447
- LIT-448
- LIT-tmp7ppws
- LIT-tmpnrsms
- LIT-tmpo7np5
- LIT-tmpt5h4h
summary: >-
  Geng, Deng, Bai, Kolter and He, CMU and MIT (2025), [ARXIV-2505.13447](https://arxiv.org/abs/2505.13447). Train
  a network for the average velocity u(z, r, t) over an interval, using the
  identity u = v − (t − r)·du/dt with du/dt from a Jacobian-vector product
  and the target under stop-gradient. With r = t it is flow matching. From
  scratch on ImageNet-256 with DiT-XL/2 and guidance folded into the target,
  one-step FID is 3.43 at 240 epochs and two-step 2.20 at 1,000. The best
  one-step baselines it beats, Shortcut 10.60 and IMM 7.77, are copied rows
  at other budgets. Behind iCT on CIFAR-10. One run per row.
---

<!-- inactive-ok-file: SOTA-tmpckzto SOTA-tmpqagel — Proposed practices this paper is the source of, named in its standing -->

# LIT-tmpkkjv3: Mean Flows for One-step Generative Modeling

Geng, Deng, Bai, Kolter and He, CMU and MIT (2025) — [ARXIV-2505.13447](https://arxiv.org/abs/2505.13447). Read
at v1 (19 May 2025), main text and Appendices A–C; no later version on
arXiv.

## Key takeaways

- **The object is an interval average, not a velocity** (§4.1, Eqs. 3–6).
  u(z_t, r, t) is the displacement from r to t divided by t − r. It is a
  field defined by the flow, independent of any network. Differentiating
  its definition in t gives the MeanFlow identity u = v − (t − r)·du/dt.
  The total derivative expands to v·∂_z u + ∂_t u (Eq. 8), a Jacobian-vector
  product with tangent (v, 0, 1). The loss regresses u_θ onto that
  right-hand side under stop-gradient (Eqs. 9–11). One-step sampling is
  x = ε − u_θ(ε, 0, 1) (Alg. 2).
- **It is flow matching plus a correction, and the correction is what
  works** (Table 1a, B/4, 80 epochs, one step, no guidance). With r = t
  always, FID is 328.91. With r ≠ t on 25% of samples it is 61.06, and on
  100% it is 67.32. Wrong JVP tangents give 137.96 to 329.22 (Table 1b).
- **The loss and sampler settings matter** (Table 1d–e). An adaptive weight
  1/(‖Δ‖² + c)^p with p = 1 gives 61.06, p = 0.5 (close to Pseudo-Huber)
  63.98, plain squared L2 79.75. A logit-normal (r, t) sampler beats uniform,
  61.06 against 65.90.
- **Guidance is folded into the target** (§4.2, Eqs. 13–19, App. B.1). The
  network learns the average velocity of the guided field, so a guided
  sample still costs one evaluation. Guidance scale 3.0 takes the ablation
  model from 61.06 to 15.53 (Table 1f). Mixing in the conditional output (κ)
  takes 20.15 to 18.63 at an effective scale of 2.0 (Table 5).
- **Headline** (Table 2, ImageNet-256, from scratch, 240 epochs, batch
  256). One-step FID 6.17, 5.01, 3.84 and 3.43 for B/2, M/2, L/2 and XL/2.
  Two-step XL/2 2.93; with 1,000 epochs and retuned settings (XL/2+), 2.20.
- **Unconditional CIFAR-10** (Table 3), one step, no EDM preconditioner:
  2.92, against iCT 2.83, sCT 2.97, IMM 3.20 and ECT 3.60.
- **The JVP is cheap here** (App. B.4). Its output sits inside the
  stop-gradient, so no second-order backward is needed. The measured cost
  is 0.052 against 0.045 s/iter for flow matching, 16% more.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"A relative margin of 50% to 70%"** (§1). The rows it beats are copied:
  Shortcut's 10.60 from its paper, IMM's 7.77 from its paper, and iCT's
  34.24 as IMM re-ran it (Table 2, †). The budgets differ, and in
  MeanFlow's favour. MeanFlow trains 240 epochs at batch 256 (App. A). IMM
  trains 1.2M iterations at batch 4,096, which is about 3,800 epochs. The
  margin is real and is not a matched comparison.
- **"On par with … SiT (FID 2.15)"** (§5.2). Table 2 lists SiT-XL/2 at 2.06,
  not 2.15. The 2.20 needs the 1,000-epoch XL/2+ run with its own guidance
  interval, [0.3, 0.8] (Table 4). The one-step 3.43 uses guidance on
  t ∈ [0.0, 0.75].
- **MeanFlow-M is 308M parameters in Table 2 and 497.8M in Table 4.** The
  difference is not explained.
- **"Self-contained … without any pre-training, distillation, or the
  curriculum learning"** (§5.2). That holds for MeanFlow. The CIFAR-10 sCT
  row it is set against does not train from scratch: sCM initializes every
  consistency model from a pretrained diffusion model ([LIT-tmpt5h4h](LIT-tmpt5h4h.md),
  App. G). On CIFAR-10 MeanFlow is second to iCT.
- **"Few step sampling is also straightforward"** (§4.1). Only one and two
  evaluations are reported. Whether quality rises with more steps, as it
  does for Shortcut and IMM, is not shown.
- **FID is the only metric**, one run per row. There is no precision,
  recall or diversity measure, and guidance raises fidelity at diversity's
  cost.

## Which comparisons are like for like

- **Table 1** is a clean internal ablation: one B/4 backbone, 80 epochs,
  one variable at a time.
- **Table 2, left** compares models of the same DiT-XL/2 size, but at
  different training budgets and from numbers copied out of three papers.
  The iCT row is IMM's own re-implementation, which IMM reports as prone to
  collapse.
- **Table 3** shares one ~55M U-Net across all rows. The baselines use EDM
  preconditioning and MeanFlow does not, and the sCT row starts from a
  pretrained diffusion model.

## Standing in the anthology

Its Table 2 comparison against the other from-scratch one-step models is the source of [SOTA-tmpqagel](../practices.d/SOTA-tmpqagel.md), and its adaptive loss weight (Table 1e) is the second group behind [SOTA-tmpckzto](../practices.d/SOTA-tmpckzto.md).

It extends Flow Matching ([LIT-630](LIT-630.md)). The training target substitutes the
conditional velocity for the marginal one, the step that makes flow
matching trainable, and with r = t the method is exactly flow matching
(§4.1). What it adds is a second time and the identity tying the average
to the instantaneous field.

Its comparisons are to the other two-time, from-scratch models. Against
Shortcut Models ([LIT-tmpo7np5](LIT-tmpo7np5.md)) it scores 3.43 against 10.60 at one step.
Shortcut enforces the same additivity of intervals with discrete binary
steps, where MeanFlow differentiates it. Against Inductive Moment Matching
([LIT-tmp7ppws](LIT-tmp7ppws.md)) it scores 2.93 against 7.77 at two evaluations; IMM's needs
two because it applies guidance at sampling time. Against iCT ([LIT-tmpnrsms](LIT-tmpnrsms.md))
it scores 3.43 against 34.24 on ImageNet-256, the iCT number being IMM's
re-run. On CIFAR-10 it trails iCT, 2.92 against 2.83. Against sCT
([LIT-tmpt5h4h](LIT-tmpt5h4h.md)) it scores 2.92 against 2.97 on CIFAR-10. The many-step
references are DiT-XL/2 ([LIT-448](LIT-448.md)) at 2.27 and SiT-XL/2 ([LIT-447](LIT-447.md)) at 2.06,
both at 250 × 2 evaluations.

The score-regularized consistency paper ([LIT-tmpkegvh](LIT-tmpkegvh.md), App. F.1) shows
MeanFlow's objective is a continuous-time consistency trajectory model
under the rectified-flow schedule, and reports that form training worse
than plain sCM when used to distil a large text-to-image model. That is
one qualitative figure, run "without extensive hyperparameter tuning".

**On [SOTA-206](../practices.d/SOTA-206.md) it is weak support.** The average-velocity field admits any
step count by construction (Eq. 12), but only one and two steps are
measured. At XL/2 the second step improves FID from 3.43 to 2.93.

The (r, t) sampler is SD3's logit-normal ([LIT-449](LIT-449.md)). The finding that it
beats uniform carries over from flow matching to the two-time objective.

Filed without a NOTE: the takeaways come from one full reading of v1,
including the appendices. Fig. 1 and Fig. 4 are read only through the
numbers given in Table 2 and the figure labels.
