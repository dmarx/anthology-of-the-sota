---
number: 392
status: Proposed
formerly:
- SOTA-tmp62nb7
promote_when: >-
  A second controlled comparison of distillation alone against reflow
  followed by distillation, for one-step or few-step generation from a
  rectified-flow model, at matched total training compute and at a scale
  beyond CIFAR-10, with the many-step quality of the reflowed model also
  reported.
consensus: contested
contested_by:
- LIT-796
consensus_note: >-
  Contested at scale by InstaFlow (LIT-796). On Stable Diffusion 1.4 at
  matched budget (100K steps, 3.2M generated pairs), reflow then
  distillation beats distilling directly: one-step FID-5k 31.0 against 40.9,
  FID-30k 20.0 against 34.6. Its teacher is a curved diffusion model and its
  distiller an LPIPS regression, so it narrows the practice to a teacher that
  is already a rectified flow rather than refuting that case. Lee et al.
  (LIT-791) refine reflow (one round, trained like a distillation) and
  do not test the ordering. Shortcut Models (LIT-787) find progressive
  distillation alone ahead of one reflow at one step from a flow-matching
  teacher, with no reflow-then-distil arm. The video line reaches few steps
  by distillation without reflow: CausVid and Self Forcing (LIT-631,
  LIT-629), HunyuanVideo's guidance distillation (LIT-620), DMAD (LIT-770)
  and rCM (LIT-783) on the rectified-flow Wan2.1. That is adoption,
  not a test. Read as of 2026-10.
title: 'To get a one-step sampler from a rectified flow, distil it; treat reflow as an optional extra pass, and keep the pre-reflow model for many steps'
version: 3
history:
- version: 2
  date: '2026-10-02'
  note: >-
    Adds DMAD (LIT-770) to the consensus note as one more
    distribution-matching distillation of a rectified-flow model without
    reflow. Adoption, not a test; status and consensus unchanged.
- version: 3
  date: '2026-10-03'
  note: >-
    InstaFlow (LIT-796) and Lee et al. (LIT-791) are now filed.
    InstaFlow is the at-scale, matched-budget comparison and finds reflow
    first better, from a diffusion teacher with regression distillation, so
    it is recorded as contesting the practice and consensus moves from
    unreplicated to contested. The Conditions narrow the claim: for
    regression distillation from a curved diffusion teacher, reflow is not
    optional. Lee et al. are added as a refinement (if you reflow, once, with
    U-shaped timesteps and LPIPS-Huber) and Shortcut Models' Table 1 as
    adjacent evidence. The comment saying both papers were not in the record
    is updated, and InstaFlow is removed from Rectified Flow's
    implementations so the two documents agree. Status stays Proposed: no
    comparison yet starts from a rectified flow at scale.
tags:
- generative-modeling
- flows-and-transport
- few-step-generation
- inference-optimization
date: '2026-09-24'
source:
- LIT-636
# Was LIT-636 until the correction pass. Rectified Flow proposes reflow as
# the way to straight paths and uses reflow-then-distil for its headline
# result; "distil first, reflow optional" is this record's reading of its
# Table 1a (NOTE-337, R2), not advice the paper gives. InstaFlow
# (LIT-796) and Lee et al. 2024 (LIT-791) were searched for here
# and are now filed. Both keep reflow: the first finds it essential for
# one-step Stable Diffusion and is recorded under contested_by, the second
# argues one round suffices. The distribution-matching distillers this
# record holds (LIT-643, LIT-631, LIT-629) skip reflow without arguing
# against it. Still searched and not found: a paper that recommends
# distilling a rectified flow without reflow. Naming one is how a reader
# would change introduced_by (ADR-053).
introduced_by: []
summary: >-
  Liu, Gong and Liu (2022), [LIT-636](../literature.d/LIT-636.md). On CIFAR-10, one-step FID is 378 from
  the base model, 6.18 after distillation alone, 12.21 after one reflow, and
  4.85 after reflow and distillation (Table 1a). Distillation does most of
  the work. Reflow adds a further gain at the cost of a second training pass,
  and worsens many-step quality from 2.58 to 3.36. InstaFlow
  (LIT-796) contests it at text-to-image scale, starting from a
  diffusion model rather than a rectified flow.
explained_by:
- THEORY-123
---

# SOTA-392: To get a one-step sampler from a rectified flow, distil it; treat reflow as an optional extra pass, and keep the pre-reflow model for many steps

## Source

Liu, Gong and Liu (2022), [LIT-636](../literature.d/LIT-636.md) — Rectified Flow, Table 1a.

## The claim

Rectified Flow's title promises generation that is "straight and fast", and
its abstract reports high quality from a single Euler step. That result
needs two further procedures. **Reflow** retrains the model on pairs it
generated itself, which straightens its paths. **Distillation** trains a
one-step student. Table 1a separates them, on CIFAR-10 with the same
architecture. FID at one Euler step:

| Model | Undistilled | Distilled |
|---|---|---|
| 1-rectified flow (no reflow) | 378 | 6.18 |
| 2-rectified flow (one reflow) | 12.21 | 4.85 |

Both procedures, and the table, come from [LIT-636](../literature.d/LIT-636.md), which proposes reflow
as the way to straight paths and uses reflow followed by distillation for its
headline one-step result. The ordering recommended here, distillation first
and reflow optional, is a reading of that paper's Table 1a, not advice the
paper gives. That is why [LIT-636](../literature.d/LIT-636.md) is this practice's source and not its
origin: the paper supplies the numbers and argues for the opposite pipeline,
and the record has found no paper that makes the recommendation, so
`introduced_by` is left empty ([ADR-053](../decisions.d/ADR-053.md)).

**Distillation does most of the work.** It takes the base model from 378 to
6.18 on its own. Reflow before distillation improves that to 4.85, at the
cost of generating a paired dataset and training a second time.

**Reflow costs quality at many steps.** With full RK45 sampling, FID
worsens from 2.58 for the base model to 3.36 after one reflow and 3.96 after
two. The paper says reflow "worsens the results in the large step regime"
(§5.2).

So: distil first. Reflow if the last increment of one-step quality is worth
another training pass, and keep the pre-reflow model when you need
many-step quality. That also follows [SOTA-206](SOTA-206.md), which says to keep a
multi-step option in a few-step model.

## Contested at scale, from a different starting point

InstaFlow ([LIT-796](../literature.d/LIT-796.md)) runs the comparison this practice's
promote_when describes, at text-to-image scale and matched budget, and finds
the opposite order. On Stable Diffusion 1.4 with the same U-Net, batch,
100K training steps and 3.2M generated pairs, distilling SD directly to one
step reaches FID 40.9 on COCO-2017-5k and 34.6 on COCO-2014-30k. Spending
half the budget on one reflow and half on distillation reaches 31.0 and
20.0 (its Table 1, App. C). The tuning, if anything, favours the direct arm,
which got a nine-cell learning-rate grid. It is one seed at 0.9B.

It differs from this practice's case in two ways, and both are why it
narrows the claim rather than refuting it. Its starting point is a diffusion
model's curved probability-flow ODE, so the reflowed model is the first
rectified flow in its pipeline. And its distiller is an LPIPS regression onto
one teacher output per noise, not distribution matching. **For regression
distillation from a curved teacher, reflow is not optional.** When the
teacher is already a rectified flow, the only measurement is still
Rectified Flow's CIFAR-10 table, where reflow adds 6.18 → 4.85 rather than
deciding success.

It agrees with the practice's last clause. Its reflowed model loses a little
many-step quality, 21.5 against SD 1.5's 20.1 FID-5k at 25 steps, so keeping
the pre-reflow model for many steps still holds. A second reflow did not
reliably help (its Table 4).

**If you reflow, reflow once, and train it like a distillation.** Lee et al.
([LIT-791](../literature.d/LIT-791.md)) refine the reflow stage rather than test the ordering.
Starting from EDM, one round trained with a U-shaped timestep distribution
and an LPIPS-Huber loss reaches one-step FID 3.07 on CIFAR-10 and 4.31 on
ImageNet-64 with no separate distillation stage, and they argue further
rounds only add error. Their own table has DMD, a distribution-matching
distiller with no reflow, ahead on ImageNet-64 at 2.62. They run no
distillation-alone arm from the same teacher and no matched many-step
comparison, so they do not meet promote_when.

**Adjacent evidence for distilling without reflow.** Shortcut Models
([LIT-787](../literature.d/LIT-787.md), Table 1) start from a flow-matching model, a 1-rectified
flow, on DiT-B at 256 px. Progressive distillation alone beats one reflow
at one step on both datasets, 14.8 against 23.2 on CelebA-HQ and 35.6
against 44.8 on ImageNet, at roughly matched compute. There is no
reflow-then-distil arm, so it does not test the ordering either. It does
say that from a straight-path teacher, distillation without reflow beats
reflow without distillation, which is this practice's direction.

## Conditions

- **CIFAR-10 only.** The comparison is at 32×32 on one dataset. The paper's
  larger-image results are qualitative.
- **Training budgets are not matched.** Reflow-plus-distillation costs more
  training than distillation alone, and the table does not normalize for it.
- **The distillation uses an LPIPS loss** for the one-step student (App. A).
  Whether the balance holds with other distillation objectives, such as the
  distribution matching the video line uses, is untested. InstaFlow's test
  uses LPIPS regression too.
- **The teacher has to be a rectified flow already.** From a curved
  diffusion teacher with regression distillation, the one test at scale
  finds reflow first better by 9.9 FID-5k ([LIT-796](../literature.d/LIT-796.md), above). The
  practice does not cover that case. InstaFlow was listed here as an
  implementation until the correction pass after [#395](https://github.com/dmarx/anthology-of-the-sota/issues/395), because it
  implements the opposite pipeline; it is now filed as the paper that
  contests this one, and on 2026-10-03 its listing among Rectified Flow's
  implementations was removed for the same reason.
- **The theory is about the reflowed coupling.** The straightness theorems
  apply to the model after reflow, not to the single-pass model most people
  train ([SOTA-266](SOTA-266.md)).
