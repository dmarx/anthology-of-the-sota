---
status: Active
title: 'Fantastic Pretraining Optimizers and Where to Find Them II: Hyperball Optimization'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2026-06-01'
arxiv: '2606.16899'
first_author: 'Wen'
keywords:
- 'optimizer'
- 'weight-decay'
- 'muon'
- 'hyperparameter-transfer'
- 'weight-norm'
summary: >-
  Wen et al. (2026), [ARXIV-2606.16899](https://arxiv.org/abs/2606.16899). The follow-up that diagnoses why
  matrix optimizers' gains shrink with scale: constant decoupled weight decay
  fixes the equilibrium weight norm and so fixes the angular learning rate.
  Pinning the Frobenius norms instead recovers 20–30% over the weight-decay
  baseline.
---

# LIT-tmp2hq9o: Fantastic Pretraining Optimizers and Where to Find Them II: Hyperball Optimization

Wen et al. (2026) — [ARXIV-2606.16899](https://arxiv.org/abs/2606.16899)

## Key takeaways

- Takes its own predecessor's negative result as the problem statement:
  matrix-based optimizers such as Muon speed up pretraining, and the gain
  shrinks as model and data scale grow **under standard constant decoupled
  weight decay**. The qualifier turns out to be doing the work.
- The mechanism is the weight-decay equilibrium: training with weight decay
  settles a matrix at a norm determined by the training hyperparameters
  rather than by the data, and through that norm the decay is really setting
  the *angular* learning rate — how fast the weight matrix's direction turns.
- **Hyperball** is a wrapper rather than an optimizer: given Adam or Muon, it
  sets the Frobenius norms of the weight matrices and of their updates to
  fixed constants, which controls the angular rate directly instead of
  through a proxy.
- On Qwen3-style models up to 1.2B, Muon+Hyperball reaches a 20–30%
  token-equivalent speedup over the weight-decay baseline, and improves
  learning-rate transfer across both width and depth.

## Standing in the anthology

Filed for a convergence the record can now see. This paper and Learnable
Multipliers ([LIT-121](LIT-121.md)) diagnose the *same* pathology — the weight-decay
equilibrium norm is an artefact of the hyperparameters, not a property of
the solution — from two groups who cite different literatures, and answer it
in opposite directions. LRM gives the scale its own learned parameter and
lets the data choose it; Hyperball pins the norm to a constant and takes it
out of the optimizer's hands entirely.

That is a genuine disagreement about whether the equilibrium should be
*learned* or *removed*, and both report gains against the same baseline. The
<!-- inactive-ok: SOTA-122 — the Proposed practice this paper offers a rival remedy for -->
record holds both and prefers neither: [SOTA-122](../practices.d/SOTA-122.md) stays *Proposed*, and the
condition it names — a result from outside the authors' group — is not met
by this, which is a different remedy rather than a replication.
