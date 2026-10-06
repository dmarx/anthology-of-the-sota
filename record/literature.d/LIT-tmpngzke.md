---
status: Active
title: 'Speed by Simplicity: A Single-Stream Architecture for Fast Audio-Video Generative Foundation Model'
version: 1
tags:
- generative-modeling
- multimodal-learning
- model-architecture
- inference-optimization
date: '2026-10-06'
published: '2026-03-23'
arxiv: '2603.21986'
first_author: 'Chern'
keywords:
- 'single-stream-transformer'
- 'audio-video-generation'
- 'human-centric-generation'
- 'sandwich-architecture'
- 'timestep-free-denoising'
- 'per-head-gating'
- 'latent-space-super-resolution'
- 'dmd-2-distillation'
implementations:
- 'daVinci-MagiHuman (SII-GAIR, Sand.ai)'
compared_against:
- LIT-tmpkvsya # quality, WER and human preference against LTX 2.3, cited to the LTX-2 paper
- LIT-tmpouvmz # quality, WER and human preference against Ovi 1.1
- LIT-tmpe78xc
summary: >-
  SII-GAIR and Sand.ai (2026), [ARXIV-2603.21986](https://arxiv.org/abs/2603.21986). A 15B, 40-layer transformer
  denoises text, video and audio tokens in one sequence with self-attention
  only, sharing weights in the middle 32 layers. It has no timestep
  embedding, and gates each attention head. Distilled to 8 steps, it makes 5 s
  of 256p in 2.0 s and of 1080p in 38.4 s on one H100 (Table 2). Raters prefer
  it to LTX 2.3 in 60.9% of 1,000 pairs against 21.9%. No ablation tests any
  architectural choice. No competitor is timed, so the title's link from
  simplicity to speed is not measured.
---

# LIT-tmpngzke: Speed by Simplicity: A Single-Stream Architecture for Fast Audio-Video Generative Foundation Model

Chern, Teng, Sun and 40 others, project leads Cao and Liu, SII-GAIR and
Sand.ai (2026) — [ARXIV-2603.21986](https://arxiv.org/abs/2603.21986). Read at v1 (23 Mar 2026), the only
version, main text and Appendix A (author list). The report is five pages of
text.

## Key takeaways

- **One stream for every modality** (§2, Fig. 2). Text tokens, a reference
  image latent and noisy video and audio tokens share one sequence in a 15B,
  40-layer transformer. Self-attention is the only mixing. There is no
  cross-attention and no fusion module.
- **Sandwich layout** (§2). The first 4 and last 4 layers have
  modality-specific projections and RMSNorm parameters. The middle 32 share
  all parameters across modalities.
- **No timestep input** (§2). The model infers the noise level from the
  noisy latents themselves, following Sun et al. 2025 and Tang et al. 2025.
  There is no AdaLN and no timestep embedding.
- **Per-head sigmoid gate** (§2). Each head's output is multiplied by
  σ(g_h) before the output projection, citing the gated-attention work of
  [LIT-138](LIT-138.md). It is "introduced to improve numerical stability during training
  and to enhance model representability".
- **The inference stack** (§2). The base model generates at 256p. A
  dedicated super-resolution checkpoint upsamples the video latent
  trilinearly, adds noise and refines it in 5 steps, with the base-stage
  audio latent reused, noised, as input. At 1080p that checkpoint "enables
  local attention in many layers". Encoding uses the Wan2.2 VAE and decoding
  a retrained Turbo-VAED decoder. A full-graph compiler gives about 1.2× on
  H100. DMD-2 ([LIT-646](LIT-646.md)) distils the base model to 8 steps without CFG.
- **Latency** (Table 2, one H100, 5 s clip). 256p: 1.6 s base and 0.4 s
  decode, 2.0 s total. 540p: 8.0 s. 1080p: 1.6 s base, 31.0 s
  super-resolution, 5.8 s decode, 38.4 s total.
- **Automatic quality** (Table 1). VideoScore2 on VerseBench, then visual
  quality, text alignment and physical consistency: MagiHuman 4.80 / 4.18 /
  4.52, LTX 2.3 4.76 / 4.12 / 4.56, Ovi 1.1 4.73 / 4.10 / 4.41. WER on
  TalkVid-Bench, transcribed by GLM-ASR (character-level for CJK): 14.60%,
  19.23% and 40.45%.
- **Human preference** (Fig. 3). 10 raters each judge 100 pairs against each
  competitor, 2,000 judgements in all. Against Ovi 1.1: 80.0% win, 8.2% tie,
  11.8% loss. Against LTX 2.3: 60.9% win, 17.2% tie, 21.9% loss.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Speed by simplicity" is not measured.** Table 2 times only MagiHuman,
  and only the distilled model. No competitor is timed on the same
  hardware, and the undistilled single-stream base is not timed at all. The
  measured speed combines a 256p base, 8-step DMD-2 distillation without
  CFG, a 5-step latent super-resolution, a lightweight decoder and a
  compiler. The paper separates none of them from the architecture. The
  claim that single-stream computation is "hardware-friendly" is argued,
  not shown.
- **No architectural choice is ablated.** Single stream against dual
  stream, the 4–32–4 sandwich, timestep-free denoising and per-head gating
  are each adopted with a citation or a sentence of motivation. There is no
  comparison.
- **The automatic-score margins are small and unreplicated.** On VideoScore2
  the spread across all three models is 0.07 (visual quality), 0.08 (text
  alignment) and 0.15 (physical consistency), where LTX 2.3 leads. No seeds,
  sample counts or intervals are given. The WER gap is large, but TalkVid-Bench
  is a talking-head benchmark and MagiHuman is built for human-centric
  speech, so the benchmark matches its specialty.
- **"Highest … among leading open models"** (abstract) is a comparison with
  two models. MOVA, which the report cites, is not evaluated.
- **The human study does not say** where the prompts came from, who the 10
  raters were, at what resolution each model ran, or whether MagiHuman's
  clips came from the base or distilled model. Table 1 is silent on the same
  settings.
- **Nothing about training is reported.** There is no data, recipe, step
  count, resolution schedule, or size for the super-resolution checkpoint.
  The local attention at 1080p has no stated window or pattern, and its
  quality cost is not measured.

## Which comparisons are like for like

- **None in full.** Table 1 and Fig. 3 compare released models under their
  own pipelines. No retraining on shared data, no matched resolution or step
  count is stated.
- **The LTX baseline is LTX 2.3**, cited to the LTX-2 paper ([LIT-tmpkvsya](LIT-tmpkvsya.md)),
  which describes only LTX-2. The baseline is a later release than the
  cited document.
- **Table 2 is internally consistent.** The base stage is fixed at 256p, so
  the rows differ only in super-resolution and decode cost.

## Standing in the anthology

It is the record's single-stream counterpoint to the dual-stream joint
audio-video models in this batch. Against LTX 2.3, which descends from the
LTX-2 design ([LIT-tmpkvsya](LIT-tmpkvsya.md)), it reports 60.9% human wins against 21.9%,
better WER (14.60% against 19.23%) and VideoScore2 within 0.06. LTX 2.3
leads on physical consistency, 4.56 against 4.52. LTX-2 puts video and
audio in separate streams of 14B and 5B joined by cross-attention. Here
both share one set of middle-layer weights. Against Ovi 1.1 ([LIT-tmpouvmz](LIT-tmpouvmz.md))
the gaps are wider: 80.0% wins against 11.8%, and WER 14.60% against
40.45%. Neither comparison isolates the architecture, because the models
also differ in data, scale and inference pipeline.

Its attention is dense full self-attention over the joint sequence at the
256p base. The only restriction is the unspecified "local attention" in the
1080p super-resolution checkpoint. It therefore takes the opposite route to
Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)), which keeps audio separate and makes video attention
block-sparse at native 2K. MagiHuman avoids the long sequence by generating
at 256p and refining in latent space. It is a second instance, after
LTX-2's cascade, of an open joint model that reaches 1080p by latent
upscaling rather than native high-resolution training. That supports
Prism's framing of the alternative.

The per-head gate is the practice of [SOTA-134](../practices.d/SOTA-134.md), from [LIT-138](LIT-138.md), applied here to
a diffusion transformer. This paper is adoption, not evidence for it in
that setting, since no arm removes the gate ([DP-005](../../docs/design-principles.md#dp-5)). The 8-step student is
DMD-2 ([LIT-646](LIT-646.md)) used off the shelf.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and author appendix. Figs. 1–2 are samples and a diagram, and Fig. 3's
percentages are stated in the text.
