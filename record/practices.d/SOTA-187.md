---
number: 187
status: Active
formerly:
- SOTA-tmphxjle
title: 'Train the generative model in a learned compressed latent, not at full resolution'
version: 2
history:
- version: 2
  date: '2026-09-10'
  note: >-
    Enriched from the #123 readings. The recommendation is unchanged;
    the source list, the numbers or the neighbourhood are.
tags:
- representation-and-encoding
consensus: universal
date: '2026-09-08'
source:
- LIT-062
# LIT-036 section 4.3 MEASURES this practice's premise -- that most of a
# pixel-space model's capacity describes imperceptible detail -- two years
# before LIT-062 acts on it as an assumption.
- LIT-036
implementations:
- Stable Diffusion
---

# SOTA-187: Train the generative model in a learned compressed latent, not at full resolution

## Source

Rombach et al. (2022), [LIT-062](../literature.d/LIT-062.md) — [ARXIV-2112.10752](https://arxiv.org/abs/2112.10752), CVPR 2022.

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

**The transferable claim is a compute-allocation one**, and it is why this is
filed under `model-architecture` rather than as a diffusion technique: when
the expensive model's input carries structure a cheap model can strip, strip
it first and let the expensive model work on what is left. The two-stage
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
first stage are invisible to the second stage's loss.

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
