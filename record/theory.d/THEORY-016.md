---
number: 16
status: Active
formerly:
- THEORY-tmpm49yp
title: 'Test-time weight scaling computes a geometric-mean average over the dropout ensemble, exactly for logistic units and to second order elsewhere'
version: 1
tags:
- model-stability
date: '2026-09-17'
source:
- LIT-393
- LIT-395
explains:
- SOTA-240
summary: >-
  Baldi and Sadowski (2013), [LIT-393](../literature.d/LIT-393.md) — the single forward pass with
  scaled weights is not a heuristic stand-in for the ensemble. For a logistic
  unit it computes the normalized weighted geometric mean over all dropout
  configurations *exactly*, and the logistic and constant functions are the
  only ones with that property. In deep networks one approximation remains,
  it is exact for consistent units and good to second order, and
  [LIT-395](../literature.d/LIT-395.md)'s Monte-Carlo comparison is the empirical check.
---

# THEORY-016: Test-time weight scaling computes a geometric-mean average over the dropout ensemble, exactly for logistic units and to second order elsewhere

## Source

Baldi and Sadowski (2013), [LIT-393](../literature.d/LIT-393.md);
corroborated empirically by Srivastava et al. (2014),
[LIT-395](../literature.d/LIT-395.md) §7.5.

## What was actually shown

**The single-unit result is an identity, not a bound.** Let a unit's output
under dropout configuration `i` be `Oᵢ`, occurring with probability `Pᵢ`.
Define the weighted geometric mean `G = ∏ Oᵢ^Pᵢ`, the same over the
complements `G' = ∏ (1−Oᵢ)^Pᵢ`, and the normalized weighted geometric mean
`NWGM = G/(G+G')`. For a logistic unit,

    NWGM(O₁,...,O_m) = σ(E[S])

exactly. The proof is two lines and turns entirely on the logistic identity
`[1−σ(x)]/σ(x) = c·e^{−λx}`, which converts a product over configurations
into an exponential of a sum. With Bernoulli gating this means the `NWGM`
over *all* dropout configurations is computed by one forward pass:
`σ(Σⱼ wⱼ pⱼ Iⱼ)`. Scaling the weights by their retention probabilities is
that computation.

**The sharp part is the converse.** The only functions `f` satisfying
`NWGM(f) = f(E)` are the constants and the logistic functions. So this is a
property of the nonlinearity rather than a general fact about averaging — the
scaling rule works because of what a sigmoid is.

**In a deep network, three recursive equations and only one approximation.**
The averaging behaviour reduces to `E(Oᵢ) ≈ NWGM(Oᵢ)`, then
`NWGM(Oᵢ) = σᵢ[E(Sᵢ)]`, then `E(Sᵢ) = Σ wᵢⱼ pⱼ E(Oⱼ)`. The second and third
are exact — the second by the identity above, the third by linearity of
expectation. **Only the first is an approximation**, and its error is
characterized rather than assumed: it is exact iff the unit's activity is the
same across all subnetworks (a *consistent* unit), degrades with the variance
of that activity, holds to second order in general, and is exact whenever
`NWGM ≤ E` or activities are consistently low. Linear units do not need it at
all, so a regression network with linear output layers loses one layer of
approximation.

**What could have come out the other way, and separately did not.**
[LIT-395](../literature.d/LIT-395.md) §7.5 runs Monte-Carlo
averaging over `k` sampled subnetworks against weight scaling on MNIST. If
the scaling rule were a poor stand-in, sampled averaging would keep improving
past it; instead weight scaling sits where 50-plus samples land. That is an
empirical check of a claim derived analytically, by different authors, and it
agrees.

## What this does not say

**It does not say dropout works because it is an ensemble.** This account
explains why the *test-time procedure* is cheap and legitimate. It says
nothing about why training under multiplicative noise generalizes better,
which is a different question with a different answer —
[THEORY-015](THEORY-015.md), from the same paper's §5 and from
[LIT-396](../literature.d/LIT-396.md). Reading the ensemble story
as the reason dropout helps is the overreach this document exists to mark.

**The averaging is geometric, not arithmetic, and the difference is not
cosmetic.** What one forward pass computes is the `NWGM`, and the paper's
whole third section is devoted to how far that is from the mean. Descriptions
of dropout as "averaging the predictions of exponentially many networks"
elide exactly the quantity that required the analysis.

**The exactness is for logistic units.** The derivation is given for sigmoidal
networks, with a similar result noted for normalized exponential (softmax)
transfer functions. It does not transfer by default to the rectified-linear
networks that dropout is mostly used in today, and the record holds no
equivalent result for them.

**Consistency is assumed to be benign and never measured.** The approximation
degrades with across-subnetwork activity variance, the bounds are corroborated
by simulation, and nobody in this line reports that variance in a trained
network of practical size. The account's weakest joint is the one it names
itself.
