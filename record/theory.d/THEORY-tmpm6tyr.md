---
status: Proposed
title: "Soft targets transfer the teacher's similarity structure over wrong classes, which carries more information per example than a hard label"
version: 1
tags:
- inference-optimization
- training-optimization
date: '2026-09-25'
source:
- LIT-tmpa3ip4
explains:
- SOTA-tmprzws7
promote_when: >-
  An experiment that holds the soft targets' entropy fixed while scrambling
  the ranking over wrong classes, and shows that the ranking is what
  transfers. Until then the account cannot be told apart from generic
  output-confidence regularization, which predicts the same gains. A further
  distillation success does not help, because both accounts predict it.
summary: >-
  Hinton et al. (2015), [LIT-tmpa3ip4](../literature.d/LIT-tmpa3ip4.md). The small probabilities a trained model
  assigns to wrong classes encode how it generalizes: a BMW is rarely
  mistaken for a garbage truck, but far more often than for a carrot. Raising
  the temperature exposes that structure, and a student trained on it gets
  more information and less gradient variance per example. This is the
  account usually called "dark knowledge", a phrase that is not in the paper.
  Its evidence does not rule out the simpler reading, that soft targets are a
  regularizer.
---

<!-- inactive-ok-file: SOTA-tmprzws7 — Proposed; the practice this account would explain -->

# THEORY-tmpm6tyr: Soft targets transfer the teacher's similarity structure over wrong classes, which carries more information per example than a hard label

## Source

Hinton, Vinyals and Dean (2015), [LIT-tmpa3ip4](../literature.d/LIT-tmpa3ip4.md), Introduction and §§3, 6.

## The account

"The relative probabilities of incorrect answers tell us a lot about how the
cumbersome model tends to generalize." At `T = 1` those probabilities are
tiny and contribute almost nothing to the cross-entropy. At higher `T` they
are exposed. "When the soft targets have high entropy, they provide much more
information per training case than hard targets and much less variance in the
gradient between training cases, so the small model can often be trained on
much less data … and using a much higher learning rate."

## The evidence offered, and why it does not settle the account

- **The omitted-class transfer.** A student never shown a 3 gets 98.6% of test
  3s right, but only after the 3's bias is raised by 3.5, a value chosen
  because it "optimizes overall performance on the test set". Without that
  shift it errs on 133 of 1,010 test 3s.
- **The 3%-data result.** 44.5% → 57.0% test frame accuracy on speech with soft
  targets. The teacher was trained on the full data, so the targets carry
  information about the other 97%. That fits the account. It also fits "the
  teacher is a better label source".
- **The "much higher learning rate"** is asserted and never tested.

None of these separates *the ranking over wrong classes* from *any
softening of the target*. Label smoothing softens targets with no ranking at
all. An account that predicted only what label smoothing also predicts would
not need the similarity structure. The record holds no paper that runs that
separation in either direction.

## What it explains

Why [SOTA-tmprzws7](../practices.d/SOTA-tmprzws7.md) uses a raised temperature at all, and why
a starved student prefers a moderate one. Under this account a moderate `T`
keeps the informative wrong-class ranking and drops the noise in very
negative logits that a small model cannot fit anyway.
