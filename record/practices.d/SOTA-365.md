---
number: 365
status: Active
formerly:
- SOTA-tmp1kmsu
consensus: converged
consensus_note: >-
  The asymmetric family is what the descendants inherited. `LIT-216`
  (I-JEPA), which this record already held, is built on a predictor plus an
  EMA target; the `#304` units still to file — DINO and DINOv2 — carry the
  same structure. What has not converged is *why* it works — the body cites
  the deferred account — and a converged practice with a contested
  explanation is exactly the pair `ADR-031` splits apart. Read as of
  2026-09.
title: 'Learn without negatives by breaking the symmetry: a predictor on one branch and a stop-gradient on the other'
version: 1
tags:
- representation-and-encoding
- model-architecture
- model-stability
date: '2026-09-23'
source:
- LIT-594
- LIT-593
introduced_by:
- LIT-594
implementations: []
explained_by:
- THEORY-087
---

# SOTA-365: Learn without negatives by breaking the symmetry: a predictor on one branch and a stop-gradient on the other

## Source

Grill et al. (2020), [LIT-594](../literature.d/LIT-594.md) — [ARXIV-2006.07733](https://arxiv.org/abs/2006.07733), and Chen & He (2020),
[LIT-593](../literature.d/LIT-593.md) — [ARXIV-2011.10566](https://arxiv.org/abs/2011.10566).

## The claim

You can drop the negatives entirely. Match two augmented views of the same
input and nothing else — **provided the two branches are not the same
function**.

The minimal recipe, which is SimSiam's:

1. one encoder, shared weights, both views through it;
2. a small **prediction MLP** on one branch only;
3. a **stop-gradient** on the other branch.

BYOL adds a third asymmetry — the unpredicted branch is an EMA copy rather
than the same weights — and reaches 74.3% ImageNet linear against SimSiam's
67.7% at 100 epochs. The EMA helps. SimSiam's result is that it is not
*required*.

## What is load-bearing, as far as anyone has shown

- **Stop-gradient is not optional.** Removing it, with everything else held
  fixed, sends the loss to its minimum of −1 immediately — the optimiser
  finds the constant solution in a few steps.
- **The predictor is not optional either.** Removing it from BYOL yields an
  unsupervised Mean Teacher, which collapses.
- **The EMA target is optional, but only just.** BYOL can drop it if the
  predictor is kept near-optimal — solved in closed form per batch (52.5%)
  or merely given a higher learning rate (66.5%). Raise the projector's rate
  as well and it falls to ≈25%. What matters is the predictor being ahead of
  what it predicts.

So the shared content of the two papers is: **the branch being predicted
must not be chasing the branch predicting it.** Every mechanism in this
family is a way of arranging that.

## Why bother, when negatives work

Negatives cost a batch or a queue ([SOTA-363](SOTA-363.md)) and they impose a
distribution you must design — the negative sampling *is* an assumption that
two different images are dissimilar, which is wrong for near-duplicates and
for fine-grained classes. Removing them removes that assumption and the
memory that carried it.

## Conditions

- **Nothing here explains why it works**, and the two papers' explanations
  <!-- inactive-ok: THEORY-087 — Deferred by design: the question is open and this cluster is where the record says so. Citing it is the point, not an oversight. -->
  are incompatible. [THEORY-087](../theory.d/THEORY-087.md) is the dispute; treat the recipe as
  empirical and do not reason from the mechanism.
- **The collapse failure is silent unless you look for it.** Loss goes
  *down*. Run [SOTA-366](SOTA-366.md).
- **Weight decay is part of the method.** BYOL reports that removing it
  makes both BYOL and SimCLR diverge.
- **The augmentation dependence does not go away** ([SOTA-361](SOTA-361.md)); these
  methods still rely on the view construction to define what is invariant.
- **The alternative family exists and is competitive** — [SOTA-367](SOTA-367.md) puts
  the constraint in the loss instead and lands within a couple of points.

## Known implementations

-
