---
number: 443
status: Proposed
formerly:
- SOTA-tmpckzto
promote_when: >-
  A group outside OpenAI's consistency line and the MeanFlow authors trains a
  self-bootstrapped few-step objective (consistency, flow map, shortcut or
  average velocity) at 256 px or above, compares a robust loss or adaptive
  error weight against plain squared L2 with everything else held, and
  reports one- or two-step FID for each arm. A sweep over batch size would
  also settle whether the gain is only a variance effect. A paper that uses
  Pseudo-Huber without the squared-L2 arm does not count. That is adoption.
consensus: emerging
consensus_note: >-
  Two groups have measured it against squared L2, on two different
  objectives: iCT for discrete-time consistency training (LIT-786,
  OpenAI, CIFAR-10 curves) and MeanFlow for average-velocity regression
  (LIT-784, CMU and MIT, one ImageNet-256 ablation table). Both find
  squared L2 worst. sCM (LIT-790), from iCT's line, controls the same
  variance by normalizing the tangent instead, and rCM (LIT-783,
  Tsinghua and NVIDIA) adopts that. A third group, Lee et al. (LIT-791),
  finds Pseudo-Huber no better than squared L2 at batch 512 in reflow
  training, a different objective. Nobody in the record argues for plain
  squared L2. Read as of 2026-10.
title: 'Down-weight large residuals in consistency and MeanFlow training: use a Pseudo-Huber loss or an adaptive inverse-error weight, not plain squared L2'
version: 1
tags:
- generative-modeling
- few-step-generation
- model-stability
date: '2026-10-03'
source:
- LIT-786
- LIT-784
introduced_by:
- LIT-786
implementations:
- 'iCT'
- 'MeanFlow'
summary: >-
  Song and Dhariwal (2023), [LIT-786](../literature.d/LIT-786.md), and Geng et al. (2025),
  [LIT-784](../literature.d/LIT-784.md). When the regression target is the model's own output under
  stop-gradient, squared L2 trains worse than a loss that limits the pull of
  large errors. iCT's Pseudo-Huber beats squared L2 on CIFAR-10 (Fig. 2,
  curves). MeanFlow's adaptive weight 1/(‖Δ‖² + c)^p takes one-step
  ImageNet-256 FID from 79.75 at p = 0 to 61.06 at p = 1 (Table 1e). Two
  groups, small settings, one run per arm.
explained_by:
- THEORY-118
---

<!-- inactive-ok-file: THEORY-118 — Proposed, and the account declared in `explained_by:`; cited in Conditions for the gradient-shape relation it states, not as a settled result -->

# SOTA-443: Down-weight large residuals in consistency and MeanFlow training: use a Pseudo-Huber loss or an adaptive inverse-error weight, not plain squared L2

## Source

Song and Dhariwal (2023), [LIT-786](../literature.d/LIT-786.md) — iCT, §3.3, Fig. 2 and Fig. 6.

Geng, Deng, Bai, Kolter and He (2025), [LIT-784](../literature.d/LIT-784.md) — MeanFlow, §4.3,
Table 1e and App. B.2.

## What to do

Some few-step objectives regress the network onto a target built from the
network itself, under stop-gradient. Consistency training and distillation
do this, and so does MeanFlow's average-velocity loss. In these objectives,
do not regress with plain squared L2. Use one of two forms:

- **Pseudo-Huber**, d(x, y) = √(‖x − y‖² + c²) − c. It is quadratic for small
  errors and linear for large ones. iCT's heuristic for d-dimensional data
  is c = 0.00054·√d.
- **An adaptive per-sample weight** on the squared error,
  w = 1/(‖Δ‖² + c)^p, held under stop-gradient, with c small (MeanFlow uses
  10⁻³). This is the gradient of ‖Δ‖^(2(1 − p)). MeanFlow's best is p = 1,
  and p = 0.5 is close to Pseudo-Huber.

Do not reach for LPIPS instead. It was the original consistency models'
metric, and iCT dropped it because LPIPS is trained on ImageNet, as is the
Inception network that scores FID. [SOTA-337](SOTA-337.md) is about the same
risk.

## Evidence

**iCT** ([LIT-786](../literature.d/LIT-786.md), §3.3). On CIFAR-10, every arm uses the paper's other
fixes. Pseudo-Huber gives "notably better sample quality than the squared ℓ2
metric" (Fig. 2b–c). With the wider step-count range iCT adopts
(s₀ = 10, s₁ = 1,280), it beats consistency training with LPIPS, which the authors
describe as a first for a metric that uses no learned features. c = 0.03 is best on
CIFAR-10. The proposed mechanism is lower update variance. Fig. 6b shows
Adam's parameter-update norms vary less under Pseudo-Huber than under
squared L2. All of this is FID curves at batch 512, one run each, with no
tabled values.

**MeanFlow** ([LIT-784](../literature.d/LIT-784.md), Table 1e). ImageNet-256, B/4, 80 epochs from
scratch, one-step FID with no guidance:

| p | 0 (squared L2) | 0.5 (≈ Pseudo-Huber) | 1.0 | 1.5 | 2.0 |
|---|--:|--:|--:|--:|--:|
| FID | 79.75 | 63.98 | **61.06** | 66.57 | 69.19 |

The authors note that squared L2 "still produces meaningful results". Too much down-weighting hurts too, so there is an
optimum, not a direction to push. One run per row.

The two papers come from different groups and test different objectives,
and they agree. MeanFlow takes its weighting from ECT (Geng et al. 2024,
not held), which shares its first author, so the adaptive form is
one line of work.

## Conditions

- **The objective matters, and batch size alone may not.** Lee et al.
  ([LIT-791](../literature.d/LIT-791.md), §4.2, Table 1) train a 2-rectified flow onto fixed
  (noise, teacher output) pairs. There, Pseudo-Huber beat squared L2 at batch
  128 on CIFAR-10, and at batch 512 it was even: 5.17 → 5.24 on CIFAR-10,
  6.81 → 7.06 on FFHQ-64, 9.03 → 8.20 on AFHQ-64. iCT's own CIFAR-10
  ablations also ran at batch 512 and found a clear gain. [THEORY-118](../theory.d/THEORY-118.md)
  draws the line by objective. In consistency and MeanFlow training the
  residual is the network's own tangent along the ODE, a finite difference
  of it in discrete time, and its large values come from the network's
  time derivative. Down-weighting them is tangent normalization. A reflow
  residual against a fixed teacher sample is not a tangent, and the account
  gives no reason for the robust loss to pay there. That boundary is the
  theory's, and no paper has run both objectives under both losses.
- **In continuous time the variance is controlled elsewhere.** sCM
  ([LIT-790](../literature.d/LIT-790.md), §4.2, Fig. 5a) keeps squared L2. It divides the tangent in its
  target by ‖df/dt‖ + 0.1, or clips it, and both improve one- and two-step
  FID in ImageNet-512 distillation curves. rCM ([LIT-783](../literature.d/LIT-783.md), §3.1,
  footnote 4) keeps that normalization at 14B scale and states that
  MeanFlow's p = 1 weight "is the same as tangent normalization".
  [THEORY-118](../theory.d/THEORY-118.md) checks the relation through the gradients' shape. The
  adaptive weight held under stop-gradient makes the gradient the residual
  divided by (‖Δ‖² + c)^p. At p = 1 that is rCM's normalized-tangent form,
  divided by ‖g‖² + c. At p = 0.5 it is the residual over √(‖Δ‖² + c),
  which is Pseudo-Huber's gradient and the near neighbour of sCM's own
  division by ‖df/dt‖ + 0.1. All three are one per-sample rescaling of the
  same update. So if you train with sCM's normalized tangent, you already
  have the effect, and adding Pseudo-Huber on top would apply it twice. That
  has not been tested, and nobody has run MeanFlow's weight against sCM's
  normalization in one codebase.
- **c and p were each tuned on one setting.** iCT chose c on CIFAR-10 and
  carried the √d heuristic to ImageNet-64 with no ablation there. MeanFlow
  chose p on a small model at 80 epochs and kept it for XL/2.
- **There is a theoretical reading, not a measured one.** Inductive Moment
  Matching ([LIT-775](../literature.d/LIT-775.md), §5, Lemmas 1–2) shows that the squared-L2
  consistency loss matches only the first moment, while Pseudo-Huber is a
  valid kernel for a moment-matching distance. This is offered as an account
  of iCT's loss. It does not measure anything about it.

## Known implementations

- iCT, and the improved consistency-training recipes built on it.
- MeanFlow (adaptive weight, p = 1).
