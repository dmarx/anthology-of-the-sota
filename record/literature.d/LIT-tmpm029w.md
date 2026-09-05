---
status: Active
title: 'Demystifying Training-Time Augmentation for Data-Constrained Language Model Pretraining'
version: 1
tags:
- data-pipeline
date: '2026-09-05'
published: '2026-06-01'
arxiv: '2606.16246'
first_author: 'Chen'
keywords:
- 'data-augmentation'
- 'multi-epoch-training'
- 'overfitting'
- 'fill-in-the-middle'
- 'data-constrained'
summary: >-
  Chen et al. (2026), [ARXIV-2606.16246](https://arxiv.org/abs/2606.16246). Autoregressive pretraining
  overfits badly under heavy repetition; three orthogonal families of
  augmentation — token noise, sequence permutation, offset targets — delay it
  and make hundreds of epochs on a fixed corpus productive.
---

<!-- inactive-ok-file: SOTA-124 — the Proposed practice this paper offers a third position on -->
# LIT-tmpm029w: Demystifying Training-Time Augmentation for Data-Constrained Language Model Pretraining

Chen et al. (2026) — [ARXIV-2606.16246](https://arxiv.org/abs/2606.16246)

## Key takeaways

- The premise is the regime, stated plainly: compute capacity is outrunning
  the rate at which new high-quality text is produced, so pretraining is
  moving to a data-constrained, compute-abundant setting where multi-epoch
  training on a fixed corpus has to be made *productive*.
- The failure it starts from is unambiguous: standard autoregressive
  pretraining **overfits severely** in this setting, reaching its optimum
  early and then deteriorating continuously.
- Three orthogonal augmentation families for AR pretraining: **token-level
  noise** (masking, random replacement), **sequence permutations**
  (right-to-left prediction, fill-in-the-middle), and **target offset
  prediction** (predict x_{t+i} for i > 1).
- Each individually delays overfitting and lowers validation loss against the
  baseline, with random token replacement the best single method; combining
  categories lowers the minimum further. The claim is hundreds of productive
  epochs on the same data.

## Standing in the anthology

The third position in a disagreement the record now holds in full. [SOTA-124](../practices.d/SOTA-124.md)
says heavy repetition is safe when epoch size exceeds the memorization
window; [LIT-tmp7fu4d](LIT-tmp7fu4d.md) says four epochs and then diminishing returns; this says
repetition overfits severely *and* the overfitting is a property of the
objective rather than of repetition, removable with augmentation.

That third framing is the useful one, because it makes the other two
falsifiable in the same terms: if augmentation is what buys productive
multi-epoch training, then a recipe repeating a source a hundred times is
either augmenting implicitly or paying a cost nobody measured.

There is also a connection the record can make and the paper does not.
Fill-in-the-middle appears here as a *sequence-permutation augmentation*
valued for regularisation, while [SOTA-128](../practices.d/SOTA-128.md) records FIM as a capability to be
trained for, and [LIT-119](LIT-119.md) reached for dropout when heavy repetition of a small
FIM corpus hurt HumanEval-FIM. Same transformation, three purposes.
