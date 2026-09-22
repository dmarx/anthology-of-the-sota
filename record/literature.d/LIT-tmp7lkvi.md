---
status: Active
title: 'Tensor Programs III: Neural Matrix Laws'
version: 1
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
date: '2026-09-23'
published: '2020-09-01'
arxiv: '2009.10685'
first_author: 'Yang'
keywords:
- 'tensor-programs'
- 'free-independence'
- 'random-matrix-theory'
- 'dynamical-isometry'
- 'master-theorem'
implementations: []
extends:
- LIT-tmphvjvq
summary: >-
  Yang (2020), [ARXIV-2009.10685](https://arxiv.org/abs/2009.10685). At random initialization and infinite
  width, a network's pre-activations become asymptotically free (in the
  random-matrix sense) of its weights, for any architecture: the Free
  Independence Principle. This rigorously justifies the Jacobian
  singular-value calculations behind dynamical isometry, which had assumed
  it, and gives a second justification of the gradient independence
  assumption. The general Master Theorem is also what TP-IV uses.
extended_by:
- LIT-548
---

# LIT-tmp7lkvi: Tensor Programs III: Neural Matrix Laws

Yang, Microsoft Research (2020) — [ARXIV-2009.10685](https://arxiv.org/abs/2009.10685)

## Key takeaways

- **Free Independence Principle:** weights are asymptotically free from the
  diagonal matrices built from (pre-)activations under any bounded
  coordinatewise function. This holds for any NETSOR⊤-expressible
  architecture, at random initialization only. The paper makes no claim
  about trained weights
- **What it justifies:** the free-independence assumption used to compute a
  network's input-output Jacobian singular-value distribution, the quantity
  behind dynamical isometry and the training of extremely deep networks.
  That calculation had been checked empirically but not proved
- **A new route to random matrix laws:** it re-derives the semicircle and
  Marchenko–Pastur laws from its Master Theorem, as a benchmark for the
  method
- **The Master Theorem** for general tensor programs, which TP-IV then
  applies to the whole of training

## Standing in the anthology

**Filed from `#163`**, as the third step of the Tensor Programs line. It
`extends` TP-II ([LIT-tmphvjvq](LIT-tmphvjvq.md)), and TP-IV ([LIT-548](LIT-548.md)) `extends` it. No
practice.

**Skimmed, not read:** abstract and introduction. No NOTE.
