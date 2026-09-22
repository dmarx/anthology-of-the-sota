---
status: Active
title: 'The Stability of Singular Distribution: A Spectral Perspective on the Two-Phase Dynamics of Language Model Pre-training'
version: 1
tags:
- training-optimization
- analysis-and-evaluation
- model-stability
date: '2026-09-22'
published: '2026-05-26'
arxiv: '2605.26489'
first_author: 'Zhang'
keywords:
- 'singular distribution'
- 'pre-training dynamics'
- 'two-phase loss'
- 'spectral stability'
- 'Muon'
implementations: []
summary: >-
  Zhang, Zhou, Jia, Chen and Cheng (2026), [ARXIV-2605.26489](https://arxiv.org/abs/2605.26489) —
  the trace-normalized singular spectrum stops moving long before the weight
  matrices do. Variation peaks near `10⁻²` in the first ~1000 steps, while
  validation loss falls from ~10 to ~4.0, then settles at a `10⁻⁴` floor
  that coincides with the slow-descent phase. Holds on GPT-2 and LLaMA,
  across schedules, weight decays, AdamW and Muon. Read as
  [NOTE-tmpg1l16](../notes.d/NOTE-tmpg1l16.md).
---

# LIT-tmpxqt7b: The Stability of Singular Distribution: A Spectral Perspective on the Two-Phase Dynamics of Language Model Pre-training

Zhang, Zhou, Jia, Chen and Cheng (2026) —
[ARXIV-2605.26489](https://arxiv.org/abs/2605.26489), ICML 2026. Read as
[NOTE-tmpg1l16](../notes.d/NOTE-tmpg1l16.md).

## Key takeaways

- **The shape settles before the matrix does.** Cosine similarity between the
  current and final singular-value matrix saturates well ahead of the same
  measure on the weight matrices themselves. The authors name this the
  Stability of Singular Distribution.
- **It lines up with the loss curve's elbow.** Spectral variation `ΔΣ` peaks
  near `10⁻²` while validation loss drops from ~10 to ~4.0, then falls to a
  metastable `10⁻⁴` floor exactly as the loss enters its long slow phase.
- **MLP layers move less than attention layers**, and both enter the stable
  regime together.
- **It survives changing the recipe.** GPT-2 Small and Medium, LLaMA 0.5B and
  2B; step-wise, WSD and cosine schedules; varied weight decay; AdamW and
  Muon.
- **The interpretation offered is a bound**, `ε ∝ η/‖W‖`: schedules tighten
  it, weight decay relaxes it by suppressing norm growth.

## Standing in the anthology

**It is why a spectrum-based decision can be made once.** Every practice in
this cluster — [SOTA-tmpsbgvf](../practices.d/SOTA-tmpsbgvf.md)'s per-matrix rank,
[SOTA-314](../practices.d/SOTA-314.md)'s low-rank branch — reads a spectral shape and acts on
it. This says the shape is established early and then holds, across four
models, three schedules and two optimizers, which is what makes a one-shot
reading of it meaningful rather than a snapshot of a moving target.

**Read for that one purpose.** The record took the empirical section; the
theory in section 4, which derives the stability bound, was not worked
through, and nothing here leans on it.
