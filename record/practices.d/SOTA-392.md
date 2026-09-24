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
introduced_by:
- LIT-636
implementations:
- 'InstaFlow'
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
- **The theory is about the reflowed coupling.** The straightness theorems
  apply to the model after reflow, not to the single-pass model most people
  train ([SOTA-266](SOTA-266.md)).
