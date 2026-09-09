---
status: Read
paper: LIT-062
title: 'Latent Diffusion Models'
version: 1
tags:
- generative-modeling
date: '2026-09-09'
summary: >-
  Train the diffusion model in the latent space of a pretrained autoencoder rather than in pixels. The autoencoder removes imperceptible detail; the diffusion model then spends its capacity on semantics instead of on high-frequency content nobody sees.
---

# NOTE-tmp17ke7: Latent Diffusion Models

## Contribution

Diffusion models operating in pixel space spend most of their compute
modelling detail that contributes almost nothing perceptually, which makes
both training and sampling expensive at high resolution. This paper splits
the problem: a **pretrained autoencoder** compresses images to a lower-
dimensional latent space that is **perceptually equivalent**, and the
diffusion model is trained there. The compression is done once and reused
across many diffusion models.

## Key insight

Generative modelling of images has two stages that were being done at once
and want different machinery. Removing imperceptible high-frequency detail is
a *compression* problem, solved well by an autoencoder with a perceptual
objective; modelling the semantic structure that remains is a *generative*
problem, and the diffusion model should only be asked to do that one.

The separation is what buys everything else: the latent space is small enough
that high resolutions become tractable, and because the autoencoder is
trained once, its cost amortises over every model built on it.

## Assumptions

- The autoencoder's latent space is **perceptually equivalent** to pixel
  space — that is the load-bearing assumption, and what the perceptual
  objective is for. Anything the autoencoder discards is unavailable to the
  diffusion model no matter how good it is.
- The compression rate is a real trade: too little and the latent is not much
  cheaper, too much and semantics are lost with the detail.
- Image domains at 2021 scales.

## Key results

- **Diffusion in a learned latent space** rather than in pixels, on a
  pretrained autoencoder.
- **The autoencoder is trained once and reused** across diffusion models —
  the amortisation argument.
- Substantially reduced training and sampling cost at a given resolution, and
  high-resolution synthesis made practical.
- Conditioning is introduced into the latent-space denoiser rather than
  bolted onto pixel space.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Most of a pixel-space diffusion model's capacity goes to perceptually irrelevant detail | strong | the paper's premise, supported by the compression working at all |
| C2 | A perceptually-equivalent latent space can be learned once and reused | strong | demonstrated across models |
| C3 | Diffusion in that latent is much cheaper at equal quality | strong | measured |
| C4 | The compression rate trades cost against semantic fidelity | moderate | explored, not reduced to a rule |

## Method

Train an autoencoder with a perceptual objective to map images to a compact
latent. Freeze it. Train a diffusion model on the latents, with conditioning
introduced into the denoiser. Sample in latent space and decode.

## Concepts

- **Perceptual equivalence** — the property the autoencoder must have for the
  split to be sound: what it discards is what a viewer would not notice.
- **The two-stage split** — compression then generation, as distinct
  problems with distinct objectives. The paper's real contribution, and the
  part that transfers.

## Connections

Its immediate ancestors are pixel-space diffusion and the VQ-style
autoencoder literature; its descendants are essentially every practical
image generator. The **train-in-a-learned-latent** move is the same shape
several practices in this record make for other modalities.

## Recommendations

- **R1** — Train the generative model in a learned compressed latent, not at
  full resolution. *Topic:* generative modelling. *Status:* standard.
  *Strength:* strong. *Applies when:* the signal has a perceptually
  irrelevant component, which images and audio both do.
- **R2** — Separate compression from generation and give each its own
  objective. *Topic:* architecture. *Status:* standard. *Strength:* strong.
  *Applies when:* one model is being asked to do both; the general form of
  the contribution.
- **R3** — Amortise the compressor. *Topic:* systems. *Status:* standard.
  *Strength:* moderate. *Applies when:* several generative models will share
  a domain — the autoencoder is trained once.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-187](../practices.d/SOTA-187.md) train the generative model in a learned compressed latent, not at full resolution | confirmed — C1 through C3 |

The reading adds the condition the practice most needs: the latent must be
**perceptually equivalent**, and whatever the autoencoder discards is gone
for good. That is not a caveat about quality margins — it is a hard ceiling
the diffusion model cannot see past, and it is why the compression rate is a
decision rather than a default.

## Limitations

- Images at 2021 resolutions and scales.
- C4 is explored rather than resolved: there is no rule for choosing the
  compression rate.
- The autoencoder's failure modes become the system's failure modes, and are
  not characterised here.

## Open questions

- What does the autoencoder discard that turns out to matter? The ceiling is
  acknowledged and never measured.
- R2 — separate compression from generation — is stated here for images.
  The record has no equivalent statement for text, where the analogous split
  would be the tokenizer.
