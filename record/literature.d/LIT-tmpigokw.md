---
status: Active
title: 'Deep Unsupervised Learning using Nonequilibrium Thermodynamics'
version: 1
tags:
- generative-modeling
date: '2026-09-19'
published: '2015-03-12'
arxiv: '1503.03585'
first_author: 'Sohl-Dickstein'
keywords:
- 'diffusion-models'
- 'forward-process'
- 'reverse-process'
- 'tractable-likelihood'
- 'nonequilibrium-thermodynamics'
extended_by:
- LIT-036
implementations: []
summary: >-
  Sohl-Dickstein et al. (2015), [ARXIV-1503.03585](https://arxiv.org/abs/1503.03585). Where diffusion models come
  from: destroy structure with a slow forward process, learn the reverse, and
  get a generative model that is flexible *and* tractable — a trade the paper
  frames as the central problem it is solving.
---

# LIT-tmpigokw: Deep Unsupervised Learning using Nonequilibrium Thermodynamics

Sohl-Dickstein et al. (2015) — [ARXIV-1503.03585](https://arxiv.org/abs/1503.03585)

## Key takeaways

- **The framing is flexibility versus tractability**, and the paper says so in
  its first sentence: modelling complex data needs flexible distribution
  families, but learning, sampling, inference and evaluation have to stay
  computationally reachable. Diffusion is presented as a way to have both
- **Destroy structure slowly, then learn to undo it.** An iterative forward
  diffusion process converts the data distribution into a tractable one; a
  learned reverse process restores it. That is the whole construction, and it
  is unchanged in everything downstream
- **Slowness is what buys tractability.** Each step is small enough that its
  reverse is well-approximated by a simple distribution — which is why the
  model can have "thousands of layers or time steps" and still be trainable
- **Probabilities are computable, not just samples.** The paper stresses
  evaluating likelihoods and computing conditional and posterior probabilities
  under the learned model — a property the later, sample-quality-driven line
  largely stopped foregrounding

## Standing in the anthology

**The origin of the line, filed as a candidate from `#180` rather than
because anything here cites it.** The record holds 62 documents that mention
diffusion and four practices about it, and did not hold the paper the
construction comes from.

**Carries no practice, and the reason is specific rather than dismissive.**
The record's diffusion practices rest on what came later: [LIT-036](LIT-036.md) (DDPM) is
what made the construction work at image scale, and `SOTA-188` is sourced to
EDM, which — as `LIT-036`'s own note puts it — "derives what this paper set by
hand". A recommendation drawn from here would be a recommendation the field
has since restated with better constants.

What it supplies instead is the **framing**, which the downstream papers
inherit without restating: the forward process is a choice about *how slowly
to destroy structure*, and every later argument about noise schedules,
samplers and step counts is an argument about that choice. A reader who meets
`SOTA-203`'s higher-order ODE solver or `SOTA-206`'s multi-step option without
this is tuning a knob whose purpose is offstage.

Filed under `#180`'s warrant — a paper somebody returned to — which is a
different and legitimate basis from `#137`'s. I first declined it for having
no citations here, which was `#137`'s test applied where it does not belong.

Unread — no `NOTE`.
