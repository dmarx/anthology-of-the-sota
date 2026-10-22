---
status: Active
consensus: unassessed
consensus_note: >-
  The three interatomic potentials read in this pass, from three groups
  (LIT-tmpiq1yh, LIT-tmpm07pb, LIT-tmpj25em), all train on forces taken as
  the energy's gradient. That is adoption, not evidence. NequIP also names
  direct-force models whose forces are not gradients of an energy, so the
  conservative half is not universal. Where the field stands overall has not
  been assessed here.
title: 'Fit a machine-learned interatomic potential to forces as well as energies, taking forces as the negative gradient of the predicted energy'
version: 1
tags:
- physical-sciences
- training-optimization
date: '2026-10-22'
source:
- LIT-tmpiq1yh
- LIT-tmpm07pb
introduced_by:
- LIT-tmpiq1yh
implementations:
- 'schnetpack'
- 'mir-group/nequip'
- 'ACEsuit/mace'
summary: >-
  Schütt et al. (2017), [LIT-tmpiq1yh](../literature.d/LIT-tmpiq1yh.md) — on MD17 with 1,000 configurations,
  adding force labels cut SchNet's force MAE 17–46× (benzene 14.12 → 0.31
  kcal/mol/Å) and also lowered energy error, and beat energy-only training
  on 50,000 configurations on forces. Make the energy model smooth, take
  forces as −∂E/∂r so they conserve energy, and weight the force term
  heavily; NequIP ([LIT-tmpm07pb](../literature.d/LIT-tmpm07pb.md)) defaults to 1 : N_atoms².
---

# SOTA-tmpb43t6: Fit a machine-learned interatomic potential to forces as well as energies, taking forces as the negative gradient of the predicted energy

## Source

Schütt et al. (2017), [LIT-tmpiq1yh](../literature.d/LIT-tmpiq1yh.md). Read as [NOTE-tmppc35c](../notes.d/NOTE-tmppc35c.md). Batzner et al.
(2021), [LIT-tmpm07pb](../literature.d/LIT-tmpm07pb.md). Read as [NOTE-tmp6evsh](../notes.d/NOTE-tmp6evsh.md).

## The practice

The measurement is SchNet's ([LIT-tmpiq1yh](../literature.d/LIT-tmpiq1yh.md), Table 2). The same network,
trained on 1,000 MD17 configurations per molecule with energies alone, has
force errors of 6.56–25.36 kcal/mol/Å; trained on energies and forces, 0.31–
1.35. Energy error drops as well (aspirin 4.20 → 0.37 kcal/mol). With forces,
1,000 configurations give lower force error than 50,000 energy-only ones on
all eight molecules. On ISO17, force training also improves generalization
to molecules never seen in training (energy 3.11 → 2.40, forces 5.71 →
2.18).

The construction is older than SchNet, which credits the kernel method GDML
with energy-conserving forces as the gradient of an energy model, and
earlier neural-network potentials with the combined energy-and-force loss.
Neither is in the record; [LIT-tmpiq1yh](../literature.d/LIT-tmpiq1yh.md) is named as origin because it is the
earliest work here that states and measures the recommendation for a deep
message-passing potential.

NequIP ([LIT-tmpm07pb](../literature.d/LIT-tmpm07pb.md)) is the evidence for the weighting. On water trained
from 133 structures (Table IV), forces alone gave a liquid-water force RMSE
of 12.5 meV/Å; a force-to-energy weight of 100 : 1 gave 51.4 with an energy
RMSE of 1.6 meV/molecule, and 100,000 : 1 gave 12.2 and 1.7. On the three
ices the energy cost of the force-heavy weighting was larger (ice Ih at
2.13 kbar: 2.6 against 12.7). The paper settles on an energy-to-force weight
of 1 : N_atoms² as a default.

- **Predict a scalar energy and differentiate it.** Forces as −∂Ê/∂r are
  rotation-equivariant if the energy is invariant, and curl-free, so a
  simulation driven by them conserves energy. Both papers do this
- **Keep the energy surface smooth.** Smooth activations (shifted softplus,
  SiLU) and continuous inputs: SchNet notes that one-hot bond types make the
  surface discontinuous and the model untrainable on forces
- **Weight forces heavily.** A configuration has one energy and 3N force
  components. Tune the ratio if energies matter for the application: on
  liquid water the force-heavy weighting cut force error about fourfold, and
  on one ice it raised energy error about fivefold

## Conditions

- **It costs about twice the compute per step**, because predicting forces
  needs a full forward and backward pass through the energy model, which
  SchNet estimates at double the cost
- **It assumes the reference data has forces.** Ab-initio MD and most DFT
  datasets do; equilibrium property sets such as QM9 do not, and there the
  forces are zero by definition
- **What the 1,000-vs-50,000 comparison counts.** Configurations, not
  labels: each configuration with forces carries 3N + 1 labels from the same
  calculation. The practice is to use what the calculation already produced,
  not a claim that a force label beats an energy label
- **The small-data baseline still won on forces in places.** At 1,000
  configurations the kernel method GDML, also trained on forces, has lower
  force error than SchNet on six of eight molecules. Force training is what
  both share
