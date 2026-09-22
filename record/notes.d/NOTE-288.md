---
number: 288
status: Read
formerly:
- NOTE-tmpx2d9k
paper: LIT-544
title: 'The transition the posterior makes and the transition SGD makes are not the same transition'
version: 1
date: '2026-09-22'
summary: >-
  Read for the distinction in its title, which the record needed and did not
  have. Bayesian phase transitions are changes in where the posterior
  concentrates as sample size grows, and are well defined; dynamical
  transitions are changes in the SGD trajectory, and are not. In the one model
  where both are computed, the sharpest Bayesian transition — predicted at
  `n_cr ≈ 600` and observed at 600–700 — has no dynamical counterpart at all.
---

# NOTE-288: The transition the posterior makes and the transition SGD makes are not the same transition

<!-- inactive-ok-file: THEORY-070, THEORY-071, THEORY-072 — all Proposed, and named here as the three rival grokking mechanisms, every one of them a claim about a trajectory. That they are Proposed is the point being made when they are cited. -->

## Contribution

It picks a model small enough that singular learning theory can be carried out
exactly, derives the local learning coefficients of its critical points by
hand, uses the free energy formula to predict where the Bayesian posterior
jumps, checks the prediction by MCMC — and then, separately, watches SGD and
asks whether the same jumps appear. The answer is partly. That "partly" is the
paper.

## Key insight

**Occam's razor is not a prior somebody chose; it falls out of the free
energy, and it is a function of how much data you have.** With
`F_n ≈ min_α [n L_n(w*_α) + λ_α log n + c_α]`, at small `n` the complexity term
dominates and the posterior prefers a simple, badly-fitting solution; at large
`n` the loss term dominates and it will pay complexity for fit. Learning, in
the Bayesian picture, is a sequence of such swaps.

The corollary is the caution. That sequence is indexed by **sample size**. A
training curve is indexed by **step**. These are different orderings over
different objects, and the paper is the first thing in this record to say so
and then measure both.

## Assumptions

- The **Toy Model of Superposition** (Elhage et al.) with `r = 2` hidden
  dimensions, in the high-sparsity limit. Tiny, deliberately.
- The `k`-gon classification is not claimed exhaustive: "we do not claim to
  have found all possible critical points of the TMS".
- The free energy formula absorbs the volume constant and `log log n` terms
  into a constant `c_α` treated as effectively constant — the paper notes the
  constants "can play a nontrivial role" at low `n`.
- `λ̂` estimates are used where theoretical values are unavailable, with
  caveats the paper localizes to an appendix.
- MCMC classification "becomes increasingly uncertain" below `n = 400`, and
  MCMC fails outright for `n` much above the reported range.

## Key results

- **`k`-gons are critical points**, proved for `r = 2`; standard `k`-gons for
  `k ∈ {5,6,7,8}` with `k < c` are minimally singular, and the `k = c` case is
  non-degenerate. Exact local learning coefficients are derived for the ones
  MCMC actually visits.
- **The local free energy formula.**
  `F_n(W_α) = n L_n(w*_α) + λ_α log n − (m_α − 1) log log n + O_p(1)`.
  A Bayesian phase transition `α → β` occurs when `F_n(W_β) − F_n(W_α)` changes
  sign.
- **A number, predicted and then observed.** The `5 → 6` transition is
  predicted at **`n_cr ≈ 600`** and appears in the MCMC phase proportions at
  **`600 ≤ n ≤ 700`**. *Holds when:* `n ≳ 400`, below which the classification
  is unreliable and the paper says not to read the correspondence.
- **The same critical points explain SGD plateaus**, which the paper argues is
  not a coincidence: SLT associates posterior phases with singularities of the
  KL divergence, and nonlinear dynamics associates trajectory behaviour with
  singularities of a potential.
- **And the negative result.** "There is no necessary relation between these
  two kinds of transitions." The `5 → 6` Bayesian transition **has not been
  observed as a dynamical transition** — possibly because the regions are
  distant or separated by high energy barriers, possibly because it occurs with
  low probability per step.
- **The Bayesian Antecedent Hypothesis (BAH).** Dynamical transitions
  encountered in training have Bayesian antecedents. Its obstruction is that a
  Bayesian transition requires `λ` to *increase*. The paper's analysis finds
  antecedents for the dynamical transitions it observed, **with two cases where
  the analysis is inconclusive**.

## Limitations

**Two hidden dimensions.** This is the price of being able to derive anything.
Nothing here transfers by argument; what transfers is the distinction and the
demonstration that the two kinds of transition can come apart.

**The BAH is a conjecture and is labelled one.** It is the bridge from a
well-defined theory to the phenomena people care about, and it is the least
supported thing in the paper.

**The constants matter where the data is thin.** The `c_α` term is treated as
constant and the paper notes it is not, at exactly the small-`n` end where
Bayesian transitions are densest.

## Bearing on the record

**Every grokking mechanism this record holds is dynamical.** `THEORY-072`
(a walk down the weight norm), `THEORY-071` (norm moving between circuits)
and `THEORY-070` (leaving the lazy regime) are all claims about a
trajectory, all `Proposed`, and none is general. Everything singular learning
theory proves is about a posterior indexed by sample size. This paper is where
the gap between those two things is named, and the record needed that before it
could hold both literatures without conflating them.

**It also bears on `SOTA-200`.** A capability that appears suddenly at some
scale is a claim about `n`, which is the Bayesian axis; a capability that
appears suddenly during training is a claim about `t`. The practice's third
check now says "move the regime and see whether the discontinuity moves", and
`n` is one of the regimes — with, in this model, a predicted crossing point.

## Open questions

- **Is the BAH true?** Nothing outside this paper tests it, and two of its own
  cases are inconclusive.
- **Does a Bayesian transition with no dynamical counterpart mean anything for
  a practitioner?** The `5 → 6` case is the most striking result here and the
  record cannot say what to do with it.
