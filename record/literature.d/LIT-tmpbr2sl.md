---
status: Active
title: 'Wan: Open and Advanced Large-Scale Video Generative Models'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- representation-and-encoding
- data-pipeline
- distributed-optimization
- multimodal-learning
date: '2026-09-24'
published: '2025-03-01'
arxiv: '2503.20314'
first_author: 'Wan Team'
keywords:
- 'video-generation'
- 'text-to-video'
- 'image-to-video'
- 'diffusion-transformer'
- 'flow-matching'
- 'causal-video-vae'
- 'context-parallelism'
implementations:
- 'Wan2.1-T2V-14B'
- 'Wan2.1-T2V-1.3B'
- 'Wan2.1-I2V-14B'
extends:
- LIT-448
- LIT-449
- LIT-tmpmi3yo
compared_against:
- LIT-tmpkcchp
- LIT-tmplthcn
- LIT-tmpqns7l
summary: >-
  Wan Team, Alibaba (2025), [ARXIV-2503.20314](https://arxiv.org/abs/2503.20314). The open Wan2.1 video models,
  1.3B and 14B, and the full recipe behind them. The recipe covers data
  curation, a 127M causal 3D VAE compressing 4×8×8, a cross-attention DiT
  trained by rectified flow on an image-then-video resolution curriculum, the
  2D context parallelism it needs, and a mask-conditioned image-to-video
  variant. The abstract claims video scaling laws in data and model size, but
  the report plots no scaling curve.
---

# LIT-tmpbr2sl: Wan: Open and Advanced Large-Scale Video Generative Models

Wan Team, Alibaba (2025) — [ARXIV-2503.20314](https://arxiv.org/abs/2503.20314)

## Key takeaways

- **It discloses a recipe.** Weights, code, data pipeline, VAE, training
  schedule, parallelism and inference tricks are all published for a model
  that its authors' own benchmark and blind human preference put ahead of the
  closed systems it names. It is the video counterpart of an open language
  model report.
- **Backbone.** A DiT with cross-attention to umT5 text embeddings, full
  spatio-temporal self-attention over latent patches, and a rectified-flow
  velocity loss with logit-normal timesteps, following [LIT-449](LIT-449.md). One
  timestep MLP is shared across all blocks, with a learned bias per block,
  instead of a separate adaLN MLP in every block. This saves about 25% of
  parameters.
- **Wan-VAE.** A 127M 3D causal VAE compresses 4× in time and 8×8 in space
  into 16 channels, and the first frame is compressed spatially only, so
  images and videos share one latent. GroupNorm is replaced with RMSNorm to
  keep it causal, which lets a chunked feature cache encode and decode
  arbitrarily long video in bounded memory. It is inflated from a 2D image
  VAE rather than trained from scratch.
- **The curriculum.** It starts with 256px text-to-image pre-training, then
  joint image and video training at 192px, 480px and 720px. The reason given
  is systems, not quality. At 81 frames of 720p, throughput and memory force
  small batches, and the report attributes loss spikes to the resulting
  gradient variance.
- **Attention dominates at video sequence lengths.** Sequences run to
  hundreds of thousands of tokens, and at 1M tokens attention is up to 95% of
  step time. The response is FSDP for parameters and a 2D context
  parallelism, Ring Attention outside and Ulysses inside, in place of tensor
  parallelism. At 256K tokens on 16 GPUs this cuts communication overhead
  from over 10% to under 1%. Activation offloading is preferred over
  checkpointing because compute grows quadratically in sequence length while
  memory grows linearly, so transfers can hide behind compute.
- **Image-to-video is a channel-concatenation recipe.** The conditioning
  frame is padded with zero frames and VAE-encoded. It is concatenated on the
  channel axis with the noise latent and a binary mask of which frames are
  given, and a zero-initialized projection absorbs the extra channels. The
  same mask trains image-to-video, continuation, first-and-last-frame
  interpolation and random-frame interpolation as one task. A CLIP image
  embedding enters through decoupled cross-attention in fine-tuning only.
  Training clips are kept only when the first frame's SigLIP features are
  close to the mean of the rest. Early runs failed to learn stable
  image-driven generation without that filter.
- **Where the hedges are.** Per [DP-010](../../docs/design-principles.md#dp-10):
  - The abstract says the 14B model "demonstrates the scaling laws of video
    generation with respect to both data and model size". Nothing in the
    body plots either axis. The evidence is two model sizes.
  - All three ablations run on the 1.3B model, on text-to-image, and two of
    them are judged by training loss. On the one measured by FID (Table 6),
    Qwen-VL-7B's second-last layer scores 42.91 against umT5's 43.01. umT5
    was kept for its size, not because it generated better.
  - "Minimal contamination (< 10%) by generated images can significantly
    degrade the performance" is asserted with no experiment.
  - The comparisons against commercial models use anonymized opponents and
    the authors' own Wan-Bench. On image-to-video matching, Wan loses to
    CN-TopA (−4.2%, Table 7).

## Standing in the anthology

**This is the report [LIT-218](LIT-218.md) said the record was missing.**
[LIT-218](LIT-218.md)'s note ends by asking for "a frontier video training report with a
disclosed recipe — the video equivalent of what [LIT-139](LIT-139.md) or [LIT-131](LIT-131.md) are
for language". Before this note, the record held the backbone
([LIT-448](LIT-448.md)) and the objective ([LIT-449](LIT-449.md)), but no video model
built from them.

It is filed as a source and has not been mined yet. Candidate practices, each
of which would need its evidence checked against this text first:

- Pre-train a video diffusion model on images at low resolution, then raise
  resolution before adding length. The report justifies this by throughput,
  and it has no ablation. The image-first half is now [SOTA-tmp3b17n](../practices.d/SOTA-tmp3b17n.md),
  sourced from the earlier controlled studies. Wan is adoption of it, not
  evidence. The resolution-then-length ordering is still unfiled.
- Condition image-to-video by channel-concatenating a masked latent through a
  zero-initialized projection, and filter clips by how close the first frame
  is to the rest. This is the report's most transferable engineering.
- Use context parallelism rather than tensor parallelism once attention
  dominates. This bears on the record's distributed-training practices, and
  the 10%→1% figure is measured.

It is adoption evidence for [SOTA-187](../practices.d/SOTA-187.md), not a source for it: Wan
trains in a learned latent and does not test that choice against anything
else ([DP-005](../../docs/design-principles.md#dp-5)). Its VAE ablation compares two latents
(reconstruction loss against diffusion loss), not latent against pixel.

**Tags.** `generative-modeling` comes first because the report's subject is
the generator. `vision-and-graphics` is there because this is a visual
foundation model. `representation-and-encoding` covers Wan-VAE, a learned
latent designed for its compression ratio and causality. `data-pipeline`
covers a third of the report, including the motion-quality tiers.
`distributed-optimization` covers the parallelism and memory analysis.
`multimodal-learning` covers the text-encoder ablation and the image branch
of image-to-video. The FP8 attention work (§4.4.3) and the diffusion cache
(§4.4.2) are real but each takes about a page, so they are left as candidates
for `numerics-and-precision` and `inference-optimization` if that material
is ever mined. No new topic was needed: the vocabulary already names both
the generator and the modality.
