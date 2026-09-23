---
number: 74
status: Proposed
formerly:
- THEORY-tmpzq41c
title: 'A phase transition of the Bayesian posterior and a transition in the training trajectory are different events, and only the first is well defined'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
- model-stability
- capability-thresholds
date: '2026-09-22'
source:
- LIT-544
extends:
- THEORY-075
promote_when: >-
  The Bayesian Antecedent Hypothesis is tested somewhere the answer could come
  out either way — a model where dynamical transitions are observed and the
  posterior can be sampled, with at least one dynamical transition shown to
  have **no** Bayesian antecedent, or a principled account of why none can. The
  source finds antecedents for its own transitions with two inconclusive cases,
  in a model with two hidden dimensions. Confirmation in a second toy model
  would not move this.
summary: >-
  Chen, Lau, Mendel, Wei and Murfet ([LIT-544](../literature.d/LIT-544.md)). A **Bayesian** phase
  transition is a change in where the posterior concentrates as sample size `n`
  grows, follows from the free energy formula
  `F_n ≈ min_α [n L_n(w*_α) + λ_α log n + c_α]`, and is mathematically well
  defined. A **dynamical** transition is a change in the SGD trajectory as a
  function of step, and its "formal status has remained elusive". In the one
  model where both are computed, the sharpest Bayesian transition — predicted
  at `n_cr ≈ 600`, observed at 600–700 — has no dynamical counterpart at all.
---

# THEORY-074: A phase transition of the Bayesian posterior and a transition in the training trajectory are different events, and only the first is well defined

<!-- inactive-ok-file: THEORY-070, THEORY-071, THEORY-072 — all Proposed, and named here as the three rival grokking mechanisms, every one of them a claim about a trajectory. That they are Proposed is the point being made when they are cited. -->
<!-- inactive-ok-file: THEORY-073 — Proposed, filed in this same contribution as the stagewise account this one cautions; new, not retired. -->
<!-- inactive-ok-file: ADR-031 — Proposed, cited as the decision that separates an explanation from the practice it explains, which is the schema this document is filed under; Proposed is the resting state of an unmoved decision here. -->

## The account

Two things in this literature are called phase transitions and they are indexed
by different variables.

**The Bayesian one.** The local free energy of a region `W_α` dominated by a
critical point is

    F_n(W_α) = n L_n(w*_α) + λ_α log n − (m_α − 1) log log n + O_p(1)

so, approximately, `F_n ≈ min_α [n L_n(w*_α) + λ_α log n + c_α]`. At small `n`
the `λ log n` term dominates and the posterior sits on a **simple region even
at high loss**; as `n` grows the `n L_n` term takes over and it moves to a
**lower-loss, more complex** region. A transition is where the ordering swaps.
This is Occam's razor as an automatic consequence of the free energy, indexed by
**sample size**, and it is a theorem.

**The dynamical one.** A plateau in the training curve followed by a sudden
drop, indexed by **step**. This is what everybody actually observes and, as the
source puts it, its formal status has remained elusive.

**They are not the same event.** "There is no necessary relation between these
two kinds of transitions." A Bayesian transition need not have a dynamical
counterpart — the regions may be far apart or separated by barriers SGD does
not cross. The paper's own headline Bayesian transition is an example.

## The evidence, in one model

The Toy Model of Superposition at `r = 2` hidden dimensions, where regular
`k`-gons are proved to be critical points and their local learning coefficients
can be derived rather than estimated:

- The free energy formula predicts the **`5 → 6` transition at `n_cr ≈ 600`**;
  MCMC over the posterior shows it at **`600 ≤ n ≤ 700`**. A number, predicted
  and then observed.
- The same `k`-gon critical points explain the plateaus of SGD training curves
  — which the paper argues is no coincidence, since SLT ties posterior phases
  to singularities of the KL divergence and nonlinear dynamics ties trajectory
  behaviour to singularities of a potential.
- **And the `5 → 6` transition has not been observed as a dynamical
  transition.** The strongest Bayesian result in the paper is the one with no
  training-time counterpart.

## The Bayesian Antecedent Hypothesis

The conjecture that dynamical transitions encountered in neural network
training *do* have Bayesian antecedents. Its obstruction is stated: a Bayesian
transition `α → β` requires `λ` to **increase**, so a dynamical transition that
reduces loss without increasing degeneracy has nowhere to come from. The
paper's analysis finds antecedents for the dynamical transitions it observed,
**with two cases where the analysis is inconclusive**.

## Why it is `Proposed`, and what is not in doubt

The **distinction** is not in doubt — it is definitional, and the `5 → 6` case
demonstrates the two can come apart. What is `Proposed` is the bridge: whether
the transitions people care about are governed by the theory that is
well-defined. That is the BAH, it is labelled a hypothesis by its authors, and
it is supported in a model with two hidden dimensions and a critical-point
classification the paper declines to call exhaustive.

## Why the record needed this

**Every grokking mechanism it holds is dynamical.** `THEORY-072` (a walk
down the weight norm), `THEORY-071` (norm moving from a memorising circuit
to a more efficient one) and `THEORY-070` (leaving the lazy regime) are
all claims about a trajectory, all `Proposed`, and none is general.
`THEORY-073`'s stages are dynamical too. Everything `THEORY-075`
supplies is Bayesian.

Without this document the record would hold two literatures that use the same
words for different objects, and its own summary of them would blur the two —
which is the failure it filed `ADR-031` and the two-collapse-accounts precedent
to avoid.

**It also sharpens `SOTA-200`.** A capability appearing suddenly *at some
scale* is a claim about `n`; a capability appearing suddenly *during training*
is a claim about `t`. The practice's third check now says to move the regime
and see whether the discontinuity moves; `n` is one of those regimes, and this
is the only work the record holds that predicts where the crossing should be.
