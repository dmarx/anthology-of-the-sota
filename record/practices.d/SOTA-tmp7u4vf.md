---
status: Proposed
promote_when: >-
  Adoption by independent SAE evaluations of a downstream-loss measure that
  is not normalized by zero ablation, with a demonstration beyond the
  source's one example that fraction-of-loss-recovered ranks SAEs
  differently from, or less discriminatingly than, that measure.
title: 'Report a sparse autoencoder''s fidelity as downstream loss in compute-equivalent terms, not as fraction of loss recovered against zero ablation'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-tmpydijh
introduced_by:
- LIT-tmpydijh
consensus: unassessed
consensus_note: >-
  "Fraction of loss recovered" remains common in SAE papers and
  benchmarks. How widely the compute-equivalent framing has been taken up
  has not been assessed here.
implementations: []
summary: >-
  Gao et al. (2024), [LIT-tmpydijh](../literature.d/LIT-tmpydijh.md) — splice the SAE's reconstruction into the
  forward pass and report the resulting loss as the pretraining compute a
  model of that loss would need. Zero-ablating the residual stream is so
  destructive that "loss recovered" against it flatters any reconstruction.
  Their 16M-latent GPT-4 SAE scores 98.2% on it, and equals a GPT-4 trained
  on 10% of the compute.
---

# SOTA-tmp7u4vf: Report a sparse autoencoder's fidelity as downstream loss in compute-equivalent terms, not as fraction of loss recovered against zero ablation

## Source

Gao et al. (2024), [LIT-tmpydijh](../literature.d/LIT-tmpydijh.md), §4.1 and footnote 11. Read as
[NOTE-tmpr5ct1](../notes.d/NOTE-tmpr5ct1.md).

## The practice

- **Measure fidelity downstream.** Replace the activations with the SAE's
  reconstruction during the forward pass, and report the change in
  cross-entropy or the KL to the original output. MSE alone understates
  differences between SAEs that matter to the model
- **Do not normalize by zero ablation.** Zeroing the residual stream
  destroys the model, so almost any reconstruction "recovers" most of the
  gap. 98.2% sounds nearly lossless. It is not
- **Anchor it to something a reader can weigh.** The paper's anchor is the
  fraction of the subject model's pretraining compute that reaches the same
  loss (10% for its best GPT-4 SAE). A smaller model from the same family,
  or a mean-ablation baseline, serves the same purpose where no
  compute-loss curve is available

## Conditions

- **The compute-equivalent figure needs a scaling curve** for the subject
  model, which outside labs rarely have
- **Fidelity is not usefulness.** A faithful SAE can still fail to help on
  a task ([LIT-tmp57c8v](../literature.d/LIT-tmp57c8v.md))
