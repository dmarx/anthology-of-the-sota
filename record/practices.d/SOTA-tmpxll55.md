---
status: Proposed
promote_when: >-
  Early dropout tried on a language-model pretraining run, where underfitting
  is the normal regime rather than a small-model artifact, with training loss
  reported alongside the downstream number. A further vision result would
  broaden the evidence and would not reach the case this record is mostly
  about.
consensus: unreplicated
consensus_note: >-
  One group, one paper, one domain. Nobody has published a failure either.
  Scheduled dropout strength is not itself new — the source compares against
  linearly increasing and curriculum schedules and beats both — but moving
  dropout to a *prefix* of training, and reporting a fall in training loss as
  the point, is this paper's.
title: 'Put dropout at the start of training if the model underfits, and at the end if it overfits — the schedule decides the sign, not the rate'
version: 1
tags:
- model-stability
- training-optimization
date: '2026-09-21'
source:
- LIT-tmpfdpkj
introduced_by:
- LIT-tmpfdpkj
implementations: []
explained_by:
- THEORY-tmpbaqnm
---

# SOTA-tmpxll55: Put dropout at the start of training if the model underfits, and at the end if it overfits — the schedule decides the sign, not the rate

## Source

Liu, Xu, Jin, Shen and Darrell (2023), [LIT-tmpfdpkj](../literature.d/LIT-tmpfdpkj.md) — read as
[NOTE-tmpbrbwv](../notes.d/NOTE-tmpbrbwv.md). ImageNet-1K, models from 5M to 86M parameters, three
seeds.

## The claim

Dropout has been tuned on one axis — the rate — and scheduled on another that
was barely used. Move it, and the operator changes sign.

**If the model underfits** (it does *worse* with standard dropout): apply
dropout for the first stretch of training, then switch it off. This lowers
**training** loss, which no regularizer does, and raises test accuracy.
ViT-T on ImageNet-1K goes 73.9 → 74.3 with early dropout and 73.9 → **67.9**
with standard dropout; training loss goes 3.443 → 3.394 and 3.443 → 3.885
respectively.

**If the model overfits** (it does better with standard dropout): skip dropout
for the first stretch and apply it afterwards. ViT-B 81.6 → **82.3**, beating
a linearly increasing schedule (82.1) and a curriculum schedule (82.0) at
their own best settings.

Stochastic depth substitutes for dropout throughout and often does better.

## How to tell which regime you are in

The source's test is the outcome of the comparison: **if the model generalizes
better with standard dropout it is overfitting; if better without, it is
underfitting.** That is honest and it is not free — the precondition costs a
run with and without.

[SOTA-240](SOTA-240.md) gives the cheaper prior: the question is whether the model can
memorize what it is shown. A model small relative to its corpus underfits.

## Settings

Two hyperparameters, both reported robust on the source's models:

- **Switch point** — anywhere from 1% to 50% of total epochs works. The
  mechanism suggests it should sit near where the gradient-direction-error
  curves cross, about 1000 iterations for ViT-T, but no result ties the two
  together and the robustness range is wide enough that it may not matter.
- **Drop rate** — chosen as for standard dropout, "moderately robust".

## Conditions

**All the evidence is vision.** ImageNet-1K classification and vision
transfer. Nothing here is a language model, and the underfitting regime the
practice targets is a 5–20M-parameter model on a fixed 1.2M-image set — not
obviously the same object as a large model under-trained on a large corpus,
which is the underfitting a reader of this record is likely to have.
`ADR-026` is why the practice is filed anyway: a claim takes its kind, not its
domain. It does not make the evidence wider.

**Read the table against the noise.** Three seeds, average standard deviation
**0.142%**. The +0.4 to +0.9 results are real; ConvNeXt-F's +0.2 is not, and
the source gives you the deviation to work that out with.

**The gains survive a stronger baseline, and shrink.** Doubling epochs and
weakening mixup and cutmix raised ViT-T to 76.3, past published numbers, and
early dropout still added 0.4. So it is not only rescuing an undertrained
recipe — but the margin is what it is.

**Training loss is the claim to check.** If you try this and training loss does
not fall, you have not reproduced the effect, whatever the accuracy did. That
is the only measurement here that distinguishes an optimization intervention
from a lucky regularizer.

**The switch point has no theory.** The one number is where ViT-T's curves
crossed. The 1%–50% robustness result is doing the work, and it is an
empirical range on one family.

## Its relation to [SOTA-240](SOTA-240.md)

None of this contests [SOTA-240](SOTA-240.md), which says to apply dropout where the
model can memorize and not where it cannot. The source's six-point drop on
ViT-T is the strongest evidence in the record for that practice's negative
half.

What it adds is that the negative half is about dropout **throughout
training**. On a prefix, in the same regime, the same operator helps. A reader
following `SOTA-240` alone would conclude "no dropout" and the fuller
conclusion is "no dropout after the first stretch".
