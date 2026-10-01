---
status: Active
title: 'Erwin: A Tree-based Hierarchical Transformer for Large-scale Physical Systems'
version: 1
tags:
- attention-techniques
- model-architecture
date: '2026-10-01'
published: '2025-02-24'
arxiv: '2502.17019'
first_author: 'Zhdanov'
# The cross-ball connection is Swin's shifted window carried to point
# clouds, rotating the cloud instead of sliding the windows; the paper names
# the model after it.
extends:
- LIT-723
keywords:
- 'hierarchical-transformer'
- 'ball-tree'
- 'ball-attention'
- 'point-clouds'
- 'linear-time-attention'
- 'physical-systems'
- 'cosmology'
- 'molecular-dynamics'
- 'pde-surrogates'
- 'fluid-dynamics'
implementations:
- 'maxxxzdn/erwin'
summary: >-
  Zhdanov et al. (2025), ARXIV-2502.17019 — Erwin. Build a ball tree over an
  irregular point set so that every ball at a level holds the same number of
  points in contiguous memory, then run full self-attention inside each ball,
  coarsen and refine through the tree in a U-Net, and alternate with a tree
  built on a rotated copy of the cloud so balls exchange information. Runtime
  fits n^1.054. Best on cosmology at large training sets, on EAGLE
  turbulence (3× faster and 8× less memory than EAGLE's own model), and on
  ShapeNet-Car; a clear failure on the Airfoil PDE mesh.
---

# LIT-tmpv26b7: Erwin: A Tree-based Hierarchical Transformer for Large-scale Physical Systems

Zhdanov, Welling and van de Meent, University of Amsterdam (2025) — ARXIV-2502.17019

## Key takeaways

- **The mechanism.** A ball tree recursively splits the point set at the
  median of its widest dimension, and is padded with virtual nodes to a
  perfect binary tree. Two properties make it a GPU structure rather than a
  CPU one: every ball at a level holds exactly 2^k leaves, and a permutation
  exists under which each ball's points are contiguous, so selecting a level
  is a reshape. Attention is computed independently within each ball (size
  m), costing O(n·m) instead of O(n²). Position enters twice, as a relative
  offset from the ball's centre of mass added to features and as a learned
  distance-decaying attention bias.
- **Cross-ball interaction by rotation.** Because the tree splits along
  coordinate axes it is not rotation-invariant, and the paper uses this: it
  builds a second tree on a rotated copy of the cloud, which groups points
  differently, and alternates layers between the two trees. This is
  Swin's shifted window with rotation in place of the shift, which is where
  the name comes from.
- **Hierarchy.** Coarsening concatenates a ball's children with their
  relative positions and projects up in width; refinement reverses it; a
  U-Net with skip connections runs the encoder and decoder. A small MPNN
  embeds local geometry at the input.
- **Scaling.** A power law fitted for n ≥ 1024 gives runtime ∝ n^1.054
  (R² 0.999); building the tree is under 5% of total time. Gradient-based
  receptive-field probing shows a global receptive field where a 6-layer MPNN
  is limited to its hop count.
- **Cosmology (5,000 halos, predict velocities).** Equivariant graph models
  (NequIP, SEGNN) lead at small training sets and plateau as data grows; the
  point transformers keep improving and Erwin is best at the largest sets
  (Fig. 6, up to 8,192 training examples). Ball size ablation (Table 2):
  test loss 0.595 at 256 against 0.620 at 32, for 229.6 against 126.0 ms.
- **Molecular dynamics.** Accuracy is about the same for every model, which
  the authors attribute to the beads carrying no charge so only local
  interactions matter; Erwin's gain is runtime, 1.7–2.5× over the MPNN at
  matched loss.
- **PDE benchmarks (Table 4), the mixed result.** Best of the listed
  transformer surrogates on Elasticity (0.34) and Plasticity (0.10), as
  printed in the table, but 2.57 on Airfoil against 0.48 for Transolver++,
  the worst entry in that column, and not best on Pipe.
  The authors attribute it to the mesh's density falling steeply away from
  the centre, so balls of equal count span very different scales. Baselines
  are taken from Luo et al. rather than rerun.
- **ShapeNet-Car pressure (Table 5).** 15.85 (S) and 15.43 (M) MSE, against
  17.42 for the strongest PTv3 and 17.02 for GP-UPT. The best Erwin and PTv3
  configurations used no coarsening at all, so this task rewards the ball
  attention, not the hierarchy.
- **EAGLE turbulence (Table 6).** Best at both horizons on velocity and
  pressure (e.g. +50-step velocity RMSE 0.281 against EAGLE's 0.349), at
  11 ms and 0.2 GB per batch of eight.
- **What is ablated (Table 3).** Adding the MPNN embedding helps MD (0.738 →
  0.720) and not ShapeNet-Car; relative position embedding helps a little;
  the rotating tree is what matters on ShapeNet-Car, 30.02 → 15.85. Without
  cross-ball connection the model is nearly twice as bad there.

## Standing in the anthology

The direct ancestor in the record is Swin (LIT-723). Erwin takes Swin's
answer to windowed attention's isolation, a second partition offset from the
first and alternated with it layer by layer, and transplants it from image
grids to point sets, where a shift is not defined and a rotation of the
input is. The ablation is the evidence the transplant works: removing the
rotated tree roughly doubles ShapeNet-Car error. It is also the same
connectivity requirement SOTA-208 kept as its surviving lesson, that a local
window alone is not the design, met here with a second partition rather than
a strided head.

The cosmology sweep is a measurement SOTA-358 does not yet have outside
vision: graph models with built-in equivariance win at small data and are
overtaken by attention models without it as the training set grows. It is a
single benchmark and the crossover is read from a figure, so it informs
rather than supports. SOTA-349 applies to how far it can be trusted. The
paper credits attention with capturing long-range interactions that message
passing misses; the cosmology baselines come from the benchmark's repository,
and the paper states hyperparameter tuning for every model only for the MD
task, which is exactly the situation that practice warns about.

There is no topic for scientific or physical-system surrogates. The paper is
filed on its kind of claim, an attention architecture, and that is
appropriate for what it argues. But the record now holds a model whose whole
evaluation is cosmology, polymer dynamics, PDE solving and fluid flow, and
none of `vision-and-graphics`, `biomolecular-modeling` or `signal-structure`
says that. Under ADR-059 this is a finding about the vocabulary.

Unread — no NOTE.
