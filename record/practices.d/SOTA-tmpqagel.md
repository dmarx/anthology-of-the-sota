---
status: Proposed
promote_when: >-
  A group other than MeanFlow's authors trains MeanFlow and at least one
  other from-scratch few-step objective (iCT-style consistency training, a
  shortcut model or Inductive Moment Matching) in one codebase, at matched
  epochs and batch size, at 256 px or above, and reports one-step FID for
  each. MeanFlow's own comparison sets its runs against rows copied from
  three papers at different budgets. A comparison against training a
  diffusion teacher and distilling it, at equal total compute, would settle
  the separate question of whether going without a teacher is the right
  choice at all.
consensus: unreplicated
consensus_note: >-
  One group, one paper (LIT-tmpkkjv3, CMU and MIT). Its ImageNet-256 lead over
  the other from-scratch one-step models is large, but the baselines are
  copied rows: Shortcut Models' and Inductive Moment Matching's from their
  papers, iCT's as Inductive Moment Matching re-ran it. On CIFAR-10 it is
  second to iCT. rCM (LIT-tmpkegvh, App. F.1) finds a MeanFlow-style
  objective worse than plain sCM when distilling a large text-to-image model,
  which is the teacher case this practice excludes. Nobody has re-run
  MeanFlow from scratch. Read as of 2026-10.
title: 'Without a pretrained teacher, train a one-step generator as a MeanFlow average-velocity model rather than by consistency training or a shortcut model'
version: 1
tags:
- generative-modeling
- few-step-generation
- flows-and-transport
date: '2026-10-03'
source:
- LIT-tmpkkjv3
introduced_by:
- LIT-tmpkkjv3
implementations:
- 'MeanFlow'
summary: >-
  Geng et al. (2025), [LIT-tmpkkjv3](../literature.d/LIT-tmpkkjv3.md). Train a network for the average velocity
  over an interval, regressed onto v − (t − r)·du/dt under stop-gradient, with
  du/dt from a Jacobian-vector product. From scratch on ImageNet-256 with
  DiT-XL/2, one-step FID is 3.43 after 240 epochs, against 10.60 for a
  shortcut model and 34.24 for iCT as Inductive Moment Matching re-ran it
  (Table 2). Those rows are copied, at other budgets. No arm compares
  distilling a teacher.
---

<!-- inactive-ok-file: SOTA-tmpckzto — Proposed, filed in the same contribution; named for the loss weighting MeanFlow uses, not as settled advice -->

# SOTA-tmpqagel: Without a pretrained teacher, train a one-step generator as a MeanFlow average-velocity model rather than by consistency training or a shortcut model

## Source

Geng, Deng, Bai, Kolter and He (2025), [LIT-tmpkkjv3](../literature.d/LIT-tmpkkjv3.md) — MeanFlow, §4,
Tables 1–3 and App. B.4.

## What to do

If you need a one- or two-step generator and have no pretrained diffusion or
flow model to distil from, train one directly as a MeanFlow model:

- The network takes two times, u_θ(z_t, r, t), and predicts the average
  velocity over [r, t], the displacement divided by t − r.
- Regress it onto u_tgt = v − (t − r)·(v·∂_z u_θ + ∂_t u_θ), with the target
  under stop-gradient. Here v is the conditional flow-matching velocity
  ε − x, and the bracket is one Jacobian-vector product with tangent
  (v, 0, 1).
- Use r ≠ t on a minority of samples (25% was best), sample (r, t) from a
  logit-normal, and use the adaptive loss weight with p = 1
  ([SOTA-tmpckzto](SOTA-tmpckzto.md)).
- Fold classifier-free guidance into the target, so a guided sample still
  costs one evaluation.
- Sample in one step: x = ε − u_θ(ε, 0, 1).

With r = t on every sample the objective is plain flow matching. The second
time is what makes one step work.

## Evidence

**Against the other from-scratch one-step models** ([LIT-tmpkkjv3](../literature.d/LIT-tmpkkjv3.md), Table 2,
ImageNet-256, DiT-XL/2 size, with guidance):

| Method | NFE | FID | Budget |
|---|--:|--:|---|
| iCT (re-run by Inductive Moment Matching) | 1 | 34.24 | as IMM ran it |
| Shortcut Models | 1 | 10.60 | 160–250 epochs at batch 256 |
| **MeanFlow** | 1 | **3.43** | 240 epochs at batch 256 |
| Inductive Moment Matching | 1 × 2 | 7.77 | about 3,800 epochs at batch 4,096 |
| **MeanFlow** | 2 | **2.93** | 240 epochs |

The budgets are not matched, and the mismatch mostly runs against MeanFlow.
Inductive Moment Matching trained about sixteen times as many epochs.
Shortcut Models' XL run is about 160 passes over ImageNet by its appendix
and 250 epochs by its own table ([LIT-tmpo7np5](../literature.d/LIT-tmpo7np5.md)). Either way it is close to
MeanFlow's 240.

**The second time is the active ingredient** (Table 1a, B/4, 80 epochs, one
step, no guidance). With r = t always, FID is 328.91, which is flow matching.
With r ≠ t on 25%, 50% and 100% of samples it is 61.06, 63.14 and
67.32. Wrong JVP tangents give 137.96 to
329.22 (Table 1b).

**It scales** (Table 2). One-step FID 6.17, 5.01, 3.84 and 3.43 for B/2,
M/2, L/2 and XL/2.

**It is cheap per step** (App. B.4). The JVP's output sits inside the
stop-gradient, so there is no second-order backward pass. Measured cost is
0.052 against 0.045 s per iteration for flow matching, 16% more.

## Conditions

- **The alternatives were not re-run.** Shortcut Models' and Inductive
  Moment Matching's rows are their own papers' numbers. The iCT row is
  Inductive Moment Matching's re-implementation, which that paper says
  "often collapses" ([LIT-tmp7ppws](../literature.d/LIT-tmp7ppws.md)). iCT at its own recipe has never been
  run on ImageNet-256.
- **On CIFAR-10 it is second to iCT** (Table 3, one shared U-Net):
  MeanFlow 2.92 against iCT 2.83 in one step. It beats sCT's 2.97, but sCT
  starts from a pretrained diffusion model ([LIT-tmpt5h4h](../literature.d/LIT-tmpt5h4h.md), App. G), so that
  row is not from scratch. It also beats Inductive Moment Matching's 3.20.
  The large ImageNet lead does not appear at 32 px.
- **Not tested against train-then-distil.** The paper frames itself as
  needing "no pre-training, distillation, or curriculum learning" and runs
  no distillation arm. Where a teacher already exists, the record's
  evidence points elsewhere. rCM ([LIT-tmpkegvh](../literature.d/LIT-tmpkegvh.md), App. F.1) shows MeanFlow's
  objective is a continuous-time consistency trajectory model under the
  rectified-flow schedule, and finds it distils a large text-to-image model
  worse than plain sCM, in quality and diversity. That is one figure, run
  "without extensive hyperparameter tuning".
- **The step count is a weak dial.** The average-velocity field admits any
  step count by construction, but only one and two steps are reported. That
  is thinner than the multi-step evidence behind [SOTA-206](SOTA-206.md) from Shortcut
  Models and Inductive Moment Matching.
- **FID is the only metric.** There is no precision, recall or diversity
  measure, guidance is folded into the model, and there is one run per row.
- **Teacher-free one-step training is not easy in general.** Flow map
  matching ([LIT-tmpuz24v](../literature.d/LIT-tmpuz24v.md), §3.5) found learning the full one-step map
  directly "challenging", and trained a short-interval map first.
  MeanFlow's direct one-step training at ImageNet-256 has not been re-run
  by anyone else.

## Known implementations

- MeanFlow, the source's code.
