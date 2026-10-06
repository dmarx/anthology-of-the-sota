---
status: Active
title: 'SLA: Beyond Sparsity in Diffusion Transformers via Fine-Tunable Sparse-Linear Attention'
version: 1
tags:
- attention-techniques
- inference-optimization
- generative-modeling
- adaptation-and-tuning
date: '2026-10-06'
published: '2025-09-28'
arxiv: '2509.24006'
first_author: 'Zhang'
keywords:
- 'sparse-linear-attention'
- 'block-sparse-attention'
- 'linear-attention'
- 'trainable-sparse-attention'
- 'low-rank-attention-weights'
- 'diffusion-transformer'
- 'video-generation'
implementations:
- 'SLA (thu-ml)'
# The linear branch is this paper's kernelized attention: phi(Q)(phi(K)^T V)
# normalized by phi(Q) rowsum(phi(K)^T) (§2.2, Eq. 5).
extends:
- LIT-428
# Table 1 fine-tunes VSA, VMoBA and a trainable SpargeAttn on the same Wan2.1
# data and runs training-free SpargeAttn; Table 3 repeats VSA, VMoBA and
# SpargeAttn on LightningDiT.
compared_against:
- LIT-tmp5vqlh
- LIT-tmpmuiol
- LIT-tmpxwbvb
- LIT-tmpbgw07
summary: >-
  Zhang, Wang, Jiang et al., Tsinghua and UC Berkeley (2025), [ARXIV-2509.24006](https://arxiv.org/abs/2509.24006).
  Block-sparse attention for video DiTs that keeps the top 5% of key blocks
  per query block exact, skips the bottom 10%, and sends the other 85% through
  one linear-attention term with a learned output projection. After 2,000
  fine-tuning steps on Wan2.1-1.3B it scores level with fine-tuned full
  attention on VBench at 95% sparsity, with attention FLOPs 2.74T against
  52.75T and 2.2× end to end on an RTX 5090. The paper says the linear
  branch is a learned compensation, not an approximation of the dropped
  weights, so it does not test its own low-rank story. Every number is one run.
---

<!-- inactive-ok-file: SOTA-tmpaeox9 SOTA-tmpjldsh — Proposed practices on block geometry and block selection, named in the standing to say this paper does not bear on them -->

# LIT-tmpk75wo: SLA: Beyond Sparsity in Diffusion Transformers via Fine-Tunable Sparse-Linear Attention

Zhang, Wang, Jiang, Yang, Zheng, Xi, Wang, Zhu, Zhao, Stoica, Gonzalez, Zhu
and Chen, Tsinghua University and UC Berkeley (2025) — [ARXIV-2509.24006](https://arxiv.org/abs/2509.24006).
Read at v2 (19 Nov 2025), main text and Appendices A.1–A.3; v1 is 28 Sep
2025.

## Key takeaways

- **The observation** (§3.1–3.2, Figs. 1 and 3). In one sampled Wan2.1
  attention map, 8.1% of weights exceed the mean 1/N and about 45% fall below
  1/(100N). Dropping the smallest 45% gives under 3% relative L1 error in
  the output. Keeping only the top 8.1% (92% sparsity) gives about 33%. The
  stable rank of the full map is 6,226, of the top 8% alone 6,230, and of
  the bottom 92% alone 9. The paper's reading is that attention is "sparse
  few, low-rank many".
- **The method** (§4, Alg. 1). Q and K are mean-pooled over blocks of 64
  tokens and a pooled map P_c = softmax(pool(Q)pool(K)ᵀ/√d) is computed. In
  each row, the top k_h% of key blocks are critical and run through sparse
  FlashAttention. The bottom k_l% are skipped. The rest are marginal, and
  their φ(K_j)ᵀV_j sums enter one linear-attention output per query block.
  The output is O = O_s + Proj(O_l), where Proj is a learned d×d map. The
  defaults are k_h = 5%, k_l = 10%, φ = softmax, and b_q = b_kv = 64.
  Forward and backward passes are one fused kernel (Algs. 1–2). App. A.3
  adds a lookup table for very sparse masks, pre-aggregation of the linear
  sums, and the Method of Four Russians for masks near 50% marginal.
- **The linear branch is not an approximation** (§4.2, "Insight"). The
  authors say the linear term "does not approximate the output corresponding
  to marginal attention weights, but serves as a learnable compensation".
  That is why the model must be fine-tuned.
- **Main result** (Table 1, Wan2.1-1.3B, 480p). Every row is fine-tuned on
  the same 20,000 private 5-second clips, 2,000 steps at batch 64, except
  the training-free Sparge-F. Selected columns (VA / VT / IQ / AQ / VR /
  attention FLOPs / sparsity):
  - Full attention: 76.78 / 82.88 / 62.5 / 56.1 / 0.059 / 52.75T / 0%
  - SLA: 76.96 / 83.92 / 62.2 / 55.9 / 0.048 / 2.74T / 95%
  - Sparge-T (trainable SpargeAttn, authors' implementation): 73.83 / 77.87
    / 61.9 / 55.4 / 0.014 / 7.38T / 84%
  - VSA: 55.37 / 64.61 / 60.6 / 51.9 / −0.069 / 5.92T / 89%
  - VMoBA: 32.33 / 35.79 / 58.0 / 46.2 / −0.175 / 7.91T / 85%
  - Sparge-F (training-free SpargeAttn): 0.002 / 0.026 / 26.0 / 35.7 /
    −0.216 / 7.91T / 85%
- **Ablations** (Table 2). Linear attention alone collapses (VA 0.042, IQ
  39.5). The sparse branch alone at 85% scores VA 64.00 and IQ 57.2. Summing
  separately computed linear and sparse outputs (L+S, 90%) scores VA 29.65,
  worse than sparse alone. φ = softmax beats elu+1 and hedgehog by 1.5–2.4
  VA. Raising k_h from 5% to 10% and 20% leaves VA within 1.7 points and
  moves VR from 0.048 to 0.057 and 0.059, at 2× and 4× the FLOPs.
- **Speed** (§6.3, Fig. 6, RTX 5090). The forward kernel is 13.7× faster
  than FlashAttention2 and the backward 6.8×. At 95% sparsity it is 1.93×
  faster than VSA and 3.36× faster than VMoBA. End to end, attention goes
  from 97 s to 11 s while the other 62 s stay fixed, 159 s to 73 s (2.2×).
- **Images** (App. A.2, Table 3). LightningDiT-1p0B/1 is trained from scratch
  on ImageNet 512×512 for 100,000 steps at batch 128. FID is 31.49 for SLA
  at 87.5% sparsity and 31.87 for full attention. VSA (2D) scores 35.75 and
  VMoBA (2D) 39.45, both at 75%. SpargeAttn scores 46.05 trained and 206.11
  training-free.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The low-rank decomposition motivates the method and is not what the
  method does.** The rank evidence is one sampled attention map (Fig. 3),
  with no statistics over layers, heads or timesteps. The paper then says
  its linear branch does not approximate the marginal weights (§4.2). Two
  results agree with that. Linear attention alone fails, and adding a
  separately computed linear output to sparse attention (L+S) makes it worse.
  What the tables support is that a learned O(Nd²) side branch, fed only
  marginal blocks and fine-tuned, recovers quality. Whether it does so by
  capturing the low-rank tail is not tested.
- **"Without loss of generation quality."** SLA is level with full attention
  on VA, VT, OC and SC and slightly below on IQ (62.2 against 62.5), AQ
  (55.9 against 56.1) and VR (0.048 against 0.059). VR reaches the full
  value only at k_h = 20%, 80% sparsity (Table 2). No row reports seeds or a
  prompt count, so none of these gaps can be called real or noise.
- **Sparsity counts the linear blocks as sparse.** 95% means 5% of blocks
  run exactly. The other 85% still cost a linear pass. The FLOPs column is
  consistent with this (5% of 52.75T plus 0.10T for the linear branch gives
  2.74T), so the 19.3× figure is honest about FLOPs. "Sparsity" against
  other methods' sparsity is not the same quantity.
- **Baselines are not at matched sparsity.** VSA runs at 89%, VMoBA and
  Sparge-F at 85%, and Sparge-T at 84%, against SLA at 95%. The paper argues
  that they are already worse at lower sparsity, so a 95% comparison would
  not be quality-matched (§6.3). True, but no baseline is shown at 95%, and
  SLA at 85% sparse-only (64.00 VA) is not SLA's design point either. The
  kernel comparison at 95% (1.93× over VSA, 3.36× over VMoBA) is then a
  speed comparison at a sparsity where those baselines' quality is not
  reported.
- **Baselines are run on the authors' data and recipe.** VSA and VMoBA use
  official code, Sparge-T is the authors' own implementation. The paper does
  not say whether every baseline got the same 2,000 steps or loss. VSA's own
  paper puts its Wan2.1-1.3B retrofit 0.86 VBench points below a same-data
  dense fine-tune. Its VA of 55.37 here should be read as VSA under SLA's
  data and fine-tuning budget.
- **The L+S ablation is not the sum of the two other rows.** It is described
  as the sum of Linear Only and Sparse Only, but it runs at 90% sparsity
  (5.37T), while Sparse Only runs at 85% (7.91T). Its sparse part is
  therefore not the Sparse Only arm.
- **The kernel baseline is FlashAttention2 on a consumer GPU.** The paper
  says FA2 is the fastest available version on an RTX 5090. No H100 or FA3
  number is given, so the 13.7× is against the slower kernel.
- **The image result is a short pretraining run.** Full attention's FID of
  31.87 after 100K steps is far from a converged LightningDiT. That SLA
  matches it (31.49) shows SLA can be trained from scratch at this budget.
  It does not show parity at convergence. k_h for images and the FID sample
  count are not stated.

## Which comparisons are like for like

- **Sparge-F against Sparge-T** (Table 1) is the closest thing here to a
  controlled training-free against trainable comparison. Same selection
  family, 85% against 84% sparsity, same model and data. Untrained, the
  videos collapse (VA 0.002, IQ 26.0). Trained, they are near full attention
  (VA 73.83, IQ 61.9). The trainable version is the authors' own
  implementation.
- **Table 2's SLA rows** share data, steps and model and differ only in φ or
  k_h. The k_h sweep varies sparsity on purpose, so it is a quality-against-
  cost curve, not a matched comparison.
- **Sparse Only against SLA** is not matched: 85% against 95%. No row shows
  SLA's sparse branch alone at 95%, which is the arm that would isolate the
  linear branch's contribution.
- **Full attention** is fine-tuned on the same data for the same steps, so
  the comparison with it is fair on training. Fig. 6's latency column is
  inference with the same 62 s of non-attention work in every row.

## Evidence on the batch's questions

- **3D tiles.** Blocks are 64 consecutive tokens of the flattened sequence.
  The paper does not reorder tokens into spatiotemporal cubes and does not
  discuss block geometry. It runs VSA and VMoBA, which do, as baselines
  under its own recipe.
- **Content-chosen block shape or size.** None. Block size is fixed at 64.
- **Selection rule.** Per-row top-k on the pooled map for the critical set,
  bottom-k for the skipped set, with the middle sent to the linear branch.
  The only ablation is k_h ∈ {5, 10, 20}%, which changes sparsity with it.
  There is no top-p arm and k_l is not ablated.

## Standing in the anthology

It is the Tsinghua group's step between training-free SpargeAttention and
SpargeAttention2. Against SpargeAttention ([LIT-tmpxwbvb](LIT-tmpxwbvb.md)), its own Table 1
shows the training-free method failing at 85% on Wan2.1-1.3B (VA 0.002)
and a fine-tuned version of it working (73.83). That gap is what SLA's
fine-tuning premise rests on. SLA also outscores both versions of it, at
95% sparsity. Against VSA ([LIT-tmp5vqlh](LIT-tmp5vqlh.md)) and VMoBA ([LIT-tmpmuiol](LIT-tmpmuiol.md)), both
fine-tuned on the same 20,000 clips, SLA at 95% scores higher on every
quality column than VSA at 89% (VA 76.96 against 55.37) and VMoBA at 85%
(32.33). Its kernel at 95% runs 1.93× and 3.36× faster than theirs. On
LightningDiT the gaps are smaller: FID 31.49 against 35.75 for VSA and 39.45
for VMoBA, at 87.5% against 75% sparsity.

Its linear branch extends the kernelized attention of Katharopoulos et al.
([LIT-428](LIT-428.md)). SLA uses that paper's reordering, φ(Q)(Σφ(K)ᵀV) over
φ(Q)Σφ(K)ᵀ, but sums only over the marginal blocks of each query block, and
it passes the result through a learned projection before adding it to the
sparse output. Its ablation (Table 2) shows that construction failing on its own in a
video DiT: linear attention alone, fine-tuned on Wan2.1, collapses (IQ 39.5
against 62.5). It earns its place only as a side branch
next to exact attention on the top 5% of blocks. The softmax feature map
beat elu+1, the map used by Katharopoulos et al., by 1.5 VA.

The two later papers that build on it take it in opposite directions.
SpargeAttention2 ([LIT-tmpbgw07](LIT-tmpbgw07.md)), from the same group five months later, runs SLA
as a trained baseline at 95% sparsity on Wan2.1-1.3B. There SLA scores IQ
63.14 and VQA-a 72.66 with 11 s of attention, below full attention (63.67,
81.28) and below SpargeAttention2 (67.68, 83.86, 6 s). SpargeAttention2
drops the linear branch and gets its quality from a top-k ∪ top-p mask and
distillation from the dense model instead. PISA ([LIT-tmp7p0tb](LIT-tmp7p0tb.md)) keeps the idea
of approximating the unselected blocks rather than dropping them. It argues
that SLA's additive O_s + Proj(O_l) breaks softmax normalization and so
needs fine-tuning, and it folds the approximation into the softmax numerator
and denominator instead. PISA never runs SLA, so that argument is untested
there.

Combining sparse exact attention with a low-rank remainder is older than this
paper. Scatterbrain (Chen, Dao et al., 2021, arXiv 2110.15343), not in the
record, approximated attention as a sparse plus a low-rank term without
training. SLA does not cite it. What is new here is the block-level split by
pooled score, the learned projection, and fine-tuning the model around the
branch.

On the record's practices: it is evidence for the trained half of
[SOTA-138](../practices.d/SOTA-138.md), from a different modality. Its Sparge-F against Sparge-T rows
show that fine-tuning under the mask matters at 85% sparsity. Its selector
is pooled dot products with no learned indexer, as in the other video
papers. It uses raster blocks, so it bears on [SOTA-tmpaeox9](../practices.d/SOTA-tmpaeox9.md) only as one more
method that did not use 3D cubes. It uses top-k alone, so it does not bear
on [SOTA-tmpjldsh](../practices.d/SOTA-tmpjldsh.md).

Filed without a NOTE: the takeaways come from one full reading of v2, main
text and Appendices A.1–A.3. Figs. 2, 5 and 7 are video stills and were not
assessed. Fig. 6 is read for the values printed on it.
