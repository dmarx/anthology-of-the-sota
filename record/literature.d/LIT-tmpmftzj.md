---
status: Active
title: 'Small Singular Values Matter: A Random Matrix Analysis of Transformer Models'
version: 1
tags:
- analysis-and-evaluation
- inference-optimization
date: '2026-09-22'
published: '2024-10-23'
arxiv: '2410.17770'
first_author: 'Staats'
keywords:
- 'random matrix theory'
- 'Marchenko-Pastur'
- 'singular value spectra'
- 'SVD-based pruning'
- 'weight matrices'
implementations: []
summary: >-
  Staats, Thamm and Rosenow (2024), [ARXIV-2410.17770](https://arxiv.org/abs/2410.17770) — the
  singular spectrum of a trained transformer weight matrix is a
  Marchenko-Pastur bulk plus outliers, and in **non-square** matrices the
  outliers appear at *both* ends. Removing the smallest decile of the
  Down-Projection drops Llama-3 8B on GSM8K from 43.2% to **2.0%**, while the
  smallest decile of the square Attention-Output matrix costs almost nothing.
  Magnitude order is not importance order. Read as [NOTE-tmpsv1p1](../notes.d/NOTE-tmpsv1p1.md).
---
<!-- inactive-ok-file: THEORY-059 — Proposed, and this paper is the evidence
     bearing on whether its spectral premise holds. Naming the account you are
     supplying a measurement for is not leaning on it. -->

# LIT-tmpmftzj: Small Singular Values Matter: A Random Matrix Analysis of Transformer Models

Staats, Thamm and Rosenow (2024) —
[ARXIV-2410.17770](https://arxiv.org/abs/2410.17770), NeurIPS 2025. Read as
[NOTE-tmpsv1p1](../notes.d/NOTE-tmpsv1p1.md).

## Key takeaways

- **A trained transformer weight matrix is an MP bulk plus outliers.** At
  initialization the singular values follow the Marchenko-Pastur law exactly;
  training pushes a few out of the bulk. Measured on BERT, Pythia-410M and
  Llama-3.1-8B.
- **Non-square matrices get outliers at the bottom too.** The MP law for a
  rectangular matrix has a lower edge strictly above zero, so singular values
  can fall *below* the bulk as well as rise above it. Square matrices cannot
  do this.
- **Those bottom outliers carry data directions.** Their singular vectors
  overlap the eigenvectors of the activation covariance far more than chance,
  at 3σ.
- **And removing them is expensive.** Llama-3 8B, GSM8K, 43.2% baseline:
  zeroing the smallest decile of the Down-Projection gives **2.0%**, worse
  than every decile but the largest. The square Attention-Output matrix gives
  40.0% for the same operation.
- **Fine-tuning is what makes them load-bearing.** Prune-then-fine-tune
  recovers; fine-tune-then-prune does not. This reconciles two published
  results that appeared to contradict each other.

## Standing in the anthology

**It is the measurement [THEORY-059](../theory.d/THEORY-059.md) asked for, and it answers more than
half of the question.** That account rests on weight spectra being steep and
quantization-error spectra being flat, with the steep half plotted only on
diffusion transformers. This plots it on three language models, and supplies
something better than a plot: Marchenko-Pastur is the distribution an
i.i.d. matrix produces, so RMT gives the theory's *flat* case a name and a
predicted shape as well — while still not measuring it.

**Its sharper contribution to this record is a warning about the residual.**
[SOTA-314](../practices.d/SOTA-314.md) peels the top singular directions into a high-precision
branch and quantizes what is left. What is left contains the bottom outliers,
and this paper says those are, in the MLP projections, among the most
load-bearing directions in the matrix. Nobody has checked what 4-bit
quantization does to them.
