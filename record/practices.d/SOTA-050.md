---
number: 50
status: 'Active'
title: 'Scale attention weights by 1/sqrt(head_dim)'
version: 1
tags:
- model-stability
date: '2026-08-24'
published: '2017-06-01'
source:
- LIT-008
summary: >-
  Vaswani et al. (2017), [LIT-008](../literature.d/LIT-008.md) — [ARXIV-1706.03762](https://arxiv.org/abs/1706.03762).
extended_by:
- SOTA-192
---

# SOTA-050: Scale attention weights by 1/sqrt(head_dim)

## Source

Vaswani et al. (2017), [LIT-008](../literature.d/LIT-008.md) — [ARXIV-1706.03762](https://arxiv.org/abs/1706.03762).

## Why the square root, specifically

The dot product of two vectors whose components are independent with unit
variance has variance equal to their dimension, so raw attention logits grow
like the head dimension. Feed those into a softmax and it saturates: one
weight goes to nearly one, the rest to nearly zero, and the gradient through
the softmax vanishes.

Dividing by √d_head restores unit variance, which keeps the softmax in the
range where it still has a gradient. The scaling is not a tuning constant — it
is the factor that makes the initialisation-time variance independent of head
dimension, which is why it is the same in every implementation and why nobody
tunes it.

## Where it stops being sufficient

At scale it does not hold on its own. Attention logits can still grow during
training as the query and key projections align, and the practices that bound
them — [SOTA-131](SOTA-131.md)'s QK-Clip, QK-norm and its relatives — exist because the
initialisation-time argument says nothing about step 100,000.

That is the useful reading of this practice today: a necessary normalisation
that everything assumes, plus the observation that it is not the whole of the
problem it addresses. Filed under model-stability rather than
attention-techniques for that reason, which is one of the seams the
unbound-lineage report keeps returning.
