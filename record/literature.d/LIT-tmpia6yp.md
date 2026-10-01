---
status: Active
title: 'Rigorous dynamical mean field theory for stochastic gradient descent methods'
version: 1
tags:
- training-optimization
- analysis-and-evaluation
date: '2026-10-01'
published: '2022-10-12'
arxiv: '2210.06591'
first_author: 'Gerbelot'
keywords:
- 'dynamical-mean-field-theory'
- 'stochastic-gradient-descent'
- 'high-dimensional-asymptotics'
- 'empirical-risk-minimization'
- 'momentum'
- 'teacher-student'
implementations:
- 'SPOC-group/Rigorous-dynamical-mean-field-theory'
summary: >-
  Gerbelot et al. (2022), [ARXIV-2210.06591](https://arxiv.org/abs/2210.06591) — a proof that the discrete-time
  dynamical mean-field equations of statistical physics are exact for a
  family of first-order methods (multi-pass SGD, heavy-ball and Nesterov
  momentum, Langevin noise, learning-rate schedules) learning a shallow
  estimator on Gaussian data, in the limit where samples and dimension grow
  together and the mini-batch is a fixed fraction of the data. On a
  teacher-student perceptron the solved equations match simulation at
  d = 1000 across learning rates and batch fractions.
---

# LIT-tmpia6yp: Rigorous dynamical mean field theory for stochastic gradient descent methods

Gerbelot et al. (2022) — [ARXIV-2210.06591](https://arxiv.org/abs/2210.06591)

## Key takeaways

- **What is proved.** Closed-form equations for the exact high-dimensional
  asymptotics of a generic family of discrete-time first-order iterations,
  learning an estimator (an M-estimator, a shallow network with a finite
  number `q` of hidden units) by empirical risk minimization on Gaussian
  data. Samples `n` and dimension `d` go to infinity together; `q` stays
  finite. The equations coincide with a discretization of the dynamical
  mean-field theory (DMFT) physicists derive for gradient flow.
- **What the family covers.** Multi-pass SGD with mini-batches modelled as
  independent Bernoulli selections — so the batch must be a **finite
  fraction of the dataset**, not a constant number of examples; heavy-ball
  and Nesterov momentum; time-dependent updates including learning-rate
  schedules and thermal (Langevin) noise; any differentiable regularizer;
  and, through non-separable update functions, data with a generic
  well-conditioned covariance rather than identity.
- **What is new against the prior rigorous result** (Celentano et al.,
  reference 11 in the paper): stochasticity of the algorithm and non-identity
  data covariance, by a different proof — iterative Gaussian conditioning
  rather than a mapping onto approximate message passing — which also shows
  explicitly how the memory kernels of the effective dynamics build up.
  The paper treats discrete time only, arguing that is what algorithms run.
- **Numerics**: for a teacher-student perceptron with ridge regularization,
  the cosine similarity to the teacher (which fixes the generalization error
  in that model) from the solved equations agrees with SGD simulations at
  `d = 1000`, across learning rates and batch fractions.
- **Limits it states**: the solver is stable only to relatively short
  times, a long-standing problem for DMFT; the data covariance cannot change
  during training, so a learned feature map is outside it; and extracting
  simple governing quantities from the equations is left open.

## Standing in the anthology

**A different exact limit from the ones the record holds.** [THEORY-009](../theory.d/THEORY-009.md),
from [LIT-271](LIT-271.md) and its neighbours, is also a "mean-field" account of SGD, but
of another limit: width goes to infinity and the object that moves is the
distribution of neurons. Here width stays finite and it is the number of
samples and the dimension that grow. [LIT-454](LIT-454.md) derives SGD's limiting
dynamics as a Langevin equation, with an exact Ornstein–Uhlenbeck solution
for linear regression. Neither connects to this paper's equations, and the
record has no document that uses DMFT.

**It does not bear on the optimizer cluster.** [SOTA-121](../practices.d/SOTA-121.md), [SOTA-165](../practices.d/SOTA-165.md) and the
theory around them concern matrix preconditioners on deep networks at scale.
This paper covers first-order iterations with a scalar step size and
momentum on Gaussian data and shallow models; whether its non-separable
update functions could express a matrix preconditioner is not something it
discusses. Its relation to the record's batch-size material ([SOTA-198](../practices.d/SOTA-198.md),
[LIT-058](LIT-058.md)) is that batch size enters as a fraction of the dataset, which is
not the regime those practices are about.

Filed as a seed: the rigorous end of SGD-dynamics theory, for when the
record has a claim about high-dimensional training dynamics that it could
test.

Unread — no NOTE.
