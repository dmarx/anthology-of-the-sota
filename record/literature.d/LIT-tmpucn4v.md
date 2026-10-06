---
status: Active
title: 'Sparse VideoGen2: Accelerate Video Generation with Sparse Attention via Semantic-Aware Permutation'
version: 1
tags:
- attention-techniques
- inference-optimization
- systems-optimization
- generative-modeling
date: '2026-10-06'
published: '2025-05-24'
arxiv: '2505.18875'
first_author: 'Yang'
keywords:
- 'sparse-attention'
- 'semantic-aware-permutation'
- 'k-means-clustering'
- 'centroid-based-top-p-selection'
- 'dynamic-block-size-kernel'
- 'training-free'
- 'video-diffusion-transformer'
implementations:
- 'Sparse-VideoGen (svg-project)'
# Table 1 and Appendix Tables 2-4: dense Wan 2.1 (I2V and T2V, 14B) and dense
# HunyuanVideo-T2V-13B are the reference rows every sparse method is scored
# against, for PSNR/SSIM/LPIPS and VBench.
compared_against:
- LIT-619
- LIT-620
summary: >-
  Yang, Xi et al., UC Berkeley, MIT, NVIDIA and Stanford (2025), NeurIPS
  2025, ARXIV-2505.18875. Training-free sparse attention for video DiTs that
  replaces blocks of consecutive tokens with k-means clusters of queries and
  of keys, run separately per head and layer, permutes each cluster into a
  contiguous run, and keeps key clusters by top-p on centroid scores. At
  matched density it beats Sparse VideoGen on fidelity to the dense output
  (Wan 2.1 T2V PSNR 25.8 against 23.0 at about 30% density) at about the
  same speed. The abstract's 1.89× and "PSNR up to 26" on Wan come from two
  different rows. Every number is one run, and the p used is never stated.
---

# LIT-tmpucn4v: Sparse VideoGen2: Accelerate Video Generation with Sparse Attention via Semantic-Aware Permutation

Yang, Xi, Zhao, Li, Zhang, Cai, Lin, Li, Xu, Chen, Han, Keutzer and Stoica,
UC Berkeley, MIT, NVIDIA and Stanford University (2025), NeurIPS 2025 —
ARXIV-2505.18875. Read at v5 (6 May 2026), main text and Appendices A–E; v1
is 24 May 2025.

## Key takeaways

- **The diagnosis** (§3.1–3.2, Figs. 3–4). On Wan2.1-I2V-14B an oracle that
  keeps the highest-scoring tokens reaches 95% attention recall at 13%
  density. Block-wise methods fall well short of that curve at every density
  (Fig. 3, curves only). The paper gives two reasons. Blocks of consecutive
  tokens mix tokens with different activations, so a mean-pooled block
  representative scores the block badly. And the tokens that matter are
  scattered, so a tensor-core tile computes many tokens that do not. The 4×4
  example in Fig. 4 is a constructed illustration, not a measurement.
- **The mechanism** (§4.1–4.2). For each head and layer, k-means runs on the
  queries and, separately, on the keys: Cq = 100 query clusters and Ck = 500
  key clusters for 720p Wan 2.1 (21 latent frames × 3,600 tokens) and
  HunyuanVideo (33 × 3,600). Each cluster is permuted into a contiguous run,
  with V sharing the key permutation, so the output is exact after the
  inverse permutation. Cluster pairs are scored from centroid dot products
  weighted by key-cluster size (Eqs. 1–2), and key clusters are kept in
  descending order until their estimated mass reaches p. That is top-p, with
  no top-k component.
- **System pieces** (§4.3, §5.3, Fig. 7). Starting k-means from the previous
  denoising step's centroids makes clustering 76× faster at equal or lower
  density (Fig. 7a). Cluster sizes vary, so a fixed 128×128 block kernel
  pads them. The custom FA2/FA3 kernel takes variable block sizes, loads
  keys by per-token offsets, and reaches over 85% of the dense-FA3 time
  scaled by density. Against static-block FlashInfer at 90% recall it does
  1.48× less computation on average, and 1.88× less at (Cq, Ck) = (100, 500)
  (Fig. 7b).
- **Head to head at 30% dense warm-up** (Table 1; H100, 720p). Wan 2.1 I2V:
  SVG2 scores PSNR 26.56 at 31.28% density (1.58×), SVG 24.06 at 30.25%
  (1.56×), SpargeAttn 21.18 at 38.99% (1.47×). Wan 2.1 T2V: 25.81 at 29.51%
  (1.60×), against 22.99 at 30.25% (1.58×) and 20.52 at 42.03% (1.44×).
  HunyuanVideo T2V: 30.45 at 25.45% (2.30×), SVG 29.16 at 29.86% (1.91×),
  XAttention 28.89 at 39.32% (1.56×), SpargeAttn 27.89 at 42.62% (1.53×).
  VBench totals sit within 0.004 of dense in every SVG2 row (0.838 against
  0.841, 0.842 against 0.846, 0.852 against 0.850).
- **Turbo** (Table 1). A lower-budget setting reaches 12.87% density on Wan
  T2V at 1.89× with PSNR 23.68, still above SVG's 22.99 at 30.25%. On Wan
  I2V it reaches 14.13% at 1.84× with PSNR 24.51.
- **Without warm-up** (App. B, Table 2). With sparsity from the first step,
  PSNR falls to 18.28, 16.50 and 19.88, against SVG's 15.61, 13.29 and
  12.30, at 1.86–2.69× end to end.
- **What the permutation itself buys** (§5.5, Fig. 8). With mean pooling and
  the same cluster size, permuted clusters give higher attention recall than
  unpermuted blocks at every density. This is shown as a curve, and no values
  are given. On a fixed set of selected tokens, feeding the GPU the permuted
  contiguous layout instead of the scattered one cuts computation by 36% on
  average.
- **Queries and keys need their own clusters** (App. D.3, Table 6). At the
  same p, clustering Q and K independently gives PSNR 26.56 at 31.28%
  density. Using the query permutation for both gives 22.44 at 38.23%. Using
  the key permutation for both gives 22.18 at 38.58%. Clustering the
  pre-projection hidden states and sharing the result gives 26.50, but at
  87.27% density. The mean adjusted Rand index between Q and K clusterings is
  0.345.
- **How many clusters** (App. D.1–D.2, Table 5, Figs. 11–12). The kernel
  slows sharply once Cq passes 200 but is flat in Ck up to 4,000, because a
  64-row wgmma tile needs about 64 tokens per query cluster. Cq 50 gives PSNR
  22.56, Cq 100 gives 26.13 and Cq 400 gives 26.49, at 1.90×, 1.89× and
  1.25×. Ck 250, 500 and 1,000 give 25.50, 26.13 and 26.28.

## Where the hedges are

Per DP-010:

- **The abstract pairs a speed and a quality from different rows.** "Up to
  2.30× and 1.89× speedup while maintaining a PSNR of up to 30 and 26". On
  Wan 2.1, 1.89× is the Turbo row at PSNR 23.68 (Table 1). PSNR 25.81 is the
  standard row at 1.60×. The introduction gives the Wan figure as 1.84× on
  I2V instead. Against SVG at matched density the Wan speedups are 1.58×
  against 1.56× and 1.60× against 1.58×. On Wan the gain is fidelity, not
  speed. The speed gap opens only on HunyuanVideo, where SVG2 also runs at
  lower density.
- **The selection threshold is never reported.** No row in any table states
  its p, and Turbo is not defined beyond "lower density". Density is an
  outcome of p, so the matched-density comparisons were matched after the
  fact. The paper does not say how p was chosen per model.
- **Dense reference numbers move between tables.** Dense HunyuanVideo scores
  VBench 0.850 in Tables 1 and 4 but 0.820 in Tables 2 and 3. Dense Wan T2V
  scores 0.846 and 0.851. These are the same models, so prompts, seeds or
  settings differ between runs. No variance is reported anywhere, and the
  prompt count for the Penguin and VBench I2V sets is not given.
- **Table 5 does not reproduce Table 1.** The chosen (100, 500) setting gives
  PSNR 26.13 at 1.89× in Table 5. Table 1's Wan rows give 26.56 at 1.58× (I2V)
  and 25.81 at 1.60× (T2V). The model, task and warm-up behind Table 5 are not
  stated.
- **"Up to 80% of computation can be wasted"** (§1, pointing to §3.2). §3.2
  measures nothing, and §5.5 reports a 36% average reduction.
- **PSNR on Wan is near its own noise floor.** App. E reports that swapping
  dense-attention backends alone (FlexAttention, FlashAttention, SDPA) moves
  Wan 2.1 to PSNR 27–28 against itself, and HunyuanVideo to 33–34. SVG2's
  Wan PSNRs of 25.8–26.6 are 1–2 dB below that floor. The Wan
  ranking rests on fidelity differences of the same size as kernel
  nondeterminism.
- **Warm-up does most of the work.** At 30% dense warm-up SVG2's Wan T2V
  PSNR is 25.81, and with none it is 16.50 (Tables 1–2). The ranking
  survives without warm-up, but the method is not near-lossless there.
- **Baselines run at their own densities.** SpargeAttn and XAttention ran
  "official configurations" at 39–43% density, so their rows are not at
  matched compute. Only the SVG rows sit near SVG2's density. The Pareto
  curve (Fig. 2) is Wan I2V only.

## Which comparisons are like for like

- **Table 1, SVG2 against SVG**, at 25–31% density with the same 30% warm-up
  on the same model and prompts. This is the cleanest comparison. SpargeAttn
  and XAttention ran at higher density.
- **Fig. 8 and §5.5** hold everything but the permutation fixed: same cluster
  size and mean pooling for recall, and the same selected tokens for the 36%
  compute figure. These are the only measurements that isolate the layout.
- **Table 6** holds p fixed and changes only which permutation each side
  uses.
- **Fig. 7b** compares the custom kernel against FlashInfer on the same
  selected workloads, measured in FLOPs, not wall-clock.

## Standing in the anthology

It is the record's training-free, inference-only answer to the question the
2026 trainable sparse attention papers (Prism LIT-tmpe78xc, SpargeAttention2
LIT-tmpbgw07, VMoBA LIT-tmpmuiol, VSA LIT-tmp5vqlh) take up during training:
what should a block be. SVG2 drops spatial blocks altogether. A cluster is
whatever set of tokens k-means groups by Q or K activation, it has no shape
in the (T, H, W) grid, and its size varies. Prism LIT-tmpe78xc reuses SVG2's
diagnosis from a year earlier, that fixed blocks mix dissimilar tokens and
so give unreliable mean-pooled representatives. Prism keeps spatial 3D
blocks and varies their shape per zone. Prism cites SVG2 and runs it only as
a training-free baseline at inference on its full-attention model (71%
sparsity, below full attention on every metric).

Two of its measurements bear on Prism's design and are not tested there.
Table 6 finds that one grouping shared by queries and keys costs 4 dB PSNR
at matched p compared with separate groupings. Prism's query and key blocks
come from one partition. Prism also says most selection rules spend a fixed
budget per query. SVG2 already selected by top-p. Neither point shows Prism
wrong, since Prism trains and SVG2 does not, but both are prior art for
choices Prism presents as its own.

The dense models it accelerates are Wan 2.1 (LIT-619) and HunyuanVideo
(LIT-620). Table 1 measures SVG2's output against theirs, and the two
backbones respond differently: App. E shows HunyuanVideo tolerating kernel
numerics far better than Wan, which is why every method scores 4.6–7.4 dB
higher PSNR on it. The Sparse VideoGen predecessor it beats is not in the record.
Native Sparse Attention (LIT-143) also scores blocks through a pooled
representative, but over fixed contiguous blocks in a trained model, so it
is the language-model counterpart of the design SVG2 argues against.

Filed without a NOTE: the takeaways come from one full reading of v5, main
text and Appendices A–E. Figs. 2, 3, 7, 8, 11 and 12 are curves, and only
values stated in the text or tables are quoted. Figs. 9–10 are video stills
and were not assessed.
