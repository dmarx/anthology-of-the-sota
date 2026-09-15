---
status: Read
paper: LIT-tmpcjyw1
title: 'EGGROLL, Unrolled'
version: 1
tags:
- training-optimization
date: '2026-09-15'
summary: >-
  Works out what EGGROLL's low-rank update converges to — a resolvent-filtered
  gradient, which can be nonconservative and can turn an attracting optimum
  into a repelling one, while being exact on every quadratic objective — and
  turns the finite-population half of the analysis into LOO-ROLL, which
  replaces two antithetic evaluations per direction with one leave-one-out
  evaluation at unchanged expected field.
---

# NOTE-tmpn2q7k: EGGROLL, Unrolled

## Contribution

Asks what a low-rank ES update is actually optimizing, and answers exactly.
Three separable findings: the mean field is a resolvent applied to the
smoothed gradient and need not be the gradient of anything; the finite-rank
variance surcharge is negligible at transformer width; and the antithetic
implementation is spending an evaluation it can get back. The third is the
practical yield and the first is the one that should change how people set the
perturbation radius.

## Key insight

**Identity covariance is not enough to make a perturbation law behave like a
Gaussian.** A rank-one product has the same covariance as a dense Gaussian and
lives on a measure-zero subset of the matrix space. The paper's move is to
stop arguing about whether that is worrying and compute the consequence: the
population field is `R∇f̃` for an explicit resolvent `R` acting as an
anisotropic low-pass filter. Because the filter attenuates singular components
unequally, it can *tilt* a mode rather than scale it, and a superposition of
tilted modes has a nonsymmetric Jacobian — a field that is not the gradient of
any function. The separation that makes this useful rather than alarming is
that the whole effect vanishes on quadratics, so it is governed by how
non-quadratic the objective is over the perturbation radius.

## Assumptions

- **Rank-`r` Gaussian-product perturbations** as in EGGROLL, with the
  antithetic implementation as the baseline being improved on.
- **Smoothness for the bounds**: Lipschitz gradient for the first field-error
  bound; Lipschitz Hessian for the second, which gains a power of `σ` from the
  cancellation in the antithetic difference.
- **A local affine model** for the variance comparison against dense Gaussian
  ES.
- **Global Fourier regularity** for the conservativity analysis, which is
  carried out mode by mode on real trigonometric polynomials — a device for
  constructing counterexamples, not a claim about LLM objectives.
- The LOO-ROLL derivation assumes the existing per-prompt centering and
  standardization are retained, so the two estimators differ only in the
  baseline and not in how scores are scaled.

## Key results

- **The population field is `R∇f̃`.** An explicit resolvent applied to the
  gradient of the perturbation-smoothed objective. The resolvent's attenuation
  factor decreases monotonically from one and reaches one half at a
  characteristic threshold; the transformed singular coefficient is *not*
  monotone, increasing up to that threshold and decreasing beyond it.
- **Nonconservativity.** A theorem characterizes which perturbation laws give
  a conservative field for every real trigonometric polynomial; the
  Gaussian-product law fails, so a trigonometric-polynomial objective with a
  nonconservative population field exists. The obstruction disappears at
  `r = 1` when the matrix reduces to a vector, where the law is spherical.
- **Stability reversal.** A bounded smooth counterexample in which the largest
  real part of the population-field Jacobian's eigenvalues is **positive at
  rank one and negative at rank two** — rank-two dynamics converge to a point
  rank-one dynamics run away from. Reproduced numerically.
- **Exactness on quadratics.** For any quadratic `f` and any direction, the
  antithetic difference equals the directional derivative exactly. **EGGROLL
  is exact on the whole quadratic class, at every rank and every radius.**
- **Nonasymptotic field-error bounds** for smooth objectives, separating the
  error from ordinary smoothing from the additional error caused by finite
  rank, with the leading finite-rank correction identified.
- **Variance.** Under the local affine model, rank-one perturbations raise the
  gradient-estimator variance by a small factor over dense Gaussian ES —
  tangible in a small matrix, near-negligible at full transformer width.
  Monte Carlo agrees with the exact prediction at every tested rank.
- **Transformer audit.** Perturbing a sub-block of one attention or MLP matrix
  in Qwen3-0.6B against a backpropagated reference gradient, over four radii,
  8192 directions, three seeds: rank-one single-direction MSE sits above the
  dense baseline and falls toward it by rank eight, while the estimated
  population mean keeps **cosine near one** with the true block gradient at
  every rank.
- **LOO-ROLL.** A leave-one-out baseline built from the population mean that
  score centering already computes. Preserves the finite-rank population field
  exactly before standardization; needs no extra fitness evaluations, no extra
  model-sized state, no extra communication rounds. At fixed population size,
  estimating the baseline adds only a lower-order term to the directional
  variance. At equal evaluation cost it **halves estimator MSE in transformer
  blocks**, because the budget funds `N` independent directions rather than
  `N/2` antithetic ones.
- **End-to-end.** Ten matched-wall-time post-training settings, models up to
  8B: **seven improvements, three unresolved, no significant loss**, five
  surviving Holm correction. GSM8K accuracy rises at 0.6B and at 8B.
- **Rank does not pay.** No reproducible reward-based advantage for rank eight
  over rank one at matched wall time.
- **Two derived techniques set aside.** Rank extrapolation and a
  reference-point control variate are derived as the natural responses to the
  finite-rank bias and finite-population variance, and the experiments find no
  practical gain for their cost.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The low-rank population field is a resolvent-filtered gradient | strong | derived explicitly, verified numerically |
| C2 | That field can be nonconservative | strong as an existence claim | a theorem plus a constructed counterexample; says nothing about frequency at LLM scale |
| C3 | Finite rank can reverse the local stability of an optimum | strong as an existence claim | eigenvalue calculation, reproduced numerically |
| C4 | EGGROLL is exact on every quadratic objective at every rank and radius | strong | an identity, not an approximation |
| C5 | Finite-rank variance surcharge is negligible at transformer width | strong | affine prediction plus the Qwen3-0.6B audit |
| C6 | The rank-one mean direction still tracks the true gradient in a transformer block | strong | cosine near one across ranks and radii |
| C7 | LOO-ROLL preserves the expected field at half the evaluation cost | strong | derivation, plus measured MSE halving |
| C8 | LOO-ROLL improves end-to-end post-training | moderate | seven of ten paired tests, five surviving Holm, no losses — honest and not overwhelming |
| C9 | Rank above one is not worth its cost | moderate | no reproducible advantage at matched wall time, several settings |
| C10 | These pathologies occur in practice at LLM scale | not claimed | and the paper is careful not to |

## Method

LOO-ROLL, concretely: sample `N` independent one-sided low-rank directions
rather than `N/2` antithetic pairs. Score each. Remove the population-level
reward offset with a leave-one-out baseline — the population mean already
computed for centering — instead of subtracting an antithetic partner. The
leave-one-out scores differ from population-centered scores by a common factor
that cancels under standardization, so the existing centering and scaling code
is reused unchanged. Seed-based perturbation reconstruction, layerwise weight
updates and weight synchronization are all retained from EGGROLL.

## Concepts

- **Population field** — the mean update direction after averaging over
  perturbations, as distinct from the gradient of the objective.
- **Resolvent** — the explicit operator mapping the smoothed gradient to the
  population field; here an anisotropic low-pass filter.
- **Conservative field** — one that is the gradient of some scalar function,
  equivalently has a symmetric Jacobian. The property the low-rank field can
  lack.
- **Leave-one-out baseline** — a per-member baseline formed from the rest of
  the population, replacing the antithetic partner's role.

## Connections

Directly about EGGROLL, and it is the first paper in the line to ask a
correctness question rather than a throughput or leaderboard question. Its
framing of ES as zeroth-order optimization connects it to the memory-efficient
fine-tuning literature, where the antithetic estimator it replaces is the
default. Lineage is on the LIT.

## Recommendations

<!-- inactive-ok-block: SOTA-tmph4wug — Proposed, filed in this same change; named as the practice this paper's estimator argument supports -->
- **R1** — Use one evaluation per direction with a leave-one-out baseline
  rather than antithetic pairs. *Topic:* post-training. *Status:*
  experimental. *Strength:* strong. Filed as [SOTA-tmph4wug](../practices.d/SOTA-tmph4wug.md).
- **R2** — Use rank one. Higher rank buys down a variance surcharge that was
  not the binding constraint. *Topic:* post-training. *Strength:* moderate.
  Not filed — one group, one paper.
- **R3** — Treat the perturbation radius as the parameter that decides whether
  you are in the safe regime, since the analysis is exact on quadratics and
  degrades with how non-quadratic the objective is over that radius. *Topic:*
  post-training. *Strength:* moderate, and the most transferable idea here.

## Bearing on the record

<!-- inactive-ok-block: SOTA-tmph4wug — Proposed, filed in this same change; named as the practice this paper's estimator argument supports -->
Filed as [LIT-tmpcjyw1](../literature.d/LIT-tmpcjyw1.md), `corrects:` [LIT-tmp4zb0l](../literature.d/LIT-tmp4zb0l.md). It is the primary source
for [SOTA-tmph4wug](../practices.d/SOTA-tmph4wug.md), where [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) corroborates from an entirely
different argument: that paper found empirically that the antithetic second
evaluation buys nothing on reasoning because autoregressive regeneration
breaks the pair's shared randomness, while this one proves a leave-one-out
baseline preserves the expected field at half the cost. **Two groups, two
arguments, one instruction** — which is the strongest shape of evidence this
record's consensus axis can record short of adoption.

It does not disturb [LIT-tmp4zb0l](../literature.d/LIT-tmp4zb0l.md)'s throughput result, which is measured and
untouched, nor its Theorem 2, which is asymptotic in parameter dimension while
this correction is about finite rank at finite radius.

## Limitations

Stated: the counterexamples are existence results. From this reading: the
transformer audit is one 0.6B model and a single sub-block; the end-to-end
gains are real but modest and honestly reported as such; and the conservativity
analysis needs global Fourier regularity, which is a device for building
counterexamples rather than a description of a language-model objective.

## Open questions

- **Do the pathologies occur at LLM scale?** The paper builds the instrument
  and does not take the measurement. What would close it: estimating the
  antisymmetric part of the population-field Jacobian during a real run.
- **What radius keeps you in the near-quadratic regime?** The theory says this
  is the governing parameter and offers no procedure for choosing it.
  [LIT-tmp81or2](../literature.d/LIT-tmp81or2.md) reports the same parameter has a two-sided empirical failure
  mode, from the other direction, and neither paper connects the two.
- **Does LOO-ROLL's advantage grow with population size?** The variance
  argument suggests it should, and the experiments are at matched wall time
  rather than across a population sweep.
