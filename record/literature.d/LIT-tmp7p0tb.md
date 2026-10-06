---
status: Active
title: 'PISA: Piecewise Sparse Attention Is Wiser for Efficient Diffusion Transformers'
version: 1
tags:
- attention-techniques
- inference-optimization
- generative-modeling
- systems-optimization
date: '2026-10-06'
published: '2026-02-01'
arxiv: '2602.01077'
first_author: 'Li'
keywords:
- 'piecewise-sparse-attention'
- 'training-free-sparse-attention'
- 'block-sparse-attention'
- 'block-wise-taylor-expansion'
- 'exact-or-approximate'
- 'covariance-aware-block-selection'
- 'diffusion-transformer'
implementations:
- 'PISA (HKUST-GZ)'
# The kernel is FlashAttention's tiled online softmax with an approximate
# phase over pooled keys and a global correction fused into the same pass
# (Alg. 1, Fig. 4).
extends:
- LIT-074
# Tables 1-3 and Fig. 5: SpargeAttn at matched sparsity on Wan2.1,
# HunyuanVideo, SD 3.5 and FLUX, and in kernel latency; Tables 1-2: Sparse
# VideoGen2 at its official configuration on the same three video models.
compared_against:
- LIT-tmpxwbvb
- LIT-tmpucn4v
- LIT-tmpx3dxt
summary: >-
  Li, Shao, Zhong et al., HKUST (Guangzhou) (2026), [ARXIV-2602.01077](https://arxiv.org/abs/2602.01077).
  Training-free block-sparse attention for DiTs that approximates the
  unselected key blocks instead of dropping them. Each one enters the softmax
  numerator and denominator through its mean key, plus one global first-order
  term. At 87.5% sparsity it runs 1.91× end to end on Wan2.1-14B and 2.57× on
  HunyuanVideo, ahead of SpargeAttn at the same sparsity on every VBench and
  similarity column. Sparse VideoGen2, at lower sparsity, is closer to dense
  output on most similarity columns. The first-order term buys about 1 dB
  PSNR on Wan2.1-14B. Every number is one run.
extended_by:
- LIT-tmpx3dxt
---

<!-- inactive-ok-file: SOTA-tmpaeox9 SOTA-tmpjldsh — Proposed practices on block geometry and block selection, named in the standing to say this paper does not bear on them -->

# LIT-tmp7p0tb: PISA: Piecewise Sparse Attention Is Wiser for Efficient Diffusion Transformers

Li, Shao, Zhong, Zhou, Bai, Xiong and Xie, The Hong Kong University of
Science and Technology (Guangzhou) (2026) — [ARXIV-2602.01077](https://arxiv.org/abs/2602.01077). Read at v2
(3 Feb 2026), main text and Appendices A–F; v1 is 1 Feb 2026.

## Key takeaways

- **The observation** (§3.1, Fig. 3). In Wan2.1-1.3B, pre-softmax scores of
  uncritical blocks cluster in a narrow bell at zero or negative values, where
  a first-order Taylor expansion of exp is accurate. Important blocks
  spread out. The figure is one visualization.
- **The formulation** (§3.2, Eqs. 3–6). Keys and values are cut into blocks
  of B = 64. For each query, the selected blocks are computed exactly. Each
  unselected block j is expanded around its mean key k̄_j. The zeroth-order
  term adds B·exp(q·k̄_j) to the denominator and exp(q·k̄_j)·ΣV_j to the
  numerator. The first-order term adds exp(q·k̄_j)·q·H_j to the numerator,
  where H_j = Σ(k − k̄_j)ᵀv is a d×d matrix per block. Its contribution to
  the denominator is zero.
- **The hybrid** (§3.3, Eqs. 7–10). Loading a d×d matrix per block is memory
  bound. So the first-order term uses one global matrix H̄, the mean of H_j
  over all blocks, computed once, scaled by Σ_j exp(q·k̄_j). Theorem 3.1
  bounds the error of that replacement by C_q·M·ρ/B, where ρ is the attention
  mass in unselected blocks and M = max‖H_j − H̄‖.
- **Selection** (§3.3 Eq. 11, App. D). Blocks are ranked by a pooled score
  softmax(q·k̄_j/√d + log(M_j + ε)), which also favours blocks whose H_j is
  far from H̄. Top-k is applied at a fixed density. The covariance term is
  used for images only. Video uses the plain pooled score.
- **Kernel** (§3.4, Alg. 1, Figs. 4–6, H800). Phase 1 runs exact attention
  over selected blocks, phase 2 scans the pooled keys in groups with selected
  columns masked, and phase 3 adds q·H̄ scaled by the tail mass. At 87.5%
  sparsity it is faster than FA3 and SpargeAttn from 4K to 32K tokens.
  SpargeAttn is slower than FA3 at 4K. PISA beats FA3 at densities below 50%
  above 8K tokens and below 70% at 4K (curves only).
- **Video** (Table 1, with dense warm-up). At 87.5% sparsity (VBench SC /
  IQ / AQ, PSNR, latency):
  - Wan2.1-1.3B 480p: dense 94.96 / 66.09 / 60.79, 98 s. PISA 94.58 / 65.94
    / 60.03, PSNR 22.62, 48 s (2.04×). SpargeAttn 93.76 / 64.89 / 58.66,
    20.75, 1.92×. SVG2 at 84.4%: 93.79 / 64.51 / 59.09, 22.85, 1.58×.
  - Wan2.1-14B 720p: dense 95.98 / 67.71 / 63.08, 1,564 s. PISA 95.80 /
    67.88 / 63.38, 22.69, 818 s (1.91×). SpargeAttn 21.47, 1.85×. SVG2 at
    80.6%: 22.92, 1.77×.
  - HunyuanVideo-13B 720p: dense 1,651 s. PISA IQ 68.16 against dense 67.65,
    PSNR 26.17, 641 s (2.57×). SpargeAttn 24.85, 2.51×. SVG2 at 81.4%: 26.40,
    2.54×.
- **Without warm-up** (Table 2), PISA stays ahead of both baselines on every
  column. On Wan2.1-14B it scores IQ 69.95 and PSNR 12.04 at 2.75×, against
  SpargeAttn's 60.03 and 9.48 and SVG2's 58.85 and 10.67.
- **Images** (Table 3, 1024²). On FLUX.1-dev, PISA at 85% scores FID 15.91
  and PSNR 17.07 at 6.87 s, against dense 16.35 at 8.32 s and SpargeAttn at
  80% 19.20 and 12.88 at 7.47 s. On SD 3.5-Medium, at 70% for both, PISA
  scores FID 14.78 against SpargeAttn's 19.52 and dense 15.48.
- **Ablation** (Table 4, Fig. 8). On Wan2.1-14B the zeroth-order term alone
  gives SSIM 0.772 / PSNR 21.68 / LPIPS 0.136 at 1.93×, and the hybrid
  0.787 / 22.69 / 0.124 at 1.91×. On FLUX.1-dev the exact block-wise first
  order reaches PSNR 17.04 but runs at 0.96×, slower than dense. The hybrid
  reaches 17.01 at 1.24×. Covariance-aware selection adds 0.005 SSIM.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The headline speedup has two values.** The abstract and Table 1 give
  1.91× on Wan2.1-14B, from 1,564 s to 818 s. Fig. 1 gives 2.14×, from
  1,468 s to 687 s, for the same model, and says "no appreciable quality
  loss". The figure's setting is not stated. Table 2's no-warm-up speedup is
  2.75×, so Fig. 1 matches neither table.
- **VBench cannot see how far the outputs drift.** Without warm-up, PISA's
  Wan2.1-14B IQ is 69.95, above dense 67.71, at a PSNR of 12.04 against the
  dense video. Those are different videos that score well. The same pattern
  holds with warm-up, where PISA "surpasses full attention" on IQ and AQ for
  Wan2.1-14B and IQ for HunyuanVideo by 0.2–0.5 points. Only three VBench
  dimensions are reported, with no prompt count or seeds.
- **Against SVG2 the quality claim splits by metric.** With warm-up, SVG2 is
  closer to the dense output on SSIM and PSNR for all three models (for
  example 22.92 against 22.69 PSNR on Wan2.1-14B) and on LPIPS for both Wan
  models. PISA wins VBench and speed. SVG2 runs at its official
  configuration, 80.6–84.4% sparsity, against PISA's 87.5%, so sparsity is
  not matched in either direction's favour.
- **"Strictly lower error bound than standard sparse attention"** (§2). No
  theorem in the paper compares PISA with block-sparse attention. Theorem 3.1
  bounds only the step from block-wise H_j to global H̄. The Taylor
  truncation error is dismissed in a remark (App. C, Remark 3) because the
  unselected blocks are "sparse and flat", with no bound. Fig. 8 shows lower
  output error than sparse attention at 32K tokens and 20% density, as
  curves.
- **"Full attention span with sub-quadratic complexity."** Phase 2 scores
  every query against every unselected block's mean key, which is L·(L/B)·d
  work. That is quadratic in sequence length divided by B = 64. Fig. 2
  counts it as 0.4% of dense FLOPs at 20% density on Wan2.1-1.3B.
- **The argument against SLA is not tested.** The paper says hybrid methods
  such as SLA sum branch outputs, break softmax normalization, and therefore
  need fine-tuning (§2, App. A). No experiment runs SLA, with or without
  fine-tuning.
- **Warm-up is part of every Table 1 number.** The first 15 steps (Wan2.1-
  1.3B) or 10 steps (the others) and the first layer stay dense (App. E,
  Table 5). The total step count is the models' default and is not stated.
- **Image baselines are not at matched sparsity.** PISA runs at 85% and
  SpargeAttn at 80% on three of four image models. The FID sample count and
  reference set are not stated.
- **Small inconsistencies.** The ablation text names "Wan2.1-13B", which
  does not exist. Table 4 gives the FLUX.1-dev hybrid 1.24×, while Table 3's
  latencies give 1.21×.

## Which comparisons are like for like

- **PISA against SpargeAttn on video** (Tables 1–2) is at the same 87.5%
  sparsity, same models, same warm-up, on H800. It is the cleanest
  comparison in the paper, and PISA leads on every column.
- **Table 4's PISA-0th against PISA-hyd** holds selection and sparsity fixed
  and changes only the approximation. On Wan2.1-14B it is the one measure of
  the first-order term on video, as similarity only.
- **SVG2** runs at its own configuration and sparsity. Its row is a
  comparison of methods at their recommended settings, not at matched cost.
- **Fig. 5** measures kernels at fixed density against FA2, FA3 and
  SpargeAttn on H800, and is curves only.

## Evidence on the batch's questions

- **3D tiles.** Blocks are 64×64 tiles over the sequence as given. The paper
  does not reorder video tokens into spatiotemporal cubes or discuss
  geometry.
- **Content-chosen block shape or size.** None. Selection is content-driven,
  with the covariance prior for images, but block size is fixed.
- **Selection rule.** Top-k at a fixed density. There is no top-p or hybrid
  arm. Covariance-aware against plain top-k is the only selection ablation,
  at matched sparsity, on FLUX.1-dev only, and it moves SSIM by 0.005.
- **Trainable against training-free.** PISA is training-free and runs no
  trained baseline.

## Standing in the anthology

Its baselines are both training-free. Against SpargeAttention
([LIT-tmpxwbvb](LIT-tmpxwbvb.md)), at the same 87.5% sparsity on Wan2.1-1.3B, Wan2.1-14B and
HunyuanVideo, PISA leads on every VBench and similarity column and runs
slightly faster. On Wan2.1-14B it scores PSNR 22.69 against 21.47 at 1.91×
against 1.85×. Without warm-up the gap widens to 12.04 against 9.48. In
kernel timing SpargeAttn falls behind FA3 at 4K tokens and PISA does not.
Against Sparse VideoGen2 ([LIT-tmpucn4v](LIT-tmpucn4v.md)), run at its official 80.6–84.4%
sparsity, PISA is faster on all three models and higher on VBench. SVG2's
outputs are still closer to dense on SSIM and PSNR in all three, so PISA's
advantage there is cost and perceptual score, not fidelity.

Its kernel extends FlashAttention ([LIT-074](LIT-074.md)). It keeps the tiled online
softmax and adds two phases to the same running max and normalizer. One
phase scans the unselected blocks' pooled keys in groups, and the other adds
the global first-order term once per query block. FlashAttention's tiling
is what lets the exact and approximate paths share one normalizer, which is
PISA's answer to the normalization problem it sees in SLA.

SLA ([LIT-tmpk75wo](LIT-tmpk75wo.md)) is the record's other attempt to keep the unselected
blocks. SLA routes them through a separate linear-attention output added
after a learned projection and fine-tunes the model to use it. PISA folds a
Taylor approximation into the softmax itself and does not train. The two
papers are not compared on a common model, and SLA's own paper says its
branch is a learned compensation, not an approximation. PISA's critique
targets something SLA did not claim to do.

Sol-Attn ([LIT-tmpx3dxt](LIT-tmpx3dxt.md)), with the same first author at NVIDIA six months
later, extends PISA and compares against it. It keeps PISA's zeroth-order
block term, exp(q·k̄_j) weighting ΣV_j and B·exp(q·k̄_j) in the denominator,
drops the global first-order term, and replaces top-k with a per-query
mean-plus-β-deviations threshold computed inside the kernel. At about 85%
sparsity Sol-Attn reruns PISA as its strongest baseline. On Wan2.1-14B PISA
scores VBench 76.03 at 1.86× against Sol-Attn's 76.13 at 2.02×. On
HunyuanVideo PISA leads on quality, 77.02 against 76.81, at 1.88× against
2.12×. So the later paper's gain over PISA is speed, from 1.06× to 1.29×,
with quality level.

On the record's practices: it is inference-only and training-free, so it
does not bear on [SOTA-138](../practices.d/SOTA-138.md). It uses raster tiles and top-k, so it is not
evidence for [SOTA-tmpaeox9](../practices.d/SOTA-tmpaeox9.md) or [SOTA-tmpjldsh](../practices.d/SOTA-tmpjldsh.md). It suggests that whatever
block layout and selection rule are used, approximating the remainder from
pooled keys recovers some of what dropping it loses. PISA reports that cost
only as a latency breakdown (Fig. 6). Sol-Attn's measurement of the
zeroth-order version, on identical block indices, is 1.6–9.4% of kernel
time.

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A–F. Figs. 1, 7, 9, 10 and 11 are images and were not
assessed. Figs. 2, 3, 5, 6 and 8 are plots, and only values printed on them
or stated in the text are quoted.
