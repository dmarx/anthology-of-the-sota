---
status: Active
title: 'LTX-2: Efficient Joint Audio-Visual Foundation Model'
version: 1
tags:
- generative-modeling
- multimodal-learning
- model-architecture
- inference-optimization
date: '2026-10-06'
published: '2026-01-06'
arxiv: '2601.03233'
first_author: 'HaCohen'
keywords:
- 'text-to-audio-video'
- 'asymmetric-dual-stream-transformer'
- 'bidirectional-audio-video-cross-attention'
- 'cross-modality-adaln'
- 'modality-aware-classifier-free-guidance'
- 'thinking-tokens'
- 'audio-vae'
- 'multi-scale-multi-tile-inference'
implementations:
- 'LTX-2 (Lightricks)'
extends:
- LIT-618 # same group's video latent space, data and backbone, with an audio stream added
compared_against:
- LIT-619 # per-step H100 timing against Wan 2.2-14B, cited to the Wan report
- LIT-tmpouvmz # human preference and speed against Ovi, reported without numbers
summary: >-
  HaCohen et al., Lightricks (2026), ARXIV-2601.03233. Extends LTX-Video into
  joint audio and video generation: a 14B video stream and a 5B audio stream
  exchange information through bidirectional cross-attention at every layer,
  using only the temporal part of RoPE. The one number is speed: 1.22 s per
  diffusion step against 22.30 s for Wan 2.2-14B at 121 frames of 720p on an
  H100 (Table 1). The quality claims rest on human studies and a public
  leaderboard with no counts, win rates or raters reported, and no component
  is ablated. It describes LTX-2 only, not the later LTX-2.3.
---

# LIT-tmpkvsya: LTX-2: Efficient Joint Audio-Visual Foundation Model

HaCohen, Brazowski, Chiprut, Bitterman and 25 others, Lightricks (2026) —
ARXIV-2601.03233. Read at v1 (6 Jan 2026), the only version, main text and
Supplementary A.1 (two figures).

## Key takeaways

- **Two streams of unequal width** (§3.1, Fig. 2). A 14B-parameter video
  stream and a 5B-parameter audio stream run at the same depth. Each block
  does self-attention within its modality, cross-attention to text,
  bidirectional audio-video cross-attention, then an FFN. Video uses 3D RoPE
  over (x, y, t) and audio 1D temporal RoPE. In the audio-video
  cross-attention only the temporal RoPE component is applied, so
  cross-modal attention is aligned in time and not in space (§3.1.1).
- **Timestep conditioning crosses modalities** (§3.1, §3.1.2). AdaLN
  modulation of Q and of (K, V) uses the stream's own timestep. The gate on
  the attended output uses the other modality's timestep. The stated purpose
  is to handle the two modalities sitting at different noise levels or
  temporal resolutions.
- **Separate latents per modality** (§1, §3.3). Video uses a
  spatiotemporal causal VAE "building upon" LTX-Video's latent space. Audio
  is stereo mel at 16 kHz through a causal audio VAE, one 128-dimensional
  token per 1/25 s. A HiFi-GAN vocoder with doubled channels turns the mel
  into a 24 kHz stereo waveform (§3.3.1).
- **Text conditioning** (§3.2). Gemma3-12B, frozen, with features taken
  from every decoder layer, mean-centred per layer, flattened and projected
  by a matrix W. W is trained briefly with the DiT and then frozen. A
  bidirectional "text connector", one per stream, appends learnable
  "thinking tokens" in place of padding before the DiT cross-attends to it.
- **Modality CFG** (§4.1). Each stream gets a text term and a cross-modal
  term: M̂ = M + s_t (M − M(x, ∅, m)) + s_m (M − M(x, t, ∅)). All results use
  s_t = 3, s_m = 3 for video and s_t = 7, s_m = 3 for audio.
- **High resolution by cascade, not natively** (§4.2). A base latent is
  generated at about 0.5 megapixels. A latent upscaler raises its spatial
  resolution, and overlapping spatial and temporal tiles are refined with
  the same model and blended in latent space before decoding to 1080p.
- **Speed** (§6.3, Table 1). At 121 frames of 720p, one Euler step and
  CFG = 1 on one H100, a step takes 1.22 s for LTX-2 (19B, audio and video)
  against 22.30 s for Wan 2.2-14B (video only), about 18×. Up to 20 s of
  video with audio is supported (§6.3).

## Where the hedges are

Per DP-010:

- **"State-of-the-art audiovisual quality … among open-source systems"**
  (abstract). The evidence is §6.1: "Our internal benchmarks indicate" LTX-2
  "significantly outperforms" Ovi and is "comparable" to Veo 3 and Sora 2.
  No prompt count, rater count, win rate or tie rate is given. The video-only
  claim is a leaderboard position (3rd image-to-video, 4th text-to-video on
  Artificial Analysis, as of 6 Nov 2025), not an experiment.
- **No component is ablated.** Thinking tokens give "significantly improved
  phonetic accuracy" (§2.2), the multi-layer extractor "yielded an
  improvement" (§3.2.1), and larger s_m gives better synchronization
  "empirically" (§4.1). None of these has a number. The asymmetric widths,
  the temporal-only RoPE in cross-attention and the cross-modality AdaLN
  have no comparison against an alternative.
- **The 18× is per step, with different latents.** Table 1 times one
  denoising step at the same pixel size. LTX-2's latent is LTX-Video's
  heavy compression and Wan's is not, so the ratio combines token count,
  width and architecture. VAE, text-encoder and upscaler costs are not
  included, and neither is the step count each model needs. "Faster than
  Ovi" (§6.3) is asserted with no timing.
- **The parameter counts disagree.** The abstract and §3.1 say 14B video and
  5B audio (19B in Table 1). The conclusion says "a pretrained 13B video
  diffusion transformer with a lightweight 3B audio stream".
- **The training recipe is absent.** The conclusion mentions "progressive
  joint training", which the body never describes. There are no steps,
  batch sizes, resolutions, learning rates or data sizes. The data is "a
  subset of the same dataset employed in LTX-Video" (§5), with captions from
  an in-house audio-visual captioner that is not evaluated.
- **The audio VAE and vocoder have no reconstruction metric**, as LTX-Video's
  video VAE had none.

## Which comparisons are like for like

- **Table 1** is the only quantitative comparison. Same GPU, frame count,
  resolution and solver settings. It compares a joint audio-video model with
  a video-only one, which favours Wan on workload.
- **The Wan model timed is Wan 2.2-14B**, cited to the Wan report
  (LIT-619), which describes Wan 2.1. The report does not describe the
  model in the table.
- **Nothing else is like for like.** The human studies and the leaderboard
  ranking have no stated protocol.

## Standing in the anthology

It extends LTX-Video (LIT-618). LTX-2 keeps LTX-Video's "spatiotemporal
latent space" and design principles (§1), trains on a subset of LTX-Video's
dataset (§5), and copies LTX-Video's compact-latent idea for audio (§3.3).
LIT-618's speed came from compressing the latent 1:8192, and Table 1 here
is that bet extended to a model with sound. The paper does not say whether
the video VAE or LTX-Video's denoising decoder is unchanged. LIT-618's
cross-attention-for-text choice carries over, now with an LLM encoder.

It compares against Wan (LIT-619) on speed only: 1.22 against 22.30 s per
step at 121 frames of 720p (Table 1). Against Ovi (LIT-tmpouvmz), the paper's
closest open joint audio-video rival, it claims better human preference and
higher speed. It reports neither with a number. It describes Ovi as
duplicating and combining existing T2V and T2A backbones (§2.1). LTX-2's
stated alternative is an audio stream narrower than the video stream.

**Which LTX it is.** This paper describes LTX-2 only. "2.3" does not appear
in it, and there is one arXiv version. Prism (LIT-tmpe78xc) and
daVinci-MagiHuman (LIT-tmpngzke) both compare against "LTX-2.3" and cite
this paper for it. Nothing in this paper says what changed in 2.3. What it
does fix is the shape of the LTX pipeline: a base at about 0.5 MP, a latent
upscaler, then tiled refinement to 1080p (§4.2). That supports Prism's
reading that its LTX baseline was not trained natively at 2K. It does not
confirm Prism's "720p" base, since §4.2 says 0.5 MP for LTX-2.

It has no sparse attention. Video self-attention is dense within each
stream, and audio-video cross-attention is dense with temporal RoPE. The
only spatiotemporal tiling is the inference-time latent tiling of §4.2,
which splits the generation into separate passes and does not restrict
attention inside one. Its gated cross-attention output is AdaLN-based and
is not the per-head sigmoid gate of SOTA-134.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and the supplementary figures. Figs. 1–5, A1 and A2 are diagrams and
attention maps, and only values stated in the text and Table 1 are quoted.
