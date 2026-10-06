---
status: Active
title: 'Prism: Dynamic Sparse Attention for Native 2K Joint Video-Audio Generation Model Training'
version: 1
tags:
- attention-techniques
- generative-modeling
- multimodal-learning
date: '2026-10-06'
published: '2026-10-04'
arxiv: '2610.05416'
first_author: 'Tu'
keywords:
- 'block-sparse-attention'
- 'trainable-sparse-attention'
- 'dynamic-block-shape'
- 'top-k-top-p-selection'
- 'joint-video-audio-generation'
- 'native-high-resolution-training'
- 'diffusion-transformer'
implementations:
- 'Prism (Tencent Hunyuan)'
# MOVA is the backbone it is initialized from and modifies; LongCat-Video's
# block sparse attention is the mechanism it says it "builds on" (§1).
extends:
- LIT-tmpmipjh
- LIT-tmpid6gf
# Tables 1, 2, 5: every open joint model, sparse-attention method and
# high-resolution method it retrained or ran on its 2K data.
compared_against:
- LIT-tmpmipjh
- LIT-tmpkvsya
- LIT-tmpouvmz
- LIT-tmpngzke
- LIT-tmpid6gf
- LIT-tmp5vqlh
- LIT-tmp1ecle
- LIT-tmpmuiol
- LIT-tmpbgw07
- LIT-tmpucn4v
- LIT-tmpx3dxt
- LIT-tmpqhnq9
- LIT-tmppxw6w
- LIT-tmpva88i
- LIT-tmp8ew94
summary: >-
  Tu, Tian et al., Fudan and Tencent Hunyuan (2026), [ARXIV-2610.05416](https://arxiv.org/abs/2610.05416).
  Block-sparse video self-attention for a 16B joint video-audio DiT
  fine-tuned at 2K. Each 8×8×8 zone of tokens gets a block shape chosen from
  feature variance along each axis and from how strongly audio
  cross-attention touches it. Selection is SpargeAttention2's union of
  top-k (5% of blocks) and top-p (0.2), uncredited. Per-step training time is 10.6 against 26.5 minutes for
  full attention, and Prism scores better than full attention on every
  metric of its own 2K benchmark (aesthetic 0.61 against 0.42, cpCER 0.187
  against 0.374). Every number is one run, and Prism trained a fixed 5
  epochs while competitors trained "until convergence". At 480p full
  attention wins.
---

# LIT-tmpe78xc: Prism: Dynamic Sparse Attention for Native 2K Joint Video-Audio Generation Model Training

Tu, Tian, Huang, Wu, Han, Pan, Kong, Xiong, Zhang, Wu and Jiang, Fudan
University, Tencent Hunyuan and Zhejiang University (2026) —
[ARXIV-2610.05416](https://arxiv.org/abs/2610.05416). Read at v1 (4 Oct 2026), the only version, main text and
Appendices A.1–A.19.

## Key takeaways

- **The setting** (§3, Fig. 4, App. A.6). The backbone is MOVA, a
  dual-branch video and audio DiT with a Wan2.2-style high-noise and
  low-noise expert pair. Video self-attention is replaced with block-sparse
  attention, while audio self-attention and all cross-attention stay dense.
  Fine-tuning is 5 epochs on 100k filtered 2K clips (8–12 s at 24 fps, about
  870K tokens for 10 s), with only the attention modules trainable, on 160
  H800s.
- **Block shape follows content** (§3.1, App. A.4). The token grid is cut
  into 8×8×8 macro-zones. In each zone, per head and per layer, the method
  measures how much the value features vary along T, H and W, and adds an
  audio term gated by audio-to-video cross-attention norm. That term is taken
  from the previous layer because the current one has not run yet. A density
  score picks the block size (64, 128 or 256 tokens). Minimizing a per-axis
  mean-pooling loss under a fixed volume gives edge lengths proportional to
  g_d^(−1/2), and these are quantized to one of 16 shapes. Fast-varying axes
  get short edges.
- **Selection adapts per query** (§3.2, Table 7). Key blocks are scored by
  mean-pooled dot products, and each query keeps the union of the top 5% and
  the smallest set reaching 0.2 cumulative weight. On MotionQ, top-k alone
  scores 0.61, top-p alone 0.37, and the union 0.89, at 10.6 against 9.8
  minutes per step. The rule is not Prism's. SpargeAttention2
  ([LIT-tmpbgw07](LIT-tmpbgw07.md)) defined the same union over a mean-pooled block softmax,
  with the same p = 0.2, eight months earlier. Prism's related work credits
  that paper only with "a distillation objective".
- **Against other attention schemes at 2K** (Table 2). Every trainable
  method was retrained on the same data. Prism scores 0.61 aesthetic quality,
  0.63 DeSync and 0.89 MotionQ. The best of the rest, SpargeAttn2, scores
  0.47 / 0.90 / 0.61, full attention 0.42 / 1.05 / 0.53, and plain block-sparse
  attention 0.33 / 1.36 / 0.34. The two training-free methods, applied to
  the full-attention model, score below it.
- **The resolution ladder** (Table 12). Full attention leads at 480p (AQ 0.56
  against 0.54) and gets worse as resolution rises (0.42 at 2K). Prism is
  the only method that improves on every metric from 480p to 2K.
- **Cost** (Tables 5, 13). Per-step training time is 10.6 against 26.5
  minutes, 2.5×. Inference for a 10 s 2K clip on four H800s takes 331 s
  against 1,091 s, at 38.0 against 72.8 GB per GPU. Shape assignment and
  block scoring are 13.6% of inference time.

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **Training budgets differ by construction.** Prism trains for a fixed 5
  epochs at a learning rate of 1e−5. "All competitors and ablated variants
  are instead trained until their own loss converges" (App. A.6). The paper
  does not say how many steps that took, or whether the competitors also
  froze everything but attention.
- **"Surpassing full attention" rests on a full-attention model that gets
  worse with more resolution.** Trained on the same clips resized, full
  attention scores AQ 0.56 at 480p and 0.42 at 2K, and its loss curve at 2K
  is spiky with a rising audio loss (App. A.11). The paper's explanation is
  attention diluted across redundant tokens, shown with attention maps
  (App. A.12). A full-attention 2K fine-tune that did not converge well
  would look the same. No hyperparameter search for the full-attention
  baseline is reported.
- **Much of the gain over block-sparse baselines does not need dynamic
  shapes.** Inside Prism's own pipeline, a fixed isotropic 4×4×4 block
  scores AQ 0.55 and MotionQ 0.77 (Table 9). The plain block-sparse baseline
  scores 0.33 and 0.34 (Table 2), and dynamic shapes 0.61 and 0.89. So
  between the baseline and Prism, most of the gap opens before block shape
  varies at all, in the selection rule, block size or training setup. The
  paper does not separate them.
- **The selection ablation does not hold sparsity fixed, and the earlier one
  did.** Table 7's union adds blocks to top-k alone (9.8 against 10.6
  minutes per step), so its margin mixes the rule with the budget.
  SpargeAttention2 ([LIT-tmpbgw07](LIT-tmpbgw07.md)) calibrated its single-rule arms to near
  the union's sparsity. On a 1.3B Wan model it found the union only slightly
  ahead of top-k alone, and behind it on one metric.
- **Most of what Prism presents as new has precedents among its own
  baselines.** SpargeAttention v1 ([LIT-tmpxwbvb](LIT-tmpxwbvb.md)) acted on the diagnosis
  first, that a mean cannot represent a block of dissimilar tokens, by
  computing such blocks densely, and it already selected by top-p over a
  mean-pooled block map. Sparse VideoGen2 ([LIT-tmpucn4v](LIT-tmpucn4v.md)) answered the same
  diagnosis with content-defined k-means clusters. Sparse VideoGen
  ([LIT-tmpms9qj](LIT-tmpms9qj.md)) already chose an anisotropic window per head and step from
  content, between two fixed patterns.
  VMoBA ([LIT-tmpmuiol](LIT-tmpmuiol.md)) already varied block shape, cycling temporal slabs,
  spatial columns and 3D cubes by layer. Sliding Tile Attention
  ([LIT-tmp1yfvi](LIT-tmp1yfvi.md)) and VSA ([LIT-tmp5vqlh](LIT-tmp5vqlh.md)) already used fixed 4×4×4 cubes laid
  out as kernel tiles, the same cube as Prism's "Fixed 4³" ablation.
  LongCat-Video ([LIT-tmpid6gf](LIT-tmpid6gf.md)) tried a top-p rule before dropping it for
  load imbalance. What remains Prism's own is choosing each zone's shape
  from feature variance and audio coupling.
- **Two baselines' budgets are mislabelled.** Table 2 calls its "Base
  Sparsity" column "the Top-k budget", but Sparse VideoGen2 selects by top-p
  and Sol-Attn ([LIT-tmpx3dxt](LIT-tmpx3dxt.md)) by a mean-plus-deviation threshold. Neither
  uses top-k.
- **No variance anywhere.** More than forty ablation rows, and every one is
  below the full method on nearly every metric. Small changes move MotionQ a
  lot. α = 1 against the derived α = 1/2 gives 0.82 against 0.89, and top-p
  0.2 against 0.1 gives 0.89 against 0.74. Nothing says how much a reseed
  moves these numbers.
- **The headline benchmark is the authors'.** 2K-Bench (300 clips) was built
  to stress "the capabilities that native high-resolution training is
  specifically designed to improve". MotionQ is a score from Gemini 3.1. On
  the public 720p benchmarks the margins are smaller, which the authors
  attribute to less redundancy (Tables 3–4).
- **The backbone ablation is confounded.** "LTX-2.3 + Prism" beats LTX-2.3
  (Table 6), but the baseline is LTX-2.3's 720p-plus-upscaler pipeline. Its
  arm is therefore native 2K training and Prism together.
- **Commercial models are ahead on every metric** (Table 8): Wan3.0,
  Seedance2.5, Kling3.0 and MiniMax-H3, the last at 30B with an upsampling
  pipeline.

## Which comparisons are like for like

- **Table 2** retrains each trainable sparse method on the same 2K data from
  the same initialization, each at its own best sparsity. The training-free
  rows are the full-attention model with sparsity at inference only.
- **Table 12** derives every resolution from the same videos by resizing,
  and resizes outputs to 1080p for the resolution-sensitive metrics.
- **Tables 1 and 13** compare against other open models fine-tuned on the
  authors' 2K data, except LTX-2.3. Their full-attention MOVA row is the
  same model as Table 2's full-attention row.

## The comparisons, paper by paper

All numbers are Prism's, on its 2K-Bench unless marked, as aesthetic quality
(AQ, higher is better), DeSync (lower is better) and MotionQ.

- **Its backbone.** MOVA ([LIT-tmpmipjh](LIT-tmpmipjh.md)) is the dual-stream video-audio DiT
  that Prism initializes from and modifies. Fine-tuned at 2K with full
  attention, it is the "Full Attn" row everywhere: 0.42 / 1.05 / 0.53, at
  26.5 minutes per training step and 1,091 s per clip at inference.
- **The block-sparse mechanism it builds on.** LongCat-Video's block sparse
  attention ([LIT-tmpid6gf](LIT-tmpid6gf.md)) uses fixed-shape blocks, mean-pooled
  representatives and top-k selection. Retrained at 90% sparsity it scores
  0.33 / 1.36 / 0.34, the worst trainable row. Prism's fixed 4×4×4 variant
  scores 0.55 / 0.72 / 0.77, which is where most of the gap closes.
- **Other trainable sparse attention** (Table 2), each retrained on the same
  data: VSA ([LIT-tmp5vqlh](LIT-tmp5vqlh.md)) at 90% sparsity, 0.39 / 1.08 / 0.46.
  HunyuanVideo 1.5's selective and sliding tile attention ([LIT-tmp1ecle](LIT-tmp1ecle.md)) at
  85%, 0.43 / 0.97 / 0.54. VMoBA ([LIT-tmpmuiol](LIT-tmpmuiol.md)) at 90%, 0.46 / 0.91 / 0.59.
  SpargeAttention2 ([LIT-tmpbgw07](LIT-tmpbgw07.md)) at 95%, 0.47 / 0.90 / 0.61, the closest
  rival and the source of Prism's selection rule.
- **Training-free sparse attention** applied at inference to the
  full-attention model (Table 2): Sparse VideoGen2 ([LIT-tmpucn4v](LIT-tmpucn4v.md)) at 71%,
  0.35 / 1.28 / 0.38. Sol-Attn ([LIT-tmpx3dxt](LIT-tmpx3dxt.md)) at 85%, 0.40 / 1.11 / 0.47.
  Both are below the dense model they sparsify.
- **Other routes to high resolution** (Table 5). UltraGen ([LIT-tmp8ew94](LIT-tmp8ew94.md))
  scores 0.43 / 1.06 / 0.46. Prism lists it as training-free on the 720p
  model, but the published method is a 50-epoch fine-tune whose fusion
  layers and LoRA branches do not exist untrained. That row therefore does
  not measure UltraGen as published. LUVE
  ([LIT-tmppxw6w](LIT-tmppxw6w.md)), a cascade with frequency experts, scores 0.50 / 0.85 /
  0.62 at 18.7 minutes per step. Pyramidal Flow Matching ([LIT-tmpqhnq9](LIT-tmpqhnq9.md))
  scores 0.51 / 0.84 / 0.70 at 18.3 minutes. T3 ([LIT-tmpva88i](LIT-tmpva88i.md)), native 2K
  with multi-scale windows, scores 0.53 / 0.79 / 0.71 at 16.9 minutes.
- **Other open joint models** (Table 1), fine-tuned on the same 2K data
  except LTX: Ovi ([LIT-tmpouvmz](LIT-tmpouvmz.md)) 0.38 / 1.12 / 0.42, daVinci-MagiHuman
  ([LIT-tmpngzke](LIT-tmpngzke.md)) 0.40 / 1.08 / 0.58, and LTX-2 ([LIT-tmpkvsya](LIT-tmpkvsya.md)), run as
  "LTX-2.3" through its own low-resolution-then-upscale pipeline, 0.48 /
  0.95 / 0.66.

Every row above was trained by Prism's authors "until convergence" with no
step counts. Each is one run.

## Standing in the anthology

It is the record's first trainable sparse attention paper for video
generation, and its first for joint video and audio. It is relevant to
[SOTA-138](../practices.d/SOTA-138.md), which recommends training sparse attention natively, warmed up
under dense attention, from DeepSeek's language-model work. Prism takes the
same route in a different modality. It starts from a dense model's weights
and fine-tunes with sparsity on, and in Table 2 both training-free methods
applied to the dense model score below the dense model itself. Its selection
uses mean-pooled block scores and no learned indexer, the rule
SpargeAttention2 introduced. It differs from that
practice in another way: it claims sparsity is *better* than dense at 2K,
not just cheaper. That claim rests on the under-specified dense baseline
above, so it is not evidence for the practice's warm-up step or against
dense attention.

It is a different design from the record's other sparse attention lines.
Native Sparse Attention ([LIT-143](LIT-143.md)) and the Sparse Transformer's factorized
patterns ([LIT-225](LIT-225.md)) attend over blocks or strides of a fixed shape. Here the shape of the
block is the variable, chosen per zone, head and layer from the content. The
Table 9 comparison above suggests the shape matters less than the selection
rule wrapped around it. Prism's fixed 4×4×4 arm uses VSA's exact cube, and
it scores 0.55 / 0.72 / 0.77 against VSA's row at 0.39 / 1.08 / 0.46. So
that gap is selection rule, gated coarse output and sparsity, not block
shape. Prism does not separate them.

The backbone descends from Wan ([LIT-619](LIT-619.md)) through MOVA's high-noise and
low-noise experts. The objective is rectified-flow velocity matching
([LIT-636](LIT-636.md)). Neither is changed here. Prism alters only which video tokens
each query sees.

Filed without a NOTE: the takeaways come from one full reading of v1, main
text and Appendices A.1–A.19. Figs. 13–31 are images and curves, and only
values in the text and tables are quoted. No practice or theory is drawn
from it. The paper's account of why dense attention degrades at 2K
(attention diluted across redundant tokens) has no test that could come out
the other way, so it is not filed as a theory.
