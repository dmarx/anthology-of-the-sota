---
status: Proposed
promote_when: >-
  The same discriminating construction outside factorization models: a
  problem built so that the minimum-norm and minimum-rank solutions differ,
  trained with a non-linear network of the ordinary kind (ReLU, a
  transformer block) at a practical step size and initialization, by a group
  other than Razin and Cohen's, reporting which of the two gradient descent
  approaches. What would NOT meet it: further measurements that trained weight
  matrices are low rank, which a small-norm bias also produces in almost every
  setting, since the two only come apart on a problem constructed to separate
  them; or further proofs inside matrix and tensor factorization, which is
  where the account already holds.
title: 'Gradient descent on a factorized model is biased toward low rank, not small norm: there are problems where it sends every norm to infinity to lower the rank'
version: 1
tags:
- training-optimization
- model-stability
- analysis-and-evaluation
date: '2026-10-01'
source:
- LIT-tmpw8qxm
explains: []
summary: >-
  Razin (2024), [LIT-tmpw8qxm](../literature.d/LIT-tmpw8qxm.md), Part II, "Implicit Regularization in Deep
  Learning May Not Be Explainable by Norms" (Razin and Cohen, NeurIPS 2020). Complete a 2×2 matrix from three entries, with every norm and
  quasi-norm minimized at a bounded value of the missing one. Gradient flow
  on a depth L ≥ 2 matrix factorization, from initialization arbitrarily close
  to zero, sends that entry to infinity with probability 0.5 — every norm
  diverges together while the effective rank falls to its minimum of 1. So no
  norm can be what the implicit regularization minimizes; rank is the
  reading left standing. Proved for linear factorizations and extended,
  under conditions, to tensor factorizations equivalent to polynomial-activation
  networks — not to ReLU networks.
---

<!-- inactive-ok-file: THEORY-072, THEORY-041, THEORY-045 — Proposed; named to say how this account bears on them, not cited as support -->

# THEORY-tmp654td: Gradient descent on a factorized model is biased toward low rank, not small norm: there are problems where it sends every norm to infinity to lower the rank

## Source

Razin (2024), [LIT-tmpw8qxm](../literature.d/LIT-tmpw8qxm.md) — PhD thesis; the matrix result is Part II's
reprint of Razin and Cohen (NeurIPS 2020), §3, Theorem 1 and Corollary 1, and the tensor
results Razin, Maman and Cohen (ICML 2021, 2022).

## The account

Overparameterized models fitting the same training data have many
interpolating solutions, and gradient descent picks one. The standing guess
for *which* one, in matrix factorization, was a norm: Gunasekar et al. (2017)
conjectured the nuclear norm, and Arora et al. (2019) conjectured that no
norm or quasi-norm describes it. Neither paper is in the record. The account
here is the second conjecture made into a proof, plus a positive claim about
what replaces the norm: **the bias is toward low rank, and where the two
conflict gradient descent gives up the norm entirely.**

## What was actually shown

**The construction.** Complete a 2×2 matrix from `W₁₂ = 1`, `W₂₁ = 1`,
`W₂₂ = 0`. Every solution has the form `[[W₁₁, 1], [1, 0]]`. Any norm or
quasi-norm is minimized with `W₁₁` in a bounded interval (Proposition 1),
while the rank approaches its minimum of 1 only as `|W₁₁| → ∞`. Minimizing a
norm and minimizing rank therefore demand opposite things, and which one
gradient descent does is observable.

**The proof.** [LIT-tmpw8qxm](../literature.d/LIT-tmpw8qxm.md) shows that under gradient flow on a depth `L ≥ 2`
factorization the sign of the end matrix's determinant never changes. Every
exact solution has determinant `−1`. A run that starts with positive
determinant can only approach the solution set by letting `W₁₁ · W₂₂` stay
above 1 while `W₂₂ → 0` — that is, by sending `|W₁₁|` to infinity. Theorem 1:
for such a run, lowering the loss raises every norm and quasi-norm and drives
the rank surrogates toward 1; Corollary 1: if the loss goes to zero, every
norm goes to infinity. Under any initialization whose entries are drawn
independently from continuous distributions symmetric about zero, a positive
determinant has probability exactly 0.5, and rescaling the initialization
toward the origin does not change it. So "initialize small and gradient
descent finds the minimum-norm solution" is false here half the time, for
every norm at once.

**What could have come out the other way.** The construction is the test: a
norm-minimizing bias would have kept `W₁₁` bounded. The thesis also runs
gradient descent with small step size and small initialization at several
depths, balanced and unbalanced, and the unobserved entry grows as the loss
falls, as the theorem predicts. That is a check that the gradient-flow idealization
is not what produces the result; it is shown as plots of representative runs.

**The positive half is weaker than the negative half.** That no norm explains
the bias is proved, by counterexample. That *rank* does is offered as "a
potentially more useful interpretation" — consistent with the construction,
and with Arora et al.'s finding that deep factorization promotes sparse
singular values, but not a characterization: global rank minimization is
computationally hard in the worst case, so gradient descent can at most be
"searching for low rank locally". The thesis then extends the rank reading to
tensor factorization (equivalent to a shallow convolutional network with
polynomial non-linearity) and hierarchical tensor factorization (a deep one),
proving incremental learning toward low tensor rank "under certain
conditions". ReLU networks are outside every proof.

## How it bears on what the record already holds

- **[THEORY-072](THEORY-072.md)** explains grokking by the weight norm walking down toward a
  critical value. This does not contradict it: the construction shows that
  "gradient descent minimizes a norm" fails as a general principle, not that
  norm never governs a particular phenomenon, and weight decay — which
  [THEORY-072](THEORY-072.md) relies on — is an explicit norm penalty, not implicit
  regularization. What it removes is the fallback that a norm account of
  generalization can lean on gradient descent's own bias when there is no
  weight decay.
- **[THEORY-041](THEORY-041.md)** reports that unconstrained transformer matrices drift toward
  rank deficiency. A bias toward low rank would produce exactly that, but
  nothing in [LIT-tmpw8qxm](../literature.d/LIT-tmpw8qxm.md) was measured on a transformer, and [THEORY-041](THEORY-041.md)'s
  account is about conditioning; this is consistent with it and is not
  evidence for it.
- **[THEORY-045](THEORY-045.md)** measures generalization by the volume of behaviourally
  equivalent parameter space, a different complexity measure from rank or
  norm; neither bears on the other.

## What this does not say

- **It does not say trained networks are low rank because of gradient
  descent.** Small norm also tends to produce low rank. The two only separate
  on a problem built to separate them, and that problem is a 2×2 matrix.
- **It says nothing about the other half of initializations.** With negative
  initial determinant the theorem is silent.
- **It is gradient flow on a linear model, and its non-linear extension is
  to polynomial activations.** The idealization is checked with small finite
  steps; it is not checked at learning rates anyone trains with.
- **One group.** The four papers the thesis collects share an advisor.
