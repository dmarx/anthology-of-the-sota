---
number: 106
status: Active
formerly:
- THEORY-tmpxkux1
title: 'Gaussian flow matching is a diffusion model; what separates the named recipes is loss weighting, network output and sampling schedule'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Kingma and Gao (LIT-692) filed and added as a source. It carries
    the weighting identity, which is now scoped to the unshifted cosine and
    to uniform-t flow matching; its App. D.2.1, which claims otherwise, is
    wrong. Identity 4 is re-cited to its §3.2, because THEORY-027 covers
    only the unweighted bound. The equivalence is stated as one of expected
    loss. The account is unchanged, and it stays Active.
tags:
- generative-modeling
- training-optimization
date: '2026-09-25'
source:
- LIT-678
- LIT-630
- LIT-692
extends:
- THEORY-027
explains:
- SOTA-266
promote_when: >-
  Active for the equivalence, which is algebra anyone can check. The sub-claim
  that "straight" is not the operative variable is illustrated on toys only.
  It would be settled by a controlled comparison on real data that holds the
  weighting and the sampling schedule fixed and varies only the interpolant,
  or only the network output (û against v̂). A new "flow matching beats
  diffusion" result that changes all three at once would not settle it.
summary: >-
  Gao et al. (2024), [LIT-678](../literature.d/LIT-678.md), on [LIT-630](../literature.d/LIT-630.md). With a Gaussian
  source the flow-matching interpolant is a diffusion forward process with
  `α_t = 1−t, σ_t = t`. The conditional flow-matching loss is an ε-MSE under
  one particular weighting, and the flow-matching Euler sampler is DDIM. So a
  result labelled "flow matching against diffusion", or "straight against
  curved path", is a comparison of three things: the loss weighting, the
  network output and the sampling schedule. "Straight" describes the
  conditional path to one data point, not the marginal ODE a sampler
  integrates.
---

# THEORY-106: Gaussian flow matching is a diffusion model; what separates the named recipes is loss weighting, network output and sampling schedule

## Source

Gao, Hoogeboom, Heek, De Bortoli, Murphy and Salimans (2024), [LIT-678](../literature.d/LIT-678.md),
a blog post that assembles derivations. Part of the account is already in
[LIT-630](../literature.d/LIT-630.md), whose Theorem 3 and "diffusion is one choice of path"
make the forward-process half. The weighting identity is derived in Kingma and
Gao (2023), [LIT-692](../literature.d/LIT-692.md), App. D.3: "the CFM loss is equivalent to the
v-prediction loss with cosine schedule".

## The account

Four identities, each a piece of algebra:

1. **Forward process.** Flow matching's `z_t = (1−t)x + tε` with Gaussian `ε`
   is a diffusion forward process `z_t = α_t x + σ_t ε` with `α_t = 1−t, σ_t
   = t`.
2. **Loss.** Every network output (`ε̂`, `x̂`, `v̂`, the flow-matching field `û`)
   gives an MSE that equals `w(λ)·‖ε̂ − ε‖²` for an output-specific weight.
   Flow matching's weight (OT path, uniform `t`) is the one v-MSE gets under
   the *unshifted* cosine schedule, `e^{−λ/2}`. A resolution-shifted cosine
   reweights v-MSE toward high noise by up to `(d/64)²`, so the identity does
   not survive the shift. The source's App. D.2.1 says it does, and it is
   wrong.
3. **Sampler.** DDIM, rewritten in the coordinates that suit the `û` output,
   is exactly the flow-matching Euler step. Stochastic samplers (DDPM, or
   EDM-style churn) are available to both.
4. **Schedule.** Given the weighting, the training loss depends on the
   schedule only through its endpoints, and the schedule's shape sets only
   the estimator's variance ([LIT-692](../literature.d/LIT-692.md), §3.2). [THEORY-027](THEORY-027.md)
   is the unweighted special case.

**Consequence.** Pick a weighting, a network output and a sampling schedule,
and you have fixed a model in one family. The labels "flow matching" and
"diffusion" name conventional bundles of those three choices. They are not
different model classes.

**"Straight" is a property of the conditional path.** The interpolant is a
straight line from one data point to noise. The marginal ODE a sampler
actually integrates is straight only when the target is a single point. On
the post's 1-D toy, a variance-preserving schedule gives straighter marginal
paths for wide data distributions, and the flow-matching schedule does so
for narrow ones.

## What it explains

**[SOTA-266](../practices.d/SOTA-266.md)'s result, as a decomposition, not an
intervention.** [SOTA-266](../practices.d/SOTA-266.md) recommends the straight-line path because controlled
comparisons found it better, and its Conditions say "No mechanism has been
isolated". This account says what those comparisons change. Moving from a
VP path to the linear one changes the implied loss weighting, the network
output (`û` under flow matching) and the sampling schedule together. So
"straight beats curved" is shorthand for one bundle of three choices beating
another. The measured result is untouched. What changes is which variable
it may be attributed to. And this is the record's inference, not the post's:
[LIT-630](../literature.d/LIT-630.md)'s controlled FM-OT against FM-diffusion comparison, which holds
architecture and budget fixed, still moves the weighting and the sampling
schedule together.

[SOTA-266](../practices.d/SOTA-266.md)'s own "Relation" paragraph already treats SD3's logit-normal timestep
density as the rectified-flow expression of EDM's log-normal, meaning a
weighting written in different coordinates. This account is the general form
of that reading.

## Where it stops

- **Gaussian source only.** Non-Gaussian or learned sources, and flow matching
  on manifolds, are outside it.
- **Exact for first-order samplers.** Under higher-order solvers the network
  output changes the numerical trajectory, which is where the two
  specifications stop being operationally identical. The source also allows
  that the output "may also affect the training dynamics".
- **It says nothing about which bundle is best.** The source declines to
  recommend, and leaves the importance of `û` and of the `1−t, t` schedule on
  real data as "future work".
- **The equivalence is of expected loss.** Flow matching and cosine v-MSE
  sample `λ` from different densities, logistic and hyperbolic secant, so
  the gradient variance differs. The network outputs also differ.
- **No ranking of the three choices is imported.** Kingma and Gao's 64×64
  ablations, changing one at a time, find the training schedule makes no
  measurable difference. The weighting and the sampler each move FID by
  0.1–0.3, and the network output by up to 0.1. These are single seeds. The
  blog's "weighting is the most important part" is not supported against
  the sampler.
- **The straightness sub-claim rests on toys.** It is a well-argued
  correction of a label, and the evidence for it is a 1-D Gaussian.
