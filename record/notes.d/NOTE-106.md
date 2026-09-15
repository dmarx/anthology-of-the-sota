---
number: 106
status: Read
formerly:
- NOTE-tmp8fnry
paper: LIT-305
title: 'A Bayesian Perspective on Generalization and Stochastic Gradient Descent'
version: 1
tags:
- training-optimization
date: '2026-09-15'
summary: >-
  SGD implicitly samples from a Bayesian posterior over parameters, and the
  effective "temperature" of that posterior is controlled by the noise scale g
  = εN/B. Increasing batch size B while holding ε fixed cools the posterior,
  biasing the optimizer toward sharper, less-generalizing minima.
---
# NOTE-106: A Bayesian Perspective on Generalization and Stochastic Gradient Descent

## Contribution

The paper provides a Bayesian framework unifying why SGD generalizes well
and why large-batch training hurts generalization. It identifies a noise
scale g ≈ εN/B governing SGD dynamics, derives the scaling law B_opt ∝ εN
(and B_opt ∝ 1/(1-m) with momentum m), and empirically confirms that the
optimal batch size shifts linearly with learning rate and training set size.
The Bayesian evidence (cost + Occam factor penalizing sharp minima) is shown
to track test performance better than the training loss alone.

## Key insight

SGD implicitly samples from a Bayesian posterior over parameters, and the
effective "temperature" of that posterior is controlled by the noise scale g
= εN/B. Increasing batch size B while holding ε fixed cools the posterior,
biasing the optimizer toward sharper, less-generalizing minima. Batch size
and learning rate are therefore not independent hyperparameters — they are
coupled through this noise scale, and the ratio ε/B is what actually matters
for generalization.

## Assumptions

- Mini-batch gradient noise is approximately Gaussian (CLT assumption); this
  holds for sufficiently large B but may fail for very small batches or
  heavy-tailed gradient distributions.
- The loss surface near a minimum is locally quadratic, enabling the Laplace
  approximation to the posterior; deep network loss surfaces may violate
  this significantly.
- The SDE discretization error (from using finite learning rate ε) is small
  relative to the noise scale g; this requires ε to be below some task-
  specific threshold.
- The stationary distribution of the SDE approximation is the Bayesian
  posterior P(ω) ∝ exp(-C(ω)); this holds exactly only when the SDE is in
  stationarity and discretization error is negligible.
- The noise scale g = εN/B is the sufficient statistic for generalization
  performance; other hyperparameters (batch order, data augmentation,
  dropout) are treated as secondary.
- The Hessian eigenvalues at the minimum are the correct measure of
  sharpness; this ignores non-quadratic loss geometry farther from the
  minimum.

## Key results

- **Noise scale and optimal batch size (Sections 2-3).** The noise scale g =
  εN/B governs the SGD posterior temperature. The optimal batch size
  maximizing test accuracy satisfies B_opt ∝ εN. With momentum m, B_opt ∝
  εN/(1-m). Empirically confirmed on MNIST with linear trends in Figures 5b,
  6b, and 7b.
  *Holds when:* Validated on a shallow 800-unit ReLU network on MNIST with
  batch sizes 1–1000 and learning rates 0.01–3. Deep network validation is
  qualitative only.
- **Bayesian evidence predicts generalization (Section 2).** Log Bayesian
  evidence = -[training cost + (1/2) Σᵢ log(λᵢ/λ)] tracks test cross-entropy
  and correctly identifies the optimal regularization strength, including on
  randomly-labeled data.
  *Holds when:* Demonstrated for logistic regression on MNIST (Figure 2).
  Qualitatively consistent with deep network experiments from Krueger et al.
  (2017).
- **LR decay = batch size increase equivalence (Section 4).** Decaying the
  learning rate by factor α is equivalent to multiplying batch size by 1/α
  under the noise scale framework. Both operations reduce g by the same
  factor, producing the same posterior temperature trajectory.
  *Holds when:* Derived analytically from g = εN/B; directly verified in
  follow-up paper (Smith et al. 2017, Don't Decay the LR).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The Bayesian evidence (cost function + Occam factor penalizing curvature) is strongly correlated with test set performance and correctly predicts whether a model will generalize, even on randomly labeled data. | strong | Demonstrated quantitatively in logistic regression on MNIST: log evidence ratio tracks test cross-entropy with minima at the same regularization strength (Figure 2). Also qualitatively consistent with Krueger et al. (2017) showing Hessian eigenvalue increases on random labels in deep networks. |
| C2 | There is an optimal batch size B_opt that maximizes test accuracy; test accuracy falls both below (training instability) and above (sharp minima) this optimum. | strong | Empirically demonstrated on a shallow 800-hidden-unit ReLU network trained on MNIST (Figure 4b), sweeping batch sizes from 1 to 1000 at fixed learning rate ε=1. |
| C3 | The optimal batch size scales linearly with the learning rate: B_opt ∝ ε. | strong | Confirmed empirically across multiple learning rates (Figure 5); linear trend is clearly visible in Figure 5b. Derived analytically from the SDE noise scale g = εN/B: holding g fixed requires B ∝ ε. |
| C4 | The optimal batch size scales linearly with training set size: B_opt ∝ N. | strong | Empirically confirmed by varying training set size (Figure 6b) at fixed ε=1, observing a clear linear trend between N and the best observed batch size. |
| C5 | With momentum coefficient m, the noise scale becomes g ≈ εN / [B(1-m)], implying B_opt ∝ 1/(1-m). | strong | Derived by modeling SGD with momentum as a second-order SDE (Appendix D) and verified empirically in Figure 7b with "remarkably good agreement" to the scaling rule. |
| C6 | L2 regularization significantly reduces the generalization gap between small-batch and large-batch training. | moderate | Shown in Appendix B (Figure 8): with λ=0.1, the generalization gap shrinks considerably relative to the unregularized case, and test cross-entropy no longer degrades after many gradient steps. |

## Method

**Stochastic Differential Equation (SDE) Analysis of SGD + Bayesian Evidence
Framework.**

1. Model the SGD parameter update as the discretization of an Itô SDE: dω/dt
= -dC/dω + η(t), where η(t) is Gaussian white noise. 2. Identify the noise
covariance: the mini-batch gradient error α = (d̂C/dω - dC/dω) is
approximated as Gaussian by the CLT, with variance ∝ ε²(N/B - 1)/N ≈ εg/N,
giving noise scale g ≈ εN/B. 3. The stationary distribution of this SDE is
P(ω) ∝ exp(-C(ω)), i.e., the Bayesian posterior (Langevin dynamics), meaning
SGD naturally samples broad minima. 4. To maximize test accuracy, hold g
fixed when changing ε or N, yielding B_opt ∝ εN. 5. For SGD with momentum,
model as a second-order SDE (Appendix D) to derive g ≈ εN / [B(1-m)], giving
the additional rule B_opt ∝ 1/(1-m). 6. Validate all scaling rules
empirically on MNIST with a shallow ReLU network.

- Noise scale g = εN/B (or εN/[B(1-m)] with momentum): the single parameter
  governing generalization
- Bayesian evidence = exp(-E(ω₀)) where E = cost + Occam factor; Occam
  factor = Σ log(λᵢ/λ) over Hessian eigenvalues
- Laplace approximation to the posterior for computing the Occam factor
- SDE / Langevin dynamics interpretation mapping SGD noise to posterior
  temperature
- Empirical batch-size sweep on MNIST shallow network to locate B_opt

## Concepts

- **noise scale (g)** — g = ε(N/B - 1) ≈ εN/B, where ε is the learning rate,
  N is training set size, and B is batch size. It characterizes the
  amplitude of the stochastic noise injected by mini-batch sampling and is
  the key determinant of which minima SGD finds.
- **Bayesian evidence** — P(y|x; M), the marginal likelihood of the data
  under model M. Under the Laplace approximation, log evidence ≈ -E(ω₀) =
  -[cost(ω₀) + Occam factor], where the Occam factor = (1/2) Σᵢ log(λᵢ/λ)
  penalizes sharp minima (large Hessian eigenvalues λᵢ) relative to the
  prior width λ.
- **Occam factor** — The term in the Bayesian evidence that penalizes model
  complexity; under the Laplace approximation it equals (1/2) Σᵢ log(λᵢ/λ),
  where λᵢ are Hessian eigenvalues and λ is the prior precision. It favors
  broad minima over sharp ones and is invariant to model reparameterization
  (unlike raw curvature).
- **generalization gap** — In this paper specifically: the drop in test
  accuracy observed when the batch size is increased while holding all other
  hyperparameters fixed. Not the train-test accuracy gap.
- **optimal batch size (B_opt)** — The batch size that maximizes test set
  accuracy at a given learning rate and training set size. Scales as B_opt ∝
  εN (or B_opt ∝ εN/(1-m) with momentum m). Below this size training is
  unstable; above it the posterior cools and sharp minima dominate.
- **posterior temperature** — Implicit concept: the noise scale g plays the
  role of temperature in the Langevin/Bayesian posterior. High g (small B,
  large ε) = hot posterior = broad exploration; low g (large B, small ε) =
  cold posterior = convergence to sharper, potentially worse minima.

## Connections

**Builds on.**

- Bayesian Learning via Stochastic Gradient Langevin Dynamics (Welling &
  Teh, 2011) — Foundational paper showing that adding isotropic Gaussian
  noise to SGD gradients yields approximate Bayesian posterior sampling.
  Smith & Le show that ordinary SGD mini-batch noise already achieves a
  similar effect without explicit noise injection.
- On Large-Batch Training for Deep Learning: Generalization Gap and Sharp
  Minima (Keskar et al., 2016) — Empirically established the generalization
  gap phenomenon. Smith & Le provide the Bayesian theoretical explanation
  for why it occurs.
- Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour (Goyal et al.,
  2017) — Observed the linear scaling rule B ∝ ε empirically in ResNets.
  Smith & Le derive this rule theoretically from the SDE noise scale
  argument.
- Understanding Deep Learning Requires Rethinking Generalization (Zhang et
  al., 2016) — Motivating empirical puzzle (memorization of random labels).
  Smith & Le replicate it in linear models and explain it via Bayesian
  evidence.

**Related.**

- Don't Decay the Learning Rate, Increase the Batch Size (Smith et al.,
  2017) — Direct follow-up by the same first author showing that learning
  rate decay and batch size increase are equivalent operations under the
  noise scale framework.

## Recommendations

- **R1** — When scaling to larger batch sizes for parallelism, increase the
  learning rate proportionally (ε ∝ B) to maintain the same noise scale g =
  εN/B and preserve generalization performance.
  *Topic:* batch size / learning rate scaling · *Strength:* strong · *When:*
  Applies when retraining a fixed model with more GPUs. Valid up to learning
  rates where discretization error dominates (empirically ε ~ 3 in the
  paper's normalized units).
- **R2** — When increasing the momentum coefficient m, also increase the
  batch size proportionally as B ∝ 1/(1-m) to keep the effective noise scale
  constant.
  *Topic:* momentum / batch size coupling · *Strength:* moderate · *When:*
  Applies to SGD with momentum. The paper verifies this empirically but only
  on MNIST shallow networks; deep network validation is limited.
- **R3** — Use the heuristic from Appendix E: start at ε=0.1, m=0.9, sweep
  batch size on log scale to find B_opt, then successively increase B by 3×
  while scaling ε ∝ B, then (1-m) ∝ 1/B, until accuracy drops or hardware
  limits are hit.
  *Topic:* hyperparameter tuning procedure · *Strength:* moderate · *When:* Only
  worthwhile if the model will be retrained many times (amortizing the
  tuning cost).
- **R4** — Use Bayesian evidence (or its proxy, the Hessian trace/largest
  eigenvalue) as a model selection criterion alongside training loss,
  particularly when evaluating whether a model trained on a new dataset will
  generalize.
  *Topic:* model evaluation / generalization prediction · *Strength:* moderate ·
  *When:* Practically computable only for small models (linear, shallow
  networks) where Hessian is tractable. Qualitatively useful as intuition
  for deep networks.

## Bearing on the record

The noise scale `g = eps*N/B` is the same quantity the record's gradient-
noise-scale practice measures, reached two months earlier and from a
Bayesian argument rather than an empirical one. That the two lines converged
on one statistic, independently, is the strongest thing this reading says
about the record.

## Limitations

- The SDE / Langevin analogy assumes Gaussian mini-batch gradient noise.
  This holds approximately by the CLT but fails for sparse gradients, very
  small batches, or heavy-tailed gradient distributions.
- The Bayesian evidence is computed via Laplace approximation, which
  requires the Hessian. This is intractable for large neural networks
  (millions to billions of parameters), so the theory is validated primarily
  on small/linear models.
- Neural networks have exponentially many equivalent minima (permutation
  symmetry of hidden units), making the evidence computation require careful
  accounting of degeneracy — not addressed in full generality.
- The paper does not account for learning rate schedules or batch size warm-
  up strategies that are standard in practice (cosine decay, linear warm-
  up). The analysis assumes a constant learning rate.
- The optimal batch size result and scaling rules are validated on MNIST
  with shallow networks. Generalization to very deep networks on large
  datasets (ImageNet scale) is assumed but not directly verified in this
  paper.
- The analysis treats all minima as having roughly isotropic curvature for
  the SDE approximation. Anisotropic curvature (common in deep networks) may
  alter the noise scale dynamics.

## Open questions

- Is there a single universal noise scale g* that is optimal across all
  architectures and datasets, or does g_opt vary substantially across
  problem settings?
- How does the noise scale framework interact with adaptive optimizers
  (Adam, RMSProp)? Those methods implicitly rescale gradients in a
  parameter-dependent way that changes the effective noise covariance.
- Can the Bayesian evidence be efficiently approximated in large networks
  (e.g., via stochastic trace estimators for the Hessian) to make the
  generalization prediction practically useful?
- The paper shows L2 regularization reduces the generalization gap. Can
  regularization fully substitute for small-batch noise, enabling large-
  batch training without quality loss?
- How does the noise scale interact with data augmentation, dropout, or
  other implicit regularizers that also inject stochasticity?
