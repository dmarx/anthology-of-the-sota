---
number: 292
status: Read
formerly:
- NOTE-tmpib9c9
paper: LIT-548
title: 'Tensor Programs IV'
version: 1
date: '2026-09-22'
summary: >-
  Classifies width-scaling parametrizations (abc-parametrizations) and proves
  that every stable, nontrivial one either learns features in the wide limit
  or trains as a kernel, not both. The standard parametrization is stable
  only at an O(1/width) learning rate, which is the kernel side. Introduces µP
  as the unique member that updates every layer maximally. Read end to end
  through §10 and Appendices A, C.1 and D. The proofs in Appendix H were not
  checked line by line.
---

# NOTE-292: Tensor Programs IV

## Contribution

A space of parametrizations, a theorem splitting it in two, and the point in
it everybody now calls µP. Before this, the NTK and mean-field limits were
separate results with separate conventions. After it they are two faces of
one polyhedron, and the question "does this parametrization learn features
at width" has a one-line answer: compute `r`.

## Key insight

**Initialization and updates scale differently with width.** Random
init sums independent terms, so it grows like `√n`. An update is correlated
with the activations it next meets, so it grows like `n`. SP scales the
initialization correctly and so has to shrink the learning rate by `1/n` to
keep the update in range. At that rate the features barely move. µP scales
the two separately.

## Assumptions

- **Architecture:** `L`-hidden-layer MLP. Appendix C sketches the general
  case, and every experiment is an MLP
- **Optimizer:** SGD, batch size 1 in the main text ("straightforward to
  generalize to larger batch sizes"). No momentum, no Adam
- **Nonlinearity:** `tanh` or `σ`-gelu with small `σ` for the classification
  (Assumption 3.1). Only a polynomially bounded weak second derivative for
  computing limits (Assumption H.22)
- **Training time `O(1)` in width.** Width goes to infinity with the number
  of steps fixed
- **Input dimension fixed** as width grows

The record's practices assume Adam-family optimizers on Transformers. None of
that is covered here.

## Key results

- **Theorem 3.3 (stability):** stable iff `a₁+b₁=0`, `aₗ+bₗ=½` for
  `2≤l≤L`, `a_{L+1}+b_{L+1}≥½`, `r≥0`, `2a_{L+1}+c≥1`, and
  `a_{L+1}+b_{L+1}+r≥1`
- **Theorems 3.6 / 3.8 / Corollary 3.9 (Dynamical Dichotomy):** a stable,
  nontrivial parametrization learns features iff `r = 0`, and is in the
  kernel regime iff `r > 0`
- **Corollary 3.10:** any feature-learning limit has the network output
  identically 0 at initialization, in the limit
- **Theorem 4.1:** SP needs a learning rate of `O(1/n)` for finite logits,
  and then it is in the kernel regime
- **Definition 5.1 (µP):** `c = 0`, `bₗ = ½` for all `l`, `a₁ = −½`,
  `aₗ = 0` for middle layers, `a_{L+1} = ½`. Appendix C.1 gives the general
  rule and states µP is the unique stable abc-parametrization with every
  tensor updated maximally and readouts initialized maximally
- **Table 2 (Omniglot 1-shot 5-way, linear 1-hidden-layer):** µP limit
  66.42 ± 0.19, against 47.60 (ReLU GP), 47.82 (ReLU NTK) and 41.68 (linear
  GP/NTK). Finite µP rises from 55.34 at width 2 to 66.41 at width 2¹³
- **Table 3 (Word2Vec CBOW word analogy):** µP limit 43.31 on text8 and
  56.45 on fil9, against 0.0 for GP/NTK. Finite widths 2⁶, 2⁸, 2¹⁰ rise
  toward the limit

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Every stable, nontrivial abc-parametrization is either feature-learning or kernel, not both | strong | Corollary 3.9, proved (Appendix H) |
| C2 | SP is stable only at an `O(1/width)` learning rate and is then in the kernel regime | strong | Theorem 4.1 |
| C3 | Under µP the maximum stable learning rate is constant in width, under SP it scales `1/width` | moderate | theory plus one CIFAR-10 MLP plot, widths 512–8192 |
| C4 | Kernel limits make pretraining useless for transfer | strong | Theorem H.17, as a limit statement |
| C5 | Feature-learning limits beat kernel limits on tasks that need features | moderate | two tasks, linear 1-hidden-layer networks only |
| C6 | The Tensor Programs recipe gives the limit of any architecture and SGD-like optimizer | weak | asserted, and the paper works only MLPs |

## Concepts

- **abc-parametrization** — `Wₗ = n^(−aₗ) wₗ`, `wₗ ~ N(0, n^(−2bₗ))`,
  learning rate `η n^(−c)`. Shifting `a` up and `b` down by `θ` together with
  `c` down by `2θ` leaves training unchanged (Eq. 5), so per-layer multipliers
  and per-layer learning rates are interchangeable
- **stable** — (pre)activations `Θ(1)` at init, and activations and logits
  stay `O(1)` through training as `n → ∞`
- **trivial** — the function does not change during training in the limit
- **feature learning** — the last hidden layer's embedding moves by `Ω(1)`
  per coordinate
- **updated maximally** — a layer's accumulated update contributes `Θ(1)`
  coordinates to the next preactivation

## Connections

The fourth of the Tensor Programs series. Appendix A says it was the
*motivation* for the series, and the first three papers were written to make
the machinery usable first. It unifies the NTK and mean-field lines, and
its "lazy vs active" distinction is the Chizat–Bach one made rigorous. It is
built on by TP-V ([LIT-148](../literature.d/LIT-148.md)), which carries µP to Adam and Transformers and
turns it into hyperparameter transfer. It is re-derived from a spectral-norm
condition by [LIT-437](../literature.d/LIT-437.md).

## Recommendations

- **R1** — Do not scale a model up in the standard parametrization and keep
  its tuned learning rate. The maximum stable rate falls like `1/width`.
  *Topic:* training-optimization. *Status:* standard. *Strength:* strong for
  the exponent, moderate as a practical claim. *Applies when:* widths differ
  by a large factor. Already carried by [SOTA-143](../practices.d/SOTA-143.md).

## Bearing on the record

- **[SOTA-143](../practices.d/SOTA-143.md)** is sourced to TP-V for µP. The parametrization and the reason
  it is needed are here, and are filed as [THEORY-076](../theory.d/THEORY-076.md), which explains
  that practice
- **The 2026-09-19 curation entry's claim that TP-V "is" the µP paper is
  wrong.** TP-V is µTransfer, and µP was introduced here
- **[THEORY-037](../theory.d/THEORY-037.md)** calls the maximal-update principle "what muP is for". That
  principle is Definition 5.2 and Proposition 5.3 here

## Limitations

- **SGD only**, and so no statement about the Adam form of µP practitioners
  use
- **The real-task evidence is linear networks**, because the nonlinear limit
  costs super-exponential time in the number of steps (§8)
- **Fixed training time.** Nothing about what happens when steps grow with
  width. The authors say a quantitative Master Theorem would allow it, and do
  not prove one here
- **The maximum stable learning rate is not the optimal one.** The paper does
  not claim the optimum transfers

## Open questions

- Does the optimal learning rate, not just the stable ceiling, have zero
  width exponent under µP? TP-V answers empirically
- What does the dichotomy become when depth also grows? [LIT-150](../literature.d/LIT-150.md) and [LIT-462](../literature.d/LIT-462.md)
  take this up
