---
status: Active
title: 'Stabilizing Transformer Training by Preventing Attention Entropy Collapse'
version: 1
tags:
- model-stability
- attention-techniques
- training-optimization
date: '2026-09-22'
published: '2023-03-11'
arxiv: '2303.06296'
first_author: 'Zhai'
keywords:
- 'attention entropy'
- 'entropy collapse'
- 'spectral normalization'
- 'training stability'
- 'reparameterization'
implementations:
- ml-sigma-reparam
summary: >-
  Zhai et al. (2023), [ARXIV-2303.06296](https://arxiv.org/abs/2303.06296) — proves a tight lower
  bound on attention entropy that falls like `Ω(Tσe^{-σ})` in the spectral
  norm of `W_K W_Q^T`, then removes the growth by reparameterizing every
  linear layer as `γ·W/σ(W)`. A ViT trained this way reaches 82.2% on
  ImageNet **without pre-LN, warmup, weight decay or an adaptive optimizer**.
  Read as [NOTE-tmp4pghv](../notes.d/NOTE-tmp4pghv.md).
---

# LIT-tmpzz9pi: Stabilizing Transformer Training by Preventing Attention Entropy Collapse

Zhai, Likhomanenko, Littwin, Busbridge, Ramapuram, Zhang, Gu and Susskind
(2023) — [ARXIV-2303.06296](https://arxiv.org/abs/2303.06296). Read as
[NOTE-tmp4pghv](../notes.d/NOTE-tmp4pghv.md).

## Key takeaways

- **A theorem where the record had an observation.** Attention entropy is
  bounded below by a quantity behaving like `Ω(Tσe^{−σ})` for `σ =
  ‖W_K W_Q^T‖₂·‖XX^T‖₂`, and the bound is attained for some inputs. Low
  entropy is not a coincidence of large weights; it is forced by them.
- **A reason the spectral norm grows.** Under an idealized Adam update the
  update's own spectral norm is bounded below by something scaling like `√w`
  in the matrix width. Adaptive optimizers push spectral norms up faster the
  wider the matrix.
- **σReparam.** Replace every linear layer's `W` with `γ·W/σ(W)`, `γ` learnable
  and initialized to 1, `σ` from power iteration on the parameters — two
  matrix-vector products, no activation cost, and foldable at inference.
- **The crutches come out.** ViT-B: DeiT baseline 81.8%, σReparam **82.2%**,
  with no pre-LN, no LR warmup, no weight decay and LARS instead of Adam.
- **The learned scalar is what does it.** Spectral normalization alone scores
  **69.81%** and WeightNorm 77.51% on the same setup. The `γ` is not a detail.
- **Five modalities.** Image classification, image self-supervised learning,
  machine translation (post-LN at 6/18/50/100 layers, 3 seeds), speech
  recognition and language modelling.

## Standing in the anthology

**It is the third remedy for a failure this record already documents, and the
only one that proves the bound.** [SOTA-192](../practices.d/SOTA-192.md) normalizes queries and
keys; [SOTA-131](../practices.d/SOTA-131.md) clips the weights when logits exceed a threshold. Both
act on the same invariant and both rest on the observation that unbounded
logits saturate the softmax. This supplies the inequality behind it and a
third instrument that acts on every linear layer rather than on attention
alone.

**Its account is disputed by a later paper this record also holds.**
[LIT-tmp8a9ww](LIT-tmp8a9ww.md) gives a counterexample: attention maps that
are sparse but not low-rank have near-zero entropy and train perfectly well.
That is one group contradicting another and is recorded as such.

**Read for what it removes, not for what it adds.** Accuracy moves by fractions
of a point. What moves is the hyperparameter surface — three of the papers in
this cluster independently report training without warmup, by three unrelated
spectral mechanisms.
