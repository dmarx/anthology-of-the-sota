---
number: 181
status: Read
formerly:
- NOTE-tmptzfh5
paper: LIT-403
title: 'Understanding Black-box Predictions via Influence Functions'
version: 1
date: '2026-09-17'
summary: >-
  Traces a prediction back to the training points responsible for it by
  upweighting each point infinitesimally and differentiating, which needs only
  gradients and Hessian-vector products rather than retraining. Establishes
  the four uses of training-data attribution — explanation, poisoning,
  domain-mismatch debugging, and finding mislabelled data.
---

# NOTE-181: Understanding Black-box Predictions via Influence Functions

<!-- inactive-ok-file: SOTA-246, THEORY-017 — the practice and
     the (Rejected) explanation this reading files. The Rejected theory is this paper's own
     account, so it is the correct target. -->

## Contribution

Before this, "which training data is responsible for this prediction?" was a
question you answered by retraining without the data, which nobody does. This
paper makes it a computation on the trained model.

The move is to replace deletion with infinitesimal upweighting. Perturb the
weight on a training point `z` by `ε`, differentiate the resulting parameters
with respect to `ε` at zero, and chain through to the test loss. The result is
`I(z, z_test) = −∇L(z_test, θ̂)ᵀ H_θ̂⁻¹ ∇L(z, θ̂)` — the alignment of the two
gradients, measured in the geometry the Hessian defines.

## Key insight

**Attribution is a gradient alignment, warped by curvature.** A training point
matters to a test point to the extent their loss gradients agree, and the
inverse Hessian is what converts "agree" from a naive dot product into
something that accounts for how the parameters actually move.

The engineering insight that made it usable is separate and just as
important: **you never need the Hessian, only products with it.** A
Hessian-vector product costs about a gradient, so both offered
solvers — conjugate gradients and the stochastic estimator — turn an
`O(p²)` object into a sequence of `O(p)` operations.

## Assumptions

- The empirical risk is **twice-differentiable and strictly convex** in the
  parameters, and `θ̂` is the global minimizer. Both are relaxed
  experimentally in §4 and neither holds for a trained neural network.
- Under non-convergence and non-convexity the paper substitutes a damped
  convex quadratic approximation `H + λI` around the parameters actually
  obtained. The damping is a hyperparameter tuned so the expansion converges.
- **Non-differentiability is not survivable by that route.** The hinge loss
  experiment is the honest negative result.
- The scaling of the loss must satisfy `∇²L ⪯ I` for the stochastic estimator;
  where no bound is available it is tuned.

## Key results

- **Influence matches leave-one-out retraining** on 10-class MNIST: for the
  500 most influential training points, the predicted change tracks the
  measured change from removing and retraining. *This is the validation that
  later work restricts to the convex case.*
- **The stochastic estimator is cheap and robust.** Accurate with `r = 10`
  repeats and `t = 5,000` iterations; `H⁻¹v` was estimated without visiting
  every one of the 55,000 points. Even `r = 1` identified the most influential
  points, more noisily.
- **Same predictions, different mechanism.** Inception v3 (lower layers
  frozen) and an RBF-SVM on a 900-per-class dog-versus-fish ImageNet subset.
  SVM influence varies inversely with raw pixel distance — a soft nearest
  neighbour. Inception's does not, and its **fifth most helpful image for
  classifying a fish was a dog**.
- **Training-set attacks are the same computation.** Visually
  indistinguishable perturbations, mathematically equivalent to prior
  gradient-based poisoning. The most influential example was the most
  ambiguous one — an image containing both a dog and a fish, the model's
  lowest-confidence training point at 77% against a next-lowest of 90%.
- **Domain mismatch, localized.** In a hospital-readmission model, four
  training children were each **30–40× as influential** as the next most
  influential example; the one child not readmitted had strongly positive
  influence and the other three strongly negative.
- **Dataset repair.** Enron1 spam, 4,147 training examples, logistic
  regression on bag-of-words, 10% of labels flipped. Inspecting points in
  influence order repaired the dataset after checking fewer points than
  ordering by highest training loss, or at random — 40 repeats, no access to
  test data.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Influence functions predict the effect of removing a training point and retraining | strong **for convex models** | derived, and matched against retraining on MNIST |
| C2 | The approximation remains informative on non-convex, non-converged models | moderate | damped-quadratic argument plus experiments |
| C3 | It breaks on non-differentiable losses unless smoothed | strong | the hinge-loss experiment, a negative result |
| C4 | Influence reveals mechanism where predictions do not | moderate | the Inception/SVM comparison, one task |
| C5 | Influence-prioritized inspection repairs a mislabelled dataset faster than loss-ordering | moderate | one dataset, one model class, 40 repeats |
| C6 | The same computation constructs training-set attacks | strong | demonstrated, and equivalent to known attacks |

## Method

Compute `∇L(z_test, θ̂)`, solve for `s_test = H⁻¹∇L(z_test, θ̂)` by conjugate
gradients or stochastic estimation, then take `−s_testᵀ∇L(z, θ̂)` for every
training point. For self-influence set `z_test = z`.

## Concepts

- **Upweighting instead of deletion** — the substitution that makes the
  counterfactual differentiable.
- **Hessian-vector products as the unit of cost** — why an `O(p²)` object
  never has to be built.
- **Helpful and harmful** — the paper's terms for positive and negative
  influence, later renamed to proponents and opponents by [LIT-400](../literature.d/LIT-400.md) on the
  grounds that the originals prejudge the finding.
- **Explanation and attack as one computation** — an uncomfortable identity
  that recurs whenever a method can say what would change a model.

## Connections

The direct descendants are [LIT-400](../literature.d/LIT-400.md), which replaces the Hessian with a
trace over checkpoints, and [LIT-401](../literature.d/LIT-401.md), which keeps the Hessian and
approximates it well enough to reach 52B parameters. They are genuine
alternatives rather than a succession: one needs the training run's
checkpoints, the other needs only the final model.

[LIT-402](../literature.d/LIT-402.md) is the correction, and it is a correction to C1 specifically
rather than to the method.

## Recommendations

- **R1** — Find mislabelled training data by influence rather than by
  training loss. *Topic:* data pipeline. *Strength:* moderate.
- **R2** — When two models agree, compare what they are relying on before
  concluding they work the same way. *Strength:* moderate, and general.
- **R3** — Treat the magnitude of achievable influence as a measure of
  exposure to data poisoning. *Strength:* moderate.
- **R4** — Smooth a non-differentiable loss before computing influences.
  *Strength:* strong, and narrow.

## Bearing on the record

Sources [SOTA-246](../practices.d/SOTA-246.md) (R1), corroborated by [LIT-400](../literature.d/LIT-400.md).

It also states [THEORY-017](../theory.d/THEORY-017.md), which is the account of what the estimate
*measures* — filed separately because the record keeps explanations apart from
recommendations ([ADR-031](../decisions.d/ADR-031.md)), and because this particular explanation was
corrected while the practice built on it was not.

R2, R3 and R4 are not filed. R4 is algorithm-local in [ADR-041](../decisions.d/ADR-041.md)'s sense — it
belongs to whoever is implementing influence functions on a hinge loss, and
this note is where they would find it. R3 is real and the record holds nothing
about adversarial data at all, which makes it a topic rather than a gap this
reading can close. R2 is a good habit, and the honest statement of its support
is one comparison on one task.

## Limitations

- The theory is convex; every model anyone wants to use is not.
- Every experiment is small: MNIST, a 1,800-image ImageNet subset, a
  4,147-document spam corpus, one clinical dataset.
- The Inception experiment freezes all but the top layer, so it is attribution
  for a linear model on fixed features.
- C1 is the claim that did not survive — see [THEORY-018](../theory.d/THEORY-018.md).

## Open questions

- The paper's own framing — "how would the model change if this point were
  removed" — turns out not to be what the estimate answers for neural
  networks. Which of the four use cases survive that? [LIT-402](../literature.d/LIT-402.md) answers
  this directly and in the affirmative for two of them.
