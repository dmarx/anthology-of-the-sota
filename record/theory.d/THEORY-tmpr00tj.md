---
status: Active
promote_when: >-
  Active for the three derivations: a Gaussian step has an exact
  likelihood, the whole chain has only a bound, and one trained velocity
  defines a family of SDEs with the ODE's marginals and a closed-form
  per-step KL. What is only illustrated is that the construction survives
  discretization. At the few rollout steps used in practice the SDE's
  samples visibly differ from the ODE's, and the noise schedule used is
  singular at the starting time. It would be narrowed by a measurement of
  how far the discretized SDE's marginals sit from the ODE's at the rollout
  step count, for the fine-tuned model, and whether the gap moves the
  reward. Another RL-tuned flow model that reports a higher benchmark score
  would not bear on it.
title: "A diffusion or flow sampler can be trained by a likelihood-ratio policy gradient only when each step is stochastic with a tractable density, and a same-marginal SDE built from the trained velocity supplies that without changing the marginals"
version: 1
tags:
- adaptation-and-tuning
- generative-modeling
- flows-and-transport
date: '2026-10-03'
source:
- LIT-tmpdktqx
- LIT-tmp7vihu
- LIT-645
explains:
- SOTA-tmp6jbkw
summary: >-
  Black et al. (2023), [LIT-tmp7vihu](../literature.d/LIT-tmp7vihu.md), and Liu et al. (2025), [LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md).
  A policy gradient needs the log-density of each action. Treated as one
  action, a diffusion model's sample has only a variational bound. Treated
  as T actions, each DDPM step is an isotropic Gaussian with an exact
  density. A flow's ODE step is deterministic, so it has no per-step
  density and explores nothing past the initial noise. The stochastic-
  interpolant identity ([LIT-645](../literature.d/LIT-645.md)) gives, for any noise level, an SDE with the
  ODE's marginals, built from the trained velocity alone. Each of its steps
  is Gaussian, so the ratio and the KL to the reference are closed form.
  All of this is derivation. What is not shown is that it survives the
  ten-step discretization used for rollouts.
---

<!-- inactive-ok-file: SOTA-tmp6jbkw — Proposed, and declared in `explains:`; the practice this account underwrites. Explaining a practice not yet in force is the normal case. -->
<!-- inactive-ok-file: SOTA-302, THEORY-054 — Proposed; named to say how this account bears on the distilled-generator case, not cited as support -->

# THEORY-tmpr00tj: A diffusion or flow sampler can be trained by a likelihood-ratio policy gradient only when each step is stochastic with a tractable density, and a same-marginal SDE built from the trained velocity supplies that without changing the marginals

## Source

Black, Janner, Du, Kostrikov and Levine (2023), [LIT-tmp7vihu](../literature.d/LIT-tmp7vihu.md), §4.2–4.3.
Liu et al. (2025), [LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md), §4, Eqs. 6–9, and App. A. Albergo, Boffi
and Vanden-Eijnden (2023), [LIT-645](../literature.d/LIT-645.md), Cors. 10 and 18.

## The account

**A likelihood-ratio gradient needs the action's log-density.** REINFORCE
and PPO estimate the reward gradient as reward times ∇ log π(action). Both
need that density in closed form, and PPO's clipped ratio needs it under
two sets of weights.

**As one action, a diffusion sample has none.** DDPO ([LIT-tmp7vihu](../literature.d/LIT-tmp7vihu.md), §4.2)
casts reward-weighted regression as a one-step MDP whose action is the
final image. The diffusion loss "does not involve an exact log-likelihood",
only a variational bound, so that procedure "is not theoretically
justified". Cast instead as a T-step MDP whose state is (prompt, t, x_t)
and whose action is x_{t−1}, each step of a standard sampler is an isotropic
Gaussian. That "allows for the evaluation of exact log-likelihoods and their
gradients" (§4.3).

**A flow's ODE step is not a policy step.** A flow-matching sampler
integrates dx = v dt, so each step is a deterministic function of the last.
Flow-GRPO ([LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md), §4) names two failures. The ratio needs
p(x_{t−1} | x_t), which "becomes computationally expensive under
deterministic dynamics due to divergence estimation". And there is "no
randomness beyond the initial seed" to explore with. Strictly, a
deterministic step's transition is a point mass, so the per-step ratio is
not defined at all. Only the whole chain's density exists, through the
divergence integral.

**A same-marginal SDE restores the policy without retraining.** The
stochastic-interpolant paper ([LIT-645](../literature.d/LIT-645.md), Cors. 10 and 18) shows that one
learned velocity and score define an ODE and, for every noise level
ε(t) ≥ 0, an SDE with the same marginals, with ε chosen after training.
Flow-GRPO uses that family (Eq. 7, proved in App. A). For the linear path
the score is a function of the velocity, so the SDE needs only the trained
v_θ (Eq. 8). Its Euler–Maruyama step (Eq. 9) is an isotropic Gaussian
with variance σ_t²Δt. Two consequences are closed-form algebra: the ratio
between new and old weights is a density ratio of two Gaussians, and the
KL between the tuned and reference policies at a step is the squared
difference of their means over 2σ_t²Δt (§4).

## What it explains

**[SOTA-tmp6jbkw](../practices.d/SOTA-tmp6jbkw.md), all three of its clauses.** The practice says to roll the
model out as a same-marginal SDE, built from its own velocity, and to
anchor each step with the closed-form KL. On this account the SDE is what
makes the model a policy at all, building it from the velocity is what lets
a model trained only for the ODE be used, and the closed-form KL comes free
with the Gaussian step. The practice's noise level a is an exploration
knob, and the account says why it has to be nonzero. Flow-GRPO's own sweep
has a = 0.1 learning slowly and a = 0.7 and 1.0 equally fast (Fig. 7b).

It also says why the practice can sample its evaluations with the ODE.
The SDE and the ODE share marginals for any velocity, including the tuned
one, so a policy improved through the SDE is the same generative model
sampled the other way. [SOTA-265](../practices.d/SOTA-265.md) records the same freedom used for sample
quality.

## Where it stops

- **Continuous time only.** The marginal equivalence holds for the SDE, not
  for its ten-step discretization. Flow-GRPO's 10-step rollouts show colour
  drift and blurred detail (Fig. 19), which the 40-step ODE evaluation does
  not share. Its σ_t = a√(t/(1 − t)) is infinite at the noise end, where
  sampling starts, and the paper does not say how the first step is taken.
- **Likelihood-ratio methods only.** Methods that differentiate a reward
  through the sampler, or that fit preferences through the diffusion loss
  as Diffusion-DPO does ([LIT-tmp4m2nj](../literature.d/LIT-tmp4m2nj.md)), need no per-step policy density.
  The account says nothing against them.
- **It does not say a KL anchor is enough.** It says the anchor is
  computable per step. Flow-GRPO's evidence that the anchor prevents reward
  hacking is measured with other reward models, and DDPO ran with no anchor
  at all and degraded under over-optimization.
- **It does not reach a one-step generator.** A distilled one-step model
  has one deterministic step and no SDE family to swap in, so this
  construction gives it neither a policy density nor a tractable anchor.
  That is the case [SOTA-302](../practices.d/SOTA-302.md) covers, by moving the regularizer into noise
  space, and [THEORY-054](THEORY-054.md) is the record's account of why that works.
