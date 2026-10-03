---
status: Active
title: 'Neural Ordinary Differential Equations'
version: 1
tags:
- model-architecture
- generative-modeling
- flows-and-transport
date: '2026-10-03'
published: '2018-06-19'
arxiv: '1806.07366'
first_author: 'Chen'
keywords:
- 'neural-ode'
- 'adjoint-sensitivity-method'
- 'continuous-normalizing-flow'
- 'instantaneous-change-of-variables'
- 'latent-ode'
- 'adaptive-ode-solver'
implementations: []
summary: >-
  Chen, Rubanova, Bettencourt and Duvenaud, Toronto and Vector (2018),
  [ARXIV-1806.07366](https://arxiv.org/abs/1806.07366). Parameterize a hidden state's derivative with a network,
  integrate it with a black-box solver, and backpropagate by solving the
  adjoint ODE backwards, at memory constant in depth (§2, Alg. 1). For
  densities, the log-density of a state moving under dz/dt = f obeys
  d log p/dt = −tr(∂f/∂z) (Theorem 1), so a continuous normalizing flow
  needs a trace, not a determinant. The CNF evidence is 2-D toys. An MNIST
  ODE-Net matches a ResNet at 0.42% against 0.41% error.
extended_by:
- LIT-tmpezs1l
---

# LIT-tmp29nh5: Neural Ordinary Differential Equations

Chen, Rubanova, Bettencourt and Duvenaud, University of Toronto and Vector
Institute (2018) — [ARXIV-1806.07366](https://arxiv.org/abs/1806.07366). NeurIPS 2018. Read at v5 (14 Dec 2019).

## Key takeaways

- **Depth becomes integration time** (§1, Eq. 2). A residual update
  h_{t+1} = h_t + f(h_t) is an Euler step. Take the limit and let an
  adaptive ODE solver choose the evaluations. The number of function
  evaluations (NFE) plays the role of depth and grows during training
  (Fig. 3d).
- **The adjoint method gives O(1)-memory gradients through any solver**
  (§2, Eqs. 3–5, Alg. 1, App. B). The adjoint a(t) = ∂L/∂z(t) obeys
  da/dt = −aᵀ∂f/∂z. One backward solve of the augmented state [z, a, ∂L/∂θ]
  returns every gradient using vector-Jacobian products, without storing the
  forward pass. On the trained MNIST model the backward pass used about
  half the forward pass's NFE (Fig. 3c).
- **The instantaneous change of variables** (§4, Theorem 1, App. A). For a
  state moving under a Lipschitz field, ∂log p(z(t))/∂t = −tr(∂f/∂z(t)).
  The trace is linear, so a field that is a sum of M terms costs O(M) rather
  than O(M³) (Eq. 10), and the field need not be bijective itself: unique
  ODE solutions make the map invertible. App. A.2 relates it to the
  Liouville equation, the zero-diffusion case of Fokker–Planck.
- **MNIST** (Table 1). Test error 0.42% for the ODE-Net with 0.22M parameters,
  0.41% for a ResNet with 0.60M, 0.47% for the same network
  backpropagated through a Runge–Kutta integrator.
- **Latent ODE for irregular time series** (§5, Table 2). An RNN encoder
  infers z(t₀), an ODE carries it to arbitrary observation times, trained as
  a VAE. On noisy 2-D spirals predictive RMSE is 0.1642, 0.1502 and 0.1346
  at 30, 50 and 100 of 100 points, against an RNN's 0.3937, 0.3202 and
  0.1813.
- **Tolerance trades accuracy for speed after training** (§3, Fig. 3a–b).
  Forward time is proportional to NFE, and the paper suggests training at
  high accuracy and evaluating at lower. Classification and density runs
  used tolerances of 1e-3 and 1e-5 "without degrading performance" (§6).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The CNF is demonstrated only in two dimensions** (§4.1, Figs. 4–5).
  Density matching to known 2-D targets and maximum likelihood on Two
  Circles and Two Moons, with planar-flow dynamics throughout (App. A.1).
  No image or tabular likelihood is reported. FFJORD ([LIT-tmpezs1l](LIT-tmpezs1l.md)) is the
  paper that takes the CNF to data.
- **The CNF-against-NF comparison is not matched** (§4.1). The CNF trains
  10,000 iterations with Adam. The planar NF trains 500,000 with RMSprop, as
  in Rezende and Mohamed. The loss comparison (Fig. 4d) is in loss units
  read off a plot.
- **The parameter-efficiency claim was withdrawn.** The acknowledgements
  thank a reader "for pointing out an unsupported claim about parameter
  efficiency". Table 1 still shows 0.22M against 0.60M, but the ODE-Net's
  cost is in function evaluations, which the table writes as O(L̃) and does
  not count.
- **Minibatching couples the error control** (§6). A batched solve controls
  error jointly, so in principle needs more evaluations than per-example
  solves. The paper says "in practice the number of evaluations did not
  increase substantially" and gives no number.
- **Reverse reconstruction can drift** (§6). Recomputing z(t) backwards can
  diverge from the forward trajectory. The paper "informally checked" that
  reversing CNFs recovered the initial states.

## Which comparisons are like for like

- **MNIST (Table 1)**: ResNet, RK-Net and ODE-Net share the downsampling
  stem and differ only in the six residual blocks or their replacement.
  Error rates are single numbers with no seeds. The 1-layer MLP row is
  LeCun et al.'s.
- **Latent ODE against RNN (Table 2)**: the baseline is a 25-unit RNN, also
  run with time differences concatenated to its inputs; the table gives one
  RNN row, and the text does not say which variant it is.
- **CNF against NF (Fig. 4)**: different optimizers and iteration counts, as
  above.

## Standing in the anthology

The record holds it for the continuous normalizing flow, which is the object
flow matching trains. Flow Matching ([LIT-630](LIT-630.md)) trains a CNF without
simulation, by regressing a velocity field. The stochastic-interpolant paper
([LIT-644](LIT-644.md)) builds a normalizing flow the same way, and measures FFJORD's
per-epoch cost against its own. Theorem 1 is how any of
them computes an exact likelihood at test time. The training method is what
changed: this paper and FFJORD integrate the ODE inside every training step,
and the simulation-free objectives exist to avoid exactly that.

FFJORD ([LIT-tmpezs1l](LIT-tmpezs1l.md)) extends it. It replaces the exact trace, O(D²) for an
unrestricted network, with Hutchinson's unbiased estimator, and runs the
adjoint method on GPU solvers at image scale.

Its other half — the ODE as a layer, trained by the adjoint — is a model
architecture with no practice in the record. The memory claim holds; the
cost moved from memory to function evaluations, which this paper reports
growing through training and FFJORD later calls "prohibitive".

Filed without a `NOTE`: the takeaways come from one full reading of v5,
appendices included, done for this filing. The proofs of Theorem 1 and the
adjoint (Apps. A–B) were followed but not checked line by line.
