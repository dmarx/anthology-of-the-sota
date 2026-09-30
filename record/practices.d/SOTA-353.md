---
number: 353
status: Proposed
formerly:
- SOTA-tmpej1tr
promote_when: >-
  Calibration of a learned self-accuracy head measured by someone other than
  its builders, on data after the model's cutoff, showing that ranking
  samples or filtering outputs by it beats the unranked alternative. Or the
  same head design shown calibrated outside structure prediction.
title: 'Train a head that predicts the model''s own accuracy on each output, against the metric you care about, and use it to rank samples and filter predictions'
version: 1
tags:
- analysis-and-evaluation
- biomolecular-modeling
date: '2026-09-23'
source:
- LIT-583
- LIT-584
introduced_by:
- LIT-583
consensus: unassessed
consensus_note: >-
  pLDDT and pTM are how AlphaFold predictions are read in practice. That is
  adoption, which is not evidence (DP-005). The calibration figures are the
  builders' own. Independent assessments exist in the structural-biology
  literature and have not been assessed here.
implementations:
- AlphaFold
- AlphaFold 3
summary: >-
  Jumper et al. (2021), [LIT-583](../literature.d/LIT-583.md) — regress the per-residue lDDT the
  prediction will score (pLDDT) and the predicted TM-score. They track truth
  at r = 0.76 and 0.85 over 10,795 chains, and pLDDT filters the
  self-distillation set. Abramson et al. (2024), [LIT-584](../literature.d/LIT-584.md), keep the head
  under diffusion by rolling out a cheap sample during training. They rank
  seeds by it, and antibody-interface quality keeps rising up to 1,000
  seeds.
---

# SOTA-353: Train a head that predicts the model's own accuracy on each output, against the metric you care about, and use it to rank samples and filter predictions

## Source

Jumper et al. (2021), [LIT-583](../literature.d/LIT-583.md), and Abramson et al. (2024),
[LIT-584](../literature.d/LIT-584.md). Read as [NOTE-321](../notes.d/NOTE-321.md) and [NOTE-320](../notes.d/NOTE-320.md).

## The practice

- **Supervise a confidence head with the real metric.** Train it against the
  metric the prediction will actually be scored on (lDDT per residue,
  TM-score per chain), computed on the model's own prediction during
  training
- **For a sampler, train it on a sample.** AF3 runs a cheap, large-step
  rollout of the diffusion sampler during training so the head sees a
  complete structure
- **Use it to spend inference compute.** Draw several seeds or samples and
  keep the one the head rates best. Add hard penalties for constraint
  violations (chirality, clashes) that the head does not capture
- **Use it to curate training data** ([SOTA-354](SOTA-354.md))

## Conditions

- **Calibration is shown in aggregate** (r = 0.76 for pLDDT). A single
  confident prediction can still be wrong
- **The head inherits the model's blind spots.** AF3's hallucinated
  regions are low-confidence, but not recognizably disordered
<!-- inactive-ok-file: SOTA-354 — Proposed, filed alongside as a use of this practice -->
