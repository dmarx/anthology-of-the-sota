---
status: Active
title: 'E(3)-Equivariant Graph Neural Networks for Data-Efficient and Accurate Interatomic Potentials'
version: 1
tags:
- physical-sciences
- graphs-and-networks
- model-architecture
date: '2026-10-22'
published: '2021-01-08'
arxiv: '2101.03164'
first_author: 'Batzner'
keywords:
- 'nequip'
- 'interatomic-potentials'
- 'e(3)-equivariance'
- 'tensor-field-networks'
- 'molecular-dynamics'
- 'data-efficiency'
- 'learning-curves'
implementations:
- 'mir-group/nequip'
compared_against:
- LIT-tmpiq1yh
- LIT-tmpj25em
summary: >-
  Batzner et al. (Nature Communications 2022), [ARXIV-2101.03164](https://arxiv.org/abs/2101.03164). NequIP: a
  message-passing interatomic potential whose features are O(3) tensors up
  to order l, combined by Clebsch–Gordan tensor products with spherical-
  harmonic filters, with forces as the gradient of the energy. On MD17 with
  1,000 configurations, aspirin force MAE 8.2 meV/Å against SchNet's 58.5.
  The same network with only l = 0 features scores 41.9 on revised MD17,
  and 12.9 at l = 1. The equivariant variants also show a steeper log-log
  learning curve than the invariant one, on water and aspirin, read from
  figures. "1000× fewer data" is a force-error comparison against an older,
  non-smooth DeepMD; on energies DeepMD stays ahead.
---
<!-- inactive-ok-file: THEORY-tmpghjc1 — Proposed, filed in the same contribution; named as the record's re-reading of this paper's learning-curve claim -->

# LIT-tmpm07pb: E(3)-Equivariant Graph Neural Networks for Data-Efficient and Accurate Interatomic Potentials

Batzner, Musaelian, Sun, Geiger, Mailoa, Kornbluth, Molinari, Smidt,
Kozinsky, Harvard, EPFL, Bosch and LBNL (Nature Communications 2022) —
[ARXIV-2101.03164](https://arxiv.org/abs/2101.03164)

## Key takeaways

- **The architecture**: atom features are direct sums of irreducible O(3)
  representations (l = 0…l_max, both parities). A convolution is a tensor
  product of the neighbor's feature with a filter `R(r_ij) Y^l(r̂_ij)`, where
  only the radial MLP on a Bessel basis is learned, inside a cutoff r_c.
  Energy is a sum of per-atom scalars; forces are its negative gradient.
  Turning off every path above 0 ⊗ 0 → 0 leaves a SchNet-style invariant
  network
- **MD17** (Table I, 1,000 configurations, energy meV, forces meV/Å):
  aspirin 5.7 / 8.2 for NequIP l = 3, against SchNet 16.0 / 58.5, DimeNet
  8.8 / 21.6, GemNet forces 9.4 and UNiTE forces 6.8. Best or tied on most
  molecules, not all
- **Revised MD17** (Table II) carries the rotation-order ablation: aspirin
  forces 41.9 at l = 0, 12.9 at l = 1, 8.7 at l = 2, 8.5 at l = 3. Most of the
  gain is the step from 0 to 1. The authors recommend revised MD17 for
  comparison, because original MD17 energies have a higher noise floor
- **Water and ice** (Table IV, RMSE): trained on 133 structures against
  DeepMD's 133,500, NequIP's force errors are lower on all four systems
  (liquid water 12.2–12.5 against 40.4 meV/Å). Its energy errors are higher
  on all four (liquid water 1.6–1.7 against 1.0 meV/molecule; ice 2.5–12.7
  against 0.7–0.8), and they depend strongly on the energy–force weighting
- **Weighting the loss** (Methods): energy to forces 1 : N_atoms² as a
  default; on water, forces alone give force RMSE 12.5 meV/Å, and a force
  weight of 100 against energy 1 gives 51.4
- **Dynamics**: Li diffusivity in LiPS from NequIP-driven MD, trained on
  2,500 frames, is 1.25 × 10⁻⁵ cm²/s against 1.37 × 10⁻⁵ from AIMD (9%).
  Trained on melt only, it reproduces the quenched Li4P2O7 glass's radial and
  angular distributions
- **Learning curves** (Figures 7, 8, 11): on water (10 to 1,000 structures)
  and aspirin (150 to 950), l ≥ 1 networks have a steeper log-log slope than
  l = 0, and raising l beyond 1 only shifts the curve. On aspirin, l = 0
  networks matched to l = 1 in weight count and in feature count keep the
  shallow slope. No slope is reported as a number

## Standing in the anthology

**Filed from the graph-coverage pass** (gap list from the record's own
review, 2026-10-22). It is `compared_against` SchNet ([LIT-tmpiq1yh](LIT-tmpiq1yh.md)): Table I
puts SchNet's published MD17 numbers beside its own, roughly 7× lower force
error on aspirin, and the l = 0 ablation is the paper's own SchNet-style
model. Its water and ice loss-weighting table is the
evidence behind the weighting advice in [SOTA-tmpb43t6](../practices.d/SOTA-tmpb43t6.md).

**The data-efficiency claim has two parts and they are not equally
strong.** "Up to three orders of magnitude fewer training data" rests on the
water and ice comparison, which wins on forces and loses on energies, against
a DeepMD version the authors note is not smooth. The learning-curve result is
the more interesting one. It is a figure over one to two decades of training
size, for two systems with no seed count given, and its control holds the
invariant model's size fixed but not its body order. MACE ([LIT-tmpj25em](LIT-tmpj25em.md))
re-ran the aspirin experiment with an invariant model of higher body order
and got the steep slope without equivariance. [THEORY-tmpghjc1](../theory.d/THEORY-tmpghjc1.md) states that
reading.

**Against the record's prior on priors.** [SOTA-358](../practices.d/SOTA-358.md) says a built-in prior
pays at small data and is overtaken at large data. NequIP's slope claim is
the opposite shape, a prior that steepens the curve rather than offsetting
it, inside 1,000 structures. Erwin ([LIT-763](LIT-763.md)) measured NequIP itself on
cosmology velocities and found it leading at small training sets and then
plateauing while attention models kept improving. Different targets and
data scales; the two do not contradict, and neither covers the other's
range.

Read — [NOTE-tmp6evsh](../notes.d/NOTE-tmp6evsh.md).
