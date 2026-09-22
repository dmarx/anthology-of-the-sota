---
status: Active
title: 'Do pretrained Transformers Learn In-Context by Gradient Descent?'
version: 1
tags:
- in-context-learning
- analysis-and-evaluation
- adaptation-and-tuning
date: '2026-09-22'
published: '2023-10-12'
arxiv: '2310.08540'
first_author: 'Shen'
keywords:
- 'in-context learning'
- 'gradient descent'
- 'order sensitivity'
- 'pretraining objective'
- 'LLaMA'
implementations: []
summary: >-
  Shen, Mishra and Khashabi (2023), [ARXIV-2310.08540](https://arxiv.org/abs/2310.08540), ICML 2024 — the
  challenge from outside. It separates two hypotheses the field had been
  conflating: that ICL in a naturally pretrained model *is* gradient descent,
  and that transformer weights *exist* that simulate it. Theorem 1 says an
  algorithm equivalent to ICL must share its order sensitivity, and gradient
  descent is order-stable while ICL is not; on LLaMA-7B, ICL and fine-tuning
  disagree on accuracy, top-10 token overlap and overlap cosine similarity
  across four datasets. Read as [NOTE-tmp4ho8v](../notes.d/NOTE-tmp4ho8v.md).
---

# LIT-tmpvwpn4: Do pretrained Transformers Learn In-Context by Gradient Descent?

Shen, Mishra and Khashabi (2023) — [ARXIV-2310.08540](https://arxiv.org/abs/2310.08540), ICML 2024. Read as
[NOTE-tmp4ho8v](../notes.d/NOTE-tmp4ho8v.md).

## Key takeaways

- **Two hypotheses, and only the weaker one was ever tested.** *Hypothesis 1*:
  for any weights arising from self-supervised pretraining and any well-defined
  task, ICL is algorithmically equivalent to gradient descent. *Hypothesis 2*:
  for a given task, there **exist** transformer weights for which a simulated
  ICL is equivalent to gradient descent. Hypothesis 2 is a statement about
  architectural expressivity and is what the constructions establish.
- **Theorem 1 is a one-line contradiction.** If `A` is equivalent to ICL then
  `M_Θ0(σ_A ∘ x_t) − M_Θ0(σ_B ∘ x_t) = M_{Θ_σA}(x_t) − M_{Θ_σB}(x_t)` for any
  two orderings of the demonstrations. Gradient descent averages over a batch,
  so its right-hand side is zero; ICL's left-hand side is not. Measured on
  LLaMA-7B/AGNews over 10 orderings of 8 demonstrations, ICL's output-
  distribution spread exceeds GD's, SGD's and Adam's throughout training.
- **The hand-constructed weights do not look like real ones.** Reproducing
  [ARXIV-2212.07677](https://arxiv.org/abs/2212.07677)'s construction at LLaMA's `N_x = N_y = 4096` requires
  sparsity above 99.99% in `W_K` and `W_Q` and about 75% in `W_V`; measured
  sparsity in LLaMA at every threshold from 10⁻² to 10⁻⁶ is far lower. `P =
  (η/N)I` also diverges at `N = 0`.
- **ICL is a property of a family of weights, not a point.** Across GPT-J
  checkpoints, ICL accuracy on AGNews is flat while parameters keep moving.
  Equivalence shown for one choice of parameters is not equivalence.
- **The empirical comparison covers three metrics and finds a gap on all
  three.** LLaMA-7B on AGNews, CB, SST-2 and RTE, `N ∈ {1, 2, 4, 8}`, four
  learning rates, 200 epochs, against whole-model GD and against sub-model GD
  on `W_V` of a middle and a deep layer. ICL agrees with *itself under a
  different demonstration order* more than with any GD variant.

## Standing in the anthology

**`Active`, and it is the paper that makes this cluster filable as a
dispute rather than a finding.** Its Hypothesis-1/Hypothesis-2 distinction is
reusable well beyond in-context learning: a proof that an architecture *can*
compute something, plus a model trained on the task to show it *does*, is
weaker evidence about pretrained models than it reads as.

The authors state the conclusion as "the equivalence remains an open
hypothesis", not as a refutation, and the record follows them on that.
