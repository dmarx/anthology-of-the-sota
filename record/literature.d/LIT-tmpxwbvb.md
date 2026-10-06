---
status: Active
title: 'SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference'
version: 1
tags:
- attention-techniques
- inference-optimization
- systems-optimization
- generative-modeling
date: '2026-10-06'
published: '2025-02-25'
arxiv: '2502.18137'
first_author: 'Zhang'
keywords:
- 'sparse-attention'
- 'training-free'
- 'selective-token-compression'
- 'block-self-similarity'
- 'top-cdf'
- 'sparse-online-softmax'
- 'hilbert-curve-permutation'
- 'quantized-attention'
implementations:
- 'SpargeAttn (thu-ml, github.com/thu-ml/SpargeAttn)'
# Table 1: dense CogVideoX (2B) is one of the full-attention reference models
# every sparse method is scored against.
compared_against:
- LIT-622
- LIT-tmp7p0tb
- LIT-tmpbgw07
- LIT-tmpk75wo
- LIT-tmpucn4v
summary: >-
  Zhang, Xiang, Huang et al., Tsinghua and UC Berkeley (2025), ICML 2025,
  [ARXIV-2502.18137](https://arxiv.org/abs/2502.18137). Training-free block-sparse attention for any model. Q and
  K blocks are mean-pooled into one token each, a block whose tokens are not
  similar enough (cosine below θ) is always computed, and among the rest each
  query block keeps the key blocks reaching τ cumulative mass on the pooled
  map (top-p). A second filter skips P·V in warps whose local row max trails
  the running max. Hyperparameters are grid-searched per layer to an L1
  error bound. At 31–54% sparsity it stays near dense on LLM, image and
  video metrics. The headline 1.83× on Mochi includes 8-bit SageAttention;
  sparsity alone gives 1.49×.
---

# LIT-tmpxwbvb: SpargeAttention: Accurate and Training-free Sparse Attention Accelerating Any Model Inference

Zhang, Xiang, Huang, Wei, Xi, Zhu and Chen, Tsinghua University and UC
Berkeley (2025), ICML 2025 — [ARXIV-2502.18137](https://arxiv.org/abs/2502.18137). Read at v8 (19 Nov 2025),
main text and Appendices A.1–A.4; v1 is 25 Feb 2025, and was checked
against v8 for Tables 1 and 4.

## Key takeaways

- **Stage one: predict the block mask from pooled blocks** (§3.2–3.3, Eqs.
  4–5, Alg. 1). Q is cut into blocks of 128 tokens and K, V into blocks of
  64, in sequence order. Each block is mean-pooled to one token, and its
  self-similarity is the mean cosine similarity among its tokens. Key blocks
  below a threshold θ are masked out of the pooled map. The softmax of the
  pooled scores gives a block attention map P̂. For each query block,
  TopCdf keeps the highest-scoring key blocks until their cumulative mass
  reaches τ. That is a top-p rule with no top-k floor. Any query or key
  block below θ ("fix block") is computed in full regardless, because a mean
  does not represent it.
- **Stage two: skip P·V inside the kernel** (§3.4). In FlashAttention's
  online softmax, if a block's local row max is far below the running max,
  exp(S − m) is near zero and P̃V adds almost nothing. Each warp checks
  max(m_local − m) < λ for its rows and skips its P̃V product. On Llama3.1 at
  128K, stage one alone gives 51.2% sparsity, stage two alone 27.7%, and
  both 54% (Table 6).
- **Per-layer calibration** (§3.6). τ, θ and λ are grid-searched for each
  layer on five inputs. τ and θ are chosen for maximum sparsity with
  relative L1 error below l1, then λ with error below l2. The bounds differ
  by model: (0.08, 0.09) for Llama3.1, (0.05, 0.06) for CogVideoX and Mochi,
  (0.07, 0.08) for Flux and SD3.5, (0.03, 0.035) for Open-Sora-Plan.
- **Hilbert-curve ordering for visual tokens** (§3.7, Table 4, App. A.1
  Table 9). Before attention, video tokens are reordered along a 3D Hilbert
  curve, so that consecutive runs of 128 or 64 tokens are compact regions of
  (T, H, W). Same hyperparameters, five prompts, sparsity / L1 on CogVideoX
  and Mochi:
  - Random: 0.027 / 0.0348 and 0.048 / 0.0414
  - Row-major: 0.242 / 0.0265 and 0.363 / 0.0307
  - Column-major: 0.198 / 0.0274 and 0.366 / 0.0342
  - Time-major: 0.238 / 0.0294 and 0.338 / 0.0342
  - Hilbert: 0.265 / 0.0323 and 0.392 / 0.0389

  Hilbert gives the highest block self-similarity and sparsity, and a
  higher L1 error than row-major.
- **End-to-end metrics** (Table 1). Llama3.1-8B at 128K, sparsity 0.54:
  WikiText perplexity 6.020 against 6.013 dense, LongBench 39.06 against
  38.68, NIAH 0.909 against 0.907. CogVideoX at 0.46: CLIPSIM 0.1798 against
  0.1819, VQA-a 78.28 against 80.38, FScore 5.03 against 5.34. Mochi at 0.47:
  VQA-a 54.18 against 56.47. Flux at 0.38: FID 163.98 against 166.10.
  SD3.5-large at 0.31: FID 166.19 against 166.10. Open-Sora-Plan at 0.34:
  VQA-a 77.59 against 81.40, VQA-t 76.91 against 80.60, at 393 s against
  629 s.
- **Speed** (Table 1, Table 2, Fig. 10). Attention speed, measured as dense
  operations over wall time with prediction included, is 708 against 157 on
  Llama3.1 at 128K, and 508 against 166 on CogVideoX. End to end, Mochi on an
  L40 takes 1,897 s dense, 1,544 s with SageAttention and 1,037 s with
  SpargeAttn. CogVideoX on an RTX 4090 takes 87, 68 and 53 s. Prediction
  costs 3.78% of dense attention time at 8K and 0.52% at 128K (Table 3).
- **The self-similarity judge** (Table 5, App. A.2 Table 10). Removing it on
  Mochi drops VQA-a from 54.18 to 34.66 and FScore from 1.81 to 1.14. Averaged
  over all attention calls it changes L1 and sparsity very little (0.0316
  against 0.0325, 0.199 against 0.203 on CogVideoX). On the 2% of calls
  where L1 differs by more than 0.05, L1 is 0.084 with the judge against
  0.214 without.
- **Sparsity varies by layer, head, step and length** (Table 7, App. A.4).
  On Llama3.1 at a fixed error bound, sparsity rises from 6.8% at 8K to 54%
  at 128K. On CogVideoX, layer means range from 0.09 to 0.60, around a
  global mean of 0.27, and sparsity rises over denoising steps.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **The speedups include 8-bit quantization.** Every SpargeAttn number runs
  on SageAttention's INT8 kernel (footnote 1). The dense baseline is
  FlashAttention in FP16. Table 2 separates the two. The 1.83× on Mochi is
  1.23× from SageAttention and 1.49× from sparsity. On CogVideoX the sparse
  part is 1.28×, and on Llama3.1 at 128K it is 1.40×. "2.5x to 5x faster
  than existing dense and sparse attention" (§1) is the kernel-speed column
  of Table 1, quantization included.
- **"No performance loss" is not true of every video row.** Open-Sora-Plan
  loses 3.8 VQA-a and 3.7 VQA-t points. Mochi loses 2.3 VQA-a, CogVideoX 2.1
  VQA-a and 0.31 FScore. The text says "almost no end-to-end metric loss"
  in §4.2 and "no performance loss" in Fig. 1 and the Open-Sora-Plan
  sentence.
- **"Enhances LLM performance" rests on small single-run gains** (§4.3).
  LongBench +0.38, InfiniteBench +0.004, NIAH +0.002. The offered reason,
  that sparsity helps the model focus, is not tested.
- **The error bounds were set per model.** Open-Sora-Plan got the tightest
  bound and the lowest sparsity (0.34). The paper does not say how the bounds
  were chosen, or whether looser ones were tried and failed.
- **Baseline settings are inconsistent.** The text says MInference ran at
  30% and 70%, but Table 1 labels it 0.5 and 0.3. Fig. 9's caption gives
  SpargeAttn 0.5 and FlexPrefill 0.54 on the Llama3.1 needle task, where
  Table 1 gives 0.54 and 0.5.
- **The baselines are language-model methods used out of domain.**
  MInference and FlexPrefill collapse on SD3.5 (FID 337–350 against 166) and
  FlexPrefill on every image and video model. Some of those failures are
  probably configuration, not method. MInference at 0.3 is close to dense on
  Flux (FID 170.22) but not on SD3.5 (337.53).
- **The Hilbert ablation is not at matched error.** Hyperparameters are held
  fixed, so sparsity and L1 move together. Hilbert raises sparsity over
  row-major by 0.023 on CogVideoX and 0.029 on Mochi while L1 rises by 0.0058
  and 0.0082. The paper calls the accuracy difference marginal.
- **No variance.** Every number is one run. The permutation and judge
  ablations use five prompts.
- **v8 against v1.** The v1 tables are the same numbers. v8 adds the
  Open-Sora-Plan row and Appendix A.4, and renames the speed column from
  "TOPS" to 1/t. Table 11 still uses TOPS, and its dense speed at 24K is the
  same 156.9 as Table 1's at 128K.

## Which comparisons are like for like

- **Table 2's three columns** run the same model and prompts with dense
  FlashAttention, SageAttention, and SpargeAttn on SageAttention. The middle
  column is what isolates sparsity.
- **Tables 4 and 9** hold model, prompts, hyperparameters and block sizes
  fixed and change only the token order. Sparsity and error are not held
  fixed.
- **Table 1's baselines** run at their own sparsities (0.3–0.6) against
  SpargeAttn's calibrated ones (0.31–0.54), so they are not at matched
  compute. Where sparsity is close, as with FlexPrefill at 0.45 against 0.46
  on CogVideoX, the gap in VQA-a is 7.7 against 78.3.
- No experiment trains the model with the mask, and no ablation compares
  top-p against top-k selection.

## Standing in the anthology

It is the record's earliest general training-free block-sparse attention
operator, and the base of the Tsinghua SpargeAttention line. Its predictor
is the one the later video papers argue over: mean-pooled Q and K blocks, a
softmax over block scores, and a cumulative-mass rule. It also already
names the weakness Sparse VideoGen2 ([LIT-tmpucn4v](LIT-tmpucn4v.md)) later builds on, that a
pooled representative fails when a block's tokens are dissimilar. Its fix
differs. It computes those blocks densely, gated by a cosine
self-similarity threshold, and it reorders video tokens along a Hilbert
curve so that runs of consecutive tokens are compact in (T, H, W).

On the questions this batch asks: it does not tile in 3D, but its Hilbert
ordering is a measured alternative to raster runs, worth 0.02–0.03 sparsity
at the same hyperparameters, at somewhat higher error. Block size is fixed
(128 and 64). What content decides is whether a block is pooled at all. The
selection rule is top-p alone, and no experiment compares it with top-k.
The paper is training-free only. SLA ran the trained-against-untrained
comparison later.

SpargeAttention2 ([LIT-tmpbgw07](LIT-tmpbgw07.md)), from the same group a year later, keeps
the mean-pooled block map and the cumulative-mass rule, adds a top-k floor,
and fine-tunes with a distillation loss. It runs this method as a baseline
on Wan2.1 at 89% sparsity (1.3B) and 86% (14B), far past the 31–54% this
paper calibrated to. There it scores Imaging Quality 35.28 against 63.67 for
full attention, VQA-a 3.26 against 81.28, and 38.46 against 68.01 at 14B.
That shows the method does not reach 90% sparsity untrained. It does not
show it fails at its own operating point. SpargeAttention2's own
training-free arm (same hybrid masker, no fine-tuning) is the cleaner
evidence that training matters at 95%. Its argument for a top-k floor, that
top-p alone fills its budget with attention-sink blocks, is an argument
against this paper's TopCdf rule.

SLA ([LIT-tmpk75wo](LIT-tmpk75wo.md)), the same group's step between this paper and
SpargeAttention2, runs it both ways on Wan2.1-1.3B at 480p. Untrained at
85% sparsity the videos collapse (VBench VA 0.002, Imaging Quality 26.0).
Fine-tuned on the same 20,000 clips at 84%, the same selection family
scores VA 73.83 and IQ 61.9, against 76.78 and 62.5 for full attention. That
is the record's closest controlled comparison of this method trained
against untrained, with the caveat that the trainable version is SLA's
authors' own implementation. On ImageNet LightningDiT it scores FID 46.05
trained and 206.11 untrained, against 31.87 dense.

PISA ([LIT-tmp7p0tb](LIT-tmp7p0tb.md)) is the one later paper that runs it at matched
sparsity, 87.5%, with the same dense warm-up on Wan2.1-1.3B, Wan2.1-14B and
HunyuanVideo. There SpargeAttn trails PISA on every column, PSNR 21.47
against 22.69 on Wan2.1-14B at 1.85× against 1.91×, and 9.48 against 12.04
without warm-up. Its kernel is slower than FlashAttention-3 at 4K tokens.
On FLUX.1-dev at 80% it scores FID 19.20 against 16.35 dense. Even 87.5%
is well past this paper's calibrated range.

Sparse VideoGen2 ([LIT-tmpucn4v](LIT-tmpucn4v.md)) runs it with its official configuration on
Wan 2.1 and HunyuanVideo at 39–43% density. It scores PSNR 21.18 on Wan I2V,
20.52 on Wan T2V and 27.89 on HunyuanVideo, against SVG2's 26.56, 25.81 and
30.45 at 25–31% density. The comparison is not at matched density, and
SpargeAttn ran at more density and lower fidelity.

Dense CogVideoX-2B ([LIT-622](LIT-622.md)) is one of the reference models in Table 1. At
0.46 sparsity SpargeAttn keeps it close on alignment (CLIPSIM 0.1798
against 0.1819) and loses 2.1 VQA-a and 0.31 FScore. FlexPrefill at 0.45
falls to VQA-a 7.7 and MInference at 0.5 to 70.5. The language model is Llama
3.1-8B ([LIT-179](LIT-179.md)). The kernel follows FlashAttention's tiling
and online softmax ([LIT-074](LIT-074.md)), and the sparse skip is defined inside that
loop. Sparse VideoGen ([LIT-tmpms9qj](LIT-tmpms9qj.md)), whose author list overlaps, cites this
paper but does not compare against it.

Filed without a NOTE: the takeaways come from one full reading of v8, main
text and Appendices A.1–A.4, with v1's tables compared. Figs. 1–2, 6–9 and
11–13 are images, and Figs. 10 and 14–17 are curves and bars. Only values
in the text, tables or bar labels are quoted.
