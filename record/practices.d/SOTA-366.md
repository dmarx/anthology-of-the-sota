---
number: 366
status: Active
formerly:
- SOTA-tmp3wrpo
consensus: unassessed
consensus_note: >-
  Not judged, and that is the honest answer rather than a gap. The
  derivation is arithmetic and the check is three lines, and it appears in
  SimSiam's own figures — but whether practitioners run it has not been
  measured here, and the `#304` reading so far gives no grounds either way.
  A value invented to fill this column would be worse than the admission
  (`luria.yaml`, `consensus`).
title: 'Monitor the standard deviation of the l2-normalized embedding; healthy is one over root d and collapsed is zero'
version: 1
tags:
- analysis-and-evaluation
- model-stability
date: '2026-09-23'
source:
- LIT-593
introduced_by:
- LIT-593
implementations: []
---

# SOTA-366: Monitor the standard deviation of the l2-normalized embedding; healthy is one over root d and collapsed is zero

## Source

Chen & He (2020), [LIT-593](../literature.d/LIT-593.md) — [ARXIV-2011.10566](https://arxiv.org/abs/2011.10566), §4.1.

## The claim

While training any joint-embedding model, log the **per-channel standard
deviation, across samples, of the ℓ2-normalised output** `z / ‖z‖₂`. It has
two reference values you can compare against without a baseline run:

- **0** — the outputs have collapsed to a constant vector. Every channel's
  standard deviation over the dataset is zero by definition.
- **1/√d** — the outputs are scattered over the unit hypersphere. If `z` were
  zero-mean isotropic Gaussian then `z_i/‖z‖₂ ≈ z_i/√d`, so each normalised
  channel has standard deviation about `1/√d`.

SimSiam's runs sit at `1/√d` with the stop-gradient and drop to `0` without
it. A number that is neither is a partial collapse, and its distance from
`1/√d` is roughly how much of the sphere is being used.

## Why this rather than the loss

**Because the loss endorses the failure.** Without the stop-gradient,
SimSiam's optimiser "quickly finds a degenerated solution and reaches the
minimum possible loss of −1" — the best value the objective can take. A
training curve heading confidently to its floor is what collapse looks like,
and is indistinguishable from success if the loss is all you plot.

This is the second time in the `#304` reading that a contrastive failure has
been *rewarded* by the obvious metric — [SOTA-364](SOTA-364.md) is the first, where the
batch-norm leak makes the loss fall faster. In both cases the diagnosis came
from measuring something the objective does not optimise.

## What it is good for beyond the alarm

- **It has an absolute scale.** No baseline run, no reference checkpoint;
  `1/√d` is computable from the embedding width alone, so a single run can be
  judged on its own.
- **It separates two failures the loss conflates**: a collapse to a point
  (standard deviation → 0) from a collapse to a low-dimensional subspace
  (standard deviation near `1/√d` on some channels and near 0 on others).
  The per-channel breakdown is what distinguishes them.
- **SimSiam pairs it with a kNN probe on real labels**, which is the other
  half: the standard deviation says the embedding is spread out, the kNN
  monitor says the spread means something. Cheap enough to run every epoch,
  and neither substitutes for the other.

## Conditions

- **`1/√d` assumes the ℓ2 normalisation and an isotropic reference.** An
  embedding deliberately shaped otherwise — a learned temperature, a
  non-spherical prior — needs its own reference value derived the same way,
  not this one.
- **It is a necessary condition, not a sufficient one.** A well-spread
  embedding can still be useless; that is what the kNN probe is for.
- **Measured on one method in one paper.** The derivation is general and the
  arithmetic is checkable, which is why this is `Active` despite a single
  source, but the empirical grounding is narrow.

## Known implementations

-
