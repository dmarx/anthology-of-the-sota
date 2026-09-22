---
status: Active
title: 'Transformers Learn Low Sensitivity Functions: Investigations and Implications'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
- model-stability
date: '2026-09-22'
published: '2024-03-11'
arxiv: '2403.06925'
first_author: 'Vasudeva'
keywords:
- 'inductive bias'
- 'sensitivity'
- 'simplicity bias'
- 'robustness'
- 'grokking'
implementations: []
summary: >-
  Vasudeva et al. (2024), [ARXIV-2403.06925](https://arxiv.org/abs/2403.06925) — sensitivity to
  token-wise random input perturbations is one number that separates
  transformers from MLPs, CNNs, ConvMixers and LSTMs across vision and
  language. It also predicts robustness, tracks flatness, can be regularized
  for, and keeps falling through a grokking plateau while the loss does not
  move. Read as [NOTE-tmpwuv3u](../notes.d/NOTE-tmpwuv3u.md).
---
<!-- inactive-ok-file: THEORY-041 — Proposed, named as one of the accounts
     circling what distinguishes transformer training, in a sentence saying
     the record cannot currently answer that. -->

# LIT-tmpc05l0: Transformers Learn Low Sensitivity Functions: Investigations and Implications

Vasudeva, Fu, Zhou, Kau, Huang and Sharan (2024) —
[ARXIV-2403.06925](https://arxiv.org/abs/2403.06925), ICLR 2025. Read as
[NOTE-tmpwuv3u](../notes.d/NOTE-tmpwuv3u.md).

## Key takeaways

- **One metric, and it separates architectures.** Sensitivity — how likely the
  output is to change under random token-wise perturbation of the input —
  is lower for transformers than for MLPs, CNNs, ConvMixers and LSTMs,
  across both vision and language, at matched training accuracy.
- **It has a pedigree.** On Boolean inputs, sensitivity relates to the degree
  of the representing multilinear polynomial and to decision-tree size, so low
  sensitivity is a form of simplicity bias. The paper proves the low-sensitivity
  bias of transformers in the NTK regime via spectral bias, and proves low
  sensitivity implies better robustness.
- **It is actionable.** Regularizing for low sensitivity improves robustness
  further, on CIFAR-10-C.
- **It tracks flatness**, connecting an inductive-bias statement to the
  loss-landscape literature.
- **It moves during a grokking plateau.** On modular addition, sensitivity
  falls while the training loss does not, which makes it a progress measure.

## Standing in the anthology

**It answers a question the record poses and cannot currently answer.**
[THEORY-041](../theory.d/THEORY-041.md), [SOTA-012](../practices.d/SOTA-012.md) and
[THEORY-035](../theory.d/THEORY-035.md) all circle what distinguishes transformer training
from everything else, in terms of conditioning and sharpness. This offers a
single scalar that is architecture-comparable, cheap, and defined on the
function rather than on the weights.

**Its grokking result belongs beside [SOTA-200](../practices.d/SOTA-200.md).** That practice
says to check whether an emergent capability is a metric artefact, and cites
the reverse-engineering of one network to recover the continuous progress
under its discontinuity. Sensitivity is a candidate progress measure that
needs no reverse engineering and is defined for any architecture. The record
does not fold it into the practice, because it is demonstrated on one
synthetic task.

**Filed for the metric, not the ranking.** "Transformers beat CNNs on
robustness" is a comparison the record has no use for. That a single computable
quantity predicts robustness, tracks flatness and moves during a plateau is
the reason this is here.
