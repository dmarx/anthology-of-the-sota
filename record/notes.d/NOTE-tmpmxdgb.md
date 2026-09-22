---
status: Read
paper: LIT-tmp700y6
title: 'The algorithm changes with depth, and the one it lands on is Bayes-optimal ridge'
version: 1
date: '2026-09-22'
summary: >-
  Read as the second, independent arrival at the mesa-optimization
  construction. Its title asks which algorithm, and its answer is that there
  is no single one: shallow learners sit nearest gradient descent, deeper ones
  nearest ridge, deepest nearest ordinary least squares, and under label noise
  the best-fitting ridge parameter is the Bayes-optimal `σ²/τ²` at every
  setting. The gradient-descent phase is the small-model phase.
---

# NOTE-tmpmxdgb: The algorithm changes with depth, and the one it lands on is Bayes-optimal ridge

<!-- inactive-ok-file: THEORY-tmpvwjjo — Rejected, and cited as the rejected account itself: this document is part of the evidence that retired it, not a recommendation resting on it. -->

## Contribution

Two constructions and a behavioural sweep. The constructions show a
transformer needs only constant depth and `O(d)` width to compute a gradient
step, and constant depth and `O(d²)` to compute a closed-form ridge update —
so expressivity does not pick between them. The sweep then asks which one a
*trained* learner behaves like, and finds the answer depends on the model's
size and on the noise in the data.

## Key insight

**Asking "which algorithm" presupposes there is one.** The paper's own answer
is a phase diagram: the implemented algorithm moves with depth and with
hidden size, and what it converges to as capacity grows is the Bayes-optimal
estimator rather than any particular procedure for reaching it. A learner that
lands on the minimum-Bayes-risk predictor has been selected by its training
objective, which is a squared-error loss; that it does so is a statement about
what training optimizes, not about what the forward pass computes.

## Assumptions

- **Trained on the ICL objective** on linear regression, `d ∈ {8, 16}` —
  the Garg et al. setting again.
- Ground-truth weights `w ~ N(0, τ²)`, label noise `ε_i ~ N(0, σ²)`, so the
  learner can never be certain of the target.
- Hyperparameter search over depth `L ∈ {1, 2, 4, 8, 12, 16}` and hidden size,
  with the others tuned at each point.
- Comparisons are **behavioural** — squared prediction difference between the
  learner's outputs and a reference predictor's — except the probing section,
  which the paper labels preliminary.

## Key results

- **Theorem 1.** A transformer computes the prediction of one gradient-descent
  step on an in-context example with a constant number of layers and `O(d)`
  hidden space.
- **Theorem 2.** A transformer predicts according to a single
  Sherman–Morrison ridge update with a constant number of layers and `O(d²)`
  hidden space. *Both extend to `n` steps by stacking `n` groups of layers.*
- **Noiseless data:** an `L = 16, H = 512, M = 4` learner matches ordinary
  least squares, including the **minimum-norm** solution in the
  underdetermined region `n < d = 8`, where many linear models fit exactly.
  Compared against 3-NN (uniform and weighted), one-pass SGD, one-step batch
  GD, and ridge at several `λ`.
- **Noisy data:** sweeping `σ²` and `τ²`, the ridge parameter that best
  explains the learner's behaviour tracks `σ²/τ²` — which is exactly the
  Bayes-optimal regularizer, and is the closed form of `E[y | x, D]` under
  these Gaussian assumptions. *Holds at every `(σ², τ²)` pair tested.*
- **Algorithmic phases with depth** (Figure 3, `d = 8` and `d = 16`): very
  shallow learners sit closest to gradient descent, then ridge, then OLS.
- **Probing:** late layers non-linearly encode weight vectors and moment
  matrices. The paper calls this preliminary; so does this reading.

## Limitations

**The strongest empirical claim is not the one in the title.** Matching the
minimum-Bayes-risk ridge predictor is a statement about *what* is computed;
"which learning algorithm" asks *how*, and behavioural agreement between
outputs cannot answer it — a closed form and enough iterations of a solver
produce the same numbers. [ARXIV-2310.17086](https://arxiv.org/abs/2310.17086) is the paper that goes after the
*how* with a rate.

**The gradient-descent regime is the small-model regime.** A reader who takes
this paper as support for "in-context learning is gradient descent" has taken
the phase the paper reports for its least capable learners.

**Everything is trained on the ICL objective**, with the consequences
[ARXIV-2310.08540](https://arxiv.org/abs/2310.08540) sets out.

## Bearing on the record

It is the independent second source under [THEORY-tmpknb4d](../theory.d/THEORY-tmpknb4d.md): two different
constructions, by different authors, for two different algorithms, which is
precisely why the expressivity claim cannot identify an algorithm.

For [THEORY-tmpvwjjo](../theory.d/THEORY-tmpvwjjo.md) it is evidence on both sides, and the record files it that
way rather than counting it for the side its title suggests.

## Open questions

- **Does the depth phase diagram survive outside linear regression?** The
  three regimes are measured on one problem class where all three reference
  predictors are available in closed form.
