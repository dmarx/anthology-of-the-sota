---
status: Active
title: 'HunyuanVideo 1.5 Technical Report'
version: 1
tags:
- generative-modeling
- attention-techniques
- vision-and-graphics
- inference-optimization
date: '2026-10-06'
published: '2025-11-24'
arxiv: '2511.18870'
first_author: 'Wu'
keywords:
- 'video-generation'
- 'selective-and-sliding-tile-attention'
- 'block-sparse-attention'
- 'causal-3d-vae'
- 'video-super-resolution'
- 'glyph-aware-text-encoding'
- 'muon-optimizer'
- 'progressive-training'
- 'rlhf'
implementations:
- 'HunyuanVideo 1.5 (Tencent Hunyuan)'
- 'flex-block-attn (Tencent Hunyuan)'
# The same team's successor: its video data pipeline is built "upon the
# pipeline in" HunyuanVideo, and it keeps that model's MLLM text encoder
# with token refiner and its dual-stream blocks.
# SSTA's local half is the STA mask, used as published.
extends:
- LIT-620
- LIT-tmp1yfvi
# Tables 3-6: ratings and GSB against Wan2.2, cited to the Wan report.
compared_against:
- LIT-619
- LIT-tmpe78xc
summary: >-
  Tencent Hunyuan Foundation Model Team (2025), [ARXIV-2511.18870](https://arxiv.org/abs/2511.18870). An 8.3B
  dual-stream video DiT on a 16×16×4 causal VAE, with a cascaded
  super-resolution DiT to 1080p. Its sparse attention, SSTA, scores 3D
  key tiles by pooled query-key similarity minus key-key redundancy, keeps
  the top-k, and combines that mask with a Sliding Tile Attention window.
  It is switched on only during distillation. The one measured gain is
  speed: 2.95 against 5.51 s per step for 241 frames of 720p on 8 H800s
  (1.87×), but 1.28× at 121 frames. Tile size, window, k and sparsity are
  not given. No number compares output quality with and without SSTA.
---

# LIT-tmp1ecle: HunyuanVideo 1.5 Technical Report

Tencent Hunyuan Foundation Model Team (project leader Zhao Zhong; arXiv
lists Bing Wu first), Tencent (2025) — [ARXIV-2511.18870](https://arxiv.org/abs/2511.18870). Read at v2 (25 Nov
2025; v1 24 Nov 2025), the whole report: §§1–7, contributor list and
references. There are no appendices.

## Key takeaways

- **The model** (§3.1, Table 1). 54 dual-stream blocks, width 2048, FFN
  8192, 16 heads of dimension 128, 8.3B parameters, 3D RoPE. The VAE is a
  causal 3D transformer compressing 16× in each spatial axis and 4× in time
  into 32 channels. Text goes through Qwen2.5-VL with a token refiner plus
  Glyph-ByT5 for rendered text. For image-to-video, the image latent is
  concatenated on channels and SigLIP features are appended to the
  sequence. One model is trained jointly on T2I, T2V and I2V.
- **SSTA, as written** (§3.1, Algorithm 1). Q and K are cut into 3D tiles of
  tile_t × tile_h × tile_w tokens. Each tile is mean-pooled. A key tile's
  importance for a query tile is λ·(pooled q·k) − β·(mean pooled k·k
  similarity of that key tile to all other key tiles), so redundant key
  tiles are penalized. The top-k tiles form a selection mask, which is
  combined with a Sliding Tile Attention window mask of size
  (w_t, w_h, w_w) and run as block-sparse attention in a ThunderKittens
  kernel (flex-block-attn). The algorithm combines the two masks with ∧
  (line 20). Read literally, that keeps only selected tiles inside the
  window, which contradicts the stated aim of adding "dynamic global
  adaptive selection" to a local prior. The paper does not resolve this.
  Tile sizes, window size, k, λ and β are not reported.
- **When it is on** (§3.1). SSTA is "parameter-free" and "can be integrated
  at any training stage". It is enabled during the distillation phase, which
  the authors say "more effectively preserves output quality". No
  comparison with enabling it later, or with training-free use, is shown.
- **Speed** (§6, Tables 7–8). These are timings of the CFG-distilled model
  on 8 H800s with context parallelism. Without engineering acceleration,
  720p at 241 frames takes 5.51 s per step with FlashAttention-3 and 2.95 s
  with SSTA (1.87×). At 121 frames it is 2.01 against 1.56 s (1.28×). With
  SageAttention, torch.compile and feature caching, 50 steps at 720p take
  96.78 against 58.39 s at 241 frames (1.66×) and 28.33 against 26.41 s at
  121 frames (1.07×). Peak memory with offloading and VAE tiling is 13.6 GB
  for 720p at 121 frames on one GPU.
- **Training recipe** (§4, Table 2). Two T2I stages (256p on 5B images, 512p
  on 1B), then four mixed stages at a T2I:T2V:I2V ratio of 1:6:3, from 256p
  at 16 fps on 800M clips through 480p and 720p to 720p at 24 fps on 100M.
  The flow-matching shift is scheduled by token length, in the manner of SD3
  ([LIT-449](LIT-449.md)). Then come continued training on 1M clips per task, SFT, and
  RLHF. I2V uses online RL with MixGRPO and a VLM reward model. T2V uses
  offline DPO on human-annotated pairs and then the same online RL. Muon
  with weight decay 0.01 is used throughout.
- **Super-resolution** (§§3.2, 4.3). A second 8.3B DiT, initialized from the
  T2V model, takes the low-resolution latent through a separately trained
  latent upsampler, concatenated on channels, and refines it to 1080p. It is
  trained on 1M clips of 1K–4K.
- **Evaluation** (§5, Tables 3–6). T2V ratings: instruction following
  61.57 against Veo3's 73.77, structural stability 79.75 (best of five),
  aesthetic quality 63.30 (worst of five). GSB at 720p on 300 prompts, one
  sample each, over 100 assessors: T2V net win +17.12% against Wan2.2,
  +12.6% Kling2.1, +11.02% Seedance Pro, −10.32% Veo3. I2V: +12.65% Wan2.2,
  +9.72% Kling2.1, −5.77% Seedance Pro, −3.61% Veo3.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"End-to-end speedup of 1.87×"** (abstract, §1) is a per-diffusion-step
  ratio from Table 7, at 241 frames, without acceleration. It excludes the
  text encoders, the VAE and the super-resolution stage. With the
  acceleration stack deployed (Table 8) the same setting gives 1.66×, and at
  121 frames 1.07×. The table measures speed only.
- **SSTA has no quality evaluation.** No table or figure compares SSTA
  against full attention, against plain STA, or against selection alone, and
  its sparsity is never stated. It is unknown whether the Tables 3–6 models
  are the sparse or the dense ones. The redundancy term β·Score_r, the part
  that is new relative to pooled top-k selection, is not ablated.
- **The algorithm is not reproducible from the text.** No tile shape,
  window, k, λ or β is given. The mask combination is printed as ∧ where
  the prose implies a union. The redundancy score is normalized by 1/(N−1)
  with N defined as the tile size, though the sum runs over tiles. The
  released flex-block-attn code is the only way to settle these.
- **"State-of-the-art among open-source models"** rests on one open
  competitor, Wan2.2, rated on the authors' own undefined scales. Wan2.2
  beats HunyuanVideo 1.5 on aesthetic quality (65.98 against 63.30) and I2V
  image consistency (73.53 against 72.07). No public benchmark is reported.
  The GSB tables have one sample per prompt and no confidence intervals.
- **Muon "attains a lower training loss than AdamW in only half the
  number of training steps"** (§3.1) with no figure, model size or step
  count.
- **The training stages are not ablated**, and neither are the T2I warm
  start, the shift schedule, the SigLIP branch or the glyph encoder. Fig. 4
  shows the post-training stages as images only.

## Which comparisons are like for like

- **Tables 7 and 8** are the only controlled comparisons. They use the same
  model, hardware and frame count, with the attention backend switched
  between FlashAttention-3 (or SageAttention) and SSTA. They measure time
  only.
- **Tables 3–6** compare against other systems at their default settings,
  at different parameter counts, VAEs and resolutions. The tables say only
  "Wan2.2". §1 describes Wan2.2 as two 14B experts (27B in total) and
  also mentions its 5B variant. Which one was rated is not stated.
- **Table 4** includes a within-model comparison: 480p plus super-resolution
  against native 720p. The cascade wins on structural stability (70.13
  against 66.67) and loses on image consistency (68.82 against 72.07).

## Standing in the anthology

It extends HunyuanVideo ([LIT-620](LIT-620.md)), whose team wrote it. The video data
pipeline is described as built "upon the pipeline in" that report, and the
multimodal LLM text encoder with token refiner and the dual-stream block
carry over. Three things are new. The model is smaller (8.3B against 13B).
[LIT-620](LIT-620.md)'s 8×8×4 VAE is replaced by a 16×16×4 one. [LIT-620](LIT-620.md) used full
attention throughout, and this report adds a sparse path. Like [LIT-620](LIT-620.md), it
justifies its design choices by citation and reports no controlled
ablation of the model.

SSTA extends Sliding Tile Attention ([LIT-tmp1yfvi](LIT-tmp1yfvi.md)), whose window mask it
uses unchanged. What it adds is a dynamic top-k over 3D tiles, scored by
pooled similarity, with a penalty on key tiles that resemble the rest.
The tiles are 3D and spatiotemporal, but the paper does not measure the
difference against 1D runs. The tile shape is fixed and not reported. Its
comparison with Wan ([LIT-619](LIT-619.md)) is against Wan2.2, cited to the Wan report,
which describes Wan 2.1. It is a net GSB win of 17.12% for T2V and 12.65%
for I2V on the authors' 300-prompt sets.

For Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)), from the same organization, SSTA is a baseline.
Retrained by Prism at 2K at 85% sparsity, it scores AQ 0.43 and MotionQ
0.54, against full attention's 0.42 and 0.53. Prism's related-work section
describes this report as one that "scale[s] the training data". That is a
loose description of a report whose sparse attention is a published
algorithm. Nothing here bears on [SOTA-138](../practices.d/SOTA-138.md)'s indexer or warm-up. SSTA is
switched on during distillation, after dense training, but the paper
reports no evidence for that ordering.

Filed without a NOTE: the takeaways come from one full reading of v2, the
whole of a 14-page report. Figs. 1–5 are diagrams and sample frames, and
only values printed in the text and tables are quoted.
