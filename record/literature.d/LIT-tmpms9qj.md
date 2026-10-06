---
status: Active
title: 'Sparse VideoGen: Accelerating Video Diffusion Transformers with Spatial-Temporal Sparsity'
version: 1
tags:
- attention-techniques
- inference-optimization
- systems-optimization
- generative-modeling
date: '2026-10-06'
published: '2025-02-03'
arxiv: '2502.01776'
first_author: 'Xi'
keywords:
- 'sparse-attention'
- 'spatial-head'
- 'temporal-head'
- 'online-profiling'
- 'layout-transformation'
- 'training-free'
- 'video-diffusion-transformer'
- 'fp8-attention'
implementations:
- 'Sparse-VideoGen (svg-project)'
# Table 1: DiTFastAttn is run as the spatial-only baseline, and dense
# CogVideoX-v1.5 (I2V and T2V) and dense HunyuanVideo-T2V are the reference
# outputs every sparse method's PSNR/SSIM/LPIPS is measured against.
compared_against:
- LIT-tmp04qx6
- LIT-622
- LIT-620
- LIT-tmp5vqlh
- LIT-tmpmuiol
- LIT-tmpucn4v
summary: >-
  Xi, Yang et al., UC Berkeley, MIT, NVIDIA and Tsinghua (2025),
  [ARXIV-2502.01776](https://arxiv.org/abs/2502.01776). Training-free sparse attention for video DiTs. Each head
  is classified at every step as spatial (attends within a few whole frames)
  or temporal (attends to the same position across frames) by comparing both
  masks against full attention on 1% of sampled queries. The temporal mask
  is made contiguous by transposing frame-major to token-major order. At
  about 30% of attention computed and with the first 25% of steps dense, it
  reaches PSNR 28.2–30.0 against the dense output, ahead of spatial-only and
  temporal-only masks at similar FLOPs. HunyuanVideo's 2.33× needs FP8; sparse
  attention alone gives 1.92×. The abstract's Wan 2.1 1.51× has no table.
---

# LIT-tmpms9qj: Sparse VideoGen: Accelerating Video Diffusion Transformers with Spatial-Temporal Sparsity

Xi, Yang, Zhao, Xu, Li, Li, Lin, Cai, Zhang, Li, Chen, Stoica, Keutzer and
Han, UC Berkeley, MIT, NVIDIA and Tsinghua University (2025) —
[ARXIV-2502.01776](https://arxiv.org/abs/2502.01776). Read at v2 (27 Apr 2025), main text and Appendices A–B;
v1 is 3 Feb 2025.

## Key takeaways

- **Two head types** (§3.1, Fig. 3). In CogVideoX-v1.5 and HunyuanVideo the
  paper finds two attention patterns. A *spatial head* attends to tokens in
  its own frame and the frames next to it, which shows up as a block-diagonal
  map with block size set by the tokens per frame. A *temporal head* attends
  to the token at the same spatial position in every frame, which shows up as
  slashes at a stride of L, the tokens per frame. Text tokens and the first
  frame are kept in both masks. The footnote explains temporal heads by slow
  motion in the training data, and no experiment tests this.
- **The pattern changes with prompt and step, so it is chosen online** (§3.2,
  §4.1, Alg. 1). An oracle that runs full attention and keeps whichever mask
  has the lower MSE reaches PSNR above 29, but saves nothing. SVG instead
  samples a fraction of query rows, computes full, spatial and temporal
  attention for those rows only, and assigns each head the mask with the
  lower MSE. At 1% sampling, CogVideoX-v1.5-I2V scores PSNR 31.12 against
  31.32 for the 100% oracle and 30.79 at 0.1% (Table 3). The text puts the
  cost at about 3% of full attention. Table 3 gives no time column.
- **Masks are fixed windows, not selected blocks** (§3.3, §5.1). The spatial
  mask keeps c_s whole frames and the temporal mask keeps c_t positions
  across frames. With c_s = 4 frames and c_t = 1,224 tokens for CogVideoX-v1.5
  (11 latent frames × 4,080 tokens), and c_s = 10 and c_t = 1,200 for
  HunyuanVideo (33 × 3,600), each mask computes about 30% of full attention.
  The paper calls this "30% sparsity"; throughout, its "sparsity" is the
  fraction kept.
- **A layout transform makes the temporal mask fast** (§4.2, §5.5, Fig. 8).
  Strided keys cannot fill a tensor-core tile. Transposing the token-major
  tensor to a frame-major one puts the same position from every frame
  side by side, so the temporal mask becomes block-sparse. On the
  HunyuanVideo configuration the transformed kernel tracks the theoretical
  speedup, and at 10% kept it is 1.7× faster than the untransformed sparse
  kernel (3.63× over dense in the text, 3.66× in the figure).
- **Head to head** (Table 1, H100, 720p, first 25% of steps dense for every
  method). CogVideoX-v1.5-I2V: SVG PSNR 28.17 at 74.57 PFLOPs and 2.23×,
  DiTFastAttn (spatial only) 24.59 at 78.86 and 1.56×, temporal only 23.84 at
  70.27 and 1.61×, MInference 22.49 at 84.89 and 1.48×, PAB 23.23 at 105.88
  and 1.41×. CogVideoX-v1.5-T2V: SVG 29.99, against 23.20, 23.80, 22.45 and
  22.49, at 2.28×. HunyuanVideo-T2V: SVG 29.55 at 1.92×, with FP8 29.45 at
  2.33×; DiTFastAttn 21.42, temporal only 25.85, MInference 23.16.
- **Where the time goes** (Fig. 7, Table 2). On HunyuanVideo, 2,253 s falls
  to 968 s. Custom QK-norm and RoPE kernels give 1.06× (they are 7.4× and
  15.5× faster than PyTorch's in isolation), sparse attention 1.81×, and FP8
  attention 1.21×. FP8 is not used on CogVideoX-v1.5, whose head dimension
  of 64 leaves no speedup.
- **The budget can be lowered** (Table 4). On a VBench subset of
  HunyuanVideo, LPIPS is 0.154 at 13% kept, 0.135 at 18%, 0.141 at 35%,
  0.129 at 43% and 0.116 at 52%. Fixed c_s and c_t are chosen by hand per
  model. Adaptive budgets are left to future work.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"1.51× on Wan 2.1" has no measurement.** The sentence was added to the
  abstract in v2. Wan 2.1 appears only in Appendix B's stills (Figs. 10–11).
  No table or figure gives a Wan speedup, PSNR or VBench score.
- **The 2.33× headline includes FP8.** Sparse attention and the custom
  kernels give 1.92× on HunyuanVideo (Table 1, Fig. 7). The FP8 kernel is
  SageAttention-style quantization, a separate technique.
- **"PSNR above 30" (§2, App. A.1) is not what Table 1 shows.** The main rows
  are 28.17, 29.99 and 29.55. Higher numbers (31.1) come from Table 3's
  VBench subset, a different prompt set on the same model.
- **"Lossless" means PSNR about 29 against the dense output, after 25% of
  the steps ran dense.** The skipped first steps are applied to every
  method, so the ranking holds, but no row runs sparse from step one.
- **VBench does not rank SVG first.** On HunyuanVideo, DiTFastAttn has the
  highest ImageQual (67.33 against SVG's 65.90 and dense 66.11) and temporal
  only the highest SubConsist (98.53 against 93.51). On CogVideoX-I2V, PAB
  has the highest SubConsist (95.42 against 95.29). The claim to "consistently
  outperform all baselines" (§5.2) is about PSNR, SSIM and LPIPS.
- **One table row looks copied.** HunyuanVideo's temporal-only ImageQual and
  SubConsist (62.12%, 98.53%) are identical to CogVideoX-T2V's temporal-only
  values, although its PSNR and FLOPs differ. The dense HunyuanVideo
  ImageQual is 66.11%.
- **Table 4's caption says LPIPS falls as more is kept.** The values are not
  monotone: 0.135 at 18% is better than 0.141 at 35%.
- **No variance, and the subsets are unsized.** Every number is one run.
  Tables 3 and 4 use "a random subset of VBench" with no count.

## Which comparisons are like for like

- **SVG against spatial-only and temporal-only, Table 1.** These are close to
  an ablation of the per-head choice. Same model, prompts and dense warm-up,
  and FLOPs within 6% of SVG's (70.27 and 78.86 against 74.57 PFLOPs). Picking
  the pattern per head beats either fixed pattern by 3.6–6.8 PSNR on
  CogVideoX. On HunyuanVideo the three rows sit within 0.6% of each other in
  FLOPs (259.10–260.48), and SVG leads temporal only by 3.7 PSNR and spatial
  only by 8.1. The spatial-only row is DiTFastAttn ([LIT-tmp04qx6](LIT-tmp04qx6.md)), described as
  "spatial head only". The paper does not say whether it ran DiTFastAttn's
  own code, with its caching, or only its window mask.
- **MInference and PAB** ran "official configurations" at more FLOPs (84.89
  and 105.88). MInference is a language-model method, and PAB caches
  features across steps. Neither is at matched compute.
- **Fig. 8** holds the mask fixed and changes only the memory layout. It is
  the one clean measurement of the layout transform.

## Standing in the anthology

It is the record's earliest training-free sparse attention paper for video
DiTs, and the first of the Sparse VideoGen line. It does not group tokens
into 3D tiles. A spatial window is a run of whole frames in raster order,
and a temporal window is a column through time, made contiguous by a
permutation. Choosing between those two shapes is done per head, per step
and per prompt, from content (the sampled-query MSE). That makes it an
early content-chosen sparsity layout, but over two fixed anisotropic shapes,
not a block shape per region. It has no top-k or top-p selection: the
windows are fixed in size and position, and only the head's assignment
moves.

Sparse VideoGen2 ([LIT-tmpucn4v](LIT-tmpucn4v.md)), from the same group, ran it as the main
baseline at matched density and replaced its two fixed masks with k-means
clusters of queries and keys. At about 30% density with the same 30% dense
warm-up, SVG2 scores PSNR 25.81 against SVG's 22.99 on Wan 2.1 T2V and 26.56
against 24.06 on I2V, at almost the same speed (1.60× against 1.58× and 1.58×
against 1.56×). On HunyuanVideo, 30.45 at 25% density against 29.16 at 30%.
Without warm-up SVG falls to PSNR 12.3–15.6, against 16.5–19.9 for SVG2.
That is the record's evidence that the two-shape mask is the weaker design
once a content-defined grouping is available.

VMoBA ([LIT-tmpmuiol](LIT-tmpmuiol.md)) runs it as a training-free baseline at 0.50 density on
its fine-tuned Wan 2.1-1.3B. It cites SVG's per-head classification as the
costlier alternative to its own layer-index cycle of temporal, spatial and
3D blocks. VMoBA's shapes are fixed by layer, and SVG's are chosen from
content.

VSA ([LIT-tmp5vqlh](LIT-tmp5vqlh.md)) compares against it in a human study. Raters preferred
VSA's output to SVG's at 82.5% sparsity. VSA had also been fine-tuned on
Wan-14B outputs, while SVG ran on the original weights, so that study does
not isolate training as the cause.

The dense models it measures against are CogVideoX-v1.5 ([LIT-622](LIT-622.md)) and
HunyuanVideo ([LIT-620](LIT-620.md)). On both, Table 1 scores every sparse method by PSNR
against the dense model's own output, so the numbers are fidelity to that
model, not quality. Wan 2.1 ([LIT-619](LIT-619.md)) appears only in stills. Its block-sparse kernel is
built on FlashAttention ([LIT-074](LIT-074.md)) and FlashInfer, and the FP8 path follows
SageAttention, which is not in the record. SpargeAttention ([LIT-tmpxwbvb](LIT-tmpxwbvb.md)),
whose author list overlaps, is cited only in related work and is not
compared here.

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A–B, with v1 checked for the abstract's Wan sentence.
Figs. 3, 7 and 8 are maps and curves, and only values stated in the text or
labelled on the figure are quoted. Figs. 1, 6 and 9–11 are video stills and
were not assessed.
