---
status: Read
paper: LIT-tmpm07pb
title: 'NequIP'
version: 1
date: '2026-10-22'
summary: >-
  Tensor-valued equivariant features in a message-passing interatomic
  potential, with large accuracy gains over invariant models at 1,000
  configurations and a learning curve that looks steeper. The attribution of
  that slope to equivariance is the weak point. Main text, methods and
  appendices read.
---

# NOTE-tmp6evsh: NequIP

## Contribution

An E(3)-equivariant interatomic potential built from Tensor Field Network
convolutions, with energy-conserving forces, evaluated on molecules, water
and ice, a surface reaction and two lithium conductors, including MD runs
compared against ab-initio dynamics.

## Key insight

**Let the features keep direction.** An invariant model reduces each
neighbor to a distance at every layer; tensor features let angular structure
survive between layers. The l = 0 → 1 step is where almost all the gain is.

## Key results

- Revised MD17 aspirin forces: 41.9 (l = 0), 12.9 (l = 1), 8.5 (l = 3) meV/Å
- Original MD17 aspirin forces 8.2 against SchNet 58.5 and DimeNet 21.6
- Water and ice from 133 structures: force RMSE a quarter to a half of DeepMD's
  trained on 133,500; energy RMSE worse on every system
- LiPS Li diffusivity within 9% of AIMD from a model trained on 2,500
  frames
- Learning curves on water and aspirin: l ≥ 1 steeper than l = 0 in log-log,
  including against l = 0 networks matched in weights or features (aspirin)

## Limitations

- **The slope evidence is visual** — no fitted exponents, no error bars, one
  to two decades of data, two systems
- **The invariant control is two-body.** The l = 0 network matches the
  equivariant one in size but not in body order; MACE ([LIT-tmpj25em](../literature.d/LIT-tmpj25em.md)) shows
  that difference alone moves the slope
- **"1000× fewer data" is forces-only** and against a non-smooth DeepMD
- **Hyperparameters** (l, width, cutoff, loss weights) vary per system, and
  the paper calls the cutoff and small batch size important without
  ablating them
