---
status: Proposed
promote_when: >-
  A second controlled measurement, in another vision backbone, of the same
  position-encoding variants scored on both a classification task and a dense
  task. The claim that would be promoted is the task-dependence of the sign,
  not the size of the gap. A measurement on a plain global-attention ViT would
  be the most useful version, because the source's relative bias lives inside a
  7x7 window and that is the part least likely to transfer.
consensus: unreplicated
consensus_note: >-
  One group, one architecture, one ablation table (LIT-tmpev8pm, Table 4,
  Swin-T). The relative position bias itself is widely adopted in the Swin
  lineage and in the window-attention backbones that followed it, but adoption
  is not a test (ADR-017) and nobody has re-run the three-task comparison. What
  is genuinely unreplicated is the part this practice turns on: that the
  absolute term's sign depends on the downstream task. Read as of 2026-09.
title: 'In a vision backbone, carry position with a relative bias inside the attention window and do not add an absolute position embedding on top'
version: 1
tags:
- representation-and-encoding
- vision-and-graphics
- model-architecture
date: '2026-09-26'
source:
- LIT-tmpev8pm
introduced_by:
- LIT-tmpev8pm
implementations:
- 'Swin Transformer'
summary: >-
  Liu et al. (2021), [LIT-tmpev8pm](../literature.d/LIT-tmpev8pm.md), Table 4. One architecture, one recipe, three
  tasks. A relative position bias inside the attention window is best or
  tied-best on all three. An absolute position embedding is worth **+0.4**
  ImageNet top-1 and **-0.2** COCO box AP and **-0.6** ADE20K mIoU, and adding
  it on top of the relative bias costs **2.1 mIoU** while changing ImageNet
  nothing. The recommendation is the sign, not the size: this is the one design
  choice in the table that a classification benchmark scores backwards.
---

# SOTA-tmp2g7eg: In a vision backbone, carry position with a relative bias inside the attention window and do not add an absolute position embedding on top

## Source

Liu, Lin, Cao, Hu et al. (2021), [LIT-tmpev8pm](../literature.d/LIT-tmpev8pm.md) — Swin Transformer,
§3.2 and Table 4.

## The claim

Add a learned bias `B` to the attention logits that depends only on the
*relative* offset between two positions:

    Attention(Q, K, V) = SoftMax(QKᵀ/√d + B) V

with `B ∈ ℝ^{M²×M²}` drawn from a `(2M−1) × (2M−1)` parameter matrix, since
offsets along each axis lie in `[−M+1, M−1]`. Do not also add an absolute
position embedding to the input.

One architecture (Swin-T), one recipe, four variants, scored on ImageNet-1K
classification, COCO detection with Cascade Mask R-CNN, and ADE20K
segmentation with UperNet:

| | ImageNet top-1 | COCO AP_box | COCO AP_mask | ADE20K mIoU |
|---|---|---|---|---|
| no position encoding | 80.1 | 49.2 | 42.6 | 43.8 |
| absolute only | 80.5 | 49.0 | 42.4 | 43.2 |
| absolute + relative | 81.3 | 50.2 | 43.4 | 44.0 |
| **relative only** | **81.3** | **50.5** | **43.7** | **46.1** |

**The relative bias is best or tied-best on all three tasks**: +1.2/+0.8 top-1,
+1.3/+1.5 box AP, +2.3/+2.9 mIoU against no encoding and against absolute.

**The absolute term is the row that changes sign.** Against no encoding at all
it buys **+0.4** top-1 and costs **−0.2** box AP, **−0.2** mask AP and **−0.6**
mIoU. Stacked on the relative bias it leaves ImageNet unchanged at 81.3 and
costs **2.1 mIoU** (46.1 → 44.0) and 0.3 box AP. The paper's own sentence is
that absolute position embedding "improves image classification accuracy
(+0.4%)" but "harms object detection and semantic segmentation".

## Why the recommendation is about the sign

The three metrics are not commensurable — a point of top-1 accuracy, a point
of box AP and a point of mIoU are different quantities — so nothing here
supports "the effect is N times larger on dense tasks". What needs no
commensurability is the **direction**: one design choice in this table improves
the classification score and degrades both dense scores, in one model, under
one recipe. A practitioner who selects a position encoding on ImageNet top-1
and ships the backbone into detection or segmentation has, for this choice,
optimised the wrong sign.

That is also why this is filed as a recommendation about the encoding rather
than about evaluation. "Ablate on a dense task too" would be the larger lesson,
and one sign flip in one table is thin evidence for asking anybody to fund two
extra benchmark suites. Dropping the absolute term is free.

## Conditions

- **Measured inside 7×7 local windows in a hierarchical backbone.** The bias
  matrix is indexed by within-window offsets. A global relative encoding on a
  plain ViT, or any of the 1D relative schemes the language side uses, is a
  different object and this does not measure it.
- **Swin-T only, and one seed per cell.** The dense-task deltas of −0.2 box AP
  and −0.6 mIoU are small enough that a seed study could move them; the 2.1
  mIoU penalty for stacking absolute on relative is not, and is the more
  robust half of the evidence.
- **It says nothing about which position encoding to use in a 1D sequence
  model.** [SOTA-063](SOTA-063.md) (RoPE) and [SOTA-153](SOTA-153.md) (no encoding in a hybrid's global
  layers) are about causal language models, where the causal mask itself
  carries position — a mechanism that does not exist in a bidirectional vision
  encoder. Swin is an independent demonstration that position can be carried
  locally without a causal mask, but it carries it **explicitly**, with a
  learned bias, which is the opposite of what those two practices recommend.
- **The mechanism is unexplained.** The paper attributes the flip to
  translation invariance mattering more for dense prediction, and runs no
  experiment isolating that. No theory is filed; see [LIT-tmpev8pm](../literature.d/LIT-tmpev8pm.md).
