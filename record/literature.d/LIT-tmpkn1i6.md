---
status: Active
title: 'Omnigrok: Grokking Beyond Algorithmic Data'
version: 1
tags:
- analysis-and-evaluation
- model-stability
- training-optimization
date: '2026-09-22'
published: '2022-10-03'
arxiv: '2210.01117'
first_author: 'Liu'
keywords:
- 'grokking'
- 'loss landscape'
- 'weight norm'
- 'initialization scale'
- 'representation learning'
implementations: []
summary: >-
  Liu, Michaud and Tegmark (2022), [ARXIV-2210.01117](https://arxiv.org/abs/2210.01117), ICLR 2023 — the paper
  that answers whether grokking is specific to algorithmic data. No: it is
  induced on MNIST, IMDb and QM9 by shrinking the training set and scaling the
  initialization, and eliminated on algorithmic data by constraining the weight
  norm. The proposed mechanism is the "LU" mismatch — reduced training loss is
  L-shaped in weight norm and test loss U-shaped, so above the critical norm
  the two disagree. Read as [NOTE-tmpi8cjd](../notes.d/NOTE-tmpi8cjd.md).
---

# LIT-tmpkn1i6: Omnigrok: Grokking Beyond Algorithmic Data

Liu, Michaud and Tegmark (2022) — [ARXIV-2210.01117](https://arxiv.org/abs/2210.01117), ICLR 2023. Read as
[NOTE-tmpi8cjd](../notes.d/NOTE-tmpi8cjd.md).

## Key takeaways

- **Grokking is not confined to algorithmic data.** Induced on MNIST
  (depth-3 width-200 MLP, AdamW, MSE on one-hot targets), on IMDb with an
  LSTM, and on QM9 with a GCNN. The signal is weaker than on algorithmic data
  in every case.
- **It takes two deliberate changes, and the paper says so.** For MNIST: cut
  the training set from 60k to 1k, *and* multiply the Kaiming-uniform initial
  weights by `α > 1`. At `α = 1` there is no grokking. For IMDb, `α = 6`
  groks weakly and `α = 1` does not; for QM9, `α = 3`.
- **And it can be removed.** Constraining the model to a small-weight-norm
  sphere nearly eliminates grokking on algorithmic datasets.
- **The LU mechanism.** Minimizing over angular directions at fixed norm,
  reduced *training* loss falls and then stays near zero — an "L" — while
  reduced *test* loss has a minimum at a critical norm `w_c` and rises on
  both sides — a "U". Starting above `w_c` fits fast and generalizes only as
  regularization walks the norm back down. With weight decay `γ`, the
  training landscape becomes `l̃_train(α) + γα²C²`.
- **The quantitative signature.** In the teacher–student model at `α = 2.0`,
  time to 95% *training* accuracy is independent of `γ`, while time to 95%
  *test* accuracy is inversely proportional to `γ`. Small initializations
  (`α = 0.5`) generalize fast regardless.
- **Larger data de-groks** by broadening the Goldilocks zone, and there is a
  critical training-set size below which generalization does not happen at
  all — reproducing Power et al.'s rapid rise in time-to-generalize on MNIST.
- **Why algorithmic data is dramatic:** representation quality there decides
  between chance and 100%; on MNIST it decides between 95% and 100%.

## Standing in the anthology

**`Active`, and it is the paper that settles the scope question `SOTA-200`
was implicitly answering.** The record said grokking is "a data-starved-regime
phenomenon, not a fundamental one", on one paper's data-fraction result for
modular addition. This one shows the regime has at least a second axis —
where you start relative to the generalizing weight norm — and that setting
both produces grokking on ordinary supervised tasks.

**The LU mechanism itself is contested**, by [ARXIV-2310.06110](https://arxiv.org/abs/2310.06110)'s counterexample
in which the weight norm *rises* through grokking with no weight decay at all.
That contest is over the mechanism, not over the induce-and-eliminate
experiments, which nothing disputes.
