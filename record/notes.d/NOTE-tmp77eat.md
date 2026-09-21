---
status: Read
paper: LIT-tmpxz6hg
title: 'VQ-VAE: what the three-term loss actually does'
version: 1
date: '2026-09-21'
summary: >-
  Read to give the discrete-tokenizer line a root. The durable content is
  three loss terms with three different owners and a gradient that is copied
  rather than derived — an engineering settlement that every descendant still
  runs unchanged, and that the paper is unusually honest about having chosen
  rather than justified.
---

# NOTE-tmp77eat: VQ-VAE: what the three-term loss actually does

## Contribution

Made a discrete bottleneck trainable inside a deep autoencoder. Vector
quantization was decades old; what did not exist was a way to put it between
an encoder and a decoder and still get gradients to both. The settlement here
— straight-through for the encoder, an online `k`-means term for the codebook,
a commitment term to stop the encoder running away — is what made every later
image, audio and video tokenizer possible, and it is still what they run.

The secondary claim, that discreteness *solves* something rather than merely
costing something, is the posterior-collapse argument: with a uniform prior
over codes the KL term is constant in the encoder parameters, so there is
nothing for a powerful decoder to collapse the latents toward.

## Key insight

Quantization has no gradient, so do not ask for one. Copy the decoder's input
gradient to the encoder's output, and train the codebook with a separate loss
that the reconstruction term never touches. The three terms have three
different owners — decoder, codebook, encoder — and the reason the scheme
works is that none of them is trying to optimize through the `argmin`.

## Assumptions

- **Uniform prior over codes during training.** This is what makes the KL
  constant and the collapse argument go through. It is also why the prior has
  to be *learned afterwards* in a second stage rather than jointly.
- Straight-through is an approximation the authors flag as such: a subgradient
  "could also" be used, and this one "worked well for the initial
  experiments".
- The commitment weight `β` is reported insensitive over 0.1–2.0, with 0.25
  used everywhere. Everything downstream inherits that number.
- Codebook entries are updated by the `L2` term or, as an alternative the
  paper mentions and does not use, by exponential moving averages of encoder
  outputs.

## Key results

- **The objective:**
  `L = log p(x | z_q(x)) + ‖sg[z_e(x)] − e‖²₂ + β‖z_e(x) − sg[e]‖²₂`,
  averaged over the `N` latent positions.
- **ImageNet compression:** `128×128×3` → `32×32×1` indices with `K = 512`, a
  bit reduction of `(128·128·3·8)/(32·32·9) ≈ 42.6×`, with a PixelCNN prior
  over the index field.
- **Likelihood on CIFAR-10:** VAE 4.51 bits/dim, VQ-VAE 4.67, VIMCO 5.14 — all
  lower bounds. The discrete model is slightly worse than the continuous one
  and the paper reports it that way.
- **Posterior collapse:** a second-stage VQ-VAE with a PixelCNN *decoder* over
  a 21×21 latent field keeps its latents in use, in a setting the paper says
  "typically breaks VAEs". The extreme case uses three latents — 27 bits,
  less than a single float32 — for a whole frame, and recovers scene layout
  while regenerating texture procedurally.
- Also demonstrated on audio (VCTK, 64× temporal compression, speaker
  conversion, unsupervised phoneme discovery) and video.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A discrete bottleneck can be trained end-to-end with straight-through plus a codebook loss | strong | it works, across three modalities, and everything since runs it |
| C2 | VQ-VAE avoids posterior collapse | moderate | the PixelCNN-decoder demonstration is the right experiment; it is one setting, and "avoids" is argued from the constant-KL structure rather than measured against a sweep |
| C3 | Discrete latents reach parity with continuous ones | moderate | 4.67 vs 4.51 bits/dim is close and is *worse*; parity is the paper's reading of its own number |
| C4 | `β` does not matter between 0.1 and 2.0 | moderate | stated, not tabulated, on the paper's own experiments |

## Method

Encoder produces a feature field; each position is replaced by its nearest
codebook entry; decoder reconstructs. Gradients from decoder input are copied
to encoder output. Codebook entries move toward encoder outputs by `L2`;
encoder outputs are pulled toward their assigned entries by `β`-weighted `L2`.
A PixelCNN is then trained over the resulting index field as the prior, which
is what makes it generative rather than merely compressive.

## Concepts

- **commitment loss** — the `β` term. Its stated purpose is scale control: the
  embedding space is dimensionless, so if the codebook trains slower than the
  encoder the encoder's outputs grow without bound.
- **straight-through estimator** — identity on the backward pass through a
  non-differentiable forward operation.
- **posterior collapse** — latents ignored because the decoder can model the
  data alone. The failure this paper's structure is built to sidestep.
- **learned prior** — the second half of the title and the half people forget.
  The uniform prior used in training is not the prior used for generation.

## Connections

Downstream in this record: [LIT-tmpb17dj](../literature.d/LIT-tmpb17dj.md) keeps this loss and adds
perceptual and adversarial terms; [LIT-tmpig8jj](../literature.d/LIT-tmpig8jj.md) and
[LIT-tmpflmiq](../literature.d/LIT-tmpflmiq.md) keep the tokenizer and change the prior;
[LIT-494](../literature.d/LIT-494.md) keeps the codebook and moves the quantization units
off the grid. The `extended_by` declaration records the first step; the rest
chain from there.

## Recommendations

- **R1** — use straight-through plus a separate codebook loss when you need a
  discrete bottleneck. **Not filed as a practice**: it is the definition of
  the object now, not a live choice, and a recommendation nobody can decline
  is not a recommendation.
- **R2** — `β = 0.25`, and do not spend time tuning it. **Not filed**: one
  paper's stated insensitivity on its own experiments, never revisited in this
  record's sources, and the descendants inherit the number without retesting
  it. A candidate if someone sweeps it.

## Bearing on the record

Gives the line a root. [SOTA-187](../practices.d/SOTA-187.md) — train the generative model in a
learned compressed latent — is the continuous sibling of this idea, and the
record held it without holding this. Both practices filed in this
contribution rest on later measurements of the object this paper defines.

## Limitations

- **The collapse claim is structural, demonstrated once.** Nothing quantifies
  how much collapse a comparable continuous model would have suffered in the
  same setting.
- **Codebook utilization is never measured**, which is the failure mode the
  whole downstream literature ends up organized around — and which
  [SOTA-tmpjm39m](../practices.d/SOTA-tmpjm39m.md) is about. `K = 512` in 2017 was small enough that
  the problem did not bite.
- **Reconstructions at 42.6× are not perceptually good** by later standards,
  which is precisely the gap [LIT-tmpb17dj](../literature.d/LIT-tmpb17dj.md) closes with a
  perceptual and adversarial loss. The paper is measuring likelihood, not
  perceptual quality, and the two diverge badly at high compression.
- **The straight-through estimator is biased** and the paper does not
  characterize the bias.

## Open questions

- **How much does `β` actually matter at modern codebook sizes?** The 0.1–2.0
  insensitivity was found at `K = 512` and has been carried unexamined to
  `K = 16384`, where utilization dynamics are completely different.
- **Does the posterior-collapse advantage survive?** Modern VQ tokenizers pair
  with adversarial decoders rather than autoregressive ones, and the argument
  was made against the latter.
