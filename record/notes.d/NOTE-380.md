---
number: 380
status: Read
formerly:
- NOTE-tmp0yioe
paper: 'LIT-582'
title: 'GCN'
version: 1
date: '2026-10-22'
summary: >-
  A two-layer network that multiplies node features by the renormalized
  adjacency beats the 2016 semi-supervised baselines on three citation
  graphs and NELL. Its own random-split row is 2.4 points lower on
  Citeseer than the fixed-split headline. The spectral derivation
  motivates the layer and does not constrain it. Read in full, including
  both appendices.
---

# NOTE-380: GCN

## Contribution

A message-passing layer simple enough to become the default baseline:
`H' = σ(D̃^{-1/2} Ã D̃^{-1/2} H W)`, with self-loops added (`Ã = A + I`).
Each layer costs one sparse–dense product, linear in edges, and the whole
model trains full-batch.

## Key insight

**Average your neighbours, including yourself, then apply a shared linear
map.** The spectral story (§2) reaches this by truncating a Chebyshev
filter to first order, setting λ_max ≈ 2 and tying two parameters into
one. Each step is an approximation chosen for convenience, and the
"renormalization trick" is added because the tied operator has eigenvalues
in [0, 2] and would be unstable when stacked. Appendix A gives the second
reading, which is the one later work kept: the layer is a differentiable
1-WL refinement with a degree-normalized sum.

## Key results

- **Table 2, Planetoid split, mean of 100 initializations:** Citeseer
  70.3, Cora 81.5, Pubmed 79.0, NELL 66.0, against Planetoid's 64.7,
  75.7, 77.2 and 61.9
- **Table 2, last row, 10 random splits of the same size:** 67.9 ± 0.5,
  80.1 ± 0.5, 78.9 ± 0.7 and 58.4 ± 1.7. The fixed split is the
  favourable one, by 2.4 points on Citeseer and 7.6 on NELL
- **Table 3, propagation ablation:** renormalized 70.3 / 81.5 / 79.0;
  Chebyshev K = 2, 69.6 / 81.2 / 73.8; first-order with two parameters,
  68.3 / 80.0 / 77.5; a graph-free MLP, 46.5 / 55.1 / 71.4. The gaps
  between propagation rules are 1–2 points on Citeseer and Cora and up to
  5 on Pubmed. The gap to the MLP is 24–26 points on the first two
- **Wall clock (Table 2):** 4–48 s to convergence, against 13–185 s for
  Planetoid on the same GPU
- **Depth (Appendix B, 5-fold CV with all labels):** best at 2–3 layers.
  Beyond about 7, the paper says training "can become difficult" without
  residual connections, which keep deeper models trainable. Best results
  are still at 2–3 layers either way

## Limitations

- **One split, tuned on one dataset.** Hyperparameters were chosen on Cora's
  validation set and reused for Citeseer and Pubmed. The random-split row is
  lower everywhere, which is the effect [LIT-581](../literature.d/LIT-581.md) later measured across
  architectures
- **The baselines are copied from Planetoid's paper**, except ICA, which
  was re-run. Only GCN gets 100 initializations
- **The spectral motivation is not tested.** Nothing in the paper isolates
  whether behaving as a low-pass filter is why the layer works. The
  ablation compares propagation rules, not that explanation
- **Homophilous graphs only.** All four benchmarks have neighbours that
  tend to share labels. The paper names the alternative assumption (edges
  carrying information other than similarity) as its motivation and does
  not test a graph where it holds
- **The depth appendix reports the symptom, not a cause.** It attributes
  the difficulty to the receptive field growing with each layer and to
  overfitting, and does not separate the two
