---
number: 52
status: Proposed
formerly:
- THEORY-tmply7jq
promote_when: >-
  Equivariance measured rather than inferred — a representation-level test
  showing that generatively pretrained features track scale, pose and
  structural change where discriminatively pretrained ones are invariant to
  it, on the same images, and that the gap predicts which model groups unseen
  objects. What would not settle it: another demonstration that a generative
  prior transfers to a perception task and a discriminative one transfers
  less well, which is the observation this account is one explanation of.
  Capacity, output resolution and the survival of low-level detail through
  the encoder all predict the same ranking.
title: 'Synthesis requires equivariant representations and discriminative pretraining rewards invariant ones, which is why a generative prior groups objects it was never shown'
version: 1
tags:
- representation-and-encoding
- vision-and-graphics
date: '2026-09-21'
source:
- LIT-488
explains:
- SOTA-299
summary: >-
  Khangaonkar and Pirsiavash (2025), [LIT-488](../literature.d/LIT-488.md) — self-distillation and
  contrastive objectives explicitly reward representations that *do not
  change* under augmentation; instance segmentation needs representations
  that do. The paper's DINO control activates on objects and cannot separate
  their instances, which is the shape this account predicts.
---

<!-- inactive-ok-file: SOTA-299 — Proposed, filed in this same
     contribution; this theory declares `explains:` on it, so the citation is
     the relation itself and cannot wait on the practice being settled -->

# THEORY-052: Synthesis requires equivariant representations and discriminative pretraining rewards invariant ones, which is why a generative prior groups objects it was never shown

## Source

Khangaonkar and Pirsiavash (2025), [LIT-488](../literature.d/LIT-488.md) §4.3 — read as
[NOTE-237](../notes.d/NOTE-237.md).

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-299](../practices.d/SOTA-299.md) | finetune the generative model end to end rather than putting a head on a backbone | the backbone is not merely weaker here, it was trained to discard exactly what the task needs — so the recipe is not "use a bigger prior" but "use a prior of the right kind" |

## The account

Discriminative self-supervision is built on invariance. Self-distillation and
contrastive objectives take two augmented views of an image and require the
representation to be **the same** for both — that is the training signal.
Scale, crop, pose and structural change are precisely the nuisances those
objectives are designed to quotient away.

Instance segmentation needs the opposite. Deciding that two pixels belong to
one object and a third does not is a judgement about shape, extent and
boundary — quantities that **change** when the image changes, and that an
invariant representation has been trained to suppress.

Generative pretraining cannot take that shortcut. To synthesize a plausible
image from a corrupted or minimal input, a model has to represent where
things are, how large they are, and where one ends and the next begins. It
must be **equivariant**: when the scene changes, the representation has to
change with it.

**The prediction is specific and the paper's control matches it.** If this is
right, a discriminative encoder given a generative decoder should be able to
find *that* something is an object — semantics survive invariance — while
failing to say *which* object. That is what happens: the finetuned DINO-B
model "successfully activates on objects, but struggles to separate their
instances," reaching 14.9 average against MAE-B's 21.6 on the same decoder
and data.

It also explains why scale is not the lever. MAE on **unlabeled ImageNet-1K
alone** generalizes to art and x-rays, while DINO — a strong, heavily
validated representation — does not group. The difference between them is the
objective, not the corpus.

## Why `Proposed`

**The authors call it a hypothesis and it is not isolated.** They write "we
hypothesize" twice in the space of a paragraph. Nothing in the paper measures
equivariance or invariance directly; the account is inferred from which
models group and which do not.

**At least three rival explanations predict the same ranking.** MAE's decoder
survives into finetuning while DINO's features must be upsampled by an
attached module, so **low-level detail retention** alone would order the
models identically. The generative models operate at input resolution and the
discriminative ones do not, so **output resolution** would too. And the
generative models here are simply larger in the SD case, so **capacity** is
uncontrolled across part of the comparison.

**"Equivariant" is doing work the evidence does not pin down.** It is used as
a property of a representation, demonstrated by a downstream task that needs
it. That is compatible with the account and also with the weaker claim that
generative pretraining preserves spatial detail, which is less interesting and
harder to argue with.

## What it does not say

**It does not say discriminative pretraining is worse.** Invariance is the
right objective for classification and retrieval, and DINO is excellent at
what it was built for. The claim is that the property that makes it good
there is the property that costs it here — which is a statement about fit,
not quality.

**It does not say a generative prior contains segmentation.** It says the
prior contains the *ingredients* — boundaries, extent, part-whole structure —
and that a small amount of narrow supervision suffices to read them out. The
source's models do need finetuning; the masks emerge from ~3.7M of them, not
from zero.

**It says nothing about non-spatial tasks.** The whole argument turns on
dense, spatial, pixel-level structure. Whether an analogous
invariance/equivariance trade governs anything in language is not addressed
here and should not be read across.
