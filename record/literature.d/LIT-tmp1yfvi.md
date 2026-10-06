---
status: Active
title: 'Fast Video Generation with Sliding Tile Attention'
version: 1
tags:
- attention-techniques
- inference-optimization
- systems-optimization
- generative-modeling
date: '2026-10-06'
published: '2025-02-06'
arxiv: '2502.04507'
first_author: 'Zhang'
keywords:
- 'sliding-tile-attention'
- 'sliding-window-attention'
- '3d-locality'
- 'head-specialization'
- 'block-sparse-attention'
- 'video-diffusion-transformer'
- 'mask-search'
- 'attention-distillation'
implementations:
- 'FastVideo (hao-ai-lab)'
# Tables 2, 4, 7: Swin's non-overlapping shifted windows, run on HunyuanVideo
# with and without fine-tuning; Table 4: the FA2 kernel as a latency baseline;
# Tables 3-4 and Fig. 7: HunyuanVideo with full attention as the quality
# reference.
compared_against:
- LIT-723
- LIT-106
- LIT-620
summary: >-
  Zhang, Chen, Su et al., UC San Diego, Michigan, Tsinghua, UC Berkeley and
  MBZUAI (2025), [ARXIV-2502.04507](https://arxiv.org/abs/2502.04507). 3D sliding-window attention for video DiTs
  that slides by tiles, not tokens. Each tile is one FlashAttention block, so
  every block is dense or skipped. At about 90% sparsity the kernel is 10.45×
  faster than FA3, where token-wise Tiled NATTEN is 1.27×. On HunyuanVideo at
  720p a per-head, profile-searched window gives 945 s → 501 s with no
  fine-tuning. At matched 58% sparsity token-wise NATTEN keeps slightly more
  VBench quality (82.69 against 82.46): the tile buys speed, not quality. The
  fine-tune is 1,600 steps on 2,000 self-generated clips, and every score is
  one run.
extended_by:
- LIT-tmp1ecle
- LIT-tmp5vqlh
---

# LIT-tmp1yfvi: Fast Video Generation with Sliding Tile Attention

Zhang, Chen, Su, Ding, Stoica, Liu and Zhang, UC San Diego, University of
Michigan, Tsinghua University, UC Berkeley and MBZUAI (2025), ICML 2025 —
[ARXIV-2502.04507](https://arxiv.org/abs/2502.04507). Read at v3 (4 Jun 2025), main text and Appendices A–G; v1
is 6 Feb 2025.

## Key takeaways

- **The observation** (§1, Figs. 2–3). In HunyuanVideo, trained with full 3D
  attention, a (12, 24, 24) local window holding 15.52% of the tokens
  receives 70% of the attention mass on average. How local a head is varies
  by head but barely by prompt: the standard deviation across 10 prompts is
  low. The authors call this head specialization.
- **Why token-wise 3D windows are slow** (§2.2, Table 1, Fig. 4). With a
  FlashAttention kernel, a sliding window over a flattened 3D grid produces
  "mixed" blocks. They must be fully computed and then masked, and the mask
  must be evaluated per position. For a (48,48,48) video with (4,4,4) tiles,
  Tiled NATTEN at window (11,11,11) has 0.06% dense and 7.17% mixed blocks.
  STA at (12,12,12) has 1.56% dense and none mixed (Theorems 3.1–3.2).
- **The mechanism** (§3.1, App. A, Fig. 8). Tokens are re-indexed so that
  each (T,T,T) tile is a run of consecutive positions, with T³ equal to the
  FlashAttention block. The window slides one tile at a time, and every query
  in a tile attends to the same key tiles, a (W/T)³ neighbourhood clamped
  inward at the video edges. The kernel, built on ThunderKittens and FA3,
  splits warpgroups: data warpgroups decide which key tiles to load, and
  compute warpgroups run dense attention without seeing any mask. For
  HunyuanVideo's (30, 48, 80) latent the windows (18,24,24) and (30,40,40)
  are written as (3,3,3) and (5,5,5) tiles, which implies a (6,8,8) tile of
  384 tokens. The paper does not state the tile size directly.
- **Kernel speed at about 90% sparsity** (Table 2; 115.2K tokens, 24 heads,
  head dimension 128, H100). STA in ThunderKittens reaches 58.79% MFU and
  10.45× FA3. In FlexAttention it reaches 41.03% MFU and 7.30×. Tiled NATTEN
  in FlexAttention gets 8.20% and 1.27×, and in CUDA 3.73% and 0.58×. CLEAR
  and plain NATTEN are slower than dense (0.86×, 0.85×). Swin's
  non-overlapping windows reach 43.55% and 5.54×. At about 56% sparsity
  STA-ThunderKittens is 2.37× and Swin 2.08× (Table 7).
- **Training-free** (§3.2, §4.3, Algorithm 1, Table 3). For each layer and
  head, the window is chosen from a candidate list to minimize the MSE
  against the dense head's output, averaged over 16 prompts. The first 12 of
  50 steps stay dense. At 50 steps STA takes 501 s (1.89×) and scores SSIM
  87.67, PSNR 28.76 and CD-FVD 66.12 against dense HunyuanVideo's own outputs.
  A reimplemented ∆-DiT at 1.36× scores 72.86, 18.09 and 122.74. On Wan 2.1
  the same search gives 1.60× at SSIM 85.81 and PSNR 24.42, with no
  comparison row (Table 5).
- **VBench against other windows** (Table 4, Tables 8–9). Dense HunyuanVideo
  scores 82.71 total (FA3, 945 s). Without training, at about 56–58%
  sparsity: Tiled NATTEN 82.69 at 1,858 s, STA (30,40,40) 82.46 at 527 s,
  CLEAR 82.37 at 2,567 s, and Swin (48,64,64) 79.00 at 762 s. At 91% sparsity
  STA (18,24,24) drops to 80.58 at 268 s. With fine-tuning STA (18,24,24)
  recovers to 82.62 at 268 s (3.53×), and STA (30,24,40) at 75% sparsity
  scores 83.00 at 388 s (2.44×). Fine-tuned Swin falls to 75.48.
- **Human evaluation** (§4.2, Fig. 7; 200 MovieGen prompts, pairwise).
  Training-free STA at 1.89× ties dense HunyuanVideo in 83.0% of pairs and
  loses 7.0 points more often than it wins. Fine-tuned STA at 2.43× beats
  ∆-DiT at 1.8× in 70.0% against 11.0% of pairs.
- **Fine-tuning recipe** (§3.2, App. B). The loss combines a flow-matching
  data loss with per-layer attention-output and final-output MSE against the
  dense teacher (α = 1, β = 0.5, γ = 0.5). It runs 1,600 steps at batch 2 and
  learning rate 2e−5 on 2,000 clips that HunyuanVideo itself generated from
  Mixkit prompts, at 1280×768×117 frames. Guidance scale alternates between
  1 and 6. It takes 8 hours on 8 H100s.
- **Images** (App. E, Table 6). In FLUX super-resolution, 2K→4K, STA at
  95.31% sparsity scores SSIM 0.9470 and PSNR 30.19 at 3.40×. CLEAR at r=32
  scores 0.9455 and 30.07 at 2.11×.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The tile buys speed, not quality.** The only quality comparison between
  tile-wise and token-wise sliding at matched sparsity is Table 4's
  training-free rows at about 58%. There Tiled NATTEN scores 82.69 and STA
  82.46, so the token-wise window is slightly ahead. At 90% sparsity, where
  the kernel speedups are quoted, NATTEN's quality is not measured. The paper
  shows that tiling makes a 3D window run at near-dense MFU. It does not show
  that tiling preserves quality better.
- **The kernel comparison mixes implementations.** The 10.45× headline is
  STA in custom ThunderKittens code against baselines in FlexAttention or
  NATTEN's CUDA. The like-for-like figure is STA in FlexAttention against
  Tiled NATTEN in FlexAttention: 41.03% against 8.20% MFU, 7.30× against
  1.27×. The abstract's "2.8–17× over FlashAttention-2" has no FA2 kernel row
  in any table. Table 4 gives FA2 only end to end, 1,496 s against FA3's
  945 s.
- **"Without quality degradation" holds for the 1.89× setting.** At the
  abstract's 0.09% drop the setting is fine-tuned, and the drop is in VBench
  percentage points (82.71 → 82.62). Untrained at the same 91% sparsity,
  VBench quality falls from 85.34 to 81.47. The total holds up better only
  because the semantic score rises, 72.17 to 77.03. App. F.2 attributes this
  to "the text embeddings' amplified role", which nothing tests.
- **The fine-tune is self-distillation on a tiny set.** The 2,000 training
  clips are HunyuanVideo's own outputs, at 1,600 steps and batch 2. VBench
  totals from one run of each model separate configurations by 0.3–0.5
  points, with no seeds.
- **Table 4 contradicts itself on Swin.** The same window, w=(30,40,40), is
  listed at 76.49% sparsity and 175.20 PFLOPS without training and at 55.81%
  and 283.08 PFLOPS with training, at the same 497 s. At most one of the two
  can be right, and the fine-tuned-Swin comparison depends on which.
- **The mask search is not ablated against a fixed window** under one metric.
  Table 3 reports the searched 1.89× configuration by similarity to dense
  outputs. Table 4 reports a fixed (30,40,40) window at 1.79× by VBench. Head
  specialization motivates the search, but the gain from searching is not
  isolated.
- **Similarity metrics reward staying close to the teacher.** SSIM, PSNR and
  CD-FVD in Table 3 are measured against dense HunyuanVideo's output for the
  same seed and prompt, and ∆-DiT is the authors' reimplementation, tuned by
  them for each speedup budget (App. C).
- **End-to-end times exclude the VAE and text encoder** (§4).

## Which comparisons are like for like

- **Table 1** is an analytic count of block types at matched video and tile
  size, with nearly matched windows (11 against 12).
- **Table 2 and Table 7, FlexAttention rows.** STA, Tiled NATTEN, NATTEN,
  CLEAR and Swin all in FlexAttention at about 90% (Table 2) and about 56%
  (Table 7) sparsity. This isolates the sparsity pattern from kernel
  engineering.
- **Table 4, training-free block.** Same model, prompts and step count, with
  each method at about 56–58% attention sparsity. STA at 91% is a different
  operating point.
- **Table 4, fine-tuned block.** Swin and STA fine-tuned by the same recipe,
  but at different sparsity (55.81% against 75% and 91%).

## Standing in the anthology

It is the record's source for **tile-granular 3D sliding-window attention**
in video DiTs, and for the observation that a dense-trained video DiT puts
most attention mass in a small 3D neighbourhood, with locality fixed per head
across prompts. It is a fixed-pattern, mostly training-free method. The
pattern is a window whose size is chosen per head offline. Nothing is
selected per input.

Swin ([LIT-723](LIT-723.md)) is the comparison that bears on locality. Its non-overlapping
shifted windows run about as fast as STA in FlexAttention (5.54× against
7.30× at about 90% sparsity, Table 2). Dropped into HunyuanVideo, they cost
VBench 3.7 points at about 56% sparsity, and fine-tuning with them lowers the
score further, to 75.48. The paper's reading is that a query near a window
edge loses neighbours it needs. Within one layer, Swin's partition breaks 3D
locality and STA's sliding window keeps it. Swin was designed to be trained
from scratch, so a retrofit into a dense-trained DiT is not a fair test of
Swin as an architecture. It is a test of whether a dense model tolerates
losing its cross-boundary neighbours.

FlashAttention-2 ([LIT-106](LIT-106.md)) appears only as the slow end-to-end baseline. With
FA2, HunyuanVideo takes 1,496 s for a 5 s 720p clip, against 945 s with FA3
and 501 s with training-free STA. The dense quality reference throughout is
HunyuanVideo ([LIT-620](LIT-620.md)). Every similarity metric in Table 3 is measured
against its outputs. Its VBench total of 82.71 is the bar in Table 4, and
human raters in Fig. 7 judge training-free STA at 1.89× a tie with it in 83%
of pairs.

The same group's VSA ([LIT-tmp5vqlh](LIT-tmp5vqlh.md)) extends it. VSA keeps STA's re-indexing
of a 3D cube into one GPU tile and replaces the fixed local window with a
learned top-K choice of cubes, trained from scratch or by an annealed retrofit.
VSA's own framing treats STA as the post-hoc baseline it improves on.
HunyuanVideo 1.5 ([LIT-tmp1ecle](LIT-tmp1ecle.md)) ships a "selective and sliding tile
attention" whose name and tile layout follow this paper. Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)) cites STA among "training-free"
video methods. That is true of STA's headline configuration but not of its
fine-tuned one, which is the faster of the two and is tuned with an
attention-distillation loss.

The paper is relevant to the question of grouping tokens into 3D blocks.
STA's grouping is a 3D cube by construction (§3.1, Fig. 8), and its measured
evidence for cubes is about hardware: tile-wise sliding removes mixed blocks
and recovers MFU. It never compares a 3D tile against a 1D run of
consecutive raster-order tokens at the same block size, on speed or on
quality.

Filed without a NOTE: the takeaways come from one full reading of v3, main
text and Appendices A–G. Figs. 1, 3, 7 and 10–11 are charts or video frames,
and only values given in the text and tables are quoted. No practice or
theory is drawn from it.
