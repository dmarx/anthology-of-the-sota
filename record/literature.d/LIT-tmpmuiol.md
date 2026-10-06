---
status: Active
title: 'VMoBA: Mixture-of-Block Attention for Video Diffusion Models'
version: 1
tags:
- attention-techniques
- generative-modeling
- adaptation-and-tuning
- inference-optimization
date: '2026-10-06'
published: '2025-06-30'
arxiv: '2506.23858'
first_author: 'Wu'
keywords:
- 'mixture-of-block-attention'
- 'sparse-attention'
- 'video-diffusion-models'
- 'layer-wise-recurrent-block-partition'
- 'global-block-selection'
- 'threshold-based-block-selection'
- 'long-sequence-training'
implementations:
- 'VMoBA (KwaiVGI, github.com/KwaiVGI/VMoBA)'
summary: >-
  Wu, Hou, Yang et al., Peking University and Kuaishou Kling (2025),
  [ARXIV-2506.23858](https://arxiv.org/abs/2506.23858). Adapts MoBA's trainable block-sparse attention to video
  DiTs. Key blocks are cut along time, space or both in a fixed 1D-2D-3D
  cycle over layers. Each head keeps the highest query-block scores from
  its whole score map until their cumulative share reaches τ = 0.25.
  Fine-tuning Wan 2.1-1.3B at 55K tokens for 2,000 steps, it takes 187
  against 276 GPU hours and averages 68.34 against 68.25 on five VBench
  dimensions. That mean is lifted by consistency scores that reward less
  motion, and VMoBA's Dynamic Degree is lower than full attention's. The
  pretrained model scores 68.27 untouched. Every number is one run, and
  the partition ablation never tests a single shape alone.
# MoBA is the method it adapts (the parameter-free mean-pooled gate) and its
# main trained baseline; DiTFastAttn is one of its two training-free
# baselines (Tables 1-2).
extends:
- LIT-tmpvcvo8
compared_against:
- LIT-tmpbgw07
- LIT-tmpe78xc
- LIT-tmpvcvo8
- LIT-tmp04qx6
---

# LIT-tmpmuiol: VMoBA: Mixture-of-Block Attention for Video Diffusion Models

Wu, Hou, Yang, Tao, Tian, Wan, Zhang and Tong, Peking University and Kling
Team, Kuaishou Technology (2025) — [ARXIV-2506.23858](https://arxiv.org/abs/2506.23858). Read at v1 (30 Jun
2025), the only version, main text and Appendices A–D.

## Key takeaways

- **What it starts from** (§1, Fig. 1a). MoBA (LIT-tmpvcvo8) flattens the sequence, cuts it into uniform 1D blocks,
  mean-pools each key block, and lets each query attend to its own block
  plus its top-k scoring blocks. Applied directly to fine-tuning Wan 2.1,
  it drops the five-dimension VBench mean from 68.25 to 56.88. Almost all of
  that drop is Dynamic Degree: 5.80% against 61.58% (Table 2). The videos
  are nearly static.
- **Three partitions, cycled by layer** (§3.2, Eq. 1, Table 4). Layer l uses
  a temporal partition when l mod 3 = 0, spatial when l mod 3 = 1, and
  spatio-temporal when l mod 3 = 2. The assignment is fixed by layer index.
  It is not chosen from content, and the paper offers it as a cheaper
  alternative to per-head classification of the kind Sparse VideoGen does.
  The shapes are very different in size. At 93×576×1024 (latent
  24×36×64, 55K tokens) a temporal block is 3 latent frames of the whole
  36×64 grid (6,912 tokens, 8 blocks). A spatial block is a 6×8 tile through
  all 24 frames (1,152 tokens, 48 blocks). A spatio-temporal block is
  8×12×8 (768 tokens, 72 blocks). The motivation is three Wan 2.1-1.3B
  layers whose block attention maps look temporal (layer 27), spatial
  (layer 3) and 3D-local (layer 20) (Fig. 3). Because the temporal block
  spans whole frames, it is a contiguous run in frame-major raster order.
  It differs from MoBA's 1D blocks by aligning to frame boundaries and by
  being far larger.
- **Selection is global per head, with a cumulative threshold** (§3.3–3.4,
  Eqs. 3–4). For each head, the method scores every query token against
  every mean-pooled key block (an s × N_b matrix). It sorts the whole
  matrix, then keeps pairs from the top until their normalized cumulative
  score reaches τ. So the number of blocks a query receives varies with
  that query and with how concentrated the head is. This is a top-p rule
  on a per-head pool, not a per-query top-p. Its motivation is Fig. 4, where
  queries differ in their top-25% similarity mass, and Fig. 5, where two
  heads need about 25,000 different numbers of query-block pairs to reach
  50% of the mass. τ = 0.25 throughout, and the resulting token density
  is 0.18–0.19 in training (Table 2).
- **Training at longer sequences** (Table 2; 2,000 steps on Koala-36M, same
  data for every arm, 1.3B model). These are the main results.
  - 93×576×1024, 55K tokens. Full attention: 24.61 / 61.58 / 94.69 / 69.49
    / 90.86 (TextConsis / Dynamic / BGConsis / ImageQual / SubConsist), 276
    GPU hours. VMoBA: 25.88 / 56.91 / 96.76 / 67.45 / 94.72, 187 GPU hours
    (1.48×), 2.83× fewer FLOPs. MoBA: 23.06 / 5.80 / 97.60 / 63.73 / 94.30,
    226 GPU hours.
  - 141×480×832, 56K tokens. Full attention: 23.92 / 43.01 / 92.30 / 64.36
    / 92.58, 262 GPU hours. VMoBA: 23.71 / 31.36 / 93.06 / 67.66 / 93.78,
    182 GPU hours (1.44×), 2.92× fewer FLOPs.
- **Speed depends on length** (Table 5, App. D, Fig. 1b). At 33K tokens
  VMoBA trains in the same 104 GPU hours as full attention despite 1.90×
  fewer FLOPs. At 13K it is slower (103 against 88 GPU hours). The authors
  put this down to scattered memory access in the FlashAttention-based
  implementation. In training-free inference it is 1.01× at 33K tokens and
  1.35× at 76K (Table 1). Fig. 1b fits quadratics through measured
  latencies to extend the trend.
- **Partition ablation** (Table 3a, 55K-token training setting, DD / IQ /
  SC / time). Each arm drops one of the three shapes from the cycle:
  - 1-2D: 55.49 / 58.51 / 86.12, 176
  - 1-3D: 28.57 / 66.71 / 91.34, 187
  - 2-3D: 57.01 / 66.02 / 94.75, 202
  - 1-2-3D: 56.91 / 67.45 / 94.72, 187

  Removing 3D costs the most image quality and subject consistency.
  Removing 2D halves Dynamic Degree. Removing 1D changes little in quality
  but costs 8% more time, since 1D layers have the fewest blocks. No arm
  uses one shape in every layer: there is no 3D-only arm, though §3.2
  claims the cycle is more efficient than uniform 3D, and no 1D-only arm
  that would isolate partition from MoBA's selection rule.
- **Selection ablation** (Table 3b, same setting). The arms cross top-k
  against threshold and local (per query) against global (per head):
  - top-k + local: 54.87 / 65.59 / 91.64
  - threshold + local: 55.19 / 65.31 / 92.43
  - top-k + global: 55.29 / 64.58 / 92.86
  - threshold + global: 56.91 / 67.45 / 94.72

  Each change alone moves the metrics by about a point and IQ not at all.
  Combined, they gain 2–3 points. The table gives no sparsity or time for
  these arms, so it does not show whether they ran at equal density.
- **Threshold and block count** (Tables 3c–3d). Raising τ from 0.15 to 0.50
  raises density from 0.13 to 0.39 and training time from 162 to 378. IQ
  rises monotonically (66.82 to 68.17), and DD and SC do not. Block counts
  of 24-48-144 against the default 8-48-72 score better on DD and IQ
  (57.70 / 68.60) at 222 against 187.
- **Training-free use is a different method** (App. A, Table 4). The
  training-free rows of Table 1 use VMoBA's partitions with MoBA's local
  top-k selection (k = 2/6/18 at 33K). The authors found that VMoBA's own
  selection "will cause vibration effects" without training.
- **Pre-training from scratch** (App. C, Fig. 7). Models of 5.6M to 526M
  parameters, Wan architecture, every self-attention layer replaced. At 11K
  tokens VMoBA's validation loss stays above full attention's, and the gap
  narrows with size. At 46K tokens the curves overlap. These results are
  shown only as curves.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **"Comparable or superior to full attention" is a five-metric mean that
  favours less motion.** At 55K tokens VMoBA is below full attention on
  Dynamic Degree (56.91 against 61.58) and Imaging Quality (67.45 against
  69.49). It is above on Background and Subject Consistency, which also
  reward static output: MoBA, with 5.80% Dynamic Degree, has the highest
  Background Consistency in the table (97.60). The pretrained Wan 2.1, not
  fine-tuned at all, averages 68.27, between full attention (68.25) and
  VMoBA (68.34). At 141 frames VMoBA's Dynamic Degree is 31.36 against
  43.01. The "3.3% better Image Quality" there is 3.3 points, 67.66 against
  64.36.
- **The abstract combines two rows.** "2.92x FLOPs and 1.48x latency
  speedup" takes the FLOPs from the 141-frame row (whose training speedup
  is 1.44×) and the speedup from the 576×1024 row (whose FLOPs ratio is
  2.83×). The "latency" is training GPU hours.
- **The partition ablation removes one shape at a time but never tests a
  single shape.** The claim that cycling beats uniform 3D partitioning is
  argued from block counts in §3.2. Table 3a has no arm to check it. The
  vanilla MoBA arm differs from VMoBA in partition and in selection at
  once, so the big Table 2 gap, Dynamic Degree 5.80 against 56.91, cannot
  be assigned to the 3D partition. The paper's text does assign it there
  (§4.2).
- **The selection rule is under-specified.** Eq. 4 accumulates
  "normalized" similarity, but the paper does not say how raw dot products,
  which can be negative, are normalized. Global selection can in principle
  leave a query with no key block. The paper does not say whether the
  local own-block rule from MoBA is kept, and Table 3b treats "local" and
  "global" as alternatives.
- **No variance anywhere.** Single runs throughout, and the ablation
  differences are often about a point (Table 3b). The τ sweep is not
  monotone in DD or SC, so the noise floor may be of that order.
- **Only five of VBench's dimensions**, on prompts rewritten by an LLM
  for the training runs (§4.1). Fine-tuning itself lowers TextConsis for
  every method against the pretrained model (Table 2), and at 33K full
  attention's Dynamic Degree jumps from 73.45 to 98.43 (Table 5). The
  2,000-step fine-tunes therefore move these metrics as much as the
  attention choice does.
- **The training-free baselines run at a different density.** DiTFastAttn
  and SVG keep 0.50 of attention, and VMoBA keeps 0.18–0.31.

## Which comparisons are like for like

- **Table 2 and Table 5** fine-tune full attention, MoBA and VMoBA from the
  same Wan 2.1-1.3B checkpoint on the same data for 2,000 steps. The
  DiTFastAttn and SVG rows are those methods applied at inference to the
  fine-tuned full-attention model, at 0.50 density. They are not
  trained.
- **Table 3** ablations all run in the 55K-token training setting. Table 3a
  and 3c–3d report time, and Table 3b does not report time or density.
- **Table 1** compares training-free methods on the pretrained model, but
  its VMoBA row uses MoBA's selection rule (App. A). It is evidence about
  the 3D partition at inference, not about the method that was trained.
- No experiment holds the selection rule fixed and compares trained against
  untrained.

## Standing in the anthology

The record's first adaptation of MoBA to video, and one of its earliest
trainable sparse attention papers for video diffusion. MoBA itself is not
in the record. It sits beside [SOTA-138](../practices.d/SOTA-138.md), which recommends training sparse
attention natively from DeepSeek's language-model work. VMoBA takes the
same route for video: it fine-tunes a dense checkpoint with sparsity on and
reports training savings. It does not warm up a learned indexer, and
selection uses mean-pooled block scores. Its pre-training curves (App. C)
are small-scale evidence that a sparse model trained from scratch tracks
dense loss at long sequence lengths, similar to what Native Sparse Attention
([LIT-143](LIT-143.md)) reports for text.

Two later papers in the record pick up its parts. SpargeAttention2
([LIT-tmpbgw07](LIT-tmpbgw07.md)) retrains VMoBA as a baseline on Wan 2.1 at 90% sparsity
and uses a per-query union of top-k and top-p. On Wan 2.1-1.3B at 480p,
SpargeAttention2's tables put VMoBA at Imaging Quality 65.31 against
63.67 for full attention, VQA-a 78.99 against 81.28, and attention time
36 s against 97 s on an RTX 5090. That gives an outside check that VMoBA
stays near full attention once trained. VMoBA's per-head threshold
is an earlier cumulative-mass rule of that family. SpargeAttention2 argues
that a cumulative-mass rule alone fails on rows dominated by attention
sinks, which VMoBA's Table 3b does not test, since its threshold arms are
never compared with a top-k floor added. Prism ([LIT-tmpe78xc](LIT-tmpe78xc.md)) varies block shape by content, per zone,
head and layer. VMoBA already used three anisotropic block shapes (whole
frame slabs, full-length spatial columns and cubes), fixed by layer index.
Prism's dynamic shape is therefore new in being content-chosen, not in
being anisotropic.

The base model is Wan 2.1-1.3B ([LIT-619](LIT-619.md)), unchanged except for the
attention. The kernel is built on FlashAttention ([LIT-074](LIT-074.md)).

It extends MoBA (LIT-tmpvcvo8), whose parameter-free gate it keeps: each key
block is scored by its mean-pooled key, and the mixture-of-block framing is
unchanged. It replaces MoBA's uniform 1D partition with a layer-cycled
1D/2D/3D partition, and MoBA's per-query top-k with a per-head cumulative
threshold. MoBA retrained on Wan 2.1-1.3B at density 0.25 is its main
trained baseline. At 55K tokens MoBA holds Imaging Quality at 63.73, but its
Dynamic Degree collapses to 5.80% against 61.58% for full attention, at 226
against VMoBA's 187 GPU hours. The MoBA arm differs from VMoBA in both
partition and selection rule, so the motion collapse is not shown to come
from the 1D partition. DiTFastAttn (LIT-tmp04qx6) is one of its two
training-free baselines, run at a stated density of 0.50 without saying
which of its techniques or thresholds were used. It is the closest to the
dense output by PSNR at 33K tokens (22.67 against 16.00 for VMoBA, at 1.18×
against 1.01×). Applied without training to the fine-tuned full-attention
model at 55K tokens, it lowers Subject Consistency from 90.86 to 83.33.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and Appendices A–D. Figs. 1, 3–7 are images and curves, and only
values in the text and tables are quoted. No practice or theory is drawn
from it.
