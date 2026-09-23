---
status: Active
consensus: converged
consensus_note: >-
  Crop-plus-colour survived every later method this record has looked at —
  MoCo v2 adopted it, and the augmentation stack is the part SwAV, BYOL and
  DINO inherit rather than redesign. The general form, that the augmentation
  set defines the task, is stated far less often than the specific recipe is
  copied, which is the usual sign of a converged practice nobody re-derives.
  Read as of 2026-09; the `#304` units still to file are where it would be
  falsified.
title: 'Compose augmentations so the shortcut dies, and tune them for the contrastive objective rather than the supervised one'
version: 1
tags:
- data-pipeline
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmpwwvv6
introduced_by:
- LIT-tmpwwvv6
implementations: []
---

# SOTA-tmp6nbsn: Compose augmentations so the shortcut dies, and tune them for the contrastive objective rather than the supervised one

## Source

Chen et al. (2020), [LIT-tmpwwvv6](../literature.d/LIT-tmpwwvv6.md) — [ARXIV-2002.05709](https://arxiv.org/abs/2002.05709).

## The claim

In a method that learns by matching two views of the same example, **the set
of augmentations is the task specification**. Choosing it is not
preprocessing hygiene; it is deciding what the model is asked to become
invariant to, and therefore what it is allowed to throw away.

Two consequences, both measured:

**Compose, and compose specifically to kill the shortcut.** No single
transformation is enough — and the giveaway is that the model can still
"almost perfectly identify the positive pairs" while learning a poor
representation. Solving the pretext task and learning the representation are
different events. Random cropping alone fails because crops of one image
share a colour histogram, so colour identifies the image; the paper shows the
histograms separating. Crop **with** colour distortion is what works, because
the second augmentation destroys the statistic the first left intact.

**Do not import an augmentation policy from a supervised recipe.** Across
colour-distortion strength 1/8 → 1, the contrastive linear probe rises
59.6 → 64.5 while the supervised model falls 77.0 → 75.4 — opposite
gradients on the same dial. AutoAugment, a policy *searched under
supervision*, is the best option for the supervised model (77.1) and worse
than plain crop+colour for the contrastive one (61.1 vs 64.5).

## How to use it

The transferable procedure is not the recipe, it is the question: **what
statistic survives my positive-pair construction and identifies the example
on its own?** Whatever that is, an augmentation must destroy it, or the model
will find it. Colour histograms are the answer for image crops. For another
modality the shortcut will be something else — recording channel, document
length, speaker identity — and the same failure looks like a pretext task
solved to near-perfect accuracy with a representation that transfers badly.

## Conditions

- **This is about invariance-by-augmentation methods**, which is most
  joint-embedding self-supervision but not all pretraining. A masked-region
  objective (`SOTA-250`) specifies its task differently.
- **Every invariance is also a loss.** Destroying colour means the
  representation may no longer encode colour, which is a cost paid by any
  downstream task that needed it. [SOTA-tmpca2pu](SOTA-tmpca2pu.md) is the partial mitigation:
  the head absorbs the invariance and the layer before it keeps more.
- **The specific policy is not the claim.** Crop + colour + blur is SimCLR's
  answer for ImageNet in 2020. The claim is that the answer is objective-
  specific and must be derived, not inherited.
- **Measured on ImageNet linear evaluation.** The opposite-gradient result is
  one sweep on one dataset with one architecture, and its force comes from
  the direction of the effect rather than its size.

## Known implementations

-
