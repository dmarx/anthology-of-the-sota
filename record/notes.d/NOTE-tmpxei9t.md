---
status: Read
paper: LIT-tmp5pttj
title: 'Dropout as a Bayesian approximation'
version: 1
date: '2026-09-25'
summary: >-
  Dropout before every weight layer, with L2, is shown to optimize (up to an
  approximated KL term) a variational objective for a deep Gaussian process,
  so running T stochastic forward passes at test time yields a predictive
  mean and variance for free. The evidence is qualitative figures, a UCI
  regression table on 50-unit one-layer networks, and one RL run; the
  MC-versus-weight-scaling comparison is stated without numbers.
---

# NOTE-tmpxei9t: Dropout as a Bayesian approximation

## Contribution

A derivation that recasts the standard dropout-plus-weight-decay objective as
approximate variational inference, and from it a test-time procedure. That
procedure is MC dropout: keep dropout on, sample `T` passes, and read off a mean
and a variance. The model and its training are unchanged, so any existing
dropout network gains an uncertainty estimate.

## Key insight

The random masks of dropout are samples from an approximate posterior over
weights. Averaging over them at test time, instead of collapsing them into
one scaled pass, is integrating over that posterior, and how much the passes
disagree is the model's uncertainty. A softmax output is a point estimate
passed through a squashing function, and it is not that.

## Assumptions

- Dropout applied **before every weight layer**. The paper says this matches
  practice, but many networks, the LeNet here included, drop only before some
  layers.
- L2 weight decay `λ` on weights and biases. The prior length-scale `l` and
  precision `τ` are then tied by `τ = p l² / (2Nλ)`.
- A deep-GP covariance `K(x, y) = ∫ p(w)p(b) σ(wᵀx + b) σ(wᵀy + b) dw db`,
  approximated through a finite-rank spectral decomposition. The
  nonlinearity decides which GP is approximated.
- The KL between the Bernoulli-mixture variational distribution and the prior
  is **approximated** (appendix §4.2), and the likelihood term uses a single
  Monte Carlo sample per data point.
- The full derivation is in arXiv 1506.02157, which this reading did not
  cover.

## Key results

- **Eq. 4.** `L_GP-MC ∝ (1/N) Σ −log p(yₙ | xₙ, ω̂ₙ)/τ + Σᵢ (pᵢl²/2τN)‖Mᵢ‖² + (l²/2τN)‖mᵢ‖²`.
  This equals the dropout objective (Eq. 1) for a suitable `τ` and `l`.
- **Eq. 6–8.** Predictive mean ≈ `(1/T) Σₜ ŷ(x, Wᵗ)`. Predictive variance ≈
  `τ⁻¹I + (1/T) Σₜ ŷᵗᵀŷᵗ − E[y]ᵀE[y]`. Predictive log-likelihood is a
  log-sum-exp over the `T` passes.
- **Table 1 (UCI, 20 splits).** Log-likelihood beats PBP and VI on all 10
  datasets. RMSE is better on 7, tied on Kin8nm and Naval, and worse than PBP
  on Yacht (1.11 against 1.02). Boston: RMSE 2.97 ± 0.19 against PBP 3.01 ±
  0.18, LL −2.46 against −2.57.
- **Table 2 (v6 addendum).** 10× more epochs, or a second hidden layer,
  improves every dataset further. Energy RMSE, for example, goes 1.66 → 1.09 →
  0.47.
- **Boston at `p = 0`:** RMSE 3.07 and LL −2.59, against 2.97 and −2.46 with
  dropout 0.05 or 0.005.
- **RL:** reward above 1 after 25 batches with Thompson sampling, against 175
  with ε-greedy.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The dropout + L2 objective is, for matched `τ` and `l`, a variational objective for a deep GP | moderate | Derivation summarized in §3; relies on an approximated KL term and on the appendix paper, not read here |
| C2 | T stochastic passes give a usable predictive mean and variance with no change to the model | moderate | Eq. 6–8; qualitative CO₂ and MNIST figures; T = 10 "reasonable" in Fig. 3 |
| C3 | MC dropout's uncertainty is better than PBP's and VI's on UCI regression | moderate | Table 1 log-likelihood, 20 splits; tiny networks, `τ` tuned by BO on validation LL, 10× PBP's epochs |
| C4 | MC averaging beats weight scaling at test time | weak | One sentence, "we observed an improvement", with no numbers |
| C5 | Dropout uncertainty speeds exploration in RL through Thompson sampling | weak | One run, one environment, one plot |
| C6 | ReLU and TanH networks give qualitatively different uncertainty far from the data | moderate | Fig. 2c/2d, explained through the covariance functions each nonlinearity approximates |

## Method

Train a standard dropout network with weight decay. At test time keep the
Bernoulli masks active, run `T` forward passes, and take their mean as the
prediction. For regression, add `τ⁻¹` to the sample variance. For
classification, use the entropy or variation ratio of the sampled
predictions. `τ` comes from Eq. 7 or, as in the UCI experiments, from
Bayesian optimization on validation log-likelihood.

## Concepts

- **MC dropout** — the paper's name for the Monte Carlo estimate of the
  predictive mean: the average of `T` stochastic forward passes.
- **Standard dropout** — weight scaling by `p` at test time, which the paper
  treats as an approximation to MC dropout.
- **Model precision `τ`** — the observation-noise precision, fixed by
  `p`, `l`, `N` and `λ`.

## Connections

It builds on Srivastava et al. ([LIT-395](../literature.d/LIT-395.md)), whose §7.5 had already compared
Monte Carlo averaging with weight scaling empirically, and on the
infinite-width network–GP correspondence (Neal, Williams). It cites Wang and
Manning and Maeda as earlier Bayesian readings of dropout. Its comparison
methods, PBP and Graves' VI, are not in the record.

## Recommendations

- **R1** — To get predictive uncertainty from an existing dropout network,
  keep dropout on at test time and average T passes, where T of order 10 is
  enough for a rough estimate. *Topic:* analysis-and-evaluation. *Status:*
  standard. *Strength:* moderate. *Applies when:* the network already has
  dropout before its weight layers, and the extra forward passes are
  affordable.
- **R2** — Don't read a softmax output as model confidence. *Topic:*
  analysis-and-evaluation. *Status:* standard. *Strength:* moderate, since the
  argument is sound and the demonstration is one MNIST digit.

## Bearing on the record

- **No practice is filed from this reading.** R1 is a real instruction, but
  this paper compares MC dropout only against two Bayesian-NN methods on
  50-unit networks. It does not compare against deep ensembles, and it does not
  measure calibration in the ECE sense. A practice resting on it would need
  that comparison from another paper.
- **[THEORY-016](../theory.d/THEORY-016.md)** and this paper name different targets for the test-time
  average. [THEORY-016](../theory.d/THEORY-016.md) says weight scaling computes the normalized *geometric*
  mean exactly for logistic units. This paper treats the *arithmetic* mean of
  sampled passes as the target, and weight scaling as the approximation. Both
  cite [LIT-395](../literature.d/LIT-395.md) §7.5 as the check that the two agree in practice. The record
  should not treat either as refuting the other. They answer "which average?"
  differently, and no number in either paper depends on the answer.
- **[THEORY-015](../theory.d/THEORY-015.md)** is not affected. This is a third account of what the
  dropout objective *is*, and it does not bear on the data-dependent penalty
  result.
- **[SOTA-240](../practices.d/SOTA-240.md)** is not affected. Nothing here bears on whether to add dropout.

## Limitations

- The benchmark networks are 50 units and one hidden layer, with dropout
  0.05 or 0.005. That is far from the models dropout is usually used in.
- Hyperparameters are tuned on validation log-likelihood, the metric reported,
  and dropout gets 10× the training epochs of the baseline.
- There is no calibration metric, no out-of-distribution detection benchmark,
  and no ensemble baseline.
- The quality of the uncertainty depends on the GP being approximated. The
  CO₂ figure shows that as well-behaved error bars around a wrong mean.

## Open questions

- How does MC dropout's uncertainty compare with a deep ensemble at matched
  compute, on a network of practical size?
- Does the equivalence survive the KL approximation at the dropout rates
  large networks use, 0.1–0.5? The UCI results are all at 0.05 or below.
