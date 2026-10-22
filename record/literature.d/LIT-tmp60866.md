---
status: Active
title: 'E(n) Equivariant Graph Neural Networks'
version: 1
tags:
- graphs-and-networks
- model-architecture
- physical-sciences
date: '2026-10-22'
published: '2021-02-19'
arxiv: '2102.09844'
first_author: 'Satorras'
keywords:
- 'egnn'
- 'e(n)-equivariance'
- 'equivariant-message-passing'
- 'n-body'
- 'graph-autoencoder'
- 'qm9'
implementations: []
compared_against:
- LIT-tmpiq1yh
summary: >-
  Satorras, Hoogeboom, Welling (ICML 2021), [ARXIV-2102.09844](https://arxiv.org/abs/2102.09844). A message-passing
  layer that also carries a coordinate per node: messages see only squared
  distances, and coordinates move along a weighted sum of relative position
  vectors, which is E(n)-equivariant in any dimension without spherical
  harmonics. On a 3D charged 5-body system it cuts position MSE 32% against
  the next model (0.0071 vs 0.0104). On QM9 it does not update coordinates,
  which makes it an invariant distance GNN, and it is competitive rather than
  best.
---

# LIT-tmp60866: E(n) Equivariant Graph Neural Networks

Satorras, Hoogeboom, Welling, University of Amsterdam (ICML 2021) —
[ARXIV-2102.09844](https://arxiv.org/abs/2102.09844)

## Key takeaways

- **The layer** (Eqs. 3–6): `m_ij = φ_e(h_i, h_j, ‖x_i − x_j‖², a_ij)`,
  `x_i ← x_i + C Σ_j (x_i − x_j) φ_x(m_ij)`, `h_i ← φ_h(h_i, Σ_j m_ij)`.
  Features stay invariant, coordinates transform as vectors, and nothing
  depends on the dimension n. A velocity variant (Eq. 7) and a soft
  edge-inference gate (Eq. 8) are optional
- **N-body** (Table 2; 5 charged particles in 3D, 3,000 training
  trajectories, predict positions 1,000 steps ahead): EGNN MSE 0.0071, Radial
  Field 0.0104, GNN 0.0107, TFN 0.0155, SE(3)-Transformer 0.0244, linear
  0.0819. Forward time 0.0062 s per batch of 100, against 0.0343 for TFN and
  0.1346 for the SE(3)-Transformer
- **Data sweep** (Figure 2, 100 to 50,000 trajectories): EGNN is best at
  every size. Radial Field, which is equivariant but passes no features, does
  well with little data and stops improving; the plain GNN catches up only
  at large data. Values are read from a figure only
- **Graph autoencoder** (Figure 5): featureless graphs are embedded by
  feeding Gaussian noise as coordinates, which breaks the symmetry between
  identical neighborhoods. Edge error 0.11% on Erdős–Rényi graphs and 0.06%
  on Community Small, against 1.25% and 0.44% for a GNN given the same noise
  as features
- **QM9** (Table 3, MAE over 12 targets): EGNN beats SchNet on 11 of 12
  (U0 11 vs 14 meV, α 0.071 vs 0.235 bohr³) and is behind DimeNet++ on 10 of 12
  (U0 6 meV), whose splits differ slightly. Here EGNN does not update
  coordinates, so it is an invariant model over all pairwise distances
- **Why distances suffice** (Appendix E): the full set of pairwise distances
  determines a point cloud up to an E(n) transformation, so for scalar
  targets on positions alone no higher-order features are needed

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It is `compared_against` SchNet ([LIT-tmpiq1yh](LIT-tmpiq1yh.md)), whose
QM9 numbers it reports beside its own: EGNN is ahead on 11 of the 12
targets, and SchNet only on R² (0.073 against 0.106). Both models are
invariant on that task, so the gain is from the architecture around the
distances, not from equivariance.

**The proof in Appendix E needs every pair.** It holds for a complete graph,
which is what EGNN uses on QM9 (up to 29 atoms). Interatomic potentials such
as NequIP ([LIT-tmpm07pb](LIT-tmpm07pb.md)) and MACE ([LIT-tmpj25em](LIT-tmpj25em.md)) use a local cutoff, where
distances within each neighborhood do not determine the geometry, and that
is the setting their angular and equivariant features are argued for.

**Where equivariance is actually tested.** Only the N-body task predicts a
vector output, and there the comparison is fair in that every model has four
layers and its own tuned learning rate. The data sweep is the paper's
evidence for data efficiency and it is a figure on one synthetic system. It
reads in the same direction as [SOTA-358](../practices.d/SOTA-358.md), where a built-in prior pays most at
small data, but the plain GNN never overtakes EGNN within 50,000
trajectories, so the crossover that practice describes is not reached here.

Read — [NOTE-tmp58sq2](../notes.d/NOTE-tmp58sq2.md).
