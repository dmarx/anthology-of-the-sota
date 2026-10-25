---
status: Read
paper: LIT-tmpj25em
title: 'MACE'
version: 1
date: '2026-10-22'
summary: >-
  Many-body messages from tensor products of a pooled two-body basis, so two
  layers suffice and evaluation is fast. Its learning-curve experiment
  separates body order from equivariance and finds body order sets the
  slope. Main text read; appendix implementation details skimmed.
---

# NOTE-tmpbbjt7: MACE

## Contribution

An equivariant message-passing potential whose messages are (ν + 1)-body,
built ACE-style from products of a pooled basis on nodes rather than sums
over atom tuples, and a controlled study of what body order and equivariance
each contribute.

## Key insight

**Body order and receptive field were tangled.** Two-body message passing
reaches higher correlations only by stacking layers, which also widens the
receptive field and slows everything. Building four-body messages inside one
layer reaches the accuracy in two layers.

## Key results

- 3BPA at 1200 K, forces: 62.0 meV/Å (MACE L = 2) against 76.2 (NequIP),
  at 24.3 ms against 103.5 ms latency in the same code
- Aspirin learning curves: slope −0.33 / −0.51 / −0.64 for invariant ν = 1,
  2, 3; −0.64 / −0.63 / −0.64 for L = 0, 1, 2 at ν = 3; −0.33 / −0.44 /
  −0.45 for L = 0, 1, 2 at ν = 1
- rMD17 with 50 configurations: lower force error than NequIP on all ten
  molecules

## Limitations

- **The learning-curve study is one molecule**, about one decade of training
  size, no error bars on slopes
- **Small molecules only.** The authors name condensed phases and solids as
  future work; the two-layer result leans on 3BPA being about 9 Å across
- **Timings are from the authors' code** with re-implemented baselines
