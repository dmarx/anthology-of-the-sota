---
status: Active
title: 'MoBA: Mixture of Block Attention for Long-Context LLMs'
version: 1
tags:
- attention-techniques
- model-architecture
- training-optimization
- inference-optimization
date: '2026-10-06'
published: '2025-02-18'
arxiv: '2502.13189'
first_author: 'Lu'
keywords:
- 'mixture-of-block-attention'
- 'block-sparse-attention'
- 'top-k-gating'
- 'mean-pooled-key-blocks'
- 'long-context'
- 'trainable-sparse-attention'
- 'hybrid-full-sparse-attention'
- 'fine-grained-block-segmentation'
implementations:
- 'MoBA (MoonshotAI, github.com/MoonshotAI/MoBA)'
- 'Kimi long-context serving (stated in the abstract)'
summary: >-
  Lu, Jiang, Liu et al., Moonshot AI, Tsinghua and Zhejiang (2025),
  ARXIV-2502.13189. Block-sparse attention with no new parameters: keys are
  cut into fixed 1D blocks, each block is scored by the query's dot product
  with its mean-pooled key, and each query attends causally to its own
  block plus the top-k others. Trained from scratch at 8K it tracks full
  attention's loss within 1e-3 over five sizes. At 32K its trailing-token
  loss is higher at every size, and the gap closes only in a fitted
  extrapolation. Most of Table 2's parity with full attention is measured
  on inputs short enough that top-12 of 4,096-token blocks is full
  attention, and decoding is dense. One run per arm.
---

# LIT-tmpvcvo8: MoBA: Mixture of Block Attention for Long-Context LLMs

Lu, Jiang, Liu, Du, Jiang, Hong, Liu, He, Yuan, Wang, Huang, Yuan, Xu, Xu,
Lai, Chen, Zheng, Yan, Su, Wu, Zhang, Yang, Zhou, Zhang and Qiu, Moonshot
AI, Tsinghua University and Zhejiang Lab / Zhejiang University (2025) —
ARXIV-2502.13189. Read at v1 (18 Feb 2025), the only version, main text and
Appendix A.

## Key takeaways

- **The mechanism** (§2.2, Eqs. 2–6, Alg. 1). The context of length N is
  cut into n contiguous 1D blocks of B = N/n tokens. A query's affinity to
  block i is its inner product with the mean of that block's keys. A
  parameter-free top-k over those scores picks the blocks the query attends
  to. Future blocks get score −∞. The query's own block is always selected
  and attended with a causal mask, which the paper compares to a shared
  expert in an MoE. With top-k = 3, each query sees its own block and at
  most two past blocks (footnote 3). Selection is top-k only. There is no
  threshold or cumulative-mass rule.
- **Implementation** (§2.3, Alg. 1). Queries are gathered by the block they
  were routed to, each block's attention runs as variable-length
  FlashAttention, the own-block part runs separately with causal masking,
  and the two are merged by online softmax.
- **Loss scaling at 8K matches full attention** (§3.1, Table 1, Fig. 3a).
  Five models from 568M to 2.1B parameters, Chinchilla-sized token budgets
  (10.8B to 36.9B), block 512, top-3. Fitted laws: 2.625 × C^−0.063 for
  MoBA against 2.622 × C^−0.063 for full attention. The text puts the gap
  within 1e-3.
- **Trailing-token loss at 32K does not** (§3.1, Fig. 3b, App. A.1,
  Table 3). Loss on the last 2K tokens of 32K sequences, at sparsity up to
  95.31%. MoBA is higher at all five sizes. The fits are 1.546 × C^−0.108
  against 1.464 × C^−0.097. Per position (Table 3), the coefficients are
  close up to 8K (1.899 against 1.894 at 6–8K) and separate past it (1.546
  against 1.464 at 30–32K). The steeper MoBA exponent is the paper's
  evidence that the gap is "progressively narrowing".
- **Finer blocks are better at matched sparsity** (§3.1, Fig. 4). A 1.5B
  model at 32K with 8, 16, 32, 64 and 128 blocks and top 2, 4, 8, 16 and 32,
  all at 75% sparsity. The coarsest setting (2 of 8) is about 1e-2 worse in
  validation loss than the finer ones. This is the paper's one ablation of
  block size, and it varies size and k together to hold sparsity fixed.
- **Sparse-then-dense training recovers full attention's position-wise
  loss** (§3.2, Fig. 5a). Three 1.5B models, 30B tokens at 32K, block 2,048,
  top-3. MoBA for 90% of tokens and full attention for the last 10% reaches
  a position-wise loss "nearly identical" to full attention throughout. MoBA
  alone is higher on trailing positions. No loss spike at the switch.
- **SFT needs some dense layers** (§3.2, Fig. 5b–c). MoBA sometimes gives a
  worse SFT loss. The authors guess this comes from prompt-token loss
  masking, which leaves sparse gradients. Switching the last 1, 3, 5 or 10
  layers to full attention lowers SFT loss and trailing loss.
- **Continued pre-training of Llama 3.1 8B to 1M** (§3.3, Fig. 6, Table 2,
  Fig. 7). Context is extended from 128K to 1M with position interpolation.
  MoBA is then switched on for 100B tokens with block 4,096 and top-12. The
  last 3 of 32 layers stay dense, and SFT runs from 32K to 1M. The full
  attention baseline follows the same recipe. Across 16 benchmarks the two
  are close: LongBench@32K 0.4828 against 0.4821, RULER@128K 0.7818 against
  0.7849, Loogle 0.4209 against 0.4016, MBPP Sanitized 0.6926 against
  0.6615. The Needle-in-a-Haystack sweep to 1M is shown as a heat map only.
- **Speed** (§3.4, Fig. 2). Attention-layer forward time only. On the 1M
  model, MoBA is up to 6.5× faster than FlashAttention when prefilling 1M
  tokens. With 64 blocks, top-3 and block size growing with length (95.31%
  sparsity), it is 16× faster at 10M tokens. The inset shows the two about
  level from 32K to 512K.

## Where the hedges are

Per DP-010:

- **Table 2's parity is mostly not a test of sparsity.** With block 4,096
  and top-12, a query attends to everything when the sequence is under
  12 × 4,096 = 49,152 tokens. So on any input below that length,
  Llama-8B-1M-MoBA computes full attention. This covers LongBench@32K and
  every short-context row (AGIEval, GSM8K, MMLU, HumanEval and the rest),
  and the paper does not say so. Those rows compare two models trained
  differently, both running dense attention. The text gives a sparsity for
  one benchmark only, RULER@128K: "up to 62.5%", and there MoBA is 0.0031
  behind. MoBA is also used "for prefill only" and decoding switches to
  full attention (§3.3). The three dense top layers stay dense throughout.
- **"Sparsity up to" is quoted at the last position, against
  non-causal attention.** The 8K scaling runs are described as
  "sparsity up to 81.25%" in one sentence and "up to 75%" two sentences
  later (§3.1). The baseline computes causal attention. By this note's own
  arithmetic, at 8K with 16 blocks of 512 and top-3, MoBA attends to 45
  block-rows where causal full attention attends to 136, a saving of about
  two thirds.
- **"The loss gap is progressively narrowing" is a property of a fit.**
  MoBA's trailing loss is above full attention's at every one of the five
  sizes (Fig. 3b). The narrowing comes from two power laws with exponents
  −0.108 and −0.097. On this note's arithmetic, the two fits cross near 140
  PFLOP/s-days, about an order of magnitude past the largest model on the
  plot. Fig. 3's caption says "last 1K tokens" and its axis label and the
  table say last 2K.
- **The training-efficiency claim has no training measurement.** The
  abstract and conclusion stress faster training. Every timing in the paper
  is the forward pass of the attention layer (Fig. 2). There is no
  backward-pass time, end-to-end step time or throughput, and none for the
  sparse-then-dense recipe that §3.2 offers as "efficient long-context
  pre-training".
- **The hybrid results are curves only.** Fig. 5's position-wise and SFT
  losses, and Fig. 4's granularity ablation, have no table. The SFT problem
  that motivates the layer-wise hybrid is put down to loss masking in a
  sentence that begins "We speculate". No experiment tests it.
- **No variance anywhere.** Every arm is one run. Table 2's margins in
  either direction are mostly in the third decimal place.
- **Deployment in Kimi is adoption, not evidence** (abstract). No
  serving-side measurement is reported.

## Which comparisons are like for like

- **Fig. 3 and Table 1** change only the attention module. Parameters,
  learning rate, batch size and data are the same for MoBA and full
  attention at each of the five sizes.
- **Fig. 4** holds model, length and sparsity and varies block count and k
  together. It does not separate "smaller blocks" from "more blocks
  selected".
- **Fig. 5a** trains three 1.5B models on the same 30B tokens. Only the
  attention schedule differs.
- **Table 2** compares two continued pre-training and SFT runs from the same
  Llama 3.1 8B base (LIT-179) with "the only difference" being attention.
  But at the lengths of most rows the MoBA model runs dense attention (see
  above). So the comparison is of training histories more than of attention
  at inference.
- **No comparison against another sparse method.** Quest, LongHeads,
  sliding-window attention and attention sinks are related in prose only.
  The paper argues, without an experiment, that sliding-window attention and
  attention sinks (LIT-191) are special cases of MoBA's gate.

## Standing in the anthology

It is a second laboratory's evidence for SOTA-138's claim that sparse
attention can be trained natively, published two days after Native Sparse
Attention (LIT-143). Neither paper compares against the other. The
designs differ where SOTA-138 is specific. MoBA has no learned indexer: it
scores blocks with mean-pooled keys and no new parameters. It has no
compression branch and no sliding window. Its schedule is the opposite of
SOTA-138's warm-up: train sparse first, then switch to dense for the last
10% of tokens (Fig. 5a), and keep the top layers dense for SFT. It
matches full attention's loss at 8K and stays behind on trailing tokens
at 32K. SOTA-138's conditions put the payoff at 64K–1M, and MoBA's only
sparse evaluations at those lengths are RULER at 128K and the needle
heat map. It adds no test of the warm-up.

Its parameter-free gate (mean-pooled key blocks, top-k, own block forced)
is the selector that VMoBA and VSA start from. VMoBA (LIT-tmpmuiol) is built on it and could not stand
without it. It keeps the mean-pooled block score and the mixture-of-block
framing, and replaces MoBA's 1D partition and per-query top-k with a
layer-cycled 1D/2D/3D partition and a per-head cumulative threshold. VMoBA
also retrains MoBA as a baseline on Wan 2.1-1.3B. At 55K tokens, MoBA at
density 0.25 keeps Imaging Quality near full attention (63.73 against
69.49) but its Dynamic Degree falls to 5.80% against 61.58%, so its videos
are nearly static. It costs 226 against 276 GPU hours, where VMoBA costs
187 and keeps Dynamic Degree at 56.91%. At 141 frames MoBA's Dynamic Degree
is 11.97 against 43.01. In VMoBA's training-free table at 33K tokens MoBA
is slower than full attention (126 s against 103 s). VMoBA attributes this
to the number of 1D blocks. VMoBA credits the motion collapse to MoBA's 1D
partition, but its MoBA arm changes the selection rule too, so that
attribution is not isolated.

VSA (LIT-tmp5vqlh) names MoBA as one of its two inspirations (App. E)
without running it. It keeps the mean-pooled coarse stage. It also feeds
that stage's attention output into the result, where MoBA uses it only to
route. It moves from MoBA's variable-length gather to fixed 64-token tiles,
because the gather pushes MoBA to large blocks (512 in VSA's example).

For the record's questions about video block-sparse attention, MoBA is the
1D baseline. Its blocks are contiguous runs of tokens. Block size is fixed,
not chosen from content. Selection is per-query top-k. Its one block-size
ablation (Fig. 4) is in text, at matched sparsity, and favours finer
blocks. It has no top-p arm and no comparison of trained against untrained
use of the same gate. It mentions Quest as a training-free relative that
"can be viewed as MoBA" with smaller blocks and min/max pooling.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and Appendix A. Figs. 2–5, 7 and 8 are curves and heat maps, and only
values stated in the text and in Tables 1–3 are quoted. The crossover
compute and the causal block-row count are this note's arithmetic, not the
paper's.
