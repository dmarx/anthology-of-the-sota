---
status: Read
paper: LIT-tmpx1n54
title: 'Neural Tangent Kernel: Convergence and Generalization in Neural Networks'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
summary: >-
  At infinite width, gradient descent on neural networks behaves identically
  to kernel gradient descent with the NTK. The Jacobian (∂f/∂θ) becomes
  deterministic and constant, so the NTK Θ = J^T J is a fixed PSD matrix. Loss
  decays as e^{-λ_min(Θ) t}. This is the "lazy training" or "kernel regime":
  parameters barely move from initialization, and the network functions as a
  linear model in parameter space.
---
# NOTE-tmp8y014: Neural Tangent Kernel: Convergence and Generalization in Neural Networks

## Contribution

Shows that in the infinite-width limit, the function learned by a neural
network trained with gradient descent converges to a kernel method with a
deterministic kernel called the Neural Tangent Kernel (NTK). The NTK stays
constant throughout training in this limit (no feature learning), turning
the dynamics into a linear ODE in function space. Proves convergence and
characterizes generalization in terms of the NTK's spectrum.

## Key insight

At infinite width, gradient descent on neural networks behaves identically
to kernel gradient descent with the NTK. The Jacobian (∂f/∂θ) becomes
deterministic and constant, so the NTK Θ = J^T J is a fixed PSD matrix. Loss
decays as e^{-λ_min(Θ) t}. This is the "lazy training" or "kernel regime":
parameters barely move from initialization, and the network functions as a
linear model in parameter space. The key limitation for our purposes: NTK
predicts no feature learning. Teacher-student networks must learn features
(they have to identify which directions W* corresponds to), so NTK theory
does not apply to the teacher-student regime with finite width. The T15/T16
gossip experiments operate firmly in the feature-learning (mean-field /
rich) regime, not the kernel regime.

## Assumptions

- Infinite width limit (H → ∞ taken before training)
- Gaussian random initialization with variance 1/H
- Full-batch gradient descent (not SGD)
- Fixed learning rate (η → 0 continuous-time limit)

## Key results

- **Theorem 1.** The NTK converges to a deterministic kernel at
  initialization as H → ∞.
  *Holds when:* Any depth, any smooth activation
- **Theorem 2.** The NTK remains constant throughout training in the
  infinite-width limit.
  *Holds when:* Requires: η = O(1/H), width H → ∞
- **Theorem 3.** For positive-definite NTK, gradient descent achieves zero
  training loss at rate e^{-λ_min t}.
  *Holds when:* Loss is quadratic in function space (least-squares / MSE
  targets)

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Infinite-width networks are equivalent to kernel methods; no feature learning occurs. | strong | Theorem 1+2 (the kernel stays constant) |
| C2 | Generalization is characterized by the NTK's eigenvalue spectrum. | strong | Kernel regression theory |
| C3 | NTK fails to capture feature learning in finite-width networks. | strong | Widely observed empirically; formalized by Chizat & Bach 2020 (lazy vs rich regime) |

## Concepts

- **Neural Tangent Kernel (NTK)** — Θ(x, x') = ∇_θ f(x)^T ∇_θ f(x'); the
  kernel induced by the network's Jacobian. In the infinite-width limit,
  this is deterministic and constant.
- **Kernel regime (lazy training)** — Training regime where parameters
  barely move from initialization; network behaves as a fixed kernel method.
  Achieved at large width or small learning rate.
- **Feature learning (rich) regime** — Training regime where parameters move
  significantly from initialization; the network actually learns to
  represent input features. Not captured by NTK.

## Connections

**Builds on.**

- Neal 1996 (Gaussian process limit of infinite networks) — Neal showed that
  at initialization, infinite-width networks are GPs; Jacot et al. show this
  extends to training dynamics.

**Related.**

- Goldt et al. 2020 (teacher-student ODEs) ([LIT-tmpst0ap](../literature.d/LIT-tmpst0ap.md)) — Goldt's mean-
  field ODEs operate in the feature-learning regime; NTK is the
  complementary kernel-regime theory that breaks down for teacher-student
  learning.

## Recommendations

- **R1** — Do not use NTK theory to analyze two-layer ReLU teacher-student
  networks. The relevant theory is mean-field / McKean-Vlasov ODEs (Mei,
  Rotskoff, Goldt).
  *Topic:* theory selection · *Strength:* strong · *When:* Two-layer networks
  with feature learning (finite width, student must learn teacher's
  features).

## Bearing on the record

Filed as the account the mean-field papers are arguing against rather than
as one this record endorses. The NTK limit says no features are learned; the
mean-field limit says the feature distribution is the whole dynamics. They
are different scalings of the same network, and the record should say so
before it cites either.

## Limitations

- Infinite-width limit: practical finite networks deviate, especially for
  feature-learning tasks.
- Constant NTK assumption fails at practical learning rates and widths.
- Does not model the specialization/alignment dynamics seen in teacher-
  student networks.
- Full-batch GD only; stochastic dynamics require separate analysis.

## Open questions

- At what width does a ReLU network transition from kernel (NTK) to feature-
  learning (mean-field) regime?
- Can the gossip gap be computed analytically in the NTK regime (where it
  should vanish, since averaging is exact for linear models)?
