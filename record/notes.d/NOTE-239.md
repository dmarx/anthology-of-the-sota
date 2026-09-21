---
number: 239
status: Read
formerly:
- NOTE-tmpyuelo
paper: LIT-490
title: 'Denoising-corrected gradient guidance'
version: 1
date: '2026-09-21'
summary: >-
  Read for a practice the record's diffusion line was missing. The ordering
  change is well motivated and cheaply adopted; the theory is proved under
  idealized assumptions the authors name; and the useful experimental result
  is that the standard method was optimizing the plan rather than the
  executed outcome.
---

# NOTE-239: Denoising-corrected gradient guidance

## Contribution

Gradient guidance — nudging a diffusion sampler toward an external objective
— is standard and is usually implemented by adding the gradient *after* the
denoising step. This says that is the wrong order when the data live on a
structured set, and gives the reason: the denoiser is a learned approximate
projection, so putting the gradient inside it turns the sampler into an
inexact projected-gradient method instead of an unconstrained one with a
prior loosely attached.

What is true afterwards: the standard recipe has a named failure mode
(off-geometry drift), a one-line fix at identical cost, and convergence
guarantees in three geometries where previously the analysis covered linear
inverse problems with quadratic objectives.

## Key insight

**The denoiser is already the projection you were about to hand-write.**

`D(x) = E[x₀ | x]` maps a noisy point toward the data support. If the clean
data lie on a manifold or inside a convex set, that is approximately a
nearest-point projection onto it — and a sampler already calls it once per
step. So a constrained-optimization algorithm is available for free: take the
gradient step in ambient space, then let the denoiser put you back.

The reason PDG fails is the same fact read the other way. Once you have
denoised, you are on the geometry; adding a gradient afterwards is precisely
the step that leaves it, with nothing following to correct the departure.

## Assumptions

- **An exact Stein posterior-mean denoiser.** The theory assumes the denoiser
  is the true conditional mean, not a learned approximation of it.
- **The learned support faithfully represents the feasible set.** The paper
  says explicitly that projection-error terms *can* absorb learned-score
  error and that a full treatment of misspecification is left to future work.
- **Deterministic DDIM dynamics, variance-exploding diffusion, an
  exponentially decaying noise schedule.** Other samplers and schedules
  "require tracking their time-varying relaxation and denoising errors" —
  i.e. the theory does not transfer as written.
- Compactness in the convex and manifold settings; smoothness of the
  objective for the nonconvex rates.

## Key results

- **Bounds between the Stein denoiser and the relevant projection** in three
  settings: linear-Gaussian, compact convex, compact smooth submanifold.
- **Finite-time guarantees per geometry:** geometric contraction of the
  projected objective error for strongly convex objectives on linear-Gaussian
  and convex sets; a best-iterate rate for smooth nonconvex; the same rate
  locally on submanifolds.
- **Cost:** one gradient evaluation and one pretrained-denoiser call per
  reverse step, on a single trajectory — against baselines needing score
  Jacobians or repeated batch generation.
- **Trajectory tracking (double integrator, unicycle):** PDG plans track the
  reference closely and lose much of that advantage on rollout through the
  true dynamics; DCG's plans and rollouts nearly coincide. DCG reports the
  lowest rollout cost and dynamic-feasibility error among guided methods on
  both random references; on the circle reference its rollout cost is
  slightly worse than the DRGD baseline while its feasibility error is best.
- **D4RL/MuJoCo (Hopper, Walker, HalfCheetah medium-v2):** "slightly higher"
  normalized returns than PDG on all three, guidance scale tuned separately
  per method.

## Claims

**Well supported and the reason to file this:** that the ordering matters and
that the denoiser-as-projection reading explains why. The theory is proved
rather than gestured at, in three geometries rather than one, and the
mechanism predicts the experimental failure mode of the alternative.

**The most useful empirical finding, and it is a measurement finding:** PDG's
advantage is largely on the *planned* trajectory and largely gone after
execution. That is not a statement about optimizer quality — it is a
statement that the quantity being optimized was not the quantity that
mattered. A practitioner comparing guidance methods on planned cost would
have chosen PDG.

**Thin, and labelled thin by its authors:** the reinforcement-learning
result. "Slightly higher" on three MuJoCo tasks against one baseline is
consistent with the claim and does not carry it, and the paper names broader
evaluation as future work.

**Proved under assumptions that are not the deployment conditions.** Exact
posterior-mean denoiser, faithful support, DDIM, variance-exploding,
exponential schedule. Every one of those is stated; together they mean the
guarantees describe an idealization of the thing people would run.

**Not established here:** magnitudes. The comparison tables did not survive
text extraction from the HTML rendering, so this reading quotes directions
and the authors' own qualifiers rather than effect sizes. Anyone relying on
how *much* better DCG is should read Tables 2 and 3 in the source.

## Method

Define DCG as gradient-then-denoise; prove denoiser-to-projection bounds in
three geometries; read the reverse process as time-varying inexact projected
gradient and derive finite-time rates; evaluate on synthetic constrained
problems, double-integrator and unicycle trajectory tracking with rollout
through true dynamics, and a Diffuser-style D4RL pipeline.

## Connections

- [SOTA-203](../practices.d/SOTA-203.md) — sample with a higher-order ODE solver on weights you
  already trained — is the closest neighbour in kind: an inference-time
  change to the sampler, no retraining, easy to get wrong in implementation.
- [SOTA-266](../practices.d/SOTA-266.md) and [SOTA-187](../practices.d/SOTA-187.md) are about how the model is trained and
  where it lives; this is about what you do to it at sampling time when there
  is an external objective, which the record did not cover.
- [SOTA-235](../practices.d/SOTA-235.md) — update weights at inference on a structurally novel test
  instance — is the other end of the same spectrum: both adapt at inference,
  one by changing the weights and this one by changing the update order.

## Bearing on the record

One practice and one theory. The practice is the ordering and its conditions;
the theory is the denoiser-as-projection reading, which is the justification
and is `Proposed` because its proofs assume an exact denoiser and faithful
support.

It also fills a gap in the diffusion line: the record had training-time and
sampling-time practices but nothing about steering a pretrained sampler
toward an objective, which is the interface between generative models and
planning.

## Limitations

**The guarantees are for an idealization.** Exact denoiser, faithful support,
one sampler family, one noise schedule. Useful as an explanation of why the
ordering helps; not a promise about a learned model.

**One group, one paper**, and the strongest experiments are in the appendix.

**The RL evidence is the weakest part** and is the part most likely to be
cited, since D4RL numbers travel further than a unicycle tracking study.

**Effect sizes unverified in this reading** — see Claims.

## Open questions

- How much of the guarantee survives a *learned* denoiser? The authors name
  misspecification as future work and it is the whole distance between the
  theorem and the practice.
- Does the ordering still help under stochastic samplers and
  variance-preserving schedules, which is what most deployed systems use?
- Is the planned-versus-executed gap specific to guidance, or does it show up
  wherever a diffusion planner is scored on its own output rather than on the
  consequence of acting on it?
