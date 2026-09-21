---
number: 46
status: Active
formerly:
- THEORY-tmprosv3
title: 'Uniform-state discrete diffusion is the argmax of a Gaussian diffusion, which is why Gaussian technique transfers to it and not to masked diffusion'
version: 1
tags:
- generative-modeling
- model-architecture
date: '2026-09-21'
source:
- LIT-479
explains:
- SOTA-289
summary: >-
  Sahoo et al. (2025), [LIT-479](../literature.d/LIT-479.md) — taking the `argmax` of a
  Gaussian diffusion's latents carries its marginals onto those of a
  uniform-state discrete diffusion, under a reparameterization of the noise
  schedule, and the discretized process satisfies the defining ODE of a
  discrete diffusion. So it is one. Masked diffusion has no such preimage.
---

<!-- inactive-ok-file: SOTA-289 — Proposed, and the practice this account
     explains; the document's own point is that a sound explanation does not
     promote the practice, so its unsettled status is what is being said -->

<!-- inactive-ok-file: ADR-031 — Proposed, cited for the practice/explanation split
     that lets this account be Active while the practice stays Proposed -->

# THEORY-046: Uniform-state discrete diffusion is the argmax of a Gaussian diffusion, which is why Gaussian technique transfers to it and not to masked diffusion

## Source

Sahoo, Deschenaux, Gokaslan, Wang, Chiu and Kuleshov (2025),
[LIT-479](../literature.d/LIT-479.md) §3 — read as [NOTE-228](../notes.d/NOTE-228.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-289](../practices.d/SOTA-289.md) | for few-step generation, use uniform-state diffusion with consistency distillation | not a lucky transplant but a licensed one: the discrete process has a continuous preimage, so the continuous literature's methods have somewhere to land |

## The account

Run a Gaussian diffusion on `R^K` and map each latent to the one-hot vector of
its largest coordinate. Two things then have to be shown, and both are.

**The marginals match.** The `argmax` of a Gaussian latent has a closed-form
probability mass function, and it is exactly the marginal of a uniform-state
discrete diffusion — with the noise parameter reparameterized by a
*diffusion transformation operator* built from the standard normal CDF. The
two processes are different Markov chains; what the map relates is their
marginal distributions.

**The dynamics match.** The discretized marginal evolves under the linear ODE
that characterizes a discrete diffusion process. Satisfying that ODE is
necessary and sufficient, so the discretized Gaussian process **is** a
uniform-state discrete diffusion rather than something that resembles one.

The consequence is a licence. Techniques developed for Gaussian diffusion —
noise schedules, variance reduction, consistency distillation — are not being
applied to discrete diffusion by analogy; they are being applied to a process
that has a Gaussian representation. The paper cashes this twice, with a
curriculum that anneals the `argmax` through a tempered softmax and with a
discrete adaptation of consistency distillation.

**And the asymmetry is the point.** No comparable map exists for
absorbing-state (masked) diffusion. The source's conclusion says so directly,
and it is the clearest statement of why the two discrete families should be
expected to diverge in what can be borrowed for them, whatever their relative
perplexities today.

## Why `Active`

Because it is a derivation with both halves shown, and one of them checked
numerically as well. The status is about the account, not about the method's
standing: [SOTA-289](../practices.d/SOTA-289.md) is `Proposed` and `unreplicated`, and an
explanation being correct is not evidence that a practice is worth adopting —
the split [ADR-031](../decisions.d/ADR-031.md) exists to keep visible.

## What this does not say

**It does not say uniform-state diffusion is better.** Masked diffusion is
ahead on likelihood in the source's own tables, on 6 of 7 zero-shot datasets
and on both training corpora. The duality is a claim about what can be
*borrowed*, not about what currently wins.

**It does not carry the empirical result it was used to obtain.** The source's
ablation splits its three-point perplexity improvement over the previous
uniform-state model roughly evenly between a Rao-Blackwellized ELBO — which
has nothing to do with this account — and the duality-derived curriculum. The
theorem earns about 1.3 of those 3 points.

**And the curriculum it licenses is not itself a bound.** Feeding the denoising
model a continuous latent while the objective is defined for a discrete
process makes the training loss an invalid NELBO except in the limit. The
source says this and evaluates with the proper discrete bound instead. So the
theorem justifies the *shape* of the training procedure, not its status as a
likelihood bound.

**Two demonstrations is not the general claim.** That Gaussian technique
transfers is shown for a curriculum and for consistency distillation. Whether
the bridge carries the rest of that literature is the open question, and the
value of the account depends on the answer.
