---
status: Active
title: 'UltraGen: High-Resolution Video Generation with Hierarchical Attention'
version: 1
tags:
- attention-techniques
- generative-modeling
- vision-and-graphics
- adaptation-and-tuning
date: '2026-10-06'
published: '2025-10-21'
arxiv: '2510.18775'
first_author: 'Hu'
keywords:
- 'native-high-resolution-video-generation'
- 'global-local-attention-decomposition'
- 'spatially-compressed-global-attention'
- 'cross-window-local-attention'
- 'hierarchical-local-attention'
- 'domain-aware-LoRA'
- 'time-aware-fusion'
- 'HD-FVD'
implementations: []
# The model is Wan-1.3B with its attention split into three branches; all
# branches reuse Wan's projections, two through LoRA residuals.
extends:
- LIT-619
# Table 1-3: Wan and HunyuanVideo native and +SR, CogVideoX +SR.
# Table 4: local branch replaced by Swin attention.
compared_against:
- LIT-619
- LIT-620
- LIT-622
- LIT-723
- LIT-tmpe78xc
- LIT-tmpva88i
summary: >-
  Hu, Zhang, Su and Yi, Shanghai Jiao Tong and Zhejiang University (2025),
  [ARXIV-2510.18775](https://arxiv.org/abs/2510.18775). Wan-1.3B is fine-tuned for 1080P and 4K with its
  self-attention split into three branches. A local branch uses 4×4 spatial
  windows that span every frame and alternate with 5×5 windows between
  layers. A global branch runs on a latent downsampled by a strided
  convolution, and an intermediate branch uses 2×2 coarse windows. The theory
  gives 12× fewer attention FLOPs, and 4K inference is 4.78× faster than Wan.
  On its own HD-FVD it beats every native and super-resolved baseline (214 at
  1080P, 425 at 4K), but loses CLIP score to Wan plus super-resolution. The 4K
  model is trained on only 29 frames. Every number is one run.
---

# LIT-tmp8ew94: UltraGen: High-Resolution Video Generation with Hierarchical Attention

Hu, Zhang, Su and Yi, Shanghai Jiao Tong University and Zhejiang University
(2025) — [ARXIV-2510.18775](https://arxiv.org/abs/2510.18775). Read at v1 (21 October 2025), the only version,
main text and Appendices A–H.

## Key takeaways

- **Three attention branches, fused by timestep** (§4.1, Eq. 3, Fig. 2). The
  local branch attends inside spatial windows. The global branch attends over
  a spatially compressed copy of the whole video. A time-aware fusion
  α(t) = MLP(SinEncode(t)), a D-dimensional gate, mixes the two outputs, with
  the stated intent of global structure early in denoising and detail late.
  The same kind of gate fuses the two local sub-branches.
- **The local windows are 2D in space and full in time** (§4.3, Eq. 6).
  The latent is cut into K×K non-overlapping windows over (H, W) only. Each
  window keeps all T latent frames, so it is a T × H/K × W/K tube. K = 4
  (App. B). Even layers use K×K windows and odd layers use (K+1)×(K+1), so
  window boundaries in adjacent layers cross. This replaces Swin's shift. The
  paper does not say how a (K+1)-way split of a K-divisible grid is padded.
- **Global context comes from compression, not sparsity** (§4.2, Eqs. 4–5).
  A depthwise k×k convolution with stride k, initialized to average pooling,
  shrinks each frame. Attention runs over all frames at H/k × W/k. Bilinear
  upsampling and a 3D convolution then restore the resolution. The global
  branch uses Wan's Q/K/V and FFN weights plus a rank-64 LoRA residual
  ("domain-aware LoRA").
- **A third, intermediate scale** (§4.3, Eqs. 10–11). Hierarchical local
  attention uses (K/2)×(K/2) coarse windows, each 2× downsampled by a strided
  convolution so that its token count matches a local window. It alternates
  between K/2 and K/2+1 partitions and has its own LoRA.
- **Cost** (App. B, Eq. 12). Counting attention-map FLOPs only, the three
  branches cost (THW)²D · (5/(4K²) + 1/K⁴), a 4K⁴/(5K²+4) speedup. That is
  about 12× at K = 4. The appendix says the measured gain is lower because
  of the extra Q/K/V (and FFN) passes of the global and hierarchical
  branches. Measured end-to-end inference (Table 2): at 1080P, 13 min against
  35 for Wan and 43 for HunyuanVideo (2.69×). At 4K, 1 h 50 min against
  8 h 46 min for Wan and 11 h 36 min for HunyuanVideo (4.78×). Fig. 1 gives
  the setting as 81 frames on 4×H20.
- **Recipe** (App. C). Full fine-tuning of Wan-1.3B plus rank-64 LoRA for
  the global and hierarchical branches. UltraVideo (42K 4K clips), 50 epochs,
  32 H20 GPUs, batch 32, lr 1e-4. The 1080P model is trained on 81 frames
  and the 4K model on 29 frames, for memory. Inference uses 30 steps at
  CFG 5.0.
- **Results** (Table 1). At 1080P, HD-FVD is 214.12, against 237.89 for
  native HunyuanVideo and 238.75 for HunyuanVideo plus super-resolution, with
  the best HD-MSE, HD-LPIPS and temporal consistency. At 4K, HD-FVD is
  424.61, against 453.41 for HunyuanVideo plus SR, and native HunyuanVideo
  and Wan score 805 and 1,272. CLIP-L is best among native methods (0.2654 at
  1080P), but below Wan plus SR and HunyuanVideo plus SR (0.2747–0.2883).
  VBench average (App. E, Table 3): 0.8536 at 1080P and 0.8460 at 4K, the best
  of the methods shown. At 4K, HunyuanVideo leads on subject and background
  consistency.
- **Ablations** (§5.3, Fig. 6; App. F, Table 4; 1080P, since the full-model
  row equals Table 1's 1080P row). HD-FVD for each removal: global branch
  328.98, cross-window alternation 419.15, hierarchical branch 376.49,
  domain-aware LoRA 284.08. Swin attention in place of the local scheme gives
  458.93, against 214.12 for the full model. Removing the global branch gives
  repeated objects across windows ("16 golden fishes", Fig. 6).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **Its own metrics decide the comparison.** HD-FVD, HD-MSE and HD-LPIPS
  are introduced here (App. D). HD-MSE and HD-LPIPS reward energy lost when
  a frame is downsampled and upsampled again, with higher being better. They
  cannot tell detail from high-frequency noise. Native Wan at 1080P has the
  lowest HD-MSE (42.93) because it is blurred, and UltraGen the highest
  (390.19). Neither the number of prompts nor the reference set for HD-FVD is
  stated.
- **"First native 4K" carries a 29-frame footnote.** The 4K model trains on
  29 frames (App. C, G). Table 2's 4K timing is given in Fig. 1 as an
  81-frame run, and the paper does not reconcile the two settings. Step
  counts for the Wan and HunyuanVideo timings are not stated, while UltraGen
  uses 30. If the baselines ran Wan's default of 50 steps, about 1.7× of the
  4.78× comes from the step count.
- **Native baselines are untuned at the target resolution.** Wan and
  HunyuanVideo are run zero-shot at 1080P and 4K. No full-attention Wan
  fine-tuned on the same UltraVideo data is shown, so the table does not
  separate the attention design from the fine-tuning.
- **The ablation favours the full model on the paper's own metrics, not
  uniformly.** In Table 4, removing the hierarchical branch gives higher
  subject consistency (0.9800 against 0.9771) and background consistency
  (0.9821 against 0.9777). Removing domain-aware LoRA gives higher imaging
  quality (0.7424 against 0.7350). The full model wins on HD-FVD, CLIP-L,
  aesthetic quality and the VBench average. All rows are single runs.
- **No ablation of window size or window shape.** K = 4 is the only setting.
  No variant partitions time, and none uses a different number of windows.
- **No code or checkpoint is named in the paper**, only a project page.

## Which comparisons are like for like

- **Table 4** is controlled: every ablated variant is trained on the same
  recipe and evaluated at 1080P. It is the only evidence about which branch
  matters. The Swin variant isolates the local partitioning scheme: shifted
  windows against alternating K×K and (K+1)×(K+1) partitions, with both
  global branches kept.
- **Table 1's "+SR" rows** run each base model at its native resolution
  followed by the same super-resolution model (RealViformer). Among them,
  cascades win on CLIP-L, which the paper concedes in §5.2.
- **Table 2** compares a fine-tuned 3-branch model with two untuned dense
  models. The step counts are not shown to match.

## Standing in the anthology

It extends Wan ([LIT-619](LIT-619.md)): the generator is Wan-1.3B with its attention
recomputed, and every branch reuses Wan's projections. Wan is also the main
baseline. Run natively at 4K, Wan scores HD-FVD 1,272 against UltraGen's 425,
and the speedup claims are measured against its inference time. HunyuanVideo
([LIT-620](LIT-620.md)) is the strongest baseline, both natively and with super-resolution:
its SR cascade comes closest on HD-FVD and beats UltraGen on CLIP-L.
CogVideoX ([LIT-622](LIT-622.md)) appears only with super-resolution, because it cannot
generate at HD natively, and it is last on HD-FVD at both resolutions.

Replacing the local scheme with Swin's shifted windows ([LIT-723](LIT-723.md)) costs 245
HD-FVD points at 1080P. The paper reads this as Swin connecting windows
without capturing hierarchical structure. T3 ([LIT-tmpva88i](LIT-tmpva88i.md)), from an
overlapping author list, finds the same direction at 720P.

T3 is the direct successor. It reports +4.29 VQA over UltraGen's released 4K
model, though at 81 against 29 frames. T3 states UltraGen's training budget
as 128 H20 GPUs, but this paper's own appendix gives 32. The two designs
split the problem differently. UltraGen keeps every window full in time and
2D in space, with a separately parameterized compressed global branch. T3
uses 3D windows that vary by layer and a weight-shared strided global path.

Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)) lists UltraGen in its Table 5 under "Training-Free",
applied at 2K to a backbone pretrained only at 720p (Prism §4). That does not
describe this paper. UltraGen is a 50-epoch full fine-tune at the target
resolution with new convolutions, fusion MLPs and LoRA branches (App. C).
Untrained, those new modules would not exist, so Prism's 0.43 aesthetic
score measures something other than the method as published. Prism's
related work groups UltraGen and T3 as "fixed-shape windows". That is
accurate for UltraGen's K×K tubes.

Filed without a NOTE: the takeaways come from one full reading of v1,
including the appendices. Figures 4–9 are qualitative and were read only
through their captions and the text that cites them.
