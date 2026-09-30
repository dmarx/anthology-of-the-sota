---
number: 343
status: Proposed
formerly:
- SOTA-tmpeyp35
promote_when: >-
  An independent comparison, not from the tuned lens's authors, on current
  open models, showing that tuned-lens readings of intermediate layers
  agree with the model's own later behavior better than logit-lens readings
  do, with the lenses trained to convergence. The source's own lenses are,
  by its later account, undertrained.
title: 'Read a transformer''s intermediate-layer predictions through a tuned lens, not the raw logit lens'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-569
introduced_by:
- LIT-569
consensus: unreplicated
consensus_note: >-
  The logit lens is still widely used as-is. The tuned lens's advantage is
  measured across several model families, but by its authors. Whether the
  field has moved to it has not been assessed here.
implementations:
- tuned-lens
summary: >-
  Belrose et al. (2023), [LIT-569](../literature.d/LIT-569.md) — decoding a hidden state with the
  final unembedding (the logit lens, [LIT-570](../literature.d/LIT-570.md)) fails outright on BLOOM,
  OPT and GPT-Neo, and is biased by 4–5 bits where it works. Train one
  affine translator per layer by KL to the final logits, initialized to the
  identity, and read the layer through that. It is cheap (d×d per layer),
  transfers to fine-tunes, and its directions are the model's (Spearman
  0.89). Train it with Muon.
---

# SOTA-343: Read a transformer's intermediate-layer predictions through a tuned lens, not the raw logit lens

## Source

Belrose et al. (2023), [LIT-569](../literature.d/LIT-569.md). Read as [NOTE-308](../notes.d/NOTE-308.md). It refines the
logit lens, [LIT-570](../literature.d/LIT-570.md).

## The practice

When asking what a pre-LN transformer "predicts" at an intermediate layer:

- **Do not trust the logit lens on a model you have not checked it on.** On
  BLOOM and OPT-125M its top-1 at most layers is the input token. On GPT-Neo
  it is biased toward some tokens until the last layer. A clean-looking
  trajectory on GPT-2 says nothing about the next model
- **Train a translator per layer:** `h ↦ A_ℓ h + b_ℓ`, identity-initialized,
  minimizing KL from the model's own final distribution on held-out
  pretraining-like text, then apply the model's final norm and unembedding.
  Distilling toward the model, not toward labels, keeps the lens from
  learning what the model does not know
- **Optimize it properly.** The paper's later version says Muon reaches much
  lower KL than its SGD setup, and that its own lenses were undertrained
- **Reuse lenses across fine-tunes** of the same base model. The cost is at
  most 0.3 bits per byte in the paper's one test

## Conditions

- **Pre-LN transformers**
- **It is a reading tool, not a detector.** The paper's anomaly-detection
  use loses to a Mahalanobis baseline on most tasks, and for eliciting
  hidden knowledge it is not reliably better than the logit lens
