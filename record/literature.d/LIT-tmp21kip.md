---
status: Active
title: 'Diffusion Meets Flow Matching: Two Sides of the Same Coin'
version: 1
tags:
- generative-modeling
- training-optimization
- inference-optimization
date: '2026-09-25'
published: '2024-12-02'
url: 'https://diffusionflow.github.io/'
first_author: 'Gao'
keywords:
- 'flow-matching-diffusion-equivalence'
- 'loss-weighting'
- 'network-parameterization'
- 'ddim-euler-equivalence'
- 'sampling-schedule'
- 'churn'
implementations: []
extends:
- LIT-630
- LIT-038
summary: >-
  Gao, Hoogeboom, Heek, De Bortoli, Murphy and Salimans (2024), a blog post
  at diffusionflow.github.io. With a Gaussian source, **flow matching is a
  diffusion model** with the schedule `α_t = 1−t, σ_t = t`, and the
  flow-matching Euler sampler is DDIM. What separates the named recipes is
  three choices: the loss weighting, the network output and the sampling
  schedule. "Straight paths" holds only for a single-point target, and a
  variance-preserving schedule can be straighter for wide data. The content
  is derivation and toy illustration only: no trained models and no
  benchmarks.
---

# LIT-tmp21kip: Diffusion Meets Flow Matching: Two Sides of the Same Coin

Gao, Hoogeboom, Heek, De Bortoli, Murphy and Salimans (2024) — <https://diffusionflow.github.io/>

A blog post, filed under a `url:` because it has no arXiv id or DOI
(`ADR-009`'s last resort). The page uses the ICLR Blogposts 2025 template,
but acceptance to that track could not be confirmed, so treat it as
self-published. Read as text. The interactive figures (sliders and
animations) were not seen, and they are where the post's only empirical
content sits.

## Key takeaways

**The thesis, in its own words:** "diffusion models and Gaussian flow matching
are the same, although different model specifications can lead to different
network outputs and sampling schedules". It covers only "the common special
case that the source distribution used with flow matching corresponds to a
Gaussian". It also declines to take a side: "Our purpose is not to recommend
one approach over another".

**Forward process.** Diffusion's `z_t = α_t x + σ_t ε` and flow matching's
`z_t = (1−t) x + t ε` coincide when the noise is Gaussian and
`α_t = 1−t, σ_t = t`.

**Sampling: DDIM is the flow-matching Euler step.** DDIM can be rewritten as
`z̃_s = z̃_t + [output]·(η_s − η_t)`, with one reparametrization per network
output (`x̂`, `ε̂`, or the flow-matching vector field `û`). With the
flow-matching schedule the `û` row reduces to the flow-matching update:
"Diffusion with DDIM sampler == Flow matching sampler (Euler)". The post
qualifies this twice. Under a higher-order solver "the network output can
make a difference". And DDIM is invariant to a linear rescaling of `α_t,
σ_t`, which is "not true for other samplers".

**Training: every output is a weighted ε-MSE.** The loss is written
`E[w(λ_t) · dλ/dt · ‖ε̂ − ε‖²]`, with the weighting and the schedule term
kept separate on purpose. The four outputs give `ε̂: 1`, `x̂: e^{−λ}`,
`v̂: α_t²(e^{−λ}+1)²` and `û: (e^{−λ/2}+1)²`. "Flow matching weighting ==
diffusion weighting of v-MSE loss + cosine noise schedule". **That identity is
not derived here.** The post cites Kingma & Gao (2023, arXiv 2303.00848) App.
D.2–3 for it, and the record does not hold that paper.

**The training schedule is the least important of the three choices.** The
loss "is invariant to the training noise schedule … only related to the
endpoints", and the schedule "might still affect the variance of the Monte
Carlo estimator". This is [THEORY-027](../theory.d/THEORY-027.md)'s invariance restated in
weighted form. "One can choose completely different noise schedules for
training and sampling."

**"Straightness" is a misnomer.** "Flow matching schedule is only straight for
a model predicting a single point. For realistic distributions, other
schedules can give straighter paths." The support is a 1-D Gaussian toy: VP is
straighter for wide distributions, FM for narrow ones.

**Stochastic sampling applies to both.** One DDPM step is "exactly equivalent"
to a DDIM step of twice the size followed by renoising. The renoised fraction
is EDM's churn. This corrects "the common belief that flow matching is always
deterministic".

**What flow matching adds is two specifications, both left untested.** The
two are the `û` output and the `1−t, t` sampling schedule. "It would be
interesting to investigate the importance of these two model specifications
empirically … which we leave to future work."

## Traps

- **"The same model family" is not "the choice doesn't matter".** The post's
  closing bullets name the two specifications that *can* matter, network
  output and sampling schedule. It says the output "may also affect the
  training dynamics".
- **Three sentences in it are assertions, not measurements.** "The weighting
  function is the most important part of the loss" is argued perceptually and
  never tested. "SD3 weighting … is very similar to the EDM weighting" is two
  curves plotted side by side, with no models trained. And "empirically"
  refers to those plotted curves.
- **Anyone citing this post for the weighting identity is citing a pointer.**
  The derivation is in Kingma & Gao 2023.
- **Gaussian source only.** Non-Gaussian flow matching, on manifolds or with
  learned sources, is outside the claim.

## Standing in the anthology

Filed from the reading-time triage of 2026-09-25 as the account that joins
[LIT-630](LIT-630.md) (flow matching) and [LIT-038](LIT-038.md) (DDIM). Those
two were held as separate lines, and a practice sat between them that says
"straight" beats "curved" and admits it does not know why.

It sources **`THEORY-tmpxkux1`**: under a Gaussian source, a comparison
labelled "flow matching against diffusion" or "straight against curved"
changes the weighting, the network output and the sampling schedule together.
That is the decomposition [SOTA-266](../practices.d/SOTA-266.md)'s Conditions say is missing
("No mechanism has been isolated"). It supplies a decomposition, not an
intervention. The measured result behind [SOTA-266](../practices.d/SOTA-266.md) stands.

**Two follow-ups this note makes visible.** Kingma & Gao 2023 carries the
weighting identity and should be filed. And [LIT-626](LIT-626.md)'s phrase
"flow matching beats diffusion" describes one specification of one family
beating another, and should say which.
