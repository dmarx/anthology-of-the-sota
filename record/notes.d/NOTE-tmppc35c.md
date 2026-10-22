---
status: Read
paper: LIT-tmpiq1yh
title: 'SchNet'
version: 1
date: '2026-10-22'
summary: >-
  Convolution filters generated from interatomic distances give a smooth,
  invariant energy whose gradient is an energy-conserving force field.
  Training on forces as well as energies is the largest effect in the paper.
  Read in full; the supplement was not read.
---

# NOTE-tmppc35c: SchNet

## Contribution

A convolution for points at arbitrary positions, its filter an MLP of the
interatomic distance, used to build an energy model that is invariant,
smooth and differentiable, so forces come from the same model. A new
benchmark, ISO17, mixes chemical and conformational variation.

## Key insight

**If the energy model is smooth and invariant, the forces are free and
correct by construction.** Differentiate it and you get equivariant,
curl-free forces, and the force labels the reference calculation produced
anyway become training signal. One-hot bond types break this, because a
discrete input makes the energy surface jump.

## Key results

- QM9 U0: 0.31 kcal/mol at 110k, against enn-s2s 0.45 and its five-model
  ensemble 0.33
- MD17 at 1,000 configurations: energy-and-force training gives force MAE
  0.31–1.35 kcal/mol/Å, against 6.56–25.36 for energies alone. GDML is lower
  on forces for six of eight molecules
- With forces, 1,000 configurations give lower force error than 50,000
  energy-only ones on every molecule
- ISO17 unseen molecules: energy 2.40, forces 2.18 with force training;
  3.11 and 5.71 without

## Limitations

- **Label count is not controlled.** A configuration with forces carries
  3N + 1 labels. The paper does not ask whether energy labels in matching
  number would do as well, which in practice they cannot, since they come
  one per calculation
- **Invariant only.** Distances alone lose angular information within a
  neighborhood, which later equivariant and higher-body-order models
  ([LIT-tmpm07pb](../literature.d/LIT-tmpm07pb.md), [LIT-tmpj25em](../literature.d/LIT-tmpj25em.md)) set out to recover
- **The architecture was fixed on two MD17 molecules** (benzene and ethanol)
  and reused everywhere. The radial basis and cutoff are not studied
