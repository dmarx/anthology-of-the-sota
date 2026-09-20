---
status: Active
title: 'Hidden Breakthroughs in Language Model Training'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-20'
published: '2025-06-01'
arxiv: '2506.15872'
first_author: 'Kangaslahti'
keywords:
- 'phase-transitions'
- 'loss-decomposition'
- 'learning-dynamics'
- 'interpretability'
implementations:
- LIT-tmpdoa3b
summary: >-
  Kangaslahti et al. (2025), [ARXIV-2506.15872](https://arxiv.org/abs/2506.15872). A smooth loss curve is
  not evidence of smooth training. POLCA decomposes the change in loss along
  a low-rank basis of the training subspace and per example, and the
  breakthroughs the aggregate hides come back — on synthetic arithmetic it
  recovers the skill of carrying a digit, which clustering the exact loss
  curves does not.
---

# LIT-tmpdoa3b: Hidden Breakthroughs in Language Model Training

## Key takeaways

- **The premise is an artifact of averaging.** Visible discontinuities in a
  loss curve get studied as conceptual breakthroughs, and the smoothness of
  the rest gets read as "nothing happening". The paper argues breakthroughs
  are frequent throughout training and the scalar loss hides them — the more
  differently-timed transitions there are underneath, the smoother the sum
  looks. **Smoothness is what many transitions look like when added up.**
- **Two decompositions, because one is not enough.** Disaggregate the
  aggregate into *per-example* losses and cluster examples with synchronised
  changes. But one example can depend on several breakthroughs, and distinct
  concepts arriving together merge their clusters — so also decompose the
  loss change along *directions* in a low-rank subspace of the trajectory.
- **POLCA** is Loss Change Allocation modified in two ways: an arbitrary
  orthonormal basis instead of axis-aligned units, and per-example rather
  than dataset-level attribution.
- **The basis is built from curvature.** Iteratively, at each checkpoint,
  project the loss Hessian onto the nullspace of the basis so far and append
  the top eigenvectors, via Hessian-vector products. The very top
  eigenvectors reflect local oscillation rather than long-term movement, so
  directions that do not lower loss over the run are discarded.
- **The validation is a negative control.** On synthetic arithmetic,
  clustering the exact loss curves recovers digit positions. Clustering POLCA
  curves recovers digit positions **and** the skill of carrying — a concept
  the aggregate cannot see. Maximum carry fraction for exact-loss clustering
  is 0.514, which is chance.
- Offered as a route to unsupervised interpretability: find the transitions
  first, then ask what they are.
- Small scale by necessity — a 9M-parameter 3-layer transformer, POLCA
  computed every 20 iterations, 50 basis vectors.

## Standing in the anthology

**It generalises a finding the record filed two days ago.** [THEORY-028](../theory.d/THEORY-028.md) says
one specific plateau is the attention recall circuit being built, shown by
patching the circuit in. This says the same kind of thing is happening
throughout training and is invisible for a different reason — not because the
loss is flat, but because the loss is an average over data and directions
that are each doing something abrupt.

Together they make a claim the record can now state: **the aggregate loss
curve is a lossy projection of training, and it is lossy in at least three
identified ways** — it time-averages oscillation ([LIT-tmp20sa6](LIT-tmp20sa6.md)), it sums over
differently-timed transitions (this), and it reads flat while the weights are
still moving ([LIT-tmp82k5k](LIT-tmp82k5k.md)).

**It supplies an instrument the record's evaluation material lacks.**
[SOTA-198](../practices.d/SOTA-198.md) measures the gradient noise scale from the run in front of you;
[SOTA-194](../practices.d/SOTA-194.md) asks what a benchmark's composition is. Nothing in the record
says how to find out what a *training run* is doing while it runs, and the
answer "watch the loss" is the one this paper is about.

The cost is real and should be stated: POLCA needs checkpoints, Hessian-vector
products at each, and a per-example forward pass at every measurement
interval. At 9M parameters that is affordable and the paper says the model
size was chosen for exactly that reason.
