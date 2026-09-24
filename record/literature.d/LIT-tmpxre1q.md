---
status: Active
title: 'Emerging Properties in Self-Supervised Vision Transformers'
version: 1
tags:
- representation-and-encoding
- vision-and-graphics
- model-stability
date: '2026-09-24'
published: '2021-04-29'
arxiv: '2104.14294'
first_author: 'Caron'
keywords:
- 'dino'
- 'self-distillation'
- 'knn-evaluation'
- 'collapse-avoidance'
- 'attention-segmentation'
implementations:
- 'DINO'
summary: >-
  Caron et al. (2021), [ARXIV-2104.14294](https://arxiv.org/abs/2104.14294). **The origin of the DINO line, which
  31 documents here reference and 12 practices touch.** Self-supervised ViT
  features carry explicit semantic segmentation that supervised ViTs and
  convnets do not show as clearly, and reach **78.3% ImageNet top-1 with a
  plain k-NN** — no finetuning, no linear probe, no augmentation. Collapse is
  avoided by **centering and sharpening the teacher output alone**, with no
  predictor.
compared_against:
- LIT-599
---

# LIT-tmpxre1q: Emerging Properties in Self-Supervised Vision Transformers

Caron, Touvron, Misra, Jégou, Mairal, Bojanowski and Joulin (2021) — [ARXIV-2104.14294](https://arxiv.org/abs/2104.14294)

## What it is

**DINO: self-distillation with no labels.** A student network predicts the
output of a teacher built as a momentum encoder of the student, through a plain
cross-entropy loss. No negatives, no contrastive term, no predictor head.

The paper's own framing is that it *"completes the interpretation initiated in
BYOL of self-supervised learning as a form of Mean Teacher self-distillation
with no labels."*

## The two results the field took from it

**Semantic segmentation appears in the attention maps.** Self-supervised ViT
features *"contain explicit information about the semantic segmentation of an
image, which does not emerge as clearly with supervised ViTs, nor with
convnets."* This is what unsupervised object-discovery methods were built on,
and it is the property the rest of the lineage spends its time losing and
recovering.

**78.3% ImageNet top-1 with a bare k-NN**, on a small ViT, *"without any
finetuning, linear classifier nor data augmentation."* The evaluation matters
as much as the number: it says the representation is good without any fitted
read-out.

And a condition the paper states itself: the k-NN result *"only emerge[s] when
combining certain components such as momentum encoder and multi-crop
augmentation."* Multi-crop is SwAV's (`LIT-598`, and `SOTA-370` is sourced
there correctly).

## The correction it forces on a practice the record already holds

`SOTA-365` is `Active` and `converged` — *"Learn without negatives by breaking
the symmetry: a predictor on one branch and a stop-gradient on the other"* —
and its consensus note says:

> the `#304` units still to file — **DINO and DINOv2** — carry the same
> structure.

**They do not.** This paper's collapse avoidance is, in its own words, that
*"our method can work with only a centering and sharpening of the teacher
output to avoid collapse"*. There is no predictor on either branch. Centering
and sharpening are two opposing operations on the teacher's output
distribution, and that opposition is what does the work the predictor does in
BYOL and SimSiam.

So the asymmetric-predictor family is **one** route to learning without
negatives and DINO is a **second**. `SOTA-365` is amended in this same
contribution; its recommendation stands, and what changes is a claim its note
made about a paper the record did not hold.

Worth noticing how the error arose: the note is careful, it names its
uncertainty, and it asserts a structural fact about two specific unfiled
papers. **A gap the record has written down is still a gap**, and a claim made
across one is not load-bearing until somebody reads the paper.

## Standing in the anthology

Filed as the origin of a lineage the record held only the middle of.
`LIT-599` is DINOv2, `LIT-662` is the registers paper, and
`LIT-tmpuy1r1` is DINOv3, filed alongside this.

The immediate reason is a number this record printed yesterday. The registers
note reports DINOv2 at 35.3 corloc on VOC 2007 against **DINO's 61.9** — the
headline evidence that DINOv2 regressed object discovery — cited against a
paper the record did not hold. That is this paper.

`#304`'s SSL audit listed DINO as a unit still to file, and `SOTA-365`'s
consensus note says so in as many words. The gap was known, recorded, and open
for a day short of a month.
