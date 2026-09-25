---
number: 413
status: Proposed
formerly:
- SOTA-tmp7rph1
consensus: emerging
consensus_note: >-
  Chinchilla counts total parameters, and Pearce and Song and Porian et al.
  (arXiv 2406.19146, not yet held) independently find that the counting
  choice moves the allocation exponent. A named list of studies still uses
  Kaplan's non-embedding count and offset-free fit. The two proponents
  disagree on whether the input embedding belongs in the count. Read as of
  2026-09.
promote_when: >-
  A scaling study fits the same runs under both counts, extrapolates each fit
  to a held-out larger run, and reports which predicts it. Or Porian et al. is
  filed and its stepwise attribution is read next to this one. A study that
  merely adopts total counts would not settle it, because it shows the
  convention and not which convention extrapolates.
title: 'In a scaling-law study, count the output head in parameters and FLOPs, and fit loss against compute with an irreducible-loss offset'
version: 1
tags:
- training-optimization
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-688
introduced_by:
- LIT-688
implementations: []
summary: >-
  Pearce and Song (TMLR 2024), [LIT-688](../literature.d/LIT-688.md). At small scale the embedding
  and output head are a large share of the model. Excluding them from N, and
  from the FLOPs in `C = 6ND`, biases the fitted allocation exponent: 0.49
  becomes 0.74 when the same runs are relabelled. An offset-free loss–compute
  fit biases that exponent too. Do not compare exponents across studies that
  count differently.
---

# SOTA-413: In a scaling-law study, count the output head in parameters and FLOPs, and fit loss against compute with an irreducible-loss offset

## Source

Pearce and Song (2024), [LIT-688](../literature.d/LIT-688.md), explaining the gap between
[LIT-028](../literature.d/LIT-028.md) and [LIT-068](../literature.d/LIT-068.md).

## What to do

- Define N so that `6ND` matches the FLOPs training actually spends. That
  includes the output head, and the input embedding too if you follow this
  source. Porian et al. count the head and exclude the input embedding.
  State which you did.
- Fit loss against compute as `L = (C/C₀)^{−γ} + E`, with the offset `E`, not
  as a pure power law.
- Do not set your exponent against another study's until both count N the
  same way.

## Why

The optimal non-embedding size against non-embedding compute "is not a power
law". Its local slope moves from `β/(α/3+β)` to `β/(α+β)` as embeddings stop
being a large fraction of the model. A study fit at small scale on the
non-embedding count reads off the small-scale slope and calls it the
exponent. Relabelling the same five runs changes the exponent from 0.49 to
0.74.

## Conditions

- **Matters most below a few hundred million parameters.** At frontier scale
  the head is a small share and the definitions converge.
- **The source's evidence is small.** It is five runs at 0.8–4.6M with context
  16, plus a simulation from Chinchilla's own fit. Porian et al. is the large
  test (not yet held). It agrees that counting matters and finds warmup and
  per-size tuning matter as much or more. This practice is the counting part
  only.
- **Counting is not the whole Kaplan–Chinchilla gap.** Do not read this as
  "Kaplan was wrong because of embeddings".

## Known implementations

- None recorded.
