---
number: 64
status: Read
formerly:
- NOTE-tmprqunq
paper: LIT-070
title: 'Hierarchical Text-Conditional Image Generation with CLIP Latents'
version: 1
tags:
- generative-modeling
date: '2026-09-09'
published: '2022-04-01'
summary: >-
  Splits text-to-image into a prior that predicts a CLIP image embedding from a caption and a decoder that renders from that embedding. The split buys diversity rather than fidelity — humans slightly prefer GLIDE's photorealism, and strongly prefer unCLIP's diversity. Its own reconstruction figures show the CLIP embedding loses attribute binding.
---

# NOTE-064: Hierarchical Text-Conditional Image Generation with CLIP Latents

## Contribution

Text-to-image in two explicit stages:

- a **prior** mapping a caption to a **CLIP image embedding**;
- a **decoder** (diffusion) rendering an image conditioned on that embedding.

The claim is that going through an explicit image representation improves
**diversity** at minimal cost in photorealism and caption similarity, and that
the decoder can produce **variations** of any real image by encoding it and
re-decoding — preserving semantics and style while varying what the embedding
does not capture.

## Key insight

The intermediate is a *choice*, and making it explicit is what buys the
downstream capabilities. Because CLIP's space is joint over text and images,
a model that generates in it inherits **zero-shot language-guided
manipulation** — interpolations, text diffs — that a direct text-to-pixel model
has no handle for.

The corollary the paper is honest about: **whatever CLIP's embedding discards
is gone.** Figure 15's reconstructions of "difficult binding problems" mix up
which object has which colour, and fail to preserve relative size. That is not
a decoder failure; it is the representation not carrying attribute binding.

## Assumptions

- **The CLIP image embedding is a sufficient conditioning signal.** Figure 15
  is the paper's own evidence that it is not, for binding.
- A prior can be learned to hit that embedding space from text.
- 2022 scale, image–text pairs.

## Key results

- **A diffusion prior beats an autoregressive one** — computationally more
  efficient and higher sample quality. Worth noting as an early instance of
  diffusion displacing AR in a component role.
- **Humans slightly prefer GLIDE on photorealism** — the gap is small — and
  **strongly prefer unCLIP on diversity.** The two-stage split is a
  diversity/fidelity trade, stated plainly.
- **Guidance improves aesthetic quality for both models**, and unCLIP does not
  sacrifice recall to get it.
- **Guide the decoder, not the prior**: "we found that guiding the prior hurt
  results". A negative result about where in a pipeline to apply guidance.
- **Attribute binding fails in reconstruction** (Figure 15): colours swap
  between objects, relative sizes are unreliable.
- Trained with AdamW (decoupled weight decay), β₁ = 0.9.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Generating an explicit image representation improves diversity | strong | human evaluation |
| C2 | It costs little photorealism | moderate | humans still prefer GLIDE slightly |
| C3 | A diffusion prior beats an AR prior | strong | measured on both cost and quality |
| C4 | Guidance helps the decoder and hurts the prior | moderate | reported, not deeply analysed |
| C5 | The CLIP embedding does not carry attribute binding | strong | the authors' own reconstruction figure |

## Method

Train a prior (diffusion or autoregressive) from CLIP text embedding to CLIP
image embedding. Train a diffusion decoder conditioned on the image embedding.
Apply classifier-free guidance to the decoder only.

## Concepts

- **The explicit intermediate representation** — and the fact that it is a
  bottleneck with a measurable content, not a neutral relay.
- **Diversity as the thing a two-stage split buys** — most architecture papers
  report fidelity; this one is clear that the trade runs the other way.
- **Where to apply guidance in a pipeline** — C4 is a small, useful, rarely
  stated finding.

## Connections

The direct counterpart to `LIT-073` (Imagen), which conditions on frozen *text*
embeddings and reports the opposite emphasis. Read together they are the
cleanest comparison available: condition on text, or on a predicted image
representation. Imagen wins on DrawBench; this wins on diversity.

C5 is the same shape as the condition `LIT-062`'s reading attached to
`SOTA-187` — **whatever the intermediate representation discards is a hard
ceiling the downstream model cannot see past.** There it is an autoencoder and
perceptual detail; here it is CLIP and attribute binding. The record states
that condition once, for latent diffusion, and it is general.

## Recommendations

- **R1** — When inserting an explicit intermediate representation, measure what
  it fails to carry, by reconstructing through it. *Topic:* generative
  modelling. *Strength:* strong; C5 is the method as much as the finding.
- **R2** — Expect a representation bottleneck to buy diversity and cost
  fidelity. *Strength:* moderate.
- **R3** — Apply guidance at the stage that renders, not the stage that plans.
  *Strength:* weak — one reported result, no analysis.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

R1 generalises a condition the record already holds in one place. `SOTA-187`
carries "the latent must be perceptually equivalent, and what the autoencoder
discards is a hard ceiling" as a condition on latent diffusion. This paper
demonstrates the same failure in a different representation with a concrete
diagnostic — **reconstruct through the bottleneck and look at what breaks** —
and what breaks here is attribute binding, which is precisely what
text-to-image models were criticised for at the time.

That is a better-supported statement of the record's existing condition than
the record's own source gives it, and it comes with a way to test it.

The document's takeaways — "prior-guided image generation", "CLIP latent space
usage", "hierarchical generation process", "improved composition ability" —
are generic, and the last one is **backwards**: the paper's own figure shows
composition failing, in the specific form of attribute binding.

## Limitations

- 2022, and the architecture was superseded quickly.
- C2 rests on a human preference the paper concedes runs the other way.
- C4 is asserted from one observation.
- The prior is evaluated by what the decoder does with it, so prior and decoder
  errors are not separated.

## Open questions

- What else does a CLIP embedding not carry? Binding is one; the paper found it
  by looking, and nobody has enumerated the rest.
