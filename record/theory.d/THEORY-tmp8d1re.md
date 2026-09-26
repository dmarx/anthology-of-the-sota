---
status: Active
title: 'A modified-backpropagation rule that keeps only non-negative relevance produces a matrix chain that converges to rank 1, so the later layers can only flip the map''s sign'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-26'
source:
- LIT-tmpo0kkk
explains:
- SOTA-430
summary: >-
  Sixt, Granz and Landgraf (2019), [LIT-tmpo0kkk](../literature.d/LIT-tmpo0kkk.md), Theorem 1. The `z⁺`-rule
  backpropagates relevance through a product of non-negative matrices; such a
  product converges to a rank-1 matrix `C = c γᵀ`, and then `C v = λ c` for every
  `v`. So the relevance vector set at the output — the thing that carries which
  class is being explained — survives only as a scalar, and can at most flip the
  map's sign. Class-insensitivity and independence of the later layers' weights
  are the same fact. `Active` because it is a theorem with a discriminating arm
  that was published (DeepLIFT does not converge) and a second that was built to
  order (the DeepLIFT ablation does).
---

<!-- inactive-ok-file: SOTA-430 — Proposed, and declared in `explains:`; this account underwrites one family in that practice's verdict table and says explicitly which rows it does not reach. An account explaining a not-yet-in-force practice is the normal case. -->
<!-- inactive-ok-file: THEORY-113 — Proposed, and cited only to draw the boundary between the two accounts: they cover disjoint method families and neither rests on the other. -->

# THEORY-tmp8d1re: A modified-backpropagation rule that keeps only non-negative relevance produces a matrix chain that converges to rank 1, so the later layers can only flip the map's sign

## Source

Sixt, Granz and Landgraf (2019), [LIT-tmpo0kkk](../literature.d/LIT-tmpo0kkk.md) — ICML 2020, §2 and §4.

## The account

A modified-backpropagation attribution sets a relevance vector at the output
layer — for a classifier, the explained logit — and propagates it down with a
custom rule instead of the gradient. For the `z⁺`-rule, used by Deep Taylor
Decomposition, LRP-α1β0 and Excitation BP, each layer's backward operator is a
**non-negative** matrix, so the whole path is

    C_k = ∏_{l}^{k} Z⁺_l

**Theorem 1: a product of non-negative matrices converges to a rank-1 matrix.**
The proof is geometric and short: the first matrix's columns all lie in the
positive quadrant, each further multiplication takes non-negative linear
combinations of columns already inside that cone, and the cone shrinks with every
factor until it is a single direction. The paper's simulations find the
convergence exponential.

**The consequence is the finding.** Write the converged chain as `C = c γᵀ`.
Then for any relevance vector `v`,

    C v = c γᵀ v = λ c,   λ ∈ ℝ

The direction is `c` whatever `v` is. The output relevance survives only as the
scalar `λ` — so it can rescale the map and, if `λ < 0`, invert it, and nothing
else. **Which class you asked about, and what the later layers' weights are, both
enter only through `v`.** That is why these methods give the same map for "cat"
and "dog", and why their maps do not change when the last layers are randomized:
those are one mechanism, not two coincidences.

## Why this is `Active` rather than `Proposed`

Because it is a theorem about matrix products, and because the paper does the
thing this record keeps asking for — it includes arms the account says must
behave differently, in both directions.

- **A published exception.** DeepLIFT is the one tested modified-BP method that
  does not converge, and the account says why: its linear-layer rule separates
  positive and negative contributions and *intermixes* them, so the chain is not
  non-negative.
- **An exception built to order.** The authors then construct **DeepLIFT
  Ablation**, removing the intermixing so that `W⁺` drives the positive rule and
  `W⁻` the negative. The chains decouple, both become non-negative — a product
  of two non-positive matrices is non-negative — and "as predicted by the theory,
  it converges." A prediction made in advance about a variant that did not
  previously exist.
- **A measurement of the predicted quantity, not of a proxy.** Cosine similarity
  convergence traces the collapse layer by layer: every analysed method except
  LRP z and DeepLIFT reaches at least **0.99** on VGG-16 and ResNet-50.
- **And the behavioural consequence separates the same two groups twice.** On
  random logits the converging methods give "SSIM very close to 1" against 0.4
  to 0.8 for the rest; under cascading parameter randomization, the same
  clustering.

## What it does not cover

- **Not Guided Backprop, Deconv or RectGrad.** They apply a ReLU to the
  gradient, so the backward pass is not a linear map at all and Theorem 1 does
  not apply. The paper says so and hands those to Nie, Zhang and Patel (2018),
  `1805.07039`, which this record does not hold. Their failure is a **third**
  mechanism.
- **Not the gradient family.** Integrated Gradients and SmoothGrad "rely on the
  gradient directly ... which does not converge". Their randomization behaviour
  is [THEORY-113](THEORY-113.md)'s subject, the model-independent input multiplier, and the two
  accounts do not overlap or compete.
- **Not a rival to the switches story — a refutation of it.** "Other than argued
  in (Gu et al. 2018), the class insensitivity is not caused by missing ReLU
  masks and Pooling switches." Worth recording because that is the intuitive
  explanation and it is wrong.
- **Not a claim that non-convergence means faithful.** LRP-α5β4 converges less
  on VGG-16 and "also produces rather noisy saliency maps"; ROAR scores
  Integrated Gradients and Guided Backprop "equally bad, worse than a random
  baseline", so ROAR "does not separate converging from non-converging methods".
  Escaping this mechanism is necessary, not sufficient — the same shape as
  [SOTA-430](../practices.d/SOTA-430.md) being a rejection rule rather than a certificate.
- **The threshold is reported, not derived.** "Sufficiently converged" carries
  the practical weight and 0.99 is where the measurements land, not a bound.
