---
status: Active
consensus: emerging
consensus_note: >-
  Real and adopted but not dominant. Both papers reach 73.2% ImageNet linear,
  within a couple of points of the asymmetric family, and the variance term
  has evidence of working *outside* its own method — VICReg reports it
  stabilising other methods. What the record cannot show is wide adoption:
  the descendants it holds (`LIT-216`) and the ones `#304` still lists (DINO,
  DINOv2) all took the asymmetric route. `emerging` rather than `converged`
  on those grounds, and the reading is about the loss-side family, not about
  either paper's rank.
title: 'Or put the anti-collapse constraint in the loss, as a variance floor and a decorrelation term'
version: 1
tags:
- representation-and-encoding
- model-stability
date: '2026-09-23'
source:
- LIT-tmpipfcy
- LIT-tmpovcux
introduced_by:
- LIT-tmpovcux
implementations: []
---

# SOTA-tmpacu6q: Or put the anti-collapse constraint in the loss, as a variance floor and a decorrelation term

## Source

Bardes et al. (2021), [LIT-tmpipfcy](../literature.d/LIT-tmpipfcy.md) — [ARXIV-2105.04906](https://arxiv.org/abs/2105.04906). Introduced by Zbontar
et al. (2021), [LIT-tmpovcux](../literature.d/LIT-tmpovcux.md) — [ARXIV-2103.03230](https://arxiv.org/abs/2103.03230), which stated the loss-side
approach first in its cross-correlation form.

## The claim

A joint-embedding loss admits the constant solution. [SOTA-tmp1kmsu](SOTA-tmp1kmsu.md) removes it
by making the two branches different functions. The alternative is to remove
it from the objective directly, with two terms that a constant output cannot
satisfy:

- **a variance floor** — a hinge `max(0, γ − std(z_j))` per embedding
  dimension over the batch, `γ = 1`. A constant dimension has zero standard
  deviation and is penalised by exactly `γ`. This forbids collapse
  arithmetically rather than dynamically.
- **a decorrelation term** — push the off-diagonal covariance (VICReg) or
  cross-correlation (Barlow Twins) entries toward zero, so the dimensions do
  not all encode the same thing. This forbids the *partial* collapse that a
  variance floor alone allows: `d` copies of one feature each pass the floor.

Both are needed, and they fail differently. The floor stops the embedding
becoming a point; the decorrelation stops it becoming a line.

## What this buys

The list VICReg gives of what it then does not need is the argument: **weight
sharing between the branches, batch normalization, feature-wise
normalization, output quantization, stop-gradient, memory banks.** Every item
is a mechanism some other method treats as load-bearing, and dropping the
whole set at once is evidence that none of them is fundamental to the problem.

The practical consequence is that the two branches need not be the same
network — VICReg regularises each branch **separately**, where Barlow Twins
couples them through a cross-correlation. That is the difference between the
two papers and it is what makes multi-modal or asymmetric-encoder variants
straightforward.

**The variance term transplants.** VICReg reports it stabilising the training
of *other* methods and improving them, which is the only component in this
cluster with evidence of working outside the method that introduced it. That
is why this is stated as a component you can add rather than as a method you
must adopt.

## Conditions

- **Dimensionality runs the opposite way from the asymmetric family.**
  Barlow Twins keeps improving with a very high-dimensional projector output,
  "in stark contrast" to BYOL and SimCLR, where the projector reduces
  dimension sharply. The off-diagonal term is a budget of decorrelated
  directions; give it room.
- **The terms are computed over the batch**, so very small batches make the
  variance and covariance estimates noisy. This is a milder batch dependence
  than negatives impose, not an absent one.
- **It does not remove the augmentation dependence.** Barlow Twins reports
  being "not robust to removing some types of data augmentations, like SimCLR
  but unlike BYOL", and says so as a disadvantage of its own method.
- **`γ` and the term weights are hyperparameters** in a place the asymmetric
  family has none, which is the cost of making the constraint explicit.

## Known implementations

-
