---
status: Active
title: 'Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification'
version: 1
tags:
- attention-techniques
- inference-optimization
- systems-optimization
- generative-modeling
date: '2026-10-06'
published: '2026-07-27'
arxiv: '2607.24027'
first_author: 'Li'
keywords:
- 'training-free-sparse-attention'
- 'block-sparse-attention'
- 'threshold-routing'
- 'query-dependent-threshold'
- 'online-softmax'
- 'proxy-score-reuse'
- 'approximate-correction'
- 'video-diffusion-transformer'
implementations:
- 'Sol-Engine (NVIDIA)'
# The kernel is FlashAttention's tiled online softmax with routing and an
# approximate branch fused into the same pass; it is defined by that loop.
extends:
- LIT-074
# Tables 1-3 and 5, Fig. 5c: Sparse VideoGen2 at matched sparsity on Wan,
# HunyuanVideo, LTX 2.3, SANA-WM and Bernini, and its routing memory.
# Table 1: dense Wan 2.1-14B and HunyuanVideo-13B are the reference rows.
compared_against:
- LIT-tmpucn4v
- LIT-619
- LIT-620
summary: >-
  Li, Li et al., NVIDIA (2026), ARXIV-2607.24027. Training-free block-sparse
  attention for video DiTs. Each query block keeps the key blocks whose
  pooled score exceeds its own mean plus β standard deviations. The test runs
  inside the online-softmax loop, so no score map is written out, and dropped
  blocks are approximated from their pooled key. At about 85% sparsity it
  runs 2.02× end to end on Wan 2.1 and 2.12× on HunyuanVideo, against
  1.86× and 1.88× for PISA, the first author's earlier method. Quality is
  level with PISA, which wins on HunyuanVideo. The threshold rule is never
  ablated for output quality, and every number is one run.
---

# LIT-tmpx3dxt: Sol-Attn: Accelerating Video Generation Inference via On-the-Fly Attention Sparsification

Li, Li, Chen, Ye, Liu, Yu, Wang, Zhang, Xie, Xie and Han, NVIDIA (2026) —
ARXIV-2607.24027. Read at v1 (27 Jul 2026), the only version, main text and
Appendices A–C.

## Key takeaways

- **The routing rule** (§3.1, Fig. 3, Eq. 4). Block scores are the dot
  products of mean-pooled query and key blocks. Pooled over steps, layers,
  heads and rows, the standardized scores are close to Gaussian in Wan 2.1,
  HunyuanVideo 1.5 and LTX 2.3. Query block i keeps key block j when its
  score exceeds τ_i = μ_i + βσ_i. One β sets the mean density near
  1 − Φ(β), about 16% at β = 1, and the count still varies per query. μ_i
  and σ_i come from the first and second moments of the pooled keys (Eq. 5,
  App. B), in O(Ld + Nd²) time, without the N×N score map. A diagonal
  version is O(d) per query block.
- **Routing inside the kernel** (§3.2, Fig. 4, Algorithm 1). An outer loop
  streams chunks of pooled keys and scores them against the query block.
  Columns whose mean clears τ_i go to an inner loop that computes exact
  attention over the original 64-token key-value blocks. All other columns
  enter the same online-softmax state through a zeroth-order Taylor term:
  each skipped block contributes B·exp(q·K̄_j) to the denominator and
  exp(q·K̄_j)·ΣV_j to the numerator (Eqs. 8–10). The score tile is computed
  once and used both for routing and for the correction (Eq. 11). App. B
  bounds the error: second order in the within-block score spread for the
  denominator, first order and value-weighted for the numerator.
- **Kernel cost** (§4.2, Fig. 5, Fig. 10; H100). Over FA3 the kernel is
  5.41× faster at 128K tokens and 90% sparsity. Routing takes 0.33 ms
  against 3.80 ms for top-k and 10.8 ms for top-p (11.5× and 32.7×).
  Attention-processor memory is 1.45 GB and 1.48 GB on LTX 2.3 and Bernini,
  close to dense at 1.42 GB and 1.46 GB. SVG2 needs 11.52 GB and 11.67 GB.
  Against cuDNN block-sparse attention on identical block indices at 32K, the
  correction branch adds 9.4%, 3.9% and 1.6% kernel time at 10%, 15% and 20%
  density. With BSA's separate routing stage counted, Sol-Attn is 6.2–6.6%
  faster end to end.
- **Text-to-video at matched sparsity** (Table 1). Wan 2.1-14B, 720p, 81
  frames, at about 85% sparsity: VBench 76.13 against dense 75.90, PSNR
  20.59, 2.02×. PISA scores 76.03 / 20.28 at 1.86×, SVG2 75.22 / 20.71 at
  1.85× (83.66% sparsity), XAttn 74.84 / 18.62 at 1.69×. HunyuanVideo-13B,
  129 frames: Sol-Attn 76.81 / 25.21 at 2.12×, PISA 77.02 / 25.58 at 1.88×,
  SVG2 74.45 / 25.64 at 2.01×, dense 77.06. LTX 2.3-22B at 1080p, sparse in
  stage 2 only: 74.69 / 25.69 at 1.9× end to end (2.4× in stage 2), PISA
  74.67 / 25.26 at 1.8×, SVG2 71.98 / 21.94 at 1.7×.
- **Video-to-video and images** (Tables 2–5). On SANA-WM one-minute
  refinement, three steps all sparse, Sol-Attn runs 3.04× against PISA's
  2.35×, with rotation error 8.78 against PISA's 8.82 and dense 7.13. On
  Bernini editing it runs 2.34× against 2.17×, at PSNR 30.18 against 29.88.
  On Ideogram 4 at 2K the Qwen-Image-Bench average is 55.31 against dense
  59.24, PISA 54.51 and plain block-sparse attention 51.96. Sol-Attn runs
  1.56× there, BSA 1.54×. On an RTX 5090 with Wan 2.1-1.3B at 480p it scores
  PSNR 24.70 at 1.71×, SVG2 24.08 at 1.41×.
- **Ablations at the operator level** (§4.5, Figs. 8–9). At a mean density
  of 15%, per-query densities stay tightly grouped under the threshold rule.
  Top-p spreads them widely, and top-k fixes them by construction. With the
  same selected blocks, the correction term lowers relative ℓ2 error and
  raises cosine similarity to dense attention, more so at higher sparsity
  (32K tokens, curves only).
- **In a full engine** (§4.4, Fig. 7; B200). Kernel fusion, then step
  caching, then Sol-Attn take HunyuanVideo from 866.9 s to 170.6 s (5.08×)
  and Wan 2.1-14B from 563.8 s to 161.8 s (3.48×). Sol-Attn's own step on top
  of caching is 328.4 to 170.6 s (1.92×) and 217.6 to 161.8 s (1.34×).

## Where the hedges are

Per DP-010:

- **The routing rule is never tested on output quality.** Fig. 8 shows that
  thresholding gives tighter per-query densities than top-p, and Fig. 5b
  that it routes faster. No table runs Sol-Attn with top-k or top-p selection
  and reports VBench or PSNR. The paper also does not show that tight density
  per query is desirable. Prism LIT-tmpe78xc and SpargeAttention2 LIT-tmpbgw07
  both argue that the budget should vary with how concentrated a query's
  attention is, which is what top-p does.
- **The correction is ablated only on attention outputs.** Fig. 9 measures
  relative ℓ2 error and cosine similarity at one sequence length, with no
  numbers in the text. No generation is run with the correction switched
  off. The correction is also not new here. It is the zeroth-order case of
  the block-wise Taylor correction in PISA (Li et al., 2026), the first
  author's own earlier method and the strongest baseline in every table.
- **Against PISA, quality is level and the gain is speed.** On HunyuanVideo
  PISA leads on VBench (77.02 against 76.81), PSNR, SSIM and LPIPS. On Wan
  SVG2 has the higher PSNR (20.71 against 20.59). The paper's "overall
  outperforming" holds across tasks, not row by row. The speedups over PISA
  run from 1.06× (LTX) to 1.29× (SANA-WM).
- **"2.1×–3.0× end-to-end speedups across video tasks"** (§1). Table 1 gives
  2.02× on Wan and 1.9× on LTX 2.3, so the low end is 1.9×. The 3.0× is the
  three-step SANA-WM refiner, which runs sparse at every step with no dense
  warm-up.
- **"Matched sparsity" is approximate.** SVG2 runs at 83.66%, 83.15% and
  81.15% against Sol-Attn's 85–86%. β per model is not reported. For LTX
  2.3, where neither XAttn nor SVG2 has an official configuration, the
  authors adapted both.
- **No variance, prompt counts unstated.** VBench prompt counts and seeds are
  not given. Several Table 1 gaps between Sol-Attn, PISA and dense are
  under 0.3 VBench points.
- **The heavy cases share a group.** The SANA-WM refiner, where the
  speedup is largest, and Sol-Engine, which carries the 5×, are from
  overlapping NVIDIA authors.

## Which comparisons are like for like

- **Table 1 and Tables 2–3**: every method on the same model and the same
  warm-up (dense for the first 20% of steps and the first layer; LTX stage 2
  and SANA-WM sparse throughout), at approximately matched sparsity,
  measured end to end on H100 against FA3.
- **Fig. 10**: Sol-Attn against cuDNN BSA on identical block indices. This is
  the clean measure of what fusing routing and correction costs and saves.
- **Fig. 5b**: routing latency of threshold, top-k and top-p on the same
  proxy map, timed as kernels only.
- **Fig. 7** is cumulative and on B200. Each stage's gain depends on what
  came before.

## Standing in the anthology

It is a kernel paper. The video model, block layout and training are all
left alone. It extends FlashAttention (LIT-074) directly: it keeps the tiled
online-softmax loop and does two more things inside it. It decides block by
block which tiles to compute exactly, and it folds the skipped tiles in as
one pooled term each. Its blocks are FlashAttention's 64×64 tiles over the
sequence as given. The paper never says whether video tokens are reordered
into 3D tiles first.

Against Sparse VideoGen2 (LIT-tmpucn4v) the comparison is on accuracy and
cost. SVG2's k-means permutation needs about 8× the attention-processor
memory (Fig. 5c). At slightly lower sparsity it is slower than Sol-Attn on
every video task and lower on VBench in every row. Its PSNR against dense is
still slightly higher on Wan and HunyuanVideo (20.71 against 20.59, 25.64
against 25.21), while SSIM and LPIPS favour Sol-Attn (Table 1). The
evidence does not show fixed blocks plus correction matching semantic
grouping on fidelity. It shows them reaching about the same fidelity more
cheaply.

The dense backbones in Table 1 are Wan 2.1 (LIT-619) and HunyuanVideo
(LIT-620). Sol-Attn's Wan 2.1-14B output scores VBench 76.13 against the
dense model's 75.90, and its HunyuanVideo output 76.81 against 77.06, both
at about 85% sparsity. For practice in the record it is evidence on the
inference side only. SOTA-138 is about training sparse attention, and
Sol-Attn is forward-only (§6). Prism LIT-tmpe78xc applied it to a
full-attention model at 85% and labelled that budget a top-k budget, but
Sol-Attn has no top-k. Its budget comes from β.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and Appendices A–C. Figs. 3, 5, 6, 8, 9 and 10 are plots, and only
values printed on them or in the text are quoted. Figs. 1, 11 and 12 are
video stills and were not assessed.
