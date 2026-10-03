---
number: 187
status: Active
formerly:
- SOTA-tmphxjle
title: 'Train the generative model in a learned compressed latent, not at full resolution'
version: 5
history:
- version: 2
  date: '2026-09-10'
  note: >-
    Enriched from the #123 readings. The recommendation is unchanged;
    the source list, the numbers or the neighbourhood are.
- version: 3
  date: '2026-09-10'
  note: >-
    The body named model-architecture as this practice's topic, from
    before it was retagged representation-and-encoding. The argument for
    filing by kind of claim rather than as a diffusion technique is
    unchanged; only the stale topic name is fixed.
- version: 4
  date: '2026-09-23'
  note: >-
    Appends `signal-structure`. A load-bearing part of this
    document is a property of the data: it rests on a property of images:
    most of a pixel-space model's bits describe imperceptible high-frequency
    detail.
- version: 5
  date: '2026-10-03'
  note: >-
    STARFlow (LIT-785) added as a source: evidence from outside
    diffusion, a normalizing flow moved from pixels to latents (ImageNet-256
    FID 4.69 to 2.40, confounded with a decoder change). It is also added to
    the Conditions as a visible decoder ceiling: its decoder's
    reconstruction FID is worse than its generated FID. Consensus unchanged.
tags:
- representation-and-encoding
- generative-modeling
- signal-structure
consensus: universal
date: '2026-09-08'
source:
- LIT-062
# LIT-036 section 4.3 MEASURES this practice's premise -- that most of a
# pixel-space model's capacity describes imperceptible detail -- two years
# before LIT-062 acts on it as an assumption.
- LIT-036
- LIT-785
introduced_by:
- LIT-062
implementations:
- Stable Diffusion
---

# SOTA-187: Train the generative model in a learned compressed latent, not at full resolution

## Source

Rombach et al. (2022), [LIT-062](../literature.d/LIT-062.md) — [ARXIV-2112.10752](https://arxiv.org/abs/2112.10752), CVPR 2022.

Ho et al. (2020), [LIT-036](../literature.d/LIT-036.md) — [ARXIV-2006.11239](https://arxiv.org/abs/2006.11239). Its §4.3 measures
this practice's premise — that most of a pixel-space model's codelength
describes imperceptible detail — two years before Rombach et al. act on it as
an assumption.

Gu et al. (2025), [LIT-785](../literature.d/LIT-785.md) — STARFlow is evidence from outside
diffusion. The same deep-shallow normalizing flow moved from pixels to
SD-VAE latents goes from ImageNet-256 FID 4.69 to 2.40 (its Table 1). The
input space, the patch size and the decoder change together, and the latent
model decodes through a GAN-fine-tuned decoder, so the size of the gain is
confounded. The direction is the one this practice predicts, for a
likelihood model that is not a diffusion model.

Split the problem in two. First train an autoencoder that compresses the
signal to a lower-dimensional latent, keeping what a human would notice and
discarding what they would not. Then train the generative model *in that
latent space* and decode at the end.

The argument for why this is nearly free is the useful part. Likelihood-based
generative models spend most of their capacity on imperceptible
high-frequency detail — bits that cost real compute and that no evaluator
rewards. Moving to a perceptually-equivalent compressed space removes that
spend before the expensive model ever sees the data, so the generative model
works in a space whose dimensions it actually needs.

The recommendation comes from [LIT-062](../literature.d/LIT-062.md), which proposed the split for diffusion:
an autoencoder with a perceptual objective is trained once and frozen, the
diffusion model is trained on its latents with conditioning introduced into
the latent-space denoiser, and the result was substantially cheaper training
and sampling at a given resolution, making high-resolution synthesis
practical. The same paper is where the condition comes from that the latent
must be perceptually equivalent, since whatever the autoencoder discards the
diffusion model can never recover.

**The transferable claim is a compute-allocation one**, and it is why this is
filed by the kind of claim rather than as a diffusion technique: when the
expensive model's input carries structure a cheap model can strip, strip it
first and let the expensive model work on what is left.

*(This sentence named `model-architecture` until v3, from before the practice
was retagged `representation-and-encoding` — "how the signal is encoded before
the expensive network sees it … tokenizers and learned latents", which is this
exactly. The argument is unchanged and the topic is now the better fit; the
prose had simply not followed the tag.)* The two-stage
shape — learn a compact representation, then model *that* — recurs well
beyond images.

## Conditions

The compression ratio is a real trade rather than a free win: too aggressive
and the autoencoder discards detail the task needed, and no amount of
generative capacity downstream recovers it. The paper's regularised
autoencoders and their choice of downsampling factor are a tuned answer for
images at the scale it reports.

It also introduces a dependency the single-stage version does not have. The
generative model can only be as good as the decoder, and errors made in the
first stage are invisible to the second stage's loss. STARFlow
([LIT-785](../literature.d/LIT-785.md), App. B.3) shows the ceiling plainly: reconstructing 50K real
images through its noisy-latent decoder gives rFID about 2.73, worse than
the 2.40 its generator reaches. At that resolution the decoder, not the
flow, sets the FID.

Marked `universal` for the domain it was shown in: latent-space training is
what essentially every deployed image and video generator does, and doing it
at full resolution is what would need justifying.

## Why this is an encoding claim rather than an architecture one

Filed under `representation-and-encoding` alongside BPE tokenization, and the
pairing is the argument: both fit a cheap encoder that compresses the signal,
then train the expensive model on what comes out. One discrete, one
continuous. A latent autoencoder is a tokenizer that did not round.

That is also the line that keeps the topic from becoming a bag of anything
with "latent" in it. [SOTA-147](SOTA-147.md) compresses internal state at serving time and
[SOTA-180](SOTA-180.md) compresses weights; neither touches how the input signal is encoded,
and both stay where they are.

## Known implementations

- Stable Diffusion and the open image and video generation line generally
