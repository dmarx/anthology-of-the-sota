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
consensus: unreplicated
consensus_note: >-
  One source, Rectified Flow (LIT-636, Table 1a), on CIFAR-10. The large
  video reports reach few steps by distillation without reflow: CausVid and
  Self Forcing use distribution matching (LIT-631, LIT-629), and
  HunyuanVideo distils guidance (LIT-620). That fits the practice, but it is
  adoption and not a test. Read as of 2026-09.
title: 'To get a one-step sampler from a rectified flow, distil it; treat reflow as an optional extra pass, and keep the pre-reflow model for many steps'
version: 1
tags:
- generative-modeling
- inference-optimization
date: '2026-09-24'
source:
- LIT-636
# Was LIT-636 until the correction pass. Rectified Flow proposes reflow as
# the way to straight paths and uses reflow-then-distil for its headline
# result; "distil first, reflow optional" is this record's reading of its
# Table 1a (NOTE-337, R2), not advice the paper gives. Searched and not
# found: InstaFlow (arXiv 2309.06380) and Lee et al. 2024 (arXiv
# 2405.20320, "Improving the Training of Rectified Flows") both keep reflow
# — the first finds it critical for one-step Stable Diffusion, the second
# argues one round suffices — and the distribution-matching distillers this
# record holds (LIT-643, LIT-631, LIT-629) skip reflow without arguing
# against it. Naming a paper that recommends distilling without reflow is
# how a reader refutes this (ADR-053).
introduced_by: []
summary: >-
  Liu, Gong and Liu (2022), [LIT-636](../literature.d/LIT-636.md). On CIFAR-10, one-step FID is 378 from
  the base model, 6.18 after distillation alone, 12.21 after one reflow, and
  4.85 after reflow and distillation (Table 1a). Distillation does most of
  the work. Reflow adds a further gain at the cost of a second training pass,
  and worsens many-step quality from 2.58 to 3.36.
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

## Conditions

- **CIFAR-10 only.** The comparison is at 32×32 on one dataset. The paper's
  larger-image results are qualitative.
- **Training budgets are not matched.** Reflow-plus-distillation costs more
  training than distillation alone, and the table does not normalize for it.
- **The distillation uses an LPIPS loss** for the one-step student (App. A).
  Whether the balance holds with other distillation objectives, such as the
  distribution matching the video line uses, is untested.
- **At scale, the one published test points the other way, on a different
  starting point.** InstaFlow (arXiv 2309.06380, not in the record) finds
  that distilling Stable Diffusion directly to one step "fails, while reflow
  + distillation succeeds" (§3.2), and builds its one-step model on reflow.
  Its failed direct distillation starts from a diffusion model's curved
  probability-flow ODE, not from a rectified flow, so it does not test this
  practice's case. It was listed here as an implementation until the
  correction pass after [#395](https://github.com/dmarx/anthology-of-the-sota/issues/395); it implements the opposite pipeline.
- **The theory is about the reflowed coupling.** The straightness theorems
  apply to the model after reflow, not to the single-pass model most people
  train ([SOTA-266](SOTA-266.md)).
