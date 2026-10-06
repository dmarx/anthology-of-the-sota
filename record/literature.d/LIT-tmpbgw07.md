---
status: Active
title: 'SpargeAttention2: Trainable Sparse Attention via Hybrid Top-k+Top-p Masking and Distillation Fine-Tuning'
version: 1
tags:
- attention-techniques
- inference-optimization
- generative-modeling
- adaptation-and-tuning
date: '2026-10-06'
published: '2026-02-13'
arxiv: '2602.13515'
first_author: 'Zhang'
keywords:
- 'trainable-sparse-attention'
- 'block-sparse-attention'
- 'hybrid-top-k-top-p-masking'
- 'velocity-distillation'
- 'video-diffusion'
- 'attention-sinks'
implementations: []
# Tables 4-5 run VSA and VMoBA as trainable baselines on Wan2.1 at 90%
# sparsity, against SpargeAttention2 at 95%.
compared_against:
- LIT-tmp5vqlh
- LIT-tmpmuiol
summary: >-
  Zhang, Jiang, Xiang et al., Tsinghua and UC Berkeley (2026), ARXIV-2602.13515.
  Block-sparse attention for video diffusion. Each query block keeps the union
  of the top k% key blocks and the smallest set reaching p cumulative weight on
  a mean-pooled block attention map (k = 0.03, p = 0.2 or 0.16). It is then
  fine-tuned for 500 steps to match a frozen full-attention teacher's
  velocity. On Wan2.1 at 95% sparsity it matches the original model on VBench
  and VQA metrics, with attention 16.2× faster. The union beats Top-p alone by
  a wide margin. Top-k alone comes close at 1.3B and beats the union on one
  metric. Every number is one run.
---

# LIT-tmpbgw07: SpargeAttention2: Trainable Sparse Attention via Hybrid Top-k+Top-p Masking and Distillation Fine-Tuning

Zhang, Jiang, Xiang, Feng, Hu, Xi, Chen and Zhu, Tsinghua University and UC
Berkeley (2026) — ARXIV-2602.13515. Read at v1 (13 Feb 2026), the only
version, main text and Appendices A–B.

## Key takeaways

- **The masker, exactly** (§2.2, §4.1 Eq. 9, Alg. 1). Q is cut into blocks of
  bq = 128 consecutive tokens and K, V into blocks of bkv = 64 (App. A). Each
  block is mean-pooled. The pooled map is P̄ = softmax(Q̄K̄ᵀ/√d), one row per
  query block. Top-k keeps the k% largest entries of a row. Top-p keeps the
  minimal prefix of the row, sorted in descending order, whose sum is at
  least p. The block mask is M̄ᵢⱼ = 1 iff j ∈ Top-k(P̄ᵢ, k%) ∪ Top-p(P̄ᵢ, p%).
  Selected blocks then run through a FlashAttention-style online-softmax loop
  (Alg. 1), with mask construction and the forward and backward passes in
  CUDA (§4.3). The settings are k = 0.03 with p = 0.2 for Wan2.1-1.3B at
  480p, and k = 0.03 with p = 0.16 for Wan2.1-14B at 720p, calibrated to
  about 95% sparsity (App. A).
- **Why a union** (§3.2 Case 1, Table 1). If a row is near-uniform, a fixed k
  captures little probability mass. If a row is skewed, Top-p can reach its
  threshold on attention-sink blocks alone. The paper's example is a row of
  [0.6 (sink), 0.2, 0.1, …] with p = 60%. Its evidence is two hand-picked P
  matrices at equal sparsity, relative L1 error of output. On the uniform one
  the errors are Top-k 0.4150, Top-p 0.3726 and the union 0.3707. On the
  skewed one they are 0.1664, 0.2160 and 0.1671. The union tracks whichever
  single rule is better. It does not beat both.
- **Masker ablation** (Table 6, App. A). The single-rule arms are calibrated
  to near-equal sparsity. Top-k alone uses k = 0.05 for about 95%. Top-p
  alone uses p = 0.4 at 1.3B (94%) and p = 0.3 at 14B (93%). At 1.3B the
  scores are IQ / OC / AQ / VR / VQA:
  - union: 67.68 / 21.57 / 65.05 / 0.1010 / 86.73
  - Top-k only: 65.84 / 21.51 / 64.57 / 0.0916 / 86.90
  - Top-p only: 60.56 / 21.12 / 60.12 / 0.0312 / 62.57

  At 14B (100 training steps):
  - union: 68.41 / 21.06 / 65.02 / 0.1119 / 88.22
  - Top-k only: 65.24 / 20.64 / 63.99 / 0.0935 / 84.25
  - Top-p only: 63.37 / 21.33 / 63.62 / 0.1090 / 86.43

  Top-p alone collapses at 1.3B. Top-k alone is the close competitor there.
- **Trained against training-free, same masker** (Table 6). The
  "Training-free" arm uses the same sparse attention with no fine-tuning. At
  1.3B it scores IQ 53.18, AQ 48.93 and VQA 20.40, against 67.68, 65.05 and
  86.73 trained. At 14B it scores 62.17, 57.01 and 45.85, against 68.41,
  65.02 and 88.22. §3.2 Case 2 (Fig. 3, Table 2) offers a mechanism. After
  sparse fine-tuning, the share of entries needed to reach 60% of the mass
  rises from 51.3% to 56.9% sparsity, and L1 error at that sparsity falls
  from 0.4901 to 0.4119. This is one heatmap pair.
- **Distillation instead of the diffusion loss** (§3.2 Case 3, §4.2, Tables
  3 and 6). With full attention, fine-tuning on the authors' 3,000-clip
  private set lowers every metric. At 1.3B, AQ goes 0.6441 to 0.6183 and
  VQA-a 81.28 to 75.45. The proposed loss is ‖u_sparse(x_t) − u_full(x_t)‖²
  against a frozen full-attention copy, and the data is used only to build
  x_t. Replacing it with the diffusion loss ("–VD") costs AQ 65.05 to 63.34
  and VQA 86.73 to 85.05 at 1.3B.
- **Against other sparse methods** (Tables 4–5). Attention time is measured
  on an RTX 5090. On 1.3B/480p:
  - SpargeAttention2 (95% sparsity): IQ 67.68, VQA-a 83.86, attention 6 s,
    end to end 68 s
  - full attention: 63.67, 81.28, 97 s, 159 s
  - VMoBA (90%): 65.31, 78.99, 36 s
  - VSA (90%): 59.57, 33.35, 25 s
  - SLA (95%): 63.14, 72.66, 11 s
  - SpargeAttn v1 (89%): 35.28, 3.26

  On 14B/720p, attention goes from 2,550 s to 157 s (16.2×) and end to end
  from 3,043 s to 650 s (4.7×).

## Where the hedges are

Per DP-010:

- **"Consistently achieves the best" (§5.4) is not what Table 6 shows in
  every cell.** At 1.3B, Top-k alone has the higher combined VQA (86.90
  against 86.73). At 14B, Top-p alone has the higher OC (21.33 against
  21.06). The union's clear wins are over Top-p at 1.3B and over Top-k at
  14B. Table 1 supports the claim that it is "≈ best of the two" on two
  synthetic examples. It does not support "better than either".
- **No variance.** Every row in Tables 1–6 is one run, and the training set
  is 3,000 private clips. The 14B ablations ran 100 steps, while the
  headline ran 500 (App. A). That is why the union scores 68.41 IQ in
  Table 6 and 69.08 in Table 5.
- **The student beats its teacher on several metrics.** At 1.3B, IQ is 67.68
  against 63.67 for full attention, VQA-a 83.86 against 81.28, and VQA-t
  87.73 against 85.80. A velocity-distillation student whose only target is
  the full model's output gives no reason to expect that. The paper offers
  none, and with no seeds it cannot rule out noise in VBench-prompt scoring.
- **Baselines are not at the same sparsity, and their training is not
  described.** VSA and VMoBA run at 90% and SpargeAttention2 at 95%. The
  paper does not say whether the baselines got the same 500 steps, the same
  data or the distillation loss. They probably got their own diffusion loss,
  which Table 3 shows hurts on this data. If so, part of the gap is the
  objective, not the masker. SpargeAttn v1 is a training-free method listed
  among "trainable approaches" and run at 86–89% sparsity, far past its
  design point. Its near-zero VQA rows are not a meaningful comparison.
- **Attention time mixes kernels.** VSA at 90% takes 25 s and SLA at 95%
  takes 11 s. The speed comparison is partly between implementations on a
  consumer GPU, not between sparsity patterns.
- **Text and table disagree on the 14B baseline.** Table 3 gives the
  original 14B model VQA-t 87.51. Table 5's full-attention row gives 87.00
  for what should be the same model. Table 6's "VQA" is called a combination
  of VQA-a and VQA-t, but it is not their mean: 86.73 against a mean of
  85.80 at 1.3B.
- **The abstract's 4.7× is the 14B number.** At 1.3B the end-to-end speedup
  is 2.3×.

## Which comparisons are like for like

- **The masker ablation (Table 6) is the best-controlled result here.** Only
  the masker changes, and the single-rule arms are calibrated to 93–95%
  sparsity against the union's ~95%. That is closer to matched than most
  hybrid-selection ablations in this batch.
- **Training-free against trained (Table 6)** holds masker, sparsity and
  model fixed. It is a controlled answer to "does fine-tuning matter at 95%
  sparsity": yes, by a wide margin.
- **Tables 4–5** are not like for like, for the sparsity and training
  reasons above. VSA (LIT-tmp5vqlh) and VMoBA (LIT-tmpmuiol) are the trained
  baselines. At 1.3B, VMoBA is close to full attention (VQA-t 86.69, above
  it) at 90% sparsity, and VSA loses badly on alignment (VQA-a 33.35). At
  14B both are within a few points of full attention, and SpargeAttention2
  is ahead of both at a higher sparsity and shorter attention time.

## Standing in the anthology

It is the record's clearest source for **hybrid Top-k ∪ Top-p block
selection**. Its title names it, its Eq. 9 defines it, and it ran a roughly
sparsity-matched ablation of it. Prism (LIT-tmpe78xc) uses the same rule
eight months later: Top-k(Pᵢ, k) ∪ Top-p(Pᵢ, p) over a mean-pooled block
softmax, with p = 0.2 as here at 1.3B. Prism presents it as part of its own
method. Its related work describes SpargeAttention2 only as using "a
distillation objective". Prism's own Table 7 ablation of the rule does not
hold sparsity fixed (9.8 against 10.6 minutes per step). The Prism note's
claim that "the union is far better than either rule alone" should be read
against this paper, which got there first and found the union's margin over
Top-k small at 1.3B.

It bears on SOTA-138 without moving it. That practice trains sparsity
natively with a dense warm-up, following DeepSeek's language-model work
(LIT-142, LIT-143). This paper retrofits sparsity onto a dense
video model and supervises it with a frozen dense teacher rather than the
data loss. Its trained-against-training-free row is direct evidence that
adapting the weights to the mask matters at 95% sparsity. Its selector is
pooled dot products with no learned indexer. The teacher-student framing is
Hinton-style distillation (LIT-680), applied to the velocity field. The
Top-p failure it guards against is the attention-sink effect described for
language models in LIT-191.

Blocks are runs of consecutive tokens in the flattened sequence (bq = 128,
bkv = 64). The paper does not tile in 3D, does not choose block shape or
size from content, and does not discuss either. The backbones are Wan2.1
(LIT-619) at 1.3B and 14B, unmodified apart from attention.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and Appendices A–B. Figures 1–4 are images and only text and table
values are quoted. No practice is drawn from it yet. A practice on hybrid
selection would want a second group's sparsity-matched result.
