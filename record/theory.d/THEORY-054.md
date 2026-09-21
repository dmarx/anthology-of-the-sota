---
number: 54
status: Proposed
formerly:
- THEORY-tmpq2xg2
promote_when: >-
  The bound shown to hold where it is used — a measurement that the noise-space
  `L2` penalty actually tracks the data-space KL over a real training run,
  rather than merely upper-bounding it in principle. An upper bound that is
  loose everywhere constrains nothing, and the data processing inequality
  gives no guarantee of tightness. A second setting where the same
  reparameterization makes an intractable regularizer tractable would also
  count. What would not settle it: another method that regularizes in noise
  space and works, which is the observation this is one explanation of.
title: 'The regularizer that is intractable in data space is tractable in noise space, and bounds the data-space divergence'
version: 1
tags:
- generative-modeling
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-491
explains:
- SOTA-302
summary: >-
  Eyring et al. (2025), [LIT-491](../literature.d/LIT-491.md) — the KL to the base model needs
  Jacobian determinants through the generator and is intractable in data
  space. Posed over the *input noise* it reduces, under a Lipschitz condition,
  to an `L2` penalty on the modification, and the data processing inequality
  makes that an upper bound on the data-space divergence.
---

<!-- inactive-ok-file: SOTA-302 — Proposed, filed in this same
     contribution; this theory declares `explains:` on it, so the citation is
     the relation itself -->

# THEORY-054: The regularizer that is intractable in data space is tractable in noise space, and bounds the data-space divergence

## Source

Eyring, Karthik, Dosovitskiy, Ruiz and Akata (2025), [LIT-491](../literature.d/LIT-491.md) §3.1
and Appendix A.4 — read as [NOTE-240](../notes.d/NOTE-240.md).

## What it explains

| practice | what it says to do | what this says is going on |
|---|---|---|
| [SOTA-302](../practices.d/SOTA-302.md) | steer a distilled generator by modulating its input noise rather than fine-tuning its weights | the choice is not stylistic and not about parameter count — it is the difference between an objective whose anchoring term can be computed and one whose cannot, which is why the weight-space version reward-hacks |

## The account

Aligning a generator to a reward means learning a **tilted** distribution:
upweight high reward, stay near the base model. The second half is what stops
the result drifting off the data manifold to chase the score, and it is
normally written as a KL to the base distribution.

For a step-distilled generator that KL is not available. The generator is a
deterministic map from noise to image, so comparing output densities requires
the change-of-variables formula and therefore a Jacobian determinant through
a high-dimensional network. Existing treatments route around this via
stochastic optimal control, which needs the continuous-time SDE structure
that distillation removed.

**The reparameterization dissolves the problem rather than solving it.** Hold
the generator fixed and ask instead which *noise* distribution, pushed
through it, yields the tilted output distribution. Such a distribution exists
and is characterized in the paper. Now the base distribution is a standard
Gaussian, and for a residual modulation `ε ↦ ε + Δ(ε)` the change of
variables plus Stein's lemma gives a KL whose awkward term is a
log-determinant — which Theorem 1 bounds by `O(L²)` in the modulation's
Lipschitz constant. Keep `L` small and the regularizer is just
`½·E‖Δ(ε)‖²`.

**And it is the right quantity, not merely a convenient one.** The data
processing inequality says a fixed map cannot increase KL divergence, so the
noise-space KL upper-bounds the data-space KL between the steered and base
output distributions. Minimizing the computable thing therefore constrains
the thing that was wanted.

## Why `Proposed`

**Because an upper bound is not a measurement of what it bounds.** The DPI
guarantees the direction and says nothing about tightness. If the generator
contracts sharply — which a distilled one-step map plausibly does — the
noise-space KL could be large while the data-space KL is near zero, and the
penalty would be restraining a model that needed no restraint. Nothing in the
paper measures the gap.

**Because the Lipschitz condition is engineered rather than verified.** The
approximation needs `L` small; the implementation initializes the modulation
to output exactly zero, which makes it true at step 0. No measurement
establishes that it stays true as training proceeds, and the bound degrades
quadratically if it does not.

**Because the supporting evidence is the remedy working, not the mechanism.**
That direct fine-tuning degrades the model and noise modulation does not is
consistent with this account — and also with a weaker one in which the noise
parameterization simply has less capacity to destroy the generator, which
would produce the same ranking without any of the information theory.

## What it does not say

**It does not say noise space is generally the right place to regularize.**
The argument needs a fixed, deterministic generator whose input distribution
is simple enough to compare against — a Gaussian. Where the base model is
being trained, or the input is structured, none of the steps go through.

**It does not say the tilted noise distribution is unique or reachable.** The
paper characterizes an optimal tilted noise distribution and parameterizes an
approximation to it with a low-rank adapter. How much of the target that
family can represent is not addressed.

**It says nothing about which reward to tilt toward.** The machinery keeps
you near the base distribution while moving toward a reward; it has no
opinion on whether the reward is worth moving toward, and reward-hacking of
the ordinary kind — a reward that is itself a bad proxy — is untouched by any
of this.
